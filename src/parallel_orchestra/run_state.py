"""Persistent run-state for --resume support.

Saves the set of successfully completed task IDs to a JSON file alongside
the manifest so that a subsequent ``parallel-orchestra run --resume`` can skip
them and only execute the remaining tasks.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------


@dataclass
class RunState:
    """Mutable run-state persisted between invocations.

    Attributes:
        manifest_path: Absolute path to the manifest file (as a POSIX string).
        manifest_hash: SHA-256 hex digest of the manifest file contents at the
            time the state was first created.
        completed_tasks: Set of task IDs that have completed successfully.
        created_at: ISO 8601 timestamp of the initial state creation.
        updated_at: ISO 8601 timestamp of the most recent update.
    """

    manifest_path: str
    manifest_hash: str
    completed_tasks: set[str] = field(default_factory=set)
    created_at: str = field(default_factory=lambda: _utcnow_iso())
    updated_at: str = field(default_factory=lambda: _utcnow_iso())


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _utcnow_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _hash_manifest(manifest_path: Path) -> str:
    data = manifest_path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def _state_file_path(manifest_path: Path) -> Path:
    """Return the canonical path of the state file for *manifest_path*.

    Returns:
        Path to the ``.po-run-state-<stem>.json`` file.
    """
    stem = manifest_path.stem
    return manifest_path.parent / f".po-run-state-{stem}.json"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_run_state(manifest_path: Path) -> RunState | None:
    """Load the run-state file for *manifest_path* if it exists."""
    state_path = _state_file_path(manifest_path)

    if not state_path.exists():
        return None

    try:
        raw = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(
            f"Warning: --resume: failed to parse state file {state_path}: {exc}."
            " Falling back to normal run.",
            file=sys.stderr,
        )
        return None

    if not isinstance(raw, dict):
        print(
            f"Warning: --resume: state file {state_path} is malformed: "
            "expected a JSON object at top level. Falling back to normal run.",
            file=sys.stderr,
        )
        return None

    try:
        saved_hash: str = raw["manifest_hash"]
        completed_tasks: list[str] = raw.get("completed_tasks", [])
    except (KeyError, TypeError) as exc:
        print(
            f"Warning: --resume: state file {state_path} is malformed: {exc}."
            " Falling back to normal run.",
            file=sys.stderr,
        )
        return None

    current_hash = _hash_manifest(manifest_path)
    if saved_hash != current_hash:
        print(
            "Warning: --resume: manifest has changed since the last run"
            " (hash mismatch). Falling back to normal run.",
            file=sys.stderr,
        )
        return None

    return RunState(
        manifest_path=raw.get("manifest_path", str(manifest_path)),
        manifest_hash=saved_hash,
        completed_tasks=set(completed_tasks),
        created_at=raw.get("created_at", _utcnow_iso()),
        updated_at=raw.get("updated_at", _utcnow_iso()),
    )


def create_run_state(manifest_path: Path) -> RunState:
    """Create a fresh RunState for *manifest_path* and persist it."""
    manifest_hash = _hash_manifest(manifest_path)
    state = RunState(
        manifest_path=str(manifest_path),
        manifest_hash=manifest_hash,
    )
    _persist(state, manifest_path)
    return state


def state_file_path(manifest_path: Path) -> Path:
    """Return the canonical path of the state file for *manifest_path*."""
    return _state_file_path(manifest_path)


def mark_task_completed(state: RunState, task_id: str, manifest_path: Path) -> None:
    """Record *task_id* as completed and persist the updated state."""
    state.completed_tasks.add(task_id)
    state.updated_at = _utcnow_iso()
    _persist(state, manifest_path)


def delete_run_state(manifest_path: Path) -> None:
    """Delete the state file for *manifest_path* on a best-effort basis."""
    state_path = _state_file_path(manifest_path)
    try:
        state_path.unlink(missing_ok=True)
    except OSError as exc:
        print(
            f"Warning: run-state: failed to delete state file {state_path}: {exc}.",
            file=sys.stderr,
        )


def state_file_exists(manifest_path: Path) -> bool:
    """Return True if the state file for *manifest_path* exists on disk."""
    return _state_file_path(manifest_path).exists()


def _persist(state: RunState, manifest_path: Path) -> None:
    """Serialise *state* to JSON and write it to disk atomically."""
    state_path = _state_file_path(manifest_path)
    payload = {
        "manifest_path": state.manifest_path,
        "manifest_hash": state.manifest_hash,
        "completed_tasks": sorted(state.completed_tasks),
        "created_at": state.created_at,
        "updated_at": state.updated_at,
    }
    tmp_path = state_path.with_suffix(".tmp")
    try:
        tmp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(tmp_path, state_path)
    except OSError as exc:
        print(
            f"Warning: run-state: failed to persist state to {state_path}: {exc}."
            " --resume will not be able to skip this task on the next run.",
            file=sys.stderr,
        )
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass

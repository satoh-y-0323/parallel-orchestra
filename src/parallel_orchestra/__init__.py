"""parallel-orchestra: Run Claude Code agents in parallel."""

from ._exceptions import ParallelOrchestraError
from .manifest import (
    SUPPORTED_PLAN_VERSIONS,
    Defaults,
    Manifest,
    ManifestError,
    Task,
    WebhookConfig,
    load_manifest,
)
from .report import generate_report
from .runner import RunnerError, RunResult, TaskResult, run_manifest

__version__ = "0.1.0"

__all__ = [
    "ParallelOrchestraError",
    "SUPPORTED_PLAN_VERSIONS",
    "Defaults",
    "Manifest",
    "ManifestError",
    "Task",
    "WebhookConfig",
    "load_manifest",
    "generate_report",
    "RunnerError",
    "RunResult",
    "TaskResult",
    "run_manifest",
]

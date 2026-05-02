# Changelog

All notable changes to **parallel-orchestra** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.3] - 2026-05-03
### Security
- `read_only: true` tasks now receive `--read-only` instead of
  `--dangerously-skip-permissions`, scoping agent permissions to the
  declared intent.
- Webhook URLs are restricted to HTTPS only; `http://` schemes are now
  rejected at manifest parse time.
- Expanded `_BLOCKED_HOSTNAMES` to cover `localhost.localdomain`,
  `localhost4`, and `localhost6` (RHEL/CentOS `/etc/hosts` aliases) in
  addition to the previously blocked `localhost` and IPv6 variants.
- `ANTHROPIC_API_KEY` (and `ANTHROPIC_API_KEY_HELPER`) is now masked
  with `[MASKED]` in per-task log files before writing to disk.
- Per-task log directory is created with mode `0700`; log files are
  restricted to mode `0600` after each write.
- Unicode bidirectional-control and format characters (Unicode
  categories `Cf`/`Cc`) are stripped from dashboard display strings to
  prevent terminal UI spoofing.
- Run-state files larger than 1 MiB are rejected and ignored to prevent
  local memory exhaustion.

### Fixed
- `_copy_test_reports_from_worktree` removed; C3-specific report
  copying logic no longer lives in the PO core. Worktree inspection on
  failure is handled by `PO_KEEP_WORKTREE=1`.
- Dashboard is no longer started by default when `stderr` is not a TTY
  (e.g. CI environments); pass `--dashboard` to force-enable.
- `__version__` is now resolved dynamically from the installed package
  metadata (`importlib.metadata`) so it always matches `pyproject.toml`.
- `run_state.py` warning messages are emitted via `logging` instead of
  `print(file=sys.stderr)`, consistent with the project logging policy.
- `_write_task_logs` chmod failures are now logged at `WARNING` level
  instead of silently swallowed.
- Resumed multi-level dependency chains (`--resume` with A→B→C where A
  and B are already complete) now correctly propagate `_indegree`
  decrements in topological order.

## [0.1.2] - 2026-05-01
### Fixed
- Git subprocess invocations now explicitly use `encoding="utf-8"` with
  `errors="replace"`. On Windows, `text=True` alone fell back to the
  system code page (cp932 in Japanese locales), which made any git
  output containing non-ASCII bytes (commit messages, file names,
  localized error strings) crash the runner with `UnicodeDecodeError`.

## [0.1.1] - 2026-05-01
### Added
- `.github/workflows/publish.yml` — PyPI Trusted Publisher workflow.
  Builds sdist + wheel and uploads to PyPI through OIDC when a GitHub
  Release is published, so no PyPI API token has to live in repo
  secrets.

### Fixed
- CI's `pip-audit` step no longer fails on the in-tree editable install
  of the project itself. Adds `--skip-editable` and drops `--strict`
  so the audit reports only real third-party CVEs.

## [0.1.0] - 2026-04-30
### Added
- First public release.
- `parallel-orchestra run <manifest>` CLI driving Claude Code headless
  agents in parallel from a YAML-frontmatter Markdown manifest.
- Dependency-aware task scheduler (`depends_on`, `writes`,
  `concurrency_group`) plus skip propagation when a prerequisite fails.
- Read-only tasks run in place; write tasks run inside an isolated
  `git worktree`, are auto-committed, and merged back to the original
  branch on success.
- Failure classification (`transient`, `rate_limited`, `permanent`,
  `timeout`) with automatic retry. Defaults: 1 retry, 1.0s base delay,
  2.0x exponential backoff factor.
- ANSI progress dashboard with TTY auto-detection; `--dashboard` /
  `--no-dashboard` overrides.
- Per-task `stdout`/`stderr` log files (`--log-dir`, `--no-log`).
- Run summary report via `--report` (auto-detects `.json` / `.md`).
- `--resume` support backed by a `.po-run-state-*.json` file next to the
  manifest.
- `python -m parallel_orchestra` entry point in addition to the
  `parallel-orchestra` console script.
- `example/` mini-project demonstrating a parallel TDD workflow with
  `tdd-develop → tester → developer → tester` sub-agents.

[Unreleased]: https://github.com/satoh-y-0323/parallel-orchestra/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/satoh-y-0323/parallel-orchestra/releases/tag/v0.1.2
[0.1.1]: https://github.com/satoh-y-0323/parallel-orchestra/releases/tag/v0.1.1
[0.1.0]: https://github.com/satoh-y-0323/parallel-orchestra/releases/tag/v0.1.0

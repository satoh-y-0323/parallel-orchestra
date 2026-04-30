# Changelog

All notable changes to **parallel-orchestra** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/satoh-y-0323/parallel-orchestra/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/satoh-y-0323/parallel-orchestra/releases/tag/v0.1.1
[0.1.0]: https://github.com/satoh-y-0323/parallel-orchestra/releases/tag/v0.1.0

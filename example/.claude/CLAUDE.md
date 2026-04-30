# Example project for parallel-orchestra

This `example/` directory is a self-contained mini-project that exercises
parallel-orchestra's TDD workflow. The repository's headless agents are
defined under `.claude/agents/` and `.claude/skills/`, and `.claude/reports/`
holds the sample manifest used by the run.

To execute the example:

```bash
parallel-orchestra run example/.claude/reports/plan-report-tdd-example.md
```

The run spawns one isolated git worktree per task, drives the
`tdd-develop` conductor through `tester → developer → tester`, and merges
the resulting commits back into the current branch on success.

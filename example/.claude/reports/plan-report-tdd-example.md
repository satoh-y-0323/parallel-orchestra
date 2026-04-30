---
po_plan_version: "0.1"
name: "tdd-example"
cwd: "../.."

tasks:
  - id: tdd-addition
    agent: tdd-develop
    read_only: false
    prompt: |
      `example/src/addition.py` を tdd-develop の指示に従って実装してください。
      - 関数名: `add(a, b)` — 足し算
      - テスト: `example/tests/test_addition.py`

  - id: tdd-multiplication
    agent: tdd-develop
    read_only: false
    prompt: |
      `example/src/multiplication.py` を tdd-develop の指示に従って実装してください。
      - 関数名: `multiply(a, b)` — 掛け算
      - テスト: `example/tests/test_multiplication.py`
---

# TDD example: parallel addition / multiplication

This sample manifest exercises parallel-orchestra by driving two
independent TDD tasks in parallel, each through the `tdd-develop`
conductor. Run with:

```bash
parallel-orchestra run example/.claude/reports/plan-report-tdd-example.md
```

Both tasks run in their own git worktree, follow the
`worktree-tdd-workflow` skill (tester → developer → tester), and the
final implementations are auto-merged into the current branch on
success.

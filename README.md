# parallel-orchestra (PO)

複数の Claude Code ヘッドレスエージェントを **並列実行**し、結果を一つのブランチに**自動マージ**する CLI ツール。

`claude -p` を内部でオーケストレートし、書き込みタスクごとに独立した **git worktree** を確保するので、お互いの変更が衝突しません。タスクが終わると PO が auto-commit して main に取り込みます。

---

## できること

- 1 枚の Markdown マニフェスト（YAML フロントマター）から複数タスクを定義し、並列起動する
- 書き込みタスクは worktree に隔離 → 自動コミット → 完了後に元ブランチへマージ
- 失敗・タイムアウト・transient エラーをカテゴリ分けして、必要に応じて自動リトライ（デフォルト 1 回・1 秒バックオフ・係数 2）
- タスク間の依存関係（`depends_on`）と書き込みパスの宣言（`writes`）でスケジュールを最適化
- ANSI 進捗ダッシュボード、JSON / Markdown サマリレポート、レジューム機能（`--resume`）

---

## インストール

```bash
pip install parallel-orchestra
```

要件: Python 3.10+ / [Claude Code CLI](https://claude.ai/code) が `claude` コマンドとして PATH に通っていること。

### 開発版を入れたい場合

ソースから編集可能インストール:

```bash
git clone https://github.com/satoh-y-0323/parallel-orchestra.git
cd parallel-orchestra
pip install -e ".[dev]"
```

---

## 5 分で動かす

リポジトリ直下に `example/` という自己完結の雛形が入っています。

```bash
parallel-orchestra run example/.claude/reports/plan-report-tdd-example.md
```

これは以下を**並列で**実行します:

- `example/src/addition.py` の `add(a, b)` を TDD で実装
- `example/src/multiplication.py` の `multiply(a, b)` を TDD で実装

それぞれが独立した worktree で `tester → developer → tester` のサブエージェントを回し、テスト全件合格を確認してから main へマージされます。

---

## マニフェスト形式

```markdown
---
po_plan_version: "0.1"
name: "my-plan"
cwd: "."

tasks:
  - id: feature-a
    agent: developer
    read_only: false
    prompt: |
      実装してください: ...

  - id: feature-b
    agent: developer
    read_only: false
    depends_on:
      - feature-a
    prompt: |
      ...
---

# 自由記述の説明文

このセクション以降は人間向けのメモ。PO は読みません。
```

主なフィールド:

| フィールド | 必須 | 説明 |
|---|:--:|---|
| `po_plan_version` | ✅ | `"0.1"` 固定 |
| `name` | ✅ | プランの名前（ログ等に使われる） |
| `cwd` | ✅ | manifest からの相対パスで「プロジェクトの作業ディレクトリ」を指す。worktree のコピー元 `.claude/` もここから探す |
| `tasks[].id` | ✅ | `[A-Za-z0-9_-]+` |
| `tasks[].agent` | ✅ | `claude -p --agent <agent>` に渡される名前。`<cwd>/.claude/agents/<agent>.md` が定義 |
| `tasks[].read_only` | ✅ | `false` の場合 worktree が作られる |
| `tasks[].prompt` | | エージェントへの指示文 |
| `tasks[].depends_on` | | 先に成功している必要のあるタスク ID |
| `tasks[].max_retries` | | リトライ回数（未指定なら `defaults.max_retries`、それも無ければ 1） |
| `defaults.max_retries` | | manifest 全体のデフォルトリトライ回数 |

詳細な仕様は [`example/.claude/docs/parallel-orchestra-manifest.md`](example/.claude/docs/parallel-orchestra-manifest.md) にあります。

---

## CLI

```text
parallel-orchestra run <manifest_path> [options]
```

| オプション | 既定値 | 説明 |
|---|---|---|
| `--max-workers N` | 3 | 並列タスクの最大数 |
| `--claude-exe PATH` | `claude` | `claude` 実行ファイルの場所 |
| `--quiet` | off | 成功タスクの詳細出力を抑制 |
| `--log-dir PATH` | `<git-root>/.claude/logs` | per-task の stdout/stderr 保存先 |
| `--no-log` | off | per-task ログを保存しない |
| `--dry-run` | off | 計画だけ表示して実行しない |
| `--resume` | off | 前回成功タスクをスキップして再開 |
| `--report PATH` | – | `.json` / `.md` でサマリレポートを出力 |
| `--dashboard` / `--no-dashboard` | TTY 自動 | ANSI ダッシュボード強制 ON/OFF |

`python -m parallel_orchestra ...` でも同じ CLI が呼べます。

### 終了コード

| コード | 意味 |
|:--:|---|
| 0 | すべてのタスクが成功 |
| 1 | 1 つ以上のタスクが失敗 |
| 2 | マニフェストエラー |
| 3 | ランナーエラー（claude バイナリ不在など） |

---

## アーキテクチャ

```
parallel-orchestra run <manifest>
    │
    ├─ マニフェスト解析（manifest.py）
    │   └─ Task / Defaults / Manifest dataclass
    │
    ├─ DependencyScheduler（runner.py）
    │   └─ depends_on と writes に従って起動順を決定
    │
    └─ タスクごと:
        ├─ read_only=true  → cwd でそのまま claude -p を起動
        └─ read_only=false → git worktree を切り、.claude/ を複製
                              ↓
                              claude -p --agent <name> -p <prompt>
                              ↓
                              auto-commit
                              ↓
                              元ブランチへ merge
                              ↓
                              worktree cleanup
```

成功時のエージェント出力は worktree branch の auto-commit に乗って merge 経由で main に取り込まれます。失敗時は `PO_KEEP_WORKTREE=1` を設定することで worktree を保持して post-mortem 調査ができます。

---

## 環境変数

| 変数 | 用途 |
|---|---|
| `PO_KEEP_WORKTREE=1` | タスク終了後も worktree を残す（デバッグ用） |
| `PO_WORKTREE_GUARD` | 内部用。ユーザーは設定しない |

---

## 開発

```bash
pip install -e ".[dev]"
pytest                 # 185 件のユニット / 統合テスト
ruff check src tests
mypy src
```

`example/` を使ったエンドツーエンド検証:

```bash
parallel-orchestra run example/.claude/reports/plan-report-tdd-example.md
```

---

## ライセンス

未定（公開時に追記）。

---

## 関連

並列で動かす個々のエージェントを「どう書くか」「どうワークフローを定義するか」は本ツールの守備範囲外です。`example/.claude/agents/` と `example/.claude/skills/` に **TDD ワークフローの最小例**を含めているので参考にしてください。

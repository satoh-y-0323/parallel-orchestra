# parallel-orchestra (PO) — Moved

> [!IMPORTANT]
> **This repository has been merged into [claude-code-conductor (C3)](https://github.com/satoh-y-0323/claude-code-conductor) and is no longer maintained as a standalone project.**
>
> All future development happens inside the C3 repository.

## What changed

- PO のソースコード・テスト・example は C3 リポジトリの `src/parallel_orchestra/` および `tests/parallel_orchestra/` に取り込まれました。
- C3 のディストリビューション（`pip install claude-code-conductor`）に PO が同梱されているため、PO を別途インストールする必要はなくなりました。
- C3 は PO の Python API を直接呼び出すようになり、両者は密結合化しました。
- このリポジトリは GitHub Archive により読み取り専用です。Issue・PR は受け付けていません。

## Migration

### 旧（standalone PO）

```bash
pip install parallel-orchestra
parallel-orchestra run path/to/plan-report.md
```

### 新（C3 同梱）

```bash
pip install claude-code-conductor
c3 po run path/to/plan-report.md
# または後方互換のため `parallel-orchestra` コマンドも引き続き使用可能
parallel-orchestra run path/to/plan-report.md
```

両者の動作は同一です。`pip install parallel-orchestra` で入っていた古い 0.1.x が site-packages に残っている場合は、`pip uninstall parallel-orchestra` を実行してから C3 を導入してください。

## Where to file issues

PO 由来の挙動に関する報告・要望は **C3 リポジトリの Issues** へ:

→ https://github.com/satoh-y-0323/claude-code-conductor/issues

## License

MIT (unchanged). 旧コードのライセンスは git 履歴上保全されています。

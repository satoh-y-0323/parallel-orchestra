# Coding Standards

Python 3.11 + 標準ライブラリのみ（外部ライブラリ不使用）の CLI ツール向けコーディング規約。
PEP 8 に準拠する。

---

## インデント・行長

- インデントは **4スペース**（タブ禁止）
- 1行の最大長は **88文字**（コード）、**72文字**（コメント・docstring）
- 継続行は括弧内の要素に垂直揃え、またはハンギングインデント（4スペース追加）を使用する

```python
# OK: 垂直揃え
result = some_function(arg_one, arg_two,
                       arg_three, arg_four)

# OK: ハンギングインデント
result = some_function(
    arg_one, arg_two,
    arg_three, arg_four,
)
```

---

## インポート

- ファイル先頭（モジュール docstring の後）に記述する
- 1行につき1モジュール（`from X import A, B` は例外として許可）
- グループ順: **標準ライブラリ → サードパーティ → ローカル**（各グループを空行で区切る）
- ワイルドカードインポート（`from module import *`）は禁止
- 相対インポートより絶対インポートを優先する

```python
# OK
import os
import sys
from pathlib import Path
from typing import Optional

from myapp.utils import helper
```

---

## 空白

- 括弧・ブラケット・中括弧の直後/直前にスペースを入れない
- 二項演算子・比較演算子・論理演算子の前後に1スペース
- キーワード引数・デフォルト値の `=` 前後にスペースを入れない
- 型アノテーション付きデフォルト値の `=` 前後には1スペースを入れる

```python
# OK
x = 1
y = x + 1
func(arg=value)
def func(x: int = 0) -> None: ...

# NG
x=1
func( arg = value )
```

---

## 命名規則

| 対象 | 規則 | 例 |
|---|---|---|
| モジュール・パッケージ | 小文字 + アンダースコア | `my_module`, `cli_utils` |
| クラス | CapWords (PascalCase) | `MyClass`, `CliRunner` |
| 例外クラス | CapWords + `Error` サフィックス | `ConfigError` |
| 関数・変数 | 小文字 + アンダースコア | `run_task`, `file_path` |
| 定数 | 大文字 + アンダースコア | `MAX_RETRY`, `DEFAULT_TIMEOUT` |
| 非公開 | 先頭アンダースコア1つ | `_internal_helper` |
| モジュール非公開 | 先頭アンダースコア2つ | `__private` |
| ブール値 | `is_` / `has_` / `can_` / `should_` で始める | `is_valid`, `has_error` |

- 略語は使わない（`tmp` → `temporary`、`btn` → `button`）
- 単一文字変数（`l`, `O`, `I`）は禁止

---

## 型ヒント

Python 3.11 の型ヒント構文を使用する。

```python
# OK: Python 3.10+ union 構文
def greet(name: str | None = None) -> str: ...

# OK: 標準 typing
from typing import Optional
def greet(name: Optional[str] = None) -> str: ...
```

- 全パブリック関数・メソッドに引数と戻り値の型ヒントを付ける
- `Any` 型は最小限にとどめ、使用箇所にはコメントで理由を記載する
- `None` を返す関数は `-> None` を明示する

---

## Docstring

- 全パブリックモジュール・クラス・関数・メソッドに記述する
- **triple double-quotes** (`"""`) を使用する
- PEP 257 に準拠する

```python
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: List of command-line argument strings.

    Returns:
        Parsed argument namespace.

    Raises:
        SystemExit: If arguments are invalid.
    """
```

- 1行 docstring は同一行で閉じる: `"""Return the name."""`
- プライベート関数は docstring 不要（ただし複雑なロジックにはコメントを書く）

---

## コメント

- **英語**で記述する
- コード自体が読みやすく書けている場合はコメント不要（最小限主義）
- 複雑なロジック・非自明な判断には積極的にコメントを書く
- `# TODO:` / `# FIXME:` タグを使う場合は担当者と Issue 番号を記載する

```python
# TODO(username): Remove after Issue #42 is resolved
```

- コメントアウトしたコードは残さない（必要ならチケット化して削除）

---

## エラーハンドリング

- 例外を握りつぶさない（空の `except` 節禁止）
- 捕捉する例外は具体的な型を指定する（`except Exception` より `except ValueError`）
- ファイル・接続等のリソースは `with` 文で管理する
- CLI ツールはユーザー向けエラーメッセージに内部情報（スタックトレース等）を含めない

```python
# OK
try:
    data = json.loads(text)
except json.JSONDecodeError as exc:
    raise ConfigError(f"Invalid JSON: {exc}") from exc

# NG
try:
    data = json.loads(text)
except Exception:
    pass
```

---

## 関数・クラス設計

- 1関数1責務（単一責任原則）
- 関数の行数の目安は **50行以内**（超える場合は分割を検討）
- ネストの深さは **3段階以内**（深い場合は早期リターン・関数分割）
- マジックナンバー・マジック文字列は定数化する

```python
# NG
if status == 2:
    ...

# OK
STATUS_ACTIVE = 2
if status == STATUS_ACTIVE:
    ...
```

---

## Python 3.11 固有の推奨事項

- `tomllib`（標準ライブラリ）を設定ファイル読み込みに活用する
- `match` 文（構造的パターンマッチング）を複雑な条件分岐に活用する
- `ExceptionGroup` / `except*` を複数例外の集約に活用する
- `typing.Self` を自己参照型に使用する（`from typing import Self`）

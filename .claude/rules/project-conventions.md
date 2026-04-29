# Project Conventions

Python 3.11 + 標準ライブラリのみの CLI ツール向けプロジェクト規約。
コーディング規約（`coding-standards.md`）と合わせて参照すること。

---

## ディレクトリ構造

```
project-root/
├── src/
│   └── <package_name>/      # アプリケーションコード
│       ├── __init__.py
│       ├── __main__.py      # CLI エントリーポイント
│       ├── cli.py           # argparse 定義
│       └── ...
├── tests/                   # テストコード（src/ と分離）
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── pyproject.toml           # プロジェクト設定・pytest 設定
└── README.md
```

- アプリケーションコードは `src/` レイアウトに従う
- テストは `tests/` ディレクトリに分離する（インラインテスト禁止）

---

## テスト規約（pytest）

### ファイル・命名規則

- テストファイルは `test_*.py` または `*_test.py` で命名する
- テスト関数は `test_` プレフィックスを付ける
- テストクラスは `Test` プレフィックスを付け、`__init__` メソッドを持たない
- テストファイル名はプロジェクト全体で一意にする

```
tests/
├── conftest.py
├── unit/
│   ├── test_cli.py
│   └── test_parser.py
└── integration/
    └── test_main_flow.py
```

### テスト構造

- 1テスト1振る舞い（単一の動作・条件をテストする）
- **AAA パターン**（Arrange / Act / Assert）でテストを構造化する

```python
def test_parse_args_returns_verbose_flag():
    # Arrange
    argv = ["--verbose", "input.txt"]

    # Act
    result = parse_args(argv)

    # Assert
    assert result.verbose is True
```

### フィクスチャ（fixture）

- 共通セットアップは `fixture` で定義し、`conftest.py` に配置する
- フィクスチャのスコープは最小限（デフォルト `function`）にする
- スコープを広げる（`session` など）場合はコメントで理由を記載する

```python
# conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def tmp_config(tmp_path: Path) -> Path:
    """Provide a temporary config file for testing."""
    config = tmp_path / "config.toml"
    config.write_text('[tool]\nname = "test"')
    return config
```

### パラメータ化

- 同一ロジックに複数の入力パターンを検証する場合は `@pytest.mark.parametrize` を使う

```python
@pytest.mark.parametrize("value,expected", [
    ("yes", True),
    ("no", False),
    ("1", True),
])
def test_parse_bool(value: str, expected: bool) -> None:
    assert parse_bool(value) == expected
```

### カバレッジ

- **目標: 80% 以上**
- カバレッジ計測は `pytest-cov` を使用する
- 未テストの分岐・例外パスは `# pragma: no cover` でマークし、理由をコメントで記載する

### pytest 設定（pyproject.toml）

```toml
[tool.pytest.ini_options]
addopts = "--strict-markers --tb=short"
testpaths = ["tests"]
importmode = "importlib"

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## CLI ツール規約

### エントリーポイント

- `src/<package>/__main__.py` を CLI のエントリーポイントとする
- `python -m <package>` で実行できるようにする
- `argparse` を引数解析に使用する（外部ライブラリ不使用のため）

```python
# __main__.py
from myapp.cli import main

if __name__ == "__main__":
    main()
```

### 終了コード

| コード | 意味 |
|---|---|
| `0` | 正常終了 |
| `1` | 一般エラー（ユーザー起因） |
| `2` | 引数エラー（argparse デフォルト） |

### 標準出力・標準エラー

- 通常の出力は `stdout`（`print()`）
- エラー・警告メッセージは `stderr`（`print(..., file=sys.stderr)`）
- デバッグ出力は本番コードに残さない

---

## 設定ファイル

- 設定は `pyproject.toml` に集約する
- `tomllib`（Python 3.11 標準）で設定を読み込む

```python
import tomllib
from pathlib import Path

def load_config(path: Path) -> dict:
    """Load TOML configuration file."""
    with path.open("rb") as f:
        return tomllib.load(f)
```

---

## バージョン管理・ブランチ戦略

- メインブランチ: `main`
- 機能ブランチ: `feature/<issue-number>-<short-description>`
- バグ修正ブランチ: `fix/<issue-number>-<short-description>`
- コミットメッセージは英語・命令形で記述する（例: `Add config loader`, `Fix argument parsing`）

---

## Linter / Formatter

標準ライブラリのみの制約を守りつつ、以下を開発ツールとして使用する（実行環境への組み込み不要）。

| ツール | 用途 | 設定 |
|---|---|---|
| `ruff` | Lint + Format（PEP 8 準拠） | `pyproject.toml` |
| `mypy` | 型チェック | `pyproject.toml` |
| `pytest` | テスト実行 | `pyproject.toml` |
| `pytest-cov` | カバレッジ計測 | `pyproject.toml` |

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true
```

---

## ロギング

- `logging` モジュール（標準ライブラリ）を使用する
- `print()` でのデバッグ出力は禁止（テスト・本番コードともに）
- ログレベル: `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL`
- 個人情報・秘密情報はログに出力しない

```python
import logging

logger = logging.getLogger(__name__)

def run() -> None:
    logger.info("Starting task")
    try:
        ...
    except OSError as exc:
        logger.error("Failed to open file: %s", exc)
        raise
```

---

## 禁止事項

- 外部ライブラリの追加（標準ライブラリのみ使用）
- `eval()` / `exec()` の使用
- グローバル変数への書き込み（定数は許可）
- `os.system()` / `subprocess` でのシェル呼び出し（`shell=True` 禁止）
- `from module import *`（ワイルドカードインポート）

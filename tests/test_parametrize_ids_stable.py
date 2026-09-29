"""A parametrize id must be the same in every pytest-xdist worker (R-1112).

pytest-xdist imports the test modules once per worker and refuses to run when two
workers collect different test ids. An argument list that calls a source of fresh
values at import time, such as `str(uuid4())`, gives each worker its own ids, and
the whole suite then stops at collection before its first test.
"""

import ast
from pathlib import Path

TESTS = Path(__file__).resolve().parent
FRESH_VALUE_CALLS = frozenset(
    {
        "uuid1",
        "uuid4",
        "random",
        "randint",
        "choice",
        "token_hex",
        "token_urlsafe",
        "urandom",
        "time",
        "monotonic",
        "now",
        "utcnow",
    }
)


def _called_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def fresh_value_parametrize_sites(root: Path) -> list[str]:
    """Every call to a fresh-value source inside a parametrize call under root."""
    sites = []
    for path in sorted(root.rglob("*.py")):
        try:
            source = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            # R-1114: a temporary module another test wrote and removed while this scan ran
            # is gone, and xdist never collects it.
            continue
        tree = ast.parse(source, filename=str(path))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and _called_name(node) == "parametrize"):
                continue
            for inner in ast.walk(node):
                if inner is not node and isinstance(inner, ast.Call) and _called_name(inner) in FRESH_VALUE_CALLS:
                    sites.append(f"{path.relative_to(root.parent).as_posix()}:{inner.lineno}: {_called_name(inner)}()")
    return sites


def test_no_parametrize_argument_draws_a_fresh_value_at_collection() -> None:
    assert fresh_value_parametrize_sites(TESTS) == []


def test_the_scan_finds_a_fresh_uuid_in_a_parametrize_argument(tmp_path: Path) -> None:
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_sample.py").write_text(
        "import pytest\n"
        "from uuid import uuid4\n"
        "\n"
        "\n"
        '@pytest.mark.parametrize("name", ["gamma", str(uuid4())])\n'
        "def test_sample(name):\n"
        "    assert name\n",
        encoding="utf-8",
    )
    assert fresh_value_parametrize_sites(tests) == ["tests/test_sample.py:5: uuid4()"]


def test_a_test_file_that_vanished_is_skipped(tmp_path: Path) -> None:
    """R-1114: a module removed between the listing and the read is skipped, not raised over."""
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_gone.py").symlink_to(tmp_path / "missing.py")
    (tests / "test_sample.py").write_text(
        "import pytest\n"
        "from uuid import uuid4\n"
        "\n"
        "\n"
        '@pytest.mark.parametrize("name", [str(uuid4())])\n'
        "def test_sample(name):\n"
        "    assert name\n",
        encoding="utf-8",
    )
    assert fresh_value_parametrize_sites(tests) == ["tests/test_sample.py:5: uuid4()"]

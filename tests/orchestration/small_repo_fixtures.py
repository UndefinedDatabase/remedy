"""Reusable small-repo fixtures for autocoder validation.

Creates temporary real Python repos on disk for:
- fixture builder smoke
- real Ollama opt-in smoke
- repair loop tests
- source context tests

Each fixture returns the repo path. All repos are self-contained with
real files and real subprocess-runnable tests.
"""

from __future__ import annotations

from pathlib import Path


def create_missing_function_repo(root: Path) -> Path:
    """Scenario 1: test imports hello(), but app.py doesn't define it.

    Expected fix: add ``def hello(): return "hello"`` to app.py.
    """
    root.mkdir(parents=True, exist_ok=True)
    (root / "app.py").write_text(
        "# app module\n",
        encoding="utf-8",
    )
    tests_dir = root / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")
    (tests_dir / "test_app.py").write_text(
        "from app import hello\n\n"
        "def test_hello():\n"
        "    assert hello() == \"hello\"\n",
        encoding="utf-8",
    )
    return root


def create_wrong_return_repo(root: Path) -> Path:
    """Scenario 2: hello() returns wrong string.

    Expected fix: change return value to "hello".
    """
    root.mkdir(parents=True, exist_ok=True)
    (root / "app.py").write_text(
        "def hello():\n"
        "    return \"goodbye\"\n",
        encoding="utf-8",
    )
    tests_dir = root / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")
    (tests_dir / "test_app.py").write_text(
        "from app import hello\n\n"
        "def test_hello():\n"
        "    assert hello() == \"hello\"\n",
        encoding="utf-8",
    )
    return root


def create_repair_scenario_repo(root: Path) -> Path:
    """Scenario 3: two-function repo where first fix is partial.

    calc.py has add (wrong) and mul (wrong).
    Expected cycle 1: fix add, leave mul broken -> tests still fail.
    Expected cycle 2: fix mul -> all tests pass.
    """
    root.mkdir(parents=True, exist_ok=True)
    (root / "calc.py").write_text(
        "def add(a, b):\n"
        "    return a - b\n\n\n"
        "def mul(a, b):\n"
        "    return a + b\n",
        encoding="utf-8",
    )
    tests_dir = root / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")
    (tests_dir / "test_calc.py").write_text(
        "from calc import add, mul\n\n"
        "def test_add():\n"
        "    assert add(2, 3) == 5\n\n"
        "def test_mul():\n"
        "    assert mul(4, 5) == 20\n",
        encoding="utf-8",
    )
    return root


def fixture_patch_missing_function() -> dict:
    """JSON file_ops patch that fixes missing-function scenario."""
    return {
        "file_ops": [{
            "path": "app.py",
            "action": "modify",
            "content": "def hello():\n    return \"hello\"\n",
        }],
    }


def fixture_patch_wrong_return() -> dict:
    """JSON file_ops patch that fixes wrong-return scenario."""
    return {
        "file_ops": [{
            "path": "app.py",
            "action": "modify",
            "content": "def hello():\n    return \"hello\"\n",
        }],
    }


def fixture_patch_repair_cycle1() -> dict:
    """Partial fix: add correct, mul still wrong."""
    return {
        "file_ops": [{
            "path": "calc.py",
            "action": "modify",
            "content": (
                "def add(a, b):\n"
                "    return a + b\n\n\n"
                "def mul(a, b):\n"
                "    return a + b\n"
            ),
        }],
    }


def fixture_patch_repair_cycle2() -> dict:
    """Complete fix: both add and mul correct."""
    return {
        "file_ops": [{
            "path": "calc.py",
            "action": "modify",
            "content": (
                "def add(a, b):\n"
                "    return a + b\n\n\n"
                "def mul(a, b):\n"
                "    return a * b\n"
            ),
        }],
    }

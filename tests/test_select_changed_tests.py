"""The change-aware fast lane selects the owner tests of a change (operator order 2026-10-17).

``scripts/select_changed_tests.py`` is what ``scripts/remedy_test_fast.sh`` runs. Every rule is
exercised on a small repository built in ``tmp_path``; the last test runs the script itself
against this checkout, so the real test tree is indexed once.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import scripts.select_changed_tests as sel

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "select_changed_tests.py"


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.hooksPath=",
                    *args], cwd=root, check=True, capture_output=True, timeout=30)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A git repository with one module, its importers in four forms, and two guard files."""
    files = {
        "packages/core/thing.py": "VALUE = 1\n",
        "apps/cli/commands/verb.py": "def handle(args):\n    return 0\n",
        "scripts/run_me.sh": "#!/bin/sh\n",
        "README.md": "# Root\n", "docs/README.md": "# Docs\n", "docs/page.md": "# Page\n",
        "tests/test_from_module.py": "from packages.core.thing import VALUE\n",
        "tests/test_from_package.py": "from packages.core import thing\n",
        "tests/test_nested_import.py": "def test_x():\n    import packages.core.thing as t\n",
        "tests/test_unrelated.py": "import json\n",
        "tests/test_dispatch.py": "from apps.cli.grouped import main\n",
        "tests/test_names_the_name.py": 'SCRIPT = SCRIPTS / "run_me.sh"\n',
        "tests/test_names_the_path.py": 'PATH = "scripts/run_me.sh"\n',
        "tests/test_names_a_longer_path.py": 'PATH = "vendor/scripts/run_me.sh.bak"\n',
        "tests/test_writes_a_readme.py": '(repo / "README.md").write_text("x")\n',
        "tests/docs/test_docs_tree.py": "import pathlib\n",
    }
    for rel, text in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text, encoding="utf-8")
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "base")
    monkeypatch.setattr(sel, "ROOT", tmp_path)
    return tmp_path


def test_a_changed_module_selects_the_tests_that_import_it_in_every_form(repo):
    assert sel.select_test_files(["packages/core/thing.py"]) == [
        "tests/test_from_module.py", "tests/test_from_package.py", "tests/test_nested_import.py"]


def test_a_cli_module_also_selects_the_dispatch_tests(repo):
    assert "tests/test_dispatch.py" in sel.select_test_files(["apps/cli/commands/verb.py"])
    assert "tests/test_dispatch.py" not in sel.select_test_files(["packages/core/thing.py"])


def test_a_changed_test_file_selects_itself_and_a_deleted_one_does_not(repo):
    (repo / "tests/test_from_module.py").unlink()
    assert sel.select_test_files(["tests/test_unrelated.py", "tests/test_from_module.py"]) == [
        "tests/test_unrelated.py"]


def test_a_docs_change_selects_the_documentation_checks(repo):
    assert sel.select_test_files(["docs/page.md"]) == ["tests/docs/test_docs_tree.py"]


def test_a_path_is_matched_whole_and_a_unique_name_in_quotes(repo):
    assert sel.select_test_files(["scripts/run_me.sh"]) == [
        "tests/test_names_the_name.py", "tests/test_names_the_path.py"]


def test_a_name_two_tracked_files_share_is_matched_by_its_whole_path_only(repo):
    selected = sel.select_test_files(["docs/README.md"])
    assert "tests/test_writes_a_readme.py" not in selected
    assert selected == ["tests/docs/test_docs_tree.py"]


def test_a_test_file_that_vanishes_while_indexing_is_left_out(repo):
    """A running test may write a scratch test file into tests/ and remove it again."""
    index = sel.index_tests([repo / "tests/test_gone.py", repo / "tests/test_unrelated.py"])
    assert list(index) == ["tests/test_unrelated.py"]


def test_the_test_machinery_has_no_selection(repo, capsys):
    assert sel.main(["tests/conftest.py", "packages/core/thing.py"]) == 3
    out, err = capsys.readouterr()
    assert out == ""
    assert "tests/conftest.py changed; only the full suite answers" in err


def test_base_lists_committed_staged_unstaged_and_untracked_paths(repo):
    _git(repo, "checkout", "-q", "-b", "feature/x")
    (repo / "packages/core/thing.py").write_text("VALUE = 2\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "committed")
    (repo / "docs/page.md").write_text("# Staged\n", encoding="utf-8")
    _git(repo, "add", "docs/page.md")
    (repo / "scripts/run_me.sh").write_text("#!/bin/sh\necho\n", encoding="utf-8")
    (repo / "tests/test_new.py").write_text("", encoding="utf-8")
    assert sel.changed_paths_since("main") == [
        "docs/page.md", "packages/core/thing.py", "scripts/run_me.sh", "tests/test_new.py"]


def test_an_unknown_base_is_refused_with_exit_2(repo, capsys):
    assert sel.main(["--base", "no-such-ref"]) == 2
    assert "git could not list the change" in capsys.readouterr().err


def test_the_script_selects_owner_tests_in_this_checkout():
    run = subprocess.run([sys.executable, str(SCRIPT), "packages/orchestration/pi_loop_limits.py"],
                         cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)
    assert run.returncode == 0, run.stderr
    selected = run.stdout.split()
    assert "tests/orchestration/test_pi_loop_limits.py" in selected
    assert "tests/orchestration/test_job_task_runner.py" not in selected

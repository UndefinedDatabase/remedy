"""F269 T003 — the contract hygiene check (DECISION F269 D5 (1) to (4)).

What D5 requires proof of, each over a temporary git repository with a base
commit, the job's work left uncommitted as a ``run_job`` worktree leaves it:

  * ``unreferenced`` reports an added module no other file mentions — its own
    text naming its stem does not count — passes once a committed file imports
    it, and exempts ``__init__.py`` and test files;
  * ``replaced`` reports ``util_v2.py`` beside ``util.py`` and passes once
    ``util.py`` is gone;
  * ``stubs`` reports a TODO line added to a committed file and an added
    function whose body is ``pass``, and passes an ``abstractmethod``;
  * each rule, run as ``python3 -m packages.orchestration.contract_hygiene``,
    exits 0 on a clean tree, 1 on findings and 2 outside a git work tree;
  * the same argv as an F061 ``custom_cmd`` check through the real
    ``dod_gate.evaluate_dod`` is red with an orphan and green without.

No provider is called.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import contract_hygiene
from packages.orchestration.contract_hygiene import (
    EXIT_CANNOT_MEASURE,
    EXIT_CLEAN,
    EXIT_FINDINGS,
    HYGIENE_RULES,
    measure_work_tree,
    replaced_originals,
    run_hygiene_rule,
)
from packages.orchestration.dod_gate import evaluate_dod
from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck

#: The source tree this test imported the module from; the subprocess must run
#: the same code, not whatever copy an installed package points at.
SOURCE_ROOT = str(Path(contract_hygiene.__file__).resolve().parents[2])


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


def _write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _commit(repo: Path, *rels: str) -> None:
    _git(repo, "add", *rels)
    _git(repo, "commit", "-qm", "commit")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    _write(r, "main.py", "# TODO: an old marker the job did not add\nprint('hi')\n")
    _write(r, "util.py", "def helper():\n    return 1\n")
    _commit(r, "main.py", "util.py")
    return r


def _findings(repo: Path, rule: str) -> list[tuple[str, int]]:
    return [(f.path, f.line) for f in run_hygiene_rule(rule, measure_work_tree(repo))]


def _run(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONPATH=SOURCE_ROOT,
               GIT_CEILING_DIRECTORIES=str(cwd.parent))
    return subprocess.run(
        ["python3", "-m","packages.orchestration.contract_hygiene", *args],
        cwd=str(cwd), capture_output=True, text=True, env=env, check=False)


# ── unreferenced ───────────────────────────────────────────────────────────


def test_unreferenced_reports_an_added_module_only_its_own_text_names(repo):
    _write(repo, "orphan_module.py", "# orphan_module.py\nVALUE = 1\n")

    assert _findings(repo, "unreferenced") == [("orphan_module.py", 0)]
    done = _run(repo, "unreferenced")
    assert done.returncode == EXIT_FINDINGS
    assert done.stdout.splitlines() == [
        "orphan_module.py: unreferenced: an added file that no other file references"]


def test_unreferenced_passes_once_a_committed_file_imports_the_module(repo):
    _write(repo, "orphan_module.py", "VALUE = 1\n")
    _write(repo, "main.py", "import orphan_module\nprint(orphan_module.VALUE)\n")
    _commit(repo, "main.py")

    assert _findings(repo, "unreferenced") == []
    assert _run(repo, "unreferenced").returncode == EXIT_CLEAN


def test_a_longer_name_holding_the_stem_is_no_reference(repo):
    _write(repo, "orphan.py", "VALUE = 1\n")
    _write(repo, "main.py", "import orphan_module_two\n")
    _commit(repo, "main.py")

    assert _findings(repo, "unreferenced") == [("orphan.py", 0)]


def test_unreferenced_exempts_init_and_test_files(repo):
    _write(repo, "pkg/__init__.py", "")
    _write(repo, "tests/helpers.py", "X = 1\n")
    _write(repo, "test_widget.py", "def test_x():\n    assert True\n")
    _write(repo, "web/button.spec.ts", "export {}\n")

    assert _findings(repo, "unreferenced") == []
    assert _run(repo, "unreferenced").returncode == EXIT_CLEAN


def test_an_added_file_that_is_not_code_is_not_judged(repo):
    _write(repo, "notes.md", "nothing references this\n")

    assert _findings(repo, "unreferenced") == []


# ── replaced ───────────────────────────────────────────────────────────────


def test_replaced_reports_util_v2_beside_util_and_passes_once_util_is_deleted(repo):
    _write(repo, "util_v2.py", "def helper():\n    return 2\n")

    assert _findings(repo, "replaced") == [("util_v2.py", 0)]
    done = _run(repo, "replaced")
    assert done.returncode == EXIT_FINDINGS
    assert done.stdout.splitlines() == [
        "util_v2.py: replaced: added beside util.py, which it replaces"]

    (repo / "util.py").unlink()
    assert _findings(repo, "replaced") == []
    assert _run(repo, "replaced").returncode == EXIT_CLEAN


@pytest.mark.parametrize(("added", "original"), [
    ("pkg/util_new.py", "pkg/util.py"), ("util_old.py", "util.py"),
    ("util_copy.py", "util.py"), ("util_backup.py", "util.py"),
    ("util_bak.py", "util.py"), ("util_v12.py", "util.py"),
    ("new_util.py", "util.py"), ("old_util.py", "util.py"),
    ("util.py.bak", "util.py"), ("util.py.orig", "util.py"),
])
def test_each_replacement_marker_names_the_file_it_replaces(added, original):
    assert original in replaced_originals(added)


def test_a_marker_whose_original_does_not_exist_is_no_finding(repo):
    _write(repo, "parser_v2.py", "X = 1\n")

    assert _findings(repo, "replaced") == []


# ── stubs ──────────────────────────────────────────────────────────────────


def test_stubs_reports_a_todo_line_added_to_a_committed_file(repo):
    _write(repo, "util.py", "def helper():\n    return 1\n# TODO: finish this\n")

    # main.py's committed TODO was not added by the job, so it is not reported.
    assert _findings(repo, "stubs") == [("util.py", 3)]


def test_stubs_reports_an_added_function_whose_body_is_pass(repo):
    _write(repo, "feature.py", 'def run():\n    """Run it."""\n    pass\n\n\n'
                               "def ready():\n    return True\n")

    assert _findings(repo, "stubs") == [("feature.py", 1)]
    done = _run(repo, "stubs")
    assert done.returncode == EXIT_FINDINGS
    assert done.stdout.splitlines() == ["feature.py:1: stubs: function run has a stub body"]


def test_stubs_passes_an_abstractmethod(repo):
    _write(repo, "shape.py", (
        "import abc\n\n\nclass Shape(abc.ABC):\n"
        "    @abc.abstractmethod\n    def area(self):\n        raise NotImplementedError\n"))

    assert _findings(repo, "stubs") == []
    assert _run(repo, "stubs").returncode == EXIT_CLEAN


def test_stubs_reports_ellipsis_and_not_implemented_bodies(repo):
    _write(repo, "later.py", (
        "def one():\n    ...\n\n\ndef two():\n    raise NotImplementedError('soon')\n"))

    assert _findings(repo, "stubs") == [("later.py", 1), ("later.py", 5)]


# ── the command line ───────────────────────────────────────────────────────


_FINDING_FOR = {
    "unreferenced": ("orphan_module.py", "VALUE = 1\n"),
    "replaced": ("util_v2.py", "import util\n"),
    "stubs": ("util.py", "def helper():\n    return 1\n# FIXME later\n"),
}


@pytest.mark.parametrize("rule", HYGIENE_RULES)
def test_each_rule_exits_0_clean_1_on_findings_and_2_outside_a_work_tree(rule, repo, tmp_path):
    clean = _run(repo, rule)
    assert (clean.returncode, clean.stdout) == (EXIT_CLEAN, "")

    rel, text = _FINDING_FOR[rule]
    _write(repo, rel, text)
    found = _run(repo, rule)
    assert found.returncode == EXIT_FINDINGS
    assert rel in found.stdout

    outside = tmp_path / "not-a-repo"
    outside.mkdir()
    done = _run(outside, rule)
    assert done.returncode == EXIT_CANNOT_MEASURE
    assert "cannot measure" in done.stderr


def test_an_unknown_rule_exits_2():
    assert contract_hygiene.main(["everything"]) == EXIT_CANNOT_MEASURE
    assert contract_hygiene.main([]) == EXIT_CANNOT_MEASURE


def test_a_git_query_that_times_out_exits_2_cannot_measure(repo, monkeypatch, capsys):
    monkeypatch.chdir(repo)
    timeouts: list[object] = []

    def hanging_run(argv, *args, **kwargs):
        timeouts.append(kwargs.get("timeout"))
        raise subprocess.TimeoutExpired(argv, kwargs.get("timeout"))

    monkeypatch.setattr(contract_hygiene.subprocess, "run", hanging_run)

    assert contract_hygiene.main(["unreferenced"]) == EXIT_CANNOT_MEASURE
    assert timeouts == [contract_hygiene._GIT_TIMEOUT_SEC]
    err = capsys.readouterr().err
    assert "cannot measure" in err
    assert f"timed out after {contract_hygiene._GIT_TIMEOUT_SEC}s" in err


# ── through F061's real gate ───────────────────────────────────────────────


def test_the_rule_as_a_custom_cmd_check_holds_the_real_gate_on_an_orphan(repo, monkeypatch):
    monkeypatch.setenv("PYTHONPATH", SOURCE_ROOT)
    check = DoDCheck(
        id="ctr-C005", kind="custom_cmd", blocking=True, source="plan_acceptance",
        spec={"argv": ["python3", "-m", "packages.orchestration.contract_hygiene",
                       "unreferenced"]})
    dod = DoD(schema_v=DOD_SCHEMA_V, checks=[check], compiled=False, origin="deterministic")

    _write(repo, "orphan_module.py", "VALUE = 1\n")
    held = evaluate_dod(dod, repo)
    assert held.released is False
    assert held.blocking_red == ("ctr-C005",)
    assert held.evidence[0].exit_code == EXIT_FINDINGS
    assert "orphan_module.py" in held.evidence[0].output_tail

    (repo / "orphan_module.py").unlink()
    released = evaluate_dod(dod, repo)
    assert released.released is True
    assert released.evidence[0].exit_code == EXIT_CLEAN

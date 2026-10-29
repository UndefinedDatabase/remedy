"""F329 (operator order beweis): Remedy narrows its own test run to the changed parts."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from packages.orchestration.changed_test_selection import narrowed_test_argv
from packages.orchestration.dod_gate import _evidence_json
from packages.orchestration.dod_runners import STATUS_PASSED, run_check
from packages.orchestration.dod_schema import DoDCheck
from packages.orchestration.project_tests import ProjectTestCommand

PYTEST = ProjectTestCommand(argv=("python3", "-m", "pytest", "-p", "no:cacheprovider", "tests", "-q"),
                            source="tests_folder")
NPM = ProjectTestCommand(argv=("npm", "test"), source="package_json")


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), check=True, capture_output=True, text=True)


def _write(root: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text)


def _job_worktree(tmp_path: Path, files: dict[str, str]) -> Path:
    """A committed checkout holding FILES and a job worktree of it under `.remedy-wt`."""
    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (("init", "-q", "-b", "main"), ("config", "user.email", "t@e.com"), ("config", "user.name", "T"),
                 ("config", "commit.gpgsign", "false")):
        _git(repo, *args)
    _write(repo, {".gitignore": ".remedy-wt/\n", **files})
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    worktree = repo / ".remedy-wt" / "job"
    _git(repo, "worktree", "add", "-q", str(worktree), "-b", "job")
    return worktree


PY_PROJECT = {
    "pkg/a.py": "A = 1\n", "other/b.py": "B = 2\n",
    "tests/pkg/test_a.py": "from pkg.a import A\n\n\ndef test_a():\n    assert A == 1\n",
    "tests/other/test_b.py": "def test_b():\n    assert False\n",
    "tests/test_named.py": "def test_named():\n    assert True\n",
}


def test_pytest_runs_the_test_folder_of_the_touched_source_folder_and_the_named_test_file(tmp_path):
    worktree = _job_worktree(tmp_path, PY_PROJECT)
    _write(worktree, {"pkg/a.py": "A = 1  # changed\n", "tests/test_named.py": "def test_named():\n    assert 1\n"})
    argv, selection = narrowed_test_argv(PYTEST, worktree)
    assert argv == ["python3", "-m", "pytest", "-p", "no:cacheprovider", "tests/pkg", "tests/test_named.py", "-q"]
    assert selection == "pytest narrowed to 2 of the diff's parts: tests/pkg, tests/test_named.py"


def test_a_diff_over_eleven_source_folders_runs_the_full_command(tmp_path):
    worktree = _job_worktree(tmp_path, PY_PROJECT)
    _write(worktree, {f"src{n}/m.py": "X = 1\n" for n in range(11)})
    argv, selection = narrowed_test_argv(PYTEST, worktree)
    assert argv == list(PYTEST.argv)
    assert selection == "full run: the diff touches 11 source folders, more than 10"
    (worktree / "src10" / "m.py").unlink()   # ten folders narrow, and none has a test folder
    assert narrowed_test_argv(PYTEST, worktree)[1].startswith("full run: no test folder")


def test_a_changed_configuration_file_runs_the_full_command(tmp_path):
    worktree = _job_worktree(tmp_path, PY_PROJECT)
    _write(worktree, {"pkg/a.py": "A = 1  # changed\n", "pyproject.toml": "[project]\n"})
    argv, selection = narrowed_test_argv(PYTEST, worktree)
    assert argv == list(PYTEST.argv) and selection == "full run: the diff changes pyproject.toml, which every test may read"


def test_vitest_runs_the_test_files_that_import_or_are_named_like_the_changed_file(tmp_path):
    worktree = _job_worktree(tmp_path, {
        "package.json": json.dumps({"scripts": {"test": "vitest run"}}),
        "src/sum.ts": "export const sum = (a: number, b: number) => a + b;\n",
        "src/sum.test.ts": "import { sum } from './sum';\n",
        "test/uses.spec.ts": "import { sum } from \"../src/sum\";\n",
        "test/other.test.ts": "import { x } from '../src/other';\n",
        "src/other.ts": "export const x = 1;\n",
    })
    _write(worktree, {"src/sum.ts": "export const sum = (a: number, b: number) => b + a;\n"})
    argv, selection = narrowed_test_argv(NPM, worktree)
    assert argv == ["npm", "test", "--", "src/sum.test.ts", "test/uses.spec.ts"]
    assert selection == "vitest narrowed to 2 of the diff's parts: src/sum.test.ts, test/uses.spec.ts"


def test_a_test_script_that_is_not_vitest_alone_runs_the_full_command(tmp_path):
    worktree = _job_worktree(tmp_path, {"package.json": json.dumps({"scripts": {"test": "tsc && vitest run"}}),
                                        "src/sum.ts": "", "src/sum.test.ts": ""})
    _write(worktree, {"src/sum.ts": "export {};\n"})
    assert narrowed_test_argv(NPM, worktree) == (["npm", "test"], "full run: Remedy narrows only pytest and Vitest, not package_json")


def test_the_job_end_check_names_its_selection_in_the_evidence(tmp_path):
    worktree = _job_worktree(tmp_path, PY_PROJECT)
    _write(worktree, {"pkg/a.py": "A = 1  # changed\n"})
    check = DoDCheck(id="c1", kind="project_tests", spec={}, source="compiled")
    evidence = run_check(check, worktree, timeout_sec=120)
    assert evidence.status == STATUS_PASSED, evidence.output_tail   # tests/other's red test did not run
    assert "tests/pkg" in evidence.argv and "tests" not in evidence.argv
    assert _evidence_json(evidence)["selection"] == "pytest narrowed to 1 of the diff's parts: tests/pkg"

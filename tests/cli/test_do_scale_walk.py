"""The 2026-10-17 scale audit, through the real `remedy do` walk on disposable repositories.

Fake builder and reviewer, every planning and study factory a tripwire, the data root under
`tmp_path`. What each case proves is stated by its name: the lane, the number of jobs and tasks and
whether any planning call was made.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from tests.cli.test_do_bounded_lane import (  # noqa: F401 — fixtures used by name
    _commit_repo,
    _do,
    _step,
    events,
    planning_calls,
)


@pytest.fixture
def make_repo(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

    def make(files: dict[str, str]) -> Path:
        target = _commit_repo(tmp_path / "work", files)
        monkeypatch.chdir(target)
        return target
    return make


def _tasks(data: dict) -> list[dict]:
    return [task for job in data["jobs"] for task in job["tasks"]]


def test_the_hold_names_the_candidates_and_creates_no_job_and_no_mission(make_repo, capsys,
                                                                         planning_calls):
    repo = make_repo({"src/app.py": "x = 1\n", "docs/README.md": "# Docs\n",
                      "web/README.md": "# Web\n"})

    try:
        out = _do(capsys, "--json", "--plan-only", order="Fix the typo in README.md.")
    except SystemExit:
        out = capsys.readouterr().out
    data = json.loads(out)

    assert [s["name"] for s in data["steps"]][-1] == "study"
    stop = _step(data, "study")
    assert stop["status"] == "stopped"
    assert "docs/README.md" in stop["detail"] and "web/README.md" in stop["detail"]
    assert data["job_ids"] == []
    assert subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo,
                          capture_output=True, text=True, check=True).stdout.strip() == ""
    assert planning_calls == []


def test_root_readme_beside_docs_readme_is_bounded_and_serves_only_the_root_file(
        make_repo, capsys, planning_calls):
    make_repo({"README.md": "# Root\n", "docs/README.md": "# Docs\n"})

    data = json.loads(_do(capsys, "--json", "--plan-only", order="Fix the typo in README.md."))

    assert "lane: bounded" in _step(data, "plan")["detail"]
    assert [t["deliverable"] for t in _tasks(data)] == ["README.md"]
    assert planning_calls == []


def test_a_bug_fix_with_a_regression_test_is_one_job_one_task_and_keeps_the_test(
        make_repo, capsys, planning_calls):
    make_repo({"src/add.py": "def add(a, b):\n    return a - b\n",
               "tests/test_add.py": "def test_ok():\n    pass\n"})

    data = json.loads(_do(capsys, "--json", "--plan-only",
                          order="Fix the bug in src/add.py and add a regression test."))

    [job] = data["jobs"]
    [task] = job["tasks"]
    assert task["deliverable"] == "src/add.py"
    assert "lane: bounded" in _step(data, "plan")["detail"]
    from packages.orchestration.pingpong_job import load_job_plan
    stored = load_job_plan(job["job_id"]).tasks[0]
    assert stored.inputs["with_tests"] is True
    assert "test" in stored.body.lower().split("deliverable:")[-1]
    assert "the test the order asks for exists and passes" in stored.acceptance
    assert planning_calls == []


def test_running_the_tests_is_a_check_and_adds_nothing_to_the_task(make_repo, capsys, planning_calls):
    make_repo({"src/add.py": "x = 1\n", "tests/test_add.py": "def test_ok():\n    pass\n"})

    data = json.loads(_do(capsys, "--json", "--plan-only",
                          order="Fix the bug in src/add.py. Run the tests."))

    from packages.orchestration.pingpong_job import load_job_plan
    stored = load_job_plan(data["jobs"][0]["job_id"]).tasks[0]
    assert "with_tests" not in stored.inputs and len(data["jobs"][0]["tasks"]) == 1


def test_a_one_file_auth_rewrite_is_never_the_tiny_path(make_repo, capsys):
    make_repo({"src/app.ts": "export {}\n", "src/auth.ts": "export {}\n"})

    data = json.loads(_do(capsys, "--json", "--plan-only", "--no-llm",
                          order="Rewrite the complete authentication system in src/app.ts."))

    detail = _step(data, "plan")["detail"]
    assert "lane: full" in detail and "high-risk" in detail
    assert data["shape_source"] != "bounded lane"


def test_a_force_job_override_runs_bounded_and_says_so(make_repo, capsys):
    make_repo({"src/app.ts": "export {}\n", "src/auth.ts": "export {}\n"})

    data = json.loads(_do(capsys, "--json", "--plan-only", "--force-job", "--no-llm",
                          order="Rewrite the complete authentication system in src/app.ts."))

    detail = _step(data, "plan")["detail"]
    assert "--force-job" in detail and "routing alone chose the full lane" in detail


def test_a_readme_edit_in_a_large_repository_makes_no_planning_or_study_call(
        make_repo, capsys, planning_calls):
    files = {f"pkg{n // 50}/mod{n}.py": "x = 1\n" for n in range(300)}
    files["README.md"] = "# Big\n"
    make_repo(files)

    data = json.loads(_do(capsys, "--json", "--plan-only", order="Fix the typo in README.md"))

    assert "lane: bounded" in _step(data, "plan")["detail"]
    assert [len(job["tasks"]) for job in data["jobs"]] == [1]
    assert planning_calls == []


@pytest.mark.parametrize("order", [
    "Fix the typo in README.md",
    "Fix the typo in README.md.",
    "Task:\n- Fix the typo in README.md",
    "Fix the typo in README.md; change no other files",
    "Korrigiere den Tippfehler in README.md. Ändere keine anderen Dateien.",
])
def test_equivalent_orders_make_the_same_plan(make_repo, capsys, planning_calls, order):
    make_repo({"README.md": "# T\n", "src/a.py": "x = 1\n"})

    data = json.loads(_do(capsys, "--json", "--plan-only", order=order))

    assert (data["shape"], data["shape_source"]) == ("one job", "bounded lane")
    assert [(len(j["tasks"]), j["tasks"][0]["deliverable"]) for j in data["jobs"]] == [(1, "README.md")]
    assert planning_calls == []


def test_the_builder_and_the_reviewer_are_given_the_orders_own_words_not_a_summary(
        make_repo, capsys, monkeypatch):
    """The semantics of an order reach both roles: the reviewer can only fail wrong content, even in
    the right file, if it is shown what the order meant (amend1016p D3 asks it to)."""
    from packages.orchestration.pingpong_provider_fake import FakeProvider

    seen: dict[str, list[str]] = {"build": [], "review": []}
    for method in ("build", "review"):
        original = getattr(FakeProvider, method)

        def spy(self, prompt, *args, _original=original, _method=method, **kwargs):
            seen[_method].append(prompt)
            return _original(self, prompt, *args, **kwargs)
        monkeypatch.setattr(FakeProvider, method, spy)
    make_repo({"README.md": "# T\n", "src/a.py": "x = 1\n"})
    phrase = "two short German sentences about the Testbetrieb"

    _do(capsys, "--json", order=f"Append a section to README.md with {phrase}. Change no other files.")

    assert seen["build"] and seen["review"]
    missing = {role: [i for i, prompt in enumerate(prompts) if phrase not in prompt]
               for role, prompts in seen.items()}
    assert all(phrase in prompt for prompt in seen["build"] + seen["review"])

"""F312, R-1369 — the three orders of the lab runs of 2026-10-20 (Remedy 1.21, Pi over a local
model), as a fixture, walked through the real walk.

The texts are written from the feature files, not from the lab's review reports, which are not
read (DECISION F312 D1). All three are of the kind `open` (`do_scope.order_scope_kind`); the
second is walked end to end through `apps.cli.grouped.main` ("apps.cli.main.main" delegates to
it with no argv of its own), in process, with fake providers and a fixed intake and planner, no
real model or network reached.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main

#: The lab's first order of 2026-10-20: no file name, no fence — an open order.
LAB_ORDER_1 = "Bau jetzt eine minimale html showcase page nur zum testen"
#: The lab's second order of 2026-10-20 (R-1369): no file name, no fence — an open order.
LAB_ORDER_2 = "Super, jetzt mach ein schickes design"
#: The lab's third order of 2026-10-20: no file name, no fence — an open order.
LAB_ORDER_3 = "Bring die webseite auf prototyp niveau und füge funktionalität hinzu"

#: Every milestone's job outline, read exactly as the lab's planner wrote it.
LAB_OUTLINE_GOAL = "Change only README.md and describe the new design there."

_INTAKE_JSON = ('{"schema_v": "ji1", "goal": "g", "context_refs": [], "constraints": [], '
               '"acceptance_hints": [], "truncated_input": false, "clarifications": []}')


def _mission_plan_json() -> str:
    """Two milestones, each with one job outline reading `LAB_OUTLINE_GOAL`."""
    milestones = [
        {"id": "M1", "goal": "Redesign the site", "depends_on": [],
         "jobs_draft": [{"title": LAB_OUTLINE_GOAL, "goal": LAB_OUTLINE_GOAL, "est_band": "M"}]},
        {"id": "M2", "goal": "Finish the redesign", "depends_on": ["M1"],
         "jobs_draft": [{"title": LAB_OUTLINE_GOAL, "goal": LAB_OUTLINE_GOAL, "est_band": "M"}]},
    ]
    return json.dumps({"schema_v": "mission_plan_draft_v1", "milestones": milestones,
                       "risks": [], "assumptions": []})


def _task_plan_json(title: str, goal: str, hint: str, *, task_id: str = "T001") -> dict:
    return {"id": task_id, "title": title, "goal": goal, "acceptance": [f"{title} is done"],
            "depends_on": [], "est_tokens_band": "S", "files_hint": [hint]}


def _two_file_task_plan_json() -> str:
    """T002 delivering `style.css` and T003 delivering `index.html`."""
    return json.dumps({"schema_v": "task_plan_v1", "tasks": [
        _task_plan_json("Add a modern colour scheme", "Add a modern colour scheme",
                        "style.css", task_id="T002"),
        _task_plan_json("Restructure the page layout", "Restructure the page layout",
                        "index.html", task_id="T003")]})


def _checksum_task_plan_json() -> str:
    """The one task a checking-only planner ever plans: a checksum manifest, no real deliverable."""
    return json.dumps({"schema_v": "task_plan_v1", "tasks": [
        _task_plan_json("Write a checksum manifest of the site",
                        "Write a checksum manifest of the site", "checksums.json")]})


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """An unregistered git repository tracking `index.html`, `style.css`, `script.js` and `README.md`."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = tmp_path / "target"
    target.mkdir()
    _git(target, "init", "-q")
    _git(target, "config", "user.email", "t@e.com")
    _git(target, "config", "user.name", "T")
    _git(target, "config", "commit.gpgsign", "false")
    (target / "index.html").write_text("<html></html>\n")
    (target / "style.css").write_text("body {}\n")
    (target / "script.js").write_text("// nothing yet\n")
    (target / "README.md").write_text("# target\n")
    _git(target, "add", "-A")
    _git(target, "commit", "-qm", "init")
    monkeypatch.chdir(target)
    return target.resolve()


@pytest.fixture(autouse=True)
def no_model_call(monkeypatch):
    """Every factory that could reach a model fails the test when reached and not faked."""
    def tripwire(*args, **kwargs):
        raise AssertionError("the walk reached a model-call factory this fixture did not fake")

    import packages.orchestration.study  # noqa: F401 — imported before patched, as test_do_sequence_cli.py notes
    monkeypatch.setattr("packages.orchestration.study.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", tripwire)


def _fake_intake(monkeypatch):
    """The intake branch, as `test_do_sequence_scope_order.py` fakes it: an unstructured call."""
    monkeypatch.setattr(
        "packages.orchestration.intake.make_provider_call_fn",
        lambda: (lambda prompt, attempt: _INTAKE_JSON))


def _fake_planner(monkeypatch, task_plan_json_fn):
    """Fake `intake.make_structured_call_fn`, answering by its model class.

    `MissionPlanDraft` always answers the lab's two-milestone plan; `TaskPlan` answers
    `task_plan_json_fn()` and counts its own calls. Returns the call-count list.
    """
    from packages.orchestration.mission_plan_schema import MissionPlanDraft
    from packages.orchestration.schemas.models import TaskPlan

    calls: list[int] = []

    def _fake(model_cls, **kwargs):
        if model_cls is MissionPlanDraft:
            return lambda prompt, attempt: _mission_plan_json()
        if model_cls is TaskPlan:
            def _answer(prompt: str, attempt: int) -> str:
                calls.append(1)
                return task_plan_json_fn()
            return _answer
        raise AssertionError(f"the walk asked a structured call for {model_cls!r}, not faked")

    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", _fake)
    return calls


def _do_json(monkeypatch, capsys, order: str, task_plan_json_fn) -> tuple[dict, list[int]]:
    """Walk the real `do` sequence in process; the repo is the fixture's own cwd."""
    _fake_intake(monkeypatch)
    calls = _fake_planner(monkeypatch, task_plan_json_fn)
    main(["do", order, "--plan-only", "--no-ui", "--json",
         "--builder-provider", "fake", "--reviewer-provider", "fake"])
    return json.loads(capsys.readouterr().out), calls


def test_all_three_lab_orders_are_of_the_open_kind():
    from packages.orchestration.do_scope import ORDER_SCOPE_OPEN, order_scope_kind

    for order in (LAB_ORDER_1, LAB_ORDER_2, LAB_ORDER_3):
        assert order_scope_kind(order) == ORDER_SCOPE_OPEN


def test_the_second_lab_order_walks_as_milestones_with_style_and_index_deliverables(
        repo, capsys, monkeypatch):
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.task_deliverables import task_deliverable

    data, calls = _do_json(monkeypatch, capsys, LAB_ORDER_2, _two_file_task_plan_json)

    assert data["shape"] == "milestones"
    assert all(step["status"] != "failed" for step in data["steps"])
    assert len(data["job_ids"]) == 2
    assert len(calls) == 2
    for job_id in data["job_ids"]:
        tasks = load_job_plan(job_id).tasks
        assert [task_deliverable(t) for t in tasks] == ["style.css", "index.html"]


def test_the_second_lab_order_with_a_checking_only_planner_stops_and_asks(
        repo, capsys, monkeypatch):
    data, calls = _do_json(monkeypatch, capsys, LAB_ORDER_2, _checksum_task_plan_json)

    shape_step = next(s for s in data["steps"] if s["name"] == "shape")
    assert shape_step["status"] == "stopped"
    assert "asks which files the order means" in shape_step["detail"]
    assert any("remedy decision resolve" in line for line in data["next"])
    assert len(calls) == 2

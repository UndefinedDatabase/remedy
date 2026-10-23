"""Operator amendment amend1023-universe-trust, Part 2 — small orders stay small, held against the
universe's probe of 2026-10-23 (order key `luna-twmhd8`): a one-line repair in universe-chat became
three milestones and five jobs, and its first job blocked on its own criterion, a notes file
`docs/chat_gedaechtnis_map.md` nobody ordered.

The order text is `fixtures/order_luna_twmhd8.txt`, copied from the mission record that holds it
(DECISION amend1023 D2); no diagnostic part and no personal data. The walk runs in process through
`apps.cli.grouped.main` with the fake builder and reviewer and a scripted planner, as
`test_lab_orders_20261020.py` drives it; no real model or network is reached.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from apps.cli.grouped import main

#: The probe's order, exactly as the mission record holds it.
PROBE_ORDER = (Path(__file__).parent / "fixtures" / "order_luna_twmhd8.txt").read_text(encoding="utf-8").strip()
#: The criterion that blocked the probe's first job, in the planner's own words.
PROBE_CRITERION = "docs/chat_gedaechtnis_map.md exists"

_INTAKE_JSON = ('{"schema_v": "ji1", "goal": "g", "context_refs": [], "constraints": [], '
               '"acceptance_hints": [], "truncated_input": false, "clarifications": []}')


def _probe_mission_plan_json() -> str:
    """The probe planner's split: three milestones, the first with two job outlines."""
    outline = {"title": "Locate memory infobutton implementation", "est_band": "M",
               "goal": "Find source files rendering (i) in Chat Gedächtnis"}
    milestones = [
        {"id": "M001", "goal": "The memory (i) button is documented", "depends_on": [],
         "jobs_draft": [outline, {**outline, "title": "Capture standard i-button pattern"}]},
        {"id": "M002", "goal": "The memory (i) button matches", "depends_on": ["M001"], "jobs_draft": [outline]},
        {"id": "M003", "goal": "The memory (i) button is confirmed", "depends_on": ["M002"],
         "jobs_draft": [outline]},
    ]
    return json.dumps({"schema_v": "mission_plan_draft_v1", "milestones": milestones,
                       "risks": [], "assumptions": []})


def _probe_task_plan_json() -> str:
    """The probe's first task, its two criteria as the planner wrote them."""
    return json.dumps({"schema_v": "task_plan_v1", "tasks": [{
        "id": "T001", "title": "Map Chat Gedächtnis source structure",
        "goal": "Identify entry points and component files for Chat Gedächtnis UI to scope search.",
        "acceptance": [PROBE_CRITERION, "the button in src/chat/MemoryPanel.tsx has aria-haspopup"],
        "depends_on": [], "est_tokens_band": "S", "files_hint": ["src/chat/MemoryPanel.tsx"]}]})


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """A small universe-chat: the memory panel and the app's standard info button."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = tmp_path / "universe-chat"
    (target / "src" / "chat").mkdir(parents=True)
    _git(target, "init", "-q")
    for key, value in (("user.email", "t@e.com"), ("user.name", "T"), ("commit.gpgsign", "false")):
        _git(target, "config", key, value)
    (target / "src" / "chat" / "MemoryPanel.tsx").write_text("export const Info = () => <button>i</button>;\n")
    (target / "src" / "InfoButton.tsx").write_text("export const InfoButton = () => <button aria-haspopup>i</button>;\n")
    (target / "README.md").write_text("# universe-chat\n")
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


def _walk(monkeypatch, capsys, order: str) -> tuple[dict, list[str]]:
    """`remedy do <order> --plan-only --json` with the fake workers; the names of the planner calls made."""
    from packages.orchestration.mission_plan_schema import MissionPlanDraft
    from packages.orchestration.schemas.models import TaskPlan

    asked: list[str] = []

    def _structured(model_cls, **kwargs):
        if model_cls is MissionPlanDraft:
            asked.append("mission_plan")
            return lambda prompt, attempt: _probe_mission_plan_json()
        if model_cls is TaskPlan:
            asked.append("task_plan")
            return lambda prompt, attempt: _probe_task_plan_json()
        raise AssertionError(f"the walk asked a structured call for {model_cls!r}, not faked")

    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn",
                        lambda: (lambda prompt, attempt: _INTAKE_JSON))
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", _structured)
    main(["do", order, "--plan-only", "--no-ui", "--json",
          "--builder-provider", "fake", "--reviewer-provider", "fake"])
    return json.loads(capsys.readouterr().out), asked


def _story(job_id: str) -> dict:
    from packages.orchestration.client_story import job_client_story
    from packages.orchestration.pingpong_job import load_job_plan

    return job_client_story(job_id, load_job_plan(job_id))


# -- Rule 1: the scope guard reads the criteria too ------------------------------------------


def test_the_probes_notes_file_criterion_is_removed_and_named_in_the_story(repo, capsys, monkeypatch):
    from packages.orchestration.pingpong_job import load_job_plan

    data, _asked = _walk(monkeypatch, capsys, PROBE_ORDER)
    assert all(step["status"] != "failed" for step in data["steps"]), data["steps"]
    for job_id in data["job_ids"]:
        [task] = load_job_plan(job_id).tasks
        assert PROBE_CRITERION not in task.acceptance
        assert "src/chat/MemoryPanel.tsx" in task.acceptance          # a file the repository holds stays
        story = _story(job_id)
        assert story["scope_findings"] == [{"key": "criterion_dropped", "path": "docs/chat_gedaechtnis_map.md",
                                            "text": PROBE_CRITERION}]


def test_a_criterion_naming_an_ordered_or_tracked_file_or_the_tasks_own_deliverable_stays(repo):
    from packages.orchestration.schemas.models import TaskPlan
    from packages.orchestration.task_deliverables import drop_unordered_criteria

    plan = TaskPlan.model_validate(json.loads(json.dumps({"schema_v": "task_plan_v1", "tasks": [{
        "id": "T001", "title": "t", "goal": "the goal", "est_tokens_band": "S", "depends_on": [],
        "files_hint": ["src/chat/MemoryInfo.tsx"],
        "acceptance": ["README.md says so", "src/chat/MemoryInfo.tsx exists", "notes/plan.md exists"]}]})))
    kept, findings = drop_unordered_criteria(plan, "Fix the info button; README.md stays current.", str(repo))
    assert kept.tasks[0].acceptance == ["README.md says so", "src/chat/MemoryInfo.tsx exists"]
    assert findings == [{"key": "criterion_dropped", "path": "notes/plan.md", "text": "notes/plan.md exists"}]
    alone, _found = drop_unordered_criteria(
        plan.model_copy(update={"tasks": [plan.tasks[0].model_copy(update={"acceptance": ["notes/plan.md exists"]})]}),
        "Fix the info button", str(repo))
    assert alone.tasks[0].acceptance == ["the goal"]                    # never an empty criterion list


# -- Rule 2: `shape: single-job`, or exactly one named file, is one job without milestones --------


def test_without_a_header_the_probe_still_walks_as_the_planners_milestones(repo, capsys, monkeypatch):
    data, asked = _walk(monkeypatch, capsys, PROBE_ORDER)
    assert (data["shape"], data["shape_source"]) == ("milestones", "planner")
    assert "mission_plan" in asked and len(data["job_ids"]) == 4


def test_the_header_shape_single_job_makes_the_probe_one_job_the_planner_cannot_split(
        repo, tmp_path, capsys, monkeypatch):
    order_file = tmp_path / "probe.md"
    order_file.write_text(f"---\nshape: single-job\n---\n{PROBE_ORDER}\n", encoding="utf-8")
    data, asked = _walk(monkeypatch, capsys, str(order_file))
    assert (data["shape"], data["shape_source"]) == ("one job", "the order")
    assert len(data["job_ids"]) == 1 and "mission_plan" not in asked
    plan_step = next(step for step in data["steps"] if step["name"] == "plan")
    assert "lane: full (the order's header says shape: single-job, so it is one job without milestones" in (
        plan_step["detail"])
    assert "not clearly one file" in plan_step["detail"]                # what routing alone read, kept


def test_a_header_shape_other_than_single_job_is_refused():
    from packages.orchestration.order_file import OrderFileError, parse_order_file_text

    assert parse_order_file_text("---\nshape: single-job\n---\nFix it", "o.md").shape == "single-job"
    with pytest.raises(OrderFileError) as refused:
        parse_order_file_text("---\nshape: milestones\n---\nFix it", "o.md")
    assert refused.value.error == "order_file_invalid_header"


def test_an_order_naming_exactly_one_file_is_one_job_whatever_routing_chose(repo):
    from packages.orchestration.do_lane import order_single_job_reason, select_do_lane

    order = f"{PROBE_ORDER} Die Datei src/chat/MemoryPanel.tsx."
    reason = order_single_job_reason(order)
    assert reason == "the order names exactly one file, src/chat/MemoryPanel.tsx"
    assert order_single_job_reason(PROBE_ORDER) == ""
    lane = select_do_lane(PROBE_ORDER, tracked_files=["src/chat/MemoryPanel.tsx", "README.md"], single_job=reason)
    assert lane.single_job == reason and lane.reason.startswith(reason)
    forced = select_do_lane(PROBE_ORDER, tracked_files=["README.md"], force_mission=True, single_job=reason)
    assert forced.single_job == ""                                      # the operator's flag still wins


# -- Rule 3: "keine neuen Dokumentationsdateien" -----------------------------------------------


def test_the_constraint_reaches_every_planned_tasks_criteria(repo, capsys, monkeypatch):
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.task_deliverables import NO_NEW_FILES_CRITERION

    data, _asked = _walk(monkeypatch, capsys, f"{PROBE_ORDER}\n\nKeine neuen Dokumentationsdateien.")
    for job_id in data["job_ids"]:
        assert all(NO_NEW_FILES_CRITERION in task.acceptance for task in load_job_plan(job_id).tasks)


def test_a_new_file_the_order_forbade_leaves_the_result_and_never_blocks(repo):
    """The run's own fence step (`pingpong_job.task_fence_refusal`) removes it and passes the task."""
    from packages.orchestration.pingpong_job import task_fence_refusal

    base_tree = _git(repo, "rev-parse", "HEAD^{tree}").strip()
    (repo / "docs").mkdir()
    (repo / "docs" / "chat_gedaechtnis_map.md").write_text("# map\n")
    (repo / "src" / "chat" / "MemoryPanel.tsx").write_text("export const Info = () => <button aria-haspopup>i</button>;\n")
    job = SimpleNamespace(job_id="f0000000000000a1", user_prompt=f"{PROBE_ORDER}\nKeine neuen Dokumentationsdateien.",
                          mission="", repo_path=str(repo), job_workspace_path=str(repo), job_initial_tree=base_tree,
                          metadata={}, tasks=[], fences=None)
    result = SimpleNamespace(task_id="T001", staged_files=["docs/chat_gedaechtnis_map.md", "src/chat/MemoryPanel.tsx"],
                             safe_diff_files=["./docs/chat_gedaechtnis_map.md"])
    assert task_fence_refusal(job, result) == ""
    assert not (repo / "docs" / "chat_gedaechtnis_map.md").exists()
    assert (result.staged_files, result.safe_diff_files) == (["src/chat/MemoryPanel.tsx"], [])
    assert job.metadata["scope_findings"] == [
        {"key": "file_removed", "path": "docs/chat_gedaechtnis_map.md", "text": None}]


def test_without_the_words_a_new_file_stays(repo):
    from packages.orchestration.task_deliverables import drop_unordered_new_files

    base_tree = _git(repo, "rev-parse", "HEAD^{tree}").strip()
    (repo / "notes.md").write_text("n\n")
    job = SimpleNamespace(job_id="f0000000000000a2", user_prompt=PROBE_ORDER, mission="", repo_path=str(repo),
                          job_workspace_path=str(repo), job_initial_tree=base_tree, metadata={})
    result = SimpleNamespace(staged_files=["notes.md"], safe_diff_files=[])
    assert drop_unordered_new_files(job, result, ["notes.md"]) == ["notes.md"]
    assert (repo / "notes.md").exists() and job.metadata == {}

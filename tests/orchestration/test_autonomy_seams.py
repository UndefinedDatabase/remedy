"""The mission loop's own starts, driven through `run_mission` and `dispatch_milestone_job`
exactly as the production seams call them (F078, DECISION F078 D2). No part of the gate itself
is mocked: a real `autonomy_start_scope` and a real `claim_loop_start` decide every move, over a
faked provider script, a faked dispatch and a faked executor — the same style
`test_orchestrator_loop.py` and `test_orchestrator_dispatch.py` use for the loop's own tests.
"""
from __future__ import annotations

import ast
import contextlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.autonomy_gate import (
    TERMINAL_AUTONOMY_DEFERRED,
    AutonomyPolicy,
    autonomy_start_scope,
    open_deferred_starts,
)
from packages.orchestration.mission_plan_schema import MISSION_PLAN_SCHEMA_V, Milestone, MissionPlan
from packages.orchestration.mission_state import create_mission, load_mission, set_mission_plan
from packages.orchestration.orchestrator_loop import (
    OUTCOME_RESUMED,
    TERMINAL_ITERATION_LIMIT,
    LoopLimits,
    MilestoneEvidence,
    MoveOutcome,
    read_ledger,
    run_mission,
)
from packages.orchestration.orchestrator_move_schema import ORCHESTRATOR_MOVE_SCHEMA_V

PROJECT = "p" * 32
REPO_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# helpers — the same shapes test_orchestrator_loop.py and test_orchestrator_dispatch.py use
# ---------------------------------------------------------------------------


def _plan() -> MissionPlan:
    """One milestone, no dependencies — all this module needs the plan for."""
    return MissionPlan(
        schema_v=MISSION_PLAN_SCHEMA_V,
        milestones=[Milestone(id="M001", goal="The outcome of M001 holds", rationale="M001 exists",
                              depends_on=[], jobs_draft=[{"title": "M001 work", "goal": "do M001",
                                                         "est_band": "M"}])],
        compiled=True, origin="provider",
    )


@pytest.fixture()
def mission(tmp_path):
    m = create_mission(PROJECT, "Ship the thing", root=tmp_path)
    set_mission_plan(PROJECT, m.id, _plan().model_dump(), tmp_path)
    return load_mission(PROJECT, m.id, tmp_path)


def _dispatch_json(**payload: str) -> str:
    return json.dumps({"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V, "kind": "dispatch_job", "payload": payload})


def _resume_json(**payload: str) -> str:
    return json.dumps({"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V, "kind": "resume_job", "payload": payload})


def _scripted(*responses: str):
    """A fake provider that replays a fixed script, one answer per call."""
    calls: list[str] = []

    def call_fn(prompt: str, attempt: int) -> str:
        calls.append(prompt)
        index = min(len(calls) - 1, len(responses) - 1)
        return responses[index]

    return call_fn


class _FakeJob:
    """The smallest thing the dispatch seam has to return: an id and no plan."""

    def __init__(self, job_id: str) -> None:
        self.job_id = job_id
        self.task_plan = None


class _FakeCycleRun:
    def __init__(self) -> None:
        self.terminal_status = "all_green"
        self.job_status = "completed"
        self.stop_reason = ""


def _executed(job: object) -> _FakeCycleRun:
    return _FakeCycleRun()


@pytest.fixture()
def dispatched():
    """Records every dispatch the loop makes, without creating a real job record."""
    seen: list[tuple[str, str, str]] = []

    def dispatch(project_id, mission_id, step, *, root=None, now=None):
        seen.append((project_id, mission_id, step))
        return _FakeJob(f"job-{len(seen):04d}")

    dispatch.seen = seen  # type: ignore[attr-defined]
    return dispatch


def _deferred_lines(root: Path) -> list[dict]:
    path = root / "autonomy" / "deferred_starts.jsonl"
    if not path.is_file():
        return []
    return [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _l2() -> AutonomyPolicy:
    return AutonomyPolicy("L2", None, None, None, None)


def _l3() -> AutonomyPolicy:
    return AutonomyPolicy("L3", None, None, None, None)


# ---------------------------------------------------------------------------
# (a), (d): the mission loop's own starts at L2, and a later manual start closing a deferral
# ---------------------------------------------------------------------------


class TestTheLoopsOwnStartsAtL2:
    def test_the_second_dispatch_is_deferred_then_a_new_scope_closes_it(
            self, tmp_path, mission, dispatched):
        # (a) one manual start, two dispatch moves: the first runs, the second is the LOOP's own
        # and L2 refuses it.
        call_fn = _scripted(
            _dispatch_json(milestone_id="M001", step="build M001"),
            _dispatch_json(milestone_id="M001", step="build M001 again"),
        )
        with autonomy_start_scope(_l2(), manual_starts=1):
            result = run_mission(
                mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
                call_fn=call_fn, root=tmp_path, dispatch=dispatched, execute=_executed,
                control_root_path=tmp_path / "control")

        assert dispatched.seen == [(PROJECT, mission.id, "build M001")]
        assert result.terminal == TERMINAL_AUTONOMY_DEFERRED
        assert result.detail == (
            "Autonomy level L2 does not let Remedy start work that comes from the mission loop; "
            "that needs level L3 or higher. The next job of milestone M001 waits for you: run "
            f"`remedy mission run {mission.id} --project {PROJECT}` to start it yourself."
        )
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert entries[-1]["outcome"]["status"] == TERMINAL_AUTONOMY_DEFERRED

        deferred = open_deferred_starts(root=tmp_path)
        assert len(deferred) == 1
        assert set(deferred[0]) == {
            "event", "at", "origin", "level", "project_id", "mission_id", "milestone_id",
        }
        assert deferred[0]["project_id"] == PROJECT
        assert deferred[0]["mission_id"] == mission.id
        assert deferred[0]["milestone_id"] == "M001"

        # (d) after (a): a NEW scope grants one manual start to the SAME mission, which still has
        # an open deferral. Taking the grant runs the dispatch and closes the deferral.
        call_fn_2 = _scripted(_dispatch_json(milestone_id="M001", step="build M001 by hand"))
        with autonomy_start_scope(_l2(), manual_starts=1):
            result_2 = run_mission(
                mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
                call_fn=call_fn_2, root=tmp_path, dispatch=dispatched, execute=_executed,
                control_root_path=tmp_path / "control")

        assert len(dispatched.seen) == 2
        assert result_2.terminal == TERMINAL_ITERATION_LIMIT
        assert open_deferred_starts(root=tmp_path) == []
        events = [line["event"] for line in _deferred_lines(tmp_path)]
        assert events == ["deferred", "taken"]


# ---------------------------------------------------------------------------
# (b), (c): L3 runs every dispatch; so does no scope at all (the gauntlet's own path)
# ---------------------------------------------------------------------------


class TestEveryDispatchRunsWhenNothingRefuses:
    def test_at_l3_both_dispatches_run(self, tmp_path, mission, dispatched):
        call_fn = _scripted(
            _dispatch_json(milestone_id="M001", step="build M001"),
            _dispatch_json(milestone_id="M001", step="build M001 again"),
        )
        with autonomy_start_scope(_l3(), manual_starts=1):
            result = run_mission(
                mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
                call_fn=call_fn, root=tmp_path, dispatch=dispatched, execute=_executed,
                control_root_path=tmp_path / "control")

        assert len(dispatched.seen) == 2
        assert result.terminal == TERMINAL_ITERATION_LIMIT
        assert open_deferred_starts(root=tmp_path) == []

    def test_outside_any_scope_both_dispatches_run_unchecked(self, tmp_path, mission, dispatched):
        """The gauntlet's own path: `run_mission` called with no `autonomy_start_scope` open."""
        call_fn = _scripted(
            _dispatch_json(milestone_id="M001", step="build M001"),
            _dispatch_json(milestone_id="M001", step="build M001 again"),
        )
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=call_fn, root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")

        assert len(dispatched.seen) == 2
        assert result.terminal == TERMINAL_ITERATION_LIMIT
        assert open_deferred_starts(root=tmp_path) == []


# ---------------------------------------------------------------------------
# (e): a refused start never reaches the upkeep check or the job's creation
# ---------------------------------------------------------------------------


class TestARefusedStartTouchesNothingDownstream:
    def test_neither_upkeep_nor_dispatch_is_asked(self, tmp_path, mission, dispatched, monkeypatch):
        from packages.orchestration import mission_upkeep

        calls: list[int] = []
        original = mission_upkeep.make_upkeep_job_if_due

        def counted(*args, **kwargs):
            calls.append(1)
            return original(*args, **kwargs)

        monkeypatch.setattr(mission_upkeep, "make_upkeep_job_if_due", counted)

        call_fn = _scripted(_dispatch_json(milestone_id="M001", step="build M001"))
        with autonomy_start_scope(_l2(), manual_starts=0):
            result = run_mission(
                mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
                call_fn=call_fn, root=tmp_path, dispatch=dispatched, execute=_executed,
                control_root_path=tmp_path / "control")

        assert result.terminal == TERMINAL_AUTONOMY_DEFERRED
        assert calls == []
        assert dispatched.seen == []


# ---------------------------------------------------------------------------
# (f): a resume move is not a start — it runs even with no manual start left
# ---------------------------------------------------------------------------


class TestAResumeMoveIsNotAStart:
    def test_a_resume_runs_with_no_manual_start_left_at_l2(self, tmp_path, mission, monkeypatch):
        from packages.orchestration import orchestrator_loop as loop

        resumed: list[tuple[str, str, str]] = []

        def fake_resume(project_id, mission_id, milestone_id, *, root=None, execute=None):
            resumed.append((project_id, mission_id, milestone_id))
            return MoveOutcome(status=OUTCOME_RESUMED, job_id="job-0001",
                               detail=f"job job-0001 resumed for {milestone_id}")

        monkeypatch.setattr(loop, "resume_milestone_job", fake_resume)

        def evidence(project_id, mission_id, milestone_id):
            return MilestoneEvidence(job_id="job-0001", job_state="paused")

        call_fn = _scripted(_resume_json(milestone_id="M001"))
        with autonomy_start_scope(_l2(), manual_starts=0):
            result = run_mission(
                mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
                call_fn=call_fn, root=tmp_path, execute=_executed, evidence=evidence,
                control_root_path=tmp_path / "control")

        assert resumed == [(PROJECT, mission.id, "M001")]
        assert result.terminal == TERMINAL_ITERATION_LIMIT


# ---------------------------------------------------------------------------
# (g): THE CALLERS — every production caller of the loop and of the dispatch is named
# ---------------------------------------------------------------------------


SCANNED_ROOTS = ("packages", "apps", "scripts")
WATCHED_CALLS = ("run_mission", "dispatch_milestone_job")

#: Every production caller of the two watched functions, and why each one is not checked (or, for
#: mission_cmd.py, how it IS). DECISION F078 D2 (5).
EXPECTED_CALLERS: dict[str, str] = {
    "apps/cli/commands/mission_cmd.py":
        "the operator's own `remedy mission run`; its run_mission call sits inside its own "
        "autonomy_start_scope, which grants the manual start of the first job",
    "packages/orchestration/orchestrator_loop.py":
        "the mission loop's own dispatch branch, which calls dispatch_milestone_job — the one "
        "place claim_loop_start is asked",
    "packages/orchestration/gauntlet_runner.py":
        "the harness whose campaign is the evidence L3 needs; it runs by the operator's own "
        "command against its own data root (DECISION F078 D2 (5))",
}


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _callers_of_the_loop() -> set[str]:
    """Every `.py` under packages/, apps/ and scripts/ that CALLS run_mission or
    dispatch_milestone_job, by name or by attribute."""
    found: set[str] = set()
    for root_name in SCANNED_ROOTS:
        for path in (REPO_ROOT / root_name).rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            names = {_call_name(n) for n in ast.walk(tree) if isinstance(n, ast.Call)}
            if names & set(WATCHED_CALLS):
                found.add(str(path.relative_to(REPO_ROOT)))
    return found


class TestTheCallersAreAllNamed:
    def test_every_production_caller_is_exactly_the_expected_set(self):
        assert _callers_of_the_loop() == set(EXPECTED_CALLERS)

    def test_the_gauntlet_runners_reason_is_the_authored_one(self):
        assert EXPECTED_CALLERS["packages/orchestration/gauntlet_runner.py"] == (
            "the harness whose campaign is the evidence L3 needs; it runs by the operator's own "
            "command against its own data root (DECISION F078 D2 (5))"
        )

    def test_mission_cmds_run_mission_call_sits_inside_the_scope(self):
        tree = ast.parse((REPO_ROOT / "apps/cli/commands/mission_cmd.py").read_text(encoding="utf-8"))
        scoped = False
        for node in ast.walk(tree):
            if isinstance(node, ast.With) and any(
                    isinstance(item.context_expr, ast.Call)
                    and getattr(item.context_expr.func, "id", "") == "autonomy_start_scope"
                    for item in node.items):
                scoped = scoped or any(
                    isinstance(n, ast.Call) and getattr(n.func, "id", "") == "run_mission"
                    for n in ast.walk(node))
        assert scoped


# ---------------------------------------------------------------------------
# (h): the end-to-end CLI refusal — a configuration the loop refuses ends the command
# before any job exists, and before a ledger is written
# ---------------------------------------------------------------------------


@contextlib.contextmanager
def _in_data_root(data_root: Path):
    from packages.orchestration.config import reset_config

    had = "REMEDY_DATA_DIR" in os.environ
    previous = os.environ.get("REMEDY_DATA_DIR", "")
    os.environ["REMEDY_DATA_DIR"] = str(data_root)
    reset_config()
    try:
        yield
    finally:
        if had:
            os.environ["REMEDY_DATA_DIR"] = previous
        else:
            os.environ.pop("REMEDY_DATA_DIR", None)
        reset_config()


def _make_project(data_root: Path) -> str:
    from packages.orchestration.project_registry import RemyProject, save_project

    with _in_data_root(data_root):
        p = RemyProject(name="Autonomy Seams", slug="autonomy-seams")
        save_project(p)
    return str(p.id)


def _start_mission(data_root: Path, project_id: str) -> str:
    with _in_data_root(data_root):
        return str(create_mission(project_id, "Ship the thing", root=data_root).id)


class TestTheCommandRefusesBeforeAnyJobExists:
    def test_l3_with_no_gauntlet_evidence_ends_the_run_as_mission_error(self, tmp_path):
        data_root = tmp_path / "data"
        data_root.mkdir()
        working_folder = tmp_path / "work"
        working_folder.mkdir()
        project_id = _make_project(data_root)
        mission_id = _start_mission(data_root, project_id)
        (working_folder / "remedy.toml").write_text(
            '[remedy]\nautonomy.level = "L3"\n', encoding="utf-8")

        env = {**os.environ, "PYTHONPATH": str(REPO_ROOT), "REMEDY_DATA_DIR": str(data_root)}
        env.pop("REMEDY_PROJECT", None)
        proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "mission", "run", mission_id,
             "--project", project_id, "--no-llm", "--json"],
            cwd=str(working_folder), capture_output=True, text=True, timeout=120, env=env,
            stdin=subprocess.DEVNULL,
        )

        assert proc.returncode == 1
        body = json.loads(proc.stdout)
        assert body["error"] == "mission_error"
        assert body["message"] == (
            "Autonomy level L3 in remedy.toml lets Remedy start work on its own, so it needs the "
            "gauntlet that proved it can: set autonomy.gauntlet_evidence to the matrix.json of a "
            "gauntlet attempt that passed."
        )
        assert read_ledger(project_id, mission_id, data_root) == []

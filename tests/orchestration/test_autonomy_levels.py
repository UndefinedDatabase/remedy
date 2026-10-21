"""F078 T003, DECISION F078 D5 — each autonomy level end to end, and every gate of a mission at L5.

The first half loads each level from a real `remedy.toml` and drives the two seams that start work
today, the mission loop's dispatch and `claim_idea_start`, so each level shows exactly the starts
its row of the matrix adds. The second half calls six existing tests of the gates a mission meets,
as they are written and with their own fixtures, inside a start scope at L5 that grants one manual
start, with `claim_loop_start` watched: each gate must still fire, and the start check must have
been asked once per dispatch and have allowed every one.
"""
from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest

from packages.orchestration import autonomy_gate
from packages.orchestration.autonomy_gate import (
    START_ORIGIN_IDEA,
    START_ORIGIN_MANUAL,
    START_ORIGIN_ORCHESTRATOR,
    START_ORIGIN_ORDER_FILE,
    TERMINAL_AUTONOMY_DEFERRED,
    AutonomyPolicy,
    AutonomyStartVerdict,
    autonomy_may_start,
    autonomy_start_scope,
    claim_idea_start,
    load_autonomy_policy,
)
from packages.orchestration.config import load_config
from packages.orchestration.mission_state import create_mission, load_mission, set_mission_plan
from packages.orchestration.orchestrator_loop import TERMINAL_ITERATION_LIMIT, LoopLimits, run_mission
from tests.orchestration import test_orchestrator_dispatch as dispatch_tests
from tests.orchestration import test_orchestrator_loop as loop_tests
from tests.orchestration import test_watchdog as watchdog_tests
from tests.orchestration.test_autonomy_seams import PROJECT, _dispatch_json, _executed, _FakeJob, _plan, _scripted

# The fixtures the six re-run tests take, under their own names so pytest finds them here.
from tests.orchestration.test_orchestrator_dispatch import recorder  # noqa: F401
from tests.orchestration.test_orchestrator_loop import dispatched, mission  # noqa: F401
from tests.orchestration.test_watchdog import data_root, loop_mission  # noqa: F401

REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Each level end to end (DECISION F078 D5 (1))
# ---------------------------------------------------------------------------

#: level -> (the mission loop's second dispatch runs, a low-effort idea draft starts).
EXPECTED_STARTS_BY_LEVEL: dict[str, tuple[bool, bool]] = {
    "L2": (False, False),
    "L3": (True, False),
    "L4": (True, False),
    "L5": (True, True),
}


def _level_config(tmp_path: Path, level: str):
    """A real `remedy.toml` at LEVEL; from L3 with a passing gauntlet matrix and a decision record."""
    lines = ["[remedy]"]
    if level != "L2":
        (tmp_path / "matrix.json").write_text(json.dumps({"passed": True}), encoding="utf-8")
        (tmp_path / "adr.md").write_text("why the level was raised\n", encoding="utf-8")
        lines += [f'autonomy.level = "{level}"', 'autonomy.gauntlet_evidence = "matrix.json"',
                  'autonomy.change_adr = "adr.md"']
    project = tmp_path / "remedy.toml"
    project.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return load_config(project_path=project, user_path=tmp_path / "absent.toml")


@pytest.mark.parametrize("level", list(EXPECTED_STARTS_BY_LEVEL))
def test_each_level_starts_exactly_what_its_row_allows(level: str, tmp_path: Path) -> None:
    loop_runs_on, idea_starts = EXPECTED_STARTS_BY_LEVEL[level]
    config = _level_config(tmp_path, level)
    policy = load_autonomy_policy(config, root=tmp_path / "data")
    assert policy.level == level

    created = create_mission(PROJECT, "Ship the thing", root=tmp_path)
    set_mission_plan(PROJECT, created.id, _plan().model_dump(), tmp_path)
    seen: list[str] = []

    def dispatch(project_id, mission_id, step, *, root=None, now=None):
        seen.append(step)
        return _FakeJob(f"job-{len(seen):04d}")

    with autonomy_start_scope(policy, manual_starts=1):
        result = run_mission(
            load_mission(PROJECT, created.id, tmp_path).id, LoopLimits(max_iterations=2),
            project_id=PROJECT, call_fn=_scripted(_dispatch_json(milestone_id="M001", step="work")),
            root=tmp_path, dispatch=dispatch, execute=_executed, control_root_path=tmp_path / "control")

    assert len(seen) == (2 if loop_runs_on else 1)
    assert result.terminal == (TERMINAL_ITERATION_LIMIT if loop_runs_on else TERMINAL_AUTONOMY_DEFERRED)

    verdict = claim_idea_start(policy, "idea-1", effort_band="low", estimated_usd=0.0,
                               config=config, root=tmp_path / "data")
    assert verdict.allowed is idea_starts


def test_l4_adds_only_the_recurring_order_file_to_l3() -> None:
    for origin in (START_ORIGIN_MANUAL, START_ORIGIN_ORCHESTRATOR, START_ORIGIN_IDEA):
        assert autonomy_may_start(origin, "L4").allowed is autonomy_may_start(origin, "L3").allowed
    assert autonomy_may_start(START_ORIGIN_ORDER_FILE, "L3").allowed is False
    assert autonomy_may_start(START_ORIGIN_ORDER_FILE, "L4").allowed is True


def test_no_module_but_the_gate_names_the_order_file_or_the_idea_origin() -> None:
    """No starter of either origin exists yet; one that arrives must bring its own proof here."""
    names = ("START_ORIGIN_ORDER_FILE", "START_ORIGIN_IDEA", '"order-file"', "claim_idea_start")
    found = sorted(
        f"{path.relative_to(REPO_ROOT)}: {name}"
        for root in ("packages", "apps", "scripts")
        for path in (REPO_ROOT / root).rglob("*.py")
        if path.name != "autonomy_gate.py"
        for name in names
        if name in path.read_text(encoding="utf-8")
    )
    assert found == []


# ---------------------------------------------------------------------------
# Every gate of a mission run still fires at L5 (DECISION F078 D5 (2))
# ---------------------------------------------------------------------------


@pytest.fixture()
def at_l5(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[AutonomyStartVerdict | None]]:
    """A start scope at L5 with one manual start, and every answer of `claim_loop_start` recorded."""
    real = autonomy_gate.claim_loop_start
    answers: list[AutonomyStartVerdict | None] = []

    def watched(*args, **kwargs):
        answer = real(*args, **kwargs)
        answers.append(answer)
        return answer

    monkeypatch.setattr(autonomy_gate, "claim_loop_start", watched)
    with autonomy_start_scope(AutonomyPolicy("L5", None, None, None, None), manual_starts=1):
        yield answers


def _asked_and_allowed(answers: list[AutonomyStartVerdict | None], dispatches: int) -> None:
    assert len(answers) == dispatches
    assert all(answer is not None and answer.allowed for answer in answers)
    expected = [START_ORIGIN_MANUAL] + [START_ORIGIN_ORCHESTRATOR] * (dispatches - 1)
    assert [answer.origin for answer in answers] == expected


def test_the_watchdog_still_pauses_a_mission_at_l5(loop_mission, data_root, at_l5) -> None:
    watchdog_tests.test_three_dispatches_in_a_row_trip_no_progress_through_the_loop(loop_mission, data_root)
    _asked_and_allowed(at_l5, 3)


def test_a_paused_mission_still_dispatches_nothing_at_l5(loop_mission, data_root, at_l5) -> None:
    watchdog_tests.test_the_paused_mission_dispatches_nothing_on_the_next_run(loop_mission, data_root)
    _asked_and_allowed(at_l5, 3)


def test_the_iteration_limit_still_ends_a_run_at_l5(tmp_path, mission, dispatched, at_l5) -> None:
    loop_tests.TestTheLoopTerminals().test_the_iteration_limit_is_a_normal_terminal(tmp_path, mission, dispatched)
    _asked_and_allowed(at_l5, 3)


def test_the_operators_stop_still_halts_a_run_at_l5(tmp_path, mission, dispatched, at_l5) -> None:
    loop_tests.TestHumanOverridesWinInstantly().test_a_stop_request_between_iterations_halts_within_one_iteration(
        tmp_path, mission, dispatched)
    _asked_and_allowed(at_l5, 1)


def test_two_blocked_completions_still_escalate_at_l5(tmp_path, mission, dispatched, at_l5) -> None:
    loop_tests.TestTheSecondBlockedCompletionEscalates().test_two_blocked_completions_in_a_row_escalate(
        tmp_path, mission, dispatched)
    _asked_and_allowed(at_l5, 2)


def test_a_gated_plan_is_still_approved_audited_at_l5(data_root, recorder, at_l5) -> None:
    dispatch_tests.TestTheAuditedApprovalOfADispatchedJob(
    ).test_a_job_waiting_at_its_plan_gate_is_approved_audited_before_it_runs(data_root, recorder)
    _asked_and_allowed(at_l5, 1)

"""F070 T003 — a two-milestone mission runs end to end, unattended.

The feature's DONE criterion, staged once: a fake-provider mission with two
milestones, three jobs and one escalated decision runs to ``achieved``, and
every iteration leaves a ledger entry a human can audit.

The scenario, in order:

  Run 1   dispatch M001 "build the core" -> job 1; job 1 finishes and its DoD
          is met; declare M001 done (allowed); dispatch M002 "polish" -> job 2;
          job 2 raises ONE decision; the orchestrator waits -> the run
          terminates ``waiting_on_decisions``.
  Human   answers that decision — outside the loop, through the same verb a
          person uses.
  Run 2   dispatch M002 "finish after the answer" -> job 3; job 3 finishes and
          its DoD is met; declare M002 done; declare the mission achieved.

**Everything runs through the public verbs.** The jobs are created by the
loop's own dispatch (``mission_state.continue_mission``), their terminal state
is written with ``storage.save_job``, their Definition of Done is compiled by
the F061 compiler and recorded with ``dod_gate.store_dod`` /
``save_gate_result``, and the decision is raised and answered with
``escalation.enqueue_task_decision`` / ``answer_task_decision``. The loop reads
all of it back through ``collect_milestone_evidence`` — the production path,
with no ``evidence`` seam override anywhere in this file. A test-only bypass of
the evaluator would fake the acceptance rather than prove it.

What is deliberately NOT re-staged here: the DoD gate's own check EXECUTION
(F061's tested territory — this records the gate's verdict exactly as
``run_job_gate`` does, without running external check commands), and the
refused-twice escalation path (pinned by unit tests in
``test_orchestrator_loop.py``).

No network, no real provider, no process: the "orchestrator" is a local
callable replaying a script, and every path lives under ``tmp_path``.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import UUID

import pytest

from packages.core.models import RunState
from packages.orchestration.dod_compiler import compile_dod
from packages.orchestration.dod_gate import GateResult, save_gate_result, store_dod
from packages.orchestration.escalation import (
    answer_task_decision,
    enqueue_task_decision,
    open_task_decisions,
)
from packages.orchestration.mission_plan_schema import (
    MISSION_PLAN_SCHEMA_V,
    Milestone,
    MissionPlan,
)
from packages.orchestration.mission_state import (
    MISSION_STATUS_ACHIEVED,
    create_mission,
    load_mission,
    set_mission_plan,
)
from packages.orchestration.orchestrator_loop import (
    TERMINAL_ACHIEVED,
    TERMINAL_WAITING,
    LoopLimits,
    done_milestones,
    ledger_path,
    open_mission_decisions,
    read_ledger,
    render_ledger,
    run_mission,
)
from packages.orchestration.orchestrator_move_schema import (
    ORCHESTRATOR_MOVE_SCHEMA_V,
)
from packages.orchestration.schemas.models import FLIGHT_PLAN_SCHEMA_V, FlightPlan
from packages.orchestration.storage import load_job, save_job

PROJECT = "p-f070-e2e"
GOAL = "Ship the demo end to end"


# ---------------------------------------------------------------------------
# the world the loop acts on — built with the same verbs a real run uses
# ---------------------------------------------------------------------------


def _move(kind: str, rationale: str = "", **payload: str) -> str:
    body: dict[str, object] = {"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V,
                               "kind": kind, "rationale": rationale}
    if payload:
        body["payload"] = payload
    return json.dumps(body)


def _two_milestone_plan() -> dict:
    return MissionPlan(
        schema_v=MISSION_PLAN_SCHEMA_V,
        milestones=[
            Milestone(id="M001",
                      goal="The demo's core path works end to end",
                      rationale="nothing ships without the core",
                      depends_on=[],
                      jobs_draft=[{"title": "core", "goal": "build the core",
                                   "est_band": "M"}]),
            Milestone(id="M002",
                      goal="The demo is presentable to an audience",
                      rationale="a working core is not yet a demo",
                      depends_on=["M001"],
                      jobs_draft=[{"title": "polish", "goal": "polish it",
                                   "est_band": "S"}]),
        ],
        compiled=True,
        origin="provider",
    ).model_dump()


class _NoExecution:
    """What the executor seam hands back, reduced to what the loop reads."""

    terminal_status = "all_green"
    job_status = "completed"
    stop_reason = ""


def _no_execution(job):
    """The executor seam, injected so this test stays provider-free (R-0182).

    R-0186 made a dispatch also RUN its job through
    ``long_run_executor.run_cycles``, whose production default builds a real
    OllamaBuilder. This scenario drives jobs to terminal itself, through
    ``_finish_job_with_dod_met``, so the double does that job's one other
    observable thing: it takes the job OUT of ``planned``. A real executor
    always does — and the R-0186 re-dispatch guard reads exactly that state.
    ``paused`` is the honest state here: this scenario's second job asks a
    human, and the loop's next legal move after the answer is a dispatch.
    """
    job.state = RunState.PAUSED
    save_job(job)
    return _NoExecution()


def _finish_job_with_dod_met(job_id: str) -> None:
    """Take a dispatched job to a terminal state with its DoD met.

    Every step is an existing verb: the job's own record via ``save_job``, its
    Definition of Done compiled by the F061 compiler (deterministic path — no
    provider), and the gate's verdict recorded exactly where ``run_job_gate``
    records it. The gate's check EXECUTION is not re-run here; what this test
    exercises is the loop READING a recorded verdict back.
    """
    job = load_job(UUID(job_id))
    job.state = RunState.COMPLETED
    for task in job.tasks:
        task.status = RunState.COMPLETED
    save_job(job)

    plan = FlightPlan.model_validate({
        "schema_v": FLIGHT_PLAN_SCHEMA_V,
        "tasks": [{"id": "T1", "title": "the work", "goal": "do the work",
                   "acceptance": ["the work is done"], "depends_on": [],
                   "est_tokens_band": "M", "files_hint": []}],
    })
    result = compile_dod({"goal": "the work", "context_refs": [],
                          "constraints": [], "acceptance_hints": []}, plan)
    store_dod(job_id, result.dod)
    save_gate_result(job_id, GateResult(released=True))


def _raise_one_decision(job_id: str, question: str) -> str:
    """Raise ONE open decision on a job, through the existing escalation verb."""
    job = load_job(UUID(job_id))
    record = enqueue_task_decision(
        job,
        task_id=job.tasks[-1].id,
        question=question,
        options=("blue", "green"),
        impact="the polish cannot start until someone chooses",
        now=datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc))
    save_job(job)
    return str(record["decision_id"])


def _answer_the_decision(job_id: str, decision_id: str, answer: str) -> None:
    """A human's move: answer through the same verb the CLI uses."""
    job = load_job(UUID(job_id))
    record = answer_task_decision(
        job, decision_id, answer=answer,
        now=datetime(2026, 8, 3, 12, 5, tzinfo=timezone.utc))
    assert record is not None, "the decision to answer was not found"
    save_job(job)


class _ScriptedOrchestrator:
    """A fake provider: one scripted move per iteration, with a world hook.

    ``before`` runs immediately before the move it is paired with, which is how
    this test represents the world advancing BETWEEN iterations — jobs
    finishing, decisions being raised — without reaching inside the loop.
    """

    def __init__(self, script):
        self.script = list(script)
        self.prompts: list[str] = []

    def __call__(self, prompt: str, attempt: int) -> str:
        self.prompts.append(prompt)
        before, response = self.script[len(self.prompts) - 1]
        if before is not None:
            before()
        return response


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    """One data root for jobs, missions and evidence alike."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    return tmp_path


@pytest.fixture()
def mission(data_root):
    m = create_mission(PROJECT, GOAL)
    set_mission_plan(PROJECT, m.id, _two_milestone_plan())
    return load_mission(PROJECT, m.id)


@pytest.fixture()
def e2e(data_root, mission):
    """Run the whole scenario once and hand back everything it produced."""
    control = data_root / "control"
    state: dict[str, object] = {}

    def link(index: int) -> str:
        return load_mission(PROJECT, mission.id).job_links[index].job_id

    def finish_first_job():
        _finish_job_with_dod_met(link(0))

    def raise_decision_on_second_job():
        state["decision_job"] = link(1)
        state["decision_id"] = _raise_one_decision(
            link(1), "Which accent colour should the demo use?")

    run_one = _ScriptedOrchestrator([
        (None, _move("dispatch_job", "M001 is ready and nothing blocks it",
                     milestone_id="M001", step="build the core")),
        (finish_first_job,
         _move("declare_milestone_done", "the core job finished green",
               milestone_id="M001")),
        (None, _move("dispatch_job", "M001 is done, so M002 is unblocked",
                     milestone_id="M002", step="polish")),
        (raise_decision_on_second_job,
         _move("wait_on_decisions", "the polish job is asking a human")),
    ])
    result_one = run_mission(
        mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
        call_fn=run_one, execute=_no_execution, control_root_path=control)

    # Captured BEFORE the answer: what a human walking up to the paused
    # mission would see.
    open_at_pause = open_mission_decisions(load_mission(PROJECT, mission.id))

    _answer_the_decision(str(state["decision_job"]),
                         str(state["decision_id"]), "blue")

    def finish_third_job():
        _finish_job_with_dod_met(link(2))

    run_two = _ScriptedOrchestrator([
        (None, _move("dispatch_job", "the decision is answered; M002 resumes",
                     milestone_id="M002", step="finish after the answer")),
        (finish_third_job,
         _move("declare_milestone_done", "the polish job finished green",
               milestone_id="M002")),
        (None, _move("declare_mission_achieved", "both milestones are done")),
    ])
    result_two = run_mission(
        mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
        call_fn=run_two, execute=_no_execution, control_root_path=control)

    return {
        "mission_id": mission.id,
        "run_one": result_one,
        "run_two": result_two,
        "decision_id": state["decision_id"],
        "open_at_pause": open_at_pause,
        "ledger": read_ledger(PROJECT, mission.id),
        "final": load_mission(PROJECT, mission.id),
        "prompts": run_one.prompts + run_two.prompts,
    }


# ---------------------------------------------------------------------------
# the run reaches achieved
# ---------------------------------------------------------------------------


class TestTheMissionRunsToAchieved:
    def test_run_one_terminates_waiting_on_the_human(self, e2e):
        assert e2e["run_one"].terminal == TERMINAL_WAITING
        assert e2e["run_one"].iterations == 4

    def test_run_two_reaches_achieved(self, e2e):
        assert e2e["run_two"].terminal == TERMINAL_ACHIEVED
        assert e2e["run_two"].iterations == 3

    def test_the_mission_record_says_achieved(self, e2e):
        assert e2e["final"].status == MISSION_STATUS_ACHIEVED

    def test_both_milestones_are_recorded_done(self, e2e):
        assert set(done_milestones(e2e["final"])) == {"M001", "M002"}

    def test_three_distinct_jobs_are_linked_to_the_mission(self, e2e):
        job_ids = [link.job_id for link in e2e["final"].job_links]
        assert len(job_ids) == 3
        assert len(set(job_ids)) == 3

    def test_the_first_link_is_initial_and_the_rest_follow_up(self, e2e):
        roles = [link.role for link in e2e["final"].job_links]
        assert roles == ["initial", "follow_up", "follow_up"]


# ---------------------------------------------------------------------------
# the escalated decision
# ---------------------------------------------------------------------------


class TestTheEscalatedDecision:
    def test_exactly_one_decision_is_open_when_the_run_pauses(self, e2e):
        """What a human walking up to the paused mission sees.

        The decision cannot appear in a run-1 prompt: it is raised while
        iteration 4 is deciding, and that iteration's context was assembled
        before the call. The loop reading open decisions every iteration is
        pinned in test_orchestrator_loop.py; what matters here is that the run
        stopped with the question genuinely outstanding.
        """
        assert len(e2e["open_at_pause"]) == 1
        assert "Which accent colour" in e2e["open_at_pause"][0]["question"]
        assert e2e["open_at_pause"][0]["decision_id"] == e2e["decision_id"]

    def test_the_decision_is_answered_and_no_longer_open(self, e2e):
        job_ids = [link.job_id for link in e2e["final"].job_links]
        still_open = []
        for job_id in job_ids:
            still_open.extend(open_task_decisions(load_job(UUID(job_id))))
        assert still_open == []

    def test_the_second_run_started_only_after_the_answer(self, e2e):
        """The first prompt of run 2 shows no open decision."""
        assert "None open." in e2e["prompts"][4]


# ---------------------------------------------------------------------------
# the ledger — one file, both runs, auditable
# ---------------------------------------------------------------------------


class TestTheLedgerSpansBothRuns:
    def test_there_is_exactly_one_ledger_file(self, e2e, data_root):
        path = ledger_path(PROJECT, e2e["mission_id"])
        assert path.is_file()
        assert sorted(p.name for p in path.parent.glob("ledger*")) == \
            [path.name]

    def test_every_iteration_is_numbered_once_across_both_runs(self, e2e):
        numbers = [entry["iteration"] for entry in e2e["ledger"]]
        assert numbers == [1, 2, 3, 4, 5, 6, 7], (
            "iteration numbering must continue across runs, not restart")

    def test_every_entry_carries_a_context_digest_and_cost(self, e2e):
        for entry in e2e["ledger"]:
            assert entry["context_digest"].startswith("sha256:")
            assert entry["cost"]["calls"] == 1
            assert "usage_source" in entry["cost"]
            assert entry["protocol_version"]
            assert entry["recorded_at"]

    def test_the_ledger_records_the_moves_in_the_order_they_happened(self, e2e):
        assert [e["move"]["kind"] for e in e2e["ledger"]] == [
            "dispatch_job",
            "declare_milestone_done",
            "dispatch_job",
            "wait_on_decisions",
            "dispatch_job",
            "declare_milestone_done",
            "declare_mission_achieved",
        ]

    def test_no_move_was_refused(self, e2e):
        """Every move in this scenario is legitimate and the evaluator agrees."""
        statuses = [e["outcome"]["status"] for e in e2e["ledger"]]
        assert "refused" not in statuses
        assert "escalated" not in statuses


class TestAHumanCanReconstructTheRun:
    """The acceptance bar: the ledger reconstructs every decision without code."""

    @pytest.fixture()
    def rendered(self, e2e):
        return render_ledger(e2e["ledger"])

    @pytest.mark.parametrize("kind", [
        "dispatch_job", "declare_milestone_done", "wait_on_decisions",
        "declare_mission_achieved",
    ])
    def test_every_move_kind_used_is_named(self, rendered, kind):
        assert kind in rendered

    def test_the_waiting_terminal_is_visible(self, rendered):
        assert TERMINAL_WAITING in rendered

    def test_the_work_each_job_was_sent_to_do_is_visible(self, rendered):
        for step in ("build the core", "polish", "finish after the answer"):
            assert step in rendered

    def test_the_milestones_are_visible(self, rendered):
        assert "M001" in rendered and "M002" in rendered

    def test_the_reason_for_each_move_is_visible(self, rendered):
        for why in ("M001 is ready and nothing blocks it",
                    "the core job finished green",
                    "the polish job is asking a human",
                    "both milestones are done"):
            assert why in rendered

    def test_every_dispatched_job_id_is_visible(self, e2e, rendered):
        for link in e2e["final"].job_links:
            assert link.job_id in rendered

    def test_the_achieved_terminal_is_visible(self, rendered):
        assert TERMINAL_ACHIEVED in rendered

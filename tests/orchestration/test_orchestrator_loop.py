"""F070 — the orchestrator loop: move schema, context assembly, ledger, loop.

What the order requires proof of (T001):

  * the move schema is validated through the EXISTING structured-call /
    schema-registry mechanism, with no second validation path;
  * an UNKNOWN kind (``create_mission``) fails as a PARSE-class failure — the
    authority boundary is the schema's shape, not the prompt's wording;
  * context assembly puts the dossier FIRST and is byte-stable while the
    mission does not change (cache-stable prefix discipline);
  * the ledger is append-only, one entry per iteration, carrying the context
    digest, the move, the outcome and cost actuals — and renders to something
    a human can audit without reading code;
  * the loop reads the protocol document and never writes it;
  * each move kind is exercised at least once;
  * a stop request between iterations halts the loop within one iteration.

And of T002:

  * every ADVANCING move is evaluated before it executes — a job for an
    already-done milestone, a milestone claim whose job never finished or
    whose Definition of Done was not met, and an "achieved" claim with open
    milestones are all refused with a recorded reason;
  * a refused move re-prompts ONCE with that reason as feedback and a second
    refusal escalates through the existing escalation verb — never a silent
    loop;
  * the dossier update call runs every iteration;
  * every era fixture class (R-0141/43/45, R-0144, R-0146, R-0147, R-0148)
    is flagged by the evaluate step and the loop refuses to advance on it —
    the detector-level tests live in ``test_era_integrity.py``.

Every provider here is a local callable returning recorded text — no network,
no process, no real model. Every test writes into ``tmp_path``: the mission
root is passed explicitly via ``root=``, so the repository's real data root is
never touched.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration.mission_compiler import mission_plan_of
from packages.orchestration.mission_plan_schema import (
    MISSION_PLAN_SCHEMA_V,
    Milestone,
    MissionPlan,
)
from packages.orchestration.mission_state import (
    MissionNotFoundError,
    create_mission,
    load_mission,
    mission_evidence_dir,
    set_mission_plan,
    set_mission_status,
)
from packages.orchestration.orchestrator_loop import (
    CONFIG_KEY_MAX_ITERATIONS,
    DEFAULT_MAX_ITERATIONS,
    DOSSIER_FILENAME,
    LEDGER_FILENAME,
    MILESTONES_DONE_KEY,
    OUTCOME_ITERATION_RETRYING,
    OUTCOME_REFUSED,
    PROTOCOL_DOC_RELATIVE,
    PROTOCOL_VERSION,
    SECTION_DECISIONS,
    SECTION_DOSSIER,
    SECTION_FEEDBACK,
    SECTION_PLAN,
    SECTION_REPORT,
    TERMINAL_ABORTED,
    TERMINAL_ACHIEVED,
    TERMINAL_ESCALATED,
    TERMINAL_INVALID_MOVE,
    TERMINAL_ITERATION_FAILED,
    TERMINAL_ITERATION_LIMIT,
    TERMINAL_NO_PROVIDER,
    TERMINAL_NOT_ACTIVE,
    TERMINAL_STOPPED,
    TERMINAL_WAITING,
    USAGE_UNMEASURED,
    LedgerEntry,
    LoopLimits,
    MilestoneEvidence,
    attach_milestone_dod,
    run_gate_for_job,
    JobExecution,
    MoveOutcome,
    blocked_completion,
    working_milestone,
    BOUNDARY_FAILURES_BEFORE_ESCALATION,
    RETRYABLE_FAILURE_CLASSES,
    SECTION_DIRECTIVES,
    released_milestone_directives,
    all_milestones_done,
    append_ledger_entry,
    assemble_context,
    build_orchestrator_prompt,
    build_orchestrator_system_prompt,
    context_digest,
    dispatched_job_for,
    done_milestones,
    escalate_repeated_refusal,
    evaluate_dispatch,
    evaluate_milestone_done,
    evaluate_move,
    ledger_path,
    loop_limits_from_config,
    mark_milestone_done,
    measure_call_cost,
    orchestrator_protocol_text,
    protocol_document_path,
    read_ledger,
    render_ledger,
    render_mission_dossier,
    resolve_mission_project,
    run_mission,
)
from packages.orchestration.orchestrator_move_schema import (
    MAX_PAYLOAD_VALUE_CHARS,
    ORCHESTRATOR_MOVE_KINDS,
    ORCHESTRATOR_MOVE_SCHEMA_V,
    OrchestratorMove,
)
from packages.orchestration.safe_points import request_stop, stop_requested
from packages.orchestration.schemas.models import SCHEMA_REGISTRY
from packages.orchestration.schemas.validation import validate_response
from packages.orchestration.structured_outputs import (
    PARSE_ERROR_CLASS,
    run_structured_call,
)

PROJECT = "p-f070"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _plan(*milestones: tuple[str, tuple[str, ...]]) -> MissionPlan:
    """A minimal two-field plan: ``(id, depends_on)`` per milestone."""
    return MissionPlan(
        schema_v=MISSION_PLAN_SCHEMA_V,
        milestones=[
            Milestone(
                id=mid,
                goal=f"The outcome of {mid} holds",
                rationale=f"{mid} exists",
                depends_on=list(deps),
                jobs_draft=[{"title": f"{mid} work", "goal": f"do {mid}",
                             "est_band": "M"}],
            )
            for mid, deps in milestones
        ],
        compiled=True,
        origin="provider",
    )


@pytest.fixture()
def mission(tmp_path):
    """A persisted mission with a compiled two-milestone plan."""
    m = create_mission(PROJECT, "Ship the thing", root=tmp_path)
    body = _plan(("M001", ()), ("M002", ("M001",))).model_dump()
    set_mission_plan(PROJECT, m.id, body, tmp_path)
    return load_mission(PROJECT, m.id, tmp_path)


def _move_json(kind: str, **payload: str) -> str:
    body = {"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V, "kind": kind}
    if payload:
        body["payload"] = payload
    return json.dumps(body)


# ---------------------------------------------------------------------------
# the move schema — the authority boundary
# ---------------------------------------------------------------------------


class TestTheMoveSchema:
    def test_registered_in_the_one_schema_registry(self):
        assert SCHEMA_REGISTRY[ORCHESTRATOR_MOVE_SCHEMA_V] is OrchestratorMove

    @pytest.mark.parametrize("kind", ORCHESTRATOR_MOVE_KINDS)
    def test_every_kind_validates_through_the_existing_validator(self, kind):
        payload = {
            "dispatch_job": {"milestone_id": "M001", "step": "do the work"},
            "declare_milestone_done": {"milestone_id": "M001"},
            "abort_with_reason": {"reason": "the plan is wrong"},
        }.get(kind, {})
        result = validate_response(OrchestratorMove, _move_json(kind, **payload))
        assert result.ok, result.hint
        assert result.value.kind == kind

    def test_an_unknown_kind_is_a_parse_class_failure(self):
        """`create_mission` is the move the loop must never be able to make."""
        result = validate_response(
            OrchestratorMove,
            json.dumps({"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V,
                        "kind": "create_mission",
                        "payload": {"goal": "a goal I gave myself"}}))
        assert not result.ok

    def test_an_unknown_kind_through_the_structured_call_is_parse_class(self):
        """End to end: the same refusal reached through the real call path."""
        calls: list[str] = []

        def call_fn(prompt: str, attempt: int) -> str:
            calls.append(prompt)
            return json.dumps({"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V,
                               "kind": "create_mission", "payload": {}})

        outcome = run_structured_call(OrchestratorMove, "decide", call_fn)
        assert outcome.ok is False
        assert outcome.error_class == PARSE_ERROR_CLASS
        # One parse retry, and no more — the shared ceiling, not a local one.
        assert len(calls) == 2

    def test_no_kind_can_create_a_mission_or_edit_a_goal(self):
        for forbidden in ("create_mission", "edit_goal", "set_goal",
                          "rewrite_plan", "add_milestone"):
            assert forbidden not in ORCHESTRATOR_MOVE_KINDS

    def test_missing_required_payload_key_is_refused(self):
        assert not validate_response(
            OrchestratorMove, _move_json("dispatch_job",
                                         milestone_id="M001")).ok
        assert not validate_response(
            OrchestratorMove, _move_json("declare_milestone_done")).ok
        assert not validate_response(
            OrchestratorMove, _move_json("abort_with_reason")).ok

    def test_blank_required_payload_value_is_refused(self):
        assert not validate_response(
            OrchestratorMove,
            _move_json("dispatch_job", milestone_id="M001", step="   ")).ok

    def test_an_oversized_payload_value_is_refused(self):
        assert not validate_response(
            OrchestratorMove,
            _move_json("abort_with_reason",
                       reason="x" * (MAX_PAYLOAD_VALUE_CHARS + 1))).ok

    def test_an_unexpected_field_is_forbidden(self):
        assert not validate_response(
            OrchestratorMove,
            json.dumps({"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V,
                        "kind": "wait_on_decisions",
                        "authority": "full"})).ok

    def test_schema_v_is_required(self):
        assert not validate_response(
            OrchestratorMove, json.dumps({"kind": "wait_on_decisions"})).ok


# ---------------------------------------------------------------------------
# the protocol document
# ---------------------------------------------------------------------------


class TestTheProtocolDocument:
    def test_the_document_is_versioned_in_the_repo(self):
        assert protocol_document_path().is_file()
        assert PROTOCOL_DOC_RELATIVE.endswith(".md")

    def test_the_system_prompt_is_generated_from_it(self):
        prompt = build_orchestrator_system_prompt()
        assert PROTOCOL_VERSION in prompt
        assert PROTOCOL_DOC_RELATIVE in prompt
        assert orchestrator_protocol_text() in prompt

    def test_the_document_names_every_move_kind(self):
        text = orchestrator_protocol_text()
        for kind in ORCHESTRATOR_MOVE_KINDS:
            assert kind in text, f"protocol document does not mention {kind}"

    def test_there_is_no_runtime_writer_for_the_protocol(self):
        """Self-modification is a Do-not-touch. The absence IS the enforcement.

        Asserted over the source rather than by calling something: the property
        under test is that no such code path exists at all.
        """
        import packages.orchestration.orchestrator_loop as loop

        text = open(loop.__file__ or "", encoding="utf-8").read()
        assert "protocol_document_path" in text
        writes = (".write_text(", ".write_bytes(", ".open(", "shutil.")
        for line in text.splitlines():
            if "protocol" not in line.lower():
                continue
            for writer in writes:
                assert writer not in line, (
                    f"the loop must not be able to write its own protocol: "
                    f"{line.strip()}")

    def test_the_protocol_is_only_ever_read(self):
        """The one call that touches the file is a read."""
        import inspect

        source = inspect.getsource(orchestrator_protocol_text)
        assert ".read_text(" in source
        assert ".write_text(" not in source


# ---------------------------------------------------------------------------
# context assembly — dossier FIRST, byte-stable prefix
# ---------------------------------------------------------------------------


class TestContextAssembly:
    def test_the_dossier_is_the_first_section(self, mission):
        ctx = assemble_context(mission)
        assert ctx.text.startswith(SECTION_DOSSIER)
        assert ctx.sections[0][0] == SECTION_DOSSIER

    def test_the_sections_are_in_the_specified_order(self, mission):
        ctx = assemble_context(mission)
        assert [name for name, _ in ctx.sections] == [
            SECTION_DOSSIER, SECTION_PLAN, SECTION_REPORT, SECTION_DECISIONS]

    def test_the_prefix_is_byte_stable_while_the_mission_does_not_change(
            self, mission):
        """The cache-stable prefix discipline, asserted rather than hoped."""
        first = assemble_context(mission, last_report="report one")
        second = assemble_context(mission, last_report="a different report")
        prefix = first.text.split(SECTION_PLAN)[0]
        assert second.text.startswith(prefix)
        assert first.digest != second.digest

    def test_the_dossier_changes_when_the_mission_does(self, mission):
        before = assemble_context(mission)
        after = assemble_context(mission, done_milestones=("M001",))
        assert before.sections[0][1] != after.sections[0][1]

    def test_a_dossier_seam_replaces_the_stand_in(self, mission):
        ctx = assemble_context(mission, dossier=lambda m: "F071 DOSSIER")
        assert ctx.sections[0][1] == "F071 DOSSIER"

    def test_the_stand_in_says_it_is_a_stand_in(self, mission):
        text = render_mission_dossier(mission)
        assert "stand-in" in text
        assert "M001" in text and "M002" in text

    def test_plan_state_marks_ready_blocked_and_done(self, mission):
        body = assemble_context(mission).sections[1][1]
        assert "M001: ready" in body
        assert "M002: blocked on M001" in body
        after = assemble_context(mission, done_milestones=("M001",)).sections[1][1]
        assert "M001: done" in after
        assert "M002: ready" in after

    def test_open_decisions_are_rendered(self, mission):
        ctx = assemble_context(
            mission, open_decisions=[{"id": "d1", "question": "which repo?"}])
        assert "d1: which repo?" in ctx.sections[3][1]

    def test_no_open_decisions_says_so(self, mission):
        assert assemble_context(mission).sections[3][1] == "None open."

    def test_the_digest_identifies_the_context(self, mission):
        ctx = assemble_context(mission)
        assert ctx.digest == context_digest(ctx.text)
        assert ctx.digest.startswith("sha256:")


# ---------------------------------------------------------------------------
# the ledger
# ---------------------------------------------------------------------------


def _entry(iteration: int, kind: str = "wait_on_decisions", **outcome):
    return LedgerEntry(
        iteration=iteration,
        context_digest=f"sha256:{iteration:064d}",
        move={"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V, "kind": kind,
              "payload": {}, "rationale": f"because {iteration}"},
        outcome=outcome or {"status": "waiting", "detail": ""},
        cost={"calls": 1, "usage": None, "usage_source": USAGE_UNMEASURED},
    )


class TestTheLedger:
    def test_entries_append_and_read_back_in_order(self, tmp_path, mission):
        for i in (1, 2, 3):
            append_ledger_entry(PROJECT, mission.id, _entry(i), tmp_path)
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert [e["iteration"] for e in entries] == [1, 2, 3]

    def test_appending_never_rewrites_what_is_already_there(self, tmp_path,
                                                            mission):
        append_ledger_entry(PROJECT, mission.id, _entry(1), tmp_path)
        first = ledger_path(PROJECT, mission.id, tmp_path).read_text()
        append_ledger_entry(PROJECT, mission.id, _entry(2), tmp_path)
        after = ledger_path(PROJECT, mission.id, tmp_path).read_text()
        assert after.startswith(first)

    def test_the_ledger_lives_in_the_missions_own_evidence_area(self, tmp_path,
                                                                mission):
        path = ledger_path(PROJECT, mission.id, tmp_path)
        assert path.name == LEDGER_FILENAME
        assert path.parent.name == "evidence"

    def test_every_entry_carries_the_audit_fields(self, tmp_path, mission):
        append_ledger_entry(PROJECT, mission.id, _entry(1), tmp_path)
        body = read_ledger(PROJECT, mission.id, tmp_path)[0]
        for key in ("iteration", "context_digest", "move", "outcome", "cost",
                    "protocol_version", "recorded_at"):
            assert key in body, f"ledger entry is missing {key}"
        assert body["recorded_at"]
        assert body["protocol_version"] == PROTOCOL_VERSION

    def test_a_torn_line_costs_one_entry_not_the_history(self, tmp_path,
                                                        mission):
        append_ledger_entry(PROJECT, mission.id, _entry(1), tmp_path)
        path = ledger_path(PROJECT, mission.id, tmp_path)
        with path.open("a", encoding="utf-8") as fh:
            fh.write('{"iteration": 2, "move"\n')  # killed mid-write
        append_ledger_entry(PROJECT, mission.id, _entry(3), tmp_path)
        assert [e["iteration"]
                for e in read_ledger(PROJECT, mission.id, tmp_path)] == [1, 3]

    def test_no_ledger_reads_as_empty(self, tmp_path, mission):
        assert read_ledger(PROJECT, mission.id, tmp_path) == []

    def test_the_render_reconstructs_the_decision_without_code(self, tmp_path,
                                                              mission):
        append_ledger_entry(
            PROJECT, mission.id,
            LedgerEntry(
                iteration=1,
                context_digest="sha256:abc",
                move={"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V,
                      "kind": "dispatch_job",
                      "payload": {"milestone_id": "M001", "step": "write it"},
                      "rationale": "M001 is ready"},
                outcome={"status": "dispatched", "detail": "job 1234"},
                cost={"calls": 1, "usage": None,
                      "usage_source": USAGE_UNMEASURED}),
            tmp_path)
        text = render_ledger(read_ledger(PROJECT, mission.id, tmp_path))
        for expected in ("dispatch_job", "M001", "write it", "M001 is ready",
                         "dispatched", "job 1234", "sha256:abc",
                         USAGE_UNMEASURED):
            assert expected in text, f"the rendered ledger hides {expected!r}"

    def test_an_empty_ledger_renders_honestly(self):
        assert render_ledger([]) == "No ledger entries."


class TestCostActuals:
    def test_unmeasured_cost_is_recorded_as_unmeasured(self):
        class _Outcome:
            last_text = '{"schema_v": "om1", "kind": "wait_on_decisions"}'
            calls = 1
            parse_retried = False
            schema_v = ORCHESTRATOR_MOVE_SCHEMA_V

        cost = measure_call_cost(_Outcome())
        assert cost["usage"] is None
        assert cost["usage_source"] == USAGE_UNMEASURED
        assert cost["calls"] == 1

    def test_a_measured_usage_block_is_parsed_by_the_existing_parser(self):
        class _Outcome:
            last_text = json.dumps({
                "type": "result", "subtype": "success", "is_error": False,
                "result": '{"schema_v": "om1", "kind": "wait_on_decisions"}',
                "usage": {"input_tokens": 120, "output_tokens": 30,
                          "cache_read_input_tokens": 4,
                          "cache_creation_input_tokens": 2},
                "total_cost_usd": 0.01, "num_turns": 1, "duration_ms": 5,
                "session_id": "s1"})
            calls = 1
            parse_retried = False
            schema_v = ORCHESTRATOR_MOVE_SCHEMA_V

        cost = measure_call_cost(_Outcome())
        assert cost["usage_source"] == "measured"
        assert cost["usage"]["input_tokens"] == 120
        assert cost["usage"]["output_tokens"] == 30


# ---------------------------------------------------------------------------
# milestone bookkeeping — additive, through the existing writer
# ---------------------------------------------------------------------------


class TestMilestoneBookkeeping:
    def test_marking_done_is_additive_on_the_plan_body(self, tmp_path, mission):
        updated = mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        assert done_milestones(updated) == ("M001",)
        # The plan itself is untouched: the bookkeeping key is stripped by the
        # existing reader, so no MissionPlan schema change was needed.
        plan = mission_plan_of(updated)
        assert [m.id for m in plan.milestones] == ["M001", "M002"]
        assert MILESTONES_DONE_KEY in (updated.mission_plan or {})

    def test_marking_twice_does_not_duplicate(self, tmp_path, mission):
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        updated = mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        assert done_milestones(updated) == ("M001",)

    def test_all_done_only_when_every_milestone_is(self, tmp_path, mission):
        assert all_milestones_done(mission) is False
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        partial = load_mission(PROJECT, mission.id, tmp_path)
        assert all_milestones_done(partial) is False
        mark_milestone_done(PROJECT, mission.id, "M002", tmp_path)
        full = load_mission(PROJECT, mission.id, tmp_path)
        assert all_milestones_done(full) is True

    def test_a_mission_without_a_plan_cannot_mark_a_milestone(self, tmp_path):
        m = create_mission(PROJECT, "no plan here", root=tmp_path)
        with pytest.raises(ValueError):
            mark_milestone_done(PROJECT, m.id, "M001", tmp_path)


# ---------------------------------------------------------------------------
# the loop
# ---------------------------------------------------------------------------


class _FakeJob:
    """The smallest thing the dispatch seam has to return: an id and no plan."""

    def __init__(self, job_id: str = "job-0001"):
        self.id = job_id
        self.flight_plan = None


def _scripted(*responses: str):
    """A fake provider that replays a fixed script, one answer per call."""
    calls: list[str] = []

    def call_fn(prompt: str, attempt: int) -> str:
        calls.append(prompt)
        index = min(len(calls) - 1, len(responses) - 1)
        return responses[index]

    call_fn.prompts = calls  # type: ignore[attr-defined]
    return call_fn


def _met_evidence(project_id, mission_id, milestone_id):
    """A milestone whose job finished and whose Definition of Done was met."""
    return MilestoneEvidence(job_id="job-0001", job_state="completed",
                             gate_released=True)


class _FakeCycleRun:
    """What `run_cycles` hands back, reduced to what the loop reads.

    R-0186 made execution part of a dispatch. Every test that dispatches must
    therefore inject this the same way it injects `dispatch`: the production
    default builds a real OllamaBuilder, and no pytest may take a provider
    path (R-0182).
    """

    def __init__(self, terminal_status: str = "all_green",
                 job_status: str = "completed", stop_reason: str = ""):
        self.terminal_status = terminal_status
        self.job_status = job_status
        self.stop_reason = stop_reason


def _executed(job):
    """The default executor double: the job ran and went green."""
    return _FakeCycleRun()


@pytest.fixture()
def dispatched():
    """Records every dispatch the loop makes, without creating real jobs."""
    seen: list[tuple[str, str, str]] = []

    def dispatch(project_id, mission_id, step, *, root=None, now=None):
        seen.append((project_id, mission_id, step))
        return _FakeJob(f"job-{len(seen):04d}")

    dispatch.seen = seen  # type: ignore[attr-defined]
    return dispatch


class TestLoopLimits:
    def test_the_flag_beats_config(self):
        assert loop_limits_from_config(iterations_flag=3).max_iterations == 3

    def test_the_config_key_supplies_the_default(self):
        class _Config:
            def get(self, key):
                return 4 if key == CONFIG_KEY_MAX_ITERATIONS else None

        assert loop_limits_from_config(_Config()).max_iterations == 4

    def test_an_absent_config_value_falls_back_to_the_conservative_default(self):
        class _Config:
            def get(self, key):
                return None

        assert (loop_limits_from_config(_Config()).max_iterations
                == DEFAULT_MAX_ITERATIONS)

    def test_a_nonsense_bound_is_refused(self):
        with pytest.raises(ValueError):
            loop_limits_from_config(iterations_flag=0)


class TestEveryMoveKindIsExercised:
    def test_wait_on_decisions_terminates_waiting(self, tmp_path, mission,
                                                  dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, execute=_executed, control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_WAITING
        assert result.iterations == 1

    def test_dispatch_job_goes_through_the_dispatch_verb(self, tmp_path,
                                                         mission, dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="build M001")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        assert dispatched.seen == [(PROJECT, mission.id, "build M001")]
        assert result.terminal == TERMINAL_ITERATION_LIMIT
        assert result.entries[0].outcome["status"] == "dispatched"
        assert result.entries[0].outcome["job_id"] == "job-0001"

    def test_declare_milestone_done_records_the_milestone(self, tmp_path,
                                                          mission, dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("declare_milestone_done",
                                         milestone_id="M001")),
            root=tmp_path, dispatch=dispatched, execute=_executed, evidence=_met_evidence,
            control_root_path=tmp_path / "control")
        assert done_milestones(
            load_mission(PROJECT, mission.id, tmp_path)) == ("M001",)

    def test_declare_mission_achieved_sets_the_record(self, tmp_path, mission,
                                                      dispatched):
        # Achieved is a claim about every milestone, so the evaluator requires
        # every milestone to be done before it will let the claim through.
        for milestone in ("M001", "M002"):
            mark_milestone_done(PROJECT, mission.id, milestone, tmp_path)
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=_scripted(_move_json("declare_mission_achieved")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_ACHIEVED
        assert load_mission(PROJECT, mission.id, tmp_path).status == "achieved"

    def test_abort_with_reason_abandons_and_records_why(self, tmp_path,
                                                        mission, dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=_scripted(_move_json("abort_with_reason",
                                         reason="the plan is unbuildable")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_ABORTED
        assert result.detail == "the plan is unbuildable"
        assert load_mission(PROJECT, mission.id, tmp_path).status == "abandoned"


class TestTheLoopTerminals:
    def test_an_unknown_kind_ends_the_run_as_a_parse_class_failure(
            self, tmp_path, mission, dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(json.dumps({
                "schema_v": ORCHESTRATOR_MOVE_SCHEMA_V,
                "kind": "create_mission", "payload": {"goal": "mine now"}})),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_INVALID_MOVE
        assert result.entries[-1].outcome["detail"].startswith("parse-class")

    def test_no_provider_is_a_terminal_not_an_exception(self, tmp_path,
                                                        mission, dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=None, root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_NO_PROVIDER
        assert len(result.entries) == 1

    def test_the_iteration_limit_is_a_normal_terminal(self, tmp_path, mission,
                                                      dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="keep going")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_ITERATION_LIMIT
        assert result.iterations == 3
        assert len(dispatched.seen) == 3
        assert "3-iteration limit" in result.detail

    def test_a_non_active_mission_stops_immediately(self, tmp_path, mission,
                                                    dispatched):
        set_mission_status(PROJECT, mission.id, "paused", tmp_path)
        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, execute=_executed, control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_NOT_ACTIVE
        assert result.entries == []


class TestHumanOverridesWinInstantly:
    def test_a_stop_request_between_iterations_halts_within_one_iteration(
            self, tmp_path, mission, dispatched):
        control = tmp_path / "control"
        seen: list[int] = []

        def dispatch(project_id, mission_id, step, *, root=None, now=None):
            seen.append(len(seen) + 1)
            if len(seen) == 1:
                # The human presses stop while iteration 1 is still running.
                request_stop(mission.id, reason="operator says stop",
                             control_root_path=control)
            return _FakeJob(f"job-{len(seen):04d}")

        result = run_mission(
            mission.id, LoopLimits(max_iterations=5), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="work")),
            root=tmp_path, dispatch=dispatch, execute=_executed, control_root_path=control)

        assert result.terminal == TERMINAL_STOPPED
        # Exactly ONE dispatch: the stop landed at the very next safe point,
        # not at the end of the five permitted iterations.
        assert seen == [1]
        assert "operator says stop" in result.detail

    def test_the_stop_is_consumed_so_a_later_run_is_not_stopped_again(
            self, tmp_path, mission, dispatched):
        control = tmp_path / "control"
        request_stop(mission.id, reason="halt", control_root_path=control)
        first = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, execute=_executed, control_root_path=control)
        assert first.terminal == TERMINAL_STOPPED
        assert stop_requested(mission.id, control_root_path=control) is None

    def test_open_decisions_reach_the_prompt_every_iteration(self, tmp_path,
                                                             mission):
        call_fn = _scripted(_move_json("wait_on_decisions"))
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=call_fn, root=tmp_path,
            control_root_path=tmp_path / "control")
        assert SECTION_DECISIONS in call_fn.prompts[0]


class TestTheLedgerCoversEveryIteration:
    def test_one_entry_per_iteration_numbered_from_one(self, tmp_path, mission,
                                                       dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="work")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert [e["iteration"] for e in entries] == [1, 2, 3]
        assert all(e["move"]["kind"] == "dispatch_job" for e in entries)

    def test_every_entry_carries_a_context_digest_and_cost(self, tmp_path,
                                                           mission, dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="work")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        for entry in read_ledger(PROJECT, mission.id, tmp_path):
            assert entry["context_digest"].startswith("sha256:")
            assert entry["cost"]["calls"] == 1
            assert entry["cost"]["usage_source"] == USAGE_UNMEASURED

    def test_the_run_is_reconstructable_from_the_rendered_ledger(
            self, tmp_path, mission, dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(
                _move_json("dispatch_job", milestone_id="M001", step="build"),
                _move_json("declare_milestone_done", milestone_id="M001"),
                _move_json("abort_with_reason", reason="M002 is impossible")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        text = render_ledger(read_ledger(PROJECT, mission.id, tmp_path))
        for expected in ("dispatch_job", "build", "declare_milestone_done",
                         "abort_with_reason", "M002 is impossible"):
            assert expected in text


class TestThePromptComesFromTheProtocol:
    def test_the_prompt_carries_the_generated_protocol_then_the_state(
            self, mission):
        ctx = assemble_context(mission)
        prompt = build_orchestrator_prompt(ctx)
        assert prompt.index(PROTOCOL_VERSION) < prompt.index(SECTION_DOSSIER)
        assert ctx.text in prompt

    def test_the_loop_sends_that_prompt(self, tmp_path, mission):
        call_fn = _scripted(_move_json("wait_on_decisions"))
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=call_fn, root=tmp_path,
            control_root_path=tmp_path / "control")
        assert PROTOCOL_DOC_RELATIVE in call_fn.prompts[0]
        assert SECTION_DOSSIER in call_fn.prompts[0]


class TestProjectResolution:
    def test_the_project_is_found_from_the_mission_id_alone(self, tmp_path,
                                                            mission):
        assert resolve_mission_project(mission.id, tmp_path) == PROJECT

    def test_an_unknown_mission_id_is_refused(self, tmp_path):
        with pytest.raises(MissionNotFoundError):
            resolve_mission_project("deadbeef", tmp_path)


# ---------------------------------------------------------------------------
# T002 — the evaluate step
# ---------------------------------------------------------------------------


def _no_evidence(project_id, mission_id, milestone_id):
    return MilestoneEvidence()


class TestEvaluateDispatch:
    def test_a_job_for_an_already_done_milestone_is_refused(self, tmp_path,
                                                            mission):
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        updated = load_mission(PROJECT, mission.id, tmp_path)
        reason = evaluate_dispatch(updated, "M001")
        assert "already done" in reason

    def test_a_milestone_outside_the_plan_is_refused(self, mission):
        assert "not in this mission's plan" in evaluate_dispatch(mission, "M009")

    def test_a_milestone_with_unmet_dependencies_is_refused(self, mission):
        assert "depends on M001" in evaluate_dispatch(mission, "M002")

    def test_a_ready_milestone_is_allowed(self, mission):
        assert evaluate_dispatch(mission, "M001") == ""


class TestEvaluateMilestoneDone:
    def test_a_claim_with_no_dispatched_job_is_refused(self, mission):
        reason = evaluate_milestone_done(mission, "M001", MilestoneEvidence())
        assert "no job was ever dispatched" in reason

    def test_a_claim_on_a_running_job_is_refused(self, mission):
        reason = evaluate_milestone_done(
            mission, "M001",
            MilestoneEvidence(job_id="j1", job_state="running"))
        assert "not terminal" in reason

    def test_a_claim_whose_dod_is_not_met_is_refused(self, mission):
        reason = evaluate_milestone_done(
            mission, "M001",
            MilestoneEvidence(job_id="j1", job_state="completed",
                              gate_released=False,
                              gate_blocker="2 blocking checks failed"))
        assert "Definition of Done" in reason
        assert "2 blocking checks failed" in reason

    def test_a_job_without_a_stored_dod_is_not_gated(self, mission):
        """The F061 gate is additive: no DoD means no gate, not a refusal."""
        assert evaluate_milestone_done(
            mission, "M001",
            MilestoneEvidence(job_id="j1", job_state="completed",
                              gate_released=None)) == ""

    def test_a_met_claim_is_allowed(self, mission):
        assert evaluate_milestone_done(
            mission, "M001",
            MilestoneEvidence(job_id="j1", job_state="completed",
                              gate_released=True)) == ""

    def test_achieved_is_refused_while_milestones_are_open(self, tmp_path,
                                                           mission, dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=_scripted(_move_json("declare_mission_achieved")),
            root=tmp_path, dispatch=dispatched, execute=_executed, evidence=_no_evidence,
            control_root_path=tmp_path / "control")
        assert result.entries[0].outcome["status"] == OUTCOME_REFUSED
        assert "still open" in result.entries[0].outcome["detail"]
        assert load_mission(PROJECT, mission.id, tmp_path).status == "active"


class TestRefusalRePromptsOnceThenEscalates:
    def test_the_first_refusal_re_prompts_with_the_reason_as_feedback(
            self, tmp_path, mission, dispatched):
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        call_fn = _scripted(
            _move_json("dispatch_job", milestone_id="M001", step="again"),
            _move_json("wait_on_decisions"))
        result = run_mission(
            mission.id, LoopLimits(max_iterations=4), project_id=PROJECT,
            call_fn=call_fn, root=tmp_path, dispatch=dispatched, execute=_executed,
            evidence=_no_evidence, control_root_path=tmp_path / "control")
        # The refusal was recorded, and the very next prompt carried it back.
        assert result.entries[0].outcome["status"] == OUTCOME_REFUSED
        assert SECTION_FEEDBACK not in call_fn.prompts[0]
        assert SECTION_FEEDBACK in call_fn.prompts[1]
        assert "already done" in call_fn.prompts[1]
        # The re-prompt produced an acceptable move, so the loop went on.
        assert result.terminal == TERMINAL_WAITING
        assert dispatched.seen == []

    def test_a_second_refusal_escalates_through_the_escalation_verb(
            self, tmp_path, mission, dispatched):
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        escalated: list[str] = []

        def escalate(project_id, mission_id, reason):
            escalated.append(reason)
            return "d1"

        result = run_mission(
            mission.id, LoopLimits(max_iterations=5), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="again and again")),
            root=tmp_path, dispatch=dispatched, execute=_executed, evidence=_no_evidence,
            escalate=escalate, control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_ESCALATED
        assert len(escalated) == 1
        assert "already done" in escalated[0]
        # Never a silent loop: two refusals and out, not five.
        assert result.iterations == 2
        assert dispatched.seen == []

    def test_an_accepted_move_clears_the_feedback(self, tmp_path, mission,
                                                  dispatched):
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        call_fn = _scripted(
            _move_json("dispatch_job", milestone_id="M001", step="refused"),
            _move_json("dispatch_job", milestone_id="M002", step="fine"),
            _move_json("dispatch_job", milestone_id="M001", step="refused"),
            _move_json("wait_on_decisions"))
        result = run_mission(
            mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
            call_fn=call_fn, root=tmp_path, dispatch=dispatched, execute=_executed,
            evidence=_no_evidence, control_root_path=tmp_path / "control")
        # Prompt 3 follows an ACCEPTED move, so it carries no stale feedback.
        assert SECTION_FEEDBACK in call_fn.prompts[1]
        assert SECTION_FEEDBACK not in call_fn.prompts[2]
        assert result.terminal == TERMINAL_WAITING

    def test_the_default_escalation_uses_the_existing_verb(self, tmp_path,
                                                          mission):
        """No job linked yet, so the honest answer is that there is nowhere to attach."""
        reason = escalate_repeated_refusal(PROJECT, mission.id, "refused twice",
                                           root=tmp_path)
        assert "no job is linked" in reason


class TestTheDossierIsUpdatedEveryIteration:
    def test_the_update_call_runs_once_per_iteration(self, tmp_path, mission,
                                                     dispatched):
        seen: list[str] = []
        run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="work")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            update_dossier=lambda p, m, mission: seen.append(m),
            control_root_path=tmp_path / "control")
        assert seen == [mission.id] * 3

    def test_the_default_update_writes_the_dossier_beside_the_ledger(
            self, tmp_path, mission, dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, execute=_executed, control_root_path=tmp_path / "control")
        path = ledger_path(PROJECT, mission.id, tmp_path).parent / DOSSIER_FILENAME
        assert path.is_file()
        assert "Ship the thing" in path.read_text()

    def test_the_update_tracks_the_mission_as_it_changes(self, tmp_path,
                                                         mission, dispatched):
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, execute=_executed, control_root_path=tmp_path / "control")
        text = (ledger_path(PROJECT, mission.id, tmp_path).parent
                / DOSSIER_FILENAME).read_text()
        assert "M001 [done]" in text
        assert "M002 [open]" in text


class TestTheMaintainedDossierIsThePromptPrefix:
    """F071 T003 — the maintained document drives the live loop.

    The dossier is assembled FIRST and its bytes are the prefix of the mission
    state, so a provider's prompt cache survives an iteration in which only the
    volatile sections changed.
    """

    def _run(self, tmp_path, mission, dispatched, **kwargs):
        iterations = kwargs.pop("iterations", 1)
        # dispatch_job is NON-terminal, so a multi-iteration run really runs
        # that many iterations; wait_on_decisions ends the run after one.
        move = _move_json("dispatch_job", milestone_id="M001", step="work") \
            if iterations > 1 else _move_json("wait_on_decisions")
        return run_mission(
            mission.id, LoopLimits(max_iterations=iterations),
            project_id=PROJECT, call_fn=_scripted(move), root=tmp_path,
            dispatch=dispatched, execute=_executed, control_root_path=tmp_path / "control",
            **kwargs)

    def test_the_newest_version_is_the_byte_prefix_of_the_mission_state(
            self, tmp_path, mission, dispatched):
        from packages.orchestration.mission_dossier import newest_dossier_text

        prompts: list[str] = []
        self._run(tmp_path, mission, dispatched,
                  on_call=lambda a, v, r, prompt: prompts.append(prompt))
        newest = newest_dossier_text(PROJECT, mission.id, tmp_path)
        assert newest
        assert f"# Mission state\n\n{SECTION_DOSSIER}\n\n{newest}" in prompts[0]

    def test_the_dossier_section_leads_the_assembled_context(self, tmp_path,
                                                             mission,
                                                             dispatched):
        from packages.orchestration.mission_dossier import newest_dossier_text

        self._run(tmp_path, mission, dispatched)
        newest = newest_dossier_text(PROJECT, mission.id, tmp_path)
        context = assemble_context(mission, dossier=lambda m: newest)
        assert context.sections[0][0] == SECTION_DOSSIER
        assert context.text.startswith(f"{SECTION_DOSSIER}\n\n{newest}")

    def test_the_prefix_is_the_maintained_document_not_the_stand_in(
            self, tmp_path, mission, dispatched):
        from packages.orchestration.mission_dossier import (
            SECTION_GOAL,
            newest_dossier_text,
        )

        self._run(tmp_path, mission, dispatched)
        newest = newest_dossier_text(PROJECT, mission.id, tmp_path)
        assert f"## {SECTION_GOAL}" in newest
        assert "stand-in" not in newest

    def test_one_version_file_lands_per_iteration(self, tmp_path, mission,
                                                  dispatched):
        from packages.orchestration.mission_dossier import dossier_versions

        self._run(tmp_path, mission, dispatched, iterations=3)
        assert dossier_versions(PROJECT, mission.id, tmp_path) == [2, 3, 4]

    def test_the_goal_is_byte_identical_across_every_version(self, tmp_path,
                                                             mission,
                                                             dispatched):
        from packages.orchestration.mission_dossier import (
            dossier_version_path,
            dossier_versions,
        )

        self._run(tmp_path, mission, dispatched, iterations=3)
        goals = set()
        for version in dossier_versions(PROJECT, mission.id, tmp_path):
            text = dossier_version_path(
                PROJECT, mission.id, version, tmp_path).read_text()
            goals.add(text.split("## MILESTONES")[0])
        assert len(goals) == 1
        assert "Ship the thing" in goals.pop()

    def test_a_compression_failure_iteration_still_renders_the_whole_document(
            self, tmp_path, mission, dispatched):
        from packages.orchestration.mission_dossier import (
            open_items,
            refresh_mission_dossier,
            render_dossier,
        )

        # A tight budget forces compression; the provider answers with garbage,
        # so the iteration must keep the complete document and FLAG it.
        def refresh(project_id, mission_id, mission_record):
            result = refresh_mission_dossier(
                project_id, mission_id, mission_record, root=tmp_path,
                budget=1, call_fn=lambda prompt, attempt: "not json")
            assert result.over_budget is True
            return result

        prompts: list[str] = []
        self._run(tmp_path, mission, dispatched, update_dossier=refresh,
                  on_call=lambda a, v, r, prompt: prompts.append(prompt))

        from packages.orchestration.mission_dossier import load_dossier_state

        state = load_dossier_state(PROJECT, mission.id, tmp_path)
        assert state.over_budget is True
        text = render_dossier(state)
        assert "OVER BUDGET" in text
        assert "Nothing was truncated" in text
        # Every open item is still in the prompt — flagged, never trimmed.
        for item in open_items(state):
            assert item.id in prompts[0]


# ---------------------------------------------------------------------------
# T002 — the era corpus stops the loop
# ---------------------------------------------------------------------------

ERA_FIXTURES = Path(__file__).parent / "fixtures" / "era"

#: One entry per finding class. The detector tests live in
#: test_era_integrity.py; THESE assert the loop refuses to advance on them.
ERA_CORPUS = sorted(p.name for p in ERA_FIXTURES.glob("*.json"))


def _era_handback(name: str):
    body = json.loads((ERA_FIXTURES / name).read_text(encoding="utf-8"))
    return body["finding_class"], body["handback"]


class TestTheEraCorpusRefusesToAdvance:
    @pytest.mark.parametrize("name", ERA_CORPUS)
    def test_a_defective_handback_blocks_the_milestone(self, tmp_path, mission,
                                                       dispatched, name):
        finding_class, handback = _era_handback(name)

        def evidence(project_id, mission_id, milestone_id):
            # Everything else about this milestone is impeccable: the job
            # finished and its Definition of Done was met. Only the handback
            # carries the era defect, so nothing but the corpus can refuse it.
            return MilestoneEvidence(job_id="j1", job_state="completed",
                                     gate_released=True, handback=handback)

        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=_scripted(_move_json("declare_milestone_done",
                                         milestone_id="M001")),
            root=tmp_path, dispatch=dispatched, execute=_executed, evidence=evidence,
            escalate=lambda p, m, r: "d1",
            control_root_path=tmp_path / "control")

        # Flagged, named, and the milestone did NOT advance.
        first = result.entries[0].outcome
        assert first["status"] == OUTCOME_REFUSED
        assert "refuses to advance" in first["detail"]
        assert finding_class in first["detail"], (
            f"{name} was refused without naming its finding class")
        assert done_milestones(load_mission(PROJECT, mission.id, tmp_path)) == ()

    @pytest.mark.parametrize("name", ERA_CORPUS)
    def test_a_defective_handback_also_blocks_a_dispatch(self, tmp_path,
                                                         mission, dispatched,
                                                         name):
        finding_class, handback = _era_handback(name)
        result = run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="carry on")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            evidence=lambda p, m, ms: MilestoneEvidence(handback=handback),
            control_root_path=tmp_path / "control")
        assert result.entries[0].outcome["status"] == OUTCOME_REFUSED
        assert finding_class in result.entries[0].outcome["detail"]
        assert dispatched.seen == []

    def test_a_clean_handback_does_not_block_anything(self, tmp_path, mission,
                                                      dispatched):
        clean = {"commits": ["aaa"], "reported_commits": ["aaa"],
                 "changed_files_tables": {"aaa": ["packages/x.py"]}}
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("declare_milestone_done",
                                         milestone_id="M001")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            evidence=lambda p, m, ms: MilestoneEvidence(
                job_id="j1", job_state="completed", gate_released=True,
                handback=clean),
            control_root_path=tmp_path / "control")
        assert done_milestones(
            load_mission(PROJECT, mission.id, tmp_path)) == ("M001",)


class TestMilestoneAttributionComesFromTheLedger:
    def test_the_ledger_records_which_job_served_which_milestone(
            self, tmp_path, mission, dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="build M001")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        assert dispatched_job_for(PROJECT, mission.id, "M001",
                                  tmp_path) == "job-0001"
        assert dispatched_job_for(PROJECT, mission.id, "M002", tmp_path) == ""


class TestAPlanLessMissionCannotBeDeclaredAchieved:
    """R-0170 — "no milestones are open" is not evidence that a goal is met.

    A mission with no compiled plan has ``milestone_ids() == ()``, so the
    open-milestone check found nothing to object to and the claim executed:
    one iteration, zero evidence, status achieved. ``all_milestones_done``
    already required ``bool(ids)``; the claim is now held to the same bar.
    """

    @pytest.fixture()
    def plan_less(self, tmp_path):
        return create_mission(PROJECT, "A goal with no plan", root=tmp_path)

    def test_the_claim_is_refused_with_a_recorded_reason(self, tmp_path,
                                                          plan_less, dispatched):
        result = run_mission(
            plan_less.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("declare_mission_achieved")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        outcome = result.entries[0].outcome
        assert outcome["status"] == OUTCOME_REFUSED
        assert "no compiled plan" in outcome["detail"]

    def test_the_mission_stays_active(self, tmp_path, plan_less, dispatched):
        run_mission(
            plan_less.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("declare_mission_achieved")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")
        assert load_mission(PROJECT, plan_less.id, tmp_path).status == "active"

    def test_a_second_claim_escalates_and_never_executes(self, tmp_path,
                                                          plan_less, dispatched):
        escalated: list[str] = []
        result = run_mission(
            plan_less.id, LoopLimits(max_iterations=5), project_id=PROJECT,
            call_fn=_scripted(_move_json("declare_mission_achieved")),
            root=tmp_path, dispatch=dispatched, execute=_executed,
            escalate=lambda p, m, reason: escalated.append(reason) or "d1",
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_ESCALATED
        assert len(escalated) == 1 and "no compiled plan" in escalated[0]
        assert result.iterations == 2
        assert load_mission(PROJECT, plan_less.id, tmp_path).status == "active"

    def test_the_evaluator_says_so_directly(self, plan_less):
        move = OrchestratorMove.model_validate_json(
            _move_json("declare_mission_achieved"))
        reason = evaluate_move(plan_less, move, observe=_no_evidence,
                               project_id=PROJECT, mission_id=plan_less.id)
        assert "no compiled plan" in reason

    def test_a_planned_mission_with_every_milestone_done_still_passes(
            self, tmp_path, mission):
        """The fix refuses ABSENCE of a plan, not a legitimately finished one."""
        for milestone in ("M001", "M002"):
            mark_milestone_done(PROJECT, mission.id, milestone, tmp_path)
        updated = load_mission(PROJECT, mission.id, tmp_path)
        move = OrchestratorMove.model_validate_json(
            _move_json("declare_mission_achieved"))
        assert evaluate_move(updated, move, observe=_no_evidence,
                             project_id=PROJECT, mission_id=mission.id) == ""


# ---------------------------------------------------------------------------
# F075 R3 — the exception boundary
# ---------------------------------------------------------------------------
#
# Before this boundary existed, a raise from the iteration's own work escaped
# run_mission: no ledger entry, no post-mortem, no terminal, and the loop's own
# docstring promise ("every iteration leaves a ledger entry") was false exactly
# when a reader would need it most. The DECISION of record is the F075 R2
# verdict. Three seams can raise — the provider call, the dispatch and the
# dossier refresh — and each must end the run honestly instead of escaping.


class TestTheIterationBoundary:
    """A raise inside an iteration becomes an account, never an escape."""

    def _boom(self, message: str):
        def raiser(*args, **kwargs):
            raise RuntimeError(message)
        return raiser

    def _postmortems(self, tmp_path, mission_id):
        return sorted(mission_evidence_dir(PROJECT, mission_id, tmp_path)
                      .rglob("postmortem.json"))

    def test_a_raising_provider_call_does_not_propagate(self, tmp_path, mission):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            root=tmp_path, call_fn=self._boom("the model host went away"))
        assert result.terminal == TERMINAL_ITERATION_FAILED
        assert "the model host went away" in result.detail

    def test_a_raising_dispatch_does_not_propagate(self, tmp_path, mission):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            root=tmp_path,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="start the work")),
            evidence=_no_evidence,
            dispatch=self._boom("died between the move and the dispatch"))
        assert result.terminal == TERMINAL_ITERATION_FAILED
        assert "died between the move and the dispatch" in result.detail

    def test_a_raising_dossier_refresh_does_not_propagate(self, tmp_path, mission):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            root=tmp_path, call_fn=_scripted(_move_json("wait_on_decisions",
                                                        reason="waiting")),
            update_dossier=self._boom("died mid-write"))
        assert result.terminal == TERMINAL_ITERATION_FAILED
        assert "died mid-write" in result.detail

    def test_the_failing_iteration_still_leaves_a_ledger_entry(self, tmp_path,
                                                              mission):
        run_mission(mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
                    root=tmp_path, call_fn=self._boom("provider exploded"))
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert len(entries) == 1
        assert entries[0]["outcome"]["status"] == TERMINAL_ITERATION_FAILED
        assert "provider exploded" in entries[0]["outcome"]["detail"]

    def test_the_failure_is_classified_into_a_postmortem(self, tmp_path, mission):
        run_mission(mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
                    root=tmp_path, call_fn=self._boom("request timed out"))
        written = self._postmortems(tmp_path, mission.id)
        assert [p.parent.name for p in written] == ["iteration_1"]
        body = json.loads(written[0].read_text(encoding="utf-8"))
        assert body["failure_class"] == "provider_timeout"
        assert body["terminal_status"] == TERMINAL_ITERATION_FAILED
        assert "request timed out" in body["raw_reason"]

    def test_a_class_it_cannot_determine_is_recorded_as_unknown(self, tmp_path,
                                                               mission):
        """Said out loud, never invented — and the gauntlet's
        no-unknown-postmortems criterion is what makes that visible.

        The example used to be "HTTP 503 from the host". That was the dishonest
        unknown R-0185 fixed: the classifier reads a 503 as
        ``provider_unavailable`` now, so this test needs a failure nothing can
        actually recognise. The assertion is unchanged."""
        run_mission(mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
                    root=tmp_path, call_fn=self._boom("the flurb did not glorp"))
        body = json.loads(self._postmortems(tmp_path, mission.id)[0]
                          .read_text(encoding="utf-8"))
        assert body["failure_class"] == "unknown"

    def test_the_boundary_adds_no_retry_of_its_own(self, tmp_path, mission):
        """One catch per iteration, then the run ends. Transport retries are
        F001's, below call_fn — a second attempt here would hide them."""
        calls: list[int] = []

        def counting(prompt, attempt):
            calls.append(attempt)
            raise RuntimeError("always down")

        run_mission(mission.id, LoopLimits(max_iterations=5), project_id=PROJECT,
                    root=tmp_path, call_fn=counting)
        assert calls == [0]

    def test_a_keyboard_interrupt_propagates(self, tmp_path, mission):
        """An operator stopping Remedy is not a failure to classify."""
        def interrupted(*args, **kwargs):
            raise KeyboardInterrupt

        with pytest.raises(KeyboardInterrupt):
            run_mission(mission.id, LoopLimits(max_iterations=2),
                        project_id=PROJECT, root=tmp_path, call_fn=interrupted)

    def test_a_system_exit_propagates(self, tmp_path, mission):
        def exiting(*args, **kwargs):
            raise SystemExit(2)

        with pytest.raises(SystemExit):
            run_mission(mission.id, LoopLimits(max_iterations=2),
                        project_id=PROJECT, root=tmp_path, call_fn=exiting)

    def test_the_mission_record_survives_a_boundary_catch(self, tmp_path, mission):
        run_mission(mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
                    root=tmp_path, call_fn=self._boom("provider exploded"))
        reloaded = load_mission(PROJECT, mission.id, tmp_path)
        assert reloaded.id == mission.id
        assert reloaded.goal == mission.goal
        assert mission_plan_of(reloaded) is not None

    def test_an_unwritable_postmortem_is_reported_not_raised(self, tmp_path,
                                                             mission, monkeypatch):
        """A post-mortem that cannot be written must not become a second,
        louder failure on top of the first."""
        import packages.orchestration.failure_postmortem as pm

        def refuse(*args, **kwargs):
            raise OSError("the evidence area is read-only")

        monkeypatch.setattr(pm, "write_postmortem", refuse)
        result = run_mission(mission.id, LoopLimits(max_iterations=2),
                             project_id=PROJECT, root=tmp_path,
                             call_fn=self._boom("provider exploded"))
        assert result.terminal == TERMINAL_ITERATION_FAILED
        assert "the post-mortem could not be written" in result.detail
        assert "provider exploded" in result.detail

    def test_the_injected_provider_error_classifies_as_a_provider_failure(
            self, tmp_path, mission):
        """R-0185, end to end through record_iteration_failure: attempt 1's
        injected 503 used to land in the evidence as `unknown`."""
        def boom(*args, **kwargs):
            raise ConnectionError("provider API error mid-move: the model host "
                                  "returned HTTP 503 and closed the connection")

        result = run_mission(mission.id, LoopLimits(max_iterations=2),
                             project_id=PROJECT, root=tmp_path, call_fn=boom)
        # R-0196: provider_unavailable is retryable, so the second identical
        # failure on the same milestone escalates rather than ending the run
        # at the first. The CLASS is what this test is about, and it is
        # unchanged.
        assert result.terminal == TERMINAL_ESCALATED
        body = json.loads(self._postmortems(tmp_path, mission.id)[0]
                          .read_text(encoding="utf-8"))
        assert body["failure_class"] == "provider_unavailable"

    def test_the_injected_harness_death_classifies_as_a_machine_failure(
            self, tmp_path, mission):
        """The other injected shape: nothing about the provider went wrong."""
        def die(*args, **kwargs):
            raise OSError("harness death mid-write: killed while writing the dossier")

        result = run_mission(mission.id, LoopLimits(max_iterations=2),
                             project_id=PROJECT, root=tmp_path,
                             call_fn=_scripted(_move_json("wait_on_decisions",
                                                          reason="waiting")),
                             update_dossier=die)
        # R-0196, as above: io_failure is retryable, so two in a row escalate.
        assert result.terminal == TERMINAL_ESCALATED
        body = json.loads(self._postmortems(tmp_path, mission.id)[0]
                          .read_text(encoding="utf-8"))
        assert body["failure_class"] == "io_failure"


# ---------------------------------------------------------------------------
# F075 R-0186 — the loop executes what it dispatches
# ---------------------------------------------------------------------------
#
# Campaign attempt 1 recorded ten missions whose jobs all sat at `planned`: the
# loop created work and walked away, so no milestone could become done and the
# DoD gate was never reached. T1_F070's Design specified the executor step
# ("run it through the multi-cycle executor -> evaluate"); this is that step.
# Every test here injects the executor seam — no pytest may take a provider
# path (R-0182).


class TestTheLoopExecutesWhatItDispatches:

    def _run(self, tmp_path, mission, execute, dispatched, **kw):
        return run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=execute,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="build the core")), **kw)

    def test_the_dispatched_job_is_executed_in_the_same_iteration(
            self, tmp_path, mission, dispatched):
        seen: list[Any] = []

        def execute(job):
            seen.append(job)
            return _FakeCycleRun()

        self._run(tmp_path, mission, execute, dispatched)
        assert len(seen) == 1, "exactly one execution per dispatch"
        assert str(seen[0].id) == "job-0001", "the job just created, not another"

    def test_what_execution_produced_is_on_the_ledger(self, tmp_path, mission,
                                                      dispatched):
        """The next iteration's context has to show WHY a milestone is or is
        not claimable, so the outcome carries the executor's own verdict."""
        def execute(job):
            return _FakeCycleRun(terminal_status="all_green",
                                 job_status="completed")

        self._run(tmp_path, mission, execute, dispatched)
        detail = read_ledger(PROJECT, mission.id, tmp_path)[0]["outcome"]["detail"]
        assert "executed: terminal=all_green" in detail
        assert "job_status=completed" in detail

    def test_a_stop_reason_from_the_executor_is_recorded(self, tmp_path, mission,
                                                         dispatched):
        def execute(job):
            return _FakeCycleRun(terminal_status="stopped",
                                 job_status="paused", stop_reason="budget")

        self._run(tmp_path, mission, execute, dispatched)
        detail = read_ledger(PROJECT, mission.id, tmp_path)[0]["outcome"]["detail"]
        assert "stop=budget" in detail

    def test_a_raising_executor_degrades_through_the_boundary(
            self, tmp_path, mission, dispatched):
        """Execution lives INSIDE the R3 boundary: it must not escape.

        R-0196 changed what "degrades" means for this class: an OSError is a
        machine fault, so the iteration is ledgered and the loop goes round
        again. Here the budget is one iteration, so the run ends on the limit
        — the assertions that matter are that nothing escaped and that the
        failure is on the record."""
        def execute(job):
            raise OSError("the executor died mid-cycle")

        result = self._run(tmp_path, mission, execute, dispatched)
        assert result.terminal == TERMINAL_ITERATION_LIMIT
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert entries[-1]["outcome"]["status"] == OUTCOME_ITERATION_RETRYING
        assert "the executor died mid-cycle" in entries[-1]["outcome"]["detail"]
        body = json.loads(sorted(mission_evidence_dir(PROJECT, mission.id, tmp_path)
                                 .rglob("postmortem.json"))[0]
                          .read_text(encoding="utf-8"))
        assert body["failure_class"] == "io_failure"

    def test_the_production_default_is_the_existing_executor(self):
        """No second executor: the default is long_run_executor.run_cycles,
        reached through one named function that reuses limits_from_config."""
        import inspect

        from packages.orchestration.orchestrator_loop import (
            execute_dispatched_job,
        )
        source = inspect.getsource(execute_dispatched_job)
        assert "run_cycles" in source
        assert "limits_from_config" in source
        assert "default_task_step" in source


class TestTheReDispatchGuard:
    """One milestone, one job at a time (R-0186)."""

    def _evidence(self, state: str, released=None):
        return MilestoneEvidence(job_id="job-0001", job_state=state,
                                 gate_released=released)

    @pytest.mark.parametrize("state", ["pending", "planned", "running"])
    def test_a_second_job_is_refused_while_the_first_is_in_flight(
            self, mission, state):
        refusal = evaluate_dispatch(mission, "M001", self._evidence(state))
        assert "already has job job-0001 in flight" in refusal
        assert state in refusal

    def test_the_refusal_says_what_to_do_instead(self, mission):
        refusal = evaluate_dispatch(mission, "M001", self._evidence("planned"))
        assert "wait_on_decisions" in refusal
        assert "declare_milestone_done" in refusal

    def test_a_released_gate_is_told_to_declare_done(self, mission):
        refusal = evaluate_dispatch(mission, "M001",
                                    self._evidence("running", released=True))
        assert "declare_milestone_done for M001" in refusal

    @pytest.mark.parametrize("state", ["completed", "failed", "cancelled"])
    def test_a_terminal_job_allows_a_new_dispatch(self, mission, state):
        assert evaluate_dispatch(mission, "M001", self._evidence(state)) == ""

    def test_a_paused_job_still_allows_a_dispatch(self, mission):
        """The move schema has no resume kind, so refusing here would deadlock
        the mission instead of guarding it."""
        assert evaluate_dispatch(mission, "M001", self._evidence("paused")) == ""

    def test_a_milestone_with_no_job_is_untouched(self, mission):
        assert evaluate_dispatch(mission, "M001", MilestoneEvidence()) == ""

    def test_the_six_identical_dispatches_are_now_impossible(
            self, tmp_path, mission, dispatched):
        """The exact R-0184 shape: the model asks for the same milestone again
        while its job has not advanced."""
        moves = _scripted(_move_json("dispatch_job", milestone_id="M001",
                                     step="build the core"))
        in_flight = MilestoneEvidence(job_id="job-0001", job_state="planned")
        result = run_mission(
            mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
            root=tmp_path, dispatch=dispatched, execute=_executed,
            evidence=lambda p, m, ms: in_flight, call_fn=moves)
        # First refusal re-prompts once, the second escalates — never six jobs.
        assert result.terminal == TERMINAL_ESCALATED
        assert len(dispatched.seen) == 0


# ---------------------------------------------------------------------------
# F075 R-0188 — the production DoD path
# ---------------------------------------------------------------------------
#
# Before this, `store_dod` had zero callers and `run_job_gate`'s only caller was
# the fixture-demo fulfillment spine, so no real run could ever produce a gate
# verdict and `dod_blocking_green` was unmeetable by construction.


def _a_dod(check_id: str = "tests", argv=("python3", "-c", "pass"),
           blocking: bool = True):
    """A minimal deterministic DoD: one custom_cmd check that really runs.

    ``python3`` because the gate only executes allow-listed executables — a
    check naming anything else is refused before it runs, which is the point of
    the allowlist and not something to work around.
    """
    from packages.orchestration.dod_schema import DoD

    return DoD.model_validate({
        "schema_v": "dod_v1",
        "checks": [{"id": check_id, "kind": "custom_cmd", "blocking": blocking,
                    "spec": {"argv": list(argv)}, "source": "standard"}],
        "compiled": False,
        "origin": "deterministic",
    })


class TestTheDoDReachesTheJob:

    def _write_milestone_dod(self, tmp_path, mission, milestone_id="M001"):
        from packages.orchestration.mission_compiler import (
            milestone_dod_filename,
            mission_plan_of,
        )
        evidence = mission_evidence_dir(PROJECT, mission.id, tmp_path)
        evidence.mkdir(parents=True, exist_ok=True)
        name = milestone_dod_filename(milestone_id)
        (evidence / name).write_text(
            json.dumps(_a_dod().model_dump()), encoding="utf-8")
        plan = mission_plan_of(mission)
        body = plan.model_copy(update={"milestones": [
            m.model_copy(update={"dod_ref": name}) if m.id == milestone_id else m
            for m in plan.milestones]}).model_dump()
        set_mission_plan(PROJECT, mission.id, body, tmp_path)
        return load_mission(PROJECT, mission.id, tmp_path)

    def test_a_dispatch_stores_the_milestones_compiled_dod(self, tmp_path, mission):
        from packages.orchestration.dod_gate import load_dod

        mission = self._write_milestone_dod(tmp_path, mission)
        stored = attach_milestone_dod(PROJECT, mission.id, mission, "M001",
                                      "job-0001", tmp_path)
        assert stored is True
        assert load_dod("job-0001") is not None

    def test_a_milestone_with_no_dod_ref_stores_nothing(self, tmp_path, mission):
        """Honest absence: the gate stays un-run rather than inventing a DoD."""
        assert attach_milestone_dod(PROJECT, mission.id, mission, "M001",
                                    "job-0002", tmp_path) is False

    def test_an_unreadable_dod_artifact_stores_nothing(self, tmp_path, mission):
        from packages.orchestration.mission_compiler import (
            milestone_dod_filename,
            mission_plan_of,
        )
        evidence = mission_evidence_dir(PROJECT, mission.id, tmp_path)
        evidence.mkdir(parents=True, exist_ok=True)
        name = milestone_dod_filename("M001")
        (evidence / name).write_text("{ not a dod", encoding="utf-8")
        plan = mission_plan_of(mission)
        body = plan.model_copy(update={"milestones": [
            m.model_copy(update={"dod_ref": name}) if m.id == "M001" else m
            for m in plan.milestones]}).model_dump()
        set_mission_plan(PROJECT, mission.id, body, tmp_path)
        reloaded = load_mission(PROJECT, mission.id, tmp_path)
        assert attach_milestone_dod(PROJECT, mission.id, reloaded, "M001",
                                    "job-0003", tmp_path) is False

    def test_nothing_is_recompiled(self, tmp_path, mission):
        """The artifact F069 already wrote is COPIED, never rebuilt."""
        import inspect

        source = inspect.getsource(attach_milestone_dod)
        assert "compile_milestone_dod" not in source
        assert "store_dod" in source


class TestTheGateRunsAtJobCompletion:

    def test_a_job_with_a_dod_gets_a_persisted_verdict(self, tmp_path, monkeypatch):
        from packages.orchestration.dod_gate import load_gate_result, store_dod

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_dod("job-0100", _a_dod())
        released, blocker = run_gate_for_job("job-0100")
        assert released is True and blocker == ""
        assert load_gate_result("job-0100")["released"] is True

    def test_a_job_without_a_dod_is_not_gated_at_all(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        assert run_gate_for_job("job-0101") == (None, "")

    def test_a_failing_check_blocks_and_names_its_blocker(self, tmp_path,
                                                          monkeypatch):
        from packages.orchestration.dod_gate import store_dod

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        store_dod("job-0102", _a_dod(check_id="impossible",
                                     argv=("python3", "-c", "raise SystemExit(1)")))
        released, blocker = run_gate_for_job("job-0102")
        assert released is False
        assert "impossible" in blocker

    def test_the_verdict_has_one_author(self):
        """run_job_gate persists its own result — no second store here."""
        import inspect

        source = inspect.getsource(run_gate_for_job)
        assert "run_job_gate" in source
        assert "save_gate_result" not in source


class TestAReleasedGateMakesTheMilestoneClaimable:

    def test_a_released_gate_allows_declare_milestone_done(self, mission):
        evidence = MilestoneEvidence(job_id="job-1", job_state="completed",
                                     gate_released=True)
        assert evaluate_milestone_done(mission, "M001", evidence) == ""

    def test_a_blocked_gate_refuses_and_shows_the_blocker(self, mission):
        evidence = MilestoneEvidence(job_id="job-1", job_state="completed",
                                     gate_released=False,
                                     gate_blocker="dod_blocking_red:tests")
        refusal = evaluate_milestone_done(mission, "M001", evidence)
        assert "is not met" in refusal
        assert "dod_blocking_red:tests" in refusal

    def test_the_execution_outcome_reports_the_gate(self, tmp_path, mission,
                                                    dispatched):
        def execute(job):
            return JobExecution(terminal_status="all_green",
                                job_status="completed", gate_released=True)

        run_mission(mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
                    root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
                    execute=execute,
                    call_fn=_scripted(_move_json("dispatch_job",
                                                 milestone_id="M001",
                                                 step="build the core")))
        detail = read_ledger(PROJECT, mission.id, tmp_path)[0]["outcome"]["detail"]
        assert "gate=released" in detail

    def test_an_ungated_job_says_so_rather_than_implying_green(
            self, tmp_path, mission, dispatched):
        run_mission(mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
                    root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
                    execute=_executed,
                    call_fn=_scripted(_move_json("dispatch_job",
                                                 milestone_id="M001",
                                                 step="build the core")))
        detail = read_ledger(PROJECT, mission.id, tmp_path)[0]["outcome"]["detail"]
        assert "gate=not-run" in detail


# ---------------------------------------------------------------------------
# F075 R-0190 — a gate that blocks twice in a row goes to a human
# ---------------------------------------------------------------------------
#
# With jobs finishing (R-0186) and the gate really running (R-0188), a blocked
# milestone made the model dispatch again and again until the iteration limit:
# six identical failed attempts, the R-0184 shape back for an honest reason.
# The loop's own refuse-once-then-escalate rule is the precedent.


class TestTheSecondBlockedCompletionEscalates:

    def _blocked(self, blocker: str = "dod_blocking_red:tests"):
        def execute(job):
            return JobExecution(terminal_status="all_green",
                                job_status="completed", gate_released=False,
                                gate_blocker=blocker)
        return execute

    def _released(self):
        def execute(job):
            return JobExecution(terminal_status="all_green",
                                job_status="completed", gate_released=True)
        return execute

    def _dispatch_moves(self, *milestones: str):
        return _scripted(*[_move_json("dispatch_job", milestone_id=m,
                                      step=f"work on {m}") for m in milestones])

    def test_two_blocked_completions_in_a_row_escalate(self, tmp_path, mission,
                                                       dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=self._blocked(), call_fn=self._dispatch_moves("M001", "M001"))
        assert result.terminal == TERMINAL_ESCALATED
        assert "M001" in result.detail
        assert "2 completed jobs in a row" in result.detail

    def test_the_escalation_names_both_blockers(self, tmp_path, mission,
                                                dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=self._blocked("dod_blocking_red:acc-001"),
            call_fn=self._dispatch_moves("M001", "M001"))
        assert result.detail.count("acc-001") == 2

    def test_the_escalation_says_what_budget_it_saved(self, tmp_path, mission,
                                                     dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=self._blocked(), call_fn=self._dispatch_moves("M001", "M001"))
        assert "more iteration(s) of this run's budget" in result.detail

    def test_the_first_block_is_still_a_retry_opportunity(self, tmp_path,
                                                          mission, dispatched):
        """One block escalates nothing — the context carries the blocker and
        the model gets its legitimate targeted-fix attempt."""
        result = run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=self._blocked(), call_fn=self._dispatch_moves("M001"))
        assert result.terminal == TERMINAL_ITERATION_LIMIT

    def test_a_released_gate_between_two_blocks_resets_the_streak(
            self, tmp_path, mission, dispatched):
        calls = {"n": 0}

        def execute(job):
            calls["n"] += 1
            released = calls["n"] == 2
            return JobExecution(terminal_status="all_green",
                                job_status="completed", gate_released=released,
                                gate_blocker="" if released else "dod_blocking_red:x")

        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=execute, call_fn=self._dispatch_moves("M001", "M001", "M001"))
        assert result.terminal == TERMINAL_ITERATION_LIMIT

    def test_blocks_on_two_different_milestones_do_not_escalate(
            self, tmp_path, mission, dispatched):
        """The streak is per milestone: two different ones are two first
        attempts, not a stuck loop."""
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=self._blocked(), call_fn=self._dispatch_moves("M001", "M002"))
        assert result.terminal == TERMINAL_ITERATION_LIMIT

    def test_the_escalation_lands_in_the_ledger(self, tmp_path, mission,
                                                dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=self._blocked(), call_fn=self._dispatch_moves("M001", "M001"))
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert entries[-1]["outcome"]["status"] == TERMINAL_ESCALATED
        assert "M001" in entries[-1]["outcome"]["detail"]

    def test_the_escalation_goes_through_the_existing_f051_verb(
            self, tmp_path, mission, dispatched):
        """Not a second escalation mechanism: the same hand_over the
        twice-refused path uses."""
        seen: list[str] = []

        def escalate(project_id, mission_id, reason):
            seen.append(reason)
            return "td:0001"

        result = run_mission(
            mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
            root=tmp_path, evidence=_no_evidence, dispatch=dispatched,
            execute=self._blocked(), escalate=escalate,
            call_fn=self._dispatch_moves("M001", "M001"))
        assert len(seen) == 1 and "M001" in seen[0]
        assert "td:0001" in result.detail

    def test_a_non_dispatch_move_does_not_disturb_the_streak(self, mission):
        """Unit-level: only dispatches count toward the streak."""
        from packages.orchestration.orchestrator_move_schema import OrchestratorMove

        move = OrchestratorMove.model_validate(
            json.loads(_move_json("wait_on_decisions", reason="waiting")))
        assert blocked_completion(move, MoveOutcome(status="waiting")) == ("", "")


# ---------------------------------------------------------------------------
# F075 R-0191 — the released-gate dispatch guard (the triad's third leg)
# ---------------------------------------------------------------------------
#
# The R7 re-proof dispatched M001 six times, every job completing with a
# RELEASED gate, and the model never claimed the milestone. In flight -> wait
# (R-0186); blocked twice -> escalate (R-0190); completed and released -> this.


class TestTheReleasedGateDispatchGuard:

    def _released(self, job_id: str = "job-0001"):
        return MilestoneEvidence(job_id=job_id, job_state="completed",
                                 gate_released=True)

    def test_a_dispatch_is_refused_when_the_work_is_done_and_proven(self, mission):
        refusal = evaluate_dispatch(mission, "M001", self._released())
        assert "already finished" in refusal
        assert "job-0001" in refusal

    def test_the_refusal_names_the_only_move_that_advances(self, mission):
        refusal = evaluate_dispatch(mission, "M001", self._released())
        assert "declare_milestone_done for M001" in refusal

    def test_a_blocked_gate_is_not_this_guards_business(self, mission):
        """R-0190 owns that case; two guards on one fact would fight."""
        evidence = MilestoneEvidence(job_id="job-1", job_state="completed",
                                     gate_released=False,
                                     gate_blocker="dod_blocking_red:x")
        assert evaluate_dispatch(mission, "M001", evidence) == ""

    def test_an_ungated_completed_job_is_not_refused(self, mission):
        """No stored DoD means no verdict — nothing is proven, so a further
        dispatch is legitimate."""
        evidence = MilestoneEvidence(job_id="job-1", job_state="completed")
        assert evaluate_dispatch(mission, "M001", evidence) == ""

    def test_an_in_flight_job_still_takes_the_r0186_path(self, mission):
        evidence = MilestoneEvidence(job_id="job-1", job_state="running",
                                     gate_released=True)
        refusal = evaluate_dispatch(mission, "M001", evidence)
        assert "in flight" in refusal
        assert "already finished" not in refusal

    def test_a_newer_unreleased_job_supersedes_an_older_released_one(
            self, tmp_path, mission, dispatched):
        """LATEST rules: the evidence collector reads the last job the ledger
        attributes to the milestone, so a newer un-released one wins."""
        newer = MilestoneEvidence(job_id="job-0002", job_state="completed",
                                  gate_released=False,
                                  gate_blocker="dod_blocking_red:x")
        assert evaluate_dispatch(mission, "M001", newer) == ""

    def test_the_verdict_is_read_not_re_derived(self):
        """The guard trusts load_gate_result's answer, which reaches it on the
        evidence — it never inspects checks itself."""
        import inspect

        from packages.orchestration.orchestrator_loop import (
            _released_gate_refusal,
        )
        source = inspect.getsource(_released_gate_refusal)
        assert "gate_released" in source
        assert "blocking_red" not in source and "checks" not in source

    def test_a_model_that_follows_the_instruction_achieves_the_mission(
            self, tmp_path, mission, dispatched):
        """End to end: refused dispatch -> re-prompt -> declaration -> achieved."""
        evidence = {"M001": self._released("job-0001"),
                    "M002": self._released("job-0002")}

        moves = _scripted(
            _move_json("dispatch_job", milestone_id="M001", step="redo it"),
            _move_json("declare_milestone_done", milestone_id="M001"),
            _move_json("declare_milestone_done", milestone_id="M002"),
            _move_json("declare_mission_achieved"),
        )
        result = run_mission(
            mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
            root=tmp_path, dispatch=dispatched, execute=_executed,
            evidence=lambda p, m, ms: evidence[ms], call_fn=moves)
        assert result.terminal == TERMINAL_ACHIEVED

    def test_the_ledger_shows_the_refusal_then_the_declaration(
            self, tmp_path, mission, dispatched):
        evidence = {"M001": self._released("job-0001"),
                    "M002": self._released("job-0002")}
        moves = _scripted(
            _move_json("dispatch_job", milestone_id="M001", step="redo it"),
            _move_json("declare_milestone_done", milestone_id="M001"),
            _move_json("declare_milestone_done", milestone_id="M002"),
            _move_json("declare_mission_achieved"),
        )
        run_mission(mission.id, LoopLimits(max_iterations=6), project_id=PROJECT,
                    root=tmp_path, dispatch=dispatched, execute=_executed,
                    evidence=lambda p, m, ms: evidence[ms], call_fn=moves)
        statuses = [e["outcome"]["status"]
                    for e in read_ledger(PROJECT, mission.id, tmp_path)]
        assert statuses[0] == OUTCOME_REFUSED
        assert "milestone_done" in statuses
        assert statuses[-1] == TERMINAL_ACHIEVED
        assert dispatched.seen == [], "no job was created for finished work"


# ---------------------------------------------------------------------------
# F075 R-0192 — a refused dispatch is not a dispatch
# ---------------------------------------------------------------------------
#
# The R-0191 guard made refused dispatch_job entries common, and
# dispatched_job_for kept the LAST such entry's job_id unconditionally — so a
# refusal (no job_id) erased the real attribution and the next declare move was
# refused with "no job was ever dispatched" for a milestone that was finished.


class TestARefusedDispatchDoesNotEraseTheAttribution:

    def _ledger(self, tmp_path, mission, *entries):
        for entry in entries:
            append_ledger_entry(PROJECT, mission.id, entry, tmp_path)

    def _dispatch_entry(self, iteration: int, milestone: str, job_id: str = ""):
        outcome = {"status": "dispatched" if job_id else OUTCOME_REFUSED,
                   "detail": "x"}
        if job_id:
            outcome["job_id"] = job_id
        return LedgerEntry(
            iteration=iteration, context_digest="d",
            move={"kind": "dispatch_job", "payload": {"milestone_id": milestone}},
            outcome=outcome, cost={"calls": 0, "usage": None,
                                   "usage_source": USAGE_UNMEASURED})

    def test_a_real_dispatch_followed_by_a_refusal_keeps_the_attribution(
            self, tmp_path, mission):
        self._ledger(tmp_path, mission,
                     self._dispatch_entry(1, "M001", "job-real"),
                     self._dispatch_entry(2, "M001"))
        assert dispatched_job_for(PROJECT, mission.id, "M001",
                                  tmp_path) == "job-real"

    def test_the_latest_real_dispatch_wins(self, tmp_path, mission):
        self._ledger(tmp_path, mission,
                     self._dispatch_entry(1, "M001", "job-one"),
                     self._dispatch_entry(2, "M001"),
                     self._dispatch_entry(3, "M001", "job-two"),
                     self._dispatch_entry(4, "M001"))
        assert dispatched_job_for(PROJECT, mission.id, "M001",
                                  tmp_path) == "job-two"

    def test_only_refusals_still_answers_nothing(self, tmp_path, mission):
        """Honest absence: no job was dispatched, and the answer says so."""
        self._ledger(tmp_path, mission,
                     self._dispatch_entry(1, "M001"),
                     self._dispatch_entry(2, "M001"))
        assert dispatched_job_for(PROJECT, mission.id, "M001", tmp_path) == ""

    def test_another_milestones_dispatch_is_not_borrowed(self, tmp_path, mission):
        self._ledger(tmp_path, mission,
                     self._dispatch_entry(1, "M002", "job-other"),
                     self._dispatch_entry(2, "M001"))
        assert dispatched_job_for(PROJECT, mission.id, "M001", tmp_path) == ""

    def test_the_r8_sequence_now_reaches_achieved(self, tmp_path, mission,
                                                  dispatched):
        """The live R8 trail, replayed: dispatch -> refused dispatch (R-0191)
        -> declare. It escalated before this fix; it achieves after it.

        The evidence is derived from the REAL ledger attribution, which is what
        makes this test load-bearing: with the old unconditional overwrite the
        refused entry blanks the job id and the declare move is refused.
        """
        def observe(project_id, mission_id, milestone_id):
            job_id = dispatched_job_for(project_id, mission_id, milestone_id,
                                        tmp_path)
            if not job_id:
                return MilestoneEvidence()
            return MilestoneEvidence(job_id=job_id, job_state="completed",
                                     gate_released=True)

        def execute(job):
            return JobExecution(terminal_status="all_green",
                                job_status="completed", gate_released=True)

        moves = _scripted(
            _move_json("dispatch_job", milestone_id="M001", step="build it"),
            # the R-0191 guard refuses this one; the re-prompt carries its advice
            _move_json("dispatch_job", milestone_id="M001", step="build it again"),
            _move_json("declare_milestone_done", milestone_id="M001"),
            _move_json("dispatch_job", milestone_id="M002", step="polish it"),
            _move_json("declare_milestone_done", milestone_id="M002"),
            _move_json("declare_mission_achieved"),
        )
        result = run_mission(
            mission.id, LoopLimits(max_iterations=8), project_id=PROJECT,
            root=tmp_path, dispatch=dispatched, execute=execute,
            evidence=observe, call_fn=moves)

        assert result.terminal == TERMINAL_ACHIEVED
        statuses = [e["outcome"]["status"]
                    for e in read_ledger(PROJECT, mission.id, tmp_path)]
        assert OUTCOME_REFUSED in statuses, "the R-0191 guard still fires"
        # The move the R8 run could not get past.
        assert "milestone_done" in statuses
        assert statuses[-1] == TERMINAL_ACHIEVED


# ---------------------------------------------------------------------------
# F075 R-0193 — the context says a milestone is ready BEFORE a refusal does
# ---------------------------------------------------------------------------
#
# R9's live run cost three iterations per milestone: dispatch, the R-0191
# refusal, then declare. The refusal is where the model learned the milestone
# was finished. Saying it in the context makes declare the DIRECT path; the
# refusal stays as the net for a model that ignores it.


class TestTheReleasedGateDirective:

    def _observe(self, **by_milestone):
        def observe(project_id, mission_id, milestone_id):
            return by_milestone.get(milestone_id, MilestoneEvidence())
        return observe

    def _released(self, job_id="job-0001"):
        return MilestoneEvidence(job_id=job_id, job_state="completed",
                                 gate_released=True)

    def test_a_released_milestone_gets_a_directive(self, mission):
        lines = released_milestone_directives(
            mission, self._observe(M001=self._released()),
            project_id=PROJECT, mission_id=mission.id)
        assert len(lines) == 1
        assert "M001" in lines[0] and "job-0001" in lines[0]
        assert "declare_milestone_done for M001" in lines[0]

    @pytest.mark.parametrize("evidence", [
        MilestoneEvidence(),                                        # nothing
        MilestoneEvidence(job_id="j", job_state="running",
                          gate_released=True),                      # in flight
        MilestoneEvidence(job_id="j", job_state="completed"),        # no verdict
        MilestoneEvidence(job_id="j", job_state="completed",
                          gate_released=False),                     # blocked
    ])
    def test_nothing_unproven_gets_a_directive(self, mission, evidence):
        assert released_milestone_directives(
            mission, self._observe(M001=evidence),
            project_id=PROJECT, mission_id=mission.id) == []

    def test_a_milestone_already_done_is_not_re_announced(self, tmp_path,
                                                          mission):
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        reloaded = load_mission(PROJECT, mission.id, tmp_path)
        assert released_milestone_directives(
            reloaded, self._observe(M001=self._released()),
            project_id=PROJECT, mission_id=mission.id) == []

    def test_an_observe_that_raises_costs_no_directive_and_no_crash(self, mission):
        def boom(*args):
            raise OSError("evidence unreadable")

        assert released_milestone_directives(
            mission, boom, project_id=PROJECT, mission_id=mission.id) == []

    def test_the_section_appears_in_the_context_bytes(self, mission):
        context = assemble_context(
            mission, directives=["- M001: … declare_milestone_done for M001."])
        assert SECTION_DIRECTIVES in context.text
        assert "declare_milestone_done for M001" in context.text

    def test_no_section_without_a_proven_milestone(self, mission):
        assert SECTION_DIRECTIVES not in assemble_context(mission).text

    def test_the_directive_reaches_the_prompt_of_a_live_loop(self, tmp_path,
                                                             mission, dispatched):
        """End to end through run_mission: the model sees it on iteration 2."""
        prompts: list[str] = []

        def call_fn(prompt, attempt):
            prompts.append(prompt)
            if len(prompts) == 1:
                return _move_json("dispatch_job", milestone_id="M001",
                                  step="build it")
            return _move_json("wait_on_decisions", reason="waiting")

        def execute(job):
            return JobExecution(terminal_status="all_green",
                                job_status="completed", gate_released=True)

        def observe(project_id, mission_id, milestone_id):
            if milestone_id != "M001":
                return MilestoneEvidence()
            if dispatched.seen:
                return self._released("job-0001")
            return MilestoneEvidence()

        run_mission(mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
                    root=tmp_path, dispatch=dispatched, execute=execute,
                    evidence=observe, call_fn=call_fn)
        assert SECTION_DIRECTIVES not in prompts[0], "nothing proven yet"
        assert "declare_milestone_done for M001" in prompts[1]

    def test_the_refusal_net_still_fires(self, mission):
        """The directive is guidance; the guard is the guarantee."""
        refusal = evaluate_dispatch(mission, "M001", self._released())
        assert "declare_milestone_done for M001" in refusal

    def test_a_model_that_follows_the_context_needs_two_iterations(
            self, tmp_path, mission, dispatched):
        """R9 spent three per milestone; following the directive spends two."""
        def execute(job):
            return JobExecution(terminal_status="all_green",
                                job_status="completed", gate_released=True)

        def observe(project_id, mission_id, milestone_id):
            job = dispatched_job_for(PROJECT, mission.id, milestone_id, tmp_path)
            if not job:
                return MilestoneEvidence()
            return MilestoneEvidence(job_id=job, job_state="completed",
                                     gate_released=True)

        moves = _scripted(
            _move_json("dispatch_job", milestone_id="M001", step="build it"),
            _move_json("declare_milestone_done", milestone_id="M001"),
            _move_json("dispatch_job", milestone_id="M002", step="polish it"),
            _move_json("declare_milestone_done", milestone_id="M002"),
            _move_json("declare_mission_achieved"),
        )
        result = run_mission(
            mission.id, LoopLimits(max_iterations=5), project_id=PROJECT,
            root=tmp_path, dispatch=dispatched, execute=execute,
            evidence=observe, call_fn=moves)
        assert result.terminal == TERMINAL_ACHIEVED
        assert result.iterations == 5, "two per milestone plus the achieve"
        statuses = [e["outcome"]["status"]
                    for e in read_ledger(PROJECT, mission.id, tmp_path)]
        assert OUTCOME_REFUSED not in statuses, "no iteration spent on a refusal"


# ---------------------------------------------------------------------------
# F075 R-0196 — a retryable failure costs the iteration, not the mission
# ---------------------------------------------------------------------------
#
# Campaign attempt 02 found the boundary ending three missions at iteration 1
# on transient faults, with zero milestones and therefore no DoD verdict at
# all. g07 proved in the same campaign that degrade-and-continue is possible;
# these tests pin that the boundary now does it, and — just as load-bearing —
# that it still refuses to do it for a fault Remedy cannot name.

class TestTheBoundaryContinuesOnRetryableFailures:

    def _released(self, job_id: str = "job-0001") -> MilestoneEvidence:
        return MilestoneEvidence(job_id=job_id, job_state="completed",
                                 gate_released=True)

    def _finishing(self, tmp_path, mission, dispatched):
        """Deps for a mission that can actually reach `achieved`."""
        def execute(job):
            return JobExecution(terminal_status="all_green",
                                job_status="completed", gate_released=True)

        def observe(project_id, mission_id, milestone_id):
            job = dispatched_job_for(PROJECT, mission.id, milestone_id, tmp_path)
            return self._released(job) if job else MilestoneEvidence()

        return {"dispatch": dispatched, "execute": execute, "evidence": observe}

    def _plan_moves(self):
        return [
            _move_json("dispatch_job", milestone_id="M001", step="build it"),
            _move_json("declare_milestone_done", milestone_id="M001"),
            _move_json("dispatch_job", milestone_id="M002", step="polish it"),
            _move_json("declare_milestone_done", milestone_id="M002"),
            _move_json("declare_mission_achieved"),
        ]

    def _raises_once(self, exc: BaseException):
        """A provider that fails its FIRST call and then plays the script."""
        script = self._plan_moves()
        calls: list[int] = []

        def call_fn(prompt, attempt):
            calls.append(attempt)
            if len(calls) == 1:
                raise exc
            index = min(len(calls) - 2, len(script) - 1)
            return script[index]

        return call_fn

    def test_a_provider_error_costs_one_iteration_and_the_mission_finishes(
            self, tmp_path, mission, dispatched):
        """The g06 shape: HTTP 503 on the first move used to end the run."""
        boom = ConnectionError("provider API error mid-move: the model host "
                               "returned HTTP 503 and closed the connection")
        result = run_mission(mission.id, LoopLimits(max_iterations=8),
                             project_id=PROJECT, root=tmp_path, call_fn=
                             self._raises_once(boom),
                             **self._finishing(tmp_path, mission, dispatched))
        assert result.terminal == TERMINAL_ACHIEVED
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert entries[0]["outcome"]["status"] == OUTCOME_ITERATION_RETRYING
        assert "HTTP 503" in entries[0]["outcome"]["detail"]
        assert entries[-1]["outcome"]["status"] == TERMINAL_ACHIEVED

    def test_the_failed_iteration_still_writes_its_postmortem(
            self, tmp_path, mission, dispatched):
        """Continuing must not turn the failure into a silence."""
        boom = ConnectionError("provider API error mid-move: HTTP 503")
        run_mission(mission.id, LoopLimits(max_iterations=8), project_id=PROJECT,
                    root=tmp_path, call_fn=self._raises_once(boom),
                    **self._finishing(tmp_path, mission, dispatched))
        written = sorted(mission_evidence_dir(PROJECT, mission.id, tmp_path)
                         .rglob("postmortem.json"))
        assert len(written) == 1
        body = json.loads(written[0].read_text(encoding="utf-8"))
        assert body["failure_class"] == "provider_unavailable"

    def test_a_machine_fault_mid_write_costs_one_iteration_too(
            self, tmp_path, mission, dispatched):
        """The g09 shape: killed while writing the dossier."""
        deaths: list[int] = []

        def die(project_id, mission_id, mission, **kwargs):
            deaths.append(1)
            if len(deaths) == 1:
                raise OSError("harness death mid-write: killed while writing "
                              "the dossier")

        result = run_mission(mission.id, LoopLimits(max_iterations=8),
                             project_id=PROJECT, root=tmp_path,
                             call_fn=_scripted(*self._plan_moves()),
                             update_dossier=die,
                             **self._finishing(tmp_path, mission, dispatched))
        assert result.terminal == TERMINAL_ACHIEVED
        entries = read_ledger(PROJECT, mission.id, tmp_path)
        assert entries[0]["outcome"]["status"] == OUTCOME_ITERATION_RETRYING
        body = json.loads(sorted(mission_evidence_dir(PROJECT, mission.id,
                                                      tmp_path)
                                 .rglob("postmortem.json"))[0]
                          .read_text(encoding="utf-8"))
        assert body["failure_class"] == "io_failure"

    def test_two_in_a_row_on_one_milestone_reaches_a_human(self, tmp_path,
                                                           mission):
        """A fault that is not passing is not worth the rest of the budget."""
        handed: list[str] = []

        def escalate(project_id, mission_id, reason):
            handed.append(reason)
            return "decision-0001"

        def always(prompt, attempt):
            raise ConnectionError("provider API error mid-move: HTTP 503")

        result = run_mission(mission.id, LoopLimits(max_iterations=9),
                             project_id=PROJECT, root=tmp_path, call_fn=always,
                             escalate=escalate)
        assert result.terminal == TERMINAL_ESCALATED
        assert result.iterations == BOUNDARY_FAILURES_BEFORE_ESCALATION
        assert len(handed) == 1
        assert handed[0].count("HTTP 503") == 2, "both failures named"
        assert "M001" in handed[0], "the milestone that was being worked"

    def test_a_successful_iteration_clears_the_streak(self, tmp_path, mission,
                                                      dispatched):
        """Two failures far apart are not two in a row."""
        script = self._plan_moves()
        calls: list[int] = []

        def call_fn(prompt, attempt):
            calls.append(attempt)
            if len(calls) in (1, 3):
                raise ConnectionError("provider API error mid-move: HTTP 503")
            index = min(len(calls) - (3 if len(calls) > 3 else 2),
                        len(script) - 1)
            return script[index]

        result = run_mission(mission.id, LoopLimits(max_iterations=9),
                             project_id=PROJECT, root=tmp_path, call_fn=call_fn,
                             **self._finishing(tmp_path, mission, dispatched))
        assert result.terminal == TERMINAL_ACHIEVED, \
            "the dispatch between them reset the streak"
        statuses = [e["outcome"]["status"]
                    for e in read_ledger(PROJECT, mission.id, tmp_path)]
        assert statuses.count(OUTCOME_ITERATION_RETRYING) == 2
        assert TERMINAL_ESCALATED not in statuses

    @pytest.mark.parametrize("text, expected", [
        ("the flurb did not glorp", "unknown"),
        # A timeout IS a provider fault and is still not in the set: the
        # decision named two classes, not "anything provider-shaped".
        ("request timed out", "provider_timeout"),
    ])
    def test_a_class_outside_the_narrow_set_still_ends_the_run(
            self, tmp_path, mission, text, expected):
        """Retrying a fault Remedy cannot name is how a budget disappears."""
        def boom(prompt, attempt):
            raise RuntimeError(text)

        result = run_mission(mission.id, LoopLimits(max_iterations=6),
                             project_id=PROJECT, root=tmp_path, call_fn=boom)
        assert result.terminal == TERMINAL_ITERATION_FAILED
        assert result.iterations == 1, "one catch, then the run ends"
        body = json.loads(sorted(mission_evidence_dir(PROJECT, mission.id,
                                                      tmp_path)
                                 .rglob("postmortem.json"))[0]
                          .read_text(encoding="utf-8"))
        assert body["failure_class"] == expected

    def test_the_retryable_set_is_exactly_the_two_named_classes(self):
        """NARROW by decision. Widening it is a reviewed change, not a typo."""
        assert RETRYABLE_FAILURE_CLASSES == frozenset(
            {"provider_unavailable", "io_failure"})

    def test_the_working_milestone_is_the_first_one_not_done(self, tmp_path,
                                                             mission):
        assert working_milestone(mission) == "M001"
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        assert working_milestone(
            load_mission(PROJECT, mission.id, tmp_path)) == "M002"

    def test_an_operator_stop_is_still_not_a_failure_to_classify(self, tmp_path,
                                                                 mission):
        """KeyboardInterrupt and SystemExit never became retryable."""
        for stopper in (KeyboardInterrupt, SystemExit):
            def raising(*args, **kwargs):
                raise stopper()

            with pytest.raises(stopper):
                run_mission(mission.id, LoopLimits(max_iterations=4),
                            project_id=PROJECT, root=tmp_path, call_fn=raising)


class TestOrchestratorEvidenceSink:
    """`run_mission` owns the mission's evidence dir, so it owns the trace file.

    The sink lives in the loop rather than in a caller (DECISION F105 D11), so
    both production callers inherit it. Shape copied from
    `TestMissionPlanEvidenceSink` in `test_mission_compiler.py`.
    """

    def _trace_path(self, mission, tmp_path):
        return (mission_evidence_dir(PROJECT, mission.id, tmp_path)
                / "prompt_trace.jsonl")

    def _run_once(self, tmp_path, mission, dispatched, **kwargs):
        return run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control", **kwargs)

    def test_a_run_writes_one_labelled_row_per_call(self, tmp_path, mission,
                                                    dispatched):
        self._run_once(tmp_path, mission, dispatched,
                       provider="ollama", provider_kind="ollama")

        rows = [json.loads(line) for line
                in self._trace_path(mission, tmp_path).read_text().splitlines()
                if line]
        assert len(rows) == 1
        assert rows[0]["role"] == "orchestrator"
        assert rows[0]["provider"] == "ollama"
        assert rows[0]["segment_manifest"]

    def test_a_second_run_appends_rather_than_truncating(self, tmp_path,
                                                         mission, dispatched):
        """A second `remedy mission run` must not erase the first's evidence."""
        self._run_once(tmp_path, mission, dispatched)
        first = self._trace_path(mission, tmp_path).read_text()
        self._run_once(tmp_path, mission, dispatched)

        body = self._trace_path(mission, tmp_path).read_text()
        assert len([line for line in body.splitlines() if line]) == 2
        assert body.startswith(first), "the first run's row survived"

    def test_no_provider_leaves_no_trace_file(self, tmp_path, mission,
                                             dispatched):
        """Nothing was sent, so there is no evidence file pretending it was."""
        result = run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=None, root=tmp_path, dispatch=dispatched, execute=_executed,
            control_root_path=tmp_path / "control")

        assert result.terminal == TERMINAL_NO_PROVIDER
        assert not self._trace_path(mission, tmp_path).exists()

    def test_the_cli_names_the_provider_it_runs_with(self):
        """A source guard, because an unwired CLI leaves every gate green.

        The tests above drive `run_mission` directly, so they stay green even if
        `remedy mission run` stops passing the provider. This pins the one line
        they cannot reach. Formatting-sensitive by nature — the same declared
        trade-off as `test_the_cli_names_the_provider_it_planned_with`.

        Scoped to THIS call site, never a file-wide count: the plan call in the
        same module carries its own label, and a count would make one of the two
        guards unsatisfiable (checklist item 7, finding R-0258). The window is
        200 characters from the call's start, which is the call plus 27
        characters of what follows it — measured, not the call expression
        exactly (R-0260). It stays clear of the plan call's label by thousands
        of characters, which is the property this guard exists to hold. The
        exact gap is deliberately not quoted (R-0261): no assertion pins it,
        so a number here would go stale on the next edit to mission_cmd.py.
        """
        source = (Path(__file__).resolve().parents[2]
                  / "apps" / "cli" / "commands" / "mission_cmd.py").read_text()
        ran = source.index("result = run_mission(")
        assert 'provider_kind="ollama"' in source[ran:ran + 200]

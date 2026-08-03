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
    set_mission_plan,
    set_mission_status,
)
from packages.orchestration.orchestrator_loop import (
    CONFIG_KEY_MAX_ITERATIONS,
    DEFAULT_MAX_ITERATIONS,
    DOSSIER_FILENAME,
    LEDGER_FILENAME,
    MILESTONES_DONE_KEY,
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
    TERMINAL_ITERATION_LIMIT,
    TERMINAL_NO_PROVIDER,
    TERMINAL_NOT_ACTIVE,
    TERMINAL_STOPPED,
    TERMINAL_WAITING,
    USAGE_UNMEASURED,
    LedgerEntry,
    LoopLimits,
    MilestoneEvidence,
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
            dispatch=dispatched, control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_WAITING
        assert result.iterations == 1

    def test_dispatch_job_goes_through_the_dispatch_verb(self, tmp_path,
                                                         mission, dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="build M001")),
            root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched, evidence=_met_evidence,
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
            root=tmp_path, dispatch=dispatched,
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_ACHIEVED
        assert load_mission(PROJECT, mission.id, tmp_path).status == "achieved"

    def test_abort_with_reason_abandons_and_records_why(self, tmp_path,
                                                        mission, dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=_scripted(_move_json("abort_with_reason",
                                         reason="the plan is unbuildable")),
            root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched,
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_INVALID_MOVE
        assert result.entries[-1].outcome["detail"].startswith("parse-class")

    def test_no_provider_is_a_terminal_not_an_exception(self, tmp_path,
                                                        mission, dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=None, root=tmp_path, dispatch=dispatched,
            control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_NO_PROVIDER
        assert len(result.entries) == 1

    def test_the_iteration_limit_is_a_normal_terminal(self, tmp_path, mission,
                                                      dispatched):
        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("dispatch_job", milestone_id="M001",
                                         step="keep going")),
            root=tmp_path, dispatch=dispatched,
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
            dispatch=dispatched, control_root_path=tmp_path / "control")
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
            root=tmp_path, dispatch=dispatch, control_root_path=control)

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
            dispatch=dispatched, control_root_path=control)
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
            root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched, evidence=_no_evidence,
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
            call_fn=call_fn, root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched, evidence=_no_evidence,
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
            call_fn=call_fn, root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched,
            update_dossier=lambda p, m, mission: seen.append(m),
            control_root_path=tmp_path / "control")
        assert seen == [mission.id] * 3

    def test_the_default_update_writes_the_dossier_beside_the_ledger(
            self, tmp_path, mission, dispatched):
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, control_root_path=tmp_path / "control")
        path = ledger_path(PROJECT, mission.id, tmp_path).parent / DOSSIER_FILENAME
        assert path.is_file()
        assert "Ship the thing" in path.read_text()

    def test_the_update_tracks_the_mission_as_it_changes(self, tmp_path,
                                                         mission, dispatched):
        mark_milestone_done(PROJECT, mission.id, "M001", tmp_path)
        run_mission(
            mission.id, LoopLimits(max_iterations=1), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, control_root_path=tmp_path / "control")
        text = (ledger_path(PROJECT, mission.id, tmp_path).parent
                / DOSSIER_FILENAME).read_text()
        assert "M001 [done]" in text
        assert "M002 [open]" in text


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
            root=tmp_path, dispatch=dispatched, evidence=evidence,
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
            root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched,
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
            root=tmp_path, dispatch=dispatched,
            control_root_path=tmp_path / "control")
        assert dispatched_job_for(PROJECT, mission.id, "M001",
                                  tmp_path) == "job-0001"
        assert dispatched_job_for(PROJECT, mission.id, "M002", tmp_path) == ""

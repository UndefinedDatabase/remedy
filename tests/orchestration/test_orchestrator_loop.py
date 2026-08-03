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

Every provider here is a local callable returning recorded text — no network,
no process, no real model. Every test writes into ``tmp_path``: the mission
root is passed explicitly via ``root=``, so the repository's real data root is
never touched.
"""
from __future__ import annotations

import json

import pytest

from packages.orchestration.mission_plan_schema import (
    MISSION_PLAN_SCHEMA_V,
    Milestone,
    MissionPlan,
)
from packages.orchestration.mission_state import (
    create_mission,
    load_mission,
    set_mission_plan,
)
from packages.orchestration.orchestrator_loop import (
    PROTOCOL_DOC_RELATIVE,
    PROTOCOL_VERSION,
    SECTION_DECISIONS,
    SECTION_DOSSIER,
    SECTION_PLAN,
    SECTION_REPORT,
    assemble_context,
    build_orchestrator_system_prompt,
    context_digest,
    orchestrator_protocol_text,
    protocol_document_path,
    render_mission_dossier,
)
from packages.orchestration.orchestrator_move_schema import (
    MAX_PAYLOAD_VALUE_CHARS,
    ORCHESTRATOR_MOVE_KINDS,
    ORCHESTRATOR_MOVE_SCHEMA_V,
    OrchestratorMove,
)
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
        """Self-modification is a Do-not-touch. The absence IS the enforcement."""
        import packages.orchestration.orchestrator_loop as loop

        source = (loop.__file__ or "")
        text = open(source, encoding="utf-8").read()
        assert "protocol_document_path" in text
        for writer in (".write_text(", "write_protocol", "open(protocol"):
            assert writer not in text, (
                f"the loop must not be able to write its own protocol ({writer})")


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

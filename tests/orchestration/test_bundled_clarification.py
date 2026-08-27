"""F034 T001 — intake clarifications ride the single approval decision.

Covers the contract half: stable question ids assigned by intake order,
carry-through into the plan with empty answer/answered_by, embedding into
the fp:approval decision payload, and the zero-clarification regression
(the approval flow must be identical to the plain plan).
"""

from __future__ import annotations

from packages.core.models import Job
from packages.orchestration.decision_queue import export_decision_json, list_decisions
from packages.orchestration.flight_plan import (
    _build_plan_prompt,
    apply_clarification_answers,
    carry_intake_clarifications,
    clarification_source,
    clarifications_already_resolved,
    open_clarification_questions,
    render_assumptions_md,
    render_plan_md,
    write_assumptions_md,
)
from packages.orchestration.schemas.models import FlightPlan


def _task(tid: str, **kw):
    d = {
        "id": tid,
        "title": f"Task {tid}",
        "goal": "do the thing",
        "acceptance": ["it works"],
        "est_tokens_band": "S",
    }
    d.update(kw)
    return d


def _plan(**kw) -> FlightPlan:
    d = {"schema_v": "flight_plan_v1", "tasks": [_task("T1")]}
    d.update(kw)
    return FlightPlan(**d)


def _intake(*clarifications) -> dict:
    return {
        "schema_v": "ji1",
        "goal": "ship it",
        "clarifications": list(clarifications),
    }


_Q_DB = {
    "question": "Which database?",
    "default_answer": "keep the existing SQLite file",
    "impact": "driver choice and migration work",
}
_Q_AUTH = {
    "question": "Add auth?",
    "default_answer": "no, leave auth untouched",
    "impact": "scope of the change",
}


class TestCarryIntakeClarifications:

    def test_ids_assigned_by_intake_order(self):
        plan = carry_intake_clarifications(_plan(), _intake(_Q_DB, _Q_AUTH))
        assert [c.id for c in plan.clarifications_resolved] == ["q1", "q2"]
        assert plan.clarifications_resolved[0].question == "Which database?"
        assert plan.clarifications_resolved[1].question == "Add auth?"

    def test_carried_questions_start_unanswered(self):
        plan = carry_intake_clarifications(_plan(), _intake(_Q_DB))
        c = plan.clarifications_resolved[0]
        assert c.answer == ""
        assert c.answered_by == ""
        assert c.default_answer == "keep the existing SQLite file"
        assert c.impact == "driver choice and migration work"

    def test_ids_stable_across_regeneration(self):
        intake = _intake(_Q_DB, _Q_AUTH)
        first = carry_intake_clarifications(_plan(), intake)
        second = carry_intake_clarifications(_plan(tasks=[_task("A"), _task("B")]), intake)
        assert ([(c.id, c.question) for c in first.clarifications_resolved]
                == [(c.id, c.question) for c in second.clarifications_resolved])

    def test_planner_echo_of_intake_question_stays_open(self):
        """The planner answering an intake question does not close it."""
        echoed = dict(_Q_DB, answer="postgres")
        plan = carry_intake_clarifications(
            _plan(clarifications_resolved=[echoed]), _intake(_Q_DB))
        assert len(plan.clarifications_resolved) == 1
        assert plan.clarifications_resolved[0].answer == ""
        assert plan.clarifications_resolved[0].id == "q1"

    def test_planner_assumption_preserved_after_intake_questions(self):
        assumption = {
            "question": "Which test runner?",
            "default_answer": "pytest",
            "impact": "test invocation",
            "answer": "pytest",
        }
        plan = carry_intake_clarifications(
            _plan(clarifications_resolved=[assumption]), _intake(_Q_DB))
        assert [c.id for c in plan.clarifications_resolved] == ["q1", "q2"]
        assert plan.clarifications_resolved[1].answer == "pytest"
        assert plan.clarifications_resolved[1].answered_by == ""

    def test_zero_clarifications_plan_unchanged(self):
        plan = _plan()
        assert carry_intake_clarifications(plan, _intake()) is plan
        assert carry_intake_clarifications(plan, None) is plan
        assert plan.clarifications_resolved == []


class TestOpenClarificationQuestions:

    def test_answered_entries_are_not_open(self):
        records = [
            {"id": "q1", "question": "Which database?",
             "default_answer": "sqlite", "impact": "driver", "answer": "",
             "answered_by": ""},
            {"id": "q2", "question": "Which test runner?",
             "default_answer": "pytest", "impact": "cmd", "answer": "pytest",
             "answered_by": ""},
            {"id": "q3", "question": "Add auth?", "default_answer": "no",
             "impact": "scope", "answer": "no", "answered_by": "default"},
        ]
        assert [q["id"] for q in open_clarification_questions(records)] == ["q1"]

    def test_empty_and_none_inputs(self):
        assert open_clarification_questions(None) == []
        assert open_clarification_questions([]) == []


class TestApplyClarificationAnswers:
    """T002 — write-back: supplied answer wins, everything else defaults."""

    def _open(self, qid, question, default):
        return {"id": qid, "question": question, "default_answer": default,
                "impact": "some impact", "answer": "", "answered_by": ""}

    def test_mixed_human_and_default(self):
        records = [
            self._open("q1", "Which database?", "keep the existing SQLite file"),
            self._open("q2", "Add auth?", "no, leave auth untouched"),
        ]
        out = apply_clarification_answers(records, {"q1": "use PostgreSQL"})
        assert out[0]["answer"] == "use PostgreSQL"
        assert out[0]["answered_by"] == "human"
        assert out[1]["answer"] == "no, leave auth untouched"
        assert out[1]["answered_by"] == "default"

    def test_no_answers_means_all_defaults(self):
        records = [self._open("q1", "Which database?", "keep SQLite")]
        out = apply_clarification_answers(records, None)
        assert out[0] == dict(records[0], answer="keep SQLite",
                              answered_by="default")

    def test_conservative_keep_style_default_survives_round_trip(self):
        """A9: defaults are keep/no-op, and the log must show exactly that."""
        records = [self._open("q1", "Drop the legacy table?",
                              "keep the legacy table untouched")]
        out = apply_clarification_answers(records, None)
        assert out[0]["answer"] == "keep the legacy table untouched"
        assert out[0]["answered_by"] == "default"

    def test_planner_assumption_untouched(self):
        assumption = {"id": "q1", "question": "Which test runner?",
                      "default_answer": "pytest", "impact": "cmd",
                      "answer": "pytest", "answered_by": ""}
        out = apply_clarification_answers([assumption], None)
        assert out[0] == assumption

    def test_already_resolved_records_untouched(self):
        resolved = {"id": "q1", "question": "Add auth?", "default_answer": "no",
                    "impact": "scope", "answer": "yes", "answered_by": "human"}
        out = apply_clarification_answers([resolved], {"q1": "changed"})
        assert out[0]["answer"] == "yes"
        assert out[0]["answered_by"] == "human"

    def test_input_records_not_mutated(self):
        records = [self._open("q1", "Which database?", "keep SQLite")]
        apply_clarification_answers(records, {"q1": "postgres"})
        assert records[0]["answer"] == ""
        assert records[0]["answered_by"] == ""

    def test_empty_input(self):
        assert apply_clarification_answers(None, {"q1": "x"}) == []
        assert apply_clarification_answers([], None) == []


class TestClarificationsAlreadyResolved:

    def test_open_plan_is_not_resolved(self):
        plan = carry_intake_clarifications(_plan(), _intake(_Q_DB, _Q_AUTH))
        assert clarifications_already_resolved(
            [c.model_dump() for c in plan.clarifications_resolved]) is False

    def test_planner_assumption_alone_is_not_resolved(self):
        assumption = {"id": "q1", "question": "Which test runner?",
                      "default_answer": "pytest", "impact": "cmd",
                      "answer": "pytest", "answered_by": ""}
        assert clarifications_already_resolved([assumption]) is False

    def test_written_back_plan_is_resolved(self):
        plan = carry_intake_clarifications(_plan(), _intake(_Q_DB))
        records = apply_clarification_answers(
            [c.model_dump() for c in plan.clarifications_resolved], None)
        assert clarifications_already_resolved(records) is True

    def test_empty_input(self):
        assert clarifications_already_resolved(None) is False
        assert clarifications_already_resolved([]) is False


#: T003 golden log: one human answer, one default, one planner assumption.
_GOLDEN_RECORDS = [
    {"id": "q1", "question": "Which database?",
     "default_answer": "keep the existing SQLite file",
     "impact": "driver choice and migration work",
     "answer": "use PostgreSQL", "answered_by": "human"},
    {"id": "q2", "question": "Add auth?",
     "default_answer": "no, leave auth untouched",
     "impact": "scope of the change",
     "answer": "no, leave auth untouched", "answered_by": "default"},
    {"id": "q3", "question": "Which test runner?",
     "default_answer": "pytest", "impact": "test invocation",
     "answer": "pytest", "answered_by": ""},
]

_GOLDEN_LOG = """\
# Assumptions

Every question below was asked once, at plan time, on the single \
plan-approval decision. Nothing here was asked mid-run.

| ID | Question | Answer | Source | Impact |
| --- | --- | --- | --- | --- |
| q1 | Which database? | use PostgreSQL | human | driver choice and migration work |
| q2 | Add auth? | no, leave auth untouched | default | scope of the change |
| q3 | Which test runner? | pytest | planner | test invocation |

Sources: 1 human, 1 default, 1 planner, 0 unresolved.
"""


class TestAssumptionLog:
    """T003 — the audit artifact reviewers read."""

    def test_golden_log(self):
        assert render_assumptions_md(_GOLDEN_RECORDS) == _GOLDEN_LOG

    def test_sources_classified(self):
        assert [clarification_source(r) for r in _GOLDEN_RECORDS] == [
            "human", "default", "planner"]

    def test_unanswered_question_is_unresolved(self):
        assert clarification_source(
            {"id": "q1", "answer": "", "answered_by": ""}) == "unresolved"

    def test_accepts_plan_models(self):
        plan = carry_intake_clarifications(_plan(), _intake(_Q_DB))
        log = render_assumptions_md(plan.clarifications_resolved)
        assert "| q1 | Which database?" in log
        assert "unresolved" in log

    def test_no_clarifications_states_so(self):
        for empty in (None, []):
            log = render_assumptions_md(empty)
            assert "No clarifications" in log
            assert "|" not in log

    def test_pipes_and_newlines_do_not_break_the_table(self):
        log = render_assumptions_md([{
            "id": "q1", "question": "a | b\nc", "default_answer": "d",
            "impact": "e", "answer": "f | g", "answered_by": "human"}])
        row = [ln for ln in log.splitlines() if ln.startswith("| q1 ")][0]
        # Six cell delimiters; the pipes inside the text are escaped, so
        # the row still has exactly five columns.
        assert row.replace("\\|", "").count("|") == 6
        assert "a \\| b c" in row

    def test_write_creates_evidence_file(self, tmp_path):
        path = write_assumptions_md(_GOLDEN_RECORDS, tmp_path / "evidence")
        assert path.name == "assumptions.md"
        assert path.read_text(encoding="utf-8") == _GOLDEN_LOG

    def test_plan_md_links_to_the_log(self):
        plan = carry_intake_clarifications(_plan(), _intake(_Q_DB))
        rendered = render_plan_md(plan)
        assert "[assumptions.md](assumptions.md)" in rendered
        assert "**Q:** [q1] Which database?" in rendered

    def test_plan_md_without_clarifications_has_no_link(self):
        assert "assumptions.md" not in render_plan_md(_plan())


class TestPlannerPrompt:
    """T004 — the prompt must aim for zero questions and safe defaults."""

    def test_instructs_the_model_to_resolve_what_it_can(self):
        prompt = _build_plan_prompt({"schema_v": "ji1", "goal": "ship"})
        assert "RESOLVE the intake's clarifications into plan choices" in prompt
        assert "zero questions" in prompt

    def test_carries_forward_only_ambiguous_questions(self):
        prompt = _build_plan_prompt({"schema_v": "ji1", "goal": "ship"})
        assert "ONLY genuinely ambiguous questions" in prompt
        assert "plan-approval gate" in prompt

    def test_mandates_conservative_defaults_with_impact(self):
        prompt = _build_plan_prompt({"schema_v": "ji1", "goal": "ship"})
        assert "conservative default_answer and an impact" in prompt
        assert "never\n  deletes, overwrites, migrates" in prompt

    def test_keep_style_default_survives_the_round_trip(self):
        """A9 fixture: the safe default reaches the log unchanged."""
        keep_style = {
            "question": "Drop the legacy table?",
            "default_answer": "keep the legacy table untouched",
            "impact": "data retained; migration deferred",
        }
        plan = carry_intake_clarifications(_plan(), _intake(keep_style))
        records = apply_clarification_answers(
            [c.model_dump() for c in plan.clarifications_resolved], None)
        assert records[0]["answer"] == "keep the legacy table untouched"
        assert records[0]["answered_by"] == "default"
        assert ("| q1 | Drop the legacy table? | keep the legacy table "
                "untouched | default |") in render_assumptions_md(records)


class TestApprovalDecisionPayload:

    def _pending_job(self, *clarifications) -> Job:
        plan = carry_intake_clarifications(_plan(), _intake(*clarifications))
        fp = plan.model_dump()
        fp["_approval"] = "pending"
        return Job(name="t", flight_plan=fp)

    def _fp_decision(self, job: Job):
        found = [d for d in list_decisions(job, [])
                 if d.type == "flight_plan_approval"]
        assert len(found) == 1, "exactly ONE decision per plan"
        return found[0]

    def test_two_questions_one_decision_with_payload(self):
        d = self._fp_decision(self._pending_job(_Q_DB, _Q_AUTH))
        questions = d.payload["clarifications"]
        assert [q["id"] for q in questions] == ["q1", "q2"]
        assert questions[0] == {
            "id": "q1",
            "question": "Which database?",
            "default_answer": "keep the existing SQLite file",
            "impact": "driver choice and migration work",
        }

    def test_summary_reports_open_question_count(self):
        d = self._fp_decision(self._pending_job(_Q_DB, _Q_AUTH))
        assert "2 open questions" in d.safe_summary

    def test_next_actions_show_the_answer_form(self):
        d = self._fp_decision(self._pending_job(_Q_DB))
        actions = " ".join(d.next_actions)
        assert '--answer q1="..."' in actions
        assert "--reason approve" in actions
        assert "--reason reject" in actions

    def test_payload_exported_as_json(self):
        d = self._fp_decision(self._pending_job(_Q_DB))
        exported = export_decision_json(d)
        assert exported["payload"]["clarifications"][0]["id"] == "q1"

    def test_zero_clarifications_matches_plain_plan(self):
        bundled_job = self._pending_job()
        plain_job = Job(name="t", flight_plan={"_approval": "pending"})
        bundled = self._fp_decision(bundled_job)
        plain = self._fp_decision(plain_job)

        def _shape(d, job):
            # The job id is the only legitimate difference between the two.
            return tuple(a.replace(str(job.id)[:8], "<job>") for a in d.next_actions)

        assert bundled.payload == {"options": ["approve", "reject"]}
        assert bundled.safe_summary == plain.safe_summary
        assert _shape(bundled, bundled_job) == _shape(plain, plain_job)
        assert bundled.severity == plain.severity == "blocker"

    def test_legacy_plan_without_ids_still_loads(self):
        """Pre-F034 fp1 data has no id/answered_by fields."""
        legacy = FlightPlan(**{
            "schema_v": "flight_plan_v1",
            "tasks": [_task("T1")],
            "clarifications_resolved": [{
                "question": "Which DB?", "default_answer": "postgres",
                "impact": "driver", "answer": "postgres",
            }],
        })
        c = legacy.clarifications_resolved[0]
        assert c.id == ""
        assert c.answered_by == ""
        fp = legacy.model_dump()
        fp["_approval"] = "pending"
        d = self._fp_decision(Job(name="t", flight_plan=fp))
        assert d.payload == {"options": ["approve", "reject"]}

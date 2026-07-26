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
    carry_intake_clarifications,
    open_clarification_questions,
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

        assert bundled.payload == {}
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
        assert d.payload == {}

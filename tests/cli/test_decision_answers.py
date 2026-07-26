"""F034 T001 — per-question answers on `remedy decision resolve`.

The bundled questions are answered on the ONE plan-approval decision:
`--answer q1="..."` is repeatable, answering a subset is valid, and an
unknown question id is a clean non-zero error.
"""

from __future__ import annotations

import pytest

from apps.cli.commands.decision import (
    AnswerParseError,
    _cmd_decision_resolve,
    parse_answer_options,
)
from packages.core.models import Job
from packages.orchestration.flight_plan import carry_intake_clarifications
from packages.orchestration.schemas.models import FlightPlan

_QUESTIONS = [
    {"id": "q1", "question": "Which database?",
     "default_answer": "keep SQLite", "impact": "driver choice"},
    {"id": "q2", "question": "Add auth?",
     "default_answer": "no, leave auth untouched", "impact": "scope"},
]


def _pending_job() -> Job:
    plan = carry_intake_clarifications(
        FlightPlan(**{
            "schema_v": "flight_plan_v1",
            "tasks": [{
                "id": "T1", "title": "T", "goal": "g",
                "acceptance": ["ok"], "est_tokens_band": "S",
            }],
        }),
        {"schema_v": "ji1", "goal": "ship",
         "clarifications": [
             {k: q[k] for k in ("question", "default_answer", "impact")}
             for q in _QUESTIONS
         ]},
    )
    fp = plan.model_dump()
    fp["_approval"] = "pending"
    return Job(name="t", flight_plan=fp)


class TestParseAnswerOptions:

    def test_no_answers(self):
        assert parse_answer_options(None, _QUESTIONS) == {}
        assert parse_answer_options([], _QUESTIONS) == {}

    def test_answer_one_of_two_is_valid(self):
        assert parse_answer_options(['q2=yes, add auth'], _QUESTIONS) == {
            "q2": "yes, add auth"}

    def test_answer_both(self):
        parsed = parse_answer_options(["q1=postgres", "q2=no"], _QUESTIONS)
        assert parsed == {"q1": "postgres", "q2": "no"}

    def test_answer_may_contain_equals_signs(self):
        assert parse_answer_options(["q1=DSN=postgres://x"], _QUESTIONS) == {
            "q1": "DSN=postgres://x"}

    def test_unknown_id_rejected(self):
        with pytest.raises(AnswerParseError, match="unknown question id 'q9'"):
            parse_answer_options(["q9=whatever"], _QUESTIONS)

    def test_unknown_id_error_lists_open_questions(self):
        with pytest.raises(AnswerParseError, match="q1, q2"):
            parse_answer_options(["q9=whatever"], _QUESTIONS)

    def test_missing_equals_rejected(self):
        with pytest.raises(AnswerParseError, match="malformed"):
            parse_answer_options(["q1 postgres"], _QUESTIONS)

    def test_missing_id_rejected(self):
        with pytest.raises(AnswerParseError, match="missing question id"):
            parse_answer_options(["=postgres"], _QUESTIONS)

    def test_duplicate_id_rejected(self):
        with pytest.raises(AnswerParseError, match="duplicate --answer"):
            parse_answer_options(["q1=a", "q1=b"], _QUESTIONS)

    def test_answering_a_plan_without_questions_is_an_error(self):
        with pytest.raises(AnswerParseError, match="no open questions"):
            parse_answer_options(["q1=a"], [])


class TestResolveWithAnswers:

    def test_answer_persisted_as_human(self, tmp_path, monkeypatch):
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job(job)

        _cmd_decision_resolve(
            str(job.id)[:8], "fp:approval", reason="approve",
            answer=['q1=use PostgreSQL'])

        updated = load_job(job.id)
        recs = updated.flight_plan["clarifications_resolved"]
        assert updated.flight_plan["_approval"] == "approved"
        assert recs[0]["answer"] == "use PostgreSQL"
        assert recs[0]["answered_by"] == "human"

    def test_unknown_id_exits_non_zero(self, tmp_path, monkeypatch):
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job(job)

        with pytest.raises(SystemExit) as exc:
            _cmd_decision_resolve(
                str(job.id)[:8], "fp:approval", reason="approve",
                answer=["q9=nope"])
        assert exc.value.code == 1
        # The plan must be untouched by a rejected answer set.
        assert load_job(job.id).flight_plan["_approval"] == "pending"

    def test_answer_with_reject_is_an_error(self, tmp_path, monkeypatch):
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job(job)

        with pytest.raises(SystemExit) as exc:
            _cmd_decision_resolve(
                str(job.id)[:8], "fp:approval", reason="reject",
                answer=["q1=postgres"])
        assert exc.value.code == 1
        assert load_job(job.id).flight_plan["_approval"] == "pending"

    def test_answer_on_other_decision_is_an_error(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        with pytest.raises(SystemExit) as exc:
            _cmd_decision_resolve(
                "deadbeef", "sr:whatever", reason="x", answer=["q1=a"])
        assert exc.value.code == 1


class TestWriteBackAndImmutability:
    """T002 — approve writes answers AND defaults; then they are frozen."""

    def test_mixed_answer_and_default_persisted(self, tmp_path, monkeypatch, capsys):
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job(job)

        _cmd_decision_resolve(
            str(job.id)[:8], "fp:approval", reason="approve",
            answer=["q1=use PostgreSQL"])

        recs = load_job(job.id).flight_plan["clarifications_resolved"]
        assert [(r["id"], r["answer"], r["answered_by"]) for r in recs] == [
            ("q1", "use PostgreSQL", "human"),
            ("q2", "no, leave auth untouched", "default"),
        ]
        out = capsys.readouterr().out
        assert "q1 (human): use PostgreSQL" in out
        assert "q2 (default): no, leave auth untouched" in out

    def test_no_answers_records_all_defaults(self, tmp_path, monkeypatch):
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job(job)

        _cmd_decision_resolve(str(job.id)[:8], "fp:approval", reason="approve")

        recs = load_job(job.id).flight_plan["clarifications_resolved"]
        assert [r["answered_by"] for r in recs] == ["default", "default"]
        assert [r["answer"] for r in recs] == [
            "keep SQLite", "no, leave auth untouched"]

    def test_late_answer_rejected_as_already_resolved(
            self, tmp_path, monkeypatch, capsys):
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job(job)
        _cmd_decision_resolve(
            str(job.id)[:8], "fp:approval", reason="approve",
            answer=["q1=use PostgreSQL"])
        capsys.readouterr()

        with pytest.raises(SystemExit) as exc:
            _cmd_decision_resolve(
                str(job.id)[:8], "fp:approval", reason="approve",
                answer=["q1=actually MySQL"])
        assert exc.value.code == 1
        assert "already resolved" in capsys.readouterr().err

        recs = load_job(job.id).flight_plan["clarifications_resolved"]
        assert recs[0]["answer"] == "use PostgreSQL"

    def test_no_open_decision_after_approval(self, tmp_path, monkeypatch):
        from packages.orchestration.decision_queue import list_decisions
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job(job)

        _cmd_decision_resolve(str(job.id)[:8], "fp:approval", reason="approve")

        updated = load_job(job.id)
        open_fp = [d for d in list_decisions(updated, [])
                   if d.type == "flight_plan_approval" and d.status == "open"]
        assert open_fp == []

    def test_reject_leaves_clarifications_untouched(self, tmp_path, monkeypatch):
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        before = [dict(r) for r in job.flight_plan["clarifications_resolved"]]
        save_job(job)

        _cmd_decision_resolve(str(job.id)[:8], "fp:approval", reason="reject")

        updated = load_job(job.id)
        assert updated.flight_plan["_approval"] == "rejected"
        assert updated.flight_plan["clarifications_resolved"] == before

    def test_plan_without_questions_keeps_empty_list(self, tmp_path, monkeypatch):
        from packages.orchestration.storage import load_job, save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = Job(name="t", flight_plan={"_approval": "pending"})
        save_job(job)

        _cmd_decision_resolve(str(job.id)[:8], "fp:approval", reason="approve")

        fp = load_job(job.id).flight_plan
        assert fp["_approval"] == "approved"
        assert "clarifications_resolved" not in fp


class TestAnswerOptionIsRepeatable:

    def test_catalog_declares_repeatable_answer(self):
        from apps.cli.command_catalog import CATALOG

        entry = [c for c in CATALOG if c.command_id == "decision.resolve"][0]
        opt = [a for a in entry.args if a.name == "--answer"][0]
        assert opt.is_repeatable is True
        assert opt.is_flag is False

    def test_parser_collects_repeated_answers(self):
        from apps.cli.grouped import build_parser

        parser = build_parser()
        args = parser.parse_args([
            "decision", "resolve", "abc123", "fp:approval",
            "--reason", "approve", "--answer", "q1=a", "--answer", "q2=b",
        ])
        assert args.answer == ["q1=a", "q2=b"]

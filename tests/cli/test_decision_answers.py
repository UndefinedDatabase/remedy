"""F034 T001 — per-question answers on `remedy decision resolve`.

The bundled questions are answered on the ONE plan-approval decision:
`--answer q1="..."` is repeatable, answering a subset is valid, and an
unknown question id is a clean non-zero error.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from io import StringIO

import pytest

from apps.cli.commands.decision import (
    AnswerParseError,
    _cmd_decision_resolve,
    parse_answer_options,
)
from apps.cli.grouped import main
from packages.orchestration.job_plan import carry_intake_clarifications
from packages.orchestration.pingpong_job import JobPlan
from packages.orchestration.schemas.models import TaskPlan

_QUESTIONS = [
    {"id": "q1", "question": "Which database?",
     "default_answer": "keep SQLite", "impact": "driver choice"},
    {"id": "q2", "question": "Add auth?",
     "default_answer": "no, leave auth untouched", "impact": "scope"},
]


def _pending_job() -> JobPlan:
    plan = carry_intake_clarifications(
        TaskPlan(**{
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
    return JobPlan(job_title="t", flight_plan=fp)


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
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)

        _cmd_decision_resolve(
            str(job.job_id)[:8], "fp:approval", reason="approve",
            answer=['q1=use PostgreSQL'])

        updated = load_job_plan(job.job_id)
        recs = updated.flight_plan["clarifications_resolved"]
        assert updated.flight_plan["_approval"] == "approved"
        assert recs[0]["answer"] == "use PostgreSQL"
        assert recs[0]["answered_by"] == "human"

    def test_unknown_id_exits_non_zero(self, tmp_path, monkeypatch):
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)

        with pytest.raises(SystemExit) as exc:
            _cmd_decision_resolve(
                str(job.job_id)[:8], "fp:approval", reason="approve",
                answer=["q9=nope"])
        assert exc.value.code == 1
        # The plan must be untouched by a rejected answer set.
        assert load_job_plan(job.job_id).flight_plan["_approval"] == "pending"

    def test_answer_with_reject_is_an_error(self, tmp_path, monkeypatch):
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)

        with pytest.raises(SystemExit) as exc:
            _cmd_decision_resolve(
                str(job.job_id)[:8], "fp:approval", reason="reject",
                answer=["q1=postgres"])
        assert exc.value.code == 1
        assert load_job_plan(job.job_id).flight_plan["_approval"] == "pending"

    def test_answer_on_other_decision_is_an_error(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        with pytest.raises(SystemExit) as exc:
            _cmd_decision_resolve(
                "deadbeef", "sr:whatever", reason="x", answer=["q1=a"])
        assert exc.value.code == 1


class TestWriteBackAndImmutability:
    """T002 — approve writes answers AND defaults; then they are frozen."""

    def test_mixed_answer_and_default_persisted(self, tmp_path, monkeypatch, capsys):
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)

        _cmd_decision_resolve(
            str(job.job_id)[:8], "fp:approval", reason="approve",
            answer=["q1=use PostgreSQL"])

        recs = load_job_plan(job.job_id).flight_plan["clarifications_resolved"]
        assert [(r["id"], r["answer"], r["answered_by"]) for r in recs] == [
            ("q1", "use PostgreSQL", "human"),
            ("q2", "no, leave auth untouched", "default"),
        ]
        out = capsys.readouterr().out
        assert "q1 (human): use PostgreSQL" in out
        assert "q2 (default): no, leave auth untouched" in out

    def test_no_answers_records_all_defaults(self, tmp_path, monkeypatch):
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)

        _cmd_decision_resolve(str(job.job_id)[:8], "fp:approval", reason="approve")

        recs = load_job_plan(job.job_id).flight_plan["clarifications_resolved"]
        assert [r["answered_by"] for r in recs] == ["default", "default"]
        assert [r["answer"] for r in recs] == [
            "keep SQLite", "no, leave auth untouched"]

    def test_late_answer_rejected_as_already_resolved(
            self, tmp_path, monkeypatch, capsys):
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)
        _cmd_decision_resolve(
            str(job.job_id)[:8], "fp:approval", reason="approve",
            answer=["q1=use PostgreSQL"])
        capsys.readouterr()

        with pytest.raises(SystemExit) as exc:
            _cmd_decision_resolve(
                str(job.job_id)[:8], "fp:approval", reason="approve",
                answer=["q1=actually MySQL"])
        assert exc.value.code == 1
        assert "already resolved" in capsys.readouterr().err

        recs = load_job_plan(job.job_id).flight_plan["clarifications_resolved"]
        assert recs[0]["answer"] == "use PostgreSQL"

    def test_no_open_decision_after_approval(self, tmp_path, monkeypatch):
        from packages.orchestration.decision_queue import list_decisions
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)

        _cmd_decision_resolve(str(job.job_id)[:8], "fp:approval", reason="approve")

        updated = load_job_plan(job.job_id)
        open_fp = [d for d in list_decisions(updated, [])
                   if d.type == "flight_plan_approval" and d.status == "open"]
        assert open_fp == []

    def test_reject_leaves_clarifications_untouched(self, tmp_path, monkeypatch):
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        before = [dict(r) for r in job.flight_plan["clarifications_resolved"]]
        save_job_plan(job)

        _cmd_decision_resolve(str(job.job_id)[:8], "fp:approval", reason="reject")

        updated = load_job_plan(job.job_id)
        assert updated.flight_plan["_approval"] == "rejected"
        assert updated.flight_plan["clarifications_resolved"] == before

    def test_plan_without_questions_keeps_empty_list(self, tmp_path, monkeypatch):
        from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = JobPlan(job_title="t", flight_plan={"_approval": "pending"})
        save_job_plan(job)

        _cmd_decision_resolve(str(job.job_id)[:8], "fp:approval", reason="approve")

        fp = load_job_plan(job.job_id).flight_plan
        assert fp["_approval"] == "approved"
        assert "clarifications_resolved" not in fp


def _show_assumptions(capsys, job_id: str):
    """`job show <id> --full`: the assumptions section's envelope, and its text on stderr."""
    main(["job", "show", job_id, "--full"])
    shown = capsys.readouterr()
    text = shown.err.split("--- Assumptions ---\n", 1)[1].split("\n\n--- ", 1)[0]
    return json.loads(shown.out)["sections"]["assumptions"], text


class TestAssumptionsCommand:
    """T003 — the assumption log and its evidence copy, since F261 the ``assumptions``
    section of `remedy job show <id> --full`."""

    def test_approval_writes_the_evidence_log(self, tmp_path, monkeypatch, capsys):
        from packages.orchestration.data_paths import job_evidence_export_dir
        from packages.orchestration.pingpong_job import save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)

        _cmd_decision_resolve(
            str(job.job_id)[:8], "fp:approval", reason="approve",
            answer=["q1=use PostgreSQL"])
        assert "Assumption log:" in capsys.readouterr().out

        log = (job_evidence_export_dir(str(job.job_id)) / "assumptions.md").read_text()
        assert "| q1 | Which database? | use PostgreSQL | human |" in log
        assert "| q2 | Add auth? | no, leave auth untouched | default |" in log
        assert "Sources: 1 human, 1 default, 0 planner, 0 unresolved." in log

    def test_the_section_holds_the_log(self, tmp_path, monkeypatch, capsys):
        from packages.orchestration.data_paths import job_evidence_export_dir
        from packages.orchestration.pingpong_job import save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _pending_job()
        save_job_plan(job)
        _cmd_decision_resolve(str(job.job_id)[:8], "fp:approval", reason="approve")
        capsys.readouterr()

        section, text = _show_assumptions(capsys, str(job.job_id)[:8])

        log_path = job_evidence_export_dir(str(job.job_id)) / "assumptions.md"
        assert section["ok"] is True
        assert "# Assumptions" in section["data"]["markdown"]
        assert "| q1 | Which database? | keep SQLite | default |" in section["data"]["markdown"]
        assert section["data"]["evidence_copy"] == str(log_path)
        assert "# Assumptions" in text
        assert "| q1 | Which database? | keep SQLite | default |" in text
        assert f"Evidence copy: {log_path}" in text

    def test_the_section_on_a_job_without_a_plan(self, tmp_path, monkeypatch, capsys):
        from packages.orchestration.data_paths import job_evidence_export_dir
        from packages.orchestration.pingpong_job import save_job_plan
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = JobPlan(job_title="t")
        save_job_plan(job)

        section, text = _show_assumptions(capsys, str(job.job_id)[:8])

        assert "No clarifications" in section["data"]["markdown"]
        assert "No clarifications" in text
        # A read view writes nothing: no evidence copy is reported, and none appears.
        assert section["data"]["evidence_copy"] is None
        assert "Evidence copy:" not in text
        assert not (job_evidence_export_dir(str(job.job_id)) / "assumptions.md").exists()

    def test_an_unknown_job_exits_non_zero(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        with pytest.raises(SystemExit) as exc:
            main(["job", "show", "deadbeef", "--full"])
        assert exc.value.code == 1

    def test_the_view_is_a_section_of_a_read_only_command(self):
        from apps.cli.command_catalog import get_command
        from apps.cli.commands.job import _SHOW_SECTIONS

        assert "assumptions" in [name for name, _builder in _SHOW_SECTIONS]
        assert get_command("job.show").action_class == "read_only"


def _git_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return repo


_INTAKE_WITH_ONE_CLARIFICATION = json.dumps({
    "schema_v": "ji1",
    "goal": "Test goal.",
    "context_refs": [],
    "constraints": [],
    "acceptance_hints": [],
    "truncated_input": False,
    "clarifications": [{
        "question": "Drop the legacy table?",
        "default_answer": "keep the legacy table untouched",
        "impact": "data retained; migration deferred",
    }],
})


class TestUnattendedEndToEnd:
    """T004 — `remedy do --yes` runs the whole plan gate without a human."""

    def _run_unattended(self, tmp_path, monkeypatch):
        from packages.orchestration.job_plan import (
            TaskPlanResult,
            carry_intake_clarifications,
        )

        repo = _git_repo(tmp_path)
        env = {**os.environ, "PYTHONPATH": os.getcwd(),
               "REMEDY_DATA_DIR": str(tmp_path / "data")}
        subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "init"],
            capture_output=True, text=True, timeout=60,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.setattr(
            "packages.orchestration.intake.make_provider_call_fn",
            lambda: (lambda prompt, attempt: _INTAKE_WITH_ONE_CLARIFICATION),
        )
        # The flight-plan factory too, not only `plan_job_llm` behind it: the real
        # one probes a live Ollama server, so without this the branch under test
        # is selected by whether a server happens to run on the machine, and a
        # runner without one lands on the deterministic skeleton instead.
        monkeypatch.setattr(
            "packages.orchestration.intake.make_structured_call_fn",
            lambda model_cls, **kw: (lambda prompt, attempt: "{}"),
        )

        base_plan = TaskPlan(**{
            "schema_v": "flight_plan_v1",
            "tasks": [{
                "id": "T001", "title": "Do thing", "goal": "A goal",
                "acceptance": ["Done"], "depends_on": [],
                "est_tokens_band": "M", "files_hint": [],
            }],
        })
        monkeypatch.setattr(
            "packages.orchestration.job_plan.plan_job_llm",
            lambda intake, call_fn, **kw: TaskPlanResult(
                plan=carry_intake_clarifications(base_plan, intake),
                source="llm", calls=1),
        )
        monkeypatch.chdir(str(repo))

        captured = StringIO()
        monkeypatch.setattr("sys.stdout", captured)
        from apps.cli.commands.do_cmd import _cmd_do_mission
        _cmd_do_mission("test mission", repo=str(repo), json_output=True, yes=True)
        return json.loads(captured.getvalue())

    def test_default_recorded_and_logged_without_a_human(
            self, tmp_path, monkeypatch):
        from packages.orchestration.data_paths import job_evidence_export_dir
        from packages.orchestration.decision_queue import list_decisions
        from packages.orchestration.pingpong_job import load_job_plan

        data = self._run_unattended(tmp_path, monkeypatch)
        assert "approved via --yes" in data["plan_label"]

        job = load_job_plan(data["job_id"])
        recs = job.flight_plan["clarifications_resolved"]
        assert [(r["id"], r["answer"], r["answered_by"]) for r in recs] == [
            ("q1", "keep the legacy table untouched", "default")]

        log = (job_evidence_export_dir(str(job.job_id)) / "assumptions.md").read_text()
        assert ("| q1 | Drop the legacy table? | keep the legacy table "
                "untouched | default |") in log

        open_fp = [d for d in list_decisions(job, [])
                   if d.type == "flight_plan_approval" and d.status == "open"]
        assert open_fp == []

    def test_exits_zero(self, tmp_path, monkeypatch):
        """_cmd_do_mission returning normally is exit 0 for the CLI."""
        self._run_unattended(tmp_path, monkeypatch)


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

"""Tests for the decision group CLI handler (F262 T002)."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from packages.orchestration.decision_queue import HumanDecision

_LOAD_JOB_EVENTS = "apps.cli.commands.decision._load_job_events"
_LIST_DECISIONS = "packages.orchestration.decision_queue.list_decisions"
_GET_DECISION = "packages.orchestration.decision_queue.get_decision"


def _decision(*, status="open", resolved_at=None):
    return HumanDecision(
        id="dec-1",
        type="task_decision",
        status=status,
        severity="blocker",
        source="test",
        related_node_id="",
        related_intent_id="",
        related_file="",
        safe_summary="a decision",
        next_actions=(),
        created_at="2026-09-01T00:00:00+00:00",
        resolved_at=resolved_at,
    )


class TestDecisionListText:
    @patch(_LIST_DECISIONS)
    @patch(_LOAD_JOB_EVENTS)
    def test_shows_created(self, mock_load, mock_list, capsys):
        mock_load.return_value = (None, [], "job-1")
        mock_list.return_value = [_decision()]
        from apps.cli.commands.decision import _cmd_decision_list
        _cmd_decision_list("job-1", json_output=False)
        out = capsys.readouterr().out
        assert "created=2026-09-01T00:00:00+00:00" in out
        assert "resolved=" not in out

    @patch(_LIST_DECISIONS)
    @patch(_LOAD_JOB_EVENTS)
    def test_shows_resolved_when_present(self, mock_load, mock_list, capsys):
        mock_load.return_value = (None, [], "job-1")
        mock_list.return_value = [
            _decision(status="resolved", resolved_at="2026-09-02T00:00:00+00:00"),
        ]
        from apps.cli.commands.decision import _cmd_decision_list
        _cmd_decision_list("job-1", json_output=False)
        out = capsys.readouterr().out
        assert "created=2026-09-01T00:00:00+00:00" in out
        assert "resolved=2026-09-02T00:00:00+00:00" in out


class TestDecisionListOptions:
    @patch(_LIST_DECISIONS)
    @patch(_LOAD_JOB_EVENTS)
    def test_limit_caps_returned_decisions(self, mock_load, mock_list, capsys):
        mock_load.return_value = (None, [], "job-1")
        mock_list.return_value = [_decision(), _decision(), _decision()]
        from apps.cli.commands.decision import _cmd_decision_list
        _cmd_decision_list("job-1", json_output=True, limit="2")
        import json
        out = capsys.readouterr().out
        data = json.loads(out)
        assert len(data["decisions"]) == 2

    @patch(_LIST_DECISIONS)
    @patch(_LOAD_JOB_EVENTS)
    def test_unknown_sort_field_exits_nonzero(self, mock_load, mock_list, capsys):
        mock_load.return_value = (None, [], "job-1")
        mock_list.return_value = [_decision()]
        from apps.cli.commands.decision import _cmd_decision_list
        with pytest.raises(SystemExit) as exc:
            _cmd_decision_list("job-1", json_output=True, sort="bogus")
        assert exc.value.code == 1


class TestDecisionRefusalsAnswerInTheEnvelope:
    """F283 round 6 — `decision.py`'s refusals moved onto `fail()`; these prove two of
    them answer a machine under `--json` rather than printing prose above the exit."""

    @patch(_GET_DECISION)
    @patch(_LOAD_JOB_EVENTS)
    def test_an_unknown_decision_id_answers_in_the_envelope(self, mock_load, mock_get, capsys):
        mock_load.return_value = (None, [], "job-1")
        mock_get.return_value = None
        from apps.cli.commands.decision import _cmd_decision_show
        with pytest.raises(SystemExit) as exc:
            _cmd_decision_show("job-1", "no-such-decision", json_output=True)
        assert exc.value.code == 1
        out, err = capsys.readouterr()
        assert err == ""
        body = json.loads(out)
        assert body["ok"] is False
        assert body["error"] == "decision_not_found"

    @patch(_LIST_DECISIONS)
    @patch(_LOAD_JOB_EVENTS)
    def test_an_invalid_list_option_answers_in_the_envelope(self, mock_load, mock_list, capsys):
        mock_load.return_value = (None, [], "job-1")
        mock_list.return_value = [_decision()]
        from apps.cli.commands.decision import _cmd_decision_list
        with pytest.raises(SystemExit) as exc:
            _cmd_decision_list("job-1", json_output=True, sort="bogus")
        assert exc.value.code == 1
        out, err = capsys.readouterr()
        assert err == ""
        body = json.loads(out)
        assert body["ok"] is False
        assert body["error"] == "invalid_list_option"


class TestDecisionExplainAndResolveAnswerJSONThroughTheDispatcher:
    """F283 R15 C4 (DECISION F283 D9) — `decision explain` and `decision resolve`
    now declare `--json` in the catalog; each shape proved end to end through
    the CLI dispatcher."""

    @patch("packages.orchestration.decision_queue.explain_decisions")
    @patch(_LOAD_JOB_EVENTS)
    def test_explain_answers_the_envelope(self, mock_load, mock_explain, capsys):
        from apps.cli.grouped import main

        mock_load.return_value = (None, [], "job-1")
        mock_explain.return_value = "No pending decisions."

        main(["decision", "explain", "job-1", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["job_id"] == "job-1"
        assert body["text"] == "No pending decisions."

    def test_resolve_sr_answers_the_envelope(self, capsys):
        from apps.cli.grouped import main
        from packages.orchestration.stop_reasons import StopReason

        resolved = StopReason(
            id="stop-1", job_id="job-1", source="test", reason_code="test_failed",
            severity="warning", status="resolved", created_at="2026-09-01T00:00:00+00:00",
            resolved_at="2026-09-02T00:00:00+00:00", related_node_id="",
            related_intent_id="", related_file="", safe_summary="a blocker",
            next_actions=(),
        )
        with patch("packages.orchestration.stop_reasons.resolve_stop_reason",
                   return_value=resolved):
            main(["decision", "resolve", "job-1", "sr:stop-1", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["decision_id"] == "sr:stop-1" and body["job_id"] == "job-1"
        assert body["outcome"] == "resolved"
        assert body["stop_id"] == "stop-1" and body["reason_code"] == "test_failed"

    def test_resolve_a_missing_task_decision_is_the_envelope(self, capsys):
        from apps.cli.grouped import main

        with patch("apps.cli.commands.decision.resolve_job_id_or_fail",
                   return_value="job-1"), \
             patch("packages.orchestration.pingpong_job.require_job_plan",
                   return_value=object()), \
             patch("packages.orchestration.escalation.find_task_decision",
                   return_value=None), \
             pytest.raises(SystemExit) as exc:
            main(["decision", "resolve", "job-1", "td:no-such", "--json"])
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is False
        assert body["error"] == "decision_not_found"

    def test_resolve_a_derived_decision_is_not_resolvable_in_the_envelope(self, capsys):
        from apps.cli.grouped import main

        with pytest.raises(SystemExit) as exc:
            main(["decision", "resolve", "job-1", "bogus:xyz", "--json"])
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.err == ""
        body = json.loads(captured.out)
        assert body["ok"] is False
        assert body["error"] == "decision_not_resolvable"
        assert "bogus:xyz" in body["message"]
        assert "Resolve the underlying record" in body["message"]

    def test_resolve_a_derived_decision_without_json_writes_its_two_old_stderr_lines(
        self, capsys,
    ):
        """F283 R16 C3 — the text branch is untouched by C3's `next_command`
        narrowing: `decision resolve` on a derived decision without `--json`
        still writes exactly its two old stderr lines and exits 1."""
        from apps.cli.grouped import main

        with pytest.raises(SystemExit) as exc:
            main(["decision", "resolve", "job-1", "bogus:xyz"])
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == (
            "Decision 'bogus:xyz' is derived and cannot be directly resolved.\n"
            "Resolve the underlying record (patch intent, test, etc.) instead.\n"
        )


class TestDecisionListAnswersJSONThroughTheDispatcher:
    """F283 R18 C3 (R-1031) — `decision list`'s success document, through the
    real argv dispatcher (`apps.cli.grouped.main`), carries the envelope
    `emit_ok` added at F283 R17 C5 (`dbc49b6b`)."""

    @patch(_LIST_DECISIONS)
    @patch(_LOAD_JOB_EVENTS)
    def test_list_answers_the_envelope(self, mock_load, mock_list, capsys):
        from apps.cli.grouped import main

        mock_load.return_value = (None, [], "job-1")
        mock_list.return_value = [_decision()]
        main(["decision", "list", "job-1", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["job_id"] == "job-1"


class TestDecisionResolveProposalAnswersJSONThroughTheDispatcher:
    """F283 R15 C4 (DECISION F283 D9) — `decision resolve proposal:<id>` proved
    end to end through the CLI dispatcher, over a real proposed-task store, the
    same recipe `tests/orchestration/test_proposal_decision.py` uses."""

    _JOB_ID = "12345678-1234-5678-1234-567812345678"

    @pytest.fixture
    def store(self, monkeypatch, tmp_path):
        monkeypatch.setattr(
            "packages.orchestration.proposed_tasks._STORE_DIR",
            tmp_path / "proposed_tasks",
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job_dir = tmp_path / "jobs" / self._JOB_ID
        job_dir.mkdir(parents=True, exist_ok=True)
        (job_dir / "job.json").write_text(json.dumps({
            "job_id": self._JOB_ID, "job_title": "test-job",
            "created_at": "2026-09-01T00:00:00Z", "tasks": [], "status": "pending",
            "artifacts": [], "budget": {"max_steps": 10, "max_tokens": 0, "max_cost_usd": 0.0},
            "metadata": {},
        }))
        return tmp_path

    def test_reject_answers_the_envelope(self, store, capsys):
        from apps.cli.grouped import main
        from packages.orchestration.proposed_tasks import ProposedTask, ProposedTaskStatus, add_proposed_task

        t = ProposedTask(title="Unresolved task", status=ProposedTaskStatus.PROPOSED)
        add_proposed_task(self._JOB_ID, t, root=store)

        main(["decision", "resolve", self._JOB_ID, f"proposal:{t.id}",
              "--reason", "reject", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["decision_id"] == f"proposal:{t.id}" and body["job_id"] == self._JOB_ID
        assert body["outcome"] == "rejected"
        assert body["task_id"] == t.id


class TestDecisionResolveVetoAnswersJSONThroughTheDispatcher:
    """F027 R4 — `decision resolve veto:<request id>` proved end to end through the CLI
    dispatcher, over a real vetoed job (DECISION F027 D4 (6))."""

    @pytest.fixture
    def vetoed_job(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration import task_veto as tv
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

        tasks = [TaskEntry(title="A"), TaskEntry(title="B")]
        job = JobPlan(job_title="veto-cli-job", tasks=tasks, repo_path=str(tmp_path))
        save_job_plan(job, tmp_path)
        result = tv.veto_task_command(job, task_id=tasks[0].task_id,
                                      reason="known-bad approach", actor="alice")
        assert result["outcome"] == "vetoed"
        return job, result["request_id"]

    def test_an_accept_answers_the_envelope(self, vetoed_job, capsys):
        from apps.cli.grouped import main

        job, request_id = vetoed_job
        decision_id = f"veto:{request_id}"
        main(["decision", "resolve", str(job.job_id), decision_id,
              "--reason", "accept_reduced_scope", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["decision_id"] == decision_id and body["job_id"] == str(job.job_id)
        assert body["outcome"] == "answered"
        assert body["option"] == "accept_reduced_scope"
        assert body["follow_up_job_id"] == ""

    def test_an_accept_names_job_run_not_job_resume(self, vetoed_job, capsys):
        """R-1067 — the accept's sentence sends the operator to `remedy job run`, the
        job's id as typed, since only `run` reaches the settled completion; `resume`
        hands a vetoed job to the cycle executor, which never completes it."""
        from apps.cli.grouped import main

        job, request_id = vetoed_job
        decision_id = f"veto:{request_id}"
        main(["decision", "resolve", str(job.job_id), decision_id,
              "--reason", "accept_reduced_scope"])
        out = capsys.readouterr().out
        assert f"remedy job run {job.job_id}" in out
        assert "remedy job resume" not in out

    def test_a_replan_prints_the_follow_up_jobs_id(self, vetoed_job, capsys):
        from apps.cli.grouped import main

        job, request_id = vetoed_job
        decision_id = f"veto:{request_id}"
        main(["decision", "resolve", str(job.job_id), decision_id,
              "--reason", "replan_follow_up", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True
        assert body["outcome"] == "answered"
        assert body["option"] == "replan_follow_up"
        assert body["follow_up_job_id"]

    def test_a_refusals_exit_code_matches_the_proposal_routes_own(self, vetoed_job, capsys):
        from apps.cli.grouped import main

        job, request_id = vetoed_job
        decision_id = f"veto:{request_id}"
        with pytest.raises(SystemExit) as exc:
            main(["decision", "resolve", str(job.job_id), decision_id,
                  "--reason", "bogus_option", "--json"])
        # `invalid_argument` is the SAME code, and the SAME default `fail()` exit code
        # of 1, the `proposal:` route gives its own `--reason` refusal.
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is False
        assert body["error"] == "invalid_argument"


class TestTheTokenVocabularyJoinsTheProduct:
    """R-1023, DECISION F277 D8 part (a) — one token per condition, repo-wide,
    existing spelling wins. Round 6 minted `job_has_no_project` and
    `invalid_reason`, forking spellings the product already had elsewhere in
    `apps/cli/`: `no_project` (`job.py`, `mission_cmd.py`) and
    `invalid_argument` (`job.py`, `mission_cmd.py`). This pins the SET of
    tokens `decision.py` passes to `fail()`, read off the AST, so a rename
    reds."""

    _PINNED_TOKENS = frozenset({
        "answer_parse_error", "clarifications_already_resolved",
        "decision_already_answered", "decision_not_found",
        "decision_not_resolvable",
        "follow_up_mission_error", "invalid_argument", "invalid_list_option",
        "job_not_found", "missing_argument", "mission_already_linked",
        "mission_error", "no_pending_plan_approval", "no_project",
        "option_not_applicable", "proposed_task_invalid_state",
        "proposed_task_not_found", "proposed_task_operation_failed",
        "stop_reason_not_found",
    })

    def test_the_fail_call_tokens_match_the_pin(self):
        import ast
        import pathlib

        path = (
            pathlib.Path(__file__).resolve().parents[2]
            / "apps" / "cli" / "commands" / "decision.py"
        )
        tree = ast.parse(path.read_text())
        tokens = {
            node.args[0].value
            for node in ast.walk(tree)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "fail"
                and node.args
                and isinstance(node.args[0], ast.Constant)
            )
        }
        assert tokens == self._PINNED_TOKENS, (
            f"decision.py's fail() token vocabulary changed: {tokens ^ self._PINNED_TOKENS}"
        )

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

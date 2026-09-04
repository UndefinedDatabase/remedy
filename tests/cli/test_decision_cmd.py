"""Tests for the decision group CLI handler (F262 T002)."""

from __future__ import annotations

from unittest.mock import patch

from packages.orchestration.decision_queue import HumanDecision

_LOAD_JOB_EVENTS = "apps.cli.commands.decision._load_job_events"
_LIST_DECISIONS = "packages.orchestration.decision_queue.list_decisions"


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

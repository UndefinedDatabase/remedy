"""Tests for the blocker group CLI handler (F262 T002)."""

from __future__ import annotations

from unittest.mock import patch

from packages.orchestration.stop_reasons import StopReason

_LIST_STOPS = "packages.orchestration.stop_reasons.list_stop_reasons"


def _stop(*, status="active", resolved_at=None):
    return StopReason(
        id="stop-1",
        job_id="job-1",
        source="test",
        reason_code="dirty_repo",
        severity="warning",
        status=status,
        created_at="2026-09-01T00:00:00+00:00",
        resolved_at=resolved_at,
        related_node_id="",
        related_intent_id="",
        related_file="",
        safe_summary="a blocker",
        next_actions=(),
    )


class TestBlockerListText:
    @patch(_LIST_STOPS)
    def test_shows_created(self, mock_list, capsys):
        mock_list.return_value = [_stop()]
        from apps.cli.commands.blocker import _cmd_blocker_list
        _cmd_blocker_list("job-1", json_output=False)
        out = capsys.readouterr().out
        assert "created=2026-09-01T00:00:00+00:00" in out
        assert "resolved=" not in out

    @patch(_LIST_STOPS)
    def test_shows_resolved_when_present(self, mock_list, capsys):
        mock_list.return_value = [
            _stop(status="resolved", resolved_at="2026-09-02T00:00:00+00:00"),
        ]
        from apps.cli.commands.blocker import _cmd_blocker_list
        _cmd_blocker_list("job-1", json_output=False)
        out = capsys.readouterr().out
        assert "created=2026-09-01T00:00:00+00:00" in out
        assert "resolved=2026-09-02T00:00:00+00:00" in out

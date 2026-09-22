"""Tests for the blocker group CLI handler (F262 T002)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from packages.orchestration.stop_reasons import StopReason

_LIST_STOPS = "packages.orchestration.stop_reasons.list_stop_reasons"


def _stop(*, status="active", resolved_at=None):
    return StopReason(
        id="stop-1",
        job_id="job-1",
        source="test",
        reason_code="test_failed",
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


class TestBlockerListOptions:
    @patch(_LIST_STOPS)
    def test_limit_caps_returned_blockers(self, mock_list, capsys):
        mock_list.return_value = [_stop(), _stop(), _stop()]
        from apps.cli.commands.blocker import _cmd_blocker_list
        _cmd_blocker_list("job-1", json_output=True, limit="2")
        import json
        out = capsys.readouterr().out
        data = json.loads(out)
        assert len(data["stop_reasons"]) == 2

    @patch(_LIST_STOPS)
    def test_unknown_sort_field_exits_nonzero(self, mock_list, capsys):
        mock_list.return_value = [_stop()]
        from apps.cli.commands.blocker import _cmd_blocker_list
        with pytest.raises(SystemExit) as exc:
            _cmd_blocker_list("job-1", json_output=True, sort="bogus")
        assert exc.value.code == 1


class TestABlockerRefusalIsShapedLikeTheCaller:
    """F277 T003 — the `blocker` group migrated onto the shared `fail()`."""

    def test_a_missing_blocker_is_an_envelope_under_json(self, capsys):
        import json

        from apps.cli.commands.blocker import _cmd_blocker_show

        with patch("packages.orchestration.stop_reasons.get_stop_reason",
                   return_value=None), pytest.raises(SystemExit) as exc:
            _cmd_blocker_show("job-1", "no-such-blocker", json_output=True)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.err == ""
        body = json.loads(captured.out)
        assert body["ok"] is False and body["schema_version"] == 1
        assert body["error"] == "blocker_not_found"

    def test_without_json_it_is_the_line_it_always_was(self, capsys):
        from apps.cli.commands.blocker import _cmd_blocker_show

        with patch("packages.orchestration.stop_reasons.get_stop_reason",
                   return_value=None), pytest.raises(SystemExit) as exc:
            _cmd_blocker_show("job-1", "no-such-blocker", json_output=False)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Error: blocker not found: no-such-blocker\n"

    def test_resolve_now_threads_the_flag_it_never_had(self, capsys):
        """`blocker resolve` carries no `--json` in the catalog yet; the handler is ready."""
        import json

        from apps.cli.commands.blocker import _cmd_blocker_resolve

        with patch("packages.orchestration.stop_reasons.resolve_stop_reason",
                   return_value=None), pytest.raises(SystemExit) as exc:
            _cmd_blocker_resolve("job-1", "no-such-blocker", json_output=True)
        assert exc.value.code == 1
        assert json.loads(capsys.readouterr().out)["error"] == "blocker_not_found"


class TestBlockerResolveAnswersJSONThroughTheDispatcher:
    """F283 R14 C5 (DECISION F283 D9) — `blocker resolve` now declares `--json` in
    the catalog; both shapes proved end to end through the CLI dispatcher."""

    def test_resolve_answers_the_envelope(self, capsys):
        import json

        from apps.cli.grouped import main

        resolved = _stop(status="resolved")
        with patch("packages.orchestration.stop_reasons.resolve_stop_reason",
                   return_value=resolved):
            main(["blocker", "resolve", "job-1", "stop-1", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["id"] == "stop-1" and body["reason_code"] == "test_failed"

    def test_a_missing_blocker_is_the_envelope_through_the_dispatcher(self, capsys):
        import json

        from apps.cli.grouped import main

        with patch("packages.orchestration.stop_reasons.resolve_stop_reason",
                   return_value=None), pytest.raises(SystemExit) as exc:
            main(["blocker", "resolve", "job-1", "no-such-blocker", "--json"])
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is False
        assert body["error"] == "blocker_not_found"

    def test_resolve_answers_the_full_id_not_the_text_branchs_short_one(self, capsys):
        """F283 R15 C3 — the text branch prints `sr.id[:8]`; the envelope must not
        inherit that truncation. `stop-1` (six characters) never exercised this:
        pin it with a stop id longer than eight characters."""
        import json

        from apps.cli.grouped import main

        long_id = "stop-reason-0123456789"
        resolved = _stop(status="resolved")
        resolved.id = long_id
        with patch("packages.orchestration.stop_reasons.resolve_stop_reason",
                   return_value=resolved):
            main(["blocker", "resolve", "job-1", long_id, "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["id"] == long_id
        assert len(body["id"]) > 8

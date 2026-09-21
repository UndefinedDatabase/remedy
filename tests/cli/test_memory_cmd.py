"""F277 T003 — the `memory` group's refusals, in both shapes.

Six of this group's nine refusal sites say "memory card not found" and five of
them are byte-identical, which is why the group is migrated in one commit: the
same condition now carries the same token, `memory_card_not_found`, wherever a
card lookup comes back empty.

Five of the six card commands carry no `--json` argument in the catalog yet —
they are in the read-only-without-`supports_json` set T003 empties at the end of
the slice — so their handlers are threaded and proved here at the handler, which
is where the flag will arrive once the catalog declares it.
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from apps.cli.commands.memory import (
    _cmd_memory_card_approve,
    _cmd_memory_card_contradict,
    _cmd_memory_card_reject,
    _cmd_memory_card_show,
    _cmd_memory_card_stale,
    _cmd_memory_card_supersede,
    _cmd_memory_learn,
)

_GATEWAY = "packages.memory.local_gateway."

#: (handler, gateway function it calls, the value that means "no such card").
_CARD_COMMANDS = [
    (_cmd_memory_card_show, "get_memory_card", None),
    (_cmd_memory_card_approve, "approve_memory_card", None),
    (_cmd_memory_card_reject, "reject_memory_card", None),
    (_cmd_memory_card_stale, "mark_stale", None),
]


class TestEveryCardLookupRefusesUnderOneToken:
    @pytest.mark.parametrize(("handler", "gateway", "empty"), _CARD_COMMANDS)
    def test_under_json_it_is_an_envelope_on_stdout(self, capsys, handler, gateway, empty):
        with patch(_GATEWAY + gateway, return_value=empty), \
             pytest.raises(SystemExit) as exc:
            handler("no-such-card", json_output=True)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.err == ""
        body = json.loads(captured.out)
        assert body["ok"] is False and body["schema_version"] == 1
        assert body["error"] == "memory_card_not_found"
        assert "no-such-card" in body["message"]

    @pytest.mark.parametrize(("handler", "gateway", "empty"), _CARD_COMMANDS)
    def test_without_json_it_is_the_line_it_always_was(self, capsys, handler, gateway, empty):
        with patch(_GATEWAY + gateway, return_value=empty), \
             pytest.raises(SystemExit) as exc:
            handler("no-such-card", json_output=False)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Error: memory card not found: no-such-card\n"

    def test_supersede_names_the_OLD_card_and_keeps_its_own_wording(self, capsys):
        """The one card refusal whose sentence differs — it says which id was missing."""
        with patch(_GATEWAY + "supersede_memory_card", return_value=(None, None)), \
             pytest.raises(SystemExit) as exc:
            _cmd_memory_card_supersede("old-id", "new-id", json_output=True)
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["error"] == "memory_card_not_found"
        assert body["message"] == "old memory card not found: old-id"

    def test_contradict_threads_the_flag_through_its_two_ids(self, capsys):
        with patch(_GATEWAY + "contradict_memory_card", return_value=(None, None)), \
             pytest.raises(SystemExit) as exc:
            _cmd_memory_card_contradict("no-such-card", "by-id", json_output=True)
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["error"] == "memory_card_not_found"
        assert "no-such-card" in body["message"]


class TestTheJobLookupInLearnRefusesTheSameWayEveryGroupDoes:
    def test_an_unknown_job_is_an_envelope_under_json(self, capsys):
        with pytest.raises(SystemExit) as exc:
            _cmd_memory_learn("not-a-job-id", json_output=True)
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is False
        assert body["error"] == "invalid_job_id"

    def test_without_json_it_is_the_line_it_always_was(self, capsys):
        with pytest.raises(SystemExit) as exc:
            _cmd_memory_learn("not-a-job-id", json_output=False)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err.startswith("Error: No job matches 'not-a-job-id'.")


class TestTheCatalogStillDeclaresWhatItDeclared:
    def test_the_five_card_mutations_are_still_the_json_gap_this_slice_closes_later(self):
        """A guard on the premise of this module's docstring, not on the migration.

        If one of these five gains `supports_json` before T003's catalog half
        lands, the sentence above stops being true and this test says so.
        """
        from apps.cli.command_catalog import get_command

        gap = ["memory.card-approve", "memory.card-reject", "memory.card-stale",
               "memory.card-supersede", "memory.card-contradict"]
        assert [get_command(c).supports_json for c in gap] == [False] * 5
        assert get_command("memory.card-show").supports_json is True

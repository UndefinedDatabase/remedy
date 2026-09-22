"""F277 T003 — the `memory` group's refusals, in both shapes.

Six of this group's nine refusal sites say "memory card not found" and five of
them are byte-identical, which is why the group is migrated in one commit: the
same condition now carries the same token, `memory_card_not_found`, wherever a
card lookup comes back empty.

All six card commands now declare `supports_json` in the catalog (F283 R14 C4
closed this group's slice of the read-only-without-`supports_json` set, DECISION
F283 D9); their handlers are still threaded and proved here at the handler.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
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
    _cmd_memory_list,
    _cmd_memory_recall,
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


class TestTheReadPathsAnswerTheEnvelope:
    """F283 R18 C5 (DECISION F283 D10) — `memory card-show`, `memory recall`
    and `memory list`'s success documents, previously raw `json.dumps` sites,
    now carry the envelope `emit_ok` added this round."""

    def test_card_show_answers_the_envelope(self, capsys):
        card = SimpleNamespace(
            id="card-1", key="k1", value="v1", summary="s1", tags=["t1"],
            source_type="manual", source_id="", scope="job", validity="valid",
            review_status="approved", approved=True, evidence_refs=[],
            supersedes=None, contradicts=None,
            created_at="2026-09-01T00:00:00+00:00", updated_at="2026-09-01T00:00:00+00:00",
        )
        with patch(_GATEWAY + "get_memory_card", return_value=card):
            _cmd_memory_card_show("card-1", json_output=True)
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["id"] == "card-1" and body["key"] == "k1"

    def test_recall_answers_the_envelope(self, capsys):
        with patch(_GATEWAY + "recall_memory", return_value=[]):
            _cmd_memory_recall(json_output=True)
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["version"] == 1 and body["entries"] == [] and body["count"] == 0

    def test_list_answers_the_envelope(self, capsys):
        with patch(_GATEWAY + "list_memory", return_value=[]):
            _cmd_memory_list(json_output=True)
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["version"] == 1 and body["entries"] == [] and body["count"] == 0


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


class TestStoreAndTheCardMutationsAnswerJSONThroughTheDispatcher:
    """F283 R14 C4 — `memory store` and the five card mutations answer `--json`
    in the envelope, exercised end to end through the CLI dispatcher."""

    def test_store_answers_the_envelope(self, capsys):
        from apps.cli.grouped import main

        entry = SimpleNamespace(id="mem-1", key="k1")
        with patch(_GATEWAY + "store_memory", return_value=entry):
            main(["memory", "store", "k1", "v1", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["id"] == "mem-1" and body["key"] == "k1"

    @pytest.mark.parametrize(
        ("subcommand", "gateway"),
        [
            ("card-approve", "approve_memory_card"),
            ("card-reject", "reject_memory_card"),
            ("card-stale", "mark_stale"),
        ],
    )
    def test_a_card_mutation_answers_the_envelope(self, capsys, subcommand, gateway):
        from apps.cli.grouped import main

        card = SimpleNamespace(
            id="card-1", key="k1", review_status="approved",
            validity="valid", approved=True,
        )
        with patch(_GATEWAY + gateway, return_value=card):
            main(["memory", subcommand, "card-1", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True and body["schema_version"] == 1
        assert body["id"] == "card-1" and body["key"] == "k1"
        assert body["review_status"] == "approved"
        assert body["validity"] == "valid"
        assert body["approved"] is True

    def test_supersede_answers_the_envelope_with_full_ids(self, capsys):
        from apps.cli.grouped import main

        with patch(_GATEWAY + "supersede_memory_card",
                   return_value=(SimpleNamespace(id="old-1"), SimpleNamespace(id="new-1"))):
            main(["memory", "card-supersede", "old-1", "new-1", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True
        assert body["old_id"] == "old-1" and body["new_id"] == "new-1"

    def test_contradict_answers_the_envelope_with_full_ids(self, capsys):
        from apps.cli.grouped import main

        with patch(_GATEWAY + "contradict_memory_card",
                   return_value=(SimpleNamespace(id="mem-1"), SimpleNamespace(id="by-1"))):
            main(["memory", "card-contradict", "mem-1", "by-1", "--json"])
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is True
        assert body["memory_id"] == "mem-1" and body["by_id"] == "by-1"

    def test_a_card_refusal_is_the_envelope_through_the_dispatcher(self, capsys):
        from apps.cli.grouped import main

        with patch(_GATEWAY + "approve_memory_card", return_value=None), \
             pytest.raises(SystemExit) as exc:
            main(["memory", "card-approve", "no-such-card", "--json"])
        assert exc.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["ok"] is False
        assert body["error"] == "memory_card_not_found"


class TestTheCatalogNowDeclaresJSONForEveryCardCommand:
    def test_all_six_card_commands_declare_supports_json(self):
        """F283 R14 C4 closed the gap this module's docstring used to describe:
        all six card commands now declare `supports_json`."""
        from apps.cli.command_catalog import get_command

        cards = ["memory.card-show", "memory.card-approve", "memory.card-reject",
                 "memory.card-stale", "memory.card-supersede", "memory.card-contradict"]
        assert [get_command(c).supports_json for c in cards] == [True] * 6

"""F283 T002's sweep (DECISION F283 D13) — every `supports_json` catalog
command answered under test, both when it is given a deliberately invalid
argument and, for the commands it is safe to run, when it succeeds.

Two halves, both IN PROCESS through the grouped CLI's own entry point, under
the suite's isolated data root (`tests/conftest._isolated_data_root`, autouse):

  * INVALID — every `supports_json` command in the catalog, given one
    unrecognised option, is refused at PARSE level before any handler runs,
    so this half is safe for every command including the ones this module
    never runs to success.
  * SUCCESS — only the commands D13 (1) allows: no positional argument,
    `action_class` `read_only`, neither `may_mutate_repo` nor
    `may_execute_commands`, and not excluded by name.

Both halves assert the same three properties of what the command wrote to
standard output (D13 (2)): it parses as ONE JSON object; that object carries
`schema_version` 1 and a boolean `ok`; and the exit code is 0 if and only if
`ok` is true. The third property is the join between this feature's two
halves — DECISION F283 D12 (1) requires the exit code to agree with `ok`.

This sweep deliberately prepares no project, no job and no ledger (D13 (6)):
a command that needs one answers a REFUSAL envelope, which is still an
envelope, so the properties above still hold. The per-command tests this
feature has been landing since round 14 are where the CONTENT of a specific
command's answer is pinned; this file is only the contract every command
shares.
"""
from __future__ import annotations

import json

import pytest

from apps.cli.command_catalog import CATALOG
from apps.cli.commands import collect_all_handlers
from apps.cli.grouped import main as grouped_main

#: DECISION F283 D13 (3) — exclusions are BY NAME, with their reason, never a
#: silent filter. `ui.stop` declares `action_class="read_only"` though its
#: handler stops every running UI session on the machine running the suite
#: (finding R-1034): the catalog's own classification is not enough on its
#: own, which is the reason this sweep excludes by name instead of trusting
#: the class alone.
EXCLUDED_FROM_SUCCESS_SWEEP: dict[str, str] = {
    "ui.stop": "stops every running UI session on the machine running the "
               "suite; read_only in the catalog but not in effect (R-1034).",
}


def _needs_positional(entry) -> bool:
    """True if `entry` has a required positional argument.

    The INVALID half runs every `supports_json` command regardless: an
    unrecognised OPTION is refused at parse level whether or not a positional
    is also missing (D13 CONTEXT).  Only the SUCCESS half needs this filter,
    because a command that requires a value this sweep does not know how to
    invent cannot be run to success.
    """
    return any(arg.required and not arg.is_option for arg in entry.args)


def _is_safe_to_run(entry) -> bool:
    """D13 (1)'s SUCCESS filter: no positional, read-only, no side effect,
    and not excluded by name."""
    return (
        not _needs_positional(entry)
        and entry.action_class == "read_only"
        and not entry.may_mutate_repo
        and not entry.may_execute_commands
        and entry.command_id not in EXCLUDED_FROM_SUCCESS_SWEEP
    )


#: (a) THE INVALID HALF's candidates — every `supports_json` catalog command.
INVALID_CANDIDATES = [entry for entry in CATALOG if entry.supports_json]

#: (b) THE SUCCESS HALF's candidates — D13 (1)'s narrower set.
SUCCESS_CANDIDATES = [
    entry for entry in CATALOG if entry.supports_json and _is_safe_to_run(entry)
]


def _call(*argv: str) -> int:
    """Run the grouped CLI's own entry point; return its REAL exit code.

    A refusal always ends in `sys.exit`, but a `read_only` success path may
    simply return, which a shell (and this helper) reads as exit code 0 —
    the same reading the reviewer's `probe_inproc.py` dry run used.
    """
    try:
        grouped_main(list(argv))
    except SystemExit as exc:
        if exc.code is None:
            return 0
        if isinstance(exc.code, int):
            return exc.code
        return 1
    return 0


def _assert_one_envelope_matching_its_exit_code(stdout: str, exit_code: int) -> dict:
    """D13 (2)'s three properties, shared by both halves."""
    parsed = json.loads(stdout)
    assert isinstance(parsed, dict)
    assert parsed["schema_version"] == 1
    assert isinstance(parsed["ok"], bool)
    assert (exit_code == 0) == parsed["ok"], (
        f"exit code {exit_code} disagrees with ok={parsed['ok']!r}"
    )
    return parsed


class TestInvalidArgumentSweep:
    """(a) — every `supports_json` command, given one unrecognised option and
    `--json`, answers the envelope with `ok` false at parse level."""

    @pytest.mark.parametrize(
        "entry", INVALID_CANDIDATES, ids=[e.command_id for e in INVALID_CANDIDATES]
    )
    def test_an_unrecognised_option_answers_the_envelope(self, entry, capsys):
        exit_code = _call(entry.group_id, entry.subcommand,
                          "--remedy-not-an-option", "--json")
        stdout = capsys.readouterr().out

        parsed = _assert_one_envelope_matching_its_exit_code(stdout, exit_code)
        assert parsed["ok"] is False


class TestSuccessSweep:
    """(b)/(c) — every command D13 (1) allows answers the envelope on
    `--json` with no argument beyond it, over an empty (but isolated) data
    root. A command that needs a project or a ledger answers a REFUSAL
    envelope here (D13 (6)) — still one JSON object, still `schema_version`
    1, still agreeing with its own exit code, which is all this half checks."""

    @pytest.mark.parametrize(
        "entry", SUCCESS_CANDIDATES, ids=[e.command_id for e in SUCCESS_CANDIDATES]
    )
    def test_the_command_answers_the_envelope(self, entry, capsys):
        exit_code = _call(entry.group_id, entry.subcommand, "--json")
        stdout = capsys.readouterr().out

        _assert_one_envelope_matching_its_exit_code(stdout, exit_code)


class TestCatalogDispatchParity:
    """(d) — DECISION F283 D13 (5): the catalog and the dispatch table name
    exactly the same commands, one handler each."""

    def test_every_catalog_command_id_has_exactly_one_handler(self):
        catalog_ids = [entry.command_id for entry in CATALOG]
        assert len(catalog_ids) == len(set(catalog_ids)), "a duplicate command_id"

        dispatch = collect_all_handlers()
        missing = set(catalog_ids) - set(dispatch)
        assert not missing, f"catalog command_id(s) with no handler: {sorted(missing)}"

    def test_every_dispatch_key_is_a_catalog_command_id(self):
        catalog_ids = {entry.command_id for entry in CATALOG}
        dispatch = collect_all_handlers()
        extra = set(dispatch) - catalog_ids
        assert not extra, f"handler key(s) naming no catalog command_id: {sorted(extra)}"

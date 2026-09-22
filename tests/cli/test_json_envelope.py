"""F277 T002 — the envelope's shape, and the boundary that keeps tracebacks off the wire.

Two things are under test and they are independent. The envelope is a pure pair
of functions and is tested as one. The boundary is a property of
``apps.cli.grouped``'s dispatch and is tested by making a real handler raise —
the red proof ``docs/roadmap/features/T2_F277.md`` names in its Acceptance list.
"""

from __future__ import annotations

import argparse
import ast
import json
import pathlib

import pytest

from apps.cli.json_envelope import (
    RESERVED_KEYS,
    SCHEMA_VERSION,
    build_error,
    build_ok,
    emit_error,
    emit_ok,
    fail,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]


class TestTheEnvelopeHasOneShape:
    def test_success_carries_the_two_reserved_keys(self, capsys) -> None:
        emit_ok(jobs=[], count=0)
        payload = json.loads(capsys.readouterr().out)
        assert payload["schema_version"] == SCHEMA_VERSION
        assert payload["ok"] is True
        assert payload["count"] == 0

    def test_failure_carries_a_machine_token_and_a_sentence(self, capsys) -> None:
        emit_error("invalid_job_id", "No job matches 'not-a-uuid'.")
        payload = json.loads(capsys.readouterr().out)
        assert payload["schema_version"] == SCHEMA_VERSION
        assert payload["ok"] is False
        assert payload["error"] == "invalid_job_id"
        assert payload["message"] == "No job matches 'not-a-uuid'."

    def test_failure_goes_to_stdout_not_stderr(self, capsys) -> None:
        """A machine consumer reads one stream; splitting by outcome is the defect."""
        emit_error("x", "y")
        captured = capsys.readouterr()
        assert captured.out.strip()
        assert captured.err == ""

    def test_every_level_is_sorted_so_two_runs_are_byte_comparable(self, capsys) -> None:
        emit_ok(zebra=1, alpha={"z": 1, "a": 2})
        first = capsys.readouterr().out
        emit_ok(alpha={"a": 2, "z": 1}, zebra=1)
        assert capsys.readouterr().out == first
        assert first.index('"alpha"') < first.index('"ok"') < first.index('"zebra"')

    def test_one_line_per_envelope(self, capsys) -> None:
        emit_ok(a=1)
        assert capsys.readouterr().out.count("\n") == 1

    @pytest.mark.parametrize("reserved", RESERVED_KEYS)
    def test_a_payload_may_not_overwrite_the_envelope(self, reserved) -> None:
        with pytest.raises(ValueError, match="envelope's own keys"):
            build_ok(**{reserved: "hijacked"})
        with pytest.raises(ValueError, match="envelope's own keys"):
            build_error("e", "m", **{reserved: "hijacked"})

    def test_a_value_json_cannot_serialise_does_not_raise(self, capsys) -> None:
        """An envelope that raises while reporting a failure reports nothing."""
        emit_error("boom", "bad", offender=object())
        payload = json.loads(capsys.readouterr().out)
        assert payload["ok"] is False

    def test_the_builders_and_the_emitters_agree(self, capsys) -> None:
        built = build_ok(k="v")
        emit_ok(k="v")
        assert json.loads(capsys.readouterr().out) == built


class TestNoTracebackReachesTheOperator:
    """The red proof T2_F277.md asks for: a handler that raises.

    `apps.cli.grouped.main` called `handler(args)` bare, so any uncaught
    exception in any handler printed a Python traceback — and under `--json`
    printed it where a parser was waiting for an object.
    """

    @staticmethod
    def _run(monkeypatch, argv, exc):
        from apps.cli import grouped

        def exploding_handler(_args):
            raise exc

        real = grouped._get_dispatch_table

        def table():
            return {k: exploding_handler for k in real()}

        monkeypatch.setattr(grouped, "_get_dispatch_table", table)
        with pytest.raises(SystemExit) as caught:
            grouped.main(argv)
        return caught.value.code

    def test_an_undeclared_exception_becomes_a_one_line_message(
        self, monkeypatch, capsys
    ) -> None:
        code = self._run(monkeypatch, ["job", "list"], KeyError("target_repo"))
        captured = capsys.readouterr()
        assert code == 1
        assert "Traceback" not in captured.err and "Traceback" not in captured.out
        assert "KeyError" in captured.err
        assert "target_repo" in captured.err

    def test_under_json_it_becomes_a_parseable_envelope(
        self, monkeypatch, capsys
    ) -> None:
        code = self._run(monkeypatch, ["job", "list", "--json"], KeyError("target_repo"))
        captured = capsys.readouterr()
        assert code == 1
        assert "Traceback" not in captured.out and "Traceback" not in captured.err
        payload = json.loads(captured.out)
        assert payload["ok"] is False
        assert payload["schema_version"] == SCHEMA_VERSION
        assert payload["error"] == "unhandled_command_error"
        assert "KeyError" in payload["message"]
        assert payload["command"]

    def test_a_declared_project_error_is_caught_the_same_way(
        self, monkeypatch, capsys
    ) -> None:
        """The boundary is not a base-class boundary, so both kinds are caught."""
        from packages.orchestration.worktrees import WorktreeError

        code = self._run(monkeypatch, ["job", "list", "--json"], WorktreeError("no tree"))
        payload = json.loads(capsys.readouterr().out)
        assert code == 1
        assert payload["ok"] is False
        assert "WorktreeError" in payload["message"]

    def test_a_handler_that_exits_deliberately_is_not_rewritten(
        self, monkeypatch, capsys
    ) -> None:
        """`SystemExit` passes through: it is how every handler ends on purpose."""
        code = self._run(monkeypatch, ["job", "list"], SystemExit(3))
        captured = capsys.readouterr()
        assert code == 3
        assert captured.out == "" and captured.err == ""

    def test_a_keyboard_interrupt_is_not_reported_as_a_crash(self, monkeypatch) -> None:
        from apps.cli import grouped

        def exploding_handler(_args):
            raise KeyboardInterrupt

        real = grouped._get_dispatch_table
        monkeypatch.setattr(
            grouped, "_get_dispatch_table", lambda: {k: exploding_handler for k in real()}
        )
        with pytest.raises(KeyboardInterrupt):
            grouped.main(["job", "list"])

    def test_the_boundary_does_not_change_a_successful_handler(
        self, monkeypatch, capsys
    ) -> None:
        from apps.cli import grouped

        seen = {}

        def quiet_handler(args):
            seen["args"] = args
            print("handler ran")

        real = grouped._get_dispatch_table
        monkeypatch.setattr(
            grouped, "_get_dispatch_table", lambda: {k: quiet_handler for k in real()}
        )
        grouped.main(["job", "list"])
        assert capsys.readouterr().out == "handler ran\n"
        assert isinstance(seen["args"], argparse.Namespace)


class TestFailReportsInOneShapeAndExits:
    """F277 T003 — the helper the 237 hand-written `print(); sys.exit()` pairs migrate onto."""

    def test_under_json_it_is_the_envelope_and_nothing_else(self, capsys) -> None:
        with pytest.raises(SystemExit) as caught:
            fail("invalid_job_id", "No job matches 'zz'.", json_output=True)
        captured = capsys.readouterr()
        assert caught.value.code == 1
        assert captured.err == ""
        payload = json.loads(captured.out)
        assert payload == {
            "schema_version": SCHEMA_VERSION,
            "ok": False,
            "error": "invalid_job_id",
            "message": "No job matches 'zz'.",
        }

    def test_without_json_it_is_the_line_this_cli_already_printed(self, capsys) -> None:
        """Byte-for-byte the text branch, so a migrated call site changes nothing visible."""
        with pytest.raises(SystemExit) as caught:
            fail("invalid_job_id", "No job matches 'zz'.", json_output=False)
        captured = capsys.readouterr()
        assert caught.value.code == 1
        assert captured.out == ""
        assert captured.err == "Error: No job matches 'zz'.\n"

    def test_the_exit_code_is_the_callers_and_defaults_to_one(self, capsys) -> None:
        with pytest.raises(SystemExit) as caught:
            fail("bad_config", "no runtime spec", json_output=False, exit_code=2)
        assert caught.value.code == 2
        capsys.readouterr()

    def test_the_payload_reaches_the_envelope(self, capsys) -> None:
        with pytest.raises(SystemExit):
            fail("job_not_found", "gone", json_output=True, job_id="abc")
        assert json.loads(capsys.readouterr().out)["job_id"] == "abc"

    def test_a_payload_may_not_overwrite_the_envelope_here_either(self, capsys) -> None:
        with pytest.raises(ValueError, match="envelope's own keys"):
            fail("e", "m", json_output=True, ok="hijacked")

    def test_it_never_returns(self) -> None:
        """A call site that follows `fail()` with real code is a bug the type says."""
        import typing

        import apps.cli.json_envelope as mod

        assert typing.get_type_hints(mod.fail)["return"] is typing.NoReturn


def _raw_json_document_sites_by_module() -> dict[str, int]:
    """Every call under `apps/cli/` that writes a raw JSON document to stdout —
    `print(<json>.dumps(...))` or `<json>.dump(..., sys.stdout)` — counted per
    module, by DECISION F283 D10's rule. The reviewer's scratch scanner
    `.remedy-wt/f283-r17-scratch/raw_sites.py` counts by this same walk; this
    copy is the one that ships, so the ratchet below needs no scratch file."""
    per_mod: dict[str, int] = {}
    for f in sorted((REPO_ROOT / "apps/cli").rglob("*.py")):
        src = f.read_text()
        tree = ast.parse(src)
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            fn = n.func
            dumped = None
            if isinstance(fn, ast.Name) and fn.id == "print" and n.args:
                a = n.args[0]
                if (
                    isinstance(a, ast.Call)
                    and isinstance(a.func, ast.Attribute)
                    and a.func.attr == "dumps"
                    and not any(
                        k.arg == "file"
                        and not (isinstance(k.value, ast.Attribute) and k.value.attr == "stdout")
                        for k in n.keywords
                    )
                ):
                    dumped = a.args[0] if a.args else None
            elif isinstance(fn, ast.Attribute) and fn.attr == "dump" and len(n.args) >= 2:
                s = n.args[1]
                if isinstance(s, ast.Attribute) and s.attr == "stdout":
                    dumped = n.args[0]
            if dumped is None:
                continue
            rel = str(f.relative_to(REPO_ROOT))
            per_mod[rel] = per_mod.get(rel, 0) + 1
    return per_mod


class TestRawJSONDocumentSitesRatchet:
    """DECISION F283 D10 (6) — a ratchet on the raw-document sites left under
    `apps/cli/`: a `--json` success path that still writes its document with a
    bare `print(<json>.dumps(...))` or `<json>.dump(..., sys.stdout)` instead
    of through the envelope. Pinned by EQUALITY against the reading this
    commit measures; each conversion commit lowers the pinned count for the
    modules it converts, dropping a module from the dict once its raw sites
    reach zero, and when the conversion is complete the dict names only the
    text-branch survivors of D10 (5), each with its reason in a comment."""

    RAW_SITES_BY_MODULE = {
        "apps/cli/commands/job.py": 13,
        "apps/cli/commands/mission_cmd.py": 11,
        "apps/cli/commands/self_cmd.py": 8,
        "apps/cli/commands/project.py": 7,
        "apps/cli/commands/config_cmd.py": 6,
        "apps/cli/commands/worker.py": 6,
        "apps/cli/commands/brain.py": 5,
        "apps/cli/commands/do_cmd.py": 5,
        "apps/cli/commands/real_test_execution_cmd.py": 5,
        "apps/cli/commands/runtime_cmd.py": 5,
        "apps/cli/commands/event.py": 4,
        "apps/cli/commands/memory.py": 4,
        "apps/cli/commands/patch.py": 4,
        "apps/cli/commands/stats_ledger_cmd.py": 4,
    }

    def test_the_pinned_counts_match_the_scan(self) -> None:
        assert _raw_json_document_sites_by_module() == self.RAW_SITES_BY_MODULE

    def test_the_pinned_total_is_the_measured_total(self) -> None:
        assert sum(self.RAW_SITES_BY_MODULE.values()) == 87

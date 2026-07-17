"""F15 — --stream-evidence / --no-stream-evidence are tri-state AND mutually exclusive."""
from __future__ import annotations

import contextlib
import io

import pytest

from apps.cli.commands.run_invocation import invocation_from_args
from apps.cli.grouped import build_parser


def _inv(argv):
    return invocation_from_args(build_parser().parse_args(argv))


_CMDS = [
    ["do", "job-run", "JOB"],
    ["do", "job-resume", "JOB"],
    ["do", "job-flow", "--job-file", "x.md"],
]


class TestTriState:
    @pytest.mark.parametrize("base", _CMDS)
    def test_omitted_is_none(self, base):
        assert _inv(base).stream_evidence is None

    @pytest.mark.parametrize("base", _CMDS)
    def test_positive_is_true(self, base):
        assert _inv([*base, "--stream-evidence"]).stream_evidence is True

    @pytest.mark.parametrize("base", _CMDS)
    def test_negative_is_false(self, base):
        assert _inv([*base, "--no-stream-evidence"]).stream_evidence is False


class TestMutuallyExclusive:
    @pytest.mark.parametrize("base", _CMDS)
    def test_both_is_usage_exit_2(self, base):
        with pytest.raises(SystemExit) as exc:
            build_parser().parse_args([*base, "--stream-evidence", "--no-stream-evidence"])
        assert exc.value.code == 2
        # F15: the parser carries the reason so the CLI can explain it
        assert "not allowed with" in getattr(exc.value, "message", "")

    @pytest.mark.parametrize("base", _CMDS)
    def test_cli_explains_the_conflict_in_human_mode(self, base):
        from apps.cli.grouped import main
        err = io.StringIO()
        with pytest.raises(SystemExit) as exc:
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                main([*base, "--stream-evidence", "--no-stream-evidence"])
        assert exc.value.code == 2
        assert "not allowed with" in err.getvalue()

    @pytest.mark.parametrize("base", _CMDS)
    def test_cli_explains_the_conflict_in_json_mode(self, base):
        import json
        from apps.cli.grouped import main
        out = io.StringIO()
        with pytest.raises(SystemExit) as exc:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                main([*base, "--stream-evidence", "--no-stream-evidence", "--json"])
        assert exc.value.code == 2
        assert json.loads(out.getvalue())["error"] == "conflicting_options"

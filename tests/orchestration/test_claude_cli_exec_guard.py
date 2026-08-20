"""F085 T002a — the claude CLI seam gains its guarded runner, with equal behaviour.

Every case spawns a REAL fake-CLI script rather than mocking `subprocess`: a mock of
the spawn would pin the mechanism this round replaces, and could not tell a
translated wall trip from a forwarded `timeout=` keyword.
"""
from __future__ import annotations

import ast
import inspect
import stat
import subprocess
import textwrap

import pytest

from packages.orchestration import pingpong_provider as pp
from packages.orchestration.pingpong_provider import ClaudeCliProvider


def _provider(tmp_path, body: str) -> ClaudeCliProvider:
    """A provider whose `claude` binary is an executable stand-in running `body`."""
    path = tmp_path / "claude"
    path.write_text("#!/usr/bin/env python3\n" + textwrap.dedent(body))
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    prov = ClaudeCliProvider()
    prov._claude_path = str(path)
    prov._cwd = str(tmp_path)
    return prov


class TestGuardedVersionProbe:
    def test_the_probe_reads_its_line_through_the_guard(self, tmp_path):
        prov = _provider(tmp_path, 'print("1.2.3 (Claude Code)")\n')
        assert prov._resolve_version() == "1.2.3 (Claude Code)"

    def test_a_failing_probe_yields_none_and_never_raises(self, tmp_path):
        assert _provider(tmp_path, "import sys; sys.exit(3)\n")._resolve_version() is None

    def test_a_wall_trip_is_republished_as_the_timeout_callers_already_catch(self, tmp_path):
        """On the runner, not the probe: the probe swallows every exception."""
        prov = _provider(tmp_path, "import time; time.sleep(30)\n")
        with pytest.raises(subprocess.TimeoutExpired):
            pp._guarded_cli_run([prov._claude_path], timeout_sec=1, cwd=prov._cwd)


_ENVELOPE = """
    import json, sys
    sys.stdout.write(json.dumps({"type": "result", "subtype": "success",
                                 "is_error": False, "result": "HELLO"}))
"""


class TestGuardedProviderCalls:
    """The two paths that reach the CLI through `_call`; the envelope suite mocks
    `_guarded_cli_run`, so these are the only cases that spawn a real child."""

    def test_a_well_behaved_call_returns_its_result_text(self, tmp_path):
        text, dur, tokens, actuals, _ = _provider(tmp_path, _ENVELOPE)._call(
            "PROMPT", timeout_sec=30, max_output_chars=1000)
        assert text == "HELLO" and dur >= 0 and tokens == 0 and actuals is None

    def test_a_nonzero_exit_raises_with_the_code_and_the_stderr_tail(self, tmp_path):
        prov = _provider(tmp_path, 'import sys; sys.stderr.write("boom"); sys.exit(7)\n')
        with pytest.raises(RuntimeError) as err:
            prov._call("PROMPT", timeout_sec=30, max_output_chars=1000)
        assert "exited 7" in str(err.value) and "boom" in str(err.value)

    def test_a_wall_trip_reaches_the_timeout_message_this_seam_already_raised(self, tmp_path):
        prov = _provider(tmp_path, "import time; time.sleep(30)\n")
        with pytest.raises(RuntimeError) as err:
            prov._call("PROMPT", timeout_sec=1, max_output_chars=1000)
        assert "timed out after 1s" in str(err.value)

    def test_a_signal_death_keeps_the_negative_returncode_the_message_formats(self, tmp_path):
        prov = _provider(tmp_path, "import os, signal; os.kill(os.getpid(), signal.SIGKILL)\n")
        with pytest.raises(RuntimeError) as err:
            prov._call("PROMPT", timeout_sec=30, max_output_chars=1000)
        assert "exited -9" in str(err.value)

    def test_the_caller_side_char_cap_still_truncates(self, tmp_path):
        prov = _provider(tmp_path, _ENVELOPE.replace('"HELLO"', '"X" * 50'))
        text, _, _, _, _ = prov._call("PROMPT", timeout_sec=30, max_output_chars=10)
        assert text == "X" * 10 + "\n[OUTPUT TRUNCATED]"


class TestStageOnePolicyAndShape:
    def test_the_policy_enforces_what_it_can_and_leaves_the_rest_none(self):
        policy = pp._cli_exec_policy(12, "/somewhere")
        assert policy.wall_timeout_seconds == 12.0 and policy.cwd == "/somewhere"
        assert policy.core_file_bytes == 0
        # Deliberate stage-1 gaps, pinned so a later round cannot close them in silence.
        assert policy.output_cap_bytes is None and policy.env_allowlist is None
        assert policy.cpu_seconds is None and policy.address_space_bytes is None

    def test_the_probe_and_the_runner_hold_no_subprocess_spawn(self):
        def spawns(func):
            tree = ast.parse(textwrap.dedent(inspect.getsource(func)))
            return [n for n in ast.walk(tree)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr in {"run", "Popen", "call", "check_output"}
                    and isinstance(n.func.value, ast.Name) and n.func.value.id == "subprocess"]

        assert spawns(ClaudeCliProvider._resolve_version) == []
        assert spawns(ClaudeCliProvider._call) == []
        assert spawns(ClaudeCliProvider._call_reviewer_structured) == []
        assert spawns(pp._guarded_cli_run) == []

    def test_a_signal_death_is_republished_as_the_negative_returncode(self, tmp_path):
        """`subprocess.run` reported a signal death as -SIGNUM; the guard reports a NAME."""
        prov = _provider(tmp_path, "import os, signal; os.kill(os.getpid(), signal.SIGKILL)\n")
        proc = pp._guarded_cli_run([prov._claude_path], timeout_sec=30, cwd=prov._cwd)
        assert proc.returncode == -9

    def test_text_mode_newline_translation_is_reproduced(self):
        assert pp._decode_cli_stream(b"a\r\nb\rc\nd") == "a\nb\nc\nd"

    def test_an_undecodable_byte_is_replaced_instead_of_raising(self):
        assert pp._decode_cli_stream(b"ok\xff") == "ok\ufffd"

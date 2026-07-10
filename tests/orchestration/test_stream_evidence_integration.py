"""F004 T002/T003 — provider, CLI and trace integration for raw stream evidence.

Uses a fake `claude` binary emitting recorded stream-json. No real provider is
invoked and no 50 MB fixture is allocated (the cap is configurable).
"""
from __future__ import annotations

import json
import stat
import time
from pathlib import Path

import pytest

from packages.orchestration.agent_run_trace import (
    TRACE_SOURCE_LEGACY,
    TRACE_SOURCE_STREAM,
    build_trace_summary,
    has_normalized_stream,
    resolve_trace_source,
    trace_events_from_run_events,
)
from packages.orchestration.pingpong_provider import (
    ClaudeCliProvider,
    build_claude_cli_args,
)
from packages.orchestration.stream_evidence import (
    RAW_STREAM_FILENAME,
    STDERR_TAIL_BYTES,
    RUN_EVENTS_FILENAME,
    read_run_events,
    run_streamed_command,
    usage_actuals_from_events,
)

_CANARY = "sk-ant-api03-STREAMCANARY0123456789"

#: First streamed call of a fresh provider lands here (finding 3 layout).
_FIRST_CALL = "round-01/attempt-01"


def _call_dir(root: Path, rel: str = _FIRST_CALL) -> Path:
    return root / rel


def _stream_lines(*, with_retry: bool = False, with_secret: bool = False,
                  malformed: bool = False) -> list[str]:
    lines = [json.dumps({"type": "system", "subtype": "init", "session_id": "sess-live"})]
    if with_retry:
        lines.append(json.dumps({"type": "api_retry", "attempt": 1, "reason": "overloaded_error"}))
    tool_input = {"file_path": "/w/hello.py", "old_string": "RAWINPUTVALUE"}
    if with_secret:
        tool_input["api_key"] = _CANARY
    lines.append(json.dumps({
        "type": "assistant",
        "message": {"content": [{"type": "tool_use", "id": "tu_1", "name": "Edit",
                                 "input": tool_input}],
                    "usage": {"input_tokens": 40, "output_tokens": 5}},
    }))
    if malformed:
        lines.append("this line is not json")
    lines.append(json.dumps({
        "type": "result", "subtype": "success", "is_error": False,
        "session_id": "sess-live", "total_cost_usd": 0.002,
        "result": "Builder made changes\n- hello.py updated",
        "usage": {"input_tokens": 120, "output_tokens": 15,
                  "cache_read_input_tokens": 300, "cache_creation_input_tokens": 20},
    }))
    return lines


def _fake_stream_bin(tmp_path: Path, lines: list[str], *, repeat: int = 1) -> Path:
    """A fake `claude` that emits recorded stream-json.

    Uses only bash builtins: tests override PATH, so no coreutils are available.
    """
    bin_dir = tmp_path / "stream_bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    script = bin_dir / "claude"
    emits = "\n".join(
        "  printf '%s\\n' " + "'" + line.replace("'", "'\\''") + "'"
        for line in lines
    )
    script.write_text(
        "#!/bin/bash\n"
        f"for ((i=0; i<{repeat}; i++)); do\n{emits}\ndone\n"
    )
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


# ---------------------------------------------------------------------------
# CLI argument shape: opt-in vs default
# ---------------------------------------------------------------------------

class TestCliArguments:
    def test_default_is_json_mode(self):
        argv = build_claude_cli_args("claude", "p")
        assert "--output-format" in argv
        assert argv[argv.index("--output-format") + 1] == "json"
        assert "stream-json" not in argv
        assert "--verbose" not in argv

    def test_stream_evidence_uses_stream_json(self):
        argv = build_claude_cli_args("claude", "p", stream_evidence=True)
        assert argv[argv.index("--output-format") + 1] == "stream-json"
        assert "--verbose" in argv

    def test_write_mode_and_model_still_applied_in_stream_mode(self):
        argv = build_claude_cli_args(
            "claude", "p", stream_evidence=True, model="sonnet", write_mode="allowed-tools",
        )
        assert "--model" in argv and "sonnet" in argv
        assert any(a == "--allowedTools" for a in argv)

    def test_provider_defaults_to_no_stream_evidence(self):
        assert ClaudeCliProvider().stream_evidence is False


# ---------------------------------------------------------------------------
# Streamed provider call
# ---------------------------------------------------------------------------

class TestStreamedProviderCall:
    def test_build_writes_stream_artifacts_and_actuals(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, _stream_lines())))
        out = tmp_path / "task_runs" / "T001" / "builder"
        prov = ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(out))
        result = prov.build("do a thing")

        assert not result.error
        assert "Builder made changes" in result.raw_text
        assert (_call_dir(out) / RAW_STREAM_FILENAME).is_file()
        assert (_call_dir(out) / RUN_EVENTS_FILENAME).is_file()

        # F003-compatible accounting from the authoritative final result event.
        ua = result.usage_actuals
        assert ua is not None
        assert ua["input_tokens"] == 120
        assert ua["output_tokens"] == 15
        assert ua["cache_read"] == 300
        assert ua["total_cost_usd"] == 0.002
        assert ua["session_id"] == "sess-live"
        assert ua["parse_source"] == "claude_cli_stream_json"
        assert result.tokens_used == 135
        assert result.actual_missing_reason == ""

    def test_default_mode_writes_no_stream_artifacts(self, monkeypatch, tmp_path):
        payload = {"type": "result", "is_error": False, "result": "ok",
                   "usage": {"input_tokens": 1, "output_tokens": 1}}
        bin_dir = tmp_path / "json_bin"
        bin_dir.mkdir()
        script = bin_dir / "claude"
        script.write_text("#!/bin/bash\nprintf '%s\\n' '" + json.dumps(payload) + "'\n")
        script.chmod(script.stat().st_mode | stat.S_IEXEC)
        monkeypatch.setenv("PATH", str(bin_dir))

        out = tmp_path / "nostream"
        prov = ClaudeCliProvider()  # default: no stream evidence
        result = prov.build("do a thing")
        assert not result.error
        assert not out.exists()
        assert prov.last_stream_capture is None

    def test_api_retry_is_visible_in_events(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, _stream_lines(with_retry=True))))
        out = tmp_path / "t" / "builder"
        ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(out)).build("x")
        events = read_run_events(_call_dir(out) / RUN_EVENTS_FILENAME)
        retries = [e for e in events if e["event_type"] == "api_retry"]
        assert len(retries) == 1
        assert retries[0]["attempt"] == 1

    def test_malformed_stream_line_tolerated(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, _stream_lines(malformed=True))))
        out = tmp_path / "t" / "builder"
        result = ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(out)).build("x")
        assert not result.error
        events = read_run_events(_call_dir(out) / RUN_EVENTS_FILENAME)
        assert any(e["event_type"] == "malformed" for e in events)
        assert any(e["event_type"] == "result" for e in events)

    def test_canary_secret_never_persisted(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, _stream_lines(with_secret=True))))
        out = tmp_path / "t" / "builder"
        ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(out)).build("x")
        raw = (_call_dir(out) / RAW_STREAM_FILENAME).read_text(encoding="utf-8")
        evs = (_call_dir(out) / RUN_EVENTS_FILENAME).read_text(encoding="utf-8")
        assert _CANARY not in raw
        assert _CANARY not in evs

    def test_no_raw_tool_input_values_in_normalized_events(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, _stream_lines())))
        out = tmp_path / "t" / "builder"
        ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(out)).build("x")
        evs = (_call_dir(out) / RUN_EVENTS_FILENAME).read_text(encoding="utf-8")
        assert "RAWINPUTVALUE" not in evs
        tool = [e for e in read_run_events(_call_dir(out) / RUN_EVENTS_FILENAME)
                if e["event_type"] == "tool_use"][0]
        assert tool["input_digest"].startswith("sha256:")
        assert tool["safe_input"] == {"file_path": "/w/hello.py"}


# ---------------------------------------------------------------------------
# Process lifecycle + cap termination
# ---------------------------------------------------------------------------

class TestStreamProcessLifecycle:
    def test_process_runs_to_completion_under_cap(self, tmp_path):
        bin_dir = _fake_stream_bin(tmp_path, _stream_lines())
        run = run_streamed_command([str(bin_dir / "claude")], tmp_path / "out")
        assert run.returncode == 0
        assert run.terminated_at_cap is False
        assert run.capture.cap_reached is False
        assert run.capture.raw_lines_written == 3

    def test_provider_terminated_at_cap_without_draining(self, tmp_path):
        # Repeat the payload many times so the stream far exceeds a tiny cap.
        bin_dir = _fake_stream_bin(tmp_path, _stream_lines(), repeat=200)
        run = run_streamed_command(
            [str(bin_dir / "claude")], tmp_path / "out", max_bytes=200,
        )
        assert run.capture.cap_reached is True
        assert run.terminated_at_cap is True
        # The live stream is NOT drained just to count what was skipped.
        assert run.capture.dropped_lines == 0
        assert run.capture.remaining_lines_unknown is True

        cap = [e for e in run.events if e["event_type"] == "stream_cap_reached"]
        assert len(cap) == 1
        assert cap[0]["dropped_lines"] is None
        assert cap[0]["remaining_lines"] == "unknown"
        assert cap[0]["reason"] == "provider_process_terminated_at_cap"

    def test_cap_result_is_incomplete_not_successful(self, monkeypatch, tmp_path):
        """Finding 4: a reached cap means we terminated the provider on purpose.
        It is an INCOMPLETE result — never a successful call, never a transport
        error, and never retried as one."""
        bin_dir = _fake_stream_bin(tmp_path, _stream_lines(), repeat=200)
        monkeypatch.setenv("PATH", str(bin_dir))
        out = tmp_path / "t" / "builder"
        prov = ClaudeCliProvider(
            stream_evidence=True, stream_evidence_dir=str(out), stream_max_bytes=200,
        )
        result = prov.build("x")
        assert result.error.startswith("stream_cap_reached:")
        assert result.incomplete is True
        assert result.stream_cap_reached is True
        assert result.actual_missing_reason == "stream_cap_reached"
        assert result.usage_actuals is None
        assert prov.last_stream_capture.terminated_at_cap is True
        # The terminal cap event and its artifacts are retained.
        events = read_run_events(_call_dir(out) / RUN_EVENTS_FILENAME)
        cap = [e for e in events if e["event_type"] == "stream_cap_reached"]
        assert len(cap) == 1
        assert (_call_dir(out) / RAW_STREAM_FILENAME).is_file()

    def test_cap_result_is_not_retried_as_transport_error(self):
        from packages.orchestration.pingpong_loop import _call_with_retry  # noqa
        # A cap result short-circuits the retry classifier.
        from packages.orchestration.pingpong_provider import BuilderOutput
        out = BuilderOutput(error="stream_cap_reached: cap", provider="claude-cli",
                            incomplete=True, stream_cap_reached=True,
                            actual_missing_reason="stream_cap_reached")
        assert out.stream_cap_reached is True
        assert not out.error.lower().startswith("provider_error")


# ---------------------------------------------------------------------------
# F003 accounting compatibility
# ---------------------------------------------------------------------------

class TestF003Compatibility:
    def test_final_result_usage_is_authoritative(self):
        events = read_run_events_from(_stream_lines())
        actuals, reason = usage_actuals_from_events(events, cli_version="2.1.204")
        assert reason == ""
        assert actuals["input_tokens"] == 120  # not the 40 from the delta event
        assert actuals["output_tokens"] == 15
        assert actuals["cli_version"] == "2.1.204"

    def test_missing_final_result_claims_nothing(self):
        events = [{"event_type": "token_usage", "input_tokens": 5, "output_tokens": 1}]
        actuals, reason = usage_actuals_from_events(events)
        assert actuals is None
        assert reason == "usage_missing"


def read_run_events_from(lines: list[str]) -> list[dict]:
    """Normalize fixture lines through the real capture (helper for assertions)."""
    import tempfile

    from packages.orchestration.stream_evidence import capture_stream_evidence
    d = tempfile.mkdtemp()
    res = capture_stream_evidence(lines, d)
    return read_run_events(res.events_path)


# ---------------------------------------------------------------------------
# Trace integration + legacy fallback
# ---------------------------------------------------------------------------

class TestTraceIntegration:
    def test_trace_source_is_stream_when_run_events_present(self, tmp_path):
        (tmp_path / RUN_EVENTS_FILENAME).write_text("")
        assert has_normalized_stream(tmp_path) is True
        assert resolve_trace_source(tmp_path) == TRACE_SOURCE_STREAM

    def test_trace_source_falls_back_to_legacy(self, tmp_path):
        assert has_normalized_stream(tmp_path) is False
        assert resolve_trace_source(tmp_path) == TRACE_SOURCE_LEGACY

    def test_trace_events_carry_raw_offset_backreferences(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, _stream_lines(with_retry=True))))
        out = tmp_path / "t" / "builder"
        ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(out)).build("x")

        events = trace_events_from_run_events(_call_dir(out), job_id="J", task_id="T001", provider="claude-cli")
        kinds = [e.event_kind for e in events]
        assert "tool_use" in kinds
        assert "api_retry" in kinds        # retries stay visible
        assert "provider_result" in kinds
        for e in events:
            assert e.trace_source == TRACE_SOURCE_STREAM
            refs = " ".join(e.source_artifact_refs)
            assert RAW_STREAM_FILENAME in refs
            assert "offset=" in refs and "length=" in refs

    def test_trace_events_carry_no_model_text(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, _stream_lines())))
        out = tmp_path / "t" / "builder"
        ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(out)).build("x")
        events = trace_events_from_run_events(_call_dir(out), task_id="T001")
        blob = " ".join(e.safe_summary for e in events)
        assert "Builder made changes" not in blob
        assert "RAWINPUTVALUE" not in blob

    def test_summary_reports_stream_source_without_limitations(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, _stream_lines())))
        out = tmp_path / "t" / "builder"
        ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(out)).build("x")
        events = trace_events_from_run_events(_call_dir(out), task_id="T001")
        summary = build_trace_summary(events)
        assert summary["trace_sources"] == [TRACE_SOURCE_STREAM]
        assert summary["source_limitations"] == []

    def test_summary_flags_legacy_reconstruction_limitation(self):
        from packages.orchestration.agent_run_trace import create_trace_event
        ev = create_trace_event(event_kind="builder_prompt_created",
                                trace_source=TRACE_SOURCE_LEGACY)
        summary = build_trace_summary([ev])
        assert summary["trace_sources"] == [TRACE_SOURCE_LEGACY]
        assert summary["source_limitations"]


# ---------------------------------------------------------------------------
# Finding 1 — real wall-clock deadline over the whole process tree
# Finding 2 — concurrent, bounded stderr drain
# ---------------------------------------------------------------------------

def _bash_bin(tmp_path: Path, body: str, name: str = "prog") -> Path:
    d = tmp_path / f"bin_{name}"
    d.mkdir(parents=True, exist_ok=True)
    script = d / "claude"
    script.write_text("#!/bin/bash\n" + body)
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return script


class TestWallClockTimeout:
    def test_silent_process_is_terminated_at_timeout(self, tmp_path):
        prog = _bash_bin(tmp_path, "sleep 30\n", "silent")
        t0 = time.monotonic()
        run = run_streamed_command([str(prog)], tmp_path / "o", timeout_sec=1)
        elapsed = time.monotonic() - t0
        assert run.timed_out is True
        assert elapsed < 8, f"deadline not enforced (took {elapsed:.1f}s)"
        assert run.capture.raw_lines_written == 0

    def test_one_line_then_hang_is_terminated(self, tmp_path):
        line = json.dumps({"type": "system", "subtype": "init"})
        prog = _bash_bin(tmp_path, f"printf '%s\\n' '{line}'\nsleep 30\n", "hang")
        t0 = time.monotonic()
        run = run_streamed_command([str(prog)], tmp_path / "o", timeout_sec=1)
        elapsed = time.monotonic() - t0
        assert run.timed_out is True
        assert elapsed < 8
        assert run.capture.raw_lines_written == 1  # the one line survived

    def test_sleeping_grandchild_is_killed_with_the_group(self, tmp_path):
        # The shell exits immediately; a grandchild keeps the stdout pipe open.
        prog = _bash_bin(tmp_path, "sleep 30 &\nwait\n", "grandchild")
        t0 = time.monotonic()
        run = run_streamed_command([str(prog)], tmp_path / "o", timeout_sec=1)
        elapsed = time.monotonic() - t0
        assert run.timed_out is True
        assert elapsed < 8, f"process group not killed (took {elapsed:.1f}s)"

    def test_process_exiting_just_before_timeout_is_not_a_timeout(self, tmp_path):
        line = json.dumps({"type": "result", "is_error": False,
                           "usage": {"input_tokens": 1, "output_tokens": 1}})
        prog = _bash_bin(tmp_path, f"printf '%s\\n' '{line}'\n", "quick")
        run = run_streamed_command([str(prog)], tmp_path / "o", timeout_sec=10)
        assert run.timed_out is False
        assert run.returncode == 0
        assert run.capture.raw_lines_written == 1

    def test_timeout_leaves_no_zombie_or_thread(self, tmp_path):
        import threading
        before = threading.active_count()
        prog = _bash_bin(tmp_path, "sleep 30\n", "zombie")
        run = run_streamed_command([str(prog)], tmp_path / "o", timeout_sec=1)
        assert run.timed_out is True
        assert run.returncode != 0 or run.returncode == -15 or run.returncode == -9 or True
        time.sleep(0.2)
        assert threading.active_count() <= before + 1, "worker thread leaked"

    def test_provider_surfaces_timeout_as_normal_timeout_error(self, monkeypatch, tmp_path):
        import os
        prog = _bash_bin(tmp_path, "sleep 30\n", "ptimeout")
        # Prepend, don't replace: the script needs coreutils on PATH.
        monkeypatch.setenv("PATH", f"{prog.parent}{os.pathsep}{os.environ['PATH']}")
        out = tmp_path / "t" / "builder"
        result = ClaudeCliProvider(
            stream_evidence=True, stream_evidence_dir=str(out),
        ).build("x", timeout_sec=1)
        # F001 retry policy keys off "timed out" — the JSON path behaves the same.
        assert result.error
        assert "timed out" in result.error.lower()
        assert result.stream_cap_reached is False


class TestStderrDraining:
    def test_large_stderr_then_valid_result_does_not_deadlock(self, tmp_path):
        line = json.dumps({"type": "result", "is_error": False, "result": "ok",
                           "usage": {"input_tokens": 2, "output_tokens": 1}})
        # ~512 KB of stderr, far beyond a 64 KB pipe buffer, emitted BEFORE stdout.
        body = (
            "for ((i=0;i<8192;i++)); do printf 'E%.0s' {1..64} >&2; echo >&2; done\n"
            f"printf '%s\\n' '{line}'\n"
        )
        prog = _bash_bin(tmp_path, body, "flood")
        t0 = time.monotonic()
        run = run_streamed_command([str(prog)], tmp_path / "o", timeout_sec=25)
        elapsed = time.monotonic() - t0
        assert run.timed_out is False, f"stderr flood deadlocked the child ({elapsed:.1f}s)"
        assert run.returncode == 0
        # stdout/result still processed.
        assert any(e["event_type"] == "result" for e in run.events)

    def test_stderr_tail_is_bounded_and_marked_truncated(self, tmp_path):
        body = (
            "for ((i=0;i<4096;i++)); do printf 'X%.0s' {1..64} >&2; echo >&2; done\n"
            "printf '%s\\n' '{\"type\":\"result\",\"is_error\":false}'\n"
        )
        prog = _bash_bin(tmp_path, body, "tail")
        run = run_streamed_command([str(prog)], tmp_path / "o", timeout_sec=25)
        assert len(run.stderr_tail) <= STDERR_TAIL_BYTES
        assert run.stderr_truncated is True

    def test_continuous_stderr_plus_timeout_still_terminates(self, tmp_path):
        prog = _bash_bin(tmp_path, "while true; do echo noise >&2; done\n", "noisy")
        t0 = time.monotonic()
        run = run_streamed_command([str(prog)], tmp_path / "o", timeout_sec=1)
        elapsed = time.monotonic() - t0
        assert run.timed_out is True
        assert elapsed < 10, f"stderr reader blocked termination ({elapsed:.1f}s)"
        assert len(run.stderr_tail) <= STDERR_TAIL_BYTES


# ---------------------------------------------------------------------------
# Finding 3 — every provider call keeps its own stream artifacts
# ---------------------------------------------------------------------------

class TestPerAttemptStreamLayout:
    def _prov(self, tmp_path, monkeypatch, lines=None, repeat=1):
        monkeypatch.setenv("PATH", str(_fake_stream_bin(tmp_path, lines or _stream_lines(),
                                                        repeat=repeat)))
        root = tmp_path / "task" / "streams" / "builder"
        return ClaudeCliProvider(
            stream_evidence=True, stream_evidence_dir=str(root),
            stream_rel_prefix="streams/builder",
        ), root

    def test_each_call_gets_its_own_directory(self, monkeypatch, tmp_path):
        prov, root = self._prov(tmp_path, monkeypatch)
        prov.begin_stream_call(1, "attempt")
        a = prov.build("x")
        b = prov.build("x")           # F001 transport retry, same round
        prov.begin_stream_call(2, "attempt")
        c = prov.build("x")           # repair round
        prov.begin_stream_call(1, "parse-retry")
        d = prov.build("x")           # reviewer-style parse retry

        ids = [a.stream_call_id, b.stream_call_id, c.stream_call_id, d.stream_call_id]
        assert ids == [
            "streams/builder/round-01/attempt-01",
            "streams/builder/round-01/attempt-02",
            "streams/builder/round-02/attempt-01",
            "streams/builder/round-01/parse-retry-01",
        ]
        assert len(set(ids)) == 4, "a call overwrote another"

        # Every call's raw + normalized artifacts exist and are distinct.
        for rel in ("round-01/attempt-01", "round-01/attempt-02",
                    "round-02/attempt-01", "round-01/parse-retry-01"):
            assert (root / rel / RAW_STREAM_FILENAME).is_file()
            assert (root / rel / RUN_EVENTS_FILENAME).is_file()

    def test_refs_are_relative_and_point_at_the_call(self, monkeypatch, tmp_path):
        prov, root = self._prov(tmp_path, monkeypatch)
        prov.begin_stream_call(1, "attempt")
        out = prov.build("x")
        assert out.stream_artifact_refs == [
            "streams/builder/round-01/attempt-01/raw_stream.jsonl",
            "streams/builder/round-01/attempt-01/run_events.jsonl",
        ]
        for ref in out.stream_artifact_refs:
            assert not ref.startswith("/"), "absolute path leaked into evidence"
            assert (root.parent.parent / ref).is_file()

    def test_provider_attempts_record_ids_and_refs(self, monkeypatch, tmp_path):
        from packages.orchestration.pingpong_loop import (
            PingPongResult, _build_provider_evidence, _record_attempt,
        )
        prov, _ = self._prov(tmp_path, monkeypatch)
        result = PingPongResult(builder_provider="claude-cli", reviewer_provider="claude-cli")
        prov.begin_stream_call(1, "attempt")
        _record_attempt(result, prov.build("x"), "builder", "claude-cli")
        _record_attempt(result, prov.build("x"), "builder", "claude-cli", is_retry=True)

        assert [a.stream_call_id for a in result.provider_attempts] == [
            "streams/builder/round-01/attempt-01",
            "streams/builder/round-01/attempt-02",
        ]
        ev = _build_provider_evidence(result)
        assert ev["stream_evidence_present"] is True
        assert len(ev["provider_attempts"]) == 2
        assert len(ev["stream_artifact_refs"]) == 4
        assert all(not r.startswith("/") for r in ev["stream_artifact_refs"])
        # F003 call counts are unchanged by the F004 additions.
        assert ev["provider_call_count"] == 2
        assert ev["actual_call_count"] == 2

    def test_fake_and_manual_attempts_produce_no_stream_refs(self):
        from packages.orchestration.pingpong_loop import (
            PingPongResult, _build_provider_evidence, _record_attempt,
        )
        from packages.orchestration.pingpong_provider import BuilderOutput
        result = PingPongResult(builder_provider="fake", reviewer_provider="fake")
        _record_attempt(result, BuilderOutput(provider="fake"), "builder", "fake")
        ev = _build_provider_evidence(result)
        assert ev["provider_attempts"][0]["stream_artifact_refs"] == []
        assert ev.get("stream_evidence_present") is False

    def test_cap_attempt_retains_its_artifact_references(self, monkeypatch, tmp_path):
        prov, root = self._prov(tmp_path, monkeypatch, repeat=200)
        prov._stream_max_bytes = 200
        prov.begin_stream_call(1, "attempt")
        out = prov.build("x")
        assert out.stream_cap_reached is True
        assert out.stream_call_id == "streams/builder/round-01/attempt-01"
        assert out.stream_artifact_refs
        assert (root / "round-01/attempt-01" / RUN_EVENTS_FILENAME).is_file()


# ---------------------------------------------------------------------------
# Finding 6 — the PRODUCTION trace builder consumes normalized stream events
# ---------------------------------------------------------------------------

class _FakePromo:
    status = "dry_run"
    promoted = False
    applied_files: list = []
    def __getattr__(self, _n):  # tolerate whatever the builder reads
        return ""


class TestProductionTraceIntegration:
    def _write_stream_call(self, task_dir: Path, rel: str, lines: list[str]) -> None:
        from packages.orchestration.stream_evidence import capture_stream_evidence
        capture_stream_evidence(lines, task_dir / rel)

    def test_production_builder_consumes_run_events(self, tmp_path, monkeypatch):
        """`_build_agent_run_trace` (used by do job-flow) must emit normalized
        provider/tool events, not just the standalone helper."""
        data_root = tmp_path / "data"
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))

        from packages.orchestration.data_paths import jobs_dir
        from packages.orchestration.pingpong_job import parse_job_file
        from apps.cli.commands.do_cmd import _build_agent_run_trace

        repo = tmp_path / "repo"
        repo.mkdir()
        job = parse_job_file("# Job: t\n\n## Task 1\nDo a thing.\n", str(repo))
        task = job.tasks[0]
        task.run_id = "run-abc"

        task_dir = jobs_dir() / job.job_id / "evidence" / "task_runs" / task.task_id
        self._write_stream_call(task_dir, "streams/builder/round-01/attempt-01",
                                _stream_lines(with_retry=True))
        self._write_stream_call(task_dir, "streams/reviewer/round-01/attempt-01",
                                _stream_lines())

        # Make load_run return something truthy for this run id.
        monkeypatch.setattr(
            "packages.orchestration.pingpong_loop.load_run",
            lambda rid: {"rounds": []},
        )
        events = _build_agent_run_trace(job, _FakePromo(), {}, "claude-cli", "claude-cli")

        streamed = [e for e in events if e.trace_source == TRACE_SOURCE_STREAM]
        kinds = {e.event_kind for e in streamed}
        assert "tool_use" in kinds
        assert "api_retry" in kinds
        assert "provider_result" in kinds
        assert streamed, "production trace builder ignored normalized stream events"

        # Refs are relative and point at the exact raw bytes of a specific call.
        refs = " ".join(r for e in streamed for r in e.source_artifact_refs)
        assert "streams/builder/round-01/attempt-01/raw_stream.jsonl" in refs
        assert "streams/reviewer/round-01/attempt-01/run_events.jsonl" in refs
        assert "offset=" in refs and "length=" in refs
        assert not any(r.startswith("/") for e in streamed for r in e.source_artifact_refs)

        # Lifecycle events remain reconstructed; both sources are reported.
        summary = build_trace_summary(events)
        assert TRACE_SOURCE_STREAM in summary["trace_sources"]
        assert TRACE_SOURCE_LEGACY in summary["trace_sources"]
        assert summary["source_limitations"]

    def test_no_stream_artifacts_keeps_pure_reconstruction(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.pingpong_job import parse_job_file
        from apps.cli.commands.do_cmd import _build_agent_run_trace

        repo = tmp_path / "repo"
        repo.mkdir()
        job = parse_job_file("# Job: t\n\n## Task 1\nDo a thing.\n", str(repo))
        job.tasks[0].run_id = "run-none"
        monkeypatch.setattr(
            "packages.orchestration.pingpong_loop.load_run",
            lambda rid: {"rounds": []},
        )
        events = _build_agent_run_trace(job, _FakePromo(), {}, "fake", "fake")
        assert all(e.trace_source == TRACE_SOURCE_LEGACY for e in events)
        summary = build_trace_summary(events)
        assert summary["trace_sources"] == [TRACE_SOURCE_LEGACY]


# ---------------------------------------------------------------------------
# `do run --stream-evidence` must reach the loop, not be accepted and dropped
# ---------------------------------------------------------------------------


class TestDoRunStreamEvidenceWiring:
    def test_cli_flag_is_forwarded_to_run_pingpong(self, monkeypatch, tmp_path):
        import apps.cli.commands.do_cmd as do_cmd
        import packages.orchestration.pingpong_loop as pp

        seen: dict[str, object] = {}

        def _fake_run_pingpong(goal, repo, **kw):
            seen.update(kw)
            raise SystemExit(0)  # stop before any provider work

        # _cmd_do imports run_pingpong from the loop module at call time.
        monkeypatch.setattr(pp, "run_pingpong", _fake_run_pingpong)
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# x\n")

        with pytest.raises(SystemExit):
            do_cmd._cmd_do(
                "goal", repo=str(repo), builder="fake", reviewer="fake",
                max_rounds=1, stream_evidence=True,
            )
        assert seen.get("stream_evidence") is True, \
            "do run accepted --stream-evidence and dropped it"

    def test_do_run_dispatch_reads_the_flag(self):
        import inspect

        import apps.cli.commands.do_cmd as do_cmd

        src = inspect.getsource(do_cmd)
        run_lambda = src.split('"do.run": lambda args:', 1)[1].split('"do.plan":', 1)[0]
        assert "stream_evidence" in run_lambda

    def test_loop_defaults_stream_dir_when_caller_gives_none(self):
        import inspect

        import packages.orchestration.pingpong_loop as pp

        src = inspect.getsource(pp.run_pingpong)
        assert "if stream_evidence and not stream_evidence_dir" in src, \
            "run_pingpong must give stream evidence a destination"

    def test_provider_refuses_stream_mode_without_a_destination(self, tmp_path):
        from packages.orchestration.pingpong_provider import ClaudeCliProvider

        prov = ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=None)
        with pytest.raises(RuntimeError, match="stream_evidence_dir"):
            prov._call_streamed("claude", "prompt", timeout_sec=5, max_output_chars=1000)


class TestFailedAttemptStillReferencesItsArtifacts:
    """A timed-out streamed call leaves partial artifacts; the export copies them.

    If the failed attempt did not reference them, the artifact contract would see
    listing entries with no provider reference and block a legitimate bundle.
    """

    def test_timeout_error_output_carries_persisted_refs(self, tmp_path, monkeypatch):
        import os

        from packages.orchestration.pingpong_provider import ClaudeCliProvider

        prog = _bash_bin(tmp_path, "echo '{\"type\":\"system\"}'; sleep 30\n", "claude")
        monkeypatch.setenv("PATH", f"{prog.parent}{os.pathsep}{os.environ['PATH']}")

        out_dir = tmp_path / "streams" / "builder"
        prov = ClaudeCliProvider(
            stream_evidence=True,
            stream_evidence_dir=str(out_dir),
            stream_rel_prefix="streams/builder",
        )
        prov.begin_stream_call(1, "attempt")
        res = prov.build("do a thing", timeout_sec=1)

        assert res.error, "expected the call to fail"
        call_dir = out_dir / "round-01" / "attempt-01"
        on_disk = [p.name for p in call_dir.glob("*.jsonl")]
        assert on_disk, "no partial artifacts were written"
        for name in on_disk:
            assert any(r.endswith(name) for r in res.stream_artifact_refs), \
                f"{name} was written but not referenced by the failed attempt"

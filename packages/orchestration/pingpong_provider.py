"""Ping-pong provider adapters — Builder and Reviewer providers.

Defines the provider protocol and concrete implementations:
  - FakeProvider: deterministic, for automated tests
  - ClaudeProvider: real Claude API calls via anthropic SDK

No provider executes unless explicitly selected via CLI.
No secrets in logs or reports.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from packages.orchestration.token_actuals import parse_cli_result, parse_cli_result_detailed
from packages.orchestration.stream_evidence import StreamCapReached as _StreamCapReached

# ---------------------------------------------------------------------------
# Provider output contracts
# ---------------------------------------------------------------------------

@dataclass
class BuilderOutput:
    """Structured output from a Builder provider."""
    summary: str = ""
    files_changed: list[str] = field(default_factory=list)
    commands_suggested: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    raw_text: str = ""
    error: str = ""
    provider: str = ""
    duration_ms: int = 0
    tokens_used: int = 0
    # Measured provider usage (input/output/cache/cost/session_id/parse_source)
    # when the CLI exposed a JSON usage block; None when only estimates exist.
    usage_actuals: dict[str, Any] | None = None
    actual_missing_reason: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)


@dataclass
class ReviewFinding:
    """Single reviewer finding."""
    id: str = ""
    severity: str = "medium"  # blocker, high, medium, low
    file: str = ""
    summary: str = ""
    details: str = ""
    required_fix: str = ""


@dataclass
class ReviewerOutput:
    """Structured output from a Reviewer provider."""
    verdict: str = "blocked"  # pass, fail, needs_repair, blocked
    findings: list[ReviewFinding] = field(default_factory=list)
    confidence: str = "low"  # low, medium, high
    summary: str = ""
    raw_text: str = ""
    error: str = ""
    provider: str = ""
    duration_ms: int = 0
    tokens_used: int = 0
    parse_retried: bool = False
    parse_retry_recovered: bool = False
    original_verdict: str = ""  # set when verdict was normalized
    verdict_normalized: bool = False
    # Measured provider usage (see BuilderOutput.usage_actuals); None when
    # only character-heuristic estimates are available.
    usage_actuals: dict[str, Any] | None = None
    actual_missing_reason: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Provider protocol
# ---------------------------------------------------------------------------

class PingPongProvider(Protocol):
    """Protocol for Builder/Reviewer providers."""

    @property
    def name(self) -> str: ...

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput: ...

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput: ...


# ---------------------------------------------------------------------------
# Fake provider (deterministic, for tests)
# ---------------------------------------------------------------------------

class FakeProvider:
    """Deterministic fake provider for automated testing.

    Round 1: Builder makes changes, Reviewer finds issues.
    Round 2: Builder repairs, Reviewer passes.
    Configurable via constructor for different test scenarios.
    """

    def __init__(
        self,
        *,
        builder_files: list[str] | None = None,
        fail_on_round: int = 1,
        pass_on_round: int = 2,
        max_rounds_before_block: int = 99,
        builder_error: str = "",
        reviewer_error: str = "",
        malformed_review: bool = False,
        malformed_review_recoverable: bool = False,
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._fail_round = fail_on_round
        self._pass_round = pass_on_round
        self._max_block = max_rounds_before_block
        self._builder_error = builder_error
        self._reviewer_error = reviewer_error
        self._malformed_review = malformed_review
        self._malformed_review_recoverable = malformed_review_recoverable
        self._build_count = 0
        self._review_count = 0

    @property
    def name(self) -> str:
        return "fake"

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
        self._build_count += 1
        if self._builder_error:
            return BuilderOutput(
                error=self._builder_error,
                provider="fake",
            )
        is_repair = self._build_count > 1
        return BuilderOutput(
            summary=f"{'Repair' if is_repair else 'Initial'} changes (round {self._build_count})",
            files_changed=list(self._builder_files),
            commands_suggested=[],
            assumptions=["Minimal changes only"],
            provider="fake",
            duration_ms=50,
            tokens_used=100,
        )

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        self._review_count += 1
        if self._reviewer_error:
            return ReviewerOutput(
                error=self._reviewer_error,
                provider="fake",
            )
        if self._malformed_review:
            return ReviewerOutput(
                verdict="",
                raw_text="not valid json {{{",
                error="malformed_output: no JSON found in reviewer response",
                provider="fake",
            )
        if self._malformed_review_recoverable and self._review_count == 1:
            return ReviewerOutput(
                verdict="",
                raw_text="Here is my review:\n{bad json",
                error="malformed_output: JSON parse error",
                provider="fake",
            )
        if self._review_count >= self._max_block:
            return ReviewerOutput(
                verdict="blocked",
                summary="Max rounds reached",
                provider="fake",
            )
        if self._review_count >= self._pass_round:
            return ReviewerOutput(
                verdict="pass",
                confidence="high",
                summary="All changes look correct after repair.",
                provider="fake",
                duration_ms=30,
                tokens_used=80,
            )
        # Findings on early rounds
        return ReviewerOutput(
            verdict="needs_repair",
            findings=[
                ReviewFinding(
                    id=f"R-{self._review_count:04d}",
                    severity="medium",
                    file=self._builder_files[0] if self._builder_files else "",
                    summary="Missing verification note",
                    details="The change is incomplete — add a verification note.",
                    required_fix="Add a verification note at the end of the file.",
                ),
            ],
            confidence="medium",
            summary=f"Found 1 issue in round {self._review_count}.",
            provider="fake",
            duration_ms=30,
            tokens_used=80,
        )


# ---------------------------------------------------------------------------
# Claude provider (real API calls)
# ---------------------------------------------------------------------------

_REVIEWER_JSON_SCHEMA = """\
Return ONLY valid JSON. No markdown. No code fence. No explanation outside JSON.
Your entire response must be exactly one JSON object with this structure:

{"verdict":"pass","findings":[],"confidence":"high","summary":"All changes correct."}

Fields:
- verdict: exactly one of "pass", "fail", "needs_repair", "blocked"
- findings: array of objects, each with "id", "severity" (blocker|high|medium|low), "file", "summary", "required_fix"
- confidence: "low", "medium", or "high"
- summary: one sentence

IMPORTANT: Output ONLY the JSON object. No other text.
"""

_REVIEWER_RETRY_PROMPT = """\
Your previous response was not valid JSON. Here is what you returned (excerpt):

{excerpt}

Return ONLY valid JSON with this exact shape:
{{"verdict":"pass|fail|needs_repair|blocked","findings":[],"confidence":"high","summary":"..."}}

No markdown. No code fence. No explanation. ONLY the JSON object.
"""


class ClaudeProvider:
    """Real Claude API provider via anthropic SDK.

    Requires ANTHROPIC_API_KEY environment variable.
    Never logs API keys. Timeouts required.
    """

    def __init__(
        self,
        *,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
    ) -> None:
        self._model = model
        self._max_tokens = max_tokens
        self._client: Any = None

    @property
    def name(self) -> str:
        return "claude"

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set. "
                "Set it to use --builder claude or --reviewer claude."
            )
        try:
            import anthropic
        except ImportError:
            raise RuntimeError(
                "anthropic package not installed. "
                "Install with: pip install anthropic"
            )
        self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def _call(self, prompt: str, *, timeout_sec: int, max_output_chars: int) -> tuple[str, int, int]:
        """Call Claude API. Returns (text, duration_ms, tokens_used)."""
        client = self._get_client()
        start = time.monotonic()
        response = client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=[{"role": "user", "content": prompt}],
            timeout=float(timeout_sec),
        )
        elapsed_ms = int((time.monotonic() - start) * 1000)
        text = ""
        for block in response.content:
            if hasattr(block, "text"):
                text += block.text
        tokens = getattr(response.usage, "output_tokens", 0)
        # Cap output
        if len(text) > max_output_chars:
            text = text[:max_output_chars] + "\n[OUTPUT TRUNCATED]"
        return text, elapsed_ms, tokens

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
        try:
            text, dur, tokens = self._call(
                prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            # Parse builder output — look for structured sections
            files = []
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("- ") and "/" in stripped:
                    candidate = stripped[2:].split()[0].strip("`")
                    if "." in candidate:
                        files.append(candidate)
            return BuilderOutput(
                summary=text[:500],
                files_changed=files,
                raw_text=text,
                provider="claude",
                duration_ms=dur,
                tokens_used=tokens,
                actual_missing_reason="provider_actuals_unavailable",
            )
        except Exception as exc:
            return BuilderOutput(
                error=f"provider_error: {type(exc).__name__}",
                provider="claude",
                actual_missing_reason="provider_error",
            )

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        full_prompt = prompt + "\n\n" + _REVIEWER_JSON_SCHEMA
        try:
            text, dur, tokens = self._call(
                full_prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            out = _parse_reviewer_json(text, dur, tokens)
            out.actual_missing_reason = "provider_actuals_unavailable"
            return out
        except Exception as exc:
            return ReviewerOutput(
                error=f"provider_error: {type(exc).__name__}",
                provider="claude",
                actual_missing_reason="provider_error",
            )


def _unwrap_envelope(data: dict) -> dict:
    """Unwrap common Claude CLI JSON envelope formats.

    Handles: direct reviewer JSON, {"result": {...}}, {"content": {...}},
    {"message": {...}}, {"text": "json_string"}.
    """
    if "verdict" in data:
        return data
    for key in ("result", "content", "message"):
        inner = data.get(key)
        if isinstance(inner, dict) and "verdict" in inner:
            return inner
    # text field containing JSON string
    text_field = data.get("text", "")
    if isinstance(text_field, str) and "{" in text_field:
        try:
            inner = json.loads(text_field[text_field.find("{"):text_field.rfind("}") + 1])
            if isinstance(inner, dict) and "verdict" in inner:
                return inner
        except (json.JSONDecodeError, ValueError):
            pass
    return data


def normalize_reviewer_verdict(out: ReviewerOutput) -> ReviewerOutput:
    """Normalize an incoherent ``pass`` + findings verdict.

    A reviewer that returns ``verdict="pass"`` while still reporting findings is
    internally inconsistent: the findings represent unresolved issues. Treating
    this as a plain pass would let those findings slip through unreviewed, while
    blocking it as ``review_inconsistent`` prevents the repair loop from ever
    addressing them.

    Instead, route the output back through review: the verdict is normalized to
    ``needs_repair`` (the verdict that triggers Remedy's existing repair loop —
    i.e. the findings are sent for a further review/repair pass rather than
    silently passing). The original verdict is preserved on ``original_verdict``
    for the audit trail. Mutates and returns ``out``.
    """
    if out.verdict == "pass" and out.findings:
        out.original_verdict = out.verdict
        out.verdict = "needs_repair"
        out.verdict_normalized = True
        note = (
            f"verdict normalized pass->needs_repair: reviewer reported "
            f"{len(out.findings)} finding(s) alongside a pass verdict; "
            f"routing findings to review/repair instead of passing"
        )
        out.summary = f"{out.summary} [{note}]" if out.summary else note
    return out


def _parse_reviewer_json(
    text: str, duration_ms: int, tokens_used: int, *, provider: str = "claude",
) -> ReviewerOutput:
    """Parse reviewer JSON from Claude response. Block on parse failure."""
    # Strip markdown code fences if present
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        # Remove first line (```json or ```) and last line (```)
        inner_lines = []
        started = False
        for line in lines:
            if not started:
                started = True
                continue
            if line.strip() == "```":
                break
            inner_lines.append(line)
        if inner_lines:
            stripped = "\n".join(inner_lines)

    json_start = stripped.find("{")
    json_end = stripped.rfind("}") + 1
    if json_start < 0 or json_end <= json_start:
        return ReviewerOutput(
            verdict="blocked",
            error="malformed_output: no JSON found in reviewer response",
            raw_text=text[:500],
            provider=provider,
            duration_ms=duration_ms,
            tokens_used=tokens_used,
        )
    try:
        data = json.loads(stripped[json_start:json_end])
    except json.JSONDecodeError as exc:
        return ReviewerOutput(
            verdict="blocked",
            error=f"malformed_output: JSON parse error: {exc}",
            raw_text=text[:500],
            provider=provider,
            duration_ms=duration_ms,
            tokens_used=tokens_used,
        )

    # Unwrap envelope formats
    data = _unwrap_envelope(data)

    verdict = data.get("verdict", "")
    if verdict not in ("pass", "fail", "needs_repair", "blocked"):
        return ReviewerOutput(
            verdict="blocked",
            error=f"malformed_output: invalid verdict '{verdict}'",
            raw_text=text[:500],
            provider=provider,
            duration_ms=duration_ms,
            tokens_used=tokens_used,
        )

    findings = []
    for f in data.get("findings", []):
        findings.append(ReviewFinding(
            id=f.get("id", ""),
            severity=f.get("severity", "medium"),
            file=f.get("file", ""),
            summary=f.get("summary", ""),
            details=f.get("details", ""),
            required_fix=f.get("required_fix", ""),
        ))

    return normalize_reviewer_verdict(ReviewerOutput(
        verdict=verdict,
        findings=findings,
        confidence=data.get("confidence", "medium"),
        summary=data.get("summary", ""),
        provider=provider,
        duration_ms=duration_ms,
        tokens_used=tokens_used,
    ))


# ---------------------------------------------------------------------------
# Claude CLI provider (local `claude -p` subprocess)
# ---------------------------------------------------------------------------

_VALID_CLI_WRITE_MODES = frozenset({"none", "allowed-tools", "dangerous-skip"})

_ALLOWED_TOOLS_ARGS = ["--allowedTools", "Edit,Write,MultiEdit"]
_DANGEROUS_SKIP_ARGS = ["--dangerously-skip-permissions"]


def _extract_cli_result_text(raw: str) -> str:
    """Extract Builder/Reviewer text from claude CLI stdout, Usage-independent.

    A valid JSON envelope's ``result`` field is authoritative text whether or
    not a Usage block is present. Non-JSON stdout (older CLI, plain text) falls
    back to the raw string unchanged, preserving raw-text support.
    """
    try:
        payload = json.loads(raw)
    except (ValueError, TypeError):
        return raw
    if isinstance(payload, dict) and "result" in payload:
        result_field = payload.get("result")
        if isinstance(result_field, str):
            return result_field
    return raw


def build_claude_cli_args(
    claude_path: str,
    prompt: str,
    *,
    write_mode: str = "none",
    model: str = "",
    stream_evidence: bool = False,
) -> list[str]:
    """Build safe CLI argv for claude invocation.

    write_mode:
      none: no write tools (reviewer mode, or builder without permission)
      allowed-tools: --allowedTools Edit,Write,MultiEdit
      dangerous-skip: --dangerously-skip-permissions (explicit opt-in only)
    model: if non-empty, passed as --model <model> to claude CLI.
    stream_evidence: opt-in F004 mode. Uses ``--output-format stream-json``
      (which the CLI requires ``--verbose`` for in print mode). The DEFAULT
      remains ``--output-format json`` — the accepted F003 behaviour.
    """
    if stream_evidence:
        argv = [claude_path, "-p", prompt, "--output-format", "stream-json", "--verbose"]
    else:
        argv = [claude_path, "-p", prompt, "--output-format", "json"]
    if model:
        argv.extend(["--model", model])
    if write_mode == "allowed-tools":
        argv.extend(_ALLOWED_TOOLS_ARGS)
    elif write_mode == "dangerous-skip":
        argv.extend(_DANGEROUS_SKIP_ARGS)
    return argv


class ClaudeCliProvider:
    """Provider using local `claude` CLI via `claude -p "<prompt>"`.

    Requires `claude` binary on PATH. No API key needed (CLI handles auth).
    Runs as subprocess with timeout and output cap.
    write_mode controls file edit permissions (none/allowed-tools/dangerous-skip).
    """

    def __init__(
        self,
        *,
        cwd: str | None = None,
        write_mode: str = "none",
        max_tokens: int = 4096,
        model: str = "",
        stream_evidence: bool = False,
        stream_evidence_dir: str | None = None,
        stream_rel_prefix: str = "",
        stream_max_bytes: int | None = None,
    ) -> None:
        self._cwd = cwd
        self._write_mode = write_mode
        self._max_tokens = max_tokens
        self._model = model
        self._claude_path: str | None = None
        self._cli_version: str | None = None
        self._cli_version_resolved: bool = False
        # F004 opt-in raw stream evidence. Default off: the F003 JSON path.
        self._stream_evidence = stream_evidence
        self._stream_evidence_dir = stream_evidence_dir
        self._stream_rel_prefix = stream_rel_prefix
        self._stream_max_bytes = stream_max_bytes
        self._last_stream_capture: Any = None
        # Every provider call gets its own directory, so an F001 retry, a
        # reviewer parse retry or a repair-round call can never overwrite an
        # earlier stream.
        self._stream_round = 1
        self._stream_kind = "attempt"
        self._stream_counters: dict[tuple[int, str], int] = {}
        self._last_stream_call_id = ""
        self._last_stream_refs: list[str] = []

    @property
    def stream_evidence(self) -> bool:
        return self._stream_evidence

    @property
    def last_stream_capture(self) -> Any:
        """Capture summary of the most recent streamed call (None when off)."""
        return self._last_stream_capture

    @property
    def last_stream_call_id(self) -> str:
        return self._last_stream_call_id

    @property
    def last_stream_artifact_refs(self) -> list[str]:
        return list(self._last_stream_refs)

    def begin_stream_call(self, round_no: int, kind: str = "attempt") -> None:
        """Declare the round and call kind for the next streamed provider call.

        ``kind`` is ``attempt`` for initial/transport-retry calls and
        ``parse-retry`` for a reviewer re-ask. The attempt index within a
        (round, kind) pair increments automatically, so nothing is overwritten.
        """
        self._stream_round = max(1, int(round_no or 1))
        self._stream_kind = kind or "attempt"

    def _persisted_stream_refs(self) -> list[str]:
        """Refs for artifacts this call actually wrote.

        A timed-out or non-zero-exit streamed call still leaves its partial
        raw_stream.jsonl / run_events.jsonl behind, and the export copies them.
        The artifact contract requires the listing and the provider references to
        describe the same set, so a failed attempt must still reference what it
        produced instead of silently disowning it.
        """
        from pathlib import Path as _P

        if not self._stream_evidence or not self._stream_evidence_dir:
            return []
        call_id = self._last_stream_call_id
        if not call_id:
            return []
        prefix = self._stream_rel_prefix or ""
        rel = call_id[len(prefix) + 1:] if prefix and call_id.startswith(prefix) else call_id
        call_dir = _P(self._stream_evidence_dir) / rel
        return [r for r in (self._last_stream_refs or [])
                if (call_dir / _P(r).name).is_file()]

    def _allocate_stream_call_dir(self) -> str:
        from pathlib import Path as _P
        key = (self._stream_round, self._stream_kind)
        idx = self._stream_counters.get(key, 0) + 1
        self._stream_counters[key] = idx
        rel = f"round-{self._stream_round:02d}/{self._stream_kind}-{idx:02d}"
        prefix = self._stream_rel_prefix or ""
        self._last_stream_call_id = f"{prefix}/{rel}" if prefix else rel
        self._last_stream_refs = [
            f"{self._last_stream_call_id}/raw_stream.jsonl",
            f"{self._last_stream_call_id}/run_events.jsonl",
        ]
        return str(_P(self._stream_evidence_dir) / rel)

    @property
    def name(self) -> str:
        return "claude-cli"

    @property
    def write_mode(self) -> str:
        return self._write_mode

    @property
    def model(self) -> str:
        return self._model

    def _get_claude_path(self) -> str:
        if self._claude_path is not None:
            return self._claude_path
        path = shutil.which("claude")
        if not path:
            raise RuntimeError(
                "claude CLI not found on PATH. "
                "Install Claude Code CLI to use --builder claude-cli or --reviewer claude-cli."
            )
        self._claude_path = path
        return path

    def _resolve_version(self) -> str | None:
        """Return CLI version string, cached. Never raises."""
        if self._cli_version_resolved:
            return self._cli_version
        self._cli_version_resolved = True
        try:
            claude = self._get_claude_path()
            proc = subprocess.run(
                [claude, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                # Pinned like every other provider call: an unpinned probe runs in
                # the operator's cwd and any stray write lands in the repo root.
                cwd=self._cwd,
            )
            if proc.returncode == 0 and proc.stdout and proc.stdout.strip():
                self._cli_version = proc.stdout.strip()
        except Exception:
            pass
        return self._cli_version

    def _call_streamed(
        self, claude: str, prompt: str, *, timeout_sec: int, max_output_chars: int,
    ) -> tuple[str, int, int, dict[str, Any] | None, str]:
        """F004 opt-in path: run the CLI in stream-json and capture evidence.

        The stream is consumed incrementally, redacted before persistence, and
        written to ``raw_stream.jsonl`` / ``run_events.jsonl`` in the task
        evidence directory. Token accounting stays F003-compatible: the final
        ``result`` event's usage is the authoritative total.
        """
        from packages.orchestration.stream_evidence import (
            DEFAULT_MAX_BYTES,
            final_result_text,
            run_streamed_command,
            usage_actuals_from_events,
        )

        if not self._stream_evidence_dir:
            raise RuntimeError("stream evidence enabled but no stream_evidence_dir was provided")

        argv = build_claude_cli_args(
            claude, prompt, write_mode=self._write_mode, model=self._model,
            stream_evidence=True,
        )
        call_dir = self._allocate_stream_call_dir()
        run = run_streamed_command(
            argv, call_dir, cwd=self._cwd, timeout_sec=timeout_sec,
            max_bytes=self._stream_max_bytes or DEFAULT_MAX_BYTES,
        )
        self._last_stream_capture = run

        # A real wall-clock timeout is a normal provider timeout so the F001
        # retry policy can act on it exactly as in the JSON path.
        if run.timed_out:
            raise RuntimeError(f"claude CLI timed out after {timeout_sec}s")

        # A reached cap means we deliberately terminated the provider before it
        # finished. That is NOT a successful call and NOT a transport error: it
        # is an incomplete result with its own reason, so it is neither retried
        # as a timeout nor counted as a passing Builder/Reviewer response.
        if run.terminated_at_cap:
            raise _StreamCapReached(
                f"stream evidence cap reached after {run.capture.raw_bytes_written} bytes; "
                f"provider terminated before completion",
                capture=run,
            )

        if run.returncode != 0:
            raise RuntimeError(f"claude CLI exited {run.returncode}: {run.stderr_tail[:500]}")

        events = run.events
        if any(e.get("event_type") == "provider_error" for e in events):
            err = next(e for e in events if e.get("event_type") == "provider_error")
            raise RuntimeError(f"claude CLI stream reported an error: {err.get('error', '')[:300]}")

        usage_actuals, missing_reason = usage_actuals_from_events(
            events, cli_version=self._resolve_version(),
        )
        text = final_result_text(events, run.capture.raw_path)
        tokens = 0
        if usage_actuals is not None:
            tokens = usage_actuals["input_tokens"] + usage_actuals["output_tokens"]
        if len(text) > max_output_chars:
            text = text[:max_output_chars] + "\n[OUTPUT TRUNCATED]"
        return text, run.duration_ms, tokens, usage_actuals, missing_reason

    def _call(
        self, prompt: str, *, timeout_sec: int, max_output_chars: int,
    ) -> tuple[str, int, int, dict[str, Any] | None, str]:
        """Call claude CLI. Returns (text, duration_ms, tokens_used, usage_actuals, actual_missing_reason).

        The CLI is invoked with ``--output-format json``. When the JSON parses
        into a usage block, ``text`` is taken from the ``result`` field and the
        measured token usage is returned. When parsing fails (non-JSON output,
        older CLI, no usage block), it falls back to the raw stdout as text with
        ``tokens_used=0`` and ``usage_actuals=None``.
        """
        claude = self._get_claude_path()
        if self._stream_evidence:
            return self._call_streamed(
                claude, prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
        argv = build_claude_cli_args(claude, prompt, write_mode=self._write_mode, model=self._model)
        start = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                cwd=self._cwd,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"claude CLI timed out after {timeout_sec}s")
        elapsed_ms = int((time.monotonic() - start) * 1000)
        if proc.returncode != 0:
            stderr = proc.stderr[:500] if proc.stderr else ""
            raise RuntimeError(f"claude CLI exited {proc.returncode}: {stderr}")
        raw = proc.stdout or ""

        actuals, parse_reason = parse_cli_result_detailed(raw)
        resolved_version = self._resolve_version()

        # is_error is an honest provider error regardless of any result text.
        if parse_reason == "is_error":
            raise RuntimeError("claude CLI reported is_error=true")

        # Result parsing is INDEPENDENT of Usage parsing. A valid JSON envelope
        # carrying a usable ``result`` is authoritative Builder/Reviewer text
        # even when the Usage block is missing or incomplete; Usage
        # unavailability only downgrades token accounting (usage_actuals=None,
        # actual_missing_reason set), it never invalidates a valid result.
        text = _extract_cli_result_text(raw)

        if actuals is not None:
            tokens = actuals.input_tokens + actuals.output_tokens
            cli_ver = actuals.cli_version or resolved_version
            usage_actuals: dict[str, Any] | None = {
                "input_tokens": actuals.input_tokens,
                "output_tokens": actuals.output_tokens,
                "cache_read": actuals.cache_read,
                "cache_creation": actuals.cache_creation,
                "total_cost_usd": actuals.total_cost_usd,
                "num_turns": actuals.num_turns,
                "duration_ms": actuals.duration_ms,
                "session_id": actuals.session_id,
                "cli_version": cli_ver,
                "parse_source": "claude_cli_json",
            }
            actual_missing_reason = ""
        else:
            tokens = 0
            usage_actuals = None
            actual_missing_reason = parse_reason

        if len(text) > max_output_chars:
            text = text[:max_output_chars] + "\n[OUTPUT TRUNCATED]"
        return text, elapsed_ms, tokens, usage_actuals, actual_missing_reason

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
        try:
            text, dur, tokens, usage, amr = self._call(
                prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            files = []
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("- ") and "/" in stripped:
                    candidate = stripped[2:].split()[0].strip("`")
                    if "." in candidate:
                        files.append(candidate)
            return BuilderOutput(
                summary=text[:500],
                files_changed=files,
                raw_text=text,
                provider="claude-cli",
                duration_ms=dur,
                tokens_used=tokens,
                usage_actuals=usage,
                actual_missing_reason=amr,
                stream_artifact_refs=self.last_stream_artifact_refs,
                stream_call_id=self._last_stream_call_id,
            )
        except _StreamCapReached as exc:
            return BuilderOutput(
                error=f"stream_cap_reached: {exc}",
                provider="claude-cli",
                actual_missing_reason="stream_cap_reached",
                incomplete=True,
                stream_cap_reached=True,
                stream_artifact_refs=self.last_stream_artifact_refs,
                stream_call_id=self._last_stream_call_id,
            )
        except Exception as exc:
            return BuilderOutput(
                error=f"provider_error: {type(exc).__name__}: {exc}",
                provider="claude-cli",
                actual_missing_reason="provider_error",
                stream_artifact_refs=self._persisted_stream_refs(),
                stream_call_id=self._last_stream_call_id,
            )

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        full_prompt = prompt + "\n\n" + _REVIEWER_JSON_SCHEMA
        try:
            text, dur, tokens, usage, amr = self._call(
                full_prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            out = _parse_reviewer_json(text, dur, tokens, provider="claude-cli")
            out.usage_actuals = usage
            out.actual_missing_reason = amr
            out.stream_artifact_refs = self.last_stream_artifact_refs
            out.stream_call_id = self._last_stream_call_id
            return out
        except _StreamCapReached as exc:
            return ReviewerOutput(
                error=f"stream_cap_reached: {exc}",
                provider="claude-cli",
                actual_missing_reason="stream_cap_reached",
                incomplete=True,
                stream_cap_reached=True,
                stream_artifact_refs=self.last_stream_artifact_refs,
                stream_call_id=self._last_stream_call_id,
            )
        except Exception as exc:
            return ReviewerOutput(
                error=f"provider_error: {type(exc).__name__}: {exc}",
                provider="claude-cli",
                actual_missing_reason="provider_error",
                stream_artifact_refs=self._persisted_stream_refs(),
                stream_call_id=self._last_stream_call_id,
            )


# ---------------------------------------------------------------------------
# Provider factory
# ---------------------------------------------------------------------------

def create_provider(name: str, *, model: str = "") -> PingPongProvider:
    """Create a provider by name. Raises RuntimeError if unavailable."""
    if name == "fake":
        return FakeProvider()
    if name == "claude":
        return ClaudeProvider(model=model) if model else ClaudeProvider()
    if name == "claude-cli":
        return ClaudeCliProvider(model=model)
    raise RuntimeError(f"Unknown provider: {name!r}. Available: fake, claude, claude-cli")

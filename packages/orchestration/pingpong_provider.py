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
            )
        except Exception as exc:
            return BuilderOutput(
                error=f"provider_error: {type(exc).__name__}",
                provider="claude",
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
            return _parse_reviewer_json(text, dur, tokens)
        except Exception as exc:
            return ReviewerOutput(
                error=f"provider_error: {type(exc).__name__}",
                provider="claude",
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


def build_claude_cli_args(
    claude_path: str,
    prompt: str,
    *,
    write_mode: str = "none",
    model: str = "",
) -> list[str]:
    """Build safe CLI argv for claude invocation.

    write_mode:
      none: no write tools (reviewer mode, or builder without permission)
      allowed-tools: --allowedTools Edit,Write,MultiEdit
      dangerous-skip: --dangerously-skip-permissions (explicit opt-in only)
    model: if non-empty, passed as --model <model> to claude CLI.
    """
    argv = [claude_path, "-p", prompt, "--output-format", "text"]
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
    ) -> None:
        self._cwd = cwd
        self._write_mode = write_mode
        self._max_tokens = max_tokens
        self._model = model
        self._claude_path: str | None = None

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

    def _call(self, prompt: str, *, timeout_sec: int, max_output_chars: int) -> tuple[str, int, int]:
        """Call claude CLI. Returns (text, duration_ms, tokens_used=0)."""
        claude = self._get_claude_path()
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
        text = proc.stdout or ""
        if len(text) > max_output_chars:
            text = text[:max_output_chars] + "\n[OUTPUT TRUNCATED]"
        return text, elapsed_ms, 0

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
            )
        except Exception as exc:
            return BuilderOutput(
                error=f"provider_error: {type(exc).__name__}: {exc}",
                provider="claude-cli",
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
            return _parse_reviewer_json(text, dur, tokens, provider="claude-cli")
        except Exception as exc:
            return ReviewerOutput(
                error=f"provider_error: {type(exc).__name__}: {exc}",
                provider="claude-cli",
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

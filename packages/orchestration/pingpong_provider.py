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
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._fail_round = fail_on_round
        self._pass_round = pass_on_round
        self._max_block = max_rounds_before_block
        self._builder_error = builder_error
        self._reviewer_error = reviewer_error
        self._malformed_review = malformed_review
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
                error="malformed_output",
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
Return your review as JSON with this exact structure:
{
  "verdict": "pass|fail|needs_repair|blocked",
  "findings": [
    {
      "id": "R-0001",
      "severity": "blocker|high|medium|low",
      "file": "optional/path",
      "summary": "short",
      "details": "clear explanation",
      "required_fix": "what builder must do"
    }
  ],
  "confidence": "low|medium|high",
  "summary": "human readable"
}
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


def _parse_reviewer_json(
    text: str, duration_ms: int, tokens_used: int, *, provider: str = "claude",
) -> ReviewerOutput:
    """Parse reviewer JSON from Claude response. Block on parse failure."""
    # Try to find JSON in the response
    json_start = text.find("{")
    json_end = text.rfind("}") + 1
    if json_start < 0 or json_end <= json_start:
        return ReviewerOutput(
            verdict="blocked",
            error="malformed_output: no JSON found in reviewer response",
            raw_text=text[:1000],
            provider=provider,
            duration_ms=duration_ms,
            tokens_used=tokens_used,
        )
    try:
        data = json.loads(text[json_start:json_end])
    except json.JSONDecodeError as exc:
        return ReviewerOutput(
            verdict="blocked",
            error=f"malformed_output: JSON parse error: {exc}",
            raw_text=text[:1000],
            provider=provider,
            duration_ms=duration_ms,
            tokens_used=tokens_used,
        )

    verdict = data.get("verdict", "")
    if verdict not in ("pass", "fail", "needs_repair", "blocked"):
        return ReviewerOutput(
            verdict="blocked",
            error=f"malformed_output: invalid verdict '{verdict}'",
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

    return ReviewerOutput(
        verdict=verdict,
        findings=findings,
        confidence=data.get("confidence", "medium"),
        summary=data.get("summary", ""),
        provider=provider,
        duration_ms=duration_ms,
        tokens_used=tokens_used,
    )


# ---------------------------------------------------------------------------
# Claude CLI provider (local `claude -p` subprocess)
# ---------------------------------------------------------------------------

class ClaudeCliProvider:
    """Provider using local `claude` CLI via `claude -p "<prompt>"`.

    Requires `claude` binary on PATH. No API key needed (CLI handles auth).
    Runs as subprocess with timeout and output cap.
    """

    def __init__(
        self,
        *,
        cwd: str | None = None,
        max_tokens: int = 4096,
    ) -> None:
        self._cwd = cwd
        self._max_tokens = max_tokens
        self._claude_path: str | None = None

    @property
    def name(self) -> str:
        return "claude-cli"

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
        start = time.monotonic()
        try:
            proc = subprocess.run(
                [claude, "-p", prompt, "--output-format", "text"],
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

def create_provider(name: str) -> PingPongProvider:
    """Create a provider by name. Raises RuntimeError if unavailable."""
    if name == "fake":
        return FakeProvider()
    if name == "claude":
        return ClaudeProvider()
    if name == "claude-cli":
        return ClaudeCliProvider()
    raise RuntimeError(f"Unknown provider: {name!r}. Available: fake, claude, claude-cli")

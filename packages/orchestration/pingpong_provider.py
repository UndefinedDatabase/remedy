"""Ping-pong provider adapters — Builder and Reviewer providers.

Defines the provider protocol and concrete implementations:
  - FakeProvider: deterministic, for automated tests
  - ClaudeProvider: real Claude API calls via anthropic SDK

No provider executes unless explicitly selected via CLI.
No secrets in logs or reports.
"""
from __future__ import annotations

import json
import locale
import os
import shutil
import signal
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from packages.orchestration.call_identity import (
    canonical_call_number,
    prepare_call_input,
)
from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded
from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.schemas import (
    ReviewVerdict as _ReviewVerdictSchema,
)
from packages.orchestration.schemas import (
    schema_v_of as _schema_v_of,
)
from packages.orchestration.schemas import (
    to_json_schema_str as _to_json_schema_str,
)
from packages.orchestration.schemas import (
    validate_response as _validate_response,
)
from packages.orchestration.stream_evidence import StreamCapReached as _StreamCapReached
from packages.orchestration.structured_outputs import (
    build_schema_prompt as _build_schema_prompt,
)
from packages.orchestration.structured_outputs import (
    reviewer_structured_enabled as _reviewer_structured_enabled,
)
from packages.orchestration.token_actuals import (
    parse_cli_envelope as _parse_cli_envelope,
)
from packages.orchestration.token_actuals import (
    parse_cli_result_detailed,
)

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
    # F106 T001: honest resume bookkeeping — true only when this call
    # actually resumed a prior session; the ref it resumed, "" otherwise.
    resume_used: bool = False
    resume_session_ref: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    prepared_input: Any = None  # F012: fingerprint of the EXACT transport request


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
    # F005 structured outputs: the schema version this verdict was validated
    # against ("" for the legacy free-text path), and the concise validation
    # hint carried into the single parse retry when validation failed.
    schema_v: str = ""
    parse_hint: str = ""
    # Stable machine error class ("" | "parse" | "config" | "provider_error").
    # A validation failure is "parse" so evidence classifies it without parsing
    # the human-readable ``error`` text.
    error_class: str = ""
    # Measured provider usage (see BuilderOutput.usage_actuals); None when
    # only character-heuristic estimates are available.
    usage_actuals: dict[str, Any] | None = None
    actual_missing_reason: str = ""
    # F106 T001: honest resume bookkeeping — true only when this call
    # actually resumed a prior session; the ref it resumed, "" otherwise.
    resume_used: bool = False
    resume_session_ref: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    prepared_input: Any = None  # F012: fingerprint of the EXACT transport request


# ---------------------------------------------------------------------------
# Provider protocol
# ---------------------------------------------------------------------------

class PingPongProvider(Protocol):
    """Protocol for Builder/Reviewer providers."""

    @property
    def name(self) -> str: ...

    @property
    def supports_resume(self) -> bool: ...

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput: ...

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
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
        supports_resume: bool = False,
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._supports_resume = supports_resume
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

    @property
    def supports_resume(self) -> bool:
        return self._supports_resume

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
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
            prepared_input=prepare_call_input(
                prompt=prompt, model="fake", mode="fake",
                options={"max_output_chars": max_output_chars}),
        )

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
        out.prepared_input = prepare_call_input(
            prompt=prompt, model="fake", mode="fake",
            options={"max_output_chars": max_output_chars})
        return out

    def _review_impl(
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

#: The direct-API provider's built-in default model. Resolved from the single
#: alias table (packages/orchestration/model_aliases.py) so no dated model id
#: is spelled out here; an upgrade repoints the alias, not this file.
_DEFAULT_CLAUDE_MODEL = resolve_model_alias("claude-workhorse")

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
        model: str = _DEFAULT_CLAUDE_MODEL,
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
        # F012: the builder prompt is sent verbatim — fingerprint the exact bytes.
        _pi = prepare_call_input(
            prompt=prompt, model=self._model, mode="api-legacy",
            options={"max_tokens": self._max_tokens})
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
                prepared_input=_pi,
            )
        except Exception as exc:
            return BuilderOutput(
                error=f"provider_error: {type(exc).__name__}",
                provider="claude",
                actual_missing_reason="provider_error",
                prepared_input=_pi,
            )

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        structured = _reviewer_structured_enabled()
        full_prompt = (
            _build_schema_prompt(_ReviewVerdictSchema, prompt)
            if structured else prompt + "\n\n" + _REVIEWER_JSON_SCHEMA
        )
        # F012: the schema is embedded IN ``full_prompt`` for the API path, so fingerprint the
        # exact bytes sent (``full_prompt``), NOT the caller's raw ``prompt``.
        _pi = prepare_call_input(
            prompt=full_prompt, model=self._model,
            mode="api-structured" if structured else "api-legacy",
            options={"max_tokens": self._max_tokens})
        try:
            text, dur, tokens = self._call(
                full_prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            out = (
                _parse_reviewer_structured(text, dur, tokens)
                if structured else _parse_reviewer_json(text, dur, tokens)
            )
            out.actual_missing_reason = "provider_actuals_unavailable"
            out.prepared_input = _pi
            return out
        except Exception as exc:
            return ReviewerOutput(
                error=f"provider_error: {type(exc).__name__}",
                provider="claude",
                actual_missing_reason="provider_error",
                prepared_input=_pi,
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


def _parse_reviewer_structured(
    text: str, duration_ms: int, tokens_used: int, *, provider: str = "claude",
) -> ReviewerOutput:
    """Validate a reviewer response against the F005 ReviewVerdict schema.

    On success the validated model is mapped to a ReviewerOutput carrying its
    ``schema_v``. On failure the result is a classified parse error
    (``malformed_output:`` + concise hint) so the loop's single parse retry
    fires; the hint is carried in ``parse_hint`` for the retry prompt. Schema
    mode never falls back to the free-text parser.
    """
    res = _validate_response(_ReviewVerdictSchema, text)
    if not res.ok:
        return ReviewerOutput(
            verdict="blocked",
            error=f"malformed_output: {res.hint}",
            error_class=res.error_class,  # "parse"
            parse_hint=res.hint,
            schema_v=_schema_v_of(_ReviewVerdictSchema),
            raw_text=text[:500],
            provider=provider,
            duration_ms=duration_ms,
            tokens_used=tokens_used,
        )
    v = res.value
    return normalize_reviewer_verdict(ReviewerOutput(
        verdict=v.verdict,
        findings=[
            ReviewFinding(
                id=f.id, severity=f.severity, file=f.file,
                summary=f.summary, details="", required_fix=f.required_fix,
            )
            for f in v.findings
        ],
        confidence=v.confidence,
        summary=v.summary,
        provider=provider,
        duration_ms=duration_ms,
        tokens_used=tokens_used,
        schema_v=v.schema_v,
    ))


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


def _looks_like_unknown_json_schema_option(stderr: str) -> bool:
    """Heuristic: did the CLI reject ``--json-schema`` as unknown, pre-execution?

    Matches the usual argument-parser phrasings without over-matching a normal
    provider error that merely mentions the flag.
    """
    s = (stderr or "").lower()
    if "--json-schema" not in s and "json-schema" not in s and "json_schema" not in s:
        return False
    markers = ("unknown option", "unrecognized option", "unrecognised option",
               "unknown argument", "unexpected argument", "invalid option",
               "no such option", "unknown flag")
    return any(m in s for m in markers)


def _usage_actuals_dict(actuals: Any, cli_ver: str | None) -> dict[str, Any]:
    """Shape a UsageActuals into the provider's usage_actuals dict."""
    return {
        "input_tokens": actuals.input_tokens,
        "output_tokens": actuals.output_tokens,
        "cache_read": actuals.cache_read,
        "cache_creation": actuals.cache_creation,
        "total_cost_usd": actuals.total_cost_usd,
        "num_turns": actuals.num_turns,
        "duration_ms": actuals.duration_ms,
        "session_id": actuals.session_id,
        "cli_version": actuals.cli_version or cli_ver,
        "parse_source": "claude_cli_json",
    }


class _StreamNonZeroExit(RuntimeError):
    """The streamed CLI exited nonzero, carrying what it still produced.

    Claude can emit a valid final result envelope (e.g. a native structured-output
    failure, with Usage/cost) and THEN exit nonzero. The envelope is authoritative
    for classification, so it travels with the error instead of being discarded.
    Subclasses RuntimeError, so every non-structured caller behaves exactly as
    before (provider error).
    """

    def __init__(
        self,
        message: str,
        *,
        returncode: int,
        stderr_tail: str = "",
        final: Any = None,
        usage_actuals: dict[str, Any] | None = None,
        tokens: int = 0,
        duration_ms: int = 0,
    ) -> None:
        super().__init__(message)
        self.returncode = returncode
        self.stderr_tail = stderr_tail
        self.final = final
        self.usage_actuals = usage_actuals
        self.tokens = tokens
        self.duration_ms = duration_ms


@dataclass
class StructuredCliOutcome:
    """Result of one native structured Claude CLI reviewer call.

    Parsed once from the envelope so the caller never re-parses the JSON.
    """
    value_text: str = ""          # compact JSON of structured_output ("" if none)
    duration_ms: int = 0
    tokens: int = 0
    usage_actuals: dict[str, Any] | None = None
    error_class: str = ""         # "" | "parse" | "config"
    error_detail: str = ""


def build_claude_cli_args(
    claude_path: str,
    prompt: str,
    *,
    write_mode: str = "none",
    model: str = "",
    stream_evidence: bool = False,
    json_schema: str = "",
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
    json_schema: F005 native structured output. When non-empty, passed as
      ``--json-schema <schema>`` so the provider enforces the schema itself
      instead of relying on prompt prose. Kept compact by the caller.
    """
    if stream_evidence:
        argv = [claude_path, "-p", prompt, "--output-format", "stream-json", "--verbose"]
    else:
        argv = [claude_path, "-p", prompt, "--output-format", "json"]
    if model:
        argv.extend(["--model", model])
    if json_schema:
        argv.extend(["--json-schema", json_schema])
    if write_mode == "allowed-tools":
        argv.extend(_ALLOWED_TOOLS_ARGS)
    elif write_mode == "dangerous-skip":
        argv.extend(_DANGEROUS_SKIP_ARGS)
    return argv

# F005 Finding 6: there is deliberately NO ``claude --help`` preflight. Claude
# Code's help does not list every supported flag, so its absence is not proof
# ``--json-schema`` is unsupported. Support is proven by the actual invocation;
# an unknown-option error from that invocation is classified ``config`` (see
# ``_looks_like_unknown_json_schema_option`` / ``_call_reviewer_structured``).


def _cli_exec_policy(timeout_sec: float, cwd: str | None) -> ExecGuardPolicy:
    """Stage-1 CLI-provider policy (F085 T002a) — only the limits this seam can prove.

    `output_cap_bytes` stays None on purpose: this seam parses the CLI's WHOLE JSON
    envelope, so a byte cap would cut a valid one mid-token and turn a working call
    into a parse failure. `env_allowlist` stays None for a kindred reason: the child
    is the operator's authenticated `claude` CLI and reads its credentials from the
    inherited environment. Both are stage-1 gaps, owed to T003's limitations
    document. Enforced and real: the wall deadline, the cwd pin, a zero core.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout_sec), cwd=cwd, core_file_bytes=0,
    )


def _stream_exec_policy(cwd: str | None) -> ExecGuardPolicy:
    """Stage-1 streaming-provider policy (F085 T002a) — the CHILD half only.

    `run_streamed_command` is a streaming supervisor and owns its own parent half,
    so this policy deliberately sets less than `_cli_exec_policy` does.
    `wall_timeout_seconds` stays None because that seam's watchdog is already the
    deadline for this call and a second one would fight it. `output_cap_bytes`
    stays None because that seam caps through `max_bytes` and `on_cap`, which stop
    the process tree instead of merely capping what is stored. `env_allowlist`
    stays None for the reason `_cli_exec_policy` gives: the child is the operator's
    authenticated `claude` CLI and reads its credentials from the inherited
    environment — a stage-1 gap owed to T003's limitations document. Enforced and
    real: the cwd pin and a zero core.
    """
    return ExecGuardPolicy(cwd=cwd, core_file_bytes=0)


def _decode_cli_stream(raw: bytes) -> str:
    """Decode one guarded stream the way `text=True` decoded it.

    Text mode wrapped the pipe in a `TextIOWrapper` with the locale encoding and
    universal newlines; both are reproduced. The ONE intended difference is
    `errors="replace"` — text mode raised UnicodeDecodeError from inside the spawn
    and no caller here handled it, so a mojibake CLI now parses honestly instead.
    """
    text = raw.decode(locale.getpreferredencoding(False), errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _guarded_cli_run(cmd: list[str], timeout_sec: float,
                     cwd: str | None) -> subprocess.CompletedProcess[str]:
    """Run a CLI command under the stage-1 policy, shaped like `subprocess.run`.

    The single spawn point this module's provider calls migrate onto, and the seam
    the tests mock instead of the stdlib. A wall trip is re-raised as
    `subprocess.TimeoutExpired` and a signal death republished in the -SIGNUM form,
    so every caller keeps the error text it already produced: the migration changes
    the mechanism, never the observable outcome.
    """
    guarded = run_guarded(cmd, _cli_exec_policy(timeout_sec, cwd))
    if guarded.tripped_limit == "wall_timeout":
        raise subprocess.TimeoutExpired(cmd, timeout_sec)
    code = guarded.returncode
    if code is None:
        try:
            code = -int(signal.Signals[guarded.term_signal].value)
        except (KeyError, ValueError, TypeError):
            code = -1
    return subprocess.CompletedProcess(
        cmd, code,
        _decode_cli_stream(guarded.stdout), _decode_cli_stream(guarded.stderr),
    )


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

    @property
    def last_stream_call_dir(self) -> str:
        """The ABSOLUTE directory of the most recent streamed call, or "".

        F010 writes a failed call's post-mortem next to that call's own stream artifacts
        instead of inventing a second evidence tree. Empty when this provider never
        streamed (stream evidence off, or a fake/manual provider) — the caller then falls
        back to the run's per-call directory.
        """
        from pathlib import Path as _P

        if not self._stream_evidence or not self._stream_evidence_dir:
            return ""
        call_id = self._last_stream_call_id
        if not call_id:
            return ""
        prefix = self._stream_rel_prefix or ""
        rel = call_id[len(prefix) + 1:] if prefix and call_id.startswith(prefix) else call_id
        return str(_P(self._stream_evidence_dir) / rel)

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
        # F2 (round 15): the shared canonical formatter -- the stream directory name IS
        # the call ref F010 and F012 both record, so it uses the one spelling rule.
        rel = (f"round-{canonical_call_number(max(1, self._stream_round))}/"
               f"{self._stream_kind}-{canonical_call_number(idx)}")
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
            proc = _guarded_cli_run(
                [claude, "--version"],
                # Pinned like every other provider call: an unpinned probe runs in
                # the operator's cwd and any stray write lands in the repo root.
                timeout_sec=5, cwd=self._cwd,
            )
            if proc.returncode == 0 and proc.stdout and proc.stdout.strip():
                self._cli_version = proc.stdout.strip()
        except Exception:
            pass
        return self._cli_version

    def _call_streamed(
        self, claude: str, prompt: str, *, timeout_sec: int, max_output_chars: int,
        json_schema: str = "",
    ) -> tuple[str, int, int, dict[str, Any] | None, str]:
        """F004 opt-in path: run the CLI in stream-json and capture evidence.

        The stream is consumed incrementally, redacted before persistence, and
        written to ``raw_stream.jsonl`` / ``run_events.jsonl`` in the task
        evidence directory. Token accounting stays F003-compatible: the final
        ``result`` event's usage is the authoritative total.
        """
        from packages.orchestration.stream_evidence import (
            DEFAULT_MAX_BYTES,
            final_result_envelope,
            run_streamed_command,
            usage_actuals_from_events,
        )

        if not self._stream_evidence_dir:
            raise RuntimeError("stream evidence enabled but no stream_evidence_dir was provided")

        argv = build_claude_cli_args(
            claude, prompt, write_mode=self._write_mode, model=self._model,
            stream_evidence=True, json_schema=json_schema,
        )
        call_dir = self._allocate_stream_call_dir()
        run = run_streamed_command(
            argv, call_dir, timeout_sec=timeout_sec,
            max_bytes=self._stream_max_bytes or DEFAULT_MAX_BYTES,
            policy=_stream_exec_policy(self._cwd),
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

        # F005 Finding 1: the final result envelope is parsed BEFORE the exit code
        # is interpreted. Claude can emit a valid structured-failure result and
        # then exit nonzero; that envelope is authoritative for classification and
        # its Usage/cost must not be thrown away with the return code.
        events = run.events
        usage_actuals, missing_reason = usage_actuals_from_events(
            events, cli_version=self._resolve_version(),
        )
        final_env = final_result_envelope(events, run.capture.raw_path)
        self._last_stream_final = final_env
        tokens = 0
        if usage_actuals is not None:
            tokens = usage_actuals["input_tokens"] + usage_actuals["output_tokens"]

        if run.returncode != 0:
            # Typed so the structured Reviewer can classify from the envelope it
            # carries; every other caller still sees a plain RuntimeError.
            raise _StreamNonZeroExit(
                f"claude CLI exited {run.returncode}: {run.stderr_tail[:500]}",
                returncode=run.returncode,
                stderr_tail=run.stderr_tail,
                final=final_env,
                usage_actuals=usage_actuals,
                tokens=tokens,
                duration_ms=run.duration_ms,
            )

        if any(e.get("event_type") == "provider_error" for e in events):
            err = next(e for e in events if e.get("event_type") == "provider_error")
            raise RuntimeError(f"claude CLI stream reported an error: {err.get('error', '')[:300]}")

        text = final_env.value_text
        if len(text) > max_output_chars:
            text = text[:max_output_chars] + "\n[OUTPUT TRUNCATED]"
        return text, run.duration_ms, tokens, usage_actuals, missing_reason

    def _call(
        self, prompt: str, *, timeout_sec: int, max_output_chars: int,
        json_schema: str = "",
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
                claude, prompt, timeout_sec=timeout_sec,
                max_output_chars=max_output_chars, json_schema=json_schema,
            )
        argv = build_claude_cli_args(
            claude, prompt, write_mode=self._write_mode, model=self._model,
            json_schema=json_schema,
        )
        start = time.monotonic()
        try:
            proc = _guarded_cli_run(argv, timeout_sec=timeout_sec, cwd=self._cwd)
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

    def _call_reviewer_structured(
        self, prompt: str, json_schema: str, *, timeout_sec: int, max_output_chars: int,
    ) -> StructuredCliOutcome:
        """One native structured reviewer call, classified from the envelope.

        Sends ``--json-schema`` and reads ``structured_output`` as the
        authoritative value. Native structured-output retry exhaustion and a
        success envelope missing ``structured_output`` are class ``parse``
        (usage/cost retained); an unknown ``--json-schema`` option is class
        ``config``. Provider transport failures raise as before.
        """
        claude = self._get_claude_path()
        cli_ver = self._resolve_version()

        # Stream mode: reuse the F004 capture (raw/redaction/accounting unchanged)
        # and classify from the COMPLETE final-result envelope, exactly like the
        # JSON path — never from an empty result string.
        if self._stream_evidence:
            try:
                text, dur, tokens, usage, _amr = self._call_streamed(
                    claude, prompt, timeout_sec=timeout_sec,
                    max_output_chars=max_output_chars, json_schema=json_schema,
                )
            except _StreamNonZeroExit as exc:
                # A native structured-output failure stays a parse failure even
                # when the process exits nonzero, and keeps its Usage/cost.
                if exc.final is not None and exc.final.found \
                        and exc.final.structured_retry_exhausted:
                    return StructuredCliOutcome(
                        duration_ms=exc.duration_ms, tokens=exc.tokens,
                        usage_actuals=exc.usage_actuals,
                        error_class="parse",
                        error_detail="native structured-output retries exhausted: "
                        + "; ".join(str(e) for e in exc.final.errors)[:180],
                    )
                # Anything else (ordinary error result, a "successful" structured
                # result contradicted by a nonzero exit, or no final result at
                # all) is an honest provider error.
                raise
            final = getattr(self, "_last_stream_final", None)

            if final is None or not final.found:
                return StructuredCliOutcome(
                    duration_ms=dur, tokens=tokens, usage_actuals=usage,
                    error_class="parse",
                    error_detail="streamed structured mode produced no final result line",
                )
            # Native schema exhaustion -> parse (usage/cost retained, one retry).
            if final.structured_retry_exhausted:
                return StructuredCliOutcome(
                    duration_ms=dur, tokens=tokens, usage_actuals=usage,
                    error_class="parse",
                    error_detail="native structured-output retries exhausted: "
                    + "; ".join(str(e) for e in final.errors)[:180],
                )
            # Any other error result is a genuine provider error, NOT a parse
            # failure: it must not consume the single Remedy parse retry.
            if final.is_error:
                detail = "; ".join(str(e) for e in final.errors)[:180] or final.subtype
                raise RuntimeError(
                    f"claude CLI stream reported an error ({final.subtype}): {detail}"
                )
            # Success result with no structured_output -> parse.
            if not final.has_structured_output:
                return StructuredCliOutcome(
                    duration_ms=dur, tokens=tokens, usage_actuals=usage,
                    error_class="parse",
                    error_detail="streamed structured mode success result had no structured_output",
                )
            return StructuredCliOutcome(
                value_text=text, duration_ms=dur, tokens=tokens, usage_actuals=usage,
            )

        argv = build_claude_cli_args(
            claude, prompt, write_mode=self._write_mode, model=self._model,
            json_schema=json_schema,
        )
        start = time.monotonic()
        try:
            proc = _guarded_cli_run(argv, timeout_sec=timeout_sec, cwd=self._cwd)
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"claude CLI timed out after {timeout_sec}s")
        dur = int((time.monotonic() - start) * 1000)
        raw = proc.stdout or ""
        env = _parse_cli_envelope(raw)
        usage = _usage_actuals_dict(env.usage_actuals, cli_ver) if env.usage_actuals else None
        tokens = (env.usage_actuals.input_tokens + env.usage_actuals.output_tokens
                  if env.usage_actuals else 0)

        if proc.returncode != 0:
            stderr = proc.stderr or ""
            # Finding 6: an unknown --json-schema option is a config error, proven
            # by the actual invocation, not by a --help preflight.
            if _looks_like_unknown_json_schema_option(stderr):
                return StructuredCliOutcome(
                    duration_ms=dur, tokens=tokens, usage_actuals=usage,
                    error_class="config",
                    error_detail="installed claude CLI rejected --json-schema as an unknown option",
                )
            # Native structured exhaustion can also surface on a nonzero exit.
            if env.structured_retry_exhausted:
                return StructuredCliOutcome(
                    duration_ms=dur, tokens=tokens, usage_actuals=usage,
                    error_class="parse",
                    error_detail="native structured-output retries exhausted: "
                    + "; ".join(str(e) for e in env.errors)[:180],
                )
            raise RuntimeError(f"claude CLI exited {proc.returncode}: {stderr[:500]}")

        # Finding 3: structured retry exhaustion → parse (usage/cost retained).
        if env.structured_retry_exhausted:
            return StructuredCliOutcome(
                duration_ms=dur, tokens=tokens, usage_actuals=usage,
                error_class="parse",
                error_detail="native structured-output retries exhausted: "
                + "; ".join(str(e) for e in env.errors)[:180],
            )
        if env.is_error:
            raise RuntimeError("claude CLI reported is_error=true")

        # Finding 1: prefer structured_output; a success envelope without it is a
        # parse failure — never fabricate a value.
        if env.has_structured_output:
            value_text = json.dumps(env.structured_output, separators=(",", ":"))
            return StructuredCliOutcome(
                value_text=value_text, duration_ms=dur, tokens=tokens, usage_actuals=usage,
            )
        return StructuredCliOutcome(
            duration_ms=dur, tokens=tokens, usage_actuals=usage,
            error_class="parse",
            error_detail="structured mode success envelope had no structured_output",
        )

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
        # F012: the CLI sends the builder prompt verbatim (no out-of-band schema).
        _pi = prepare_call_input(
            prompt=prompt, model=self._model, mode="cli-legacy",
            options={"write_mode": self._write_mode})
        out = self._build_impl(prompt, timeout_sec=timeout_sec,
                               max_output_chars=max_output_chars)
        out.prepared_input = _pi
        return out

    def _build_impl(
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
        structured = _reviewer_structured_enabled()
        # F012: fingerprint exactly what the transport receives — the prompt bytes plus, in
        # native structured mode, the out-of-band ``--json-schema`` argument.
        if structured:
            _pi = prepare_call_input(
                prompt=prompt, model=self._model, mode="cli-native",
                schema=_to_json_schema_str(_ReviewVerdictSchema),
                options={"write_mode": self._write_mode})
        else:
            _pi = prepare_call_input(
                prompt=prompt + "\n\n" + _REVIEWER_JSON_SCHEMA, model=self._model,
                mode="cli-legacy", options={"write_mode": self._write_mode})
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
        out.prepared_input = _pi
        return out

    def _review_impl(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        structured = _reviewer_structured_enabled()
        schema_v = _schema_v_of(_ReviewVerdictSchema)
        try:
            if structured:
                # Finding 5: the caller (loop) has already built the exact effective
                # prompt; the provider sends it verbatim and enforces the schema
                # NATIVELY through --json-schema (the full schema is out-of-band,
                # not duplicated into the prompt).
                json_schema = _to_json_schema_str(_ReviewVerdictSchema)
                oc = self._call_reviewer_structured(
                    prompt, json_schema,
                    timeout_sec=timeout_sec, max_output_chars=max_output_chars,
                )
                if oc.error_class == "config":
                    return ReviewerOutput(
                        verdict="blocked",
                        error=(
                            "structured_mode_unavailable: " + oc.error_detail
                            + "; set REMEDY_REVIEWER_FREETEXT=1 for the legacy reviewer"
                        ),
                        error_class="config",
                        schema_v=schema_v,
                        provider="claude-cli",
                        actual_missing_reason="structured_mode_unavailable",
                        usage_actuals=oc.usage_actuals,
                        stream_artifact_refs=self.last_stream_artifact_refs,
                        stream_call_id=self._last_stream_call_id,
                    )
                if oc.error_class == "parse":
                    # Finding 3/4: parse-classed, usage/cost retained so the failed
                    # attempt still counts toward totals; the malformed_output:
                    # prefix triggers the loop's one parse retry.
                    return ReviewerOutput(
                        verdict="blocked",
                        error=f"malformed_output: {oc.error_detail}",
                        error_class="parse",
                        parse_hint=oc.error_detail,
                        schema_v=schema_v,
                        provider="claude-cli",
                        duration_ms=oc.duration_ms,
                        tokens_used=oc.tokens,
                        usage_actuals=oc.usage_actuals,
                        actual_missing_reason="" if oc.usage_actuals else "usage_missing",
                        stream_artifact_refs=self.last_stream_artifact_refs,
                        stream_call_id=self._last_stream_call_id,
                    )
                out = _parse_reviewer_structured(
                    oc.value_text, oc.duration_ms, oc.tokens, provider="claude-cli",
                )
                out.usage_actuals = oc.usage_actuals
                out.actual_missing_reason = "" if oc.usage_actuals else "usage_missing"
                out.stream_artifact_refs = self.last_stream_artifact_refs
                out.stream_call_id = self._last_stream_call_id
                return out

            full_prompt = prompt + "\n\n" + _REVIEWER_JSON_SCHEMA
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

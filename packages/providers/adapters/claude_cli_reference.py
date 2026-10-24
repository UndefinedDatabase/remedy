"""The claude-cli reference adapter (F151 T003, DECISION F151 D4).

``ClaudeCliReferenceAdapter`` WRAPS today's claude-cli call path — ``build_claude_cli_args``,
``parse_cli_result_detailed``, ``redact_stream_payload``/``normalize_stream_object`` and the
shared error predicates ``_classify_error_text`` asks — and re-implements none of them. The
ping-pong loop and its seams keep owning transport, timeouts, every retry, failover, rate
pacing and per-call evidence (DECISION F151 D2 (2)); this module only builds an invocation and
maps a provider's raw output back onto the typed contract shapes. The adapter registry
(``adapter_registry.py``, DECISION F151 D5) reaches it for ``remedy worker show``, and the command
line installs that registry into the worker adapter slot, from which ``ClaudeCliProvider`` takes
the command line of every call and the usage of every call that is not streamed (DECISIONs F315
D2 and D3).
"""
from __future__ import annotations

import json
from typing import Any

from packages.contracts.adapter_contract import (
    ADAPTER_ROLES,
    AdapterCapabilities,
    AdapterInvocation,
    AdapterUsage,
    CliInvocation,
    InvocationOptions,
    WorkerIsolation,
    WorkerSandboxDefault,
)
from packages.orchestration.claude_cli_command import _claude_cli_flag, build_claude_cli_args
from packages.orchestration.failure_postmortem import FailureClass, _classify_error_text
from packages.orchestration.stream_evidence import normalize_stream_object, redact_stream_payload
from packages.orchestration.token_actuals import parse_cli_result_detailed

#: D3 (2)'s own ADR, spelled once: the one research page a claude-cli isolation record cites.
_ISOLATION_ADR_REF = "docs/adr/0002-claude-cli-worker-isolation.md"

#: The exact flags D3 (2) names — the captured help text's own lines 228-229 and 232-233 — kept
#: out of `claude_cli_launch_switches` because that function is the lean-call default every
#: caller already composes, and isolation is this adapter's own declared addition to it.
_ISOLATION_TOOL_ARGS = ("--setting-sources", "project,local", "--strict-mcp-config")

#: D3 (2)'s process names, in its own order: the shell/process names every worker needs plus
#: the model credential and both spellings of the four proxy variables.
_ISOLATION_ENV_ALLOWLIST = (
    "HOME", "LANG", "LC_ALL", "LC_CTYPE", "LOGNAME", "PATH", "SHELL", "TERM", "TMPDIR", "TZ",
    "USER", "ANTHROPIC_API_KEY", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
    "http_proxy", "https_proxy", "all_proxy", "no_proxy",
)

#: D4 (2)'s exact default profile, TOML text parsed by `parse_sandbox_profile` elsewhere (this
#: module does not import `sandbox_profiles`); the same layout as `sandbox_profile_files/strict.toml`,
#: one key per line, `[ulimits]` last.
_SANDBOX_PROFILE_TOML = (
    'fs_scope = ["{workspace}"]\n'
    'net = { allow = ["api.anthropic.com"] }\n'
    'allowed_binaries = "any"\n'
    'tmp_quota_mb = "unlimited"\n'
    "[ulimits]\n"
    'cpu_s = "unlimited"\n'
    'mem_mb = "unlimited"\n'
    "nofile = 1024\n"
)

#: D4 (2)'s exact reason the claude-cli process cannot run inside the tool sandbox.
_SANDBOX_DEFAULT_REASON = (
    "the claude command line keeps its login in the operator's home, which the tool sandbox "
    "hides (DECISION F152 D3)"
)

#: The three adapter-returnable classes `_classify_error_text` can itself produce (D4 (5)); its
#: fourth possible answer, the I/O class, is not one an adapter may return (ADAPTER_ERROR_CLASSES)
#: and is folded into unknown below, same as a text none of its predicates read.
_TEXT_CLASSIFIED_CLASSES = frozenset({
    FailureClass.PROVIDER_UNAVAILABLE, FailureClass.PROVIDER_TIMEOUT,
    FailureClass.PROVIDER_NONZERO_EXIT,
})


# WHY: the module-level classifier classify_error delegates to (D4 (5)); the kit's transport
# dimension reads it too, because the class calls it by name (amend1023 D4).
def classify_claude_cli_error(error_text: str, exit_code: int | None) -> FailureClass:
    """Classify a claude-cli failure exactly as DECISION F151 D4 (5) states.

    Asks the shared text predicates in `_classify_error_text`'s own order first. A message
    beginning ``malformed_output:`` — the adapter's own structured-output failure marker, which
    no shared predicate reads — is `parse`. Failing both, a remaining non-zero exit code (one
    the text did not already explain) is `non-zero exit`. Everything else, the I/O class the
    shared predicates can also produce included, is `unknown`.
    """
    text = error_text or ""
    if text.startswith("malformed_output:"):
        return FailureClass.PARSE
    from_text = _classify_error_text(text)
    if from_text in _TEXT_CLASSIFIED_CLASSES:
        return from_text
    if exit_code not in (None, 0):
        return FailureClass.PROVIDER_NONZERO_EXIT
    return FailureClass.UNKNOWN


class ClaudeCliReferenceAdapter:
    """Wraps the existing claude-cli call path; a thin builder/mapper, never a transport (D2 (2))."""

    # WHY: every call this adapter builds carries the same binary path, write mode, streaming
    # flag and configuration, so a caller states them once instead of on every invocation.
    def __init__(
        self, *, claude_path: str = "claude", write_mode: str = "none",
        streaming: bool = True, config: Any = None,
    ) -> None:
        self._claude_path = claude_path
        self._write_mode = write_mode
        self._streaming = streaming
        self._config = config

    # WHY: the adapter's stable name is the provider's own, so the registry linkage reaches this
    # class through the same string `provider_names.py` already uses (DECISION F151 D5).
    @property
    def adapter_id(self) -> str:
        return "claude-cli"

    # WHY: declared, not probed (D4 (6)) — nothing today measures a context size, so it stays 0.
    def capabilities(self, model: str) -> AdapterCapabilities:
        return AdapterCapabilities(
            vision=False, json_schema=True, session_resume=True,
            streaming=self._streaming, tool_use=True, max_context_tokens=0)

    # WHY: builds the exact argv `build_claude_cli_args` would, with the role's write mode and
    # per-role default `role_provider_factory.py` reads today (D4 (2)), plus the declared
    # isolation flags at the end while they apply (DECISION F152 D3 (3)).
    def build_invocation(
        self, role: str, prompt_parts: tuple[str, ...], options: InvocationOptions,
    ) -> AdapterInvocation:
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        prompt = "\n\n".join(prompt_parts)
        write_mode = self._write_mode if role == "builder" else "none"
        json_schema = (
            json.dumps(options.output_schema, separators=(",", ":"), sort_keys=True)
            if options.output_schema is not None else ""
        )
        argv = tuple(build_claude_cli_args(
            self._claude_path, prompt,
            write_mode=write_mode, model=options.model, stream_evidence=self._streaming,
            json_schema=json_schema, resume_session=options.resume_ref or "",
            config=self._config,
        ))
        declaration = self.isolation()
        if declaration.applies:
            argv = argv + declaration.tool_args
        return CliInvocation(argv=argv)

    # WHY: redacts then normalizes through the existing stream_evidence functions unchanged
    # (D4 (3)); a line the redactor cannot decode as a JSON object yields no event, because
    # counting a malformed line is per-call evidence the capture keeps, not this mapping's job.
    def map_stream(self, raw_lines: tuple[str, ...]) -> tuple[dict, ...]:
        if not self._streaming:
            return ()
        events: list[dict] = []
        for line in raw_lines:
            if not line.strip():
                continue
            _redacted, decoded = redact_stream_payload(line)
            if not isinstance(decoded, dict):
                continue
            events.extend(normalize_stream_object(decoded))
        return tuple(events)

    # WHY: answers exactly when the existing envelope parser does, carrying the provider's own
    # usage object unchanged as raw_counters (D4 (4)).
    def map_usage(self, raw: str) -> AdapterUsage | None:
        actuals, _reason = parse_cli_result_detailed(raw)
        if actuals is None:
            return None
        try:
            payload = json.loads(raw)
        except (ValueError, TypeError):
            return None
        raw_counters = payload.get("usage") if isinstance(payload, dict) else None
        if not isinstance(raw_counters, dict):
            return None
        return AdapterUsage(actuals=actuals, raw_counters=raw_counters)

    # WHY: delegates to the module-level classifier, so the shared predicates are read in one
    # place and this method's own body never spells a forbidden transport word (D4 (5)).
    def classify_error(self, error_text: str, exit_code: int | None) -> FailureClass:
        return classify_claude_cli_error(error_text, exit_code)

    # WHY: D3 (2)'s exact declaration — tool_flag, no throwaway home because the operator's own
    # login lives under the operator's own home, off exactly when the operator's own
    # `claude_cli.customizations` switch asks for the opposite.
    def isolation(self) -> WorkerIsolation:
        return WorkerIsolation(
            method="tool_flag",
            adr_ref=_ISOLATION_ADR_REF,
            tool_args=_ISOLATION_TOOL_ARGS,
            env_allowlist=_ISOLATION_ENV_ALLOWLIST,
            applies=not _claude_cli_flag(self._config, "claude_cli.customizations"),
        )

    # WHY: D4 (2)'s exact declaration — an API allowlist naming the one endpoint this adapter's
    # calls are for, declarative because D3 (4) already records an allowlist as unenforced;
    # outside the tool sandbox because the operator's login lives in the home the sandbox hides
    # (DECISION F152 D3).
    def sandbox_default(self) -> WorkerSandboxDefault:
        return WorkerSandboxDefault(
            profile_toml=_SANDBOX_PROFILE_TOML, tool_sandbox=False,
            reason=_SANDBOX_DEFAULT_REASON,
        )

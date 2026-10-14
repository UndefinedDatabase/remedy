"""The Pi execution harness as a ping-pong provider (operator amendment amend1014b, DECISION D1 to D4).

Pi supplies the agent loop and the file tools; Ollama supplies the model. This module runs the
installed `pi` command once per role call, in JSON mode, with its working directory set to the
job's isolated workspace, and reads the JSONL event stream it prints. A raw text completion is
not a coding harness: Pi reads, edits and tests inside the workspace, and the workspace diff is
the only proof of a change. Assistant prose and claimed file lists never create one.

Remedy deliberately does NOT embed Pi's SDK, start a Pi daemon, or claim an operating-system
sandbox here: Pi itself says its tools run with the invoking user's permissions, so the isolation
that holds is Remedy's own (the job worktree, the target hash guard, the scope guard and the
stop before apply). Remedy also does not copy the operator's Pi settings, credentials,
extensions, MCP servers, skills, prompt templates or themes into a worker: the runtime agent
directory below holds one `models.json` and nothing else Remedy wrote.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.call_identity import prepare_call_input
from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded
from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.pi_events import (
    PiRunSummary,
    PiStreamError,
    parse_pi_events,
    summarize_pi_events,
)
from packages.orchestration.pingpong_provider import (
    _REVIEWER_JSON_SCHEMA,
    BuilderOutput,
    ReviewerOutput,
    _parse_reviewer_json,
)

PI_PROVIDER_NAME = "pi"
#: The model server Pi talks to, and the model the whole local chain defaults to.
PI_INNER_PROVIDER = "ollama"
PI_DEFAULT_MODEL = resolve_model_alias("ollama-default")
#: The role tool allowlists (D2). The reviewer reads; it never writes, runs a shell or edits.
PI_BUILDER_TOOLS = "read,bash,edit,write,grep,find,ls"
PI_REVIEWER_TOOLS = "read,grep,find,ls"
#: An agent loop with tool turns takes minutes on a local model, so the two-minute
#: single-completion budget the execution config carries by default is a floor, not a ceiling.
PI_MIN_WALL_SECONDS = 900
#: Per stream; a Pi event stream carries one record per token delta, so 64 MiB is generous.
PI_STDOUT_CAP_BYTES = 64 * 1024 * 1024
PI_STDERR_TAIL_CHARS = 2000
_PI_ENV_ALLOWLIST = ("PATH", "HOME", "LANG", "LC_ALL", "LC_CTYPE", "LOGNAME", "SHELL",
                     "TMPDIR", "TZ", "USER", "TERM")
#: The values the verified local model needs in Pi's `models.json` (the operator's own entry).
_PI_MODEL_CONTEXT_WINDOW = 131072
_PI_MODEL_MAX_TOKENS = 16384
_PI_CALL_MODE = "pi-json"
_PI_VERSION_TIMEOUT_SEC = 20

_BUILDER_PREAMBLE = (
    "You are the builder in an isolated working copy. Your current directory IS that copy; "
    "work only inside it. Inspect the files the task names, make the edit directly with your "
    "file tools, run only checks relevant to the task, inspect the actual change you made "
    "(for example with `git diff`), and report truthfully. A change you describe but did not "
    "write to a file does not exist. Change no file the task does not name.\n\n"
)
_REVIEWER_PREAMBLE = (
    "You are the reviewer. You have read-only tools; you cannot edit. Judge the staged diff "
    "below against the task. Answer in the JSON shape the end of this message requires.\n\n"
)


class PiUnavailable(RuntimeError):
    """The Pi chain cannot run: a missing executable, model or endpoint. Names the action."""


# ---------------------------------------------------------------------------
# D2 — the invocation
# ---------------------------------------------------------------------------

def pi_role_tools(role: str) -> str:
    """The tool allowlist for a role; every reviewing role is read-only (D2)."""
    return PI_BUILDER_TOOLS if role in ("builder", "repair") else PI_REVIEWER_TOOLS


def build_pi_argv(pi_path: str, *, model: str, tools: str, prompt: str) -> list[str]:
    """Pi's argument vector for one role call. Never a shell string.

    Every resource switch is off: no extension, MCP server, skill, prompt template or theme, no
    session, no network at startup, and project-local executable resources stay untrusted.
    """
    return [
        pi_path, "--mode", "json", "--no-session",
        "--provider", PI_INNER_PROVIDER, "--model", model,
        "--offline", "--no-approve", "--no-extensions", "--no-mcp", "--no-skills",
        "--no-prompt-templates", "--no-themes", "--tools", tools, "--", prompt,
    ]


def pi_agent_dir() -> Path:
    """Remedy's private Pi agent directory, under the run data root, never `~/.pi`."""
    from packages.orchestration.data_paths import resolve_data_root

    return resolve_data_root() / "pi_agent"


def ollama_host() -> str:
    """Where Ollama lives: the existing `ollama.host` key, then the environment, then the default."""
    host = os.environ.get("REMEDY_OLLAMA_HOST", "")
    if not host:
        try:
            from packages.orchestration.config import get_config
            host = str(get_config().get("ollama.host") or "")
        except Exception:  # noqa: BLE001 — an unreadable config falls back to the local default
            host = ""
    return (host or "http://localhost:11434").rstrip("/")


def write_pi_models_json(agent_dir: Path, *, host: str, model: str) -> Path:
    """The one file Remedy writes into the runtime agent directory: the model connection."""
    agent_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    models = {"providers": {PI_INNER_PROVIDER: {
        "baseUrl": f"{host.rstrip('/')}/v1",
        "api": "openai-completions",
        "apiKey": "ollama",
        "compat": {"supportsDeveloperRole": False, "supportsReasoningEffort": False},
        "models": [{
            "id": model, "name": f"{model} (local Ollama)", "reasoning": True,
            "input": ["text"], "contextWindow": _PI_MODEL_CONTEXT_WINDOW,
            "maxTokens": _PI_MODEL_MAX_TOKENS,
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        }],
    }}}
    path = agent_dir / "models.json"
    text = json.dumps(models, indent=2, sort_keys=True) + "\n"
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
    return path


def pi_child_env(agent_dir: Path) -> dict[str, str]:
    """The environment a Pi child gets: a short allowlist plus Pi's own switches."""
    env = {key: os.environ[key] for key in _PI_ENV_ALLOWLIST if key in os.environ}
    env.update({"PI_CODING_AGENT_DIR": str(agent_dir), "PI_OFFLINE": "1",
                "PI_SKIP_VERSION_CHECK": "1", "PI_TELEMETRY": "0"})
    return env


def resolve_pi_executable() -> str:
    """The `pi` on PATH, or a PiUnavailable that says what to do (D4); no installation is tried."""
    found = shutil.which("pi")
    if not found:
        raise PiUnavailable(
            "Pi is required by the default local builder but was not found. "
            "Install Pi or select an available explicit builder provider.")
    return found


def pi_version(pi_path: str) -> str:
    """`pi --version`, or "" when it cannot be read."""
    try:
        done = subprocess.run([pi_path, "--version"], capture_output=True, text=True,
                              timeout=_PI_VERSION_TIMEOUT_SEC, check=False)
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout.strip().splitlines()[0] if done.returncode == 0 and done.stdout.strip() else ""


def _ollama_models(host: str) -> list[str]:
    """The model names the Ollama endpoint lists; raises PiUnavailable when it is unreachable."""
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=5) as response:  # noqa: S310 — operator's own configured host
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError) as exc:
        raise PiUnavailable(
            f"Ollama is not reachable at {host} ({type(exc).__name__}). Start Ollama or set "
            f"ollama.host; the default local builder needs it.") from exc
    names = [m.get("name", "") for m in payload.get("models", []) if isinstance(m, dict)]
    return [n for n in names if isinstance(n, str)]


def pi_preflight(*, model: str, workspace: str | None, role: str,
                 check_endpoint: bool = True) -> dict[str, str]:
    """D4: every prerequisite, checked before any model call. Reads only; runs no agent.

    Returns the evidence (executable, version, model, host). Raises PiUnavailable naming the
    corrective action. There is no fallback to another provider or model.
    """
    pi_path = resolve_pi_executable()
    if workspace is not None and not Path(workspace).is_dir():
        raise PiUnavailable(f"The job workspace {workspace} does not exist, so Pi has no place to work.")
    if not pi_role_tools(role):
        raise PiUnavailable(f"No Pi tool policy exists for the role {role!r}.")
    host = ollama_host()
    write_pi_models_json(pi_agent_dir(), host=host, model=model)
    if check_endpoint:
        names = _ollama_models(host)
        if model not in names and f"{model}:latest" not in names:
            raise PiUnavailable(
                f"The model {model} is not installed in Ollama at {host}. "
                f"Pull it (`ollama pull {model}`) or select another model.")
    return {"pi_path": pi_path, "pi_version": pi_version(pi_path), "model": model, "host": host}


def default_chain_checks() -> list[tuple[str, bool, str]]:
    """``(check, ok, detail)`` for each link of the default chain, for the health surfaces (D4).

    Pi on the path, the model Pi will be handed, the Ollama endpoint and the model in it. Reads
    only: it runs no agent, writes no file and never touches a repository.
    """
    found = shutil.which("pi")
    checks: list[tuple[str, bool, str]] = [
        ("pi_executable", found is not None,
         f"pi at {found} ({pi_version(found) or 'version unreadable'})" if found
         else "pi not found on PATH; install Pi or select an explicit builder provider")]
    host = ollama_host()
    try:
        names = _ollama_models(host)
    except PiUnavailable as exc:
        return checks + [("ollama_endpoint", False, str(exc)),
                         ("pi_model", False, f"{PI_DEFAULT_MODEL} cannot be checked without Ollama")]
    present = PI_DEFAULT_MODEL in names or f"{PI_DEFAULT_MODEL}:latest" in names
    return checks + [
        ("ollama_endpoint", True, f"Ollama answers at {host}"),
        ("pi_model", present,
         f"{PI_DEFAULT_MODEL} is installed in Ollama" if present
         else f"{PI_DEFAULT_MODEL} is not installed in Ollama; run `ollama pull {PI_DEFAULT_MODEL}`")]


def _redacted_tail(raw: bytes) -> str:
    from packages.orchestration.stream_evidence import redact_text

    text = raw.decode("utf-8", errors="replace")
    return redact_text(text[-PI_STDERR_TAIL_CHARS:])


def pi_failure_text(summary: PiRunSummary | None, *, exit_code: int | None, term_signal: str | None,
                    tripped: str | None, stderr: bytes, stream_error: str) -> str:
    """The one provider_error sentence for a Pi call that did not complete, or "" when it did.

    The `provider_error:` prefix is load-bearing (finding R-0378): the loop reads a verdict of
    `blocked` as a reviewer reject unless a transport failure carries it.
    """
    tail = _redacted_tail(stderr)
    if tripped == "wall_timeout":
        return "provider_error: pi_timeout: the Pi call hit its wall-clock deadline"
    if tripped == "output_bytes":
        return "provider_error: pi_output_limit: the Pi event stream passed its size cap"
    if term_signal:
        return f"provider_error: pi_killed: Pi died on {term_signal}"
    if exit_code not in (0, None):
        return f"provider_error: pi_exit_{exit_code}: {tail.strip()[-300:] or 'no diagnostic on stderr'}"
    if stream_error:
        return f"provider_error: pi_malformed_stream: {stream_error}"
    if summary is None or summary.model_turns == 0:
        return f"provider_error: pi_no_response: Pi produced no assistant message. {tail.strip()[-200:]}".rstrip()
    if summary.aborted:
        return "provider_error: pi_aborted: the Pi run was aborted"
    if not summary.settled:
        return "provider_error: pi_unsettled: the event stream ended without agent_settled"
    if summary.model_error:
        return f"provider_error: pi_model_error: {summary.model_error[:300]}"
    return ""


@dataclass
class PiCallOutcome:
    """One Pi invocation: the summary, the evidence record and the failure text ("" on success)."""

    summary: PiRunSummary | None
    evidence: dict[str, Any]
    error: str
    duration_ms: int


class PiProvider:
    """Builder/reviewer provider that runs the Pi harness in the job workspace (D1, D2)."""

    def __init__(self, *, role: str = "builder", cwd: str | None = None, model: str = "") -> None:
        self._role = role
        self._cwd = cwd
        self._model = model or PI_DEFAULT_MODEL
        self.last_evidence: dict[str, Any] = {}

    @property
    def name(self) -> str:
        return PI_PROVIDER_NAME

    @property
    def supports_resume(self) -> bool:
        return False

    @property
    def resume_unsupported_reason(self) -> str:
        return "a Pi one-shot call runs with --no-session and keeps no conversation"

    @property
    def model(self) -> str:
        return self._model

    @property
    def inner_provider(self) -> str:
        return PI_INNER_PROVIDER

    def _call(self, prompt: str, *, timeout_sec: int, max_output_chars: int) -> PiCallOutcome:
        tools = pi_role_tools(self._role)
        started = time.monotonic()
        try:
            info = pi_preflight(model=self._model, workspace=self._cwd, role=self._role,
                                check_endpoint=False)
        except PiUnavailable as exc:
            return PiCallOutcome(None, {"role": self._role}, f"provider_error: pi_unavailable: {exc}", 0)
        argv = build_pi_argv(info["pi_path"], model=self._model, tools=tools, prompt=prompt)
        policy = ExecGuardPolicy(
            wall_timeout_seconds=float(max(timeout_sec, PI_MIN_WALL_SECONDS)),
            cwd=self._cwd, core_file_bytes=0, output_cap_bytes=PI_STDOUT_CAP_BYTES,
            env=pi_child_env(pi_agent_dir()), env_allowlist=_PI_ENV_ALLOWLIST + (
                "PI_CODING_AGENT_DIR", "PI_OFFLINE", "PI_SKIP_VERSION_CHECK", "PI_TELEMETRY"))
        guarded = run_guarded(argv, policy)
        stream_error, summary = "", None
        try:
            summary = summarize_pi_events(parse_pi_events(guarded.stdout))
        except PiStreamError as exc:
            stream_error = str(exc)
        if guarded.stdout_truncated:
            stream_error = stream_error or "the stream was cut at the size cap"
        error = pi_failure_text(
            summary, exit_code=guarded.returncode, term_signal=guarded.term_signal,
            tripped=guarded.tripped_limit, stderr=guarded.stderr, stream_error=stream_error)
        duration_ms = int((time.monotonic() - started) * 1000)
        evidence = {
            "role": self._role, "provider": PI_PROVIDER_NAME, "inner_provider": PI_INNER_PROVIDER,
            "model": self._model, "pi_path": info["pi_path"], "pi_version": info["pi_version"],
            "tools": tools, "cwd": self._cwd or "", "exit_code": guarded.returncode,
            "term_signal": guarded.term_signal, "duration_ms": duration_ms,
            "stop_reason": summary.stop_reason if summary else "",
            "model_turns": summary.model_turns if summary else 0,
            "tool_calls": list(summary.tool_calls) if summary else [],
            "tool_errors": summary.tool_errors if summary else 0,
            "retries": summary.retries if summary else 0,
            "usage": dict(summary.usage) if summary else {},
            "settled": bool(summary and summary.settled), "error": error[:300],
        }
        self.last_evidence = evidence
        if summary is not None and len(summary.final_text) > max_output_chars:
            summary.final_text = summary.final_text[:max_output_chars] + "\n[OUTPUT TRUNCATED]"
        return PiCallOutcome(summary, evidence, error, duration_ms)

    def _usage_actuals(self, outcome: PiCallOutcome) -> dict[str, Any] | None:
        summary = outcome.summary
        if summary is None or not summary.model_turns:
            return None
        return {"input_tokens": summary.usage["input"], "output_tokens": summary.usage["output"],
                "total_tokens": summary.usage["totalTokens"],
                "cache_read_input_tokens": summary.usage["cacheRead"],
                "cache_creation_input_tokens": summary.usage["cacheWrite"],
                "total_cost_usd": 0.0, "model_turns": summary.model_turns,
                "parse_source": "pi_json_events"}

    def build(self, prompt: str, *, timeout_sec: int = 120, max_output_chars: int = 50000,
              resume: str | None = None) -> BuilderOutput:
        full = _BUILDER_PREAMBLE + prompt
        fingerprint = prepare_call_input(
            prompt=full, model=self._model, mode=_PI_CALL_MODE,
            options={"tools": pi_role_tools(self._role), "inner_provider": PI_INNER_PROVIDER})
        outcome = self._call(full, timeout_sec=timeout_sec, max_output_chars=max_output_chars)
        if outcome.error:
            return BuilderOutput(error=outcome.error, provider=PI_PROVIDER_NAME,
                                 duration_ms=outcome.duration_ms,
                                 actual_missing_reason="provider_error", prepared_input=fingerprint)
        summary = outcome.summary
        assert summary is not None  # an empty error means the stream parsed
        actuals = self._usage_actuals(outcome)
        # `files_changed` stays empty on purpose: the workspace diff is the authority, never
        # a list the assistant claimed.
        return BuilderOutput(
            summary=summary.final_text[:500], files_changed=[], raw_text=summary.final_text,
            provider=PI_PROVIDER_NAME, duration_ms=outcome.duration_ms,
            tokens_used=summary.usage["totalTokens"], usage_actuals=actuals,
            actual_missing_reason="" if actuals else "provider_actuals_unavailable",
            prepared_input=fingerprint)

    def review(self, prompt: str, *, timeout_sec: int = 120, max_output_chars: int = 50000,
               resume: str | None = None) -> ReviewerOutput:
        full = _REVIEWER_PREAMBLE + prompt + "\n\n" + _REVIEWER_JSON_SCHEMA
        fingerprint = prepare_call_input(
            prompt=full, model=self._model, mode=_PI_CALL_MODE,
            options={"tools": pi_role_tools("reviewer"), "inner_provider": PI_INNER_PROVIDER})
        outcome = self._call(full, timeout_sec=timeout_sec, max_output_chars=max_output_chars)
        if outcome.error:
            return ReviewerOutput(error=outcome.error, error_class="provider_error",
                                  provider=PI_PROVIDER_NAME, duration_ms=outcome.duration_ms,
                                  actual_missing_reason="provider_error", prepared_input=fingerprint)
        summary = outcome.summary
        assert summary is not None
        out = _parse_reviewer_json(summary.final_text, outcome.duration_ms,
                                   summary.usage["totalTokens"], provider=PI_PROVIDER_NAME)
        actuals = self._usage_actuals(outcome)
        out.usage_actuals = actuals
        out.actual_missing_reason = "" if actuals else "provider_actuals_unavailable"
        out.prepared_input = fingerprint
        return out


def make_pi_provider(role: str, *, cwd: str | None, model: str = "") -> PiProvider:
    """Construct a role's Pi provider after the D4 prerequisites hold; raises PiUnavailable.

    The construction check is the one that runs BEFORE any model call: an absent executable, a
    missing model or an unreachable endpoint stops the run here, with the corrective action.
    """
    chosen = model or PI_DEFAULT_MODEL
    pi_preflight(model=chosen, workspace=cwd, role=role)
    return PiProvider(role=role, cwd=cwd, model=chosen)

"""The Pi execution harness as a ping-pong provider (operator amendment amend1014b, DECISION D1 to D4).

Pi supplies the agent loop and the file tools; Ollama supplies the model. This module runs the
installed `pi` command once per role call, in JSON mode, with its working directory set to the
job's isolated workspace, and reads the JSONL event stream it prints. A raw text completion is
not a coding harness: Pi reads, edits and tests inside the workspace, and the workspace diff is
the only proof of a change. Assistant prose and claimed file lists never create one.

Pi's tools run inside the Pi process with its rights, so since DECISION amend1016sb D1 the WHOLE
Pi process runs inside the tool sandbox (`tool_sandbox`): the workspace is its one writable tree,
its network is private, and its model endpoint is reached through the trusted relay. Every bash
command of the model goes through Remedy's tool shell, which ends it at `pi.tool_timeout_seconds`
(D2); a job stop ends a running call within about a second (D6). There is no unsandboxed path: a
sandbox that cannot run makes `pi_preflight` raise `PiUnavailable`. Remedy also does not copy the
operator's Pi settings, credentials, extensions, MCP servers, skills, prompt templates or themes
into a worker: the per-call agent directory holds Remedy's `models.json` and `settings.json` only.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import time
from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
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
from packages.orchestration.pi_loop_limits import PI_LOOP_LIMIT_MARK, PiLoopWatch, bind_job_token_budget, pi_loop_limits
from packages.orchestration.pingpong_provider import (
    _REVIEWER_JSON_SCHEMA,
    BuilderOutput,
    ReviewerOutput,
    _parse_reviewer_json,
)
from packages.orchestration.provider_timeouts import PI_DEFAULT_TIMEOUT_SEC
from packages.orchestration.tool_sandbox import (
    SANDBOX_PROVIDER_PORT,
    SANDBOX_RUN_DIR,
    SandboxUnavailable,
    provider_sandbox,
    require_sandbox,
)

PI_PROVIDER_NAME = "pi"
#: The model server Pi talks to, and the model the whole local chain defaults to.
PI_INNER_PROVIDER = "ollama"
PI_DEFAULT_MODEL = resolve_model_alias("ollama-default")
#: The role tool allowlists (D2). The reviewer reads; it never writes, runs a shell or edits.
PI_BUILDER_TOOLS = "read,bash,edit,write,grep,find,ls"
PI_REVIEWER_TOOLS = "read,grep,find,ls"
# Remedy deliberately keeps no minimum wall time for Pi: an explicit timeout, the job's remaining
# wall-clock budget and its deadline are each a CEILING, and the call gets the tightest one. The
# longer Pi-specific default lives in `provider_timeouts.PI_DEFAULT_TIMEOUT_SEC`, where the
# timeout is resolved, and applies only when nobody set a timeout.
#: Per stream; a Pi event stream carries one record per token delta, so 64 MiB is generous.
PI_STDOUT_CAP_BYTES = 64 * 1024 * 1024
PI_STDERR_TAIL_CHARS = 2000
#: Yields ``(seconds_left, source)`` for the running job, or None when no job clock is bound.
_JOB_TIME_LEFT: ContextVar[Callable[[], tuple[float | None, str]] | None] = ContextVar(
    "pi_job_time_left", default=None)
#: True once the running job has a stop request; a Pi call then ends within about a second (D6).
_JOB_STOP_REQUESTED: ContextVar[Callable[[], bool] | None] = ContextVar(
    "pi_job_stop_requested", default=None)
#: The default of `pi.tool_timeout_seconds`, used when the config cannot be read.
PI_TOOL_TIMEOUT_DEFAULT_SEC = 300
#: The agent directory inside the sandbox, part of the read-only per-call run directory.
_PI_AGENT_DIR_INSIDE = f"{SANDBOX_RUN_DIR}/agent"
#: Remedy's tool shell (D2). Pi runs every bash command as `<shellPath> -c <command>` in a process
#: group of its own; `timeout` ends the command at its deadline, says so, and sweeps the group.
_TOOL_SHELL = """#!/bin/sh
shell=/bin/bash
[ -x "$shell" ] || shell=/bin/sh
timeout --foreground -k 5 {limit} "$shell" "$@"
code=$?
if [ "$code" -eq 124 ]; then
    echo "remedy: this command was ended at its tool deadline of {limit} seconds" >&2
    trap '' TERM
    kill -TERM 0 2>/dev/null
fi
exit "$code"
"""
_PI_ENV_ALLOWLIST = ("PATH", "HOME", "LANG", "LC_ALL", "LC_CTYPE", "LOGNAME", "SHELL",
                     "TMPDIR", "TZ", "USER", "TERM")
#: The values the verified local model needs in Pi's `models.json` (the operator's own entry).
_PI_MODEL_CONTEXT_WINDOW = 131072
_PI_MODEL_MAX_TOKENS = 16384
_PI_CALL_MODE = "pi-json"
_PI_VERSION_TIMEOUT_SEC = 20

# Lab order of 2026-10-17 16:2x: a correct three-line README append took 12 turns and 53,730 input
# tokens (5 reads, 3 shell calls, the edit, then more checking), because nothing told the builder
# that Remedy itself runs the project's tests and has a reviewer read the diff afterwards.
_BUILDER_PREAMBLE = (
    "You are the builder in an isolated working copy. Your current directory IS that copy; "
    "work only inside it. Read the files the task names (each once), make the edit directly with "
    "your file tools, look at the actual change once (for example with `git diff`), then stop and "
    "answer in one or two sentences. Do NOT run the project's tests or build: Remedy runs them "
    "itself after you finish, and a reviewer reads your diff; a sentence in the task asking for "
    "the tests to run is Remedy's job, not yours. Every extra step resends the whole conversation, "
    "so take as few steps as the edit needs. A change you describe but did not write to a file "
    "does not exist. Change no file the task does not name.\n\n"
)
#: How much of the workspace the builder is handed up front (lab order of 2026-10-17: a one-line
#: fix spent 8 of its 12 turns on ls, find, grep and reads before the first edit).
_CONTEXT_MAX_LISTED = 80
_CONTEXT_MAX_FILES = 4
_CONTEXT_MAX_FILE_CHARS = 6000
_CONTEXT_SKIP_DIRS = frozenset({".git", "node_modules", ".venv", "venv", "__pycache__", ".remedy-wt",
                                "dist", "build", ".next", ".cache"})
#: The repository's own agent instructions, in the order Pi itself looks for them in a folder (exec-1017c).
_CONTEXT_AGENT_FILES = ("AGENTS.md", "CLAUDE.md")
#: The most characters of a repository's instructions one call carries (exec-1018, R-1347): about 8,000
#: tokens, under which every applicable file is delivered whole; above it the call does not start, because
#: Remedy deliberately never shortens binding instructions and pretends they were followed.
PROJECT_RULES_MAX_CHARS = 32_000
#: The error mark of a call refused for that reason; the loop ends such a run `context_error`.
PROJECT_RULES_TOO_LARGE_MARK = "project_rules_too_large"


def builder_workspace_context(cwd: str, prompt: str, *, role: str = "builder") -> str:
    """The workspace's file list and the text of the files *prompt* names, for the builder's prompt.

    A named file is read by its path, so a file deep in a large repository is shown although the
    bounded listing stops before it (it lists at most `_CONTEXT_MAX_LISTED` files and says so when
    it is cut). A named file that does not exist yet (a new test) brings one existing file of its
    folder as the style to follow. Read with plain bounded calls: no symlink is followed and no
    `git` runs in the target repository, whose own configuration could run commands. "" without a
    workspace.
    """
    if not cwd or not os.path.isdir(cwd):
        return ""
    root = Path(cwd)
    listed: list[str] = []
    for folder, dirs, files in os.walk(cwd):
        dirs[:] = sorted(d for d in dirs if d not in _CONTEXT_SKIP_DIRS and not os.path.islink(os.path.join(folder, d)))
        for name in sorted(files):
            path = Path(folder) / name
            if not path.is_symlink():
                listed.append(path.relative_to(root).as_posix())
        if len(listed) > _CONTEXT_MAX_LISTED:
            break
    cut = len(listed) > _CONTEXT_MAX_LISTED
    listed = listed[:_CONTEXT_MAX_LISTED]
    named = list(dict.fromkeys(re.findall(r"[\w./-]+\.[A-Za-z0-9]{1,8}\b", prompt)))   # as the task names them
    shown = [rel for rel in named if _plain_workspace_file(root, rel)]
    for rel in named:
        if rel in shown or "/" not in rel or not _plain_workspace_dir(root, rel.rsplit("/", 1)[0]):
            continue
        folder = rel.rsplit("/", 1)[0]
        sibling = next((f"{folder}/{name}" for name in sorted(os.listdir(root / folder))
                        if _plain_workspace_file(root, f"{folder}/{name}")), "")
        if sibling and sibling not in shown:
            shown.append(sibling)
    blocks = []
    for rel in shown[:_CONTEXT_MAX_FILES]:
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if len(text) <= _CONTEXT_MAX_FILE_CHARS:
            blocks.append(f"--- {rel} ---\n{text.rstrip()}\n")
    head = (f"Files in your working copy (the first {_CONTEXT_MAX_LISTED}; the tree is larger, so search "
            "it only for a file the task needs that is neither listed nor shown below):\n" if cut else
            "Files in your working copy (the complete list; do not list or search it again):\n")
    out = head + "".join(f"- {p}\n" for p in listed) + render_project_rules(project_rules(cwd, prompt), role)
    if blocks:
        out += ("\nCurrent content of the files the task names (already read for you; do not read "
                "them again before editing):\n\n" + "\n".join(blocks))
    return out + "\n"


@dataclass(frozen=True)
class ProjectRules:
    """The repository's instructions that apply to a call: `(path, text)` from the root down, and why
    they cannot be delivered ("" when they can)."""

    files: tuple[tuple[str, str], ...] = ()
    refusal: str = ""

    @property
    def chars(self) -> int:
        return sum(len(text) for _path, text in self.files)

    def evidence(self) -> list[dict[str, Any]]:
        """What a call's evidence records of them: each file's path, size and content hash, never its text."""
        import hashlib

        return [{"path": path, "chars": len(text), "sha256": hashlib.sha256(text.encode()).hexdigest()[:16]}
                for path, text in self.files]


def project_rules(cwd: str, prompt: str) -> ProjectRules:
    """The AGENTS.md (else CLAUDE.md) of the workspace root and of every folder on the way to a file
    *prompt* names, most general first (exec-1018, R-1347).

    Pi's own loader is off (`--no-context-files`, R-1344): it also read every ANCESTOR of the
    workspace, which is no part of the repository. A nested file applies because the task touches
    a file under its folder; one beside no named file does not. Over `PROJECT_RULES_MAX_CHARS` in
    all, `refusal` names the files and their sizes and nothing is delivered.
    """
    if not cwd or not os.path.isdir(cwd):
        return ProjectRules()
    root = Path(cwd)
    folders = {""}
    for rel in re.findall(r"[\w./-]+\.[A-Za-z0-9]{1,8}\b", prompt):
        folders.update(str(parent) for parent in PurePosixPath(rel).parents if str(parent) != ".")
    found: list[tuple[str, str]] = []
    for folder in sorted(folders, key=lambda f: (f.count("/") + bool(f), f)):
        if folder and not _plain_workspace_dir(root, folder):
            continue
        rel = next((f"{folder}/{name}" if folder else name for name in _CONTEXT_AGENT_FILES
                    if _plain_workspace_file(root, f"{folder}/{name}" if folder else name)), "")
        try:
            text = (root / rel).read_text(encoding="utf-8").strip() if rel else ""
        except (OSError, UnicodeDecodeError):
            text = ""
        if text:
            found.append((rel, text))
    found = _without_repeated_rules(found)
    total = sum(len(text) for _rel, text in found)
    if total > PROJECT_RULES_MAX_CHARS:
        sizes = ", ".join(f"{rel} ({len(text):,} characters)" for rel, text in found)
        return ProjectRules((), f"the repository's instructions for coding agents that apply here, {sizes}, "
                                f"hold {total:,} characters, more than the {PROJECT_RULES_MAX_CHARS:,} one call "
                                "carries whole; Remedy does not shorten binding instructions, so this call was "
                                "not started")
    return ProjectRules(tuple(found))


#: A markdown heading line: where one section of a rule file begins.
_RULES_SECTION = re.compile(r"^(?=#{1,6} )", re.MULTILINE)


def _without_repeated_rules(found: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """*found*, each deeper file's text with what an earlier file already delivers named, not repeated.

    Lossless (exec-1018b, P1 5): a file identical to an earlier one becomes one line naming it, and a
    section (from one markdown heading to the next) identical to one delivered above becomes one
    line naming its heading and file. Nothing is shortened or summarised; a nested copy of the root
    file (a common layout) is no longer sent twice in every model turn.
    """
    delivered: dict[str, str] = {}
    sections: dict[str, str] = {}
    out: list[tuple[str, str]] = []
    for rel, text in found:
        if text in delivered:
            out.append((rel, f"[identical to {delivered[text]}, delivered above]"))
            continue
        delivered[text] = rel
        parts = []
        for section in (piece for piece in _RULES_SECTION.split(text) if piece.strip()):
            body = section.strip()
            if body in sections and body.startswith("#"):
                heading = body.splitlines()[0].lstrip("#").strip()
                parts.append(f"[the section \"{heading}\" is identical to {sections[body]}'s, delivered above]")
            else:
                sections.setdefault(body, rel)
                parts.append(body)
        repeated = any(part.startswith("[the section ") for part in parts)
        out.append((rel, "\n\n".join(parts) if repeated else text))    # untouched unless a section repeats
    return out


#: What each role is told about the repository's instructions; Remedy's own rules come first.
_PROJECT_RULES_PRECEDENCE = {
    "builder": ("Follow them in how you make this change. They never widen your task, your tools or "
                "your working copy, and a workflow step they ask for (a branch, a commit, a push, a pull "
                "request) is Remedy's after review, never yours. If the task cannot be done without "
                "breaking one of them, leave that part undone and name the instruction in your answer."),
    "reviewer": ("They bind the change: fail it when it breaks one of them, and name the file and the "
                 "instruction. A workflow step they ask for (a branch, a commit, a push, a pull request) "
                 "is Remedy's after review and never a reason to fail the change."),
}


def render_project_rules(rules: ProjectRules, role: str) -> str:
    """The prompt block of *rules* for *role*: each file whole, labelled with its path, or ""."""
    if not rules.files:
        return ""
    body = "".join(f"--- {rel} ---\n{text}\n" for rel, text in rules.files)
    precedence = _PROJECT_RULES_PRECEDENCE["reviewer" if role == "reviewer" else "builder"]
    return ("\nThis repository's own instructions for coding agents, whole, from the root down (a deeper "
            f"file refines the ones above it for the files under its folder). {precedence}\n\n{body}")


def _plain_workspace_file(root: Path, rel: str) -> bool:
    """True for a regular file inside *root*, reached through no symlink and no skipped folder."""
    return _plain_workspace_path(root, rel) and (root / rel).is_file()


def _plain_workspace_dir(root: Path, rel: str) -> bool:
    return _plain_workspace_path(root, rel) and (root / rel).is_dir()


def _plain_workspace_path(root: Path, rel: str) -> bool:
    parts = PurePosixPath(rel).parts
    if not parts or rel.startswith("/") or ".." in parts or any(p in _CONTEXT_SKIP_DIRS for p in parts):
        return False
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            return False
    return path.exists()


# amend1016p D3: the reviewer judges what the change SAYS against what the task asks, not only
# that a file changed, and fails a file the task does not ask for.
_REVIEWER_PREAMBLE = (
    "You are the reviewer. You have read-only tools; you cannot edit. Judge the staged diff "
    "below against the task: does the changed text say what the task asks for, in its content "
    "and meaning, not merely in the right file? Fail a change whose wording misses the request, "
    "and fail any file the task does not ask for (a report, a copy, a manifest). The diff below "
    "is the complete change and the files it touches are shown to you: do not list or search the "
    "repository, read a file at most once and only if the diff leaves a real doubt, and do not run "
    "the tests (Remedy runs them). Every extra step resends the whole conversation, so decide in as "
    "few steps as you can. Answer in the JSON shape the end of this message requires.\n\n"
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
    session, no network at startup, and project-local executable resources stay untrusted. No
    context file either (exec-1017c, R-1344): Pi otherwise loads the workspace's and every
    ancestor's AGENTS.md or CLAUDE.md into every turn, whatever `--no-approve` says, unbounded and
    absent from Remedy's own prompt evidence; `builder_workspace_context` shows a small one instead.
    """
    return [
        pi_path, "--mode", "json", "--no-session",
        "--provider", PI_INNER_PROVIDER, "--model", model,
        "--offline", "--no-approve", "--no-extensions", "--no-mcp", "--no-skills",
        "--no-prompt-templates", "--no-themes", "--no-context-files", "--tools", tools, "--", prompt,
    ]


def ollama_host() -> str:
    """Where Ollama lives: the existing `ollama.host` key, then the environment, then the default."""
    host = os.environ.get("REMEDY_OLLAMA_HOST", "")
    if not host:
        try:
            from packages.orchestration.config import get_config
            host = str(get_config().get("ollama.host") or "")
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            host = ""    # an unreadable config falls back to the local default
    return (host or "http://localhost:11434").rstrip("/")


def pi_models_json(*, model: str) -> str:
    """Pi's model connection: the relay port inside the sandbox, never the real endpoint."""
    models = {"providers": {PI_INNER_PROVIDER: {
        "baseUrl": f"http://127.0.0.1:{SANDBOX_PROVIDER_PORT}/v1",
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
    return json.dumps(models, indent=2, sort_keys=True) + "\n"


def pi_tool_timeout_sec() -> int:
    """`pi.tool_timeout_seconds`: one shell command's deadline inside the sandbox (D2)."""
    try:
        from packages.orchestration.config import get_config
        value = int(get_config().get("pi.tool_timeout_seconds") or PI_TOOL_TIMEOUT_DEFAULT_SEC)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        value = PI_TOOL_TIMEOUT_DEFAULT_SEC    # an unreadable config keeps the documented default
    return max(value, 1)


def pi_child_env() -> dict[str, str]:
    """The environment a Pi child gets: a short allowlist plus Pi's own switches."""
    env = {key: os.environ[key] for key in _PI_ENV_ALLOWLIST if key in os.environ}
    env.update({"PI_CODING_AGENT_DIR": _PI_AGENT_DIR_INSIDE, "PI_OFFLINE": "1",
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
    try:
        require_sandbox()
    except SandboxUnavailable as exc:
        raise PiUnavailable(f"Pi's tools run only inside the tool sandbox, which is not ready "
                            f"({exc.state}): {exc}") from exc
    host = ollama_host()
    if not host.startswith("http://"):
        raise PiUnavailable(f"The model endpoint {host} is not an http:// address; the tool sandbox "
                            "relays plain http to the configured Ollama endpoint only.")
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
    from packages.orchestration.tool_sandbox import SANDBOX_READY, sandbox_self_test

    state, detail, hint = sandbox_self_test()
    checks.append(("tool_sandbox", state == SANDBOX_READY,
                   f"{state}: {detail}" + (f"; {hint}" if hint else "")))
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


def _signal_name(number: int) -> str:
    try:
        return signal.Signals(number).name
    except ValueError:
        return f"SIG{number}"


def _redacted_tail(raw: bytes) -> str:
    from packages.orchestration.stream_evidence import redact_text

    text = raw.decode("utf-8", errors="replace")
    return redact_text(text[-PI_STDERR_TAIL_CHARS:])


def bind_job_clock(job: Any) -> None:
    """Let Pi calls made for *job* read its remaining wall-clock budget and deadline (R2), and its stop (D6)."""
    from packages.core.models import JobBudgets
    from packages.orchestration.budget_guard import job_time_remaining
    from packages.orchestration.safe_points import stop_requested

    def left() -> tuple[float | None, str]:
        try:
            budgets = job.budgets if isinstance(job.budgets, JobBudgets) else (
                JobBudgets.model_validate(job.budgets) if job.budgets else None)
            started = datetime.fromisoformat(job.first_running_at) if job.first_running_at else None
        except (ValueError, TypeError):
            return None, ""
        return job_time_remaining(budgets, started)

    _JOB_TIME_LEFT.set(left)
    job_id = getattr(job, "job_id", None)
    _JOB_STOP_REQUESTED.set((lambda: stop_requested(job_id) is not None) if job_id else None)
    bind_job_token_budget(job)    # exec-1017 D4: the job's tokens left cap a call's agent loop too


def effective_pi_timeout(configured_sec: int) -> tuple[float, dict[str, Any]]:
    """``(seconds, provenance)``: the tightest positive ceiling among the configured timeout and the job clock.

    Zero or less means the job has no time left; the caller must not start Pi then.
    """
    clock = _JOB_TIME_LEFT.get()
    left, source = clock() if clock else (None, "")
    ceilings = [(float(configured_sec), "configured")] if configured_sec > 0 else []
    if left is not None:
        ceilings.append((left, source))
    seconds, bound_by = min(ceilings) if ceilings else (float(PI_DEFAULT_TIMEOUT_SEC), "default")
    return seconds, {"configured_sec": configured_sec, "job_left_sec": None if left is None else round(left, 1),
                     "job_ceiling": source, "effective_sec": round(seconds, 1), "bound_by": bound_by}


def pi_failure_text(summary: PiRunSummary | None, *, exit_code: int | None, term_signal: str | None,
                    tripped: str | None, stderr: bytes, stream_error: str) -> str:
    """The one provider_error sentence for a Pi call that did not complete, or "" when it did.

    The `provider_error:` prefix is load-bearing (finding R-0378): the loop reads a verdict of
    `blocked` as a reviewer reject unless a transport failure carries it.
    """
    tail = _redacted_tail(stderr)
    if exit_code is not None and 128 < exit_code < 160 and not term_signal:
        # Inside the sandbox Pi is not the direct child: its signal death arrives as 128 + N.
        term_signal = _signal_name(exit_code - 128)
    if tripped == "wall_timeout":
        return "provider_error: pi_timeout: the Pi call hit its wall-clock deadline"
    if tripped == "cancelled":
        return "provider_error: pi_cancelled: the job was stopped while Pi ran, and its sandbox was ended"
    if exit_code == 126 and b"tool sandbox" in stderr:
        return f"provider_error: pi_sandbox_unavailable: {_redacted_tail(stderr).strip()[-300:]}"
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

    def __init__(self, *, role: str = "builder", cwd: str | None = None, model: str = "",
                 evidence_dir: str | None = None) -> None:
        self._evidence_dir = evidence_dir
        self._role = role
        self._cwd = cwd
        self._model = model or PI_DEFAULT_MODEL
        self.last_evidence: dict[str, Any] = {}
        self._project_rules_evidence: list[dict[str, Any]] = []

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
        wall, timeout_info = effective_pi_timeout(timeout_sec)
        if wall <= 0:
            return PiCallOutcome(None, {"role": self._role, "timeout": timeout_info},
                                 "provider_error: pi_timeout: the job's time budget is already used up", 0)
        if not self._cwd:
            return PiCallOutcome(None, {"role": self._role},
                                 "provider_error: pi_unavailable: a Pi call needs its job workspace", 0)
        argv = build_pi_argv(info["pi_path"], model=self._model, tools=tools, prompt=prompt)
        tool_limit = min(pi_tool_timeout_sec(), max(int(wall), 1))
        files = {"agent/models.json": pi_models_json(model=self._model),
                 "agent/settings.json": json.dumps({"shellPath": f"{SANDBOX_RUN_DIR}/tool-shell.sh"}),
                 "tool-shell.sh": _TOOL_SHELL.format(limit=tool_limit)}
        watch = PiLoopWatch(pi_loop_limits())
        with provider_sandbox(self._cwd, info["host"], files=files, writable=("agent",)) as (
                sandbox, relay_argv):
            guarded = run_guarded([*relay_argv, *argv], ExecGuardPolicy(
                wall_timeout_seconds=wall, cwd=self._cwd, core_file_bytes=0,
                output_cap_bytes=PI_STDOUT_CAP_BYTES, env=pi_child_env(),
                env_allowlist=_PI_ENV_ALLOWLIST + (
                    "PI_CODING_AGENT_DIR", "PI_OFFLINE", "PI_SKIP_VERSION_CHECK", "PI_TELEMETRY"),
                sandbox=sandbox, cancel_check=watch.cancel_check(_JOB_STOP_REQUESTED.get()),
                stdout_observer=watch.feed))
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
        if watch.tripped:
            error = f"provider_error: {PI_LOOP_LIMIT_MARK}: {watch.tripped}"
        # A loop ended by its cap, a stop, a timeout or a crash still used what its stream measured:
        # the turns and tokens received before the end are real and count against the budgets.
        summary = summary if summary is not None else watch.summary()
        duration_ms = int((time.monotonic() - started) * 1000)
        evidence = {
            "role": self._role, "provider": PI_PROVIDER_NAME, "inner_provider": PI_INNER_PROVIDER,
            "model": self._model, "pi_path": info["pi_path"], "pi_version": info["pi_version"],
            "tools": tools, "cwd": self._cwd or "", "sandbox": "bwrap", "exit_code": guarded.returncode,
            "term_signal": guarded.term_signal, "duration_ms": duration_ms,
            "stop_reason": summary.stop_reason if summary else "",
            "model_turns": summary.model_turns if summary else 0,
            "tool_calls": list(summary.tool_calls) if summary else [],
            "tool_errors": summary.tool_errors if summary else 0,
            "timeout": timeout_info, "tool_timeout_sec": tool_limit,
            "retries": summary.retries if summary else 0,
            "usage": dict(summary.usage) if summary else {},
            "settled": bool(summary and summary.settled), "error": error[:300],
            "loop_limits": watch.limits.to_json(), "loop_limit_tripped": watch.tripped,
            # exec-1018 (R-1347): which of the repository's instruction files this call carried.
            "project_rules": list(self._project_rules_evidence),
        }
        self.last_evidence = evidence
        self._record_call(evidence, argv, prompt)
        if summary is not None and len(summary.final_text) > max_output_chars:
            summary.final_text = summary.final_text[:max_output_chars] + "\n[OUTPUT TRUNCATED]"
        return PiCallOutcome(summary, evidence, error, duration_ms)

    def _record_call(self, evidence: dict[str, Any], argv: list[str], prompt: str) -> None:
        """Append this call to `<run dir>/pi/<role>.jsonl`; the prompt is a hash, never the text."""
        if not self._evidence_dir:
            return
        import hashlib

        shown = [f"<prompt sha256:{hashlib.sha256(prompt.encode()).hexdigest()[:16]} "
                 f"{len(prompt.encode())} bytes>" if a == prompt else a for a in argv]
        try:
            target = Path(self._evidence_dir) / "pi"
            target.mkdir(parents=True, exist_ok=True)
            with open(target / f"{self._role}.jsonl", "a", encoding="utf-8") as fh:
                fh.write(json.dumps({**evidence, "argv": shown}, sort_keys=True) + "\n")
        except OSError:
            pass    # evidence is best effort; a full disk must not fail the call it describes

    def _usage_actuals(self, outcome: PiCallOutcome) -> dict[str, Any] | None:
        summary = outcome.summary
        if summary is None or not summary.model_turns:
            return None
        return {"input_tokens": summary.usage["input"], "output_tokens": summary.usage["output"],
                "total_tokens": summary.usage["totalTokens"],
                "cache_read_input_tokens": summary.usage["cacheRead"],
                "cache_creation_input_tokens": summary.usage["cacheWrite"],
                # exec-1017 D3: the attempt record's own counter names; without them every Pi call
                # read "unmeasured" in `remedy stats calls` although Pi measured all four figures.
                "cache_read": summary.usage["cacheRead"], "cache_creation": summary.usage["cacheWrite"],
                "total_cost_usd": 0.0, "model_turns": summary.model_turns,
                "parse_source": "pi_json_events"}

    def _rules_refusal(self, prompt: str) -> str:
        """The error that keeps this call from starting because the repository's instructions cannot be
        delivered whole (exec-1018, R-1347), or ""; the delivered files' provenance goes into the
        call's evidence either way."""
        rules = project_rules(self._cwd, prompt)
        self._project_rules_evidence = rules.evidence()
        return f"provider_error: {PROJECT_RULES_TOO_LARGE_MARK}: {rules.refusal}" if rules.refusal else ""

    def _failed_call_actuals(self, outcome: PiCallOutcome) -> dict[str, Any] | None:
        """What a failed call's stream measured, so its tokens count against the budgets; None when
        it reported no tokens at all (an unknown use is never recorded as a measured zero)."""
        actuals = self._usage_actuals(outcome)
        return actuals if actuals and actuals["total_tokens"] else None

    def build(self, prompt: str, *, timeout_sec: int = PI_DEFAULT_TIMEOUT_SEC, max_output_chars: int = 50000,
              resume: str | None = None) -> BuilderOutput:
        full = _BUILDER_PREAMBLE + builder_workspace_context(self._cwd, prompt) + prompt
        fingerprint = prepare_call_input(
            prompt=full, model=self._model, mode=_PI_CALL_MODE,
            options={"tools": pi_role_tools(self._role), "inner_provider": PI_INNER_PROVIDER})
        if refused := self._rules_refusal(prompt):
            return BuilderOutput(error=refused, provider=PI_PROVIDER_NAME, actual_missing_reason="provider_error",
                                 prepared_input=fingerprint)
        outcome = self._call(full, timeout_sec=timeout_sec, max_output_chars=max_output_chars)
        capped = PI_LOOP_LIMIT_MARK in outcome.error and outcome.summary is not None
        if outcome.error and not capped:
            failed = self._failed_call_actuals(outcome)
            return BuilderOutput(error=outcome.error, provider=PI_PROVIDER_NAME,
                                 duration_ms=outcome.duration_ms, usage_actuals=failed,
                                 actual_missing_reason="" if failed else "provider_error",
                                 prepared_input=fingerprint)
        summary = outcome.summary
        assert summary is not None  # an empty error means the stream parsed
        actuals = self._usage_actuals(outcome)
        final_text = summary.final_text
        if capped:
            # Lab order of 2026-10-17: the loop cap cut a builder that had ALREADY written the
            # correct edit, and the task ended budget_exhausted with no review. The cap still
            # ends the loop; what the builder wrote goes to the reviewer, who judges the diff
            # (an unchanged workspace fails there as before). The evidence keeps the trip.
            final_text = (f"{final_text}\n\nRemedy ended this builder loop at its cap "
                          f"({outcome.error.split(PI_LOOP_LIMIT_MARK + ': ', 1)[-1]}); "
                          "the edits it wrote are kept for review.").strip()
        # `files_changed` stays empty on purpose: the workspace diff is the authority, never
        # a list the assistant claimed.
        return BuilderOutput(
            summary=final_text[:500], files_changed=[], raw_text=final_text,
            provider=PI_PROVIDER_NAME, duration_ms=outcome.duration_ms,
            tokens_used=summary.usage["totalTokens"], usage_actuals=actuals,
            actual_missing_reason="" if actuals else "provider_actuals_unavailable",
            prepared_input=fingerprint)

    def review(self, prompt: str, *, timeout_sec: int = PI_DEFAULT_TIMEOUT_SEC, max_output_chars: int = 50000,
               resume: str | None = None) -> ReviewerOutput:
        # Lab calc order of 2026-10-17: the reviewer spent 12 turns and 51,469 tokens on ls, read and grep.
        full = (_REVIEWER_PREAMBLE + builder_workspace_context(self._cwd, prompt, role="reviewer") + prompt
                + "\n\n" + _REVIEWER_JSON_SCHEMA)
        fingerprint = prepare_call_input(
            prompt=full, model=self._model, mode=_PI_CALL_MODE,
            options={"tools": pi_role_tools("reviewer"), "inner_provider": PI_INNER_PROVIDER})
        if refused := self._rules_refusal(prompt):
            return ReviewerOutput(error=refused, error_class="provider_error", provider=PI_PROVIDER_NAME,
                                  actual_missing_reason="provider_error", prepared_input=fingerprint)
        outcome = self._call(full, timeout_sec=timeout_sec, max_output_chars=max_output_chars)
        if outcome.error:
            failed = self._failed_call_actuals(outcome)
            return ReviewerOutput(error=outcome.error, error_class="provider_error",
                                  provider=PI_PROVIDER_NAME, duration_ms=outcome.duration_ms, usage_actuals=failed,
                                  actual_missing_reason="" if failed else "provider_error",
                                  prepared_input=fingerprint)
        summary = outcome.summary
        assert summary is not None
        out = _parse_reviewer_json(summary.final_text, outcome.duration_ms,
                                   summary.usage["totalTokens"], provider=PI_PROVIDER_NAME)
        actuals = self._usage_actuals(outcome)
        out.usage_actuals = actuals
        out.actual_missing_reason = "" if actuals else "provider_actuals_unavailable"
        out.prepared_input = fingerprint
        return out


def make_pi_provider(role: str, *, cwd: str | None, model: str = "",
                     evidence_dir: str | None = None) -> PiProvider:
    """Construct a role's Pi provider after the D4 prerequisites hold; raises PiUnavailable.

    The construction check is the one that runs BEFORE any model call: an absent executable, a
    missing model or an unreachable endpoint stops the run here, with the corrective action.
    """
    chosen = model or PI_DEFAULT_MODEL
    pi_preflight(model=chosen, workspace=cwd, role=role)
    return PiProvider(role=role, cwd=cwd, model=chosen, evidence_dir=evidence_dir)

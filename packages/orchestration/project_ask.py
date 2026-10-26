"""A question to a project, answered by the Claude Code CLI that may only read (amend1026, Part C2).

`POST /api/v1/projects/{project}/ask` and `remedy client ask <project> <question> --json` answer
it. Remedy starts the Claude Code CLI ONLY READING in the project's repository: its command line
names the built-in tools `Read`, `Glob` and `Grep` and no other (`--tools` offers only those,
`--allowedTools` permits only those), `--restricted` removes every tool that runs a command and
keeps the file tools inside the working directory, and `--safe-mode` with `--strict-mcp-config`
loads no hook, skill, plugin or MCP server that could add a tool. There is no Edit, no Write, no
Bash and no git. The answer is the CLI's Markdown, with the tokens and calls it used and its model.

The call is capped by `max_total_tokens`, counted as the order budget counts them (input plus
output tokens, `order_budget_used`); the four kinds are reported beside it. The stream is read
while it runs, and the CLI is ended as soon as the count passes the cap. The question, the
answer, every tool call and the redacted stream are kept as evidence under the DATA ROOT,
`evidence/asks/<ask id>/`, never in the project. The repository's git state is read before and
after the call; an ask that left it changed answers `ask_repo_changed`.

Remedy deliberately offers no attachments: the public HTTP API has no upload route, so a client
has no file inside the data root to name (operator amendment amend1026, finding of Part C2).
"""
from __future__ import annotations

import hashlib
import json
import secrets
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

#: The only tools the CLI is offered and permitted: it reads and searches, and nothing else.
ASK_TOOLS: tuple[str, ...] = ("Read", "Glob", "Grep")
#: The cap a question runs under when the command line names none.
ASK_MAX_TOTAL_TOKENS_DEFAULT = 150_000
#: The longest one ask may run, and the public API waits for it.
ASK_TIMEOUT_SECONDS = 900
#: The data-root class the evidence lives in, and its folder of asks.
ASK_EVIDENCE_CLASS = "evidence"
ASK_EVIDENCE_FOLDER = "asks"
#: The most stream bytes one ask keeps; a longer stream is cut and says so.
ASK_STREAM_CAP_BYTES = 32 * 1024 * 1024

#: The top-level keys of the answer beside the envelope's own.
PROJECT_ASK_ANSWER_KEYS: tuple[str, ...] = (
    "answer", "ask_id", "calls_used", "evidence", "model", "project", "repo_unchanged", "tokens",
    "tokens_used", "tool_calls", "turns")
#: Every refusal an ask answers, sorted.
PROJECT_ASK_REFUSAL_TOKENS: tuple[str, ...] = (
    "ask_budget_exhausted", "ask_failed", "ask_provider_unavailable", "ask_repo_changed", "ask_repo_unknown",
    "invalid_argument", "project_not_found")
#: The keys under them, as the machine client interface declares them.
PROJECT_ASK_KEY_TREE: dict[str, Any] = {
    "tokens": {"input": {}, "output": {}, "cache_creation": {}, "cache_read": {}},
}

_PROMPT = (
    "You answer one question about the software repository in your working directory. You may only "
    "read it: use the tools Read, Glob and Grep and nothing else, and change nothing. Answer in Markdown "
    "in the language of the question. Name every file your answer rests on by its path relative to the "
    "repository, and say plainly when the repository does not answer the question.\n\nQUESTION:\n")


class ProjectAskError(Exception):
    """An ask that was refused or failed, with its refusal token and, once it ran, what it used."""

    def __init__(self, error: str, message: str, **fields: Any) -> None:
        super().__init__(message)
        self.error, self.message, self.fields = error, message, fields


def build_ask_argv(claude_path: str, prompt: str) -> list[str]:
    """The Claude Code CLI's command line for one ask: the three reading tools and no other."""
    tools = ",".join(ASK_TOOLS)
    return [claude_path, "-p", prompt, "--output-format", "stream-json", "--verbose",
            "--tools", tools, "--allowedTools", tools, "--restricted", "--strict-mcp-config",
            "--safe-mode", "--no-session-persistence"]


def ask_prompt(question: str) -> str:
    return _PROMPT + question.strip()


@dataclass
class _StreamReading:
    """What the CLI's stream-json told so far: usage per message, tool calls, the result."""

    cap: int
    pending: bytes = b""
    usage_by_message: dict[str, dict[str, int]] = field(default_factory=dict)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    result: dict[str, Any] | None = None
    model: str | None = None
    lines: list[str] = field(default_factory=list)

    def tokens_used(self) -> int:
        return sum(u.get("input", 0) + u.get("output", 0) for u in self.usage_by_message.values())

    def over_cap(self) -> bool:
        return self.tokens_used() > self.cap

    def feed(self, chunk: bytes) -> None:
        self.pending += chunk
        *complete, self.pending = self.pending.split(b"\n")
        for raw in complete:
            self._line(raw.decode("utf-8", errors="replace"))

    def finish(self) -> None:
        if self.pending.strip():
            self._line(self.pending.decode("utf-8", errors="replace"))
        self.pending = b""

    def _line(self, text: str) -> None:
        if not text.strip():
            return
        self.lines.append(text)
        try:
            event = json.loads(text)
        except ValueError:
            return
        if not isinstance(event, dict):
            return
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            self.model = str(event.get("model") or "") or self.model
        elif kind == "assistant":
            message = event.get("message") or {}
            usage = message.get("usage") or {}
            if isinstance(usage, dict) and message.get("id"):
                self.usage_by_message[str(message["id"])] = _kinds(usage)
            for block in message.get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    self.tool_calls.append({"tool": str(block.get("name") or ""), "input": block.get("input")})
        elif kind == "result":
            self.result = event


def _kinds(usage: dict[str, Any]) -> dict[str, int]:
    def figure(key: str) -> int:
        value = usage.get(key)
        return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0

    return {"input": figure("input_tokens"), "output": figure("output_tokens"),
            "cache_creation": figure("cache_creation_input_tokens"), "cache_read": figure("cache_read_input_tokens")}


def repository_state(repo: Path) -> dict[str, Any]:
    """What `git` says of REPO: its HEAD, its status lines and a digest of its diff against HEAD."""
    from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded

    def git(*args: str) -> bytes | None:
        result = run_guarded(["git", "-C", str(repo), *args],
                             ExecGuardPolicy(wall_timeout_seconds=60, cwd=str(repo)))
        return result.stdout if result.returncode == 0 else None

    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain=v1", "-uall")
    diff = git("diff", "HEAD", "--binary")
    return {"head": head.decode().strip() if head is not None else None,
            "status": status.decode("utf-8", errors="replace").splitlines() if status is not None else None,
            "diff_sha256": hashlib.sha256(diff).hexdigest() if diff is not None else None}


def _resolve_project(selector: str) -> tuple[Any, Path]:
    from packages.orchestration.project_registry import list_projects_readonly

    found = [p for p in list_projects_readonly() if selector in (p.slug or "", str(p.id))]
    if len(found) != 1:
        raise ProjectAskError("project_not_found", f"no one registered project is named {selector!r}; "
                              "see remedy client projects")
    project = found[0]
    repo = project.canonical_repo_path or (project.repo_paths[0] if project.repo_paths else "")
    if not repo or not Path(repo).is_dir():
        raise ProjectAskError("ask_repo_unknown", f"project {selector!r} has no repository on this machine")
    return project, Path(repo)


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def ask_project(selector: str, question: str, *, max_total_tokens: int = ASK_MAX_TOTAL_TOKENS_DEFAULT,
                asked_by: str = "cli", claude_path: str | None = None,
                root: Path | None = None) -> dict[str, Any]:
    """Ask SELECTOR's repository QUESTION through the read-only CLI; the answer `remedy client ask`
    prints. Raises `ProjectAskError` for a refusal, a failed call, a passed cap or a changed repository."""
    from packages.orchestration.data_paths import data_class_dir
    from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded
    from packages.orchestration.stream_evidence import redact_stream_line, redact_text

    if not question.strip():
        raise ProjectAskError("invalid_argument", "the question is empty")
    if max_total_tokens <= 0:
        raise ProjectAskError("invalid_argument", "max_total_tokens must be a whole number above zero")
    project, repo = _resolve_project(selector)
    claude = claude_path or shutil.which("claude")
    if not claude:
        raise ProjectAskError("ask_provider_unavailable", "the Claude Code CLI is not on this server's PATH")
    started = datetime.now(timezone.utc)
    ask_id = f"ask-{started:%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}"
    folder = data_class_dir("evidence", root) / ASK_EVIDENCE_FOLDER / ask_id     # ASK_EVIDENCE_CLASS
    folder.mkdir(parents=True, mode=0o700)
    prompt = ask_prompt(question)
    argv = build_ask_argv(claude, prompt)
    before = repository_state(repo)
    _write_json(folder / "question.json", {
        "ask_id": ask_id, "project": project.slug, "repo_path": str(repo), "asked_by": asked_by,
        "question": question, "max_total_tokens": max_total_tokens, "started_at": started.isoformat(),
        "argv": [part if part != prompt else "<prompt>" for part in argv[1:]], "repo_before": before})
    (folder / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    reading = _StreamReading(cap=max_total_tokens)
    guarded = run_guarded(argv, ExecGuardPolicy(
        wall_timeout_seconds=ASK_TIMEOUT_SECONDS, cwd=str(repo), output_cap_bytes=ASK_STREAM_CAP_BYTES,
        stdout_observer=reading.feed, cancel_check=reading.over_cap))
    reading.finish()
    after = repository_state(repo)
    (folder / "stream.jsonl").write_text("".join(redact_stream_line(line) + "\n" for line in reading.lines),
                                         encoding="utf-8")
    with open(folder / "tool_calls.jsonl", "w", encoding="utf-8") as handle:
        for call in reading.tool_calls:
            handle.write(json.dumps(call, sort_keys=True, ensure_ascii=False) + "\n")
    result = reading.result or {}
    totals = _kinds(result["usage"]) if isinstance(result.get("usage"), dict) else {
        kind: sum(u[kind] for u in reading.usage_by_message.values())
        for kind in ("input", "output", "cache_creation", "cache_read")}
    answer = str(result.get("result") or "")
    model = reading.model or next(iter(result.get("modelUsage") or {}), None)
    used = {"ask_id": ask_id, "project": project.slug, "tokens": totals,
            "tokens_used": totals["input"] + totals["output"], "calls_used": 1,
            "turns": result.get("num_turns"), "model": model,
            "tool_calls": [call["tool"] for call in reading.tool_calls],
            "repo_unchanged": before == after, "evidence": f"{ASK_EVIDENCE_CLASS}/{ASK_EVIDENCE_FOLDER}/{ask_id}"}
    error = ""
    if before != after:
        error = "ask_repo_changed"
    elif guarded.tripped_limit == "cancelled":
        error = "ask_budget_exhausted"
    elif guarded.returncode != 0 or result.get("is_error") or not answer.strip():
        error = "ask_failed"
    (folder / "answer.md").write_text(answer + ("\n" if answer and not answer.endswith("\n") else ""),
                                      encoding="utf-8")
    _write_json(folder / "result.json", {
        **used, "error": error or None, "returncode": guarded.returncode, "tripped_limit": guarded.tripped_limit,
        "wall_seconds": round(guarded.wall_seconds, 3), "repo_after": after,
        "permission_denials": result.get("permission_denials") or [],
        "stderr": redact_text(guarded.stderr.decode("utf-8", errors="replace"))[-4000:],
        "ended_at": datetime.now(timezone.utc).isoformat()})
    if error == "ask_repo_changed":
        raise ProjectAskError(error, f"the repository of {project.slug!r} changed during the ask; "
                              f"see {used['evidence']}", **used)
    if error == "ask_budget_exhausted":
        raise ProjectAskError(error, f"the ask passed its cap of {max_total_tokens} tokens and was ended; "
                              f"see {used['evidence']}", **used)
    if error:
        raise ProjectAskError(error, f"the Claude Code CLI gave no answer (exit {guarded.returncode}); "
                              f"see {used['evidence']}", **used)
    return {**used, "answer": answer}

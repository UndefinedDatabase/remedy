"""The claude CLI's command line: the argv a `claude -p` worker call starts with (F302).

Moved unchanged out of `packages/orchestration/pingpong_provider.py` by DECISION F302 D1, under
rule 2 of the structure rule, so that the switches F302 adds to the worker's command line land
here and the provider's file, which may only shrink, does not grow. Every consumer imports these
names from here (operator amendment amend1014-luna-mission-fixes D.2).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_VALID_CLI_WRITE_MODES = frozenset({"none", "allowed-tools", "dangerous-skip"})

_ALLOWED_TOOLS_ARGS = ["--allowedTools", "Edit,Write,MultiEdit"]
_DANGEROUS_SKIP_ARGS = ["--dangerously-skip-permissions"]

#: Operator amendment amend1024-one-real-order, C1: the commands a claude-cli builder with
#: `allowed-tools` may run itself, as command beginnings; every other command is refused by the
#: CLI and logged (`log_builder_command_refusals`). `docs/system/tool-sandbox-v1.md`, "What the
#: builder may run itself", says why each is here. `dangerous-skip` keeps every tool, unchanged.
BUILDER_COMMAND_ALLOWLIST: tuple[str, ...] = (
    "git status", "git diff", "git log", "ls", "cat", "head", "tail", "wc", "grep", "rg",
    "python -m py_compile", "python3 -m py_compile", "pnpm build", "pnpm lint",
)
#: The test commands a builder may run when the project names none of its own: pytest under
#: either spelling of the interpreter (a machine may carry only `python3`) and `pnpm test`.
BUILDER_FALLBACK_TEST_COMMANDS: tuple[str, ...] = ("python -m pytest", "python3 -m pytest", "pnpm test")
#: The evidence file a builder's refused commands are appended to, beside the run's isolation line.
BUILDER_COMMAND_REFUSALS_FILENAME = "builder_command_refusals.jsonl"


def builder_test_commands(workspace: str | None) -> tuple[str, ...]:
    """The project's own test command (`project_tests.find_project_test_command`, which reads the
    `[tests]` table of `.remedy/config.toml` first) followed by `BUILDER_FALLBACK_TEST_COMMANDS`."""
    from packages.orchestration.project_tests import ProjectTestConfigError, find_project_test_command

    found = None
    if workspace:
        try:
            found = find_project_test_command(Path(workspace), "python3")
        except (ProjectTestConfigError, OSError):
            found = None
    own = (" ".join(found.argv),) if found is not None and not found.unrunnable else ()
    return tuple(dict.fromkeys((*own, *BUILDER_FALLBACK_TEST_COMMANDS)))


def builder_command_allowed(command: str, allowlist: tuple[str, ...]) -> bool:
    """True when COMMAND begins with one of ALLOWLIST's commands, word for word, and chains nothing.

    The Claude Code CLI holds its own `Bash(<prefix>:*)` rules; this is Remedy's reading of the
    same list, used to classify what the CLI refused. A command joined with `;`, `&&`, `||`, a pipe,
    a redirection or a substitution is never allowed by its first word alone.
    """
    text = command.strip()
    if not text or re.search(r"[;&|<>`]|\$\(", text):
        return False
    return any(text == prefix or text.startswith(prefix + " ") for prefix in allowlist)


def builder_bash_rules(workspace: str | None) -> list[str]:
    """The `--allowedTools` rules of the builder's Bash: one `Bash(<command>:*)` per allowed command."""
    return [f"Bash({command}:*)" for command in (*builder_test_commands(workspace), *BUILDER_COMMAND_ALLOWLIST)]


def log_builder_command_refusals(raw: str, path: str | None) -> list[dict[str, Any]]:
    """Append every Bash call the CLI refused, as its JSON envelope's `permission_denials` lists
    it, to PATH (one JSON line each, with the command and whether the list would allow it); the
    refusals, also when PATH is None. A reply that is not such an envelope refuses nothing."""
    try:
        envelope = json.loads(raw)
    except (TypeError, ValueError):
        return []
    denials = envelope.get("permission_denials") if isinstance(envelope, dict) else None
    refused = [{"tool": str(denial.get("tool_name", "")),
                "command": str((denial.get("tool_input") or {}).get("command", ""))[:500]}
               for denial in denials or () if isinstance(denial, dict)]
    if path and refused:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as handle:
            for line in refused:
                handle.write(json.dumps({**line, "reason": "outside the builder's command list"},
                                        sort_keys=True) + "\n")
    return refused

#: The model name a claude-cli call is fingerprinted under when no model is set: the CLI then
#: runs its own default, and a run manifest refuses an empty model (R-1162). It names the
#: fingerprint only; no `--model` switch is added to the command line.
CLAUDE_CLI_UNSET_MODEL = "claude-cli-default"

#: The built-in tools a worker's role uses (DECISION F302 D2): a reader reads and searches, and a
#: builder that may write also edits. Claude Code describes every tool it offers in each call's
#: context, so the others are left out unless the key `claude_cli.all_tools` is true.
_READER_TOOLS = "Read,Glob,Grep"
_WRITER_TOOLS = "Read,Glob,Grep,Edit,Write,MultiEdit,Bash"


def _claude_cli_flag(config: Any, key: str) -> bool:
    """A boolean key read as `push_after_mission_enabled` reads one: a string is true only for
    ``1``, ``true`` or ``yes``, and any value Remedy cannot read is false."""
    if config is None:
        from packages.orchestration.config import get_config

        config = get_config()
    value = config.get(key)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes")
    return False


def claude_cli_launch_switches(write_mode: str, *, config: Any = None) -> list[str]:
    """The switches that keep a worker's first call lean (F302 T003, DECISION F302 D2).

    `--safe-mode` unless `claude_cli.customizations` is true, and `--tools` naming the role's
    tools unless `claude_cli.all_tools` is true; a builder started with dangerous-skip keeps every
    tool, because the operator gave it the right to run commands. `config` defaults to the
    process's cached `get_config()`, the same reading every call of the process makes.
    """
    switches: list[str] = []
    if not _claude_cli_flag(config, "claude_cli.customizations"):
        switches.append("--safe-mode")
    if write_mode != "dangerous-skip" and not _claude_cli_flag(config, "claude_cli.all_tools"):
        switches.extend(["--tools", _WRITER_TOOLS if write_mode == "allowed-tools" else _READER_TOOLS])
    return switches


#: Read back from run records on disk; must never become an option of the child's command line.
_CLI_SESSION_REF_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z_-]{0,127}")


def build_claude_cli_args(
    claude_path: str,
    prompt: str,
    *,
    write_mode: str = "none",
    model: str = "",
    stream_evidence: bool = False,
    json_schema: str = "",
    resume_session: str = "",
    config: Any = None,
    workspace: str | None = None,
) -> list[str]:
    """Build safe CLI argv for claude invocation.

    write_mode:
      none: no write tools (reviewer mode, or builder without permission)
      allowed-tools: --allowedTools Edit,Write,MultiEdit and the builder's Bash rules
        (`builder_bash_rules` of ``workspace``, amend1024 C1)
      dangerous-skip: --dangerously-skip-permissions (explicit opt-in only)
    model: if non-empty, passed as --model <model> to claude CLI.
    stream_evidence: opt-in F004 mode. Uses ``--output-format stream-json``
      (which the CLI requires ``--verbose`` for in print mode). The DEFAULT
      remains ``--output-format json`` — the accepted F003 behaviour.
    json_schema: F005 native structured output. When non-empty, passed as
      ``--json-schema <schema>`` so the provider enforces the schema itself
      instead of relying on prompt prose. Kept compact by the caller.
    resume_session: F287 DECISION D2. When non-empty, must fully match ``_CLI_SESSION_REF_PATTERN`` (else ``ValueError``), and is passed as ``--resume <ref>``.
    config: F302 DECISION D2. The configuration `claude_cli_launch_switches` reads; the switches
      it answers end every command line.
    """
    if stream_evidence:
        argv = [claude_path, "-p", prompt, "--output-format", "stream-json", "--verbose"]
    else:
        argv = [claude_path, "-p", prompt, "--output-format", "json"]
    if model:
        argv.extend(["--model", model])
    if json_schema:
        argv.extend(["--json-schema", json_schema])
    if resume_session:
        if _CLI_SESSION_REF_PATTERN.fullmatch(resume_session) is None:
            raise ValueError(
                "refusing to resume: the session reference is not a plain session id"
            )
        argv.extend(["--resume", resume_session])
    if write_mode == "allowed-tools":
        argv.extend([*_ALLOWED_TOOLS_ARGS, *builder_bash_rules(workspace)])
    elif write_mode == "dangerous-skip":
        argv.extend(_DANGEROUS_SKIP_ARGS)
    argv.extend(claude_cli_launch_switches(write_mode, config=config))
    return argv

# F005 Finding 6: there is deliberately NO ``claude --help`` preflight. Claude
# Code's help does not list every supported flag, so its absence is not proof
# ``--json-schema`` is unsupported. Support is proven by the actual invocation;
# an unknown-option error from that invocation is classified ``config`` (see
# ``_looks_like_unknown_json_schema_option`` / ``_call_reviewer_structured``).

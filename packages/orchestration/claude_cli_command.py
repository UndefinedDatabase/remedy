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
#: Operator amendment amend1027-green-builds A3: a builder in `-p` mode is never asked; a command
#: its `--allowedTools` rules allow runs, every other one is refused at once and logged, instead of
#: waiting for an approval nobody gives. `--dangerously-skip-permissions` stays its own write mode.
_NO_PROMPT_ARGS = ["--permission-mode", "dontAsk"]
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
#: amend1027 A1: the spellings a `package.json` project's tests run under, each with any arguments.
BUILDER_NODE_TEST_COMMANDS: tuple[str, ...] = (
    "pnpm test", "pnpm run test", "pnpm vitest", "pnpm exec vitest", "pnpm exec playwright test",
    "npx vitest", "npx playwright test", "npm test", "npm run test", "vitest", "playwright test",
)
#: amend1027 A1: the spellings a Python project's tests run under, the project's own venv included.
BUILDER_PYTHON_TEST_COMMANDS: tuple[str, ...] = (
    "pytest", "python -m pytest", "python3 -m pytest", "uv run pytest", ".venv/bin/pytest",
    ".venv/bin/python -m pytest",
)
#: What each source of `find_project_test_command` adds beside the found command.
_RUNNERS_BY_SOURCE: dict[str, tuple[str, ...]] = {
    "package_json": BUILDER_NODE_TEST_COMMANDS, "tests_folder": BUILDER_PYTHON_TEST_COMMANDS,
    "go_module": ("go test",), "cargo_manifest": ("cargo test",),
}
#: A `package.json` script whose name starts so runs tests (`test`, `test:unit`, `e2e`).
_TEST_SCRIPT_PREFIXES = ("test", "e2e")
#: The evidence file a builder's refused commands are appended to, beside the run's isolation line.
BUILDER_COMMAND_REFUSALS_FILENAME = "builder_command_refusals.jsonl"


def builder_test_commands(workspace: str | None) -> tuple[str, ...]:
    """The test commands the builder may run: the project's found one first, then its spellings.

    The found command is `project_tests.find_project_test_command`'s, in its order (the `[tests]`
    table, the `package.json` test script, go, cargo, pytest); a Python interpreter path in it is
    written `python`. Then, by where it was found, the runner spellings (`_RUNNERS_BY_SOURCE`, a
    configured pytest command counting as Python), a `package.json`'s test scripts under `pnpm`,
    `pnpm run` and `npm run` (amend1027 A1), and `BUILDER_FALLBACK_TEST_COMMANDS` last.
    """
    from packages.orchestration.project_tests import ProjectTestConfigError, find_project_test_command

    found = None
    if workspace:
        try:
            found = find_project_test_command(Path(workspace), "python")
        except (ProjectTestConfigError, OSError):
            found = None
    own = (" ".join(found.argv),) if found is not None and not found.unrunnable else ()
    source = found.source if found is not None else ""
    if source == "config" and "pytest" in own[0]:
        source = "tests_folder"
    scripts = _package_test_scripts(Path(workspace)) if workspace else ()
    named = tuple(f"{runner} {name}" for name in scripts for runner in ("pnpm", "pnpm run", "npm run"))
    runners = _RUNNERS_BY_SOURCE.get(source, ())
    if scripts and source != "package_json":
        runners = (*runners, *BUILDER_NODE_TEST_COMMANDS)
    return tuple(dict.fromkeys((*own, *runners, *named, *BUILDER_FALLBACK_TEST_COMMANDS)))


def _package_test_scripts(workspace: Path) -> tuple[str, ...]:
    """The names of *workspace*'s `package.json` scripts that run tests (`_TEST_SCRIPT_PREFIXES`).

    A name is kept only when it is one plain word (letters, digits, `:`, `-`, `_`), so it can
    never widen a `Bash(<command>:*)` rule; a file that does not parse names none.
    """
    try:
        data = json.loads((workspace / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ()
    scripts = data.get("scripts") if isinstance(data, dict) else None
    if not isinstance(scripts, dict):
        return ()
    return tuple(name for name in scripts if isinstance(name, str)
                 and name.startswith(_TEST_SCRIPT_PREFIXES) and re.fullmatch(r"[\w:-]+", name))


def with_project_tools(policy: Any, cwd: str | None) -> Any:
    """*policy* with the project's tools first on `PATH` and its tests' variables (amend1027 A2).

    The child's environment is the operator's (`policy.env`, else this process's own) with
    `project_tests.project_tool_environment` of *cwd* laid over it: the project's `.venv/bin` and
    `node_modules/.bin` in front, `VIRTUAL_ENV`, and the `[tests]` table's `env`. The isolation's
    allowlist (DECISION F152 D3) is otherwise unchanged; no *cwd*, no change.
    """
    if not cwd:
        return policy
    import dataclasses
    import os

    from packages.orchestration.project_tests import project_tool_environment

    env = dict(policy.env if policy.env is not None else os.environ)
    extra = project_tool_environment(Path(cwd), env.get("PATH", ""))
    allow = policy.env_allowlist
    if allow is not None:
        allow = tuple(dict.fromkeys((*allow, *extra)))
    return dataclasses.replace(policy, env={**env, **extra}, env_allowlist=allow)


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

#: Operator amendment amend1027-green-builds C1: the config key of one claude-cli worker call's
#: time limit in minutes, and its default; the planner and the scope decision keep their own
#: shorter limit (`claude_planner.timeout_seconds`, ten minutes).
CLAUDE_CLI_CALL_TIMEOUT_KEY = "providers.claude_cli.call_timeout_minutes"
CLAUDE_CLI_CALL_TIMEOUT_MINUTES = 30


def claude_cli_call_timeout_sec(config: Any = None) -> int:
    """The configured time limit of one claude-cli worker call, in seconds (C1); a value Remedy
    cannot read as a positive whole number of minutes is the default."""
    if config is None:
        from packages.orchestration.config import get_config

        config = get_config()
    value = config.get(CLAUDE_CLI_CALL_TIMEOUT_KEY)
    minutes = value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else (
        CLAUDE_CLI_CALL_TIMEOUT_MINUTES)
    return minutes * 60


def cli_call_timeout(timeout_sec: int) -> int:
    """TIMEOUT_SEC bounded by the running job's remaining wall-clock budget (C1), never below one
    second; outside a job, or for a job with no wall-clock cap, TIMEOUT_SEC itself."""
    from packages.orchestration.pi_provider import effective_pi_timeout

    seconds, _provenance = effective_pi_timeout(int(timeout_sec))
    return max(1, int(seconds))


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
        (`builder_bash_rules` of ``workspace``, amend1024 C1), then ``--permission-mode dontAsk``
        (amend1027 A3)
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
        argv.extend([*_ALLOWED_TOOLS_ARGS, *builder_bash_rules(workspace), *_NO_PROMPT_ARGS])
    elif write_mode == "dangerous-skip":
        argv.extend(_DANGEROUS_SKIP_ARGS)
    argv.extend(claude_cli_launch_switches(write_mode, config=config))
    return argv

# F005 Finding 6: there is deliberately NO ``claude --help`` preflight. Claude
# Code's help does not list every supported flag, so its absence is not proof
# ``--json-schema`` is unsupported. Support is proven by the actual invocation;
# an unknown-option error from that invocation is classified ``config`` (see
# ``_looks_like_unknown_json_schema_option`` / ``_call_reviewer_structured``).

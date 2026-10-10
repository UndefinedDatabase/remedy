"""The claude CLI's command line: the argv a `claude -p` worker call starts with (F302).

Moved unchanged out of `packages/orchestration/pingpong_provider.py` by DECISION F302 D1, under
rule 2 of the structure rule, so that the switches F302 adds to the worker's command line land
here and the provider's file, which may only shrink, does not grow. The provider imports every
name back by name, so `from packages.orchestration.pingpong_provider import
build_claude_cli_args` keeps working.
"""

from __future__ import annotations

import re

_VALID_CLI_WRITE_MODES = frozenset({"none", "allowed-tools", "dangerous-skip"})

_ALLOWED_TOOLS_ARGS = ["--allowedTools", "Edit,Write,MultiEdit"]
_DANGEROUS_SKIP_ARGS = ["--dangerously-skip-permissions"]


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
    resume_session: F287 DECISION D2. When non-empty, must fully match ``_CLI_SESSION_REF_PATTERN`` (else ``ValueError``), and is passed as ``--resume <ref>``.
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
        argv.extend(_ALLOWED_TOOLS_ARGS)
    elif write_mode == "dangerous-skip":
        argv.extend(_DANGEROUS_SKIP_ARGS)
    return argv

# F005 Finding 6: there is deliberately NO ``claude --help`` preflight. Claude
# Code's help does not list every supported flag, so its absence is not proof
# ``--json-schema`` is unsupported. Support is proven by the actual invocation;
# an unknown-option error from that invocation is classified ``config`` (see
# ``_looks_like_unknown_json_schema_option`` / ``_call_reviewer_structured``).

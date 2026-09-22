"""The exit-code taxonomy: one meaning per code (DECISION F283 D12).

Before this module, no document gave any CLI exit code a meaning: an AST scan
of ``apps/cli/`` at ``98a85b67`` found the same literal codes written at
hundreds of sites with no shared contract behind them. D12 fixes one meaning
per code for the CLI as a whole (``CLI_EXIT_CODES``), and a second, narrower
contract for the ``runtime`` group alone (``RUNTIME_EXIT_CODES``), because a
process outside the CLI — the supervisor subprocess and
``packages/runtimes/dev_server.py`` — reads a runtime command's exit code
directly. Every other group answers the CLI table.

``apps/cli/command_catalog.py`` declares, per command, which codes above
``EXIT_CODE_FLOOR`` its handler can reach; ``tests/cli/test_exit_codes.py``
asserts that declaration against a static reading of the handler, and
``docs/guides/exit-codes.md`` is asserted equal to both tables here.

Deliberate absence (D12 (5)): this taxonomy renumbers no existing exit-code
site. A code is a contract with every script that already reads it, so an
older site that answers a not-ready condition with 1 keeps exiting 1 — the
CLI table's ``failed`` meaning already covers it, and a tidier table is not
worth breaking a shell caller.
"""

from __future__ import annotations

from typing import NamedTuple


class ExitCodeMeaning(NamedTuple):
    """One exit code, its stable name, and the one-sentence meaning it carries."""

    code: int
    name: str
    meaning: str


#: The floor every command reaches (D12 (4)): the argument parser exits 2 on a
#: malformed invocation, and the dispatch boundary exits 1 on an unhandled
#: exception, before a single line of any handler runs. 0, 1 and 2 therefore
#: need no per-command declaration; only a code above this floor does.
EXIT_CODE_FLOOR: tuple[int, ...] = (0, 1, 2)

#: D12 (1) — the CLI's own meanings, shared by every group except ``runtime``.
CLI_EXIT_CODES: tuple[ExitCodeMeaning, ...] = (
    ExitCodeMeaning(
        0, "ok",
        "The command did what it was asked, including finding nothing to do "
        "or honouring a pending stop request.",
    ),
    ExitCodeMeaning(
        1, "failed",
        "The command ran and did not do what was asked — a refusal, a failed "
        "operation, a red check, drift found; the general failure and the "
        "code of every refusal no narrower meaning claims.",
    ),
    ExitCodeMeaning(
        2, "usage",
        "The invocation itself is wrong — an unknown command, or a missing, "
        "invalid, unrecognised or conflicting argument — and nothing was "
        "attempted.",
    ),
    ExitCodeMeaning(
        3, "not_ready",
        "The invocation is well formed, but what it names is absent or not "
        "in a state the command can act on.",
    ),
    ExitCodeMeaning(
        4, "environment",
        "The machine lacks a prerequisite the command cannot supply, such as "
        "a git repository.",
    ),
)

#: D12 (2) — the ``runtime`` group's own contract. 0 and 1 mean what they mean
#: everywhere; a malformed invocation of a runtime command still exits 2, so 2
#: is repurposed here rather than reused verbatim from the CLI table.
RUNTIME_EXIT_CODES: tuple[ExitCodeMeaning, ...] = (
    ExitCodeMeaning(
        0, "ok",
        "The command did what it was asked, including finding nothing to do "
        "or honouring a pending stop request.",
    ),
    ExitCodeMeaning(
        1, "failed",
        "The command ran and did not do what was asked — a refusal, a failed "
        "operation, a red check, drift found; the general failure and the "
        "code of every refusal no narrower meaning claims.",
    ),
    ExitCodeMeaning(2, "config", "The runtime configuration is missing or invalid."),
    ExitCodeMeaning(3, "start", "The server did not start."),
    ExitCodeMeaning(4, "ready", "It started and never answered ready."),
    ExitCodeMeaning(
        5, "state",
        "A lifecycle or state failure such as a failed stop, surviving "
        "processes or an unreadable state file.",
    ),
)


def exit_codes_for_group(group_id: str) -> tuple[ExitCodeMeaning, ...]:
    """The exit-code table that governs ``group_id``'s commands (D12 (2)).

    The ``runtime`` group answers its own contract; every other group answers
    the CLI table.
    """
    if group_id == "runtime":
        return RUNTIME_EXIT_CODES
    return CLI_EXIT_CODES

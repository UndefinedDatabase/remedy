"""F272 — deleting a command is not finished until the strings that tell an
operator to run it are gone too.

F272 round 19 deleted the ``job run-loop`` command surface and its round gate
swept the DOTTED catalog id ``job.run-loop`` and the SYMBOL ``_cmd_run_loop`` to
zero. Both readings were true, and three production strings still printed
``remedy job run-loop`` as the operator's next action, because an operator types
the SPACED form that neither spelling greps for; two older sites advertised a
``remedy guide next`` that has never existed. This module is the standing guard
for that class: any ``remedy <group> <sub>`` string in tracked production code
whose pair the catalog does not carry fails the sweep here rather than in an
operator's terminal.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from apps.cli.command_catalog import CATALOG, GROUPS

#: Repository root, derived from this file rather than the working directory so
#: the sweep is the same under any invocation path.
REPO_ROOT = Path(__file__).resolve().parents[2]

#: ``remedy <group> <sub>`` as an operator types it — the spelling a catalog-id
#: or symbol grep cannot see.
_ADVERTISED_COMMAND_RE = re.compile(r"remedy\s+([a-z][a-z0-9-]*)\s+([a-z][a-z0-9-]*)")

#: A pair counts as an advertisement only when what FOLLOWS it looks like a
#: command line rather than prose: an argument placeholder, an option, a closing
#: quote, or nothing at all. Without this narrowing, ``remedy init requires a
#: git repository`` reads as a command named ``init requires``.
_COMMAND_TAIL_CHARS = "<{\"'"


def scan_advertised_commands(text: str) -> list[tuple[str, str]]:
    """Return the ``(group, subcommand)`` pairs `text` advertises as commands."""
    found: list[tuple[str, str]] = []
    for match in _ADVERTISED_COMMAND_RE.finditer(text):
        group, subcommand = match.group(1), match.group(2)
        if group not in GROUPS:
            continue
        tail = text[match.end():].lstrip(" ")
        if tail and not (tail[0] in _COMMAND_TAIL_CHARS or tail.startswith("--")):
            continue
        found.append((group, subcommand))
    return found


def _tracked_production_python_files() -> list[str]:
    """Every tracked ``.py`` under ``packages/`` and ``apps/``.

    Enumerated from ``git ls-files`` — a shell glob would silently pick up
    untracked scratch files and miss nothing else.
    """
    listing = subprocess.run(
        ["git", "ls-files", "packages", "apps"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [line for line in listing.splitlines() if line.endswith(".py")]


def collect_command_advertisements() -> tuple[int, list[str]]:
    """Sweep production code; return (advertisements seen, unresolved sites)."""
    catalog_pairs = {(entry.group_id, entry.subcommand) for entry in CATALOG}
    seen = 0
    unresolved: list[str] = []
    for relative_path in _tracked_production_python_files():
        source = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for line_number, line in enumerate(source.splitlines(), 1):
            for group, subcommand in scan_advertised_commands(line):
                seen += 1
                if (group, subcommand) not in catalog_pairs:
                    unresolved.append(f"{relative_path}:{line_number}: remedy {group} {subcommand}")
    return seen, unresolved


def test_every_advertised_command_exists_in_the_catalog() -> None:
    seen, unresolved = collect_command_advertisements()

    # Anti-blindness: a scan that matches nothing satisfies a zero-gate
    # perfectly. The real figure was 738 when this guard was written, so 100 is
    # a floor with room rather than a pin on today's count.
    assert seen > 100, f"the advertisement scan went blind: only {seen} advertisements matched"

    assert not unresolved, (
        "production code advertises commands the catalog does not carry — "
        "delete a command's advertisements in the same commit as the command:\n"
        + "\n".join(unresolved)
    )


def test_scanner_reports_a_command_the_catalog_does_not_carry() -> None:
    found = scan_advertised_commands("next_action = 'remedy job no-such-subcommand <job_id>'")

    assert found == [("job", "no-such-subcommand")]
    assert ("job", "no-such-subcommand") not in {(e.group_id, e.subcommand) for e in CATALOG}


def test_scanner_ignores_prose_that_merely_starts_with_a_group_name() -> None:
    assert scan_advertised_commands("remedy init requires a git repository") == []


def test_scanner_finds_a_real_next_action_f_string() -> None:
    found = scan_advertised_commands(
        'record.next_safe_action = f"remedy job report {record.job_id} --json"'
    )

    assert ("job", "report") in found

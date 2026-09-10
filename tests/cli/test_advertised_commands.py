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

F272 round 21 widened the sweep beyond ``.py`` to the shell scripts under
``scripts/`` and the operator-facing pages under ``docs/system/`` and
``docs/guides/``, because an operator reads a command line from a doc exactly as
they read one from a terminal.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import NamedTuple

from apps.cli.command_catalog import CATALOG, GROUPS

#: Repository root, derived from this file rather than the working directory so
#: the sweep is the same under any invocation path.
REPO_ROOT = Path(__file__).resolve().parents[2]

#: ``remedy <group> <sub>`` as an operator types it — the spelling a catalog-id
#: or symbol grep cannot see.
_ADVERTISED_COMMAND_RE = re.compile(r"remedy\s+([a-z][a-z0-9-]*)\s+([a-z][a-z0-9-]*)")

#: ``remedy <something>`` — the SINGLE-token invocation, which the two-token
#: regex above is structurally blind to. That blindness is how an invented
#: ``remedy list`` survived two rounds of a session whose subject was dead
#: advertisements: no pair regex can ever see a one-word command.
_ADVERTISED_GROUP_RE = re.compile(r"remedy\s+([a-z][a-z0-9-]*)")

#: An invocation counts as an advertisement only when what FOLLOWS it looks like
#: a command line rather than prose: an argument placeholder, an option, a
#: closing quote, a closing BACKTICK, or nothing at all. Without this narrowing,
#: ``remedy init requires a git repository`` reads as a command named ``init
#: requires``. The BACKTICK belongs here because a markdown page closes an
#: inline command with one — ``run `remedy list` `` — and omitting it hid every
#: advertisement written as an inline code span from the operator-facing sweep:
#: adding this one character raised the advertisements the scanner SEES from 641
#: to 791 over the same corpora, 150 of which had never been scanned at all.
_COMMAND_TAIL_CHARS = "<{\"'`"


def _tail_reads_as_a_command_line(text: str, end: int) -> bool:
    """Does what follows `text[:end]` read as a command line rather than prose?

    One helper for BOTH invocation forms, so the two regexes can never drift
    apart on what counts as an advertisement.
    """
    tail = text[end:].lstrip(" ")
    if not tail:
        return True
    return tail[0] in _COMMAND_TAIL_CHARS or tail.startswith("--")


def scan_advertised_commands(text: str) -> list[tuple[str, ...]]:
    """Return the invocations `text` advertises as commands.

    Two-element tuples are the ``remedy <group> <sub>`` form, one-element tuples
    the ``remedy <group>`` form. Nothing is pre-filtered against ``GROUPS``
    here: finding R-0847 records that the old ``if group not in GROUPS:
    continue`` made this scanner blind to exactly the advertisements a deletion
    feature leaves behind — once a group is deleted WHOLE, every string still
    telling an operator to run one of its commands stopped matching. Deciding
    which invocations RESOLVE is ``_resolves``'s job, not the scanner's.
    """
    found: list[tuple[str, ...]] = []
    for match in _ADVERTISED_COMMAND_RE.finditer(text):
        if not _tail_reads_as_a_command_line(text, match.end()):
            continue
        found.append((match.group(1), match.group(2)))
    for match in _ADVERTISED_GROUP_RE.finditer(text):
        if not _tail_reads_as_a_command_line(text, match.end()):
            continue
        found.append((match.group(1),))
    return found


def _resolves(invocation: tuple[str, ...]) -> bool:
    """Can the LIVE catalog run `invocation`?

    A two-element invocation must be a catalog pair. A one-element invocation
    must be a known group, because ``remedy <group>`` is the real group-help
    invocation and not a typo.
    """
    if len(invocation) == 2:
        return invocation in {(entry.group_id, entry.subcommand) for entry in CATALOG}
    return invocation[0] in GROUPS


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


#: The operator-facing corpus: the shell scripts an operator runs and the pages
#: an operator reads. NEITHER collector may reach ``tests/`` — this module's own
#: docstring quotes the very strings it forbids, so a corpus that swept the test
#: tree would fail on the guard's own prose. That exclusion is a property of the
#: corpus, not a way to make the sweep pass: no advertisement below is skipped.
_OPERATOR_FACING_ROOTS: tuple[tuple[str, str], ...] = (
    ("scripts", ".sh"),
    ("docs/system", ".md"),
    ("docs/guides", ".md"),
)


def _tracked_files_under(directory: str, suffix: str) -> list[str]:
    """Every tracked file under `directory` whose name ends in `suffix`.

    Enumerated from ``git ls-files`` — a shell glob would silently pick up
    untracked scratch files and miss nothing else.
    """
    listing = subprocess.run(
        ["git", "ls-files", directory],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [line for line in listing.splitlines() if line.endswith(suffix)]


class UnresolvedAdvertisement(NamedTuple):
    """One site advertising an invocation the live catalog cannot run."""

    path: str
    invocation: tuple[str, ...]
    line_number: int

    @property
    def key(self) -> tuple[str, str]:
        """The allowlist key: the path and the invocation, and NEVER the line
        number — a line-keyed allowlist rots on the next edit anywhere in the
        file, and would then excuse a moved advertisement while failing on the
        one that never moved."""
        return (self.path, " ".join(self.invocation))

    def __str__(self) -> str:
        return f"{self.path}:{self.line_number}: remedy {' '.join(self.invocation)}"


def _sweep(relative_paths: list[str]) -> tuple[int, list[UnresolvedAdvertisement]]:
    """Return (advertisements seen, unresolved sites) over `relative_paths`."""
    seen = 0
    unresolved: list[UnresolvedAdvertisement] = []
    for relative_path in relative_paths:
        source = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for line_number, line in enumerate(source.splitlines(), 1):
            for invocation in scan_advertised_commands(line):
                seen += 1
                if not _resolves(invocation):
                    unresolved.append(
                        UnresolvedAdvertisement(relative_path, invocation, line_number)
                    )
    return seen, unresolved


def collect_command_advertisements() -> tuple[int, list[UnresolvedAdvertisement]]:
    """Sweep production code; return (advertisements seen, unresolved sites)."""
    return _sweep(_tracked_production_python_files())


def collect_operator_facing_advertisements() -> tuple[int, list[UnresolvedAdvertisement]]:
    """Sweep the shell scripts and the operator-facing docs the same way."""
    paths: list[str] = []
    for directory, suffix in _OPERATOR_FACING_ROOTS:
        paths.extend(_tracked_files_under(directory, suffix))
    return _sweep(paths)


#: The dead advertisements the R-0847 widening EXPOSED on operator-facing pages
#: and which round 27 did not repair, held by key so that every other dead
#: advertisement in the same corpus still fails immediately. This is a RATCHET
#: in the sense DECISION F274 D1 gave the word and deliberately not a
#: suppression: every excused site is named here in full, the list may only ever
#: SHRINK (``_ALLOWLIST_CEILING``), and an entry whose advertisement is gone
#: fails too, so the list cannot go stale. It exists because widening a guard
#: and repairing four whole pages are different commits — finding R-0872 carries
#: the backlog and its fix clause. WHEN IT REACHES ZERO IT IS DELETED, together
#: with ``_ALLOWLIST_CEILING`` and
#: ``test_the_known_dead_doc_advertisement_list_only_ever_shrinks``, because a
#: ratchet at zero is a gate that cannot fail.
KNOWN_DEAD_DOC_ADVERTISEMENTS: frozenset[tuple[str, str]] = frozenset(
    (
        ('docs/system/architecture.md', 'apply-patch-intent'),
        ('docs/system/architecture.md', 'attach-project-job'),
        ('docs/system/architecture.md', 'attach-project-repo'),
        ('docs/system/architecture.md', 'attach-repo'),
        ('docs/system/architecture.md', 'brain-node'),
        ('docs/system/architecture.md', 'brain-view'),
        ('docs/system/architecture.md', 'cockpit'),
        ('docs/system/architecture.md', 'constitution'),
        ('docs/system/architecture.md', 'create-job'),
        ('docs/system/architecture.md', 'create-project'),
        ('docs/system/architecture.md', 'discover-commands'),
        ('docs/system/architecture.md', 'list-patch-intents'),
        ('docs/system/architecture.md', 'project-context'),
        ('docs/system/architecture.md', 'run-contract'),
        ('docs/system/architecture.md', 'run-tests-local'),
        ('docs/system/architecture.md', 'show-permissions'),
        ('docs/system/architecture.md', 'show-project'),
        ('docs/system/architecture.md', 'timeline'),
        ('docs/system/architecture.md', 'token-policy'),
        ('docs/system/architecture.md', 'trust-report'),
        ('docs/system/architecture.md', 'workers'),
        ('docs/system/vocabulary.md', 'absorb'),
    )
)

#: The MEASURED length of the allowlist above, written as a literal on purpose.
#: ``len(KNOWN_DEAD_DOC_ADVERTISEMENTS)`` would move with every entry added and
#: the ratchet assertion below could then never fail — a gate that cannot fail.
#: It may fall as the backlog is worked; it may never rise.
_ALLOWLIST_CEILING = 22


def test_every_advertised_command_exists_in_the_catalog() -> None:
    seen, unresolved = collect_command_advertisements()

    # Anti-blindness: a scan that matches nothing satisfies a zero-gate
    # perfectly. The real figure was 738 when this guard was written, so 100 is
    # a floor with room rather than a pin on today's count.
    assert seen > 100, f"the advertisement scan went blind: only {seen} advertisements matched"

    assert not unresolved, (
        "production code advertises commands the catalog does not carry — "
        "delete a command's advertisements in the same commit as the command:\n"
        + "\n".join(str(site) for site in unresolved)
    )


def test_every_operator_facing_advertised_command_exists_in_the_catalog() -> None:
    seen, unresolved = collect_operator_facing_advertisements()

    # Anti-blindness, exactly as the production sweep above: the real figures
    # were 88 in scripts/ and 318 in the two doc trees when this widening was
    # written, so 100 is a floor with room rather than a pin on today's count.
    assert seen > 100, f"the advertisement scan went blind: only {seen} advertisements matched"

    remainder = [
        site for site in unresolved if site.key not in KNOWN_DEAD_DOC_ADVERTISEMENTS
    ]
    assert not remainder, (
        "an operator-facing script or page advertises commands the catalog does "
        "not carry — delete a command's advertisements in the same commit as the "
        "command:\n" + "\n".join(str(site) for site in remainder)
    )


def test_the_known_dead_doc_advertisement_list_only_ever_shrinks() -> None:
    """An allowlist that may not GROW and may not go STALE is not a suppression.

    A plain skip hides a defect for as long as anyone leaves it alone. These two
    assertions make the opposite true: the list cannot take on a new excuse
    (``_ALLOWLIST_CEILING``), so a fresh dead advertisement anywhere in the
    corpus goes red at once; and it cannot keep an excuse whose advertisement
    has been repaired or deleted, so the list shrinks as the backlog is worked
    and cannot outlive it. Finding R-0872 carries the backlog itself.
    """
    assert len(KNOWN_DEAD_DOC_ADVERTISEMENTS) <= _ALLOWLIST_CEILING, (
        "the known-dead advertisement list GREW — it is a ratchet, so a new dead "
        "advertisement is repaired, never excused"
    )

    _, unresolved = collect_operator_facing_advertisements()
    live_keys = {site.key for site in unresolved}
    stale = sorted(KNOWN_DEAD_DOC_ADVERTISEMENTS - live_keys)
    assert not stale, (
        "the known-dead advertisement list excuses advertisements that are no "
        "longer there — delete the entry in the commit that repairs the site:\n"
        + "\n".join(f"{path}: remedy {invocation}" for path, invocation in stale)
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

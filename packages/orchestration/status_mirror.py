"""F053 T002 — the STATUS-mirror producer (DECISION D2).

The run report's milestone distance and capability lines are specified to come
from "the STATUS mirror".  When F053 T001 was built no such producer existed:
`docs/roadmap/STATUS.md` had no production reader anywhere in ``packages/``,
only a write fence (``scope_fences.BUILTIN_DENY``) declaring it operator
territory.  This module is that missing reader, added by DECISION D2
(docs/roadmap/features/T1_F053.md, "How it fits" amendment).

Read-only by construction: it opens the ledger, parses it, and returns a
``run_report.StatusMirror``.  It never writes that file — the fence stands, and
this module does not weaken it.

The honest-absence rule is the same one the report itself follows (P6): a
missing file, an unparseable ledger, or a ledger with no milestone line yields
``None``, and the report renders "not recorded".  A run against somebody
else's repository has no Remedy roadmap and therefore has no milestone — that
is a fact about the run, not a gap to fill with a plausible number.

Deliberate absences:
  * Remedy deliberately does not WRITE docs/roadmap/STATUS.md from any agent
    code path — it is the operator's execution ledger (A4).
  * Remedy deliberately does not hand-maintain the milestone distance: the
    number is counted from the ledger on every render, so it cannot go stale.
"""

from __future__ import annotations

import re
from pathlib import Path

from packages.orchestration.run_report import StatusMirror

#: Where the ledger lives inside a repository that has one.
STATUS_RELPATH = "docs/roadmap/STATUS.md"

#: One ledger entry: `- [x] F012 — Deterministic runs (…evidence…)`.
#: The four states are fixed by the ledger's own grammar banner:
#: `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked.
_ENTRY_RE = re.compile(r"^- \[([ x~!])\] (F\d+) — (.*)$")

#: How the milestone line names itself.  The ledger marks exactly one.
_MILESTONE_MARKER = "MILESTONE GATE"

STATE_TODO = " "
STATE_IN_PROGRESS = "~"
STATE_DONE = "x"
STATE_BLOCKED = "!"

#: The states that still count as work remaining toward the milestone.
#: Blocked (`[!]`) is deliberately NOT counted here — the amendment names
#: `[ ]`/`[~]` and a blocked line needs a human, not a countdown.
_UNCHECKED = frozenset({STATE_TODO, STATE_IN_PROGRESS})


def _title(raw: str) -> str:
    """The feature's own name, without its evidence parenthetical.

    `Deterministic runs (PR #123 · evidence: …)` -> `Deterministic runs`.
    The parenthetical is provenance, not capability, and a "can now" line
    carrying a zip filename tells a reader nothing they can use.
    """
    head = raw.split(" (", 1)[0]
    return head.strip()


def parse_status_ledger(text: str, *, milestone_id: str = "") -> StatusMirror | None:
    """Parse ledger *text* into a StatusMirror, or None if it cannot be trusted.

    *milestone_id* pins the milestone (e.g. ``"F075"``); when empty, the single
    line marked ``MILESTONE GATE`` is used.  Returns None — never a guess —
    when the text has no parseable entries or names no milestone.
    """
    entries: list[tuple[int, str, str, str]] = []
    for index, line in enumerate(text.splitlines()):
        match = _ENTRY_RE.match(line)
        if match:
            state, feature_id, raw = match.groups()
            entries.append((index, state, feature_id, _title(raw)))
    if not entries:
        return None

    milestone_index = -1
    milestone_name = ""
    for index, _state, feature_id, title in entries:
        if milestone_id:
            if feature_id == milestone_id:
                milestone_index, milestone_name = index, feature_id
                break
        elif _MILESTONE_MARKER in title:
            milestone_index, milestone_name = index, feature_id
            break
    if milestone_index < 0:
        # A ledger without the milestone it is being measured against cannot
        # answer "how far", and an unanchored count would be meaningless.
        return None

    remaining = sum(1 for index, state, _fid, _t in entries
                    if index <= milestone_index and state in _UNCHECKED)
    # P1: only accepted [x] state may become a "can now" line; [~] is work.
    accepted = tuple(title for _i, state, _fid, title in entries
                     if state == STATE_DONE and title)
    in_progress = tuple(title for _i, state, _fid, title in entries
                        if state == STATE_IN_PROGRESS and title)
    return StatusMirror(
        milestone=milestone_name,
        remaining_to_milestone=remaining,
        accepted_capabilities=accepted,
        in_progress_capabilities=in_progress,
    )


def read_status_mirror(repo_root: str | Path | None,
                       *, milestone_id: str = "") -> StatusMirror | None:
    """The StatusMirror for *repo_root*, or None when it has no ledger.

    Never raises into a render: an unreadable ledger is indistinguishable from
    an absent one as far as the report is concerned, and both render
    "not recorded".
    """
    if not repo_root:
        return None
    try:
        path = Path(repo_root) / STATUS_RELPATH
        if not path.is_file():
            return None
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError, UnicodeDecodeError):
        return None
    return parse_status_ledger(text, milestone_id=milestone_id)

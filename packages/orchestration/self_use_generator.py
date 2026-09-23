"""F258 T001 — replenishing the self-use queue without a human.

:mod:`packages.orchestration.self_use_queue` is read-only DATA by design
(DECISION F257 D2): a human curates it, and no module owns a writer. That
invariant held while the queue was a human's own list. This module is the ONE
writer the queue gains — deliberately separate from the loader, the same
separation :mod:`packages.orchestration.self_use_job` already keeps between
reading and rendering — because the day a generator can write is exactly the
day "read-only" needs a place other than the loader to stop meaning it.

The generator itself never marks anything CONSUMED: it only APPENDS a new
PENDING item when the queue is empty. Consumption stays the closure round's
own edit (DECISION F257 D2, unchanged), so a generated item still needs a
human's — or the closure round's own — decision before it is ever run.

A standing maintenance ORDER is tried first, then the three sources
``docs/roadmap/features/T5_F258.md`` T001 specifies, in that order. Of those three
only the first is real today; DECISION F258 D2 records why the other two are
honest ``None`` placeholders rather than half-built guesses:

  0. THE TOOLCHAIN REFRESH ORDER (T2_F279 T004, DECISION F279 D7).
     ``docs/orders/toolchain-refresh.md`` is itself a job file, queued VERBATIM,
     and no more than once every fourteen days: the date it was last queued is
     read back out of the provenance this tier stamps on its item. It comes
     first because the ledger tier always has an eligible finding to offer, so
     an order placed after it would never be reached.
  1. THE FINDING LEDGER. The oldest OPEN (no ``Done:`` line) Low or Medium
     finding in ``.agent/live_review.md`` that no existing queue entry already
     targets (R-0838), rendered as a job whose one task quotes the finding
     paragraph VERBATIM and whose acceptance is "repair it, or record why
     not" — never a per-finding summary this module would have to invent.
  2. A documentation-staleness catalog. Not yet built: curating a catalog of
     concrete (doc, claim, shipped-truth) checks is its own future work,
     mirroring how ``ownership`` stayed an honest empty list in F040 until
     F035 existed (DECISION F040 D3).
  3. An actionable ``remedy doctor core`` warning. Not yet reachable: today's
     ``_cmd_doctor_core`` (``apps/cli/commands/worker_facade_cmd.py``) is an
     argparse handler that prints, not an importable function returning
     structured warnings — refactoring that seam is future work too.

Public API::

    SelfUseGenerationError: a source this module needs could not be read
    default_ledger_path() -> Path
    generate_self_use_item(queue_path=None, ledger_path=None) -> SelfUseQueueEntry | None
    append_generated_item(entry, queue_path=None) -> None
    generate_and_append_if_empty(queue_path=None, ledger_path=None) -> SelfUseQueueEntry | None

Deliberate absences:
  * REMEDY DELIBERATELY DOES NOT SUMMARIZE A FINDING. The rendered job's Task 1
    body is the ledger paragraph's own bytes, unedited — the same "never
    invent" discipline the rest of this project holds findings to.
  * Remedy deliberately does not guess when a ledger paragraph might corrupt
    the job file it is embedded in: it CHECKS, by regex, for a line shaped
    like a markdown heading or an ``Acceptance:`` marker, and refuses to
    generate rather than ship a job whose task boundary the paragraph itself
    would silently move.
  * REMEDY DELIBERATELY DOES NOT JUDGE WHETHER A BUILDER CAN PERFORM A
    FINDING'S FIX (R-0784). Tier 1 has no reliable field that says a fix binds
    the reviewer's practice rather than the code, and a guess would silently
    retire findings from the track. A generated item whose fix no builder can
    make is therefore run as it is, and the run BLOCKING at the approval gate
    is the intended outcome: the gate refusing an unfinished job is the gate
    working, the closing session registers what the run surfaced, and because
    Tier 1 never re-selects a finding a queue entry already targets, such a
    finding costs the track one close and not every close after it.
  * Remedy deliberately does not call
    :func:`packages.orchestration.pingpong_job.parse_job_file` to verify the
    rendered text — that function persists a job record as a side effect
    (``_persist_job``), which a pure generation step must never trigger.
"""
from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path

from packages.orchestration.self_use_queue import (
    SelfUseQueueEntry,
    default_self_use_queue_path,
    load_self_use_queue,
    pending_self_use_items,
)

#: A registered finding line: ``- R-0418 — Low, ...``. Captures the id and
#: severity; the rest of the line (and paragraph) is read separately.
_SEVERITY_RE = re.compile(r"^- (R-\d+) — (Low|Medium|High|Critical), ", re.M)

#: A resolved finding line: ``Done: R-0418`` (the id may carry trailing text).
_DONE_RE = re.compile(r"^Done: (R-\d+)", re.M)

#: A queue item id, for finding the next free one in sequence.
_QUEUE_ID_RE = re.compile(r"^SU-(\d{3})$")

#: The provenance Tier 1 stamps on an item, and the pattern that reads the
#: targeted finding back out of it (R-0838).
_LEDGER_PROVENANCE = "generated (self-use-generator tier 1, ledger scan, {r_id})"
_LEDGER_PROVENANCE_RE = re.compile(
    r"^generated \(self-use-generator tier 1, ledger scan, (R-\d+)\)$"
)

#: THE ORDER TIER. The order file, how often it may be queued, and the provenance
#: that records the day it was, which is how the next call knows whether it is due.
ORDER_RELATIVE_PATH = "docs/orders/toolchain-refresh.md"
ORDER_CADENCE_DAYS = 14
_ORDER_PROVENANCE = "generated (self-use-generator order tier, {path}, {day})"
_ORDER_PROVENANCE_RE = re.compile(
    r"^generated \(self-use-generator order tier, (?P<path>[^,]+), (?P<day>\d{4}-\d{2}-\d{2})\)$"
)

#: Severities this generator's Tier 1 will pick from — never High or Critical,
#: which are judgement calls a generator does not make for itself.
_ELIGIBLE_SEVERITIES = ("Low", "Medium")

#: THE SENTENCE THAT MAKES A FINDING REPAIRABLE. A paragraph without one names
#: no repair, so the job rendered from it asks a builder to invent the fix and
#: the reviewer to judge an invention — which is how SU-019 to SU-023 each
#: reached the approval gate with nothing built (operator amendment
#: amend0920-selfuse-real, DECISION D2).
_FIX_SENTENCE_RE = re.compile(r"\bFIX\b\s*(?:,[^.]*?)?:", re.I)

#: WORDS THAT SAY THE FIX IS NOT THIS RUN'S TO MAKE. Each one was read off the
#: five hollow runs rather than guessed: `flaky` and `once in` mark a finding
#: whose defect does not reproduce on demand, `never captured` marks one whose
#: evidence does not exist yet, and `operator` and `waits on` mark one held by a
#: person or by another feature. A builder given any of these cannot finish, and
#: a run that cannot finish is a closure spent for nothing.
#:
#: MATCHED CASE-INSENSITIVELY, and that is load-bearing: this ledger writes a
#: finding's headline in capitals, so R-0499's own "HAS NEVER BEEN CAPTURED"
#: is invisible to a case-sensitive search for the very phrase that describes it.
#: ``never captured`` is spelled as a PATTERN for the same reason — the ledger's
#: own sentence is "has never BEEN captured", and a phrase that cannot match the
#: instance it was written for is not a filter (amend0920-selfuse-real D2).
_INELIGIBLE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"flaky", re.I),
    re.compile(r"never (?:been )?captured", re.I),
    re.compile(r"once in\b", re.I),
    re.compile(r"\boperator\b", re.I),
    re.compile(r"waits on", re.I),
)


def _is_repairable(paragraph: str) -> bool:
    """Can a builder actually finish the job this paragraph would become?

    Two questions, both answered from the paragraph's own bytes: does it NAME a
    repair (a ``FIX:`` sentence), and does it say the repair is held by
    something this run does not control (:data:`_INELIGIBLE_PATTERNS`)?

    REMEDY DELIBERATELY DOES NOT JUDGE WHETHER THE NAMED FIX IS A GOOD ONE. That
    is the reviewer's call and R-0784's ruling stands: this filter reads what
    the paragraph SAYS about its own repair, never whether the repair is right.
    What changed is that a paragraph naming NO repair at all is no longer
    treated as one that does.
    """
    if not _FIX_SENTENCE_RE.search(paragraph):
        return False
    return not any(pattern.search(paragraph) for pattern in _INELIGIBLE_PATTERNS)


class SelfUseGenerationError(RuntimeError):
    """A source this generator needs could not be read, or a render was unsafe.

    Never raised for "no eligible source" — that is a legitimate ``None``,
    the same "empty is not broken" distinction
    :class:`packages.orchestration.self_use_queue.SelfUseQueueError`'s own
    docstring already draws for the queue itself.
    """


def default_ledger_path() -> Path:
    """Where the finding ledger lives, resolved the same way the queue is."""
    root = Path(__file__).resolve().parents[2]
    return root / ".agent" / "live_review.md"


def default_order_path() -> Path:
    """Where the toolchain refresh order lives, resolved the same way the queue is."""
    return Path(__file__).resolve().parents[2] / ORDER_RELATIVE_PATH


def _last_order_day(queue_path: Path | None) -> date | None:
    """The most recent day an item from the order was queued, consumed or not."""
    days = [
        date.fromisoformat(match.group("day"))
        for match in (_ORDER_PROVENANCE_RE.match(entry.provenance)
                      for entry in load_self_use_queue(queue_path))
        if match is not None and match.group("path") == ORDER_RELATIVE_PATH
    ]
    return max(days) if days else None


def _order_tier(queue_path: Path | None, order_path: Path, today: date) -> SelfUseQueueEntry | None:
    """Tier 0: the toolchain refresh order, verbatim, when fourteen days have passed."""
    if not order_path.is_file():
        return None
    last = _last_order_day(queue_path)
    if last is not None and today - last < timedelta(days=ORDER_CADENCE_DAYS):
        return None
    try:
        text = order_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SelfUseGenerationError(f"{order_path}: unreadable ({exc})") from exc
    title = next((line[len("# Job:"):].strip() for line in text.splitlines()
                  if line.startswith("# Job:")), "")
    if not title or not re.search(r"^## Task 1\b", text, re.M):
        raise SelfUseGenerationError(
            f"{order_path}: not a job file — it needs a `# Job:` title and a `## Task 1` heading")
    intro = text.split("\n## ", 1)[0].split("\n", 1)[1].strip()
    return SelfUseQueueEntry(
        id=_next_queue_id(queue_path),
        title=title,
        why=intro,
        job_markdown=text,
        consumed_by="",
        provenance=_ORDER_PROVENANCE.format(path=ORDER_RELATIVE_PATH, day=today.isoformat()),
    )


def _targeted_findings(queue_path: Path | None) -> frozenset[str]:
    """Every finding id an existing queue entry, consumed or not, already targets."""
    return frozenset(
        match.group(1)
        for match in (
            _LEDGER_PROVENANCE_RE.match(entry.provenance)
            for entry in load_self_use_queue(queue_path)
        )
        if match is not None
    )


def _oldest_open_low_or_medium_finding(
    ledger_path: Path, exclude: frozenset[str] = frozenset()
) -> tuple[str, str] | None:
    """The oldest (lowest id) OPEN Low/Medium finding not in ``exclude``, with its paragraph.

    ``None`` means Tier 1 has nothing to offer today, not that the ledger is
    unreadable — that raises instead.
    """
    try:
        text = ledger_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SelfUseGenerationError(f"{ledger_path}: unreadable ({exc})") from exc

    done_ids = set(_DONE_RE.findall(text))
    candidates: list[tuple[int, str]] = []
    for match in _SEVERITY_RE.finditer(text):
        r_id, severity = match.group(1), match.group(2)
        if severity not in _ELIGIBLE_SEVERITIES:
            continue
        if r_id in done_ids or r_id in exclude:
            continue
        candidates.append((int(r_id.split("-")[1]), r_id))

    if not candidates:
        return None

    candidates.sort()

    # THE OLDEST REPAIRABLE ONE, not simply the oldest. Eligibility is read from
    # the paragraph, so the paragraph is extracted BEFORE the choice is made and
    # the loop walks on when it is not repairable (amend0920-selfuse-real D2).
    for _, candidate_id in candidates:
        paragraph = _finding_paragraph(text, candidate_id, ledger_path)
        if _is_repairable(paragraph):
            return candidate_id, paragraph
    return None


def _finding_paragraph(text: str, r_id: str, ledger_path: Path) -> str:
    """The registration paragraph of ``r_id``, verbatim, from ``text``."""
    paragraph_re = re.compile(
        rf"^- {re.escape(r_id)} — (?:Low|Medium), .*?(?=\n\n|\Z)",
        re.M | re.S,
    )
    paragraph_match = paragraph_re.search(text)
    if paragraph_match is None:
        raise SelfUseGenerationError(
            f"{ledger_path}: matched {r_id} by severity scan but could "
            "not re-extract its paragraph"
        )
    return paragraph_match.group(0)


def _next_queue_id(queue_path: Path | None) -> str:
    """The next ``SU-NNN`` after every id already in the queue, consumed or not."""
    entries = load_self_use_queue(queue_path)
    used = [
        int(match.group(1))
        for match in (_QUEUE_ID_RE.match(entry.id) for entry in entries)
        if match is not None
    ]
    next_n = (max(used) + 1) if used else 1
    return f"SU-{next_n:03d}"


def _ledger_tier(queue_path: Path | None, ledger_path: Path) -> SelfUseQueueEntry | None:
    """Tier 1: the oldest open Low/Medium finding no queue entry targets, as a job."""
    found = _oldest_open_low_or_medium_finding(ledger_path, _targeted_findings(queue_path))
    if found is None:
        return None
    r_id, paragraph = found

    # Defence in depth: a ledger paragraph is prose, not markdown authored for
    # this purpose, so it is NEVER trusted to be safe to embed as a job body
    # without checking. A bare `## ` or `Acceptance:` line inside it would
    # introduce a second task boundary or terminate the task's body early
    # when `parse_job_file` later reads this text — checked directly by
    # regex here, not by calling `parse_job_file` itself (see the module
    # docstring's Deliberate absences).
    if re.search(r"^## ", paragraph, re.M) or re.search(r"^Acceptance\s*:", paragraph, re.M | re.I):
        raise SelfUseGenerationError(
            f"{r_id}: its ledger paragraph contains a line shaped like a "
            "markdown heading or an Acceptance marker, which would corrupt "
            "the rendered job file's task boundary — this item is not "
            "generated"
        )

    new_id = _next_queue_id(queue_path)
    title = f"Address ledger finding {r_id}"
    job_markdown = (
        f"# Job: Address ledger finding {r_id}\n"
        "\n"
        "## Task 1\n"
        f"{paragraph}\n"
        "\n"
        "Acceptance:\n"
        f"- {r_id} is repaired with a red-to-green proof, or the reviewer "
        "records in `.agent/live_review.md` why it cannot be — either way "
        f"the ledger gains a `Done: {r_id}` line.\n"
    )
    return SelfUseQueueEntry(
        id=new_id,
        title=title,
        why=paragraph,
        job_markdown=job_markdown,
        consumed_by="",
        provenance=_LEDGER_PROVENANCE.format(r_id=r_id),
    )


def _doc_staleness_tier(_queue_path: Path | None) -> SelfUseQueueEntry | None:
    """Tier 2: not yet wired to a real check catalog (DECISION F258 D2)."""
    return None


def _doctor_warning_tier(_queue_path: Path | None) -> SelfUseQueueEntry | None:
    """Tier 3: `doctor core` is not yet an importable source (DECISION F258 D2)."""
    return None


def generate_self_use_item(
    queue_path: Path | None = None,
    ledger_path: Path | None = None,
    *,
    order_path: Path | None = None,
    today: date | None = None,
) -> SelfUseQueueEntry | None:
    """The next item to append, from the first tier that has one, or ``None``.

    Writes nothing — this is the search half only. See
    :func:`append_generated_item` for the write and
    :func:`generate_and_append_if_empty` for the seam that combines both
    behind the "only when the queue is empty" rule.
    """
    ledger = ledger_path or default_ledger_path()

    order_result = _order_tier(queue_path, order_path or default_order_path(), today or date.today())
    if order_result is not None:
        return order_result

    ledger_result = _ledger_tier(queue_path, ledger)
    if ledger_result is not None:
        return ledger_result

    doc_result = _doc_staleness_tier(queue_path)
    if doc_result is not None:
        return doc_result

    return _doctor_warning_tier(queue_path)


def append_generated_item(entry: SelfUseQueueEntry, queue_path: Path | None = None) -> None:
    """Append ``entry`` to the queue file. The ONE writer this feature adds.

    Never sets ``consumed_by`` to anything but empty — a generated item is
    PENDING, exactly like a human-curated one, until the closure round
    consumes it.
    """
    path = queue_path or default_self_use_queue_path()
    body = json.loads(path.read_text(encoding="utf-8"))
    body["items"].append({
        "id": entry.id,
        "title": entry.title,
        "why": entry.why,
        "job_markdown": entry.job_markdown,
        "consumed_by": entry.consumed_by,
        "provenance": entry.provenance,
    })
    # R-0785: `ensure_ascii=False`, so a non-ASCII character in content this
    # writer never touched keeps its own bytes rather than becoming an escape.
    path.write_text(json.dumps(body, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Re-validate through the real loader before returning, so a malformed
    # write is caught here rather than by the next unrelated reader.
    load_self_use_queue(path)


def generate_and_append_if_empty(
    queue_path: Path | None = None,
    ledger_path: Path | None = None,
    *,
    order_path: Path | None = None,
    today: date | None = None,
) -> SelfUseQueueEntry | None:
    """The seam a closure round calls: generate and append, but ONLY when empty.

    Returns the appended entry, or ``None`` when the queue already holds a
    pending item (nothing is written) or no tier had anything to offer
    (nothing is written either — an empty queue with no eligible source
    stays empty, honestly, rather than inventing an item to fill it).
    """
    if pending_self_use_items(queue_path):
        return None
    entry = generate_self_use_item(queue_path, ledger_path, order_path=order_path, today=today)
    if entry is None:
        return None
    append_generated_item(entry, queue_path)
    return entry

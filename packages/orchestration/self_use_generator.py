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

Three sources are tried in order, exactly the priority
``docs/roadmap/features/T5_F258.md`` T001 specifies. Only the first is real
today; DECISION F258 D2 records why the other two are honest ``None``
placeholders rather than half-built guesses:

  1. THE FINDING LEDGER. The oldest OPEN (no ``Done:`` line) Low or Medium
     finding in ``.agent/live_review.md``, rendered as a job whose one task
     quotes the finding paragraph VERBATIM and whose acceptance is "repair it,
     or record why not" — never a per-finding summary this module would have
     to invent.
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
  * Remedy deliberately does not call
    :func:`packages.orchestration.pingpong_job.parse_job_file` to verify the
    rendered text — that function persists a job record as a side effect
    (``_persist_job``), which a pure generation step must never trigger.
"""
from __future__ import annotations

import json
import re
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

#: Severities this generator's Tier 1 will pick from — never High or Critical,
#: which are judgement calls a generator does not make for itself.
_ELIGIBLE_SEVERITIES = ("Low", "Medium")


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


def _oldest_open_low_or_medium_finding(ledger_path: Path) -> tuple[str, str] | None:
    """The oldest (lowest id) OPEN Low/Medium finding, with its full paragraph.

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
        if r_id in done_ids:
            continue
        candidates.append((int(r_id.split("-")[1]), r_id))

    if not candidates:
        return None

    candidates.sort()
    _, oldest_id = candidates[0]

    paragraph_re = re.compile(
        rf"^- {re.escape(oldest_id)} — (?:Low|Medium), .*?(?=\n\n|\Z)",
        re.M | re.S,
    )
    paragraph_match = paragraph_re.search(text)
    if paragraph_match is None:
        raise SelfUseGenerationError(
            f"{ledger_path}: matched {oldest_id} by severity scan but could "
            "not re-extract its paragraph"
        )
    return oldest_id, paragraph_match.group(0)


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
    """Tier 1: the oldest open Low/Medium finding, rendered as a job."""
    found = _oldest_open_low_or_medium_finding(ledger_path)
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
        provenance=f"generated (self-use-generator tier 1, ledger scan, {r_id})",
    )


def _doc_staleness_tier(_queue_path: Path | None) -> SelfUseQueueEntry | None:
    """Tier 2: not yet wired to a real check catalog (DECISION F258 D2)."""
    return None


def _doctor_warning_tier(_queue_path: Path | None) -> SelfUseQueueEntry | None:
    """Tier 3: `doctor core` is not yet an importable source (DECISION F258 D2)."""
    return None


def generate_self_use_item(
    queue_path: Path | None = None, ledger_path: Path | None = None
) -> SelfUseQueueEntry | None:
    """The next item to append, from the first tier that has one, or ``None``.

    Writes nothing — this is the search half only. See
    :func:`append_generated_item` for the write and
    :func:`generate_and_append_if_empty` for the seam that combines both
    behind the "only when the queue is empty" rule.
    """
    ledger = ledger_path or default_ledger_path()

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
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    # Re-validate through the real loader before returning, so a malformed
    # write is caught here rather than by the next unrelated reader.
    load_self_use_queue(path)


def generate_and_append_if_empty(
    queue_path: Path | None = None, ledger_path: Path | None = None
) -> SelfUseQueueEntry | None:
    """The seam a closure round calls: generate and append, but ONLY when empty.

    Returns the appended entry, or ``None`` when the queue already holds a
    pending item (nothing is written) or no tier had anything to offer
    (nothing is written either — an empty queue with no eligible source
    stays empty, honestly, rather than inventing an item to fill it).
    """
    if pending_self_use_items(queue_path):
        return None
    entry = generate_self_use_item(queue_path, ledger_path)
    if entry is None:
        return None
    append_generated_item(entry, queue_path)
    return entry

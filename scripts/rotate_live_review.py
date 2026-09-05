#!/usr/bin/env python3
"""Rotate long-closed records out of ``.agent/live_review.md`` into the archive.

Operator amendment amend0905-throughput (2026-09-05), rule 2c. Every closure
sequence runs this script as its own commit: it moves, byte-verbatim, every
``Gate:`` record whose feature is ``[x]`` in ``docs/roadmap/STATUS.md`` and
every resolved finding pair (exactly one ``- R-xxxx — `` registration record
with exactly one ``Done: R-xxxx — `` record) into the append-only
``.agent/live_review_archive.md``. Nothing else is touched: the preamble,
``## Steps``, ``## Findings``, open findings, ``Landed:``/``Recurrence:``
lines, ``DECISION`` paragraphs and any id with two ``Done:`` records stay.

Record model — LINE oriented, not paragraph oriented, because some features
appended records with a single newline separator. A record starts at a line
matching one of the start patterns below at column 0 and runs to the line
before the next start; trailing blank lines are separators, not content.
Indented ``  FIX`` paragraphs and wrapped continuation lines belong to the
record above them. The colon-bearing ledger records (``Gate:``, ``- R-``,
``Done:``, ``Landed:``, ``Recurrence:``, ``DECISION``) start a record on ANY
line, glued or not; the preamble-shaped patterns (``#``, ``>``, ``R<n> ``,
``LANDED``, ``RECURRENCE of``, ``RECOVERED``) start a record only at a
paragraph boundary — the file start or after a blank line — because the
ledger holds wrapped continuation lines at column 0 that match them
(measured 2026-09-05: seven ``R<n> `` lines and one ``LANDED`` line inside
registration records) and splitting a record there would orphan its tail.

Verification happens BEFORE any write: the record model must round-trip the
ledger byte for byte; every moved record must reappear in the new archive
verbatim and hash (sha256) to the digest taken from the ledger; the new
archive must start with the old archive's bytes; the open-findings count
(``^- R-\\d{4} — `` lines minus ``^Done: R-\\d{4} — `` lines) must be identical
before and after; and the records absent from the new ledger must be exactly
the moved ones. Any failure exits non-zero and writes nothing.

Usage::

    python3 scripts/rotate_live_review.py [--ledger PATH] [--status PATH]
                                          [--archive PATH] [--dry-run]

Stdlib only. The archive is read on demand, by id — never at session start.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = REPO_ROOT / ".agent" / "live_review.md"
DEFAULT_STATUS = REPO_ROOT / "docs" / "roadmap" / "STATUS.md"
DEFAULT_ARCHIVE = REPO_ROOT / ".agent" / "live_review_archive.md"

ARCHIVE_HEADER = (
    "# Live Review Archive — rotated records\n"
    "\n"
    "> Records are moved here byte-verbatim from `.agent/live_review.md` by "
    "`scripts/rotate_live_review.py` (operator amendment amend0905-throughput); "
    "they are read on demand, by id, never at session start.\n"
)

# WHY two classes: the strong starts are the record kinds this script classifies
# and must recognise even when glued to the previous record with one newline; the
# weak starts bound the preamble and stray prose and must not split a record whose
# wrapped continuation line happens to begin with `R13 ` or `LANDED` at column 0.
_STRONG_START = re.compile(
    r"^(Gate: |- R-\d{4} — |Done: R-\d{4} — |Landed: R-\d{4}|Recurrence: R-\d{4}|DECISION F\d{3} D\d+)"
)
_WEAK_START = re.compile(r"^(#|>|R\d+ |LANDED|RECURRENCE of R-\d{4}|RECOVERED)")
_GATE_FORMS = (
    re.compile(r"^Gate: F(\d{3}) R\d+"),
    re.compile(r"^Gate: R\d+ — the F(\d{3}) R\d+ entry"),
)
_REGISTRATION = re.compile(r"^- (R-\d{4}) — ")
_DONE = re.compile(r"^Done: (R-\d{4}) — ")
_OPEN_REGISTRATION_LINE = re.compile(r"^- R-\d{4} — ", re.M)
_DONE_LINE = re.compile(r"^Done: R-\d{4} — ", re.M)
_CLOSED_FEATURE_LINE = re.compile(r"^- \[x\] F(\d{3}) — ", re.M)


class RotationError(RuntimeError):
    """A verification step failed; nothing was written."""


@dataclass(frozen=True)
class Record:
    """One ledger record: its kind, its key, its bytes and the blank lines before it."""

    kind: str  # "gate" | "reg" | "done" | "other"
    key: str | None  # feature id for a gate, finding id for reg/done, else None
    body: str  # the record's lines joined by "\n", no trailing newline
    blank_before: int  # blank separator lines between the previous record and this one


@dataclass(frozen=True)
class RotationResult:
    """Everything a rotation computed, before or instead of writing."""

    new_ledger: str
    new_archive: str
    moved: tuple[Record, ...]
    gates_moved: int
    pairs_moved: int
    unparsed_gates: int
    old_ledger_size: int
    new_ledger_size: int
    old_archive_size: int
    new_archive_size: int
    open_before: int
    open_after: int


def record_digest(body: str) -> str:
    """sha256 hex digest of a record's UTF-8 bytes, taken from the ledger before the move."""
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def count_open_findings(text: str) -> int:
    """The canonical line formula: registration lines minus ``Done:`` lines."""
    return len(_OPEN_REGISTRATION_LINE.findall(text)) - len(_DONE_LINE.findall(text))


def closed_feature_ids(status_text: str) -> frozenset[str]:
    """Feature ids ticked ``[x]`` in the STATUS ledger."""
    return frozenset(_CLOSED_FEATURE_LINE.findall(status_text))


def classify_record(body: str) -> tuple[str, str | None]:
    """Kind and key of a record from its first line.

    A ``Gate:`` header matching neither known form classifies as ``("gate", None)``
    and is never moved.
    """
    head = body.split("\n", 1)[0]
    if head.startswith("Gate: "):
        for form in _GATE_FORMS:
            match = form.match(head)
            if match:
                return "gate", match.group(1)
        return "gate", None
    match = _REGISTRATION.match(head)
    if match:
        return "reg", match.group(1)
    match = _DONE.match(head)
    if match:
        return "done", match.group(1)
    return "other", None


def _is_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    if _STRONG_START.match(line):
        return True
    if not _WEAK_START.match(line):
        return False
    return index == 0 or lines[index - 1] == ""


def split_records(text: str) -> tuple[list[Record], str]:
    """Split ledger text into records; also return the file's trailing newlines.

    Lines before the first start (normally none) form one leading ``other``
    record. ``rebuild_ledger(records, set(), trailing)`` reproduces ``text``.
    """
    content = text.rstrip("\n")
    trailing = text[len(content):]
    lines = content.split("\n") if content else []
    starts = [i for i in range(len(lines)) if _is_start(lines, i)]
    if lines and (not starts or starts[0] != 0):
        first_content = next((i for i, line in enumerate(lines) if line != ""), None)
        if first_content is not None and (not starts or first_content < starts[0]):
            starts.insert(0, first_content)
    records: list[Record] = []
    previous_end = 0  # index one past the previous record's last content line
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        body_lines = lines[start:end]
        while body_lines and body_lines[-1] == "":
            body_lines.pop()
        body = "\n".join(body_lines)
        kind, key = classify_record(body)
        records.append(Record(kind, key, body, start - previous_end))
        previous_end = start + len(body_lines)
    return records, trailing


def rebuild_ledger(records: list[Record], drop: set[int], trailing: str) -> str:
    """Join the kept records, each behind the blank lines it owned; drop the rest."""
    parts: list[str] = []
    first = True
    for index, record in enumerate(records):
        if index in drop:
            continue
        parts.append("\n" * record.blank_before if first else "\n" * (record.blank_before + 1))
        parts.append(record.body)
        first = False
    return "".join(parts) + trailing


def select_movable(records: list[Record], closed: frozenset[str]) -> list[int]:
    """Indices of the records that move, in ledger order.

    Gates of ``[x]`` features move. A finding pair moves only when its id has
    EXACTLY one registration record and EXACTLY one ``Done:`` record.
    """
    registrations: dict[str, int] = {}
    dones: dict[str, int] = {}
    for record in records:
        if record.kind == "reg" and record.key:
            registrations[record.key] = registrations.get(record.key, 0) + 1
        elif record.kind == "done" and record.key:
            dones[record.key] = dones.get(record.key, 0) + 1
    resolved = {rid for rid, n in registrations.items() if n == 1 and dones.get(rid) == 1}
    movable: list[int] = []
    for index, record in enumerate(records):
        if record.kind == "gate" and record.key is not None and record.key in closed:
            movable.append(index)
        elif record.kind in ("reg", "done") and record.key in resolved:
            movable.append(index)
    return movable


def append_to_archive(old_archive: str, bodies: list[str]) -> str:
    """The new archive text: the old bytes untouched, then each body behind one blank line."""
    out = old_archive if old_archive else ARCHIVE_HEADER
    for body in bodies:
        if out.endswith("\n\n"):
            separator = ""
        elif out.endswith("\n"):
            separator = "\n"
        else:
            separator = "\n\n"
        out += separator + body + "\n"
    return out


def _verify(
    ledger_text: str,
    new_ledger: str,
    old_archive: str,
    new_archive: str,
    records: list[Record],
    movable: list[int],
    digests: list[str],
) -> None:
    moved = [records[i] for i in movable]
    if not new_archive.startswith(old_archive):
        raise RotationError("archive is not append-only: the old archive bytes are not a prefix of the new ones")
    appended = new_archive[len(old_archive):]
    for record in moved:
        if record.body not in appended:
            raise RotationError(f"moved record not found verbatim in the archive: {record.body[:60]!r}")
    archive_records, _ = split_records(new_archive)
    tail = archive_records[len(archive_records) - len(moved):] if moved else []
    if [r.body for r in tail] != [r.body for r in moved]:
        raise RotationError("the archive's appended records do not parse back to the moved records in order")
    for record, digest in zip(tail, digests):
        if hashlib.sha256(record.body.encode("utf-8")).hexdigest() != digest:
            raise RotationError(f"sha256 mismatch for the archived record {record.body[:60]!r}")
    before = count_open_findings(ledger_text)
    after = count_open_findings(new_ledger)
    if before != after:
        raise RotationError(f"open-findings count changed: {before} before, {after} after")
    kept_bodies = [r.body for i, r in enumerate(records) if i not in set(movable)]
    new_records, _ = split_records(new_ledger)
    if [r.body for r in new_records] != kept_bodies:
        raise RotationError("the records absent from the new ledger are not exactly the moved ones")


def rotate(ledger_text: str, status_text: str, archive_text: str | None) -> RotationResult:
    """Compute the rotation and verify it; raise :class:`RotationError` instead of returning a bad one."""
    records, trailing = split_records(ledger_text)
    if rebuild_ledger(records, set(), trailing) != ledger_text:
        raise RotationError("the record model does not round-trip the ledger byte for byte")
    movable = select_movable(records, closed_feature_ids(status_text))
    moved = [records[i] for i in movable]
    digests = [record_digest(r.body) for r in moved]
    new_ledger = rebuild_ledger(records, set(movable), trailing)
    old_archive = archive_text if archive_text is not None else ""
    new_archive = append_to_archive(old_archive, [r.body for r in moved]) if moved else old_archive
    if moved:
        _verify(ledger_text, new_ledger, old_archive, new_archive, records, movable, digests)
    elif new_ledger != ledger_text:
        raise RotationError("nothing to move, yet the rebuilt ledger differs from the original")
    return RotationResult(
        new_ledger=new_ledger,
        new_archive=new_archive,
        moved=tuple(moved),
        gates_moved=sum(1 for r in moved if r.kind == "gate"),
        pairs_moved=sum(1 for r in moved if r.kind == "reg"),
        unparsed_gates=sum(1 for r in records if r.kind == "gate" and r.key is None),
        old_ledger_size=len(ledger_text.encode("utf-8")),
        new_ledger_size=len(new_ledger.encode("utf-8")),
        old_archive_size=len(old_archive.encode("utf-8")),
        new_archive_size=len(new_archive.encode("utf-8")),
        open_before=count_open_findings(ledger_text),
        open_after=count_open_findings(new_ledger),
    )


def _report(result: RotationResult) -> list[str]:
    lines = [
        f"gate records moved: {result.gates_moved}",
        f"finding pairs moved: {result.pairs_moved} ({2 * result.pairs_moved} records)",
        f"old ledger size: {result.old_ledger_size} bytes",
        f"new ledger size: {result.new_ledger_size} bytes",
        f"old archive size: {result.old_archive_size} bytes",
        f"new archive size: {result.new_archive_size} bytes",
        f"open findings before: {result.open_before}",
        f"open findings after: {result.open_after}",
    ]
    if result.unparsed_gates:
        lines.append(f"gate headers matching neither known form (left in place): {result.unparsed_gates}")
    return lines


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rotate_live_review.py",
        description=(
            "Move [x] features' Gate: records and resolved finding pairs from the live-review "
            "ledger into the append-only archive, byte-verbatim and self-verified."
        ),
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER, help="the ledger (default: .agent/live_review.md)")
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS, help="the STATUS ledger (default: docs/roadmap/STATUS.md)")
    parser.add_argument(
        "--archive", type=Path, default=DEFAULT_ARCHIVE, help="the archive (default: .agent/live_review_archive.md)"
    )
    parser.add_argument("--dry-run", action="store_true", help="print the same report and write nothing")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    ledger_text = args.ledger.read_bytes().decode("utf-8")
    status_text = args.status.read_bytes().decode("utf-8")
    archive_text = args.archive.read_bytes().decode("utf-8") if args.archive.exists() else None
    try:
        result = rotate(ledger_text, status_text, archive_text)
    except RotationError as exc:
        print(f"REFUSED, nothing written: {exc}", file=sys.stderr)
        return 2
    for line in _report(result):
        print(line)
    if not result.moved:
        print("nothing to move; no byte changed")
        return 0
    if args.dry_run:
        print("dry run; nothing written")
        return 0
    args.archive.write_bytes(result.new_archive.encode("utf-8"))
    args.ledger.write_bytes(result.new_ledger.encode("utf-8"))
    print(f"written: {args.ledger} and {args.archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

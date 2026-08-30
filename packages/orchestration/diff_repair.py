"""Repair hunk selection for diff-only repair (F111 T001).

Picks the exact source lines a repair round should carry, so a repair
prompt sends only the failure-relevant hunks with a context margin
instead of whole files.

This module is pure: it reads files under a repo root and returns data.
It holds no unified-diff parser and no applier, on purpose. `review_scope`
already turns a unified diff into per-file line ranges (this module
consumes exactly that shape, `{path: [[start, end], ...]}`) and
`source_apply` is already the strict hunk applier that lands changes.
Remedy deliberately does not add a third place that understands
unified-diff syntax.

Public API::

    select_repair_hunks(repo_root, changed_line_ranges, *,
                        margin_lines=3, max_total_chars=20000)
        -> RepairHunkSelection
    changed_line_ranges_from_patch(patch) -> {path: [[start, end], ...]}

Omission reasons reported in ``RepairHunkSelection.omitted`` are
``missing``, ``binary``, ``no_ranges``, ``out_of_bounds`` and ``budget``.
``no_ranges`` means nothing was asked for; ``out_of_bounds`` means lines
WERE asked for but none of them exist in the file, which is how a stale
diff — one whose line numbers no longer match the file on disk — becomes
visible instead of being swallowed (finding R-0299).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.review_scope import parse_diff_line_ranges
from packages.orchestration.structured_patch import StructuredPatch


# One contiguous block of source a repair prompt carries verbatim.
@dataclass(frozen=True)
class RepairHunk:
    """A single repair hunk: one file, one line span, the exact lines."""

    path: str  # repo-relative, exactly as the caller gave it
    start_line: int  # 1-based inclusive, AFTER margin expansion
    end_line: int  # 1-based inclusive, AFTER margin expansion
    text: str  # the exact source lines, newline-joined


# The whole answer of one selection pass: what is carried, what is not, how big.
@dataclass(frozen=True)
class RepairHunkSelection:
    """Selected hunks plus the per-path reasons anything was left out."""

    hunks: tuple[RepairHunk, ...]
    omitted: tuple[tuple[str, str], ...]  # (path, reason)
    total_chars: int


# Reading is split out so every failure mode becomes a reason, never an exception.
def _read_source_lines(repo_root: Path, path: str) -> tuple[list[str] | None, str]:
    """Return one file's lines, or (None, reason) when it cannot be carried."""
    try:
        raw = (repo_root / path).read_bytes()
    except (OSError, ValueError):
        return None, "missing"
    if b"\x00" in raw:
        return None, "binary"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "binary"
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()  # a trailing newline ends the last line, it is not a new one
    return lines, ""


# Margin expansion and merging live together: merging is only correct after clamping.
def _expand_and_merge_ranges(
    ranges: Sequence[Sequence[int]],
    line_count: int,
    margin_lines: int,
) -> list[tuple[int, int]]:
    """Clamp each range to the file, then fuse overlapping or adjacent spans."""
    spans: list[tuple[int, int]] = []
    for raw_range in ranges:
        if not raw_range:
            continue
        start = max(1, int(raw_range[0]) - margin_lines)
        end = min(line_count, int(raw_range[-1]) + margin_lines)
        if start > end:
            continue  # the range selects no line that exists in this file
        spans.append((start, end))
    spans.sort()
    merged: list[tuple[int, int]] = []
    for start, end in spans:
        if merged and start <= merged[-1][1] + 1:  # +1 fuses adjacent spans too
            previous_start, previous_end = merged[-1]
            merged[-1] = (previous_start, max(previous_end, end))
        else:
            merged.append((start, end))
    return merged


# Empty entries ask for no line, so only a non-empty one can land out of bounds.
def _has_non_empty_range(ranges: Sequence[Sequence[int]]) -> bool:
    """True when at least one entry names lines, so an empty result is clamping."""
    return any(bool(raw_range) for raw_range in ranges)


# The entry point F111's prompt side calls instead of attaching whole files.
def select_repair_hunks(
    repo_root: Path,
    changed_line_ranges: Mapping[str, Sequence[Sequence[int]]],
    *,
    margin_lines: int = 3,
    max_total_chars: int = 20000,
) -> RepairHunkSelection:
    """Select the margin-expanded source hunks for the given changed lines.

    Paths are visited in sorted order and hunks come back sorted by
    ``(path, start_line)``, so the same input always yields the same
    prompt. Admission stops at the first hunk that would push
    ``total_chars`` past ``max_total_chars``; every path with a hunk left
    behind is reported once with reason ``budget``.
    """
    candidates: list[RepairHunk] = []
    omitted: list[tuple[str, str]] = []

    for path in sorted(changed_line_ranges):
        ranges = changed_line_ranges[path]
        if not ranges:
            omitted.append((path, "no_ranges"))
            continue
        lines, reason = _read_source_lines(repo_root, path)
        if lines is None:
            omitted.append((path, reason))
            continue
        spans = _expand_and_merge_ranges(ranges, len(lines), margin_lines)
        if not spans:
            # Lines were named yet none survived clamping: they lie outside the file.
            reason = "out_of_bounds" if _has_non_empty_range(ranges) else "no_ranges"
            omitted.append((path, reason))
            continue
        for start, end in spans:
            candidates.append(
                RepairHunk(
                    path=path,
                    start_line=start,
                    end_line=end,
                    text="\n".join(lines[start - 1 : end]),
                )
            )

    candidates.sort(key=lambda hunk: (hunk.path, hunk.start_line))
    admitted: list[RepairHunk] = []
    total_chars = 0
    over_budget_paths: list[str] = []
    for index, hunk in enumerate(candidates):
        if total_chars + len(hunk.text) > max_total_chars:
            for dropped in candidates[index:]:
                if dropped.path not in over_budget_paths:
                    over_budget_paths.append(dropped.path)
            break
        admitted.append(hunk)
        total_chars += len(hunk.text)
    omitted.extend((path, "budget") for path in over_budget_paths)

    return RepairHunkSelection(
        hunks=tuple(admitted),
        omitted=tuple(omitted),
        total_chars=total_chars,
    )


# The bridge holds the patch it applied; this turns it into what selection consumes.
def changed_line_ranges_from_patch(patch: StructuredPatch) -> dict[str, list[list[int]]]:
    """Map an applied builder patch to the ranges ``select_repair_hunks`` takes.

    Only ``unified_diffs`` carry line numbers, and they are read through
    ``review_scope.parse_diff_line_ranges`` so hunk headers keep exactly one
    reading in this repository. A declared path whose diff text yields no
    hunk header still appears, with an EMPTY range list, and so does every
    ``file_ops`` path: an empty list comes back from ``select_repair_hunks``
    as ``no_ranges``, which a reader can see, whereas dropping the path
    would leave nothing to see. Remedy deliberately does not reconstruct
    ranges by re-diffing ``file_ops`` content against disk in v1 — that
    would be a second differ, and the full-file repair path already covers
    the case.
    """
    ranges: dict[str, list[list[int]]] = {}
    for entry in patch.unified_diffs:
        parsed = parse_diff_line_ranges(entry.diff)
        for path, spans in parsed.items():
            ranges.setdefault(path, []).extend(spans)
        if entry.path and entry.path not in parsed:
            ranges.setdefault(entry.path, [])
    for file_op in patch.file_ops:
        ranges.setdefault(file_op.path, [])
    return ranges


# The rendering convention T002b-ii step 2 needs: turning a selection into
# prompt text. No caller wires this in yet — that lands in a later round,
# gated on F106's hoisted resume-ref (DECISION F106 D1(b)) — this function
# exists on its own so the convention is frozen and tested in isolation
# before anything depends on it.
REPAIR_HUNKS_HEADING = "## Resumed Session — Changed Regions Only"
REPAIR_HUNKS_OMITTED_INTRO = "Omitted from this selection:"


def render_repair_hunks(selection: RepairHunkSelection) -> str:
    """Render a hunk selection as repair-prompt text.

    Returns the EMPTY STRING when ``selection.hunks`` is empty — a heading
    with no hunk beneath it would tell a repair round it has scoped source
    when it has none. Hunks render in ``selection.hunks``' own order
    (already ``(path, start_line)``-sorted by ``select_repair_hunks``);
    nothing here sorts or deduplicates. Omissions render as a trailing
    bulleted list, stated only when ``selection.omitted`` is non-empty, so a
    caller can see what the budget left out without reading a second
    artifact.
    """
    if not selection.hunks:
        return ""
    parts = [REPAIR_HUNKS_HEADING, ""]
    for hunk in selection.hunks:
        parts.append(f"### {hunk.path} (lines {hunk.start_line}-{hunk.end_line})")
        parts.append(f"```\n{hunk.text}\n```")
        parts.append("")
    if selection.omitted:
        parts.append(REPAIR_HUNKS_OMITTED_INTRO)
        for path, reason in selection.omitted:
            parts.append(f"- {path} ({reason})")
        parts.append("")
    return "\n".join(parts)

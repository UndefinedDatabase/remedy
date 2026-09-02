"""Tiered artifact summary schema and mechanical sectioners (F108 T001).

An oversized job artifact (a diff, a log, a report) gets a tiered
representation instead of being included in full: a short L1 summary, a
list of L2 section summaries, and the full reference path so a follow-up
prompt can consume L1 plus only the relevant L2 sections. This module owns
the schema (``ArtifactSummary``/``ArtifactSummarySection``) and the pure,
mechanical half of the feature — file-boundary diff sectioning, blank-line
log sectioning, and sibling-file storage/caching keyed by the artifact's own
content hash.

The rules this module enforces:
  * sectioning is MECHANICAL, never a provider call — ``section_diff`` and
    ``section_log`` never raise and never return an empty list for a
    non-empty input;
  * a cached summary is valid ONLY while the artifact's bytes are unchanged;
    any mismatch (missing file, missing cache, unparseable cache, or a
    hash that no longer matches) is treated identically — a cache miss;
  * generation (the provider call that fills ``l1``/``l2[].summary``/
    ``generator``/``generated_at``) is T002's concern, not this module's —
    this module only defines the shape and the mechanical split.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pydantic import BaseModel, ValidationError

#: Boundary every git unified diff in this repository uses between files.
_GIT_HEADER_RE = re.compile(r"^diff --git a/(\S+) b/(\S+)$")

#: A run of two or more consecutive newlines is a blank-line section gap.
_BLANK_GAP_RE = re.compile(r"\n{2,}")


class ArtifactSummarySection(BaseModel):
    """One L2 section: a mechanically- or provider-derived summary of a span."""

    section: str
    span_ref: str
    summary: str


class ArtifactSummary(BaseModel):
    """The ``artifact.summary.json`` schema the feature file's Design section names.

    T002 (not this module) is what populates ``generator``/``generated_at``
    and the real ``summary`` text of ``l1``/``l2[].summary`` via a provider
    call; this schema only fixes the shape.
    """

    l1: str
    l2: list[ArtifactSummarySection]
    full_ref: str
    generator: str
    generated_at: str
    artifact_hash: str


def compute_artifact_hash(artifact_bytes: bytes) -> str:
    """Return the sha256 hex digest of ``artifact_bytes``."""
    return hashlib.sha256(artifact_bytes).hexdigest()


def summary_path_for(artifact_path: Path) -> Path:
    """Return the sibling cache path for ``artifact_path`` (pure path arithmetic)."""
    return artifact_path.with_name(artifact_path.name + ".summary.json")


def load_cached_summary(artifact_path: Path) -> ArtifactSummary | None:
    """Return the cached ``ArtifactSummary`` for ``artifact_path``, or ``None``.

    A miss (never a raise) covers: no cache file, no artifact file, a cache
    file that is not valid JSON or does not match the schema, or a hash that
    no longer matches the artifact's current bytes.
    """
    cache_path = summary_path_for(artifact_path)
    if not cache_path.exists() or not artifact_path.exists():
        return None

    try:
        raw = json.loads(cache_path.read_text())
        summary = ArtifactSummary.model_validate(raw)
    except (json.JSONDecodeError, ValidationError, UnicodeDecodeError, OSError):
        return None

    current_hash = compute_artifact_hash(artifact_path.read_bytes())
    # WHY: a hash mismatch means the artifact changed since the summary was
    # generated, and must be treated exactly like a missing cache.
    if summary.artifact_hash != current_hash:
        return None
    return summary


def save_summary(artifact_path: Path, summary: ArtifactSummary) -> None:
    """Write ``summary`` as JSON to the sibling cache path, overwriting any prior file."""
    summary_path_for(artifact_path).write_text(summary.model_dump_json())


def _strip_side_prefix(raw_path: str) -> str:
    """Drop one leading ``a/`` or ``b/`` from a diff header path."""
    if raw_path.startswith("a/") or raw_path.startswith("b/"):
        return raw_path[2:]
    return raw_path


def section_diff(diff_text: str) -> list[dict[str, str]]:
    """Mechanically split a unified diff into one entry per file, in file order.

    Splits on ``diff --git a/<path> b/<path>`` boundaries. A diff with no such
    boundary (a bare unified diff, or an empty string) returns a single
    ``"(unsectioned)"`` entry rather than an empty list.
    """
    lines = diff_text.split("\n")
    boundaries: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        match = _GIT_HEADER_RE.match(line)
        if not match:
            continue
        a_side, b_side = match.group(1), match.group(2)
        path = a_side if b_side == "/dev/null" else b_side
        boundaries.append((i, _strip_side_prefix(path)))

    if not boundaries:
        return [
            {
                "section": "(unsectioned)",
                "span_ref": "file:(unsectioned)",
                "text": diff_text,
            }
        ]

    entries: list[dict[str, str]] = []
    for idx, (start, path) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(lines)
        text = "\n".join(lines[start:end])
        entries.append({"section": path, "span_ref": f"file:{path}", "text": text})
    return entries


def section_log(log_text: str, chunk_lines: int = 200) -> list[dict[str, str]]:
    """Mechanically split free-text log content into blocks.

    Primary rule: split on blank-line gaps (two or more consecutive
    newlines) into "marker blocks". Fallback: if that produces exactly one
    block and it exceeds ``chunk_lines`` lines, re-split it into fixed-size
    line chunks instead.
    """
    if log_text == "":
        return []

    raw_blocks = _BLANK_GAP_RE.split(log_text)
    blocks = [block for block in raw_blocks if block != ""]

    if len(blocks) == 1:
        lines = blocks[0].split("\n")
        if len(lines) > chunk_lines:
            return _chunk_lines(lines, chunk_lines)

    entries: list[dict[str, str]] = []
    line_cursor = 1
    for i, block in enumerate(blocks):
        block_line_count = block.count("\n") + 1
        start = line_cursor
        end = start + block_line_count - 1
        entries.append(
            {
                "section": f"block-{i}",
                "span_ref": f"lines:{start}-{end}",
                "text": block,
            }
        )
        # +1 for the blank line consumed by the split itself between blocks.
        line_cursor = end + 2
    return entries


def _chunk_lines(lines: list[str], chunk_lines: int) -> list[dict[str, str]]:
    """Fixed-size fallback split of ``lines`` into ``chunk_lines``-sized blocks."""
    entries: list[dict[str, str]] = []
    for i, start_idx in enumerate(range(0, len(lines), chunk_lines)):
        chunk = lines[start_idx : start_idx + chunk_lines]
        start = start_idx + 1
        end = start_idx + len(chunk)
        entries.append(
            {
                "section": f"block-{i}",
                "span_ref": f"lines:{start}-{end}",
                "text": "\n".join(chunk),
            }
        )
    return entries

"""Tiered artifact summary schema, sectioners, generation, the T003a call bridge, and T003b diff-tiering rendering (F108 T001/T002/T003a/T003b).

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
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ValidationError

from packages.orchestration.failure_postmortem import FailureSignals, classify, utc_now_iso
from packages.orchestration.intake import make_structured_call_fn
from packages.orchestration.role_config import resolve_role_config
from packages.orchestration.structured_outputs import run_structured_call

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


# ---------------------------------------------------------------------------
# Generation (F108 T002) — the provider call that fills l1/l2[].summary
# ---------------------------------------------------------------------------


#: Compact schema version, per the SCHEMA_V convention run_structured_call
#: requires (packages/orchestration/schemas/models.py:schema_v_of).
GENERATED_SUMMARY_SCHEMA_V = "generated_summary_v1"


class GeneratedSummaryContent(BaseModel):
    """The NARROW schema the ``summary`` role is actually asked to fill.

    Deliberately excludes ``full_ref``/``artifact_hash``/``generator``/
    ``generated_at`` — this module derives those itself and never trusts a
    provider response for them, so a provider hallucinating a path or a hash
    can never corrupt the cache key or the reference path.
    """

    SCHEMA_V: ClassVar[str] = GENERATED_SUMMARY_SCHEMA_V

    l1: str
    l2: list[ArtifactSummarySection]


#: Shown to the caller instead of silently returning an empty/stale summary.
FALLBACK_MARKER = "[summary unavailable — truncated view]"
#: How many leading characters of the combined section text the fallback keeps.
_FALLBACK_HEAD_CHARS = 2000
#: How many trailing characters of the combined section text the fallback keeps.
_FALLBACK_TAIL_CHARS = 2000


def _build_summary_prompt(sections: list[dict[str, str]]) -> str:
    """Mechanically build a summary-generation prompt from T001's section list.

    Never raises, including for ``sections == []``.
    """
    blocks = [
        f"## {entry.get('section', '')} ({entry.get('span_ref', '')})\n{entry.get('text', '')}"
        for entry in sections
    ]
    rendered = "\n\n".join(blocks) if blocks else "(no sections)"
    instruction = (
        "Write an L1 summary of about 200 tokens covering all sections above, "
        "and one L2 entry per section given above. Each L2 entry's `section` "
        "and `span_ref` MUST echo the corresponding input section's own "
        "`section`/`span_ref` values exactly — do not invent, rename, split, "
        "or merge section names."
    )
    return f"{rendered}\n\n{instruction}"


def _fallback_summary(
    sections: list[dict[str, str]],
    full_ref: str,
    artifact_hash: str,
    reason: str,
) -> ArtifactSummary:
    """The "never silent, never blocking" fallback. NEVER raises, for any input."""
    combined = "\n\n".join(entry.get("text", "") for entry in sections)

    if len(combined) <= _FALLBACK_HEAD_CHARS + _FALLBACK_TAIL_CHARS:
        # Nothing to truncate — do not fabricate a head/tail split.
        fallback_text = combined
    else:
        head = combined[:_FALLBACK_HEAD_CHARS]
        tail = combined[-_FALLBACK_TAIL_CHARS:]
        fallback_text = f"{head}\n...\n{tail}"

    return ArtifactSummary(
        l1=FALLBACK_MARKER,
        l2=[ArtifactSummarySection(section="fallback", span_ref="fallback", summary=fallback_text)],
        full_ref=full_ref,
        generator=f"fallback:{reason}",
        generated_at=utc_now_iso(),
        artifact_hash=artifact_hash,
    )


def generate_artifact_summary(
    sections: list[dict[str, str]],
    full_ref: str,
    artifact_hash: str,
    call_fn: Callable[[str, int], str] | None = None,
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    generator_label: str = "summary-role",
) -> ArtifactSummary:
    """Generate an :class:`ArtifactSummary` via the ``summary`` role, or fall back.

    NEVER raises: the fallback IS the error path, not an exception. Mirrors the
    three-way shape of :func:`packages.orchestration.dod_compiler.compile_dod`
    (``call_fn is None`` / try-except-Exception around the structured call /
    ``not outcome.ok``).

    ``full_ref``/``artifact_hash``/``generator``/``generated_at`` ALWAYS come
    from this function's own parameters/clock, never from the provider's
    response — see :class:`GeneratedSummaryContent`.
    """
    if call_fn is None:
        return _fallback_summary(sections, full_ref, artifact_hash, reason="no provider")

    prompt = _build_summary_prompt(sections)

    try:
        outcome = run_structured_call(
            GeneratedSummaryContent,
            prompt,
            call_fn,
            on_call=on_call,
            allow_parse_retry=True,
        )
    except Exception as exc:
        classification = classify(FailureSignals(exception=exc))
        return _fallback_summary(
            sections, full_ref, artifact_hash, reason=classification.failure_class.value)

    if not outcome.ok:
        classification = classify(
            FailureSignals(error_class=outcome.error_class, error_text=outcome.hint))
        return _fallback_summary(
            sections, full_ref, artifact_hash, reason=classification.failure_class.value)

    assert isinstance(outcome.value, GeneratedSummaryContent)
    return ArtifactSummary(
        l1=outcome.value.l1,
        l2=outcome.value.l2,
        full_ref=full_ref,
        generator=generator_label,
        generated_at=utc_now_iso(),
        artifact_hash=artifact_hash,
    )


# ---------------------------------------------------------------------------
# F108 T003a — bridging role_config to a call_fn, and the relevant-section rule
# ---------------------------------------------------------------------------


def summary_call_fn() -> Callable[[str, int], str] | None:
    """Build a call_fn for the `summary` role, or None.

    Bridges DECISION F108 D1's KNOWN_ROLES registration to an actual
    callable: resolve_role_config("summary") supplies the model,
    make_structured_call_fn (the only existing call_fn factory of this
    shape in the repo) does the rest. Honest None under the same
    conditions make_structured_call_fn already returns None for (no
    ollama package importable, no reachable server) — never raises.
    """
    role_cfg = resolve_role_config("summary")
    return make_structured_call_fn(GeneratedSummaryContent, model=role_cfg.model)


def select_relevant_sections(
    summary: ArtifactSummary, file_refs: Iterable[str]
) -> list[ArtifactSummarySection]:
    """Return summary.l2 entries whose `section` exactly matches a file_ref.

    F108 T003's relevant-L2-section matching rule (DECISION F108 D2): diff
    sections and ReviewFinding.file share the same repo-relative-path
    convention, so exact string equality is the match. No match returns
    [] -- "L1 plus ONLY the relevant L2 sections" reads as zero relevant
    sections meaning zero L2, never a silent fallback to the whole list.
    Never raises, for any input including an empty summary.l2 or an empty
    file_refs.
    """
    refs = set(file_refs)
    return [section for section in summary.l2 if section.section in refs]


# ---------------------------------------------------------------------------
# F108 T003b — rendering the tiered diff-inclusion text
# ---------------------------------------------------------------------------


def render_tiered_diff_text(
    diff_text: str,
    file_refs: Iterable[str],
    call_fn: Callable[[str, int], str] | None,
    *,
    threshold_chars: int,
    full_ref: str,
) -> str:
    """Render a tiered L1+relevant-L2 replacement for an oversized diff, or "".

    F108 T003b: the pre-rendered text a caller (``pingpong_loop.py``'s
    ``_builder_tiered_diff_text``) substitutes for its own flat-capped diff
    segment. Returns "" when ``diff_text`` is at or under ``threshold_chars``
    -- the caller's signal to keep its own flat-cap behavior unchanged.
    Above threshold: sections the diff (``section_diff``), generates via
    ``generate_artifact_summary`` (never raises -- the fallback IS the error
    path), selects only the sections matching ``file_refs``
    (``select_relevant_sections``), and renders the L1 summary plus each
    selected L2 section plus a ``full_ref`` line so the model knows more
    exists.
    """
    if len(diff_text) <= threshold_chars:
        return ""
    sections = section_diff(diff_text)
    artifact_hash = compute_artifact_hash(diff_text.encode("utf-8"))
    summary = generate_artifact_summary(sections, full_ref, artifact_hash, call_fn)
    relevant = select_relevant_sections(summary, file_refs)
    lines = [f"## Current Staged Diff (summarized)\n{summary.l1}\n"]
    for entry in relevant:
        lines.append(f"### {entry.section} ({entry.span_ref})\n{entry.summary}\n")
    lines.append(f"Full diff: {full_ref} ({len(diff_text)} characters)\n")
    return "\n".join(lines)

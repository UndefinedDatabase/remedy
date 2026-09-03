"""
Prompt segment registry — cache-optimal prompt ordering (F105 T001).

Prompts stop being ad hoc string concatenation: every part of a prompt is a
NAMED SEGMENT carrying a declared stability rank, and composition orders those
segments by rank so the stable prefix of a role's prompt is byte-identical
across calls and a provider cache can hit it. Composition also returns a
segment MANIFEST (name, rank, sha256) so "what was where" stays auditable after
the fact — a cache miss caused by a legitimately changed dossier is then
explainable instead of mysterious.

This module is PURE composition. It never calls a provider, reads a file,
touches the network, or writes evidence. It adds no dependency: the token
estimate rides the repo's existing chars/4 estimator in ``token_economy`` —
Remedy deliberately does not vendor a tokenizer (``tiktoken`` is banned and the
ban is asserted in tests), so every token number here is an ESTIMATE and is
named ``tokens_estimated`` wherever it surfaces.

Scope boundary — deliberate absences (a reader searching here should find this
rather than conclude the wiring was forgotten):
  - No prompt builder is migrated here; that is F105 T003, one builder per
    round, each under a content-equality golden.
  - The manifest is RETURNED but not written into call evidence here; wiring
    ``manifest_as_dicts()`` into the run evidence writer is also T003.
  - The conventions files are not loaded here; the loaders are F105 T002 and
    they import ``CONVENTIONS_TOKEN_CAP`` from this module rather than
    restating the number.

Public API::

    SegmentStabilityRank            — the documented stability scale (IntEnum)
    PromptSegment                   — one named, ranked piece of a prompt
    PromptSegmentManifestEntry      — one audit row: name, rank, sha256, sizes
    ComposedPrompt                  — composed text plus its manifest
    PromptSegmentRegistry           — ordered, duplicate-rejecting collector
    PromptSegmentError              — the one error type of this module
    PROMPT_SEGMENT_DELIMITER        — the join string between segments
    CONVENTIONS_TOKEN_CAP           — the conventions-segment cap, in tokens
    compose_prompt_segments(segments) -> ComposedPrompt
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from enum import IntEnum

from packages.orchestration.token_economy import estimate_text_tokens


# Stable prefixes first so the provider cache can hit them, volatile tails last.
class SegmentStabilityRank(IntEnum):
    """Declared stability of a prompt segment; lower composes earlier."""

    SYSTEM = 0
    CONVENTIONS = 1
    DOSSIER = 2
    JOB_CONTEXT = 3
    TASK = 4
    STEERING = 5


#: A plain blank line, and nothing else (DECISION F105 D1). T003 migrates the
#: existing builders under content-equality goldens, so composition must inject
#: no header, label or marker of its own: anything injected would change the
#: bytes of every migrated prompt and make content-equality unprovable.
PROMPT_SEGMENT_DELIMITER = "\n\n"

#: Hard cap for the role conventions segments (F105 feature file). Exported so
#: the T002 loaders import the number instead of restating it. Tokens here are
#: the chars/4 ESTIMATE, never a tokenizer count.
CONVENTIONS_TOKEN_CAP = 800


class PromptSegmentError(Exception):
    """Raised on a rejected segment: bad name, duplicate name, or over cap."""


@dataclass(frozen=True)
class PromptSegment:
    """One named, ranked piece of a prompt. Immutable once registered."""

    name: str
    rank: SegmentStabilityRank
    text: str


@dataclass(frozen=True)
class PromptSegmentManifestEntry:
    """One audit row: what segment sat where, and what its bytes hashed to."""

    name: str
    rank: int
    sha256: str
    chars: int
    tokens_estimated: int


@dataclass(frozen=True)
class ComposedPrompt:
    """A composed prompt plus the manifest of the segments that produced it.

    ``deduped_names`` holds the names of the segments whose TEXT was replaced by
    a reference marker before composition, in the order they were replaced. It
    is empty for every composition that deduped nothing, which is every
    composition THIS module performs: ``compose_prompt_segments`` never sets it,
    because this module has no opinion about dedupe and does not import it.
    F109's composition hook attaches the names after the fact, to the composed
    object it gets back. The field deliberately does NOT appear in
    ``manifest_as_dicts()`` — the ``call_segments`` table in ``token_ledger.py``
    mirrors those row keys column for column, so widening them is a token-ledger
    change and not this one.
    """

    text: str
    manifest: tuple[PromptSegmentManifestEntry, ...]
    deduped_names: tuple[str, ...] = ()

    def manifest_as_dicts(self) -> list[dict[str, str | int]]:
        """JSON-ready manifest rows, in composition order.

        The evidence writer that consumes these is F105 T003; this method is
        the seam it will call, so the manifest shape is pinned here first.
        """
        return [
            {
                "name": entry.name,
                "rank": entry.rank,
                "sha256": entry.sha256,
                "chars": entry.chars,
                "tokens_estimated": entry.tokens_estimated,
            }
            for entry in self.manifest
        ]


class PromptSegmentRegistry:
    """Collects prompt segments in registration order, rejecting duplicates.

    Registration order is load-bearing: it is the tie-break between segments of
    equal rank, so composition stays deterministic instead of depending on dict
    or set iteration order.
    """

    def __init__(self) -> None:
        self._segments: list[PromptSegment] = []
        self._names: set[str] = set()

    def register(
        self,
        name: str,
        rank: SegmentStabilityRank,
        text: str,
        *,
        token_cap: int | None = None,
    ) -> PromptSegment:
        """Append a segment and return it. Raises ``PromptSegmentError`` on a
        blank name, a name already registered, or an over-cap ``token_cap``."""
        if not isinstance(name, str) or not name.strip():
            raise PromptSegmentError("prompt segment name must be a non-empty string")
        if name in self._names:
            raise PromptSegmentError(f"duplicate prompt segment name: {name!r}")
        try:
            resolved_rank = SegmentStabilityRank(rank)
        except ValueError as exc:
            raise PromptSegmentError(
                f"prompt segment {name!r} has an unknown stability rank: {rank!r}"
            ) from exc
        if token_cap is not None:
            estimated = estimate_text_tokens(text)
            if estimated > token_cap:
                raise PromptSegmentError(
                    f"prompt segment {name!r} is over its token cap: "
                    f"{estimated} tokens estimated, cap {token_cap}"
                )
        segment = PromptSegment(name=name, rank=resolved_rank, text=text)
        self._segments.append(segment)
        self._names.add(name)
        return segment

    def registered_segments(self) -> tuple[PromptSegment, ...]:
        """Every registered segment, in registration order (not rank order)."""
        return tuple(self._segments)


def compose_prompt_segments(segments: Sequence[PromptSegment]) -> ComposedPrompt:
    """Order ``segments`` by (rank, registration index) and join them.

    The sort is stable by construction — the registration index is part of the
    key — so equal ranks keep the order they were registered in and the same
    inputs always produce the same bytes. An empty sequence is not an error: it
    composes to empty text with an empty manifest.
    """
    ordered = [
        segment
        for _, segment in sorted(
            enumerate(segments), key=lambda pair: (int(pair[1].rank), pair[0])
        )
    ]
    text = PROMPT_SEGMENT_DELIMITER.join(segment.text for segment in ordered)
    manifest = tuple(_manifest_entry_for_segment(segment) for segment in ordered)
    return ComposedPrompt(text=text, manifest=manifest)


def _manifest_entry_for_segment(segment: PromptSegment) -> PromptSegmentManifestEntry:
    encoded = segment.text.encode("utf-8")
    return PromptSegmentManifestEntry(
        name=segment.name,
        rank=int(segment.rank),
        sha256=hashlib.sha256(encoded).hexdigest(),
        chars=len(segment.text),
        tokens_estimated=estimate_text_tokens(segment.text),
    )

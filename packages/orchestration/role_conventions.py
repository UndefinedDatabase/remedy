"""
Role conventions loaders — the conventions prompt segment (F105 T002).

The worker and the reviewer conventions live in ``docs/agents/`` as reviewed
documents. This module LOADS them, verbatim, and registers each one as the
``CONVENTIONS``-ranked segment of a caller's prompt segment registry. The bytes
that reach a prompt are the bytes on disk: no strip, no re-wrap, no dedent, no
header, no label. That is what makes "extracting the conventions changed no
rule" a provable property instead of a claim.

Remedy deliberately does NOT provide a writer for either document. The rules
change through a reviewed diff of the documents themselves, so the absence of a
write path here is the enforcement rather than an omission — the same discipline
``orchestrator_protocol_text`` holds in ``orchestrator_loop``.

Scope boundary — deliberate absences (a reader searching here should find this
rather than conclude the wiring was forgotten):
  - No composed prompt is returned here. Composition stays in
    ``prompt_segments.compose_prompt_segments``, and migrating the real prompt
    builders onto it is F105 T003, one builder per round.
  - The token cap is not re-checked here. ``CONVENTIONS_TOKEN_CAP`` is IMPORTED
    from ``prompt_segments`` and handed to the registry, which enforces it — one
    spelling per concept, one place to change the number.
  - Nothing here calls a provider, opens the network, or shells out, and no
    tokenizer is imported: the cap rides the repo's chars/4 ESTIMATE.

Public API::

    ConventionsRole                 — the roles that have a conventions document
    CONVENTIONS_DOC_RELATIVE_PATHS  — role -> repo-relative document path
    CONVENTIONS_SEGMENT_NAMES       — role -> registered segment name
    RoleConventionsError            — a missing or unreadable document
    role_conventions_document_path(role, repo_root=None) -> Path
    role_conventions_text(role, repo_root=None) -> str
    register_role_conventions_segment(registry, role, *, repo_root=None) -> PromptSegment
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from packages.orchestration.prompt_segments import (
    CONVENTIONS_TOKEN_CAP,
    PromptSegment,
    PromptSegmentError,
    PromptSegmentRegistry,
    SegmentStabilityRank,
)


# The roles that carry their own conventions document. A str mixin keeps the
# member usable as a plain key; Python here is 3.10, which has no ``StrEnum``.
class ConventionsRole(str, Enum):
    """A prompt role whose conventions are authored as a reviewed document."""

    WORKER = "worker"
    REVIEWER = "reviewer"


#: Where each role's conventions document lives, relative to the repo root.
#: Keeping both under ``docs/agents/`` puts them beside the other role docs.
CONVENTIONS_DOC_RELATIVE_PATHS: dict[ConventionsRole, str] = {
    ConventionsRole.WORKER: "docs/agents/worker_conventions.md",
    ConventionsRole.REVIEWER: "docs/agents/reviewer_conventions.md",
}

#: The segment name each role's conventions register under. Names are stable:
#: they appear in the segment manifest, so renaming one rewrites audit history.
CONVENTIONS_SEGMENT_NAMES: dict[ConventionsRole, str] = {
    ConventionsRole.WORKER: "worker_conventions",
    ConventionsRole.REVIEWER: "reviewer_conventions",
}


class RoleConventionsError(PromptSegmentError):
    """A conventions document is missing or unreadable.

    Subclasses ``PromptSegmentError`` so one ``except PromptSegmentError``
    catches every rejection from the conventions layer — a missing document and
    an over-cap document are the same kind of problem to a caller building a
    prompt, and both should fail the same way.
    """


def _repo_root() -> Path:
    """This repository's root, derived from this file's own location."""
    return Path(__file__).resolve().parents[2]


def role_conventions_document_path(
    role: ConventionsRole, repo_root: Path | None = None
) -> Path:
    """Absolute path of ``role``'s conventions document."""
    return (repo_root or _repo_root()) / CONVENTIONS_DOC_RELATIVE_PATHS[role]


def role_conventions_text(role: ConventionsRole, repo_root: Path | None = None) -> str:
    """``role``'s conventions document, decoded as utf-8 and otherwise untouched.

    Raises ``RoleConventionsError`` when the document is missing or unreadable.
    """
    path = role_conventions_document_path(role, repo_root)
    # Verbatim: no strip, no newline rewriting, no dedent. This read IS the
    # content-equality guarantee that loading the conventions changed no rule.
    try:
        return path.read_bytes().decode("utf-8")
    except OSError as exc:
        raise RoleConventionsError(
            f"conventions document for role {role.value!r} is missing or "
            f"unreadable: {CONVENTIONS_DOC_RELATIVE_PATHS[role]}"
        ) from exc


def register_role_conventions_segment(
    registry: PromptSegmentRegistry,
    role: ConventionsRole,
    *,
    repo_root: Path | None = None,
) -> PromptSegment:
    """Register ``role``'s conventions into ``registry`` and return the segment.

    The CALLER's registry is used rather than a fresh one because registration
    order is the tie-break between segments of equal rank — the caller composing
    the prompt is the only party that can own that order.

    The cap is enforced by the registry, not by a second check here, so an
    over-cap document surfaces the registry's ``PromptSegmentError``.
    """
    return registry.register(
        CONVENTIONS_SEGMENT_NAMES[role],
        SegmentStabilityRank.CONVENTIONS,
        role_conventions_text(role, repo_root),
        token_cap=CONVENTIONS_TOKEN_CAP,
    )

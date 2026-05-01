"""
Artifact index helpers for Remedy.

Provides convenience functions for querying Job.artifacts by ArtifactKind.

All helpers are read-only — they never mutate the job or its artifacts.
All helpers accept a sequence of Artifact objects rather than a Job directly
so they can also be used with arbitrary artifact lists (e.g. slices, filtered
sets) without coupling to the Job model.

Public API:
  artifacts_by_kind(artifacts, kind)        → list[Artifact]
  first_artifact_by_kind(artifacts, kind)   → Artifact | None
  task_artifacts_by_kind(artifacts, task_id, kind) → list[Artifact]
  planning_artifact(artifacts)              → Artifact | None
"""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from packages.core.models import Artifact, ArtifactKind


def artifacts_by_kind(
    artifacts: Sequence[Artifact],
    kind: ArtifactKind,
) -> list[Artifact]:
    """Return all artifacts with the given kind, in original order."""
    return [a for a in artifacts if a.kind == kind]


def first_artifact_by_kind(
    artifacts: Sequence[Artifact],
    kind: ArtifactKind,
) -> Artifact | None:
    """Return the first artifact with the given kind, or None."""
    for a in artifacts:
        if a.kind == kind:
            return a
    return None


def task_artifacts_by_kind(
    artifacts: Sequence[Artifact],
    task_id: UUID,
    kind: ArtifactKind,
) -> list[Artifact]:
    """Return all artifacts for the given task_id with the given kind."""
    return [a for a in artifacts if a.task_id == task_id and a.kind == kind]


def planning_artifact(artifacts: Sequence[Artifact]) -> Artifact | None:
    """Return the planning artifact, or None if not found.

    Prefers explicit kind=PLANNING.  Falls back to the legacy convention
    (name="planning_output" and task_id=None) for artifacts produced before
    Step 14 that carry kind=UNKNOWN.

    The explicit-kind path is preferred so that if a future step introduces
    a new planning artifact with a different name, it will still be found
    without a name-string change here.
    """
    # Prefer explicit kind=PLANNING (Step 14+).
    for a in artifacts:
        if a.kind == ArtifactKind.PLANNING:
            return a
    # Legacy fallback for pre-Step-14 artifacts (kind=UNKNOWN).
    for a in artifacts:
        if a.name == "planning_output" and a.task_id is None:
            return a
    return None

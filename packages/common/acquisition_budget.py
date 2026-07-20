"""F4 (round 26): the ONE shared staged-byte acquisition budget.

Both the standalone directory reader (``build_review_manifest._view_from_dir``) and the coordinator's
``build_review_zip._StagedArtifacts`` charge every acquired member against an instance of THIS class,
so there is a single definition of "how many members / how many bytes / how large a member / no
duplicate logical acquisition" a review-package build may load. Exceeding any limit raises
:class:`AcquisitionBudgetError` — a BLOCK, never a silently-absent or silently-skipped member.

Dependency-free (stdlib only) so the standalone review-packaging scripts stay importable in the
minimal isolated environments the archive-mechanics tests use.
"""
from __future__ import annotations

#: Defaults — generous for a real evidence tree, small enough to bound memory.
MAX_MEMBER_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024
MAX_MEMBERS = 20000


class AcquisitionBudgetError(Exception):
    """A staged-byte acquisition exceeded a per-member, aggregate or count limit, or re-acquired the
    same logical member."""


class AcquisitionBudget:
    """Tracks one acquisition: logical member count, aggregate bytes, per-member bytes and duplicate
    logical acquisition. ``charge(rel, nbytes)`` raises the instant any limit is exceeded; a cached
    re-read of the SAME member must NOT call ``charge`` (that would trip the duplicate guard)."""

    def __init__(self, *, max_members=None, max_total_bytes=None, max_member_bytes=None):
        self.max_members = MAX_MEMBERS if max_members is None else max_members
        self.max_total_bytes = MAX_TOTAL_BYTES if max_total_bytes is None else max_total_bytes
        self.max_member_bytes = MAX_MEMBER_BYTES if max_member_bytes is None else max_member_bytes
        self.members = 0
        self.total = 0
        self._seen: set = set()

    def charge(self, rel: str, nbytes: int) -> None:
        if rel in self._seen:
            raise AcquisitionBudgetError(f"logical member {rel!r} was acquired twice")
        if nbytes > self.max_member_bytes:
            raise AcquisitionBudgetError(
                f"member {rel!r} is {nbytes} bytes, over the per-member limit {self.max_member_bytes}")
        if self.members >= self.max_members:
            raise AcquisitionBudgetError(
                f"acquiring {rel!r} would exceed the member-count limit {self.max_members}")
        if self.total + nbytes > self.max_total_bytes:
            raise AcquisitionBudgetError(
                f"acquiring {rel!r} would exceed the aggregate-byte limit {self.max_total_bytes}")
        self._seen.add(rel)
        self.members += 1
        self.total += nbytes

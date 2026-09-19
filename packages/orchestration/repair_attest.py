"""The attestable-source policy and the safe-diff hashing an attested task's Evidence shares.

An operator repair is attested no longer (F273, finding R-0914): the writer that recorded one
under a job's evidence directory lost its only command word with F261 and was then deleted. What
stays here is what the closure evidence producer
``job_evidence.create_manual_completion_bundle``, the review subject and the review package
builders still read: which paths are attestable source, how a ``safe.diff`` is spelled, and how
its provenance is hashed.
"""
from __future__ import annotations

import hashlib
from typing import Any


def is_attestable_source(rel: str) -> bool:
    """F9 (round 13): is this file part of a task's ATTESTED source change?

    `.agent/context.md`, `.agent/plan.md` and `.agent/live_review.md` are OPERATOR STATE — the
    notes the operator keeps about the work, not the work. Every authoritative Evidence view
    already says so and excludes them (`final_verifier._OPERATIONAL_PREFIXES`,
    `change_provenance_gate._EXCLUDE_DIRS`, the packager's alignment scan). The ATTESTED union
    was the one view that did not, so a hand-attested diff containing them disagreed with every
    proof set built from the same change — and the package was correctly refused as
    non-authoritative:

        changed-file union mismatch vs current_change_content_proof.file_hashes:
          only_in_union=['.agent/context.md', '.agent/live_review.md', '.agent/plan.md']

    One policy, applied at the one place that dissented. The files still travel in the review ZIP
    as non-authoritative operator context — excluded from the proofs, not from the reader.

    The predicate is the EXISTING one (A6: no parallel taxonomy) — imported, not re-stated.
    """
    from packages.orchestration.final_verifier import _is_source_for_alignment

    return _is_source_for_alignment(rel)


# ---------------------------------------------------------------------------
# Canonical provenance hashing — ONE shared implementation used by both the
# writer (job_evidence.create_manual_completion_bundle) and the validator
# (build_review_manifest). Any drift between the two would let a tampered
# bundle validate, so they must call this.
# ---------------------------------------------------------------------------

def canonical_provenance_sha256(
    tracked_diff_sha256: str,
    untracked_file_hashes: list[dict[str, Any]],
) -> str:
    """Deterministic provenance hash over tracked diff + sorted untracked files.

    Recomputed from: the tracked diff hash, then for each untracked file (sorted
    by path) the path, its content sha256, and its byte size.
    """
    h = hashlib.sha256()
    h.update(str(tracked_diff_sha256).encode("utf-8"))
    for uf in sorted(untracked_file_hashes, key=lambda u: str(u.get("path", ""))):
        h.update(str(uf.get("path", "")).encode("utf-8"))
        h.update(str(uf.get("sha256", "")).encode("utf-8"))
        h.update(str(uf.get("size_bytes", "")).encode("utf-8"))
    return h.hexdigest()


def build_safe_diff_text(
    tracked_diff: str,
    untracked_file_hashes: list[dict[str, Any]],
) -> str:
    """Build the exact ``safe.diff`` content: tracked diff + untracked headers.

    Kept in one place so the emitted content and its recorded ``safe_diff_sha256``
    can never diverge.
    """
    parts = [tracked_diff]
    for uf in untracked_file_hashes:
        parts.append(
            f"--- /dev/null\n+++ b/{uf['path']}\n"
            f"# new untracked file (sha256={uf['sha256']}, "
            f"size={uf['size_bytes']})\n"
        )
    return "".join(parts)


def sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def parse_safe_diff_paths(safe_diff_text: str) -> list[str]:
    """Return sorted unique file paths represented in a ``safe.diff``.

    Reads ``+++ b/<path>`` headers (skipping ``/dev/null``); handles both the
    tracked ``git diff`` hunks and the untracked ``+++ b/<path>`` markers.
    """
    paths: set[str] = set()
    for line in safe_diff_text.splitlines():
        if line.startswith("+++ "):
            p = line[4:].strip()
            if p.startswith("b/"):
                p = p[2:]
            if p and p != "/dev/null":
                paths.add(p)
    return sorted(paths)

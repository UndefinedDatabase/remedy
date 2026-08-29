"""LANDING an approved hunk selection: the seam between the subset diff and the applier.

WHY this module exists: two earlier pieces of F033 answer WHETHER a selection is coherent and
WHICH BYTES it means, and something must then hand those bytes to the applier and report what
came back in the vocabulary the operator approved in — HUNKS, not files. ``apply_structured_patch``
answers in files-modified counts and error strings; an approval screen needs "these hunk ids
landed" or "these hunk ids are why nothing did". Translating between the two is this module's
entire job, so it is a SEAM rather than a layer: it builds one ``StructuredPatch``, makes one
call, and turns one ``ApplyResult`` into one ``HunkApplyOutcome``.

THE ATOMICITY IS INHERITED, NOT BUILT HERE, and that is deliberate. ``apply_structured_patch``
already takes a mandatory verified snapshot of exactly the paths its patch names, applies each
unified diff in turn, and on ANY failure restores from that snapshot and stops — so a conflict
inside the approved set falls back to nothing-applied WHENEVER THAT RESTORE FINISHES. A second
rollback written here would be a second answer to one question, free to drift from the first, so
this module snapshots nothing, restores nothing and writes no file itself. There is one exception
and it is the reason ``_failure_lead_sentence`` exists: when the applier reports that its OWN
rollback did not finish, the fallback did not complete either and files written before the failure
may still be on disk. This module's job is then to SAY so, for exactly the reason it builds no
rollback of its own — repairing the applier's half-restored tree from here would be that second
answer. ``landed`` is EMPTY whenever ``applied`` is false, because this module learns WHICH hunks
landed only from a SUCCESSFUL apply and so has no per-hunk answer to give on failure; a partial
state on disk is reported in the MESSAGE, never by half-filling ``landed``.

DELIBERATE ABSENCE — it also runs NO permission check and NO approval check of its own. The
applier owns that boundary, refusing without the ``repo_generated_write`` capability and
without an APPROVED intent, and a copy of those rules here would be a second gate to keep in
step with the first. ``job``, ``intent_id`` and ``data_dir`` are passed through UNCHANGED.

DELIBERATE ABSENCE — it does not decide whether a selection is coherent, does not know what a
hunk id is made of, and holds no diff parsing of its own. A reader who wants whether a
decision is coherent at all wants ``packages/orchestration/hunk_approval.py``; one who wants
which bytes an approved selection means wants ``packages/orchestration/hunk_subset_diff.py``;
one who wants the apply mechanics — the snapshot, the rollback, the strict splicer — wants
``packages/orchestration/source_apply.py``; one who wants where a hunk id COMES FROM wants
``packages/orchestration/hunk_identity.py``.

THIS MODULE IS NOT TOTAL, and unlike its two siblings it must not pretend to be. ``hunk_approval``
and ``hunk_subset_diff`` are pure text-in, text-out and run WHILE the approval screen renders, so
a raise there takes down the very screen that exists to show the operator what is strange, and
totality there costs nothing because there is nothing that can legitimately fail. Here there is:
this module performs I/O through the applier, and a repository that disappeared mid-call, a
directory that is not readable, or a fence violation are REAL failures. Flattening an ``OSError``
into a polite ``HunkApplyOutcome`` would report "conflict" for a broken disk and send the
operator to re-diff a file that is not there. So it catches nothing it cannot name: every
exception the applier raises propagates to the caller unchanged.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import UUID

from packages.orchestration.hunk_subset_diff import (
    ApprovedSubsetDiff,
    SubsetRefusal,
    build_approved_subset_diff,
)
from packages.orchestration.source_apply import apply_structured_patch
from packages.orchestration.structured_patch import StructuredPatch, UnifiedDiff

# The failure codes. Each gets its own module-level NAME so a caller matches on the name and
# never on a message. They name the three ways an approved selection fails to land, and nothing
# else: a success carries the empty string.

#: ``build_approved_subset_diff`` refused, so there are no bytes to hand anyone. Its OWN code and
#: message are carried through in ``message`` and its offending ids in ``blocked``, because the
#: wrapping must lose no information the operator needs to repair the selection.
HUNK_APPLY_REFUSED = "subset_refused"
#: The applier reported failure. Named CONFLICT for the case that dominates — an approved hunk no
#: longer fits the file — but it covers every failure the applier reports, including the ones that
#: stop before any file is touched.
HUNK_APPLY_CONFLICT = "conflict"
#: The subset came back with no files at all, so there is nothing to apply. Landing nothing is not
#: an all-or-nothing apply of nothing, and calling the applier with an empty patch would mint an
#: apply id for a mutation that never existed.
HUNK_APPLY_NOTHING_TO_APPLY = "nothing_to_apply"

# THE APPLIER'S ROLLBACK VOCABULARY, RESTATED RATHER THAN IMPORTED. ``_rollback_from_snapshot`` in
# ``packages/orchestration/source_apply.py`` appends an error starting with one of these prefixes
# when the restore it attempted did not finish — the snapshot would not load, or a file could not
# be put back — and those errors arrive here in the same ``ApplyResult.errors`` list as every
# other failure. They are RESTATED rather than imported on purpose: they are that function's
# PRIVATE message vocabulary, and importing a private name to read a message would couple this
# seam to the applier's WORDING instead of to its BEHAVIOUR, which is the coupling this whole
# module exists to avoid. The trailing space on the second is load-bearing — it keeps the prefix
# off any longer word that merely starts the same way.
_ROLLBACK_UNFINISHED_PREFIXES = ("rollback_failed:", "rollback_incomplete ")


@dataclass(frozen=True)
class HunkApplyOutcome:
    """What happened to an approved selection, in HUNK ids rather than in file counts.

    ``landed`` is EMPTY whenever ``applied`` is false — a caller must not have to check two
    fields to learn that nothing landed, because there is no partial landing to distinguish it
    from. ``blocked`` is the mirror: empty on success, and on failure the ids the failure is
    attributable to. ``apply_id`` is the applier's own id, or ``""`` when no apply was attempted
    at all, which is how a caller tells "the applier refused" from "the applier was never
    called". ``message`` is one human sentence and is never parsed; ``code`` is what a caller
    matches on."""

    applied: bool
    apply_id: str
    landed: tuple[str, ...]
    blocked: tuple[str, ...]
    code: str
    message: str


def _blocked_ids(subset: ApprovedSubsetDiff, errors: list[str]) -> tuple[str, ...]:
    """The ids a failed apply is attributable to.

    TWO CASES, and the distinction is the whole point. FIRST, a per-file failure: the applier
    reports one ``f"{path}: {reason}"`` string per file it could not apply, so a file whose path
    prefixes an error line is a file that failed, and ITS hunks are the blocked ones. That is a
    MEMBERSHIP test against paths this module already knows exactly — never a parse of an error
    message, whose wording belongs to the applier and may change. SECOND, a failure that names
    no file at all: a missing permission, an unapproved intent, a snapshot that would not verify,
    a fence refusal. Every one of those stops before any file is touched, so the whole selection
    was blocked and every selected id is reported."""
    attributed: list[str] = []
    for subset_file in subset.files:
        prefix = subset_file.path + ": "
        if any(error.startswith(prefix) for error in errors):
            attributed.extend(subset_file.hunk_ids)
    if attributed:
        return tuple(attributed)
    return subset.selected


def _rollback_did_not_finish(errors: list[str]) -> bool:
    """Whether the applier reported that its OWN rollback did not complete.

    A MEMBERSHIP test against the prefixes above, never a parse of the message that follows one:
    the count of files and their names belong to the applier and may change without notice."""
    return any(
        error.startswith(prefix)
        for error in errors
        for prefix in _ROLLBACK_UNFINISHED_PREFIXES
    )


def _failure_lead_sentence(errors: list[str]) -> str:
    """The leading sentence of a failure message, DERIVED from the errors rather than asserted.

    The applier's rollback is what makes "nothing was applied" true on disk, so this module may
    only claim it when that rollback finished. When it did not, files written before the failure
    may still be there, and the sentence says so rather than denying it with the contradicting
    evidence concatenated after the claim.

    DELIBERATE ABSENCE — no fourth failure code is minted for this state. ``code`` stays
    ``HUNK_APPLY_CONFLICT``, because nothing machine-readable is wrong here and a new code would
    make every existing caller's match incomplete for a state that is a strictly worse version of
    the one it already handles. The difference is in the MESSAGE, which is what an operator reads
    when deciding whether to re-diff or to inspect the tree by hand.

    DELIBERATE ABSENCE — the affected files are NOT re-named in this sentence. The applier's own
    ``rollback_incomplete (N file(s)): a; b`` already names them and is concatenated directly
    after it, so a second naming here would only be a second list free to drift from the first."""
    if _rollback_did_not_finish(errors):
        return (
            "No approved hunk was applied, and the rollback did not finish, so the repository "
            "may still hold part of the change — inspect it before re-diffing. "
        )
    return "No approved hunk was applied; the repository is unchanged. "


# The one entry point: land exactly the approved hunks, all of them or none of them.
def apply_approved_hunks(
    diff_text: str,
    approved_hunk_ids: Iterable[str],
    repo_path: Path,
    *,
    job: Any,
    intent_id: str,
    data_dir: str | None = None,
    job_id: UUID | None = None,
) -> HunkApplyOutcome:
    """Apply exactly the approved hunks of ``diff_text`` to ``repo_path``, all or nothing.

    Returns a ``HunkApplyOutcome``. On success every approved hunk landed and ``landed`` names
    them in the subset's order; on any failure NOTHING landed, ``landed`` is empty and ``code``
    names which of the three failures it was. Raises whatever the applier raises: this module is
    not total, on purpose, and the docstring above says why.
    """
    subset = build_approved_subset_diff(diff_text, approved_hunk_ids)

    if isinstance(subset, SubsetRefusal):
        # NOTHING IS WRITTEN here: the applier is not called at all. The subset builder's own
        # code and message are carried through verbatim, so no information is lost by wrapping.
        return HunkApplyOutcome(
            applied=False,
            apply_id="",
            landed=(),
            blocked=subset.hunk_ids,
            code=HUNK_APPLY_REFUSED,
            message=f"The approved selection was refused before anything was applied "
                    f"({subset.code}): {subset.message}",
        )

    if not subset.files:
        # Unreachable through ``build_approved_subset_diff`` itself, which refuses an empty
        # approved set and refuses an id the diff does not carry, so every subset it returns has
        # at least one file. Kept as a named outcome rather than an assertion, because a caller
        # that ever synthesises an ``ApprovedSubsetDiff`` must not be able to mint an apply id
        # for a mutation that never existed.
        return HunkApplyOutcome(
            applied=False,
            apply_id="",
            landed=(),
            blocked=(),
            code=HUNK_APPLY_NOTHING_TO_APPLY,
            message="The approved selection names no file to change, so nothing was applied.",
        )

    # ``target_paths`` is set as well as ``unified_diffs``, in the same order: the applier
    # validates the two separately, and derives the snapshot path set from the diffs, so the
    # snapshot covers exactly the files this subset touches and the rollback is therefore total.
    patch = StructuredPatch(
        intent_kind="unified_diff",
        unified_diffs=tuple(
            UnifiedDiff(path=subset_file.path, diff=subset_file.diff)
            for subset_file in subset.files
        ),
        target_paths=tuple(subset_file.path for subset_file in subset.files),
    )

    result = apply_structured_patch(
        patch,
        repo_path,
        data_dir=data_dir,
        job_id=job_id,
        job=job,
        intent_id=intent_id,
    )

    if result.success:
        return HunkApplyOutcome(
            applied=True,
            apply_id=result.apply_id,
            landed=subset.selected,
            blocked=(),
            code="",
            message=f"Applied {len(subset.selected)} approved hunk(s) across "
                    f"{len(subset.files)} file(s).",
        )

    blocked = _blocked_ids(subset, result.errors)
    return HunkApplyOutcome(
        applied=False,
        apply_id=result.apply_id,
        landed=(),
        blocked=blocked,
        code=HUNK_APPLY_CONFLICT,
        message=_failure_lead_sentence(result.errors)
                + ("; ".join(result.errors) if result.errors else "The applier reported failure."),
    )

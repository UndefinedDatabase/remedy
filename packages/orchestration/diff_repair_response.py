"""Diff-only repair response record (F111 T002, response half).

A repair round asks the model for a unified diff instead of whole files, and the
answer comes back as one versioned JSON record::

    {"format": "unified_diff", "version": 1, "diff": "...", "files": [...]}

``files`` is what the model DECLARES it changed; ``diff`` is what it actually
changed. This module cross-checks the two BEFORE anything reaches the
applicator, so a diff that quietly touches a path nobody declared — or declares
a path it never touches — becomes a named validation issue instead of a
surprise write.

This module holds NO unified-diff parser. The touched paths come from
``review_scope.parse_diff_line_ranges``, this repository's single reading of
hunk headers, and no second reading grows here.

It holds NO fence policy either. The decision is ``scope_fences.check_change_set``
against the effective spec, and it is called in its NON-RAISING form: an
out-of-fence path comes back as a ``DiffFencePrecheck`` with ``allowed=False``,
a validation rejection the caller can report, rather than a
``FenceViolationError`` thrown out of the middle of an apply.

``structured_patch.UnifiedDiff`` pairs ONE path with ONE diff text, so a
``files`` list longer than one entry is split per path before conversion:
handing every declared path the whole diff would try to apply every hunk to
every file. The splitter is ``review_scope.split_diff_by_path``, the same
single walk that reads hunk headers. Remedy deliberately does not APPLY the
converted patch from this module — that is
``diff_repair_apply.apply_diff_repair``, which the bridge calls in T003 because
the job, the approved intent and the snapshot already live there.

Public API::

    DIFF_REPAIR_RESPONSE_FORMAT — the only accepted ``format`` value
    DIFF_REPAIR_RESPONSE_VERSION — the only accepted ``version`` value
    DiffRepairResponse — one decoded repair answer
    DiffFencePrecheck — the fence decision as data, never as an exception
    parse_diff_repair_response(raw_output)
        -> tuple[DiffRepairResponse | None, str]
    validate_diff_repair_response(response) -> list[str]
    diff_repair_response_to_patch(response) -> StructuredPatch
    precheck_diff_repair_fences(repo_root, response, *, job_fences=None)
        -> DiffFencePrecheck
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.review_scope import (
    parse_diff_line_ranges,
    split_diff_by_path,
)
from packages.orchestration.scope_fences import (
    TouchedPath,
    check_change_set,
    resolve_fence_spec_effective,
)
from packages.orchestration.structured_patch import (
    StructuredPatch,
    UnifiedDiff,
    extract_json_object,
    unsafe_path_issues,
)

# The only ``format`` a diff-only repair answer may carry — anything else is
# rejected by name, never coerced into the diff path by accident.
DIFF_REPAIR_RESPONSE_FORMAT = "unified_diff"

# The record's schema version. A bump means an incompatible shape, so an
# unrecognised version is a rejection rather than a best-effort read.
DIFF_REPAIR_RESPONSE_VERSION = 1


# One decoded repair answer: the diff the model produced plus the files it claims
# that diff touches. Decoded only — validation is a separate, explicit step.
@dataclass(frozen=True)
class DiffRepairResponse:
    """A parsed diff-only repair answer, not yet validated."""

    diff: str
    files: tuple[str, ...]
    format: str = DIFF_REPAIR_RESPONSE_FORMAT
    version: int = DIFF_REPAIR_RESPONSE_VERSION


# The fence answer carried as DATA, so an out-of-fence path rejects a response
# instead of raising out of the applicator half-way through a write.
@dataclass(frozen=True)
class DiffFencePrecheck:
    """Whether every declared path survives the effective fence spec."""

    allowed: bool
    denied_paths: tuple[str, ...]
    reasons: tuple[tuple[str, str], ...]  # (path, reason), sorted


# The one decoder for the repair-response wrapper: every rejection carries a
# NAMED reason, so a bad answer is reportable instead of merely falsy.
def parse_diff_repair_response(
    raw_output: str,
) -> tuple[DiffRepairResponse | None, str]:
    """Decode model output into a ``DiffRepairResponse``.

    Returns ``(response, "")`` on success and ``(None, reason)`` otherwise. The
    JSON object is located by ``structured_patch.extract_json_object``, so this
    module contains no second reading of the JSON wrapper.
    """
    json_text = extract_json_object(raw_output)
    if json_text is None:
        return None, "no_json_object"

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return None, "invalid_json"

    if not isinstance(data, dict):
        return None, "not_an_object"

    for field in ("format", "version", "diff", "files"):
        if field not in data:
            return None, f"missing_field:{field}"

    if data["format"] != DIFF_REPAIR_RESPONSE_FORMAT:
        return None, f"wrong_format:{data['format']}"

    if data["version"] != DIFF_REPAIR_RESPONSE_VERSION:
        return None, f"unsupported_version:{data['version']}"

    if not isinstance(data["files"], (list, tuple)):
        return None, "files_not_a_list"

    response = DiffRepairResponse(
        diff=str(data["diff"]),
        files=tuple(str(entry) for entry in data["files"]),
        format=DIFF_REPAIR_RESPONSE_FORMAT,
        version=DIFF_REPAIR_RESPONSE_VERSION,
    )
    return response, ""


# The gate between a decoded answer and the applicator: everything checkable
# without touching the repository, including "does the diff match the declaration".
def validate_diff_repair_response(response: DiffRepairResponse) -> list[str]:
    """Return the issues that block applying this response (empty = applicable).

    Path safety is delegated to ``structured_patch.unsafe_path_issues`` so those
    rules and their exact message strings live in one place. The two cross-check
    lists are emitted sorted, so identical input always yields an identical list.
    """
    issues: list[str] = []

    if not response.diff.strip():
        issues.append("empty diff")

    if not response.files:
        issues.append("empty files list")

    issues.extend(unsafe_path_issues(response.files))

    declared = set(response.files)
    touched = set(parse_diff_line_ranges(response.diff))

    for path in sorted(declared - touched):
        issues.append(f"declared path not touched by the diff: {path}")

    for path in sorted(touched - declared):
        issues.append(f"diff touches undeclared path: {path}")

    return issues


# The one bridge from a repair answer to the shape the existing applicator takes:
# one UnifiedDiff per DECLARED path, each carrying only that path's diff section.
def diff_repair_response_to_patch(response: DiffRepairResponse) -> StructuredPatch:
    """Convert a repair response into the ``StructuredPatch`` the applicator takes.

    One ``structured_patch.UnifiedDiff`` per DECLARED path, in ``response.files``
    order, each carrying ONLY that path's section as cut by
    ``review_scope.split_diff_by_path``.

    Callers run ``validate_diff_repair_response`` FIRST: this function converts,
    it does not judge. A declared path the diff never touches therefore gets an
    EMPTY diff string on purpose — ``structured_patch.validate_structured_patch``
    then rejects it with ``unified_diff <path>: empty diff``, so the failure is
    fail-closed and named instead of a silent no-op apply.
    """
    sections = split_diff_by_path(response.diff)
    diffs = tuple(
        UnifiedDiff(path=path, diff=sections.get(path, ""))
        for path in response.files
    )
    return StructuredPatch(
        intent_kind="unified_diff",
        unified_diffs=diffs,
        target_paths=tuple(response.files),
        applicability="applicable",
        requires_approval=True,
    )


# The fence question asked BEFORE the applicator opens a file, and answered as a
# value: ``check_change_set`` collects every violation and this function raises nothing.
def precheck_diff_repair_fences(
    repo_root: Path,
    response: DiffRepairResponse,
    *,
    job_fences: dict | None = None,
) -> DiffFencePrecheck:
    """Check every declared path against the effective fence spec. Raises nothing."""
    effective = resolve_fence_spec_effective(repo_root, job_fences=job_fences)
    touched = [
        TouchedPath(path=path, operation="modify", role="target")
        for path in response.files
    ]
    result = check_change_set(repo_root, effective.spec, touched)

    return DiffFencePrecheck(
        allowed=result.allowed,
        denied_paths=tuple(v.path for v in result.violations),
        reasons=tuple((v.path, v.reason) for v in result.violations),
    )

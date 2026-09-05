"""
Approval Queue v1 — metadata-only approval decisions for Patch Intents.

Approval is a recorded decision only. It does not apply patches, modify
repository files, or trigger any automated action. The apply step is not
implemented in this version.

Approval states:
  pending  — no decision recorded yet (the default for any new intent)
  approved — user has reviewed and approved this patch intent
  rejected — user has reviewed and rejected this patch intent

Latest decision wins: approving a rejected intent (or vice versa) is allowed
for v1, since no apply step exists and no state is irrecoverable.

Intent IDs (v1):
  "<artifact_short_id>-<idx>"

  artifact_short_id — first 8 hex characters of the owning artifact's UUID.
  idx               — 0-based index into that artifact's
                      metadata["patch_intent_explanations"] list.

  Example: "a1b2c3d4-0" for the first intent in artifact a1b2c3d4...

Approval data is stored durably in the job artifact metadata under the key
  artifact.metadata["patch_intent_approvals"]

as a dict mapping intent_id → approval dict.  The job must be persisted by
the caller after mutating (save_job is not called here).

No repository files are modified by any function in this module.
No external dependencies beyond the packages already used in this project.

Public API::

    list_patch_intents(job) -> list[dict]
    get_patch_intent(job, intent_id) -> dict | None
    set_approval_state(job, intent_id, state, *, reason=None, decided_by="user") -> dict
    make_intent_id(artifact_id, idx) -> str
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID

from packages.orchestration.patch_intent import RISK_LEVELS, RISK_UNKNOWN

if TYPE_CHECKING:
    from packages.core.models import Artifact, Job


# ---------------------------------------------------------------------------
# Approval state constants
# ---------------------------------------------------------------------------

APPROVAL_PENDING: str = "pending"
APPROVAL_APPROVED: str = "approved"
APPROVAL_REJECTED: str = "rejected"
APPROVAL_STATES: frozenset[str] = frozenset(
    {APPROVAL_PENDING, APPROVAL_APPROVED, APPROVAL_REJECTED}
)

# Max characters of diff preview surfaced in show-patch-intent.
_MAX_DIFF_DISPLAY_CHARS = 300


# ---------------------------------------------------------------------------
# Intent ID helpers
# ---------------------------------------------------------------------------


def make_intent_id(artifact_id: UUID, idx: int) -> str:
    """Build a stable intent ID from artifact UUID + 0-based index.

    Format: "<artifact_short_id>-<idx>"
    Example: "a1b2c3d4-0"
    """
    return f"{artifact_id.hex[:8]}-{idx}"


def _parse_intent_id(intent_id: str) -> tuple[str, int] | None:
    """Parse an intent_id into (short_artifact_id, idx) or return None.

    Uses rfind("-") to handle the fixed "<8hex>-<idx>" format robustly.
    Returns None if the format is invalid.
    """
    sep = intent_id.rfind("-")
    if sep < 0:
        return None
    short_id = intent_id[:sep]
    idx_str = intent_id[sep + 1 :]
    if not short_id or not idx_str:
        return None
    try:
        idx = int(idx_str)
    except ValueError:
        return None
    if idx < 0:
        return None
    return short_id, idx


def _find_artifact_for_intent(
    job: Job, intent_id: str
) -> tuple[Artifact, int] | None:
    """Resolve an intent_id to (artifact, idx).

    Returns None if the intent_id is malformed or no matching artifact exists.
    """
    parsed = _parse_intent_id(intent_id)
    if parsed is None:
        return None
    short_id, idx = parsed
    for artifact in job.artifacts:
        if artifact.id.hex[:8] == short_id:
            explanations = artifact.metadata.get("patch_intent_explanations", [])
            if 0 <= idx < len(explanations):
                return artifact, idx
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def list_patch_intents(job: Job) -> list[dict]:
    """Return all patch intents across the job with their current approval state.

    Scans ``job.artifacts`` for any artifact that has a
    ``patch_intent_explanations`` list in its metadata.  Each explanation
    entry becomes one intent record in the returned list.

    Invalid stored risk values (not in RISK_LEVELS) are coerced to
    RISK_UNKNOWN rather than propagating silently.

    The returned dicts contain:
      intent_id        — stable CLI-usable identifier
      artifact_id      — full UUID string of the owning artifact
      artifact_id_short — first 8 hex chars of artifact UUID
      task_id          — task UUID string or None
      target_path      — repo-relative path that would be changed
      action           — "create" | "modify" | "preview-only"
      risk             — validated risk level (RISK_LEVELS; RISK_UNKNOWN if bad)
      reason           — human-readable derivation reason
      summary          — truncated intent text
      created_at       — ISO datetime string or None (set once, at intent-derivation time)
      state            — APPROVAL_PENDING | APPROVAL_APPROVED | APPROVAL_REJECTED
      decided_at       — ISO datetime string or None
      decided_by       — who recorded the decision, or None
      approval_reason  — optional free-text reason supplied by the user
    """
    result: list[dict] = []
    for artifact in job.artifacts:
        explanations = artifact.metadata.get("patch_intent_explanations", [])
        if not explanations:
            continue
        approvals: dict = artifact.metadata.get("patch_intent_approvals", {})
        for idx, exp in enumerate(explanations):
            intent_id = make_intent_id(artifact.id, idx)
            approval = approvals.get(intent_id, {})
            # Validate stored risk value; coerce unknown values to RISK_UNKNOWN.
            stored_risk = exp.get("risk", RISK_UNKNOWN)
            risk = stored_risk if stored_risk in RISK_LEVELS else RISK_UNKNOWN
            result.append(
                {
                    "intent_id": intent_id,
                    "artifact_id": str(artifact.id),
                    "artifact_id_short": artifact.id.hex[:8],
                    "task_id": str(artifact.task_id) if artifact.task_id else None,
                    "target_path": exp.get("file", ""),
                    "action": exp.get("action", ""),
                    "risk": risk,
                    "reason": exp.get("reason", ""),
                    "summary": exp.get("summary", ""),
                    "created_at": exp.get("created_at"),
                    "state": approval.get("state", APPROVAL_PENDING),
                    "decided_at": approval.get("decided_at"),
                    "decided_by": approval.get("decided_by"),
                    "approval_reason": approval.get("reason"),
                }
            )
    return result


def get_patch_intent(job: Job, intent_id: str) -> dict | None:
    """Return a single patch intent record by intent_id, or None if not found."""
    for item in list_patch_intents(job):
        if item["intent_id"] == intent_id:
            return item
    return None


def set_approval_state(
    job: Job,
    intent_id: str,
    state: str,
    *,
    reason: str | None = None,
    decided_by: str = "user",
) -> dict:
    """Record an approval decision on a patch intent.

    Updates ``artifact.metadata["patch_intent_approvals"][intent_id]``
    in-place.  Latest decision wins — this function can be called repeatedly
    to change state (e.g. approve after reject).

    The caller is responsible for persisting the job (``save_job``) after
    this call returns.

    Args:
        job:        the job whose artifact metadata will be updated.
        intent_id:  the intent to approve or reject.
        state:      ``"approved"`` or ``"rejected"`` (not ``"pending"`` — that
                    is the implicit default; there is no "un-decide" operation).
        reason:     optional free-text note from the user (not logged raw).
        decided_by: who is recording the decision (default: "user").

    Returns:
        The newly recorded approval dict.

    Raises:
        ValueError: if ``state`` is not in APPROVAL_STATES, or if
                    ``intent_id`` is not found in the job.
    """
    if state not in APPROVAL_STATES:
        raise ValueError(
            f"Invalid approval state {state!r}.  "
            f"Valid values: {sorted(APPROVAL_STATES)}"
        )

    found = _find_artifact_for_intent(job, intent_id)
    if found is None:
        raise ValueError(
            f"Patch intent {intent_id!r} not found in job {job.id}.  "
            "Use 'remedy patch list <job_id>' to see available intent IDs."
        )

    artifact, idx = found
    exp = artifact.metadata["patch_intent_explanations"][idx]
    stored_risk = exp.get("risk", RISK_UNKNOWN)
    risk = stored_risk if stored_risk in RISK_LEVELS else RISK_UNKNOWN

    if "patch_intent_approvals" not in artifact.metadata:
        artifact.metadata["patch_intent_approvals"] = {}

    entry = {
        "intent_id": intent_id,
        "target_path": exp.get("file", ""),
        "action": exp.get("action", ""),
        "risk": risk,
        "state": state,
        "decided_at": datetime.now(timezone.utc).isoformat(),
        "decided_by": decided_by,
        "reason": reason,
    }
    artifact.metadata["patch_intent_approvals"][intent_id] = entry
    return entry


# ---------------------------------------------------------------------------
# Display helpers (used by CLI render functions)
# ---------------------------------------------------------------------------


def format_intent_list(intents: list[dict]) -> str:
    """Format a list of patch intents as a human-readable table for the CLI.

    Returns a ready-to-print string.  Returns a placeholder message if the
    list is empty.
    """
    if not intents:
        return "No patch intents found for this job."

    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  {'CREATED':<20}  {'DECIDED':<20}  TARGET PATH"]
    lines.append("-" * 92)
    for item in intents:
        lines.append(
            f"{item['intent_id']:<14}  "
            f"{item['state']:<8}  "
            f"{item['risk']:<8}  "
            f"{item['action']:<12}  "
            f"{(item['created_at'] or '-'):<20}  "
            f"{(item['decided_at'] or '-'):<20}  "
            f"{item['target_path']}"
        )
    return "\n".join(lines)


def format_intent_detail(item: dict, diff_preview: str | None) -> str:
    """Format a single patch intent for the show-patch-intent command.

    ``diff_preview`` is an optional truncated preview string from artifact
    metadata; pass None to omit the section.  Full artifact content is never
    rendered here.
    """
    lines = [
        f"Patch Intent: {item['intent_id']}",
        f"  target path : {item['target_path']}",
        f"  action      : {item['action']}",
        f"  risk        : {item['risk']}",
        f"  reason      : {item['reason']}",
        f"  summary     : {item['summary']}",
        f"  state       : {item['state']}",
    ]
    if item["decided_at"]:
        lines.append(f"  decided at  : {item['decided_at']}")
    if item["decided_by"]:
        lines.append(f"  decided by  : {item['decided_by']}")
    if item["approval_reason"]:
        lines.append(f"  note        : {item['approval_reason']}")
    if diff_preview:
        truncated = diff_preview[:_MAX_DIFF_DISPLAY_CHARS]
        suffix = "…" if len(diff_preview) > _MAX_DIFF_DISPLAY_CHARS else ""
        lines.append(f"  diff preview:\n{truncated}{suffix}")
    return "\n".join(lines)

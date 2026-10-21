"""The apply's own questions to the permission matrix, asked through the refusals
``job_apply`` already has: one `write_worktree`, an optional `commit` and an optional `push`
for one apply instance, and one `push` for `remedy do`'s mission-level push (DECISION F141 D3).
"""
from __future__ import annotations

from typing import Any

from packages.orchestration.permission_matrix import (
    APPROVAL_KIND_FLAG,
    InstanceApproval,
    PermissionRefusedError,
    PermissionRequest,
    pinned_job_level,
    require_permission,
    require_permissions,
)

# WHY: the prefix of a refused `write_worktree`, the one apply action none of job_apply's own
# refusal prefixes already names (DECISION F141 D3 (1)).
WRITE_PERMISSION_REFUSED = "permission_refused"


# WHY: checked before anything is written AND again right before anything is written, so a
# denied action still stops the apply and an asked one is granted once per instance, never a
# standing widening of the matrix (DECISION F141 D3 (1)).
def apply_permission_refusals(job: Any, result: Any) -> list[str]:
    """Every prefixed refusal of this apply's `write_worktree`, `commit` and `push`; reads only
    before ``result.status`` is ``approved_apply_started``, then grants each approved action once.
    """
    from packages.orchestration.job_apply import COMMIT_MODE_FLAGS, COMMIT_REFUSED, HISTORY_REFUSED, PUSH_REFUSED

    mode = result.commit_message_mode
    actions: list[str] = ["write_worktree"]
    if mode in COMMIT_MODE_FLAGS:
        actions.append("commit")
    if result.push:
        actions.append("push")
    request = PermissionRequest(
        level=pinned_job_level(str(job.job_id)),
        subject=f"the apply of job {job.job_id}", job_id=str(job.job_id),
    )
    try:
        require_permissions(tuple(actions), request)
    except PermissionRefusedError as exc:
        if exc.action == "push":
            prefix = PUSH_REFUSED
        elif exc.action == "commit":
            prefix = HISTORY_REFUSED if mode == "history" else COMMIT_REFUSED
        else:
            prefix = WRITE_PERMISSION_REFUSED
        return [f"{prefix}: {exc.reason}"]
    if result.status != "approved_apply_started":
        return []
    for action in actions:
        if action == "write_worktree":
            flag = "--approve"
        elif action == "commit":
            flag = COMMIT_MODE_FLAGS[mode]
        else:
            flag = "--push"
        require_permission(action, PermissionRequest(
            level=request.level, subject=request.subject, job_id=request.job_id,
            approval=InstanceApproval(APPROVAL_KIND_FLAG, flag),
        ))
    return []


# WHY: `remedy do`'s walk asks its one mission-level push before the upstreams' and the
# mission's own refusals are even read (DECISION F141 D3 (4)).
def push_permission_refusals(job_id: str | None) -> list[str]:
    """``[reason]`` when the push action is denied for JOB_ID's pinned level, else ``[]``."""
    try:
        require_permission("push", PermissionRequest(
            level=pinned_job_level(job_id), subject="the push of a remedy do walk", job_id=job_id,
        ))
    except PermissionRefusedError as exc:
        return [exc.reason]
    return []


# WHY: one grant per repository the walk pushes, naming the flag or key that let it through
# (DECISION F141 D3 (4)).
def grant_push_permission(job_id: str | None, approval_ref: str) -> str:
    """``""`` once the push is granted (an `ask` cell is audited by the check), else the refusal."""
    try:
        require_permission("push", PermissionRequest(
            level=pinned_job_level(job_id), subject="the push of a remedy do walk", job_id=job_id,
            approval=InstanceApproval(APPROVAL_KIND_FLAG, approval_ref),
        ))
    except PermissionRefusedError as exc:
        return exc.reason
    return ""

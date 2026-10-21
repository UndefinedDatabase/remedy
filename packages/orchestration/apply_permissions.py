"""The apply's own questions to the permission matrix, asked through the refusals
``job_apply`` already has: one `write_worktree`, an optional `commit` and an optional `push`
for one apply instance, and one `push` for `remedy do`'s mission-level push (DECISION F141 D3).
`is_dependency_manifest` and `is_migration_path` find an optional `dependency_change` and
`destructive`, each asked through a decision on the job instead of a flag when its cell is
`ask` (DECISION F141 D4).
"""
from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.escalation import (
    ESCALATION_STATUS_ANSWERED,
    ESCALATION_STATUS_OPEN,
    enqueue_task_decision,
    escalation_records,
    task_decision_answer_command,
)
from packages.orchestration.permission_matrix import (
    APPROVAL_KIND_DECISION,
    APPROVAL_KIND_FLAG,
    PERMISSION_ACTIONS,
    PERMISSION_ASK,
    InstanceApproval,
    PermissionRefusedError,
    PermissionRequest,
    permission_cell,
    pinned_job_level,
    require_permission,
    require_permissions,
)

# WHY: the prefix of a refused `write_worktree`, the one apply action none of job_apply's own
# refusal prefixes already names (DECISION F141 D3 (1)); a refused `dependency_change` or
# `destructive` takes it too (DECISION F141 D4 (2)).
WRITE_PERMISSION_REFUSED = "permission_refused"

# WHY: the nineteen file names DECISION F141 D4 (1) names as declaring or locking a project's
# dependencies, read by `is_dependency_manifest`; `_MANIFEST_NAMES` in context_inspector.py
# answers a different question (what a context prioritises) and is left alone.
DEPENDENCY_MANIFEST_NAMES: frozenset[str] = frozenset({
    "package.json", "package-lock.json", "npm-shrinkwrap.json", "yarn.lock",
    "pnpm-lock.yaml", "pyproject.toml", "poetry.lock", "uv.lock", "Pipfile",
    "Pipfile.lock", "setup.py", "setup.cfg", "requirements.txt", "Cargo.toml",
    "Cargo.lock", "go.mod", "go.sum", "Gemfile", "Gemfile.lock",
})


# WHY: a `dependency_change` is a planned path whose own file name is one of the nineteen, or
# any `requirements*.txt` (DECISION F141 D4 (1)).
def is_dependency_manifest(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    return name in DEPENDENCY_MANIFEST_NAMES or (
        name.startswith("requirements") and name.endswith(".txt"))


# WHY: where a migration tool's own files live; they are found by folder, never by file name,
# because a migration tool names its files by timestamp or sequence (DECISION F141 D4 (1)).
MIGRATIONS_FOLDER = "migrations"


# WHY: a `destructive` apply's migration paths are a folder match, not a file-name match
# (DECISION F141 D4 (1)).
def is_migration_path(path: str) -> bool:
    return MIGRATIONS_FOLDER in path.split("/")[:-1]


# WHY: the one task id every DECISION F141 D4 (2) decision is enqueued under, and its two
# answers — no flag of `remedy job apply` names `dependency_change` or `destructive`.
PERMISSION_DECISION_TASK_ID = "apply"
PERMISSION_APPROVE = "approve"
PERMISSION_DECLINE = "decline"


def _decision_question(action: str, request: PermissionRequest, paths: list[str]) -> str:
    """The sentence a `dependency_change` or `destructive` decision asks and cross-checks
    against (DECISION F141 D4 (2)): the matrix's own reason for the asked cell, then the
    paths that made it so."""
    verdict = require_permission(action, request)
    return f"{verdict.reason} The paths: {', '.join(paths)}."


def _last_decision(job: Any, question: str) -> dict[str, Any] | None:
    """The LAST of the job's decisions asking exactly QUESTION under the apply's task id, or
    None (DECISION F141 D4 (2))."""
    matches = [r for r in escalation_records(job)
              if r.get("task_id") == PERMISSION_DECISION_TASK_ID and r.get("question") == question]
    return matches[-1] if matches else None


def _discovered_actions(
    job: Any, result: Any, planned: Sequence[str],
) -> tuple[list[str], list[str], list[str]]:
    """``(actions, dependency_paths, destructive_paths)`` this apply instance asks about
    (DECISION F141 D4 (1)): the flag actions, then `dependency_change` and `destructive`
    when `planned` or, in mode `history`, the real job branch's own deletions name one."""
    from packages.orchestration.job_apply import COMMIT_MODE_FLAGS, _history_git

    mode = result.commit_message_mode
    actions: list[str] = ["write_worktree"]
    if mode in COMMIT_MODE_FLAGS:
        actions.append("commit")
    if result.push:
        actions.append("push")

    dependency_paths = sorted({p for p in planned if is_dependency_manifest(p)})
    if dependency_paths:
        actions.append("dependency_change")

    destructive_paths = sorted({p for p in planned if is_migration_path(p)})
    if mode == "history":
        target_repo = getattr(result, "target_repo", "") or ""
        if target_repo:
            branch = getattr(job, "worktree_branch", "") or ""
            rc, out, _err = _history_git(
                Path(target_repo), "diff", "--name-only", "--diff-filter=D", "-z",
                f"HEAD...refs/heads/{branch}",
            )
            if rc == 0:
                destructive_paths = sorted(
                    set(destructive_paths) | {p for p in out.split("\x00") if p})
    if destructive_paths:
        actions.append("destructive")
    return actions, dependency_paths, destructive_paths


def _decision_outcome(
    job: Any, result: Any, request: PermissionRequest, action: str, paths: list[str],
) -> tuple[str, InstanceApproval | None]:
    """``(refusal, approval)`` of one `dependency_change` or `destructive` instance whose
    cell is `ask`; both ``("", None)`` when PATHS is empty or the cell is not `ask`
    (DECISION F141 D4 (2))."""
    if not paths or permission_cell(action, request.level, push_allowed=True) != PERMISSION_ASK:
        return "", None
    question = _decision_question(action, request, paths)
    record = _last_decision(job, question)
    if record is not None and record.get("status") == ESCALATION_STATUS_ANSWERED:
        answer = str(record.get("answer") or "")
        decision_id = str(record.get("decision_id") or "")
        if answer == PERMISSION_APPROVE:
            return "", InstanceApproval(APPROVAL_KIND_DECISION, decision_id)
        return (f"{WRITE_PERMISSION_REFUSED}: {question} You answered decision "
                f"{decision_id} with {answer}, so this apply stays refused."), None
    if record is not None and record.get("status") == ESCALATION_STATUS_OPEN:
        decision_id = str(record.get("decision_id") or "")
        command = task_decision_answer_command(str(job.job_id), decision_id, PERMISSION_APPROVE)
        return (f"{WRITE_PERMISSION_REFUSED}: {question} Decision {decision_id} waits for "
                f"your answer: {command}"), None
    if getattr(result, "approved", False) and not getattr(result, "dry_run", False):
        from packages.orchestration.pingpong_job import save_job_plan

        new_record = enqueue_task_decision(
            job, task_id=PERMISSION_DECISION_TASK_ID, question=question,
            options=[PERMISSION_APPROVE, PERMISSION_DECLINE],
            safe_default=PERMISSION_DECLINE,
            impact="Approving lets this one apply go ahead; declining keeps it refused.",
            now=datetime.now(timezone.utc),
        )
        save_job_plan(job)
        decision_id = str(new_record.get("decision_id") or "")
        command = task_decision_answer_command(str(job.job_id), decision_id, PERMISSION_APPROVE)
        return (f"{WRITE_PERMISSION_REFUSED}: {question} Decision {decision_id} waits for "
                f"your answer: {command}"), None
    return (f"{WRITE_PERMISSION_REFUSED}: {question} An approved apply asks you "
            f"through a decision."), None


# WHY: checked before anything is written AND again right before anything is written, so a
# denied action still stops the apply and an asked one is granted once per instance, never a
# standing widening of the matrix (DECISION F141 D3 (1)); `dependency_change` and `destructive`
# grant through a decision on the job instead, never a flag (DECISION F141 D4 (2)).
def apply_permission_refusals(
    job: Any, result: Any, planned: Sequence[str], refused: Sequence[str],
) -> list[str]:
    """Every prefixed refusal of this apply's `write_worktree`, `commit`, `push`,
    `dependency_change` and `destructive`; reads only before ``result.status`` is
    ``approved_apply_started``, then grants each approved action once.

    ``planned`` is read for a dependency manifest or a migration path among it;
    ``refused`` is every refusal `_flag_refusals` already found (its caller still carries
    it, so this never answers it again), and (DECISION F141 D4 (3)) its presence alone
    records no grant at all, with or without a refusal of this function's own.
    """
    from packages.orchestration.job_apply import COMMIT_MODE_FLAGS, COMMIT_REFUSED, HISTORY_REFUSED, PUSH_REFUSED

    mode = result.commit_message_mode
    actions, dependency_paths, destructive_paths = _discovered_actions(job, result, planned)
    request = PermissionRequest(
        level=pinned_job_level(str(job.job_id)),
        subject=f"the apply of job {job.job_id}", job_id=str(job.job_id),
    )

    # (a) the deny walk, unchanged: a deny among every action this instance discovered
    # refuses first, a `dependency_change` or `destructive` denial taking WRITE_PERMISSION_REFUSED.
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

    # (b) `dependency_change` and `destructive` ask through a decision on the job, never a flag.
    decision_refusals: dict[str, str] = {}
    decision_approvals: dict[str, InstanceApproval] = {}
    for action, paths in (("dependency_change", dependency_paths), ("destructive", destructive_paths)):
        refusal, approval = _decision_outcome(job, result, request, action, paths)
        if refusal:
            decision_refusals[action] = refusal
        if approval is not None:
            decision_approvals[action] = approval

    # (c) the caller's own refusals, or either of these: answer (a) and (b)'s own — never
    # `refused` again, the caller already carries it — and record no grant either way.
    ordered = [decision_refusals[action] for action in PERMISSION_ACTIONS
              if action in decision_refusals]
    if refused or ordered:
        return ordered

    # (d) nothing refused: at the late call, grant every discovered action once.
    if result.status != "approved_apply_started":
        return []
    for action in actions:
        if action == "write_worktree":
            approval = InstanceApproval(APPROVAL_KIND_FLAG, "--approve")
        elif action == "commit":
            approval = InstanceApproval(APPROVAL_KIND_FLAG, COMMIT_MODE_FLAGS[mode])
        elif action == "push":
            approval = InstanceApproval(APPROVAL_KIND_FLAG, "--push")
        else:
            approval = decision_approvals.get(action)
        require_permission(action, PermissionRequest(
            level=request.level, subject=request.subject, job_id=request.job_id,
            approval=approval,
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

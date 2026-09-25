"""F026 T001 — edit one task of an approved plan while the job is not running (DECISION F026 D1).

The edit is the plan editor's own ``plan_edit_task``: a runtime edit applies exactly the
transaction ``packages/orchestration/plan_editing.py`` already runs before approval,
``apply_edit(plan, "plan_edit_task", {"task_id": <planned id>, "fields": fields})``, so the
editable fields are exactly ``EDITABLE_TASK_FIELDS``, ``revalidate`` refuses exactly what it
refuses before approval, and ``replay_edits`` still reconstructs the plan from the SAME
``_edits`` log the pre-approval editor writes to.

It is refused while the job runs because the run process holds the whole record in memory and
saves it as one object: an edit accepted while a run holds the record would be overwritten at
the run's next save, silently lost rather than refused, which is worse than refusing it up
front and telling the operator to pause first (DECISION F025 D1's pause is that "first").
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.common.secure_fs import durable_write_json
from packages.core.models import RunState
from packages.orchestration import pause_control, safe_points
from packages.orchestration.data_paths import job_dod_path, job_evidence_export_dir
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    map_task_plan_to_tasks,
    plan_content_hash,
    write_plan_md,
)
from packages.orchestration.mission_compiler import PLAN_VERSION_KEY
from packages.orchestration.pingpong_job import (
    TASK_BLOCKED,
    TASK_FAILED,
    TASK_PENDING,
    TASK_SKIPPED,
    require_job_plan,
    save_job_plan,
)
from packages.orchestration.plan_editing import (
    EDIT_LOG_EVIDENCE,
    EDIT_LOG_KEY,
    EDIT_LOG_SCHEMA_V,
    PlanEditRefused,
    apply_edit,
    plan_edit_lock,
    plan_version,
)
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables

__all__ = [
    "RUNTIME_EDITABLE_STATES",
    "TaskEditResult",
    "runtime_edit_state",
    "edit_task_at_runtime",
    "task_spec_versions",
]

#: The three states a runtime edit may find a task in. Every other task status is refused.
RUNTIME_EDITABLE_STATES: tuple[str, str, str] = ("waiting", "paused", "failed")

#: A planned id safe to use as a filename component; anything else is archived under its digest.
_PLANNED_ID_SAFE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")

_TASK_SPECS_DIRNAME = "task_specs"


def _value(state: Any) -> str:
    """The string value of a ``RunState`` or a plain string, uniformly."""
    return state.value if isinstance(state, RunState) else str(state)


def _model_body(body: dict[str, Any]) -> dict[str, Any]:
    # Mirrors `plan_editing._model_body`: the persisted body carries `_approval`,
    # `_normalization` and this module's own bookkeeping beside the model's own fields,
    # and the model forbids extras. Not imported (S2): plan_editing.py's private helper
    # is not one of the seven names this module is allowed to take from it.
    return {k: v for k, v in body.items() if not k.startswith("_")}


def runtime_edit_state(job_state: Any, approval: Any, task_status: Any, *,
                       task_paused: bool) -> str:
    """One of ``RUNTIME_EDITABLE_STATES``, or raise ``PlanEditRefused``. Pure: no I/O.

    In order: a running or terminal job refuses ``job_not_editable``; an approval of
    ``pending`` (the plan editor's own window, not this one) or ``rejected`` refuses
    ``plan_not_editable``; a pending task is ``paused`` when *task_paused* else ``waiting``;
    a ``failed`` or ``blocked`` task is ``failed``; every other task status refuses
    ``task_not_editable``.
    """
    job_value = _value(job_state)
    if job_value == RunState.RUNNING.value:
        raise PlanEditRefused("job_not_editable", f"the job is {job_value}")
    if job_value in (RunState.COMPLETED.value, RunState.FAILED.value, RunState.CANCELLED.value):
        raise PlanEditRefused("job_not_editable", f"the job is {job_value}")

    approval_value = _value(approval) if approval is not None else ""
    if approval_value in ("pending", "rejected"):
        raise PlanEditRefused("plan_not_editable", f"the plan is {approval_value}")

    status_value = _value(task_status)
    if status_value == TASK_PENDING:
        return "paused" if task_paused else "waiting"
    if status_value in (TASK_FAILED, TASK_BLOCKED):
        return "failed"
    raise PlanEditRefused("task_not_editable", f"the task is {status_value}")


@dataclass(frozen=True)
class TaskEditResult:
    """An accepted runtime edit: what it applied, and where it is recorded."""

    job_id: str
    task_id: str
    planned_id: str
    state: str
    spec_version: int
    plan_version: int
    entry: dict[str, Any]
    archive_path: Path
    restored: tuple[str, ...]


def _archive_stem(planned_id: str) -> str:
    if _PLANNED_ID_SAFE_RE.match(planned_id):
        return planned_id
    return hashlib.sha256(planned_id.encode("utf-8")).hexdigest()[:32]


def _create_only_write(path: Path, data: bytes) -> bool:
    """Publish *data* at *path* only if it does not already exist.

    True on success. False, having written nothing, when a file is already there — the
    caller owns the conflict, exactly as ``secure_fs.write_file_atomically(create_only=True)``
    does for a held directory fd. This is the path-based equivalent for an evidence
    directory that (unlike the control area) carries no symlink-hardened fd chain.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / f".{path.name}.{os.getpid()}.{secrets.token_hex(8)}.tmp"
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)
    try:
        os.link(str(tmp), str(path))
        return True
    except FileExistsError:
        return False
    finally:
        tmp.unlink(missing_ok=True)


def _archive_prior_spec(job_id: str, root: Path | None, planned_id: str, plan_task: Any,
                        entry: Any, state: str, spec_version_before: int) -> Path:
    """S5: archive the task's prior spec, create-only. Raises ``spec_archive_conflict``."""
    directory = job_evidence_export_dir(job_id, root) / _TASK_SPECS_DIRNAME
    stem = _archive_stem(planned_id)
    path = directory / f"{stem}.v{spec_version_before}.json"
    payload = {
        "plan_task": plan_task.model_dump(),
        "title": entry.title,
        "acceptance": entry.acceptance,
        "task_id": entry.task_id,
        "planned_id": planned_id,
        "spec_version": spec_version_before,
        "state": state,
        "archived_at": datetime.now(timezone.utc).isoformat(),
    }
    data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if _create_only_write(path, data):
        return path
    existing = json.loads(path.read_text(encoding="utf-8"))
    new = json.loads(data)
    existing_cmp = {k: v for k, v in existing.items() if k != "archived_at"}
    new_cmp = {k: v for k, v in new.items() if k != "archived_at"}
    if existing_cmp != new_cmp:
        raise PlanEditRefused(
            "spec_archive_conflict",
            f"an archived spec already exists at {path} with different content")
    return path


def edit_task_at_runtime(
    job_id: str,
    task_id: str,
    fields: dict[str, Any],
    *,
    expected_spec_version: int,
    actor: str,
    root: Path | None = None,
) -> TaskEditResult:
    """Edit one task of job *job_id*'s stored, approved plan, at runtime, as one transaction.

    *task_id* is the ``TaskEntry``'s own id — the one a task pause file is keyed by, not the
    plan's own task id. Under ``plan_edit_lock``: load the record, find the entry and its
    planned id, gate the job/plan/task state (S3), check *expected_spec_version* against the
    entry's own, apply the plan editor's ``plan_edit_task``, archive the prior spec, update the
    entry in place, reset a failed task (and the tasks its block skipped) to pending, reseal the
    approval hash when one was recorded, and write the record once. A refusal of any kind — the
    state gate, a version conflict, revalidation or an archive conflict — leaves the record's
    bytes, the evidence export directory and the archive untouched.
    """
    with plan_edit_lock(job_id, root):
        job = require_job_plan(job_id, root)
        body = job.task_plan
        if not isinstance(body, dict) or not body.get("tasks"):
            raise PlanEditRefused("no_task_plan", f"job {job_id} has no task plan to edit")

        idx = next((i for i, t in enumerate(job.tasks) if t.task_id == task_id), None)
        if idx is None:
            raise PlanEditRefused("unknown_task", f"job {job_id} has no task {task_id!r}")
        entry = job.tasks[idx]

        plan_info = entry.inputs.get("plan")
        if not isinstance(plan_info, dict) or not plan_info.get("planned_id"):
            raise PlanEditRefused(
                "not_a_plan_task",
                f"task {task_id!r} was not mapped from the stored plan and carries no "
                "planned id")
        planned_id = plan_info["planned_id"]

        plan = TaskPlan.model_validate(_model_body(body))
        if not any(t.id == planned_id for t in plan.tasks):
            raise PlanEditRefused("unknown_task", f"the stored plan has no task {planned_id!r}")

        task_paused = _value(job.state) == "paused"
        if _value(entry.status) == TASK_PENDING:
            paused_ids = {
                p.task_id for p in pause_control.paused_tasks(
                    job_id, control_root_path=safe_points.control_root(root))
            }
            task_paused = task_paused or task_id in paused_ids

        state = runtime_edit_state(
            job.state, body.get("_approval"), entry.status, task_paused=task_paused)

        spec_version_before = entry.spec_version
        if expected_spec_version != spec_version_before:
            raise PlanEditRefused(
                "version_conflict",
                f"the edit was made against spec version {expected_spec_version}; task "
                f"{task_id!r} is at spec version {spec_version_before}",
                current_version=spec_version_before)

        args = {"task_id": planned_id, "fields": fields}
        try:
            new_plan = apply_edit(plan, "plan_edit_task", args)
        except PlanEditRefused as exc:
            exc.current_version = spec_version_before
            raise

        # S5: the archive is written after the edit validated and before the record is
        # written — a refused edit above never reaches here, and nothing below this point
        # runs unless the archive itself succeeds or finds an equal prior write.
        plan_task = next(t for t in plan.tasks if t.id == planned_id)
        archive_path = _archive_prior_spec(
            job_id, root, planned_id, plan_task, entry, state, spec_version_before)

        mapped = map_task_plan_to_tasks(new_plan)
        record_llm_task_deliverables(mapped)
        fresh = next(
            t for t in mapped if (t.inputs.get("plan") or {}).get("planned_id") == planned_id)

        status_before = _value(entry.status)
        approved_before = body.get(APPROVED_PLAN_HASH_KEY)
        acceptance_before = entry.acceptance

        # S6: THE ENTRY IS UPDATED IN PLACE — only what the mapping wrote for this task.
        entry.title = fresh.title
        entry.acceptance = fresh.acceptance
        entry.inputs["plan"] = fresh.inputs["plan"]
        if "deliverable" in fresh.inputs:
            entry.inputs["deliverable"] = fresh.inputs["deliverable"]
        entry.spec_version = spec_version_before + 1

        # S7: THE RESET — a failed task (its status was `failed` or `blocked`) goes back to
        # pending with its error cleared, and every `skipped` task after it in plan order —
        # `_block_job`'s own skip — is restored with it.
        restored: list[str] = []
        if state == "failed":
            entry.status = TASK_PENDING
            entry.error = ""
            for later in job.tasks[idx + 1:]:
                if _value(later.status) == TASK_SKIPPED:
                    later.status = TASK_PENDING
                    restored.append(later.task_id)
        status_after = _value(entry.status)

        version = plan_version(body)
        log_entry: dict[str, Any] = {
            "version": version + 1,
            "ts": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "command": "plan_edit_task",
            "args": args,
            "before": [t.model_dump() for t in plan.tasks],
            "after": [t.model_dump() for t in new_plan.tasks],
        }

        new_body = new_plan.model_dump()
        new_body.update({k: v for k, v in body.items() if k.startswith("_")})
        new_body[PLAN_VERSION_KEY] = version + 1

        # S6: THE APPROVAL SEAL FOLLOWS THE EDIT.
        approved_after = approved_before
        if body.get("_approval") == "approved" and approved_before:
            approved_after = plan_content_hash(new_body)
            new_body[APPROVED_PLAN_HASH_KEY] = approved_after

        evidence_dir = job_evidence_export_dir(job_id, root)
        try:
            archive_rel = str(archive_path.relative_to(evidence_dir))
        except ValueError:
            archive_rel = str(archive_path)

        # R-1062 / T5_F026.md "Edge cases & assumption defaults": editing acceptance
        # after a DoD was already compiled leaves that DoD's traceability rule stale
        # until the next compile re-syncs it, so the edit log notes the pending
        # re-sync instead of staying silent about the drift. R-1063 S2: the flag
        # reads whether the acceptance VALUE actually changed, not merely that
        # "acceptance" named a field in the edit — an edit that passes an unchanged
        # acceptance beside another changed field must read false.
        has_stored_dod = job_dod_path(job_id, root).is_file()
        dod_resync_pending = entry.acceptance != acceptance_before and has_stored_dod

        log_entry["runtime"] = {
            "task_id": task_id,
            "planned_id": planned_id,
            "state": state,
            "spec_version": entry.spec_version,
            "status_before": status_before,
            "status_after": status_after,
            "restored": list(restored),
            "approved_plan_sha256_before": approved_before,
            "approved_plan_sha256_after": approved_after,
            "archive": archive_rel,
            "dod_resync_pending": dod_resync_pending,
        }

        new_body[EDIT_LOG_KEY] = [*body.get(EDIT_LOG_KEY, []), log_entry]
        job.task_plan = new_body
        save_job_plan(job, root)

    # S8: AFTER THE WRITE, outside the lock, as `edit_plan` does.
    evidence_dir = job_evidence_export_dir(job_id, root)
    write_plan_md(new_plan, evidence_dir, version=version + 1,
                 transformations=body.get("_normalization"), edits=new_body[EDIT_LOG_KEY])
    durable_write_json(evidence_dir / EDIT_LOG_EVIDENCE, {
        "schema_v": EDIT_LOG_SCHEMA_V,
        "job_id": job_id,
        "version": version + 1,
        "edits": new_body[EDIT_LOG_KEY],
    })

    return TaskEditResult(
        job_id=job_id,
        task_id=task_id,
        planned_id=planned_id,
        state=state,
        spec_version=entry.spec_version,
        plan_version=version + 1,
        entry=log_entry,
        archive_path=archive_path,
        restored=tuple(restored),
    )


def task_spec_versions(job_id: str, planned_id: str, *,
                       root: Path | None = None) -> tuple[dict, ...]:
    """Every archived spec of *planned_id*, parsed, in ascending version order.

    Empty when none exists — a task never edited at runtime has archived nothing.
    """
    directory = job_evidence_export_dir(job_id, root) / _TASK_SPECS_DIRNAME
    stem = _archive_stem(planned_id)
    prefix = f"{stem}.v"
    out: list[dict[str, Any]] = []
    if directory.is_dir():
        for path in sorted(directory.iterdir()):
            if path.name.startswith(prefix) and path.name.endswith(".json"):
                out.append(json.loads(path.read_text(encoding="utf-8")))
    out.sort(key=lambda d: d.get("spec_version", 0))
    return tuple(out)

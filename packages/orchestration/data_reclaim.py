"""Reclaiming the data root's ephemeral scratch, preview first (F276 T002).

``plan_reclaim(root)`` computes what could be freed and DELETES NOTHING;
``apply_reclaim(plan)`` deletes exactly the paths that plan holds, re-checking
every safety rule at the moment of deletion rather than trusting the plan it was
handed. The split exists so the reclaim command can print a preview an operator
reads before anything is removed, and so the preview and the deletion cannot
disagree about which paths are meant: there is one computation of the set.

THE RULES, and every one of them is a REFUSAL rather than a silent skip, because a
path this command declines to delete is exactly the path an operator needs to see:

- Only a DIRECT CHILD of an EPHEMERAL class directory is ever a candidate. A
  durable class, an unclassified top-level child, the class directory itself and
  anything nested deeper are never deleted. Durable and unclassified children are
  REPORTED with their bytes, under a heading that says they are not reclaimed.
- Under DECISION F276 D3 that leaves ONE class with candidates: ``job_workspaces``,
  whose children are the ``staging_<job>`` copies the non-git isolation path makes.
  ``workspaces``, ``runs`` and ``job_logs`` are DURABLE — each mixes scratch with
  evidence that outlives its job, and reclaim's safety comes from addressing whole
  direct children rather than reaching inside one. That is 99.98 % of the ephemeral
  bytes on the operator's measured root, so the narrowing costs almost nothing.
- A candidate's job must resolve to a record in the job store AND be terminal
  (``pingpong_job.JOB_TERMINAL_STATES``). A job that is still runnable — planned,
  running, paused, blocked, stopped — keeps its scratch, because `remedy job
  resume` will want it.
- A child that is a SYMLINK, or whose real path leaves the data root, is refused.
  Deletion therefore never follows a link out of the tree.
- ``review_staging.*`` is ephemeral but is not a class DIRECTORY with children: the
  top-level entry IS the scratch, and no job owns it. It is refused as
  ``class_not_job_keyed`` and reported, never deleted, until a later slice gives it
  an owner.

Public API::

    plan_reclaim(root, *, now=None) -> ReclaimPlan
    apply_reclaim(plan) -> ReclaimOutcome
    export_reclaim_json(plan, outcome=None) -> dict
    REFUSAL_REASONS
"""

from __future__ import annotations

import os
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.data_footprint import child_usage
from packages.orchestration.data_paths import (
    EPHEMERAL_CLASSES,
    classify_data_child,
    data_class_dir,
)

#: Every reason this command declines a path, in report order. A refusal is part of
#: the output contract, so the reasons are named here rather than spelled at the
#: sites that raise them.
REFUSAL_REASONS: tuple[str, ...] = (
    "job_not_terminal",
    "job_unresolved",
    "class_not_job_keyed",
    "not_a_direct_child",
    "symlink",
    "outside_data_root",
    "delete_failed",
)

#: The ephemeral classes whose direct children are keyed by a JOB id, and the name
#: prefix that precedes the id. Exactly one entry under DECISION F276 D3: `workspaces`,
#: `runs` and `job_logs` are DURABLE, so no job-id derivation for them exists here —
#: `runs` in particular never needed one at this layer, since a run id contains no job
#: id and the mapping lived in that run's own ``result.json``.
_JOB_KEYED_PREFIXES: dict[str, str] = {
    "job_workspaces": "staging_",
}


@dataclass(frozen=True)
class ReclaimCandidate:
    """One direct child of an ephemeral class directory that ``--apply`` would remove."""

    data_class: str
    name: str
    path: str
    job_id: str
    job_state: str
    age_days: float
    bytes: int
    files: int


@dataclass(frozen=True)
class ReclaimRefusal:
    """One path this command declines to delete, and why."""

    data_class: str
    name: str
    path: str
    reason: str
    detail: str
    bytes: int
    files: int


@dataclass(frozen=True)
class UnreclaimedChild:
    """One top-level child reclaim never addresses: durable, or in no class at all."""

    name: str
    data_class: str
    bytes: int
    files: int


@dataclass(frozen=True)
class ReclaimPlan:
    """What ``--apply`` would remove, what it refuses, and what it never addresses."""

    root: str
    exists: bool
    candidates: tuple[ReclaimCandidate, ...]
    refusals: tuple[ReclaimRefusal, ...]
    unreclaimed: tuple[UnreclaimedChild, ...]

    @property
    def total_bytes(self) -> int:
        return sum(c.bytes for c in self.candidates)

    @property
    def total_files(self) -> int:
        return sum(c.files for c in self.candidates)


@dataclass(frozen=True)
class ReclaimOutcome:
    """What ``apply_reclaim`` removed, and what it refused at the moment of deletion."""

    removed: tuple[str, ...]
    freed_bytes: int
    refusals: tuple[ReclaimRefusal, ...]

    @property
    def had_failure(self) -> bool:
        """True when a deletion was ATTEMPTED and failed — the only loud refusal.

        DECISION F276 D3 (e): every other reason is a refusal the operator asked for
        by running a guarded command, and exits 0. ``delete_failed`` means the command
        tried to free a path it had cleared and could not, so the process exits 1.
        """
        return any(r.reason == "delete_failed" for r in self.refusals)


#: The ephemeral classes that ARE directories whose children reclaim judges. The
#: prefix classes are excluded: ``review_staging.XXXXXX`` is itself the scratch.
def _class_dir_names() -> set[str]:
    return {c.name for c in EPHEMERAL_CLASSES if not c.prefix}


def _job_id_for(data_class: str, name: str) -> str:
    """The job id one direct child NAMES, or ``""`` when its name yields none.

    Every job-keyed ephemeral class carries the id in the child's own name, so this
    reads no file. It is the whole reason reclaim can decide a candidate from a
    listing plus one job record.
    """
    prefix = _JOB_KEYED_PREFIXES[data_class]
    if prefix and not name.startswith(prefix):
        return ""
    return name[len(prefix):]


def _job_state(job_id: str, root: Path) -> tuple[str, str]:
    """``(state, refusal_reason)`` for one job id; the reason is ``""`` when terminal."""
    from packages.orchestration.pingpong_job import job_is_terminal, load_job_plan_safe

    plan, _degraded = load_job_plan_safe(job_id, root)
    if plan is None:
        return ("", "job_unresolved")
    state = str(getattr(plan.state, "value", plan.state))
    if not job_is_terminal(plan.state):
        return (state, "job_not_terminal")
    return (state, "")


def _inside(path: str, root: Path) -> bool:
    """True when ``path``'s REAL path is strictly inside ``root``'s real path."""
    real = os.path.realpath(path)
    real_root = os.path.realpath(os.fspath(root))
    if real == real_root:
        return False
    try:
        return os.path.commonpath([real, real_root]) == real_root
    except ValueError:  # different drives / no common path
        return False


def _age_days(path: str, now: float) -> float:
    try:
        mtime = os.lstat(path).st_mtime
    except OSError:
        return 0.0
    return round(max(0.0, now - mtime) / 86400.0, 1)


def plan_reclaim(root: Path | str, *, now: float | None = None) -> ReclaimPlan:
    """Compute what could be freed under ``root``. Writes nothing, deletes nothing."""
    root_path = Path(root)
    root_str = os.fspath(root_path)
    at = time.time() if now is None else now
    try:
        with os.scandir(root_str) as it:
            top = sorted(it, key=lambda e: e.name)
    except OSError:
        return ReclaimPlan(root=root_str, exists=False, candidates=(),
                           refusals=(), unreclaimed=())

    class_dirs = _class_dir_names()
    candidates: list[ReclaimCandidate] = []
    refusals: list[ReclaimRefusal] = []
    unreclaimed: list[UnreclaimedChild] = []

    for entry in top:
        kind = classify_data_child(entry.name) or "unclassified"
        is_dir = entry.is_dir(follow_symlinks=False)
        if kind == "ephemeral" and entry.name in class_dirs and is_dir:
            _plan_class(entry.name, entry.path, root_path, at, candidates, refusals)
            continue
        size, files = child_usage(entry.path)
        if kind == "ephemeral":
            refusals.append(ReclaimRefusal(
                data_class=entry.name.split(".", 1)[0], name=entry.name, path=entry.path,
                reason="class_not_job_keyed",
                detail="no job owns this path; reclaim addresses job-keyed classes only",
                bytes=size, files=files,
            ))
            continue
        unreclaimed.append(UnreclaimedChild(entry.name, kind, size, files))

    return ReclaimPlan(
        root=root_str,
        exists=True,
        candidates=tuple(candidates),
        refusals=tuple(refusals),
        unreclaimed=tuple(unreclaimed),
    )


def _plan_class(
    data_class: str,
    class_path: str,
    root: Path,
    now: float,
    candidates: list[ReclaimCandidate],
    refusals: list[ReclaimRefusal],
) -> None:
    """Judge every DIRECT child of one ephemeral class directory. Reads only."""
    try:
        with os.scandir(class_path) as it:
            children = sorted(it, key=lambda e: e.name)
    except OSError:
        return

    for child in children:
        size, files = child_usage(child.path)
        reason = detail = ""
        job_id = state = ""
        if os.path.islink(child.path):
            reason, detail = "symlink", "a symlink is never followed and never deleted"
        elif not _inside(child.path, root):
            reason, detail = "outside_data_root", "its real path is not inside the data root"
        else:
            job_id = _job_id_for(data_class, child.name)
            if not job_id:
                reason, detail = "job_unresolved", "no job id can be read from this path"
            else:
                state, reason = _job_state(job_id, root)
                if reason == "job_unresolved":
                    detail = f"no readable job record for {job_id}"
                elif reason:
                    detail = f"job {job_id} is {state}, not terminal"

        if reason:
            refusals.append(ReclaimRefusal(
                data_class=data_class, name=child.name, path=child.path,
                reason=reason, detail=detail, bytes=size, files=files,
            ))
            continue
        candidates.append(ReclaimCandidate(
            data_class=data_class, name=child.name, path=child.path,
            job_id=job_id, job_state=state, age_days=_age_days(child.path, now),
            bytes=size, files=files,
        ))


def _deletion_refusal(path: str, root: Path) -> tuple[str, str]:
    """``(reason, detail)`` for a path apply must not delete; ``("", "")`` to proceed.

    The plan is INPUT, not authority. Every structural rule the planner applied is
    applied again here against the LIVE filesystem, so a plan that was hand-built,
    edited or computed against another root cannot reach a path this command is not
    allowed to touch.
    """
    parent = os.path.dirname(os.path.normpath(path))
    class_name = os.path.basename(parent)
    if class_name not in _class_dir_names():
        return ("not_a_direct_child", f"{class_name!r} is not an ephemeral class directory")
    expected = os.path.normpath(os.fspath(data_class_dir(class_name, root)))
    if os.path.normpath(parent) != expected:
        return ("not_a_direct_child", "not a direct child of this root's class directory")
    if os.path.islink(path):
        return ("symlink", "a symlink is never followed and never deleted")
    if not _inside(path, root):
        return ("outside_data_root", "its real path is not inside the data root")
    return ("", "")


def apply_reclaim(plan: ReclaimPlan) -> ReclaimOutcome:
    """Delete exactly the paths ``plan`` holds, re-checking every rule at deletion.

    A path that is already gone is neither removed nor refused — re-applying a plan
    over a state it has already reclaimed is a no-op, not an error.
    """
    root = Path(plan.root)
    removed: list[str] = []
    refusals: list[ReclaimRefusal] = []
    freed = 0

    for cand in plan.candidates:
        reason, detail = _deletion_refusal(cand.path, root)
        if reason:
            refusals.append(ReclaimRefusal(
                data_class=cand.data_class, name=cand.name, path=cand.path,
                reason=reason, detail=detail, bytes=cand.bytes, files=cand.files,
            ))
            continue
        if not os.path.lexists(cand.path):
            continue
        try:
            if os.path.isdir(cand.path):
                shutil.rmtree(cand.path)
            else:
                os.unlink(cand.path)
        except OSError as exc:
            refusals.append(ReclaimRefusal(
                data_class=cand.data_class, name=cand.name, path=cand.path,
                reason="delete_failed", detail=str(exc), bytes=cand.bytes, files=cand.files,
            ))
            continue
        removed.append(cand.path)
        freed += cand.bytes

    return ReclaimOutcome(removed=tuple(removed), freed_bytes=freed, refusals=tuple(refusals))


def export_reclaim_json(plan: ReclaimPlan, outcome: ReclaimOutcome | None = None) -> dict[str, Any]:
    """The stable machine shape the reclaim command's `--json` prints.

    ``removed`` and ``freed`` are ALWAYS present — empty on a preview — so a reader
    never has to branch on a missing key to learn that nothing was deleted.
    """
    refusals = list(plan.refusals) + list(outcome.refusals if outcome else ())
    return {
        "version": 1,
        "root": plan.root,
        "exists": plan.exists,
        "applied": outcome is not None,
        "candidates": [
            {
                "class": c.data_class, "name": c.name, "path": c.path,
                "job_id": c.job_id, "job_state": c.job_state,
                "age_days": c.age_days, "bytes": c.bytes, "files": c.files,
            }
            for c in plan.candidates
        ],
        "refused": [
            {
                "class": r.data_class, "name": r.name, "path": r.path,
                "reason": r.reason, "detail": r.detail,
                "bytes": r.bytes, "files": r.files,
            }
            for r in refusals
        ],
        "not_reclaimed": [
            {"name": u.name, "class": u.data_class, "bytes": u.bytes, "files": u.files}
            for u in plan.unreclaimed
        ],
        "total": {
            "candidates": len(plan.candidates),
            "bytes": plan.total_bytes,
            "files": plan.total_files,
            "refused": len(refusals),
        },
        "removed": list(outcome.removed) if outcome else [],
        "freed": {
            "bytes": outcome.freed_bytes if outcome else 0,
            "paths": len(outcome.removed) if outcome else 0,
        },
    }

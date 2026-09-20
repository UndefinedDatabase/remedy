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

THE ORPHANS, and the one flag that opts into them. A ``staging_<id>`` child whose job
record is GONE is refused above as ``job_unresolved``, and on a real root that refusal
is where the bytes are. MEASURED 2026-09-20 ON THE OPERATOR'S DATA ROOT with the
command round 2 built: 1107 candidates worth 284 536 286 695 bytes, against 1886
refusals of which 1885 are ``job_unresolved`` worth 638 395 396 948 bytes — and 1884 of
THOSE are ``staging_<16-hex>`` names with no job record on disk at all
(``.data/jobs/<id>`` does not exist and ``job show`` answers "No job matches"). Those
two figures SUM to 922 931 683 643, which is exactly the `job_workspaces` footprint
DECISION F276 D3 measured the same day, so the refused bytes are 69 per cent OF THAT
CLASS'S OWN 922 931 683 643 — the denominator is `job_workspaces`, not the whole data
root. ``--orphans`` opts INTO exactly that case and into nothing else:

- The flag is OFF by default, and with it off this module's output is what it was
  before the rule existed, path for path and byte for byte.
- An orphan is a child whose job record is ABSENT. A record that EXISTS and will not
  parse is never an orphan: ``load_job_plan_safe`` reports that as ``degraded``, and a
  job whose record is corrupt may still be running.
- An orphan must also be at least :data:`ORPHAN_MIN_AGE_DAYS` old, and one under the
  floor is refused under its OWN reason, ``orphan_too_young``, so the operator sees it
  rather than wondering where it went.
- An orphan candidate reports :data:`ORPHAN_JOB_STATE` as its ``job_state``, which is
  the ONE thing in the machine shape that marks it. Every other rule — direct child,
  no symlink, real path inside the root, and every one of them re-checked at the moment
  of deletion — is unchanged.

THE RULES ARE EXPORTED, not only applied. F276 T003 releases ONE job's staging copy
at the moment that job ends, which is this command narrowed to a single path, so it
calls :func:`child_deletion_refusal` and :func:`job_state_refusal` below instead of
spelling direct-child, symlink, inside-the-root and is-terminal a second time. Both
were private to this module until that caller existed; nothing about what they decide
changed when they were exported.

Public API::

    plan_reclaim(root, *, now=None, orphans=False) -> ReclaimPlan
    apply_reclaim(plan) -> ReclaimOutcome
    export_reclaim_json(plan, outcome=None) -> dict
    child_deletion_refusal(path, root, *, data_class=None) -> (reason, detail)
    job_state_refusal(job_id, root) -> (state, reason, record_exists)
    REFUSAL_REASONS / ORPHAN_MIN_AGE_DAYS / ORPHAN_JOB_STATE
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
from packages.orchestration.staging_workspace import STAGING_DIR_PREFIX

#: Every reason this command declines a path, in report order. A refusal is part of
#: the output contract, so the reasons are named here rather than spelled at the
#: sites that raise them.
REFUSAL_REASONS: tuple[str, ...] = (
    "job_not_terminal",
    "job_unresolved",
    "orphan_too_young",
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
#: The prefix is IMPORTED from the module that makes the name rather than re-spelled:
#: ``staging_workspace.create_staging_workspace`` names the directory and this command
#: reads the name, so one constant means they cannot drift apart.
_JOB_KEYED_PREFIXES: dict[str, str] = {
    "job_workspaces": STAGING_DIR_PREFIX,
}

#: How old an orphan must be before ``orphans=True`` will make it a candidate, in days.
#: WHY A FLOOR EXISTS AT ALL: "this job has no record" is read from the filesystem, and
#: a job whose record is BEING WRITTEN right now is indistinguishable, on disk, from a
#: job whose record is gone forever — ``pingpong_job._create_job_workspace_copy`` makes
#: the staging directory and the record is persisted around it, so the window is short
#: but real. WHY 1.0: the window is seconds, a day is four orders of magnitude wider
#: than it, and the orphans this rule was written for are months old, so the floor
#: costs the operator nothing and buys back the only case that could lose live work.
#: WHY THE CHILD'S OWN `lstat` MTIME AND NOT THE NEWEST MTIME IN ITS SUBTREE: the state
#: this floor insures against is a staging directory CREATED while its record is still
#: being written, and a directory that was just created has a fresh mtime OF ITS OWN.
#: A subtree walk would answer a different question — "when was anything in here last
#: touched" — which is not the question the floor asks.
ORPHAN_MIN_AGE_DAYS: float = 1.0

#: The ``job_state`` an ORPHAN candidate reports, and the only mark that distinguishes
#: one in the machine shape. NOT ``""``: an empty state is what every REFUSAL carries
#: (see :func:`_job_state`), and no reader can tell an empty string from an absent key.
#: NOT a ``RunState`` value either — no state is spelled ``no_record`` — so it can never
#: collide with a state a real job record holds, and a reader that matches on it
#: exactly is reading a token rather than parsing prose.
ORPHAN_JOB_STATE: str = "no_record"


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


def job_state_refusal(job_id: str, root: Path) -> tuple[str, str, bool]:
    """``(state, refusal_reason, record_exists)`` for one job id.

    The reason is ``""`` when the job is terminal. ``record_exists`` separates the TWO
    ways a job fails to resolve, which is the whole basis of the orphan rule: no record
    on disk is an orphan's signature, while a record that exists and cannot be parsed
    belongs to a job that may still be running and is never an orphan.
    ``load_job_plan_safe``'s ``degraded`` flag is exactly that distinction, and reading
    it here is cheaper and more honest than stat-ing the record a second time.

    PUBLIC because ``staging_workspace.release_staging_workspace`` asks the same
    question about one job at the moment that job ends; see the module docstring.
    """
    from packages.orchestration.pingpong_job import job_is_terminal, load_job_plan_safe

    plan, degraded = load_job_plan_safe(job_id, root)
    if plan is None:
        return ("", "job_unresolved", degraded)
    state = str(getattr(plan.state, "value", plan.state))
    if not job_is_terminal(plan.state):
        return (state, "job_not_terminal", True)
    return (state, "", True)


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


def _age_seconds(path: str, now: float) -> float:
    """Seconds since ``path``'s own mtime; ``lstat``, so a symlink is not followed.

    0.0 when the path cannot be stat-ed, which is the SAFE end for the orphan floor:
    an unreadable age reads as brand new and is refused.
    """
    try:
        mtime = os.lstat(path).st_mtime
    except OSError:
        return 0.0
    return max(0.0, now - mtime)


def _age_days(path: str, now: float) -> float:
    """The REPORTED age, rounded to a tenth of a day for a person to read."""
    return round(_age_seconds(path, now) / 86400.0, 1)


def _orphan_verdict(path: str, now: float) -> tuple[str, str, str]:
    """``(job_state, refusal_reason, detail)`` for a child whose job record is ABSENT.

    Reached only when the caller asked for orphans. An empty reason means CANDIDATE.

    The floor is compared on UNROUNDED seconds while :func:`_age_days` reports a
    rounded figure on purpose: a child 0.96 days old prints as ``1.0d`` and must still
    be refused, because the floor is a real threshold and not a printed one.
    """
    age = _age_seconds(path, now)
    if age >= ORPHAN_MIN_AGE_DAYS * 86400.0:
        return (ORPHAN_JOB_STATE, "", "")
    return ("", "orphan_too_young",
            f"no job record, and {age / 86400.0:.2f}d is under the "
            f"{ORPHAN_MIN_AGE_DAYS:.1f}d orphan floor")


def plan_reclaim(root: Path | str, *, now: float | None = None,
                 orphans: bool = False) -> ReclaimPlan:
    """Compute what could be freed under ``root``. Writes nothing, deletes nothing.

    ``orphans`` OPTS IN to the staging copies whose job record is gone, and to nothing
    else. It defaults to False, and with it False the plan this returns is the plan
    this function returned before the orphan rule existed — same candidates, same
    refusals, same bytes.
    """
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
            _plan_class(entry.name, entry.path, root_path, at, candidates, refusals,
                        orphans)
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
    orphans: bool = False,
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
                state, reason, record_exists = job_state_refusal(job_id, root)
                if reason == "job_unresolved":
                    detail = f"no readable job record for {job_id}"
                    # An ORPHAN, and only when the operator asked for orphans: the name
                    # carried a job id (so the prefix matched and its remainder was not
                    # empty) and no record exists for it. A record that exists and will
                    # not parse keeps the refusal above.
                    if orphans and not record_exists:
                        state, reason, detail = _orphan_verdict(child.path, now)
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


def child_deletion_refusal(path: str, root: Path, *,
                           data_class: str | None = None) -> tuple[str, str]:
    """``(reason, detail)`` for a path apply must not delete; ``("", "")`` to proceed.

    The plan is INPUT, not authority. Every structural rule the planner applied is
    applied again here against the LIVE filesystem, so a plan that was hand-built,
    edited or computed against another root cannot reach a path this command is not
    allowed to touch.

    ``data_class`` narrows the first rule from "some ephemeral class directory" to
    ONE named one. ``apply_reclaim`` passes nothing, because a plan may span classes;
    ``staging_workspace.release_staging_workspace`` names ``job_workspaces``, because
    a lifecycle release that reached any other class would be a defect and should be
    refused rather than performed.
    """
    parent = os.path.dirname(os.path.normpath(path))
    class_name = os.path.basename(parent)
    if class_name not in _class_dir_names():
        return ("not_a_direct_child", f"{class_name!r} is not an ephemeral class directory")
    if data_class is not None and class_name != data_class:
        return ("not_a_direct_child",
                f"{class_name!r} is not the {data_class!r} class directory")
    expected = os.path.normpath(os.fspath(data_class_dir(class_name, root)))
    if os.path.normpath(parent) != expected:
        return ("not_a_direct_child", "not a direct child of this root's class directory")
    if os.path.islink(path):
        return ("symlink", "a symlink is never followed and never deleted")
    if not _inside(path, root):
        return ("outside_data_root", "its real path is not inside the data root")
    return ("", "")


def _orphan_deletion_refusal(cand: ReclaimCandidate, root: Path,
                             now: float) -> tuple[str, str]:
    """``(reason, detail)`` for an ORPHAN at the moment of deletion; ``("", "")`` to go.

    :func:`child_deletion_refusal` re-derives every STRUCTURAL rule because the plan is
    input and not authority. This is the one VERDICT that has to be re-derived too: it
    is what authorises deleting a directory NOTHING points at, so it is the last thing
    that may be taken on trust. The record is read again and the mtime is read again,
    against the live filesystem — a record that appeared since the plan was computed
    refuses as ``job_unresolved``, a floor no longer met refuses as
    ``orphan_too_young``. One file read per orphan, against deleting hundreds of
    gigabytes. An ORDINARY candidate never reaches here and keeps its existing path.
    """
    from packages.orchestration.pingpong_job import load_job_plan_safe

    job_plan, degraded = load_job_plan_safe(cand.job_id, root)
    if job_plan is not None or degraded:
        return ("job_unresolved",
                f"a job record for {cand.job_id} appeared after the plan was computed")
    if _age_seconds(cand.path, now) < ORPHAN_MIN_AGE_DAYS * 86400.0:
        return ("orphan_too_young",
                f"no job record, but it no longer meets the "
                f"{ORPHAN_MIN_AGE_DAYS:.1f}d orphan floor")
    return ("", "")


def apply_reclaim(plan: ReclaimPlan) -> ReclaimOutcome:
    """Delete exactly the paths ``plan`` holds, re-checking every rule at deletion.

    A path that is already gone is neither removed nor refused — re-applying a plan
    over a state it has already reclaimed is a no-op, not an error.

    An ORPHAN candidate — one whose ``job_state`` is :data:`ORPHAN_JOB_STATE` — has its
    VERDICT re-derived here too, not only the structural rules; see
    :func:`_orphan_deletion_refusal`.
    """
    root = Path(plan.root)
    now = time.time()
    removed: list[str] = []
    refusals: list[ReclaimRefusal] = []
    freed = 0

    for cand in plan.candidates:
        reason, detail = child_deletion_refusal(cand.path, root)
        if not reason and cand.job_state == ORPHAN_JOB_STATE:
            reason, detail = _orphan_deletion_refusal(cand, root, now)
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

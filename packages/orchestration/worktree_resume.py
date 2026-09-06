"""Recover an interrupted run's worktree from the real resume path (F006).

A run that dies mid-flight leaves a persisted record whose worktree section still
says ``cleanup_status: active`` (or ``retained``). This module is what
``remedy job resume`` uses to rediscover that worktree, finish the hand-off and
release it.

Hard rules:

* recovery only ever re-opens THIS run's own branch — a mismatch blocks, it never
  creates a replacement branch and never silently falls back to a copied workspace;
* the recorded base commit must really be in the branch's history;
* the deterministic ``result.diff`` is regenerated and re-persisted;
* on success the physical worktree is removed, the result branch is KEPT, the
  cleanup status becomes ``clean`` and the active-worktree state is cleared;
* there is never an automatic merge into the checked-out branch.

This is NOT the F011 kill switch: no stop polling, no checkpoint scheduling, no
queue semantics live here.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration import worktrees as W

#: Persisted cleanup states that mean "a worktree may still be out there".
RECOVERABLE_STATES = frozenset(
    {"active", "retained", "interrupted", "failed", "failed_recoverable",
     # Not recoverable, but never forgotten: every resume must keep reporting it.
     "unrecoverable"}
)


@dataclass
class WorktreeResumeOutcome:
    """What resume did with one run's worktree."""

    run_id: str
    applicable: bool = False
    prepared: bool = False      # worktree locked and verified; NOT yet cleaned
    recovered: bool = False
    blocked: bool = False
    blocked_reason: str = ""
    branch: str = ""
    worktree_path: str = ""
    base_commit: str = ""
    head: str = ""
    result_diff_sha256: str = ""
    result_diff_size_bytes: int = 0
    cleanup_status: str = ""
    branch_kept: bool = False
    notes: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "applicable": self.applicable,
            "prepared": self.prepared,
            "recovered": self.recovered,
            "blocked": self.blocked,
            "blocked_reason": self.blocked_reason,
            "branch": self.branch,
            "worktree_path": self.worktree_path,
            "base_commit": self.base_commit,
            "head": self.head,
            "result_diff_sha256": self.result_diff_sha256,
            "result_diff_size_bytes": self.result_diff_size_bytes,
            "cleanup_status": self.cleanup_status,
            "branch_kept": self.branch_kept,
            "notes": self.notes,
        }


def _run_dir(run_id: str) -> Path:
    from packages.orchestration.data_paths import run_dir
    return run_dir(run_id)


def _update_persisted_run(run_id: str, worktree_patch: dict[str, Any]) -> None:
    """Write the corrected worktree section back into the run's result.json."""
    path = _run_dir(run_id) / "result.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    wt = data.get("worktree")
    if not isinstance(wt, dict):
        wt = {}
    wt.update(worktree_patch)
    data["worktree"] = wt
    try:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass


def _verify_recorded_diff(run_id: str, wt: dict[str, Any]) -> tuple[bool, str]:
    """Is the persisted ``result.diff`` really there, and really the recorded bytes?"""
    import hashlib

    rd = wt.get("result_diff") or {}
    if not rd or not rd.get("path"):
        return False, "no result.diff was ever persisted"
    path = _run_dir(run_id) / str(rd.get("path"))
    if not path.is_file():
        return False, f"recorded result.diff {rd.get('path')!r} is missing"
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != str(rd.get("sha256") or ""):
        return False, "result.diff does not match its recorded sha256"
    if len(data) != rd.get("size_bytes"):
        return False, "result.diff does not match its recorded size"
    return True, ""


def _safe_update_persisted_run(run_id: str, patch: dict[str, Any]) -> str:
    """Persist an update; a persistence failure is reported, never fatal."""
    try:
        _update_persisted_run(run_id, patch)
        return ""
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


def find_recoverable_runs(job_id: str) -> list[dict[str, Any]]:
    """Persisted runs of this job whose worktree may still be live.

    Only persisted metadata is consulted — this is exactly the record Finding 1
    made durable.
    """
    from packages.orchestration.data_paths import runs_dir
    from packages.orchestration.pingpong_loop import load_run

    pp_runs_root = runs_dir()
    if not pp_runs_root.is_dir():
        return []
    out: list[dict[str, Any]] = []
    for entry in sorted(p for p in pp_runs_root.iterdir() if p.is_dir()):
        data = load_run(entry.name)
        if not data or str(data.get("job_id") or "") != str(job_id):
            continue
        wt = data.get("worktree") or {}
        if wt.get("isolation_mode") != "worktree":
            continue
        if str(wt.get("cleanup_status") or "") not in RECOVERABLE_STATES:
            continue
        out.append(data)
    return out


@dataclass
class WorktreeResumeSession:
    """A recovered worktree, LOCKED and still on disk, awaiting continuation.

    Phase 1 (prepare) hands this back. The physical worktree is deliberately kept
    so the continuation can run inside it; only phase 3 (finalize) removes it, and
    only after the continuation actually succeeded.
    """

    run_id: str
    handle: Any
    outcome: WorktreeResumeOutcome

    @property
    def workspace_root(self) -> Path:
        return Path(self.handle.path)


def prepare_worktree_resume(run_id: str) -> tuple[WorktreeResumeSession | None,
                                                  WorktreeResumeOutcome]:
    """Phase 1 — lock and verify the exact recorded worktree. Nothing is removed.

    Returns ``(session, outcome)``. ``session`` is None when there is nothing to
    recover or when recovery is blocked; the outcome then says why. On success the
    worktree is present, locked by this process, its ``result.diff`` is
    regenerated, and ``session.workspace_root`` is where the continuation must run.
    """
    from packages.orchestration.pingpong_loop import load_run

    outcome = WorktreeResumeOutcome(run_id=run_id)
    data = load_run(run_id)
    if not data:
        return None, outcome                # nothing persisted: not applicable

    wt = data.get("worktree") or {}
    if wt.get("isolation_mode") != "worktree":
        return None, outcome                # copy run: no worktree to recover
    if str(wt.get("cleanup_status") or "") not in RECOVERABLE_STATES:
        return None, outcome                # already cleaned

    outcome.applicable = True
    recorded_branch = str(wt.get("branch") or "")
    recorded_path = str(wt.get("path") or "")
    recorded_base = str(wt.get("base_commit") or "")
    repo_path = str(data.get("repo_path") or "")
    outcome.branch = recorded_branch
    outcome.worktree_path = recorded_path
    outcome.base_commit = recorded_base

    def _block(reason: str):
        outcome.blocked = True
        outcome.blocked_reason = reason
        return None, outcome

    if not repo_path or not W.is_git_repo(repo_path):
        return _block(f"recorded repository is not a git repository: {repo_path!r}")

    try:
        handle = W.recover(run_id, repo_path)
    except W.WorktreeLockError:
        return _block("worktree lock is held by another process (run still active)")
    except W.WorktreeError as exc:
        return _block(f"worktree recovery failed: {exc}")
    except Exception as exc:      # recovery released its lock; block honestly
        return _block(f"worktree recovery failed: {type(exc).__name__}: {exc}")

    if handle is None:
        return _block("no worktree and no result branch left to recover")

    # --- identity checks: the same branch, the same path, the same lineage ----
    if recorded_branch and handle.branch != recorded_branch:
        W.release_lock(handle)
        return _block(
            f"recovered branch {handle.branch!r} does not match recorded "
            f"{recorded_branch!r}"
        )
    if recorded_path and handle.relative_path != recorded_path:
        W.release_lock(handle)
        return _block(
            f"recovered worktree path {handle.relative_path!r} does not match "
            f"recorded {recorded_path!r}"
        )
    root = Path(handle.repo_path)
    if recorded_base and not W.commit_exists(root, recorded_base):
        W.release_lock(handle)
        return _block(f"recorded base commit {recorded_base[:12]} is not in the repository")
    if recorded_base and W._branch_exists(root, handle.branch):
        if not W.is_ancestor(root, recorded_base, handle.branch):
            W.release_lock(handle)
            return _block(
                f"branch {handle.branch!r} did not grow from recorded base "
                f"{recorded_base[:12]}"
            )

    if not Path(handle.path).is_dir():
        # The worktree is gone. That is only an acceptable end state if the
        # branch-plus-diff hand-off is actually COMPLETE — i.e. a result.diff
        # exists and still matches its recorded hash and size. Otherwise the
        # uncommitted work is simply lost, and saying "clean" would hide that.
        W.release_lock(handle)
        outcome.branch_kept = True
        valid, why = _verify_recorded_diff(run_id, wt)
        if valid:
            outcome.cleanup_status = "handoff_complete"
            outcome.blocked = True
            outcome.blocked_reason = (
                "physical worktree is gone; verified result.diff and result branch "
                "remain the hand-off"
            )
            outcome.notes.append("result.diff verified against its recorded hash and size")
            rd = wt.get("result_diff") or {}
            outcome.result_diff_sha256 = str(rd.get("sha256") or "")
            outcome.result_diff_size_bytes = int(rd.get("size_bytes") or 0)
            _update_persisted_run(run_id, {
                "cleanup_status": "handoff_complete",
                "cleanup_error": "",
            })
            return None, outcome

        outcome.cleanup_status = "unrecoverable"
        outcome.blocked = True
        outcome.blocked_reason = (
            f"physical worktree is gone and the hand-off is incomplete: {why}"
        )
        outcome.notes.append("uncommitted work from this run is not recoverable")
        _update_persisted_run(run_id, {
            "cleanup_status": "unrecoverable",       # stays reported on every resume
            "cleanup_error": outcome.blocked_reason,
        })
        return None, outcome

    # Preserve/regenerate the deterministic diff BEFORE the continuation runs, so
    # a continuation that dies still leaves the hand-off on disk.
    try:
        outcome.head = W.snapshot(handle)
        info = W.write_result_diff(handle, _run_dir(run_id) / "result.diff")
    except Exception as exc:
        # Preparing the hand-off failed. Keep the worktree and its uncommitted
        # changes, release the lock, and block: never continue into a workspace
        # whose diff we could not preserve.
        W.retain_for_recovery(handle, f"result.diff not persisted: {exc}")
        _safe_update_persisted_run(run_id, {
            "cleanup_status": "failed_recoverable",
            "result_diff_error": f"{type(exc).__name__}: {exc}",
        })
        return _block(f"could not persist result.diff: {type(exc).__name__}: {exc}")
    outcome.result_diff_sha256 = info["sha256"]
    outcome.result_diff_size_bytes = info["size_bytes"]
    outcome.prepared = True
    outcome.cleanup_status = str(wt.get("cleanup_status") or "")   # still not clean
    outcome.branch_kept = True
    _safe_update_persisted_run(run_id, {
        "head": outcome.head,
        "result_diff": {
            "path": "result.diff",
            "sha256": info["sha256"],
            "size_bytes": info["size_bytes"],
        },
    })
    return WorktreeResumeSession(run_id=run_id, handle=handle, outcome=outcome), outcome


def finalize_worktree_resume(session: WorktreeResumeSession) -> WorktreeResumeOutcome:
    """Phase 3 — the continuation succeeded: regenerate, remove, keep the branch.

    Every step can fail. If it does, the worktree and its uncommitted changes are
    RETAINED, the lock is released, and the run stays recoverable — a half-finished
    finalization must never strand the work behind a held lock.
    """
    outcome = session.outcome
    handle = session.handle
    run_id = session.run_id

    def _retain(reason: str) -> WorktreeResumeOutcome:
        W.retain_for_recovery(handle, reason)
        outcome.recovered = False
        outcome.blocked = True
        outcome.blocked_reason = reason
        outcome.cleanup_status = "failed_recoverable"
        outcome.branch_kept = True
        _safe_update_persisted_run(run_id, {
            "cleanup_status": "failed_recoverable",
            "cleanup_error": reason,
            "result_diff_error": reason,
        })
        return outcome

    try:
        outcome.head = W.snapshot(handle)
        info = W.write_result_diff(handle, _run_dir(run_id) / "result.diff")
    except Exception as exc:
        return _retain(f"final diff not persisted: {type(exc).__name__}: {exc}")

    outcome.result_diff_sha256 = info["sha256"]
    outcome.result_diff_size_bytes = info["size_bytes"]

    # Record the hand-off BEFORE the worktree goes away: if this cannot be
    # persisted, the worktree is the only copy of the work, so it must be kept.
    persist_err = _safe_update_persisted_run(run_id, {
        "head": outcome.head,
        "result_diff": {
            "path": "result.diff",
            "sha256": info["sha256"],
            "size_bytes": info["size_bytes"],
        },
    })
    if persist_err:
        return _retain(f"run record not updated: {persist_err}")

    try:
        res = W.remove(handle, keep_branch=True)          # never a merge
    except Exception as exc:
        return _retain(f"worktree cleanup failed: {type(exc).__name__}: {exc}")

    outcome.cleanup_status = res["cleanup_status"]
    outcome.branch_kept = bool(res["branch_kept"])
    outcome.recovered = res["cleanup_status"] == "clean"
    if not outcome.recovered:
        outcome.blocked = True
        outcome.blocked_reason = res.get("cleanup_error") or "worktree cleanup failed"

    _safe_update_persisted_run(run_id, {
        "head": outcome.head,
        "cleanup_status": outcome.cleanup_status,
        "cleanup_error": res.get("cleanup_error", ""),
        "result_diff": {
            "path": "result.diff",
            "sha256": info["sha256"],
            "size_bytes": info["size_bytes"],
        },
        "recovered_by_resume": True,
    })
    return outcome


def retain_worktree_resume(session: WorktreeResumeSession,
                           reason: str) -> WorktreeResumeOutcome:
    """The continuation failed or raised: keep the worktree, stay resumable.

    The uncommitted changes are the run's only copy — they survive. The lock is
    released so a later ``remedy job resume`` can claim the SAME worktree again.
    Cleanup is never reported clean here.
    """
    outcome = session.outcome
    res = W.retain_for_recovery(session.handle, "")
    outcome.recovered = False
    outcome.cleanup_status = "retained"
    outcome.branch_kept = True
    outcome.notes.append(f"worktree retained for a later resume: {reason}")
    _update_persisted_run(session.run_id, {
        "cleanup_status": "retained",
        "cleanup_error": reason,
    })
    del res
    return outcome


def resume_worktree_run(run_id: str) -> WorktreeResumeOutcome:
    """Prepare + finalize in one step, for callers with no continuation stage."""
    session, outcome = prepare_worktree_resume(run_id)
    if session is None:
        return outcome
    return finalize_worktree_resume(session)


def prepare_job_worktrees(job_id: str) -> list[tuple[Any, WorktreeResumeOutcome]]:
    """Phase 1 for every interrupted worktree recorded for this job."""
    out: list[tuple[Any, WorktreeResumeOutcome]] = []
    for data in find_recoverable_runs(job_id):
        rid = str(data.get("run_id") or "")
        if rid:
            out.append(prepare_worktree_resume(rid))
    return out


def recover_job_worktrees(job_id: str) -> list[WorktreeResumeOutcome]:
    """Recover every interrupted worktree recorded for this job."""
    return [
        resume_worktree_run(str(data.get("run_id") or ""))
        for data in find_recoverable_runs(job_id)
        if data.get("run_id")
    ]

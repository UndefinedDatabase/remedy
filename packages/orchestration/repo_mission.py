"""One registered repository has exactly ONE lasting mission; each order is a batch under it.

DECISION amend1011b D1 (identity). A repository's mission is found from the repository, never
chosen by the operator and never guessed by a model. The identity is the registered project's
id for the project's canonical repository, and the project id plus a digest of the repository's
git common directory for any further repository the project holds, so a linked worktree of a
repository is that repository, two independent clones that share a remote are two, and a
checkout the registry moves keeps its mission. A path the project does not hold is refused.

DECISION amend1011b D2 (atomic accept). `accept_order` looks the mission up, creates it once,
seals the previous order and appends the new batch inside one exclusive lock on a lock file in
the project's mission directory, so simultaneous CLI, UI and API starts become distinct queued
batches of one mission and none can produce a second mission or lose a link.

DECISION amend1011b D3 (batches). The mission keeps the current order's order, plan and
contract in the slots it always had, so every consumer that reads "the mission's contract"
reads the current order's. Accepting the next order copies those slots into the previous
batch's ``sealed`` field first; an earlier order is therefore never overwritten.

The lock is advisory (`fcntl.flock`), as the worktree locks beside it are.
"""

from __future__ import annotations

import fcntl
import hashlib
import os
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.mission_record import (
    MISSION_ROLE_FOLLOW_UP,
    MISSION_ROLE_INITIAL,
    MISSION_STATUS_ABANDONED,
    MISSION_STATUS_ACHIEVED,
    MISSION_STATUS_ACTIVE,
    MISSION_STATUS_PAUSED,
    PLAN_VERSION_KEY,
    PLAN_VERSIONS_KEY,
    Mission,
    MissionError,
    MissionOrder,
    MissionOrderBatch,
)
from packages.orchestration.mission_state import (
    MISSING_JOB_LABEL,
    MISSION_ENDED_STATUSES,
    create_mission,
    link_job_to_mission,
    list_missions,
    list_missions_safe,
    load_mission,
    mission_dir_for_project,
    mission_job_state_label,
    project_ids_with_missions,
    save_mission,
)

LOCK_FILENAME = ".repo-mission.lock"

#: The kinds of order a batch records: one that builds, and one that only reads (DECISION
#: amend1011b D7); a read-only order adds no build job.
ORDER_KIND_BUILD = "build"
ORDER_KIND_READ_ONLY = "read_only"


class RepoMissionError(MissionError):
    """The repository cannot be tied to exactly one mission, or the mission may not take an order."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------


def _git_common_dir(path: str | Path) -> str:
    """The real path of the git common directory of the repository at *path*, or the real path."""
    real = os.path.realpath(str(path))
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=real, capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return real
    out = proc.stdout.strip()
    return os.path.realpath(out) if proc.returncode == 0 and out else real


def repo_key(project: Any, repo_root: str | Path) -> str:
    """The identity of *repo_root* within *project*, or a :class:`RepoMissionError`.

    The project's canonical repository is keyed by the project id alone; any other repository
    the project holds by the project id and a digest of its git common directory.
    """
    project_id = str(project.id)
    if not repo_root and not project.canonical_repo_path and not project.repo_paths:
        return project_id      # a project with no repository is its own identity
    wanted = _git_common_dir(repo_root)
    canonical = project.canonical_repo_path
    if canonical and _git_common_dir(canonical) == wanted:
        return project_id
    others = [path for path in project.repo_paths if path != canonical]
    held = [path for path in others if _git_common_dir(path) == wanted]
    if held:
        return f"{project_id}:{hashlib.sha256(wanted.encode()).hexdigest()[:12]}"
    raise RepoMissionError(
        f"{repo_root} is not a repository of project {getattr(project, 'slug', project_id)}; "
        f"register it before giving it an order")


@contextmanager
def repo_mission_lock(project_id: str, root: Path | None = None) -> Iterator[None]:
    """Hold the exclusive per-project lock that makes lookup, create and enqueue one step."""
    directory = mission_dir_for_project(project_id, root)
    directory.mkdir(parents=True, exist_ok=True)
    fd = os.open(directory / LOCK_FILENAME, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def canonical_candidates(project_id: str, key: str, root: Path | None = None) -> list[Mission]:
    """The live missions that may be the repository's, canonical one first (DECISION amend1011b D1).

    A record stamped with the key is the repository's. An unstamped record of the project's own
    repository (the key is the bare project id) is a legacy one and a candidate; an unstamped
    record that spans several projects is a legacy umbrella and is never one. The canonical one
    is the oldest that has jobs, else the oldest, ties broken by id; the others are duplicates
    for `reconcile_repo_missions` and are never chosen between by anything else.
    """
    missions, _degraded, _skipped = list_missions_safe(project_id, root)
    own = [m for m in missions
           if m.repo == key or (not m.repo and key == project_id and not m.project_ids)]
    return sorted(own, key=lambda m: (not m.job_links, m.created_at, m.id))


# ---------------------------------------------------------------------------
# Accepting an order
# ---------------------------------------------------------------------------


def _seal(mission: Mission) -> tuple[MissionOrderBatch, ...]:
    """The mission's batches with the current one sealed, a legacy order made a batch first."""
    orders = mission.orders
    if not orders and (mission.order is not None or mission.job_links):
        order = mission.order or MissionOrder(text=mission.goal)
        orders = (MissionOrderBatch(
            order_id=f"legacy-{mission.id[:12]}", text=order.text, source_path=order.source_path,
            source_sha256=order.source_sha256, created_at=mission.created_at),)
    if not orders or orders[-1].sealed is not None:
        return orders
    plan = mission.mission_plan
    # The chain stays in the mission's plan slot; a sealed batch keeps its own body only
    # (operator amendment amend1014-luna-mission-fixes A.1), so the record grows by one plan.
    body = ({k: v for k, v in plan.items() if k != PLAN_VERSIONS_KEY}
            if isinstance(plan, dict) else plan)
    sealed = {"sealed_at": _utc_now(), "plan_version": int((plan or {}).get(PLAN_VERSION_KEY, 0)),
              "plan": body, "contract": mission.contract}
    return (*orders[:-1], replace(orders[-1], sealed=sealed))


def _target_commit(repo_root: str | Path) -> str:
    if not repo_root:
        return ""
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo_root),
                              capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return ""
    return proc.stdout.strip() if proc.returncode == 0 else ""


def _find_or_create(project: Any, key: str, root: Path | None) -> Mission:
    """The repository's mission, created only when it has none; the caller holds the lock."""
    project_id = str(project.id)
    candidates = canonical_candidates(project_id, key, root)
    if candidates:
        return candidates[0]
    return create_mission(
        project_id, f"Maintain {getattr(project, 'slug', None) or project.name}", root=root)


def ensure_repo_mission(project: Any, repo_root: str | Path, *,
                        root: Path | None = None) -> tuple[Mission, bool]:
    """The repository's one mission and whether this call created it; no order is added."""
    key = repo_key(project, repo_root)
    with repo_mission_lock(str(project.id), root):
        existing = canonical_candidates(str(project.id), key, root)
        mission = _find_or_create(project, key, root)
        if mission.repo != key:
            mission = replace(mission, repo=key)
            save_mission(mission, root)
    return mission, not existing


def _refusal(mission: Mission | None) -> str:
    """Why *mission* takes no order: a paused or abandoned one waits for the operator; empty otherwise."""
    if mission is None or mission.status not in (MISSION_STATUS_PAUSED, MISSION_STATUS_ABANDONED):
        return ""
    return (f"mission {mission.id} of this repository is {mission.status}; "
            f"resume it first: remedy mission resume {mission.id[:12]}")


def order_refusal(project: Any, repo_root: str | Path, root: Path | None = None) -> str:
    """Why the repository's mission would refuse an order, read without creating or changing
    anything; empty when it would take one (R-1250)."""
    candidates = canonical_candidates(str(project.id), repo_key(project, repo_root), root)
    return _refusal(candidates[0] if candidates else None)


def accept_order(project: Any, repo_root: str | Path, order: MissionOrder, *,
                 kind: str = ORDER_KIND_BUILD, budgets: dict[str, Any] | None = None,
                 correlation_id: str = "", root: Path | None = None,
                 ) -> tuple[Mission, MissionOrderBatch]:
    """Append *order* as a new batch to the repository's one mission, creating it only once.

    An achieved mission is reopened by the order and the batch says so; a paused or abandoned
    one refuses until the operator resumes it (`remedy mission resume`), because a stopped
    mission is the operator's decision and a replacement mission is never created behind it.
    """
    project_id = str(project.id)
    key = repo_key(project, repo_root)
    with repo_mission_lock(project_id, root):
        mission = _find_or_create(project, key, root)
        if _refusal(mission):
            raise RepoMissionError(_refusal(mission))
        reopened = mission.status if mission.status == MISSION_STATUS_ACHIEVED else ""
        batch = MissionOrderBatch(
            order_id=uuid4().hex, text=order.text, source_path=order.source_path,
            source_sha256=order.source_sha256, created_at=_utc_now(),
            target_commit=_target_commit(repo_root), kind=kind, budgets=budgets,
            correlation_id=correlation_id, reopened_from=reopened)
        mission = replace(
            mission, repo=key, status=MISSION_STATUS_ACTIVE, order=order, contract=None,
            orders=(*_seal(mission), batch))
        save_mission(mission, root)
    return mission, batch


def accept_order_in_each(targets: list[tuple[Any, str]], order: MissionOrder, *,
                         budgets: dict[str, Any] | None = None,
                         root: Path | None = None) -> dict[str, tuple[str, str]]:
    """Accept *order* as a batch in the mission of each (project, repository) of TARGETS, and in
    none unless every one can take it (R-1250): each is asked first, then each accepts.

    An order over several repositories shares one correlation id and no umbrella mission
    (DECISION amend1011b D4). Answers each project id's (mission id, order id).
    """
    for project, repo_root in targets:
        if order_refusal(project, repo_root, root):
            raise RepoMissionError(order_refusal(project, repo_root, root))
    correlation = uuid4().hex if len(targets) > 1 else ""
    accepted: dict[str, tuple[str, str]] = {}
    for project, repo_root in targets:
        mission, batch = accept_order(project, repo_root, order, budgets=budgets,
                                      correlation_id=correlation, root=root)
        accepted[str(project.id)] = (mission.id, batch.order_id)
    return accepted


def link_order_job(project_id: str, mission_id: str, order_id: str, job_id: str,
                   root: Path | None = None) -> Mission:
    """Link a job to the mission under an order batch: the first job ever is ``initial``, then ``follow_up``."""
    with repo_mission_lock(project_id, root):
        current = load_mission(project_id, mission_id, root)
        role = MISSION_ROLE_FOLLOW_UP if current.job_links else MISSION_ROLE_INITIAL
        return link_job_to_mission(project_id, mission_id, job_id, role,
                                   order_id=order_id, root=root)


def unlink_order_jobs(project_id: str, mission_id: str, job_ids: list[str],
                      root: Path | None = None) -> Mission:
    """Take jobs that will never run out of the mission's chain (R-1247), so none of them is ever
    its latest link; a job id the chain does not hold is passed over."""
    drop = set(job_ids)
    with repo_mission_lock(project_id, root):
        current = load_mission(project_id, mission_id, root)
        kept = tuple(link for link in current.job_links if link.job_id not in drop)
        if len(kept) == len(current.job_links):
            return current
        mission = replace(current, job_links=kept)
        save_mission(mission, root)
    return mission


def order_batch_view(mission: Mission) -> list[dict[str, Any]]:
    """One row per batch, oldest first, with the jobs the chain attributes to it (DECISION amend1011b D3)."""
    rows = []
    for batch in mission.orders:
        rows.append({**batch.to_json(), "sealed": batch.sealed is not None,
                     "job_ids": [link.job_id for link in mission.job_links
                                 if link.order_id == batch.order_id]})
    unattributed = [link.job_id for link in mission.job_links
                    if not any(link.order_id == b.order_id for b in mission.orders)]
    if unattributed:
        rows.insert(0, {"order_id": "", "text": "(jobs linked before order records)",
                        "job_ids": unattributed, "sealed": True})
    return rows



def project_repo_root(project: Any) -> str:
    """The repository a project's one mission is for: its canonical one, else its first, else ""."""
    return str(project.canonical_repo_path or (project.repo_paths[0] if project.repo_paths else ""))


def ensure_project_mission(project_id: str, *, root: Path | None = None) -> tuple[Mission, bool]:
    """`ensure_repo_mission` for the project's own repository, from a project id."""
    project = project_by_id(project_id)
    return ensure_repo_mission(project, project_repo_root(project), root=root)


# WHY: one order file started twice must not quietly queue the same work again beside the
# first (T004 of docs/roadmap/features/T12_F304.md, DECISION F304 D6); since DECISION
# amend1011b D1 a repository has one mission, so the question is whether an earlier order of
# the file still has jobs that have not finished, not whether a second mission would start.
def _unfinished_jobs(mission: Mission, order_id: str) -> bool:
    from packages.orchestration.pingpong_job import JOB_TERMINAL_STATES

    finished = {state.value for state in JOB_TERMINAL_STATES} | {MISSING_JOB_LABEL}
    return any(mission_job_state_label(link.job_id) not in finished
               for link in mission.job_links if link.order_id == order_id)


def running_mission_for_order_file(source_path: str, root: Path | None = None) -> Mission | None:
    """The newest mission that has not ended and still has work of an order file, or None.

    A mission with order batches has such work when a batch that records *source_path* has a
    job that has not finished; one without batches, as before, whenever its order records
    *source_path*. Scans every project's mission area, as `mission_for_job` does, because a
    client may name the order file from anywhere. *source_path* is compared as
    `read_order_file` records it, a resolved absolute path; an empty one matches nothing.
    """
    wanted = str(source_path)
    if not wanted:
        return None

    def running(mission: Mission) -> bool:
        if mission.status in MISSION_ENDED_STATUSES:
            return False
        if not mission.orders:
            return mission.order is not None and mission.order.source_path == wanted
        return any(batch.source_path == wanted and _unfinished_jobs(mission, batch.order_id)
                   for batch in mission.orders)

    found = [mission for project_id in project_ids_with_missions(root)
             for mission in list_missions(project_id, root) if running(mission)]
    return max(found, key=lambda mission: mission.created_at, default=None)


#: How many of a mission's most recent orders and jobs the text rendering lists; a repository's
#: lasting mission can hold hundreds, and the JSON form always holds all of them.
RENDER_RECENT = 25


def chain_start(mission: Mission) -> int:
    """The index of the first job link the text rendering lists."""
    return max(0, len(mission.job_links) - RENDER_RECENT)


def render_order_lines(mission: Mission, recent: int = RENDER_RECENT) -> list[str]:
    """The order table `remedy mission show` prints: the last *recent* orders and a count of the rest."""
    lines: list[str] = []
    if mission.orders:
        lines.append(f"  Orders: {len(mission.orders)}")
        for batch in mission.orders[-recent:]:
            count = sum(1 for link in mission.job_links if link.order_id == batch.order_id)
            first_line = (batch.text.strip().splitlines() or [""])[0][:60]
            lines.append(f"    {batch.created_at[:16]}  {batch.order_id[:12]}  "
                         f"{count} job(s)  {first_line}")
        if len(mission.orders) > recent:
            lines.append(f"    ... {len(mission.orders) - recent} earlier order(s); "
                         f"all are in `remedy mission show --json`")
    return lines


def project_by_id(project_id: str) -> Any:
    """The registered project with this id, or, for an id the registry does not hold, a stand-in.

    A mission can name a project that was unregistered; its repository is then unknown and the
    project id alone is its identity, as for a project with no repository.
    """
    from types import SimpleNamespace
    from uuid import UUID

    from packages.orchestration.project_registry import ProjectNotFoundError, load_project

    try:
        return load_project(UUID(str(project_id)))
    except (ValueError, ProjectNotFoundError, OSError):
        return SimpleNamespace(id=project_id, slug=project_id, name=project_id,
                               canonical_repo_path=None, repo_paths=[])

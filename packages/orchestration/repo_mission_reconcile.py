"""Fold the duplicate missions of one repository into its one mission, losslessly (DECISION amend1011b D6).

Before DECISION amend1011b D1 every order made a mission, so a repository may hold several. This
module reads them, says what folding them would do (`reconcile_repo_missions` without
``apply``), and does it (with ``apply``) so that afterwards:

* the oldest mission with jobs (`canonical_candidates`) is the repository's one mission, and
  every other record of the repository is an ``alias_of`` redirect that no listing shows and
  that `load_mission` follows, so every old id still resolves;
* every folded mission becomes one sealed legacy batch of the canonical one, carrying its goal,
  status, plan, contract and each job's old role (``legacy_roles``), and its evidence directory
  moves under ``evidence/legacy/<old id>``; the chain is the union of all links in time order
  with exactly one ``initial``;
* a legacy mission that spans several projects gives each of its jobs to the mission of the
  project that job works in, so no job has two owners and no umbrella mission remains.

Nothing is changed before the whole project area is copied to a backup directory next to the
missions (``restore_reconcile`` puts it back), nothing is folded while a job of the group is
not ended or a record in the area cannot be read, and a run that finds a job without exactly one
owner afterwards restores the backup itself. The run is idempotent: batch ids are derived from
the folded mission's id, a job already linked in the canonical mission is not linked twice, and
a second run finds nothing to fold.
"""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.mission_record import (
    MISSION_ROLE_FOLLOW_UP,
    MISSION_ROLE_INITIAL,
    PLAN_VERSION_KEY,
    PLAN_VERSIONS_KEY,
    Mission,
    MissionError,
    MissionJobLink,
    MissionOrder,
    MissionOrderBatch,
)
from packages.orchestration.mission_state import (
    MISSING_JOB_LABEL,
    list_missions_safe,
    mission_evidence_dir,
    mission_job_state_label,
    mission_root,
    project_ids_with_missions,
    repo_mission_lock,
    save_mission,
)
from packages.orchestration.pingpong_job import JOB_TERMINAL_STATES
from packages.orchestration.repo_mission import canonical_candidates

BACKUP_DIRNAME = "reconcile-backups"
#: The labels of a job a fold may move: one that ended, and one whose record is gone. Anything
#: else, a paused job or one whose plan cannot be read included, refuses the fold (operator
#: amendment amend1014-luna-mission-fixes A.5).
_ENDED_LABELS = frozenset({state.value for state in JOB_TERMINAL_STATES} | {MISSING_JOB_LABEL})


def _legacy_batch(mission: Mission, link_roles: dict[str, str]) -> MissionOrderBatch:
    """The sealed batch a folded mission becomes."""
    order = mission.order or MissionOrder(text=mission.goal)
    return MissionOrderBatch(
        order_id=f"legacy-{mission.id[:12]}", text=order.text, source_path=order.source_path,
        source_sha256=order.source_sha256, created_at=mission.created_at,
        sealed={"legacy_mission": mission.id, "goal": mission.goal, "status": mission.status,
                "dossier_ref": mission.dossier_ref, "plan": mission.mission_plan,
                "contract": mission.contract, "legacy_roles": link_roles})


def _groups(project_id: str, root: Path | None) -> tuple[list[tuple[Mission, list[Mission]]], list[str]]:
    """``[(canonical, [duplicates])]`` of one project, and the reasons it cannot be folded."""
    missions, degraded, skipped = list_missions_safe(project_id, root)
    refused = [f"record {name} cannot be read" for name in skipped] if degraded else []
    own = [m for m in missions if not m.project_ids]
    if len({m.repo for m in own if m.repo}) > 1:
        refused.append("the project holds missions of several repositories; fold them by hand")
    keyed = canonical_candidates(project_id, own[0].repo or project_id, root) if own else []
    umbrellas = [m for m in missions if m.project_ids]
    groups = [(keyed[0], keyed[1:])] if keyed and (len(keyed) > 1 or umbrellas) else []
    if umbrellas and not keyed:
        refused.append("a legacy cross-repository mission has no mission of its own project to join")
    for umbrella in umbrellas:
        if groups:
            groups[0][1].append(umbrella)
    return groups, refused


def reconcile_repo_missions(*, apply: bool = False, root: Path | None = None) -> dict[str, Any]:
    """Report, or with *apply* carry out, the folding of every project's duplicate missions."""
    report: dict[str, Any] = {"applied": apply, "projects": [], "refused": []}
    for project_id in project_ids_with_missions(root):
        groups, refused = _groups(project_id, root)
        unended = [f"{link.job_id} ({label})" for canonical, dups in groups
                   for m in [canonical, *dups] for link in m.job_links
                   if (label := mission_job_state_label(link.job_id)) not in _ENDED_LABELS]
        if unended:
            refused.append(f"jobs have not ended: {', '.join(unended)}")
        entry = {"project_id": project_id, "refused": refused, "groups": [
            {"canonical": canonical.id,
             "folded": [{"mission": m.id, "status": m.status, "job_ids": list(m.job_ids()),
                         "evidence": str(mission_evidence_dir(project_id, m.id, root)),
                         "orders": [b.order_id for b in m.orders]} for m in dups]}
            for canonical, dups in groups]}
        if refused:
            report["refused"].append({"project_id": project_id, "reasons": refused})
        elif groups and apply:
            entry["backup"] = str(_fold_project(project_id, groups, root))
        if groups or refused:
            report["projects"].append(entry)
    report["flatten"] = _flatten_plan_versions(apply=apply, root=root)
    return report


# ---------------------------------------------------------------------------
# Flatten plan versions (operator amendment amend1014-luna-mission-fixes A.1)
# ---------------------------------------------------------------------------


def _flat_chain(body: Any) -> list[dict[str, Any]]:
    """Every version a plan body's chain holds at any depth, once each, ordered by version,
    each without a chain of its own; the innermost copy of a version wins."""
    found: dict[Any, dict[str, Any]] = {}

    def walk(node: Any) -> None:
        for version in (node or {}).get(PLAN_VERSIONS_KEY, []) if isinstance(node, dict) else []:
            walk(version)
            if isinstance(version, dict):
                found.setdefault(version.get(PLAN_VERSION_KEY),
                                 {k: v for k, v in version.items() if k != PLAN_VERSIONS_KEY})

    walk(body)
    return sorted(found.values(), key=lambda v: int(v.get(PLAN_VERSION_KEY) or 0))


def _nested(body: Any) -> bool:
    """Whether a plan body's chain holds a version that carries a chain itself."""
    return isinstance(body, dict) and any(
        isinstance(v, dict) and PLAN_VERSIONS_KEY in v for v in body.get(PLAN_VERSIONS_KEY, []))


def _flattened(mission: Mission) -> Mission | None:
    """The mission with a flat plan chain and chain-free sealed plans, or None when it has both.

    A sealed plan's own chain is dropped only when every version in it is also in the mission's
    flat chain; a folded legacy mission's chain is not, so it is kept, flattened.
    """
    plan = mission.mission_plan
    sealed_plans = [b.sealed.get("plan") for b in mission.orders if b.sealed]
    if not _nested(plan) and not any(isinstance(p, dict) and PLAN_VERSIONS_KEY in p
                                     for p in sealed_plans):
        return None
    chain = _flat_chain(plan)
    if isinstance(plan, dict):
        plan = {**plan, PLAN_VERSIONS_KEY: chain}
    orders = []
    for batch in mission.orders:
        body = (batch.sealed or {}).get("plan")
        if isinstance(body, dict) and PLAN_VERSIONS_KEY in body:
            own = _flat_chain(body)
            rest = {k: v for k, v in body.items() if k != PLAN_VERSIONS_KEY}
            body = rest if all(v in chain for v in own) else {**rest, PLAN_VERSIONS_KEY: own}
            batch = replace(batch, sealed={**batch.sealed, "plan": body})
        orders.append(batch)
    return replace(mission, mission_plan=plan, orders=tuple(orders))


def _record_bytes(mission: Mission) -> int:
    return len(json.dumps(mission.to_json(), indent=2, sort_keys=True).encode())


def _flatten_plan_versions(*, apply: bool, root: Path | None) -> list[dict[str, Any]]:
    """Report, or with *apply* write, every live mission whose plan chain nests; one backup first."""
    rows: list[dict[str, Any]] = []
    backup: Path | None = None
    for project_id in project_ids_with_missions(root):
        for mission in list_missions_safe(project_id, root)[0]:
            flat = _flattened(mission)
            if flat is None:
                continue
            row = {"project_id": project_id, "mission": mission.id,
                   "bytes_before": _record_bytes(mission), "bytes_after": _record_bytes(flat)}
            if apply:
                if backup is None:
                    backup = _backup_area(root)
                with repo_mission_lock(project_id, root):
                    from packages.orchestration.mission_state import load_mission

                    fresh = _flattened(load_mission(project_id, mission.id, root))
                    if fresh is not None:
                        save_mission(fresh, root)
                row["backup"] = str(backup)
            rows.append(row)
    return rows


def _backup_area(root: Path | None) -> Path:
    """Copy the whole mission area beside it, before anything is written."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    area = mission_root(root)
    backup = area.parent / BACKUP_DIRNAME / stamp
    shutil.copytree(area, backup)
    return backup


def _fold_project(project_id: str, groups: list[tuple[Mission, list[Mission]]],
                  root: Path | None) -> Path:
    backup = _backup_area(root)
    owned_before = _owned_jobs(root)
    try:
        with repo_mission_lock(project_id, root):
            for canonical, dups in groups:
                _fold_group(project_id, canonical, dups, root)
        owned_after = _owned_jobs(root)
        if set(owned_after) != set(owned_before):
            raise MissionError("a job lost or gained an owner while folding")
        shared = sorted({job for job in owned_after if owned_after.count(job) > 1})
        if shared:
            raise MissionError(f"jobs are linked in two live missions after folding: "
                               f"{', '.join(shared)}")
    except Exception:
        restore_reconcile(backup, root)
        raise
    return backup


def _owned_jobs(root: Path | None) -> list[str]:
    """Every job linked in any live mission, once per link, sorted.

    Before a fold a job may be linked twice: a fold interrupted after the canonical mission was
    saved and before the duplicate became an alias leaves it so, and the next run folds it
    (operator amendment amend1014-luna-mission-fixes A.3). After a fold each has one owner.
    """
    return sorted(job for project_id in project_ids_with_missions(root)
                  for m in list_missions_safe(project_id, root)[0] for job in m.job_ids())


def _fold_group(project_id: str, canonical: Mission, dups: list[Mission], root: Path | None) -> None:
    from packages.orchestration.mission_state import load_mission

    canonical = load_mission(project_id, canonical.id, root)
    sources = [canonical, *[d for d in dups if not d.alias_of]]
    batches: dict[str, MissionOrderBatch] = {b.order_id: b for b in canonical.orders}
    links: dict[str, MissionJobLink] = {link.job_id: link for link in canonical.job_links}
    roles: dict[str, dict[str, str]] = {}
    for source in sources:
        legacy_id = f"legacy-{source.id[:12]}"
        if source.orders and source is not canonical:
            batches.update({b.order_id: b for b in source.orders})
        elif not source.orders:
            roles[legacy_id] = {link.job_id: link.role for link in source.job_links}
        for link in source.job_links:
            if link.project_id and link.project_id != project_id:
                _hand_to_project_mission(link, source, legacy_id, root)
                continue
            links.setdefault(link.job_id, replace(
                link, order_id=link.order_id or legacy_id, project_id=""))
    for source in sources:
        legacy_id = f"legacy-{source.id[:12]}"
        if not source.orders and legacy_id not in batches:
            batches[legacy_id] = _legacy_batch(source, roles.get(legacy_id, {}))
    # The canonical mission's own current batch stays last: the order, plan and contract slots
    # still hold ITS order, and the next order seals them under the last batch.
    own_last = canonical.orders[-1].order_id if canonical.orders else f"legacy-{canonical.id[:12]}"
    ordered = sorted(batches.values(), key=lambda b: (b.order_id == own_last, b.created_at, b.order_id))
    chain = sorted(links.values(), key=lambda link: (link.created_at, link.job_id))
    chain = [replace(link, role=MISSION_ROLE_INITIAL if index == 0 else MISSION_ROLE_FOLLOW_UP)
             for index, link in enumerate(chain)]
    for source in dups:
        if source.alias_of:
            continue
        old = mission_evidence_dir(project_id, source.id, root)
        if old.is_dir():
            target = mission_evidence_dir(project_id, canonical.id, root) / "legacy" / source.id
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(old, target, dirs_exist_ok=True)
            shutil.rmtree(old)
    folded = replace(canonical, orders=tuple(ordered), job_links=tuple(chain),
                     project_ids=())
    save_mission(folded, root)
    for source in dups:
        if not source.alias_of:
            save_mission(Mission(
                id=source.id, project_id=source.project_id, goal=source.goal,
                status=source.status, created_at=source.created_at, alias_of=canonical.id), root)


class ReconcileBackupInvalidError(MissionError):
    """A restore was asked for from something that is not one of reconcile's own backups."""


def _check_backup(backup: Path, area: Path) -> None:
    """Refuse, before anything is written, a *backup* that reconcile did not make."""
    folder = (area.parent / BACKUP_DIRNAME).resolve()
    if not backup.is_dir():
        raise ReconcileBackupInvalidError(f"{backup} is not a directory; nothing was restored")
    if backup.resolve().parent != folder:
        raise ReconcileBackupInvalidError(
            f"{backup} is not a backup under {folder}; nothing was restored")
    if next(backup.rglob("*.json"), None) is None:
        raise ReconcileBackupInvalidError(
            f"{backup} holds no mission file; nothing was restored")


def restore_reconcile(backup: Path | str, root: Path | None = None) -> Path:
    """Put the whole mission area back as the *backup* holds it; the rollback path.

    Operator amendment amend1014-luna-mission-fixes A.2: the backup is checked before anything
    is touched, then copied beside the area and swapped in with two renames, and the replaced
    area (a copy of data the backup already holds) is removed only after the swap succeeded.
    """
    area = mission_root(root)
    backup = Path(backup)
    _check_backup(backup, area)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    staged = area.with_name(f"{area.name}.restoring-{stamp}")
    replaced = area.with_name(f"{area.name}.replaced-{stamp}")
    shutil.copytree(backup, staged)
    if area.is_dir():
        os.replace(area, replaced)
    os.replace(staged, area)
    if replaced.is_dir():
        shutil.rmtree(replaced)
    return area


def _hand_to_project_mission(link: MissionJobLink, umbrella: Mission, legacy_id: str,
                             root: Path | None) -> None:
    """Give one job of a legacy cross-repository mission to its own project's mission.

    The target is that project's canonical mission, made when it has none; the job joins it
    under a legacy batch named after the umbrella, and the umbrella's role is kept there.
    """
    from packages.orchestration.mission_state import create_mission, load_mission

    target_project = link.project_id
    found = canonical_candidates(target_project, target_project, root)
    target = found[0] if found else create_mission(
        target_project, f"Maintain {target_project}", root=root)
    target = load_mission(target_project, target.id, root)
    if link.job_id in target.job_ids():
        return
    batch = next((b for b in target.orders if b.order_id == legacy_id), None)
    if batch is None:
        batch = replace(_legacy_batch(umbrella, {}), sealed={
            "legacy_mission": umbrella.id, "goal": umbrella.goal, "status": umbrella.status,
            "plan": None, "contract": None, "legacy_roles": {}})
    sealed = dict(batch.sealed or {})
    sealed["legacy_roles"] = {**sealed.get("legacy_roles", {}), link.job_id: link.role}
    batch = replace(batch, sealed=sealed)
    orders = (*[b for b in target.orders if b.order_id != legacy_id], batch)
    role = MISSION_ROLE_FOLLOW_UP if target.job_links else MISSION_ROLE_INITIAL
    save_mission(replace(
        target, repo=target.repo or target_project, orders=orders,
        job_links=(*target.job_links, replace(link, role=role, order_id=legacy_id,
                                              project_id=""))), root)

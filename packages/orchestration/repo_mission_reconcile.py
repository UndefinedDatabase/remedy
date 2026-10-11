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
running or a record in the area cannot be read, and a run that finds a job without exactly one
owner afterwards restores the backup itself. The run is idempotent: batch ids are derived from
the folded mission's id, a job already linked in the canonical mission is not linked twice, and
a second run finds nothing to fold.
"""

from __future__ import annotations

import shutil
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.mission_record import (
    MISSION_ROLE_FOLLOW_UP,
    MISSION_ROLE_INITIAL,
    Mission,
    MissionError,
    MissionJobLink,
    MissionOrder,
    MissionOrderBatch,
)
from packages.orchestration.mission_state import (
    list_missions_safe,
    mission_evidence_dir,
    mission_job_state_label,
    mission_root,
    project_ids_with_missions,
    save_mission,
)
from packages.orchestration.repo_mission import canonical_candidates, repo_mission_lock

BACKUP_DIRNAME = "reconcile-backups"
_RUNNING_LABELS = ("running",)


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
        running = [link.job_id for canonical, dups in groups for m in [canonical, *dups]
                   for link in m.job_links if mission_job_state_label(link.job_id) in _RUNNING_LABELS]
        if running:
            refused.append(f"jobs are running: {', '.join(running)}")
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
    return report


def _fold_project(project_id: str, groups: list[tuple[Mission, list[Mission]]],
                  root: Path | None) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    area = mission_root(root)
    backup = area.parent / BACKUP_DIRNAME / stamp
    shutil.copytree(area, backup)
    owned_before = _owned_jobs(root)
    try:
        with repo_mission_lock(project_id, root):
            for canonical, dups in groups:
                _fold_group(project_id, canonical, dups, root)
        if _owned_jobs(root) != owned_before:
            raise MissionError("a job lost or gained an owner while folding")
    except Exception:
        restore_reconcile(backup, root)
        raise
    return backup


def _owned_jobs(root: Path | None) -> list[str]:
    """Every job linked in any live mission, once per link, sorted: each must have one owner."""
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


def restore_reconcile(backup: Path, root: Path | None = None) -> Path:
    """Put the whole mission area back as the *backup* holds it; the rollback path."""
    area = mission_root(root)
    if area.is_dir():
        shutil.rmtree(area)
    shutil.copytree(Path(backup), area)
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

"""F079 T001 — the context handoff: a COMPOSITION, never a new truth.

At a session or context-window boundary Remedy packages what it already
knows into one versioned artifact so a fresh context can pick the mission
up::

    <data root>/missions/<project id>/<mission id>/evidence/handoff_v1.json
    <data root>/missions/<project id>/<mission id>/evidence/handoff_v1.md

The same evidence area — and the same ``handoff_v<N>`` accumulation rule —
the dossier's ``dossier_v<N>.md`` versions already use, because a second
evidence convention would be a second place to look.

What a handoff is, and what it deliberately is not:

* It COMPOSES existing sources: the dossier's own renderer
  (:mod:`packages.orchestration.mission_dossier`), the checkpoint the run
  wrote (:mod:`packages.orchestration.checkpoints`), the open decisions the
  queue derives (:mod:`packages.orchestration.decision_queue`) and the next
  intent the checkpoint recorded. Nothing here re-implements any of them.
* It is a PURE ARTIFACT: building one reads mission, job and queue state and
  writes only into the mission's evidence area — no status move, no ledger
  entry, no queue mutation.
* It is IDEMPOTENT PER STATE. Content is derived from the sources alone —
  provenance timestamps are the SOURCE artifacts' own — so the same state
  yields byte-identical bytes, a repeat build returns the existing handoff
  rather than a duplicate, and changed state writes the next version.
* A missing source is a NAMED GAP, never invented content — a zero-progress
  mission is a valid handoff: its goal plus gap entries.

Consuming a handoff — verifying that its checkpoint and worktree references
still hold before a resumed context trusts the narrative — is F079 T002 and
deliberately does NOT live here yet.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.mission_state import (
    Mission,
    list_missions_safe,
    mission_evidence_dir,
    project_ids_with_missions,
)

#: Bumped only when the composed body's SHAPE changes. A consumer that reads a
#: version it does not know must refuse rather than guess (T002's job).
HANDOFF_SCHEMA_VERSION = 1

#: One file per version, beside the dossier versions in the mission's evidence
#: area. Never overwritten: a handoff is the account of what a successor
#: context was told, and rewriting it would destroy that account.
HANDOFF_VERSION_TEMPLATE = "handoff_v{version}.json"
HANDOFF_RENDER_TEMPLATE = "handoff_v{version}.md"

#: The rendered prompt block's section order — fixed, dossier first, so the
#: text stays a cache-stable prefix the way the dossier itself is.
HANDOFF_SECTIONS: tuple[str, ...] = (
    "Dossier",
    "Checkpoint",
    "Open decisions",
    "Next intent",
    "Gaps",
    "Provenance",
)

#: The named sources a gap can be about. Named constants rather than free text
#: so a consumer can branch on a gap without parsing prose.
GAP_DOSSIER = "dossier"
GAP_JOBS = "jobs"
GAP_CHECKPOINT = "checkpoint"
GAP_WORKTREE_HEAD = "worktree_head"
GAP_OPEN_DECISIONS = "open_decisions"
GAP_NEXT_INTENT = "next_intent"


class HandoffError(RuntimeError):
    """The handoff could not be composed."""


class MissionForHandoffNotFoundError(HandoffError):
    """No mission with that id exists under the data root.

    Not a gap: a gap is a missing PART of a mission's story, and without the
    mission there is no story to hand over.
    """

    def __init__(self, mission_id: str) -> None:
        super().__init__(f"no mission {mission_id!r} exists to hand off")
        self.mission_id = mission_id


@dataclass(frozen=True)
class HandoffGap:
    """One source that could not be read, named rather than invented."""

    source: str
    detail: str

    def to_json(self) -> dict[str, str]:
        return {"source": self.source, "detail": self.detail}


# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------

def handoff_path(project_id: str, mission_id: str, version: int,
                 root: Path | None = None) -> Path:
    """Where one version of one mission's handoff body lives."""
    return (mission_evidence_dir(project_id, mission_id, root)
            / HANDOFF_VERSION_TEMPLATE.format(version=int(version)))


def handoff_render_path(project_id: str, mission_id: str, version: int,
                        root: Path | None = None) -> Path:
    """Where one version of the rendered prompt block lives."""
    return (mission_evidence_dir(project_id, mission_id, root)
            / HANDOFF_RENDER_TEMPLATE.format(version=int(version)))


def handoff_versions(project_id: str, mission_id: str,
                     root: Path | None = None) -> list[int]:
    """Every stored handoff version number, ascending. Odd names are skipped."""
    directory = mission_evidence_dir(project_id, mission_id, root)
    if not directory.is_dir():
        return []
    prefix, suffix = HANDOFF_VERSION_TEMPLATE.split("{version}")
    found: list[int] = []
    for path in directory.glob(f"{prefix}*{suffix}"):
        raw = path.name[len(prefix):-len(suffix)]
        if raw.isdigit():
            found.append(int(raw))
    return sorted(found)


def latest_handoff_version(project_id: str, mission_id: str,
                           root: Path | None = None) -> int:
    """The newest stored handoff version, or 0 when none is stored yet."""
    versions = handoff_versions(project_id, mission_id, root)
    return versions[-1] if versions else 0


def find_mission_record(mission_id: str, root: Path | None = None,
                        ) -> Mission | None:
    """The mission with this id, whichever project holds it.

    ``build_handoff`` takes a mission id alone — a boundary is reached with
    the mission in hand, not the project — so the project is resolved from
    disk here rather than demanded from the caller.
    """
    for project_id in project_ids_with_missions(root):
        missions, _degraded, _skipped = list_missions_safe(project_id, root)
        for mission in missions:
            if mission.id == str(mission_id):
                return mission
    return None


# ---------------------------------------------------------------------------
# Redaction — the manifest denylist, reused
# ---------------------------------------------------------------------------

def redact_handoff_value(value: Any) -> Any:
    """Recursively redact a composed value with the EXISTING redactors.

    ``run_manifest.is_secret_key`` is the manifest denylist and
    ``stream_evidence`` owns the key/text redaction the evidence pipeline
    already trusts. A handoff quotes config values, next-intent payloads and
    decision commands verbatim, so it inherits both rather than growing a
    third redactor with its own blind spots.
    """
    from packages.orchestration.run_manifest import REDACTED, is_secret_key
    from packages.orchestration.stream_evidence import (
        is_sensitive_key,
        redact_text,
    )

    if isinstance(value, dict):
        return {
            str(k): (REDACTED if (is_secret_key(str(k)) or is_sensitive_key(k))
                     else redact_handoff_value(v))
            for k, v in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact_handoff_value(v) for v in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


# ---------------------------------------------------------------------------
# The sources
# ---------------------------------------------------------------------------

def _dossier_section(mission: Mission, root: Path | None,
                     gaps: list[HandoffGap]) -> dict[str, Any]:
    """The newest stored dossier text, via the dossier's OWN renderer."""
    from packages.orchestration.mission_dossier import (
        latest_dossier_version,
        load_dossier_state,
        newest_dossier_text,
    )

    version = latest_dossier_version(mission.project_id, mission.id, root)
    text = newest_dossier_text(mission.project_id, mission.id, root)
    if not text:
        gaps.append(HandoffGap(
            GAP_DOSSIER,
            "no dossier version is stored for this mission yet"))
        return {}
    state = load_dossier_state(mission.project_id, mission.id, root)
    return {
        "version": version,
        "text": text,
        "next_step": getattr(state, "next_step", "") if state else "",
        "over_budget": bool(getattr(state, "over_budget", False)) if state
        else False,
    }


def _load_job_for_decisions(job_id: str) -> Any:
    """The persisted job, or None. A job that cannot be read is a gap, not a raise."""
    from uuid import UUID

    from packages.orchestration.storage import load_job_safe

    try:
        job, _degraded = load_job_safe(UUID(str(job_id)))
    except (ValueError, TypeError):
        return None
    if job is not None:
        return job
    # A mission chain can hold non-UUID job ids (the plan-side record); the
    # plan is the other shape list_decisions already accepts.
    from packages.orchestration.pingpong_job import load_job_plan

    try:
        return load_job_plan(str(job_id))
    except Exception:  # noqa: BLE001 — an unreadable plan is a gap, not a crash
        return None


def _checkpoint_section(mission: Mission, gaps: list[HandoffGap],
                        ) -> dict[str, Any]:
    """The newest VERIFYING checkpoint of the mission's latest job."""
    from packages.orchestration.checkpoints import (
        AllCheckpointsCorruptError,
        load_latest_valid,
    )

    link = mission.latest_link()
    if link is None:
        gaps.append(HandoffGap(
            GAP_JOBS, "the mission has no job in its chain yet"))
        return {}
    try:
        checkpoint = load_latest_valid(link.job_id)
    except (AllCheckpointsCorruptError, OSError, ValueError) as exc:
        gaps.append(HandoffGap(
            GAP_CHECKPOINT,
            f"job {link.job_id} has checkpoints but none verifies: {exc}"))
        return {}
    if checkpoint is None:
        gaps.append(HandoffGap(
            GAP_CHECKPOINT, f"job {link.job_id} was never checkpointed"))
        return {}
    if not checkpoint.worktree_head:
        gaps.append(HandoffGap(
            GAP_WORKTREE_HEAD,
            f"checkpoint {checkpoint.cycle_index} of job {link.job_id} "
            "recorded no worktree head"))
    return {
        "job_id": checkpoint.job_id,
        "job_role": link.role,
        "cycle_index": checkpoint.cycle_index,
        "content_hash": checkpoint.content_hash,
        "worktree_head": checkpoint.worktree_head,
        "job_snapshot_path": checkpoint.job_snapshot_path,
        "job_snapshot_sha256": checkpoint.job_snapshot_sha256,
        "verify_result": checkpoint.verify_result,
        "verify_digest": checkpoint.verify_digest,
        "budget_spent_tokens": checkpoint.budget_spent_tokens,
        "created_at": checkpoint.created_at,
        "next_intent": dict(checkpoint.next_intent),
    }


def _open_decisions_section(mission: Mission, gaps: list[HandoffGap],
                            ) -> list[dict[str, Any]]:
    """Every still-open decision across the mission's chain, with its id."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.decision_queue import (
        list_decisions,
        open_decisions,
    )
    from packages.orchestration.timeline import load_run_events

    if not mission.job_links:
        return []
    data_root = resolve_data_root()
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    unreadable: list[str] = []
    for link in mission.job_links:
        job = _load_job_for_decisions(link.job_id)
        if job is None:
            unreadable.append(link.job_id)
            continue
        try:
            events = load_run_events(data_root, link.job_id)
        except (OSError, ValueError):
            events = []
        for decision in open_decisions(list_decisions(job, events)):
            if decision.id in seen:
                continue
            seen.add(decision.id)
            # No ``created_at``: a DERIVED decision (a stop reason, say) is
            # minted at derivation time, so carrying its timestamp would make
            # two builds of unchanged state differ. The id, type and answer
            # command are what a successor context acts on anyway.
            rows.append({
                "id": decision.id,
                "job_id": link.job_id,
                "type": decision.type,
                "severity": decision.severity,
                "summary": decision.safe_summary,
                "next_actions": list(decision.next_actions),
            })
    if unreadable:
        gaps.append(HandoffGap(
            GAP_OPEN_DECISIONS,
            "decisions could not be read for job(s): "
            + ", ".join(sorted(unreadable))))
    return rows


def _next_intent_section(checkpoint: dict[str, Any], dossier: dict[str, Any],
                         gaps: list[HandoffGap]) -> dict[str, Any]:
    """What the mission was about to do, from the most specific source that has it.

    The checkpoint's ``next_intent`` is what the RUN recorded; the dossier's
    next step is what the mission narrated. The checkpoint wins when both
    exist, and its origin is always stated — a successor context must be able
    to tell a recorded intent from a narrated one.
    """
    intent = dict(checkpoint.get("next_intent") or {})
    if intent:
        return {"source": "checkpoint", "intent": intent}
    next_step = str(dossier.get("next_step") or "")
    if next_step:
        return {"source": "dossier", "intent": {"next_step": next_step}}
    gaps.append(HandoffGap(
        GAP_NEXT_INTENT,
        "neither the checkpoint nor the dossier records a next step"))
    return {}


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------

def compose_handoff_body(mission: Mission, root: Path | None = None,
                         ) -> dict[str, Any]:
    """The handoff as data: every source that exists, every one that does not.

    Derived from the sources ALONE. No wall-clock read happens anywhere in
    here, which is what makes two builds on unchanged state byte-identical.
    """
    gaps: list[HandoffGap] = []
    dossier = _dossier_section(mission, root, gaps)
    checkpoint = _checkpoint_section(mission, gaps)
    decisions = _open_decisions_section(mission, gaps)
    next_intent = _next_intent_section(checkpoint, dossier, gaps)
    body: dict[str, Any] = {
        "schema_version": HANDOFF_SCHEMA_VERSION,
        "mission_id": mission.id,
        "project_id": mission.project_id,
        "goal": mission.goal,
        "status": mission.status,
        "dossier": dossier,
        "checkpoint": checkpoint,
        "open_decisions": decisions,
        "next_intent": next_intent,
        "gaps": [gap.to_json() for gap in gaps],
        "provenance": {
            "mission_created_at": mission.created_at,
            "job_ids": list(mission.job_ids()),
            "dossier_version": dossier.get("version", 0),
            "checkpoint_created_at": checkpoint.get("created_at", ""),
            "checkpoint_content_hash": checkpoint.get("content_hash", ""),
        },
    }
    return redact_handoff_value(body)


def handoff_body_bytes(body: dict[str, Any]) -> str:
    """The body's canonical text — sorted keys, one trailing newline."""
    return json.dumps(body, indent=2, sort_keys=True) + "\n"


def render_handoff(body: dict[str, Any]) -> str:
    """The prompt block a successor context reads: fixed order, dossier first."""
    dossier = body.get("dossier") or {}
    checkpoint = body.get("checkpoint") or {}
    decisions = body.get("open_decisions") or []
    next_intent = body.get("next_intent") or {}
    gaps = body.get("gaps") or []
    provenance = body.get("provenance") or {}

    parts: list[str] = [
        f"# Handoff — mission {body.get('mission_id', '')}",
        "",
        f"Goal: {body.get('goal', '')}",
        f"Status: {body.get('status', '')}",
        f"Schema version: {body.get('schema_version', '')}",
    ]
    bodies: dict[str, str] = {}

    bodies["Dossier"] = (str(dossier.get("text") or "").rstrip("\n")
                         if dossier else "(gap: no dossier stored)")
    if checkpoint:
        bodies["Checkpoint"] = "\n".join([
            f"- job: {checkpoint.get('job_id', '')} "
            f"(role {checkpoint.get('job_role', '')})",
            f"- cycle: {checkpoint.get('cycle_index', '')}",
            f"- content hash: {checkpoint.get('content_hash', '')}",
            f"- worktree head: {checkpoint.get('worktree_head', '') or '(none recorded)'}",
            f"- job snapshot: {checkpoint.get('job_snapshot_path', '') or '(none)'} "
            f"{checkpoint.get('job_snapshot_sha256', '')}".rstrip(),
            f"- verify: {checkpoint.get('verify_result', '') or '(none)'}",
        ])
    else:
        bodies["Checkpoint"] = "(gap: no verifying checkpoint)"

    if decisions:
        lines = []
        for d in decisions:
            lines.append(f"- [{d.get('severity', '')}] {d.get('type', '')} "
                         f"{d.get('id', '')}: {d.get('summary', '')}")
            for action in d.get("next_actions") or []:
                lines.append(f"    -> {action}")
        bodies["Open decisions"] = "\n".join(lines)
    else:
        bodies["Open decisions"] = "(none open)"

    if next_intent:
        intent = next_intent.get("intent") or {}
        bodies["Next intent"] = "\n".join(
            [f"Source: {next_intent.get('source', '')}"]
            + [f"- {k}: {v}" for k, v in sorted(intent.items())])
    else:
        bodies["Next intent"] = "(gap: no next intent recorded)"

    bodies["Gaps"] = ("\n".join(f"- {g.get('source', '')}: {g.get('detail', '')}"
                                for g in gaps) if gaps else "(none)")
    bodies["Provenance"] = "\n".join(
        f"- {k}: {v}" for k, v in sorted(provenance.items()))

    for name in HANDOFF_SECTIONS:
        parts.extend(["", f"## {name}", "", bodies[name]])
    return "\n".join(parts) + "\n"


def build_handoff(mission_id: str, root: Path | None = None) -> Path:
    """Compose this mission's handoff and return the path to its body.

    Idempotent per state: when the newest stored handoff already holds exactly
    these bytes, that file is returned untouched — a boundary reached twice
    without progress must not leave two accounts of the same moment. Changed
    state writes the next version beside it, so the newest is the highest.
    """
    mission = find_mission_record(mission_id, root)
    if mission is None:
        raise MissionForHandoffNotFoundError(str(mission_id))

    body = compose_handoff_body(mission, root)
    text = handoff_body_bytes(body)
    rendered = render_handoff(body)

    latest = latest_handoff_version(mission.project_id, mission.id, root)
    if latest:
        current = handoff_path(mission.project_id, mission.id, latest, root)
        try:
            if current.read_text(encoding="utf-8") == text:
                return current
        except OSError:  # unreadable newest: write the next version rather than
            pass         # overwrite bytes nobody could compare

    version = latest + 1
    path = handoff_path(mission.project_id, mission.id, version, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    handoff_render_path(mission.project_id, mission.id, version, root).write_text(
        rendered, encoding="utf-8")
    return path

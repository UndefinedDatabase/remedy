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

CONSUMPTION (T002) lives at the bottom of this module: the newest handoff
whose ``schema_version`` this build knows becomes the seed for iteration one
of a RESUMED mission, and its checkpoint reference is verified with the
CHECKPOINT feature's own rules before the narrative is trusted — a worktree
that has moved refuses with ``checkpoints.worktree_drift_message``, not with
a second wording of the same refusal.

**Remedy deliberately does NOT detect context pressure in flight.** There is
no watcher that notices a context window filling up and builds a handoff on
its own: v1's boundaries are the ones someone can name — the explicit
``remedy mission handoff`` command and the loop terminating for its limits or
for a stop. Automatic in-flight detection is out of scope for F079 (T1_F079.md
"Do not touch"), so a search for it lands here and finds the reason.

ROOT DISCIPLINE (R-0203). One root answers for every source. ``root`` selects
the mission area (record, dossier, evidence output); the job-side sources
(checkpoints, job records, run events) resolve the data root the product
resolves, ``data_paths.resolve_data_root()``. Passing a ``root`` that is not
the resolved data root therefore composes a mission from one world and its
jobs from another. Callers that isolate — tests, the gauntlet runner — set
``REMEDY_DATA_DIR`` to that same directory, which is what makes the two
agree; :func:`handoff_root_conflict` names the mismatch when they do not.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.mission_state import (
    Mission,
    list_missions_safe,
    mission_evidence_dir,
    project_ids_with_missions,
)

_log = logging.getLogger(__name__)

#: Bumped only when the composed body's SHAPE changes. A consumer that reads a
#: version it does not know REFUSES rather than guesses (see
#: :func:`read_handoff`).
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


# ---------------------------------------------------------------------------
# T002 — consumption: seeding a fresh context from a handoff
# ---------------------------------------------------------------------------

class HandoffSchemaVersionError(HandoffError):
    """The stored handoff carries a schema version this build does not know.

    Refusing is the point: a consumer that guessed at an unknown shape would
    hand a successor context a narrative assembled from fields it misread.
    """

    def __init__(self, path: Path, found: Any) -> None:
        super().__init__(
            f"{path} carries handoff schema_version {found!r}; this build "
            f"knows {HANDOFF_SCHEMA_VERSION} and refuses to guess")
        self.path = path
        self.found = found


class HandoffReferenceStaleError(HandoffError):
    """The handoff's checkpoint reference no longer describes the world."""


@dataclass(frozen=True)
class HandoffSeed:
    """One consumable handoff: where it came from, what it says."""

    path: Path
    body: dict[str, Any]
    text: str

    @property
    def version(self) -> int:
        return int(self.path.stem.rsplit("_v", 1)[-1] or 0)


def handoff_root_conflict(root: Path | None) -> str:
    """R-0203: name the mismatch when ``root`` and the data root disagree.

    Returns "" when they agree (or when no ``root`` was passed, which means
    "use the resolved one for everything"). The caller decides what a
    mismatch is worth — composition still works, but the mission and its jobs
    would come from two different worlds, and a silent split is the failure
    mode this exists to make visible.
    """
    if root is None:
        return ""
    from packages.orchestration.data_paths import resolve_data_root

    resolved = resolve_data_root()
    if Path(root).resolve() == Path(resolved).resolve():
        return ""
    return (f"mission sources resolve under {root} while job sources resolve "
            f"under {resolved}; set REMEDY_DATA_DIR to the mission root so "
            f"one root answers for both (R-0203)")


def read_handoff(path: Path) -> dict[str, Any]:
    """One stored handoff body, or a refusal. Never a guess."""
    body = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(body, dict):
        raise HandoffSchemaVersionError(Path(path), None)
    found = body.get("schema_version")
    if found != HANDOFF_SCHEMA_VERSION:
        raise HandoffSchemaVersionError(Path(path), found)
    return body


def verify_handoff_references(body: dict[str, Any]) -> None:
    """Check the handoff's checkpoint reference against the world it names.

    The CHECKPOINT feature's own rules do the checking: its loader decides
    what a valid checkpoint is, ``resolve_live_worktree_head`` reads the head
    that exists right now, and a drift refuses with
    ``checkpoints.worktree_drift_message`` — the same sentence
    ``remedy job resume`` prints. A handoff with no checkpoint reference (a
    named gap) has nothing to verify and passes: an absent claim cannot be
    stale.
    """
    from packages.orchestration.checkpoints import (
        AllCheckpointsCorruptError,
        load_latest_valid,
        resolve_live_worktree_head,
        worktree_drift_message,
    )

    checkpoint = body.get("checkpoint") or {}
    job_id = str(checkpoint.get("job_id", ""))
    if not job_id:
        return
    try:
        current = load_latest_valid(job_id)
    except AllCheckpointsCorruptError as exc:
        raise HandoffReferenceStaleError(
            f"no usable checkpoint for job {job_id} — "
            f"{len(exc.paths)} checkpoint(s) failed hash verification "
            f"({', '.join(exc.paths)}). They are kept on disk for "
            f"inspection.") from exc
    if current is None:
        raise HandoffReferenceStaleError(
            f"the handoff references a checkpoint of job {job_id}, but the "
            f"job has no verifying checkpoint any more")
    recorded_head = str(checkpoint.get("worktree_head", ""))
    if not recorded_head:
        return
    live_head = resolve_live_worktree_head(job_id)
    if live_head and live_head != recorded_head:
        raise HandoffReferenceStaleError(
            worktree_drift_message(recorded_head, live_head))


def latest_valid_handoff(mission_id: str, root: Path | None = None,
                         ) -> HandoffSeed | None:
    """The newest handoff this build can read, or None when there is none.

    Newest-first, exactly the way the checkpoint loader walks its own files:
    a handoff whose bytes cannot be read is skipped and logged, and the walk
    continues to the one before it. An unknown ``schema_version`` is NOT
    skipped — it is refused, because reading past a shape this build does not
    understand would silently resume a mission from an older account.
    """
    mission = find_mission_record(mission_id, root)
    if mission is None:
        raise MissionForHandoffNotFoundError(str(mission_id))
    versions = handoff_versions(mission.project_id, mission.id, root)
    for version in reversed(versions):
        path = handoff_path(mission.project_id, mission.id, version, root)
        try:
            body = read_handoff(path)
        except (OSError, ValueError) as exc:
            _log.warning("mission %s: handoff %s is unreadable — skipped, "
                         "kept on disk: %s", mission_id, path.name, exc)
            continue
        rendered = handoff_render_path(mission.project_id, mission.id,
                                       version, root)
        try:
            text = rendered.read_text(encoding="utf-8")
        except OSError:
            # The prompt block is a RENDERING of the body; re-render rather
            # than resume without one.
            text = render_handoff(body)
        _log.info("mission %s: resuming from %s", mission_id, path.name)
        return HandoffSeed(path=path, body=body, text=text)
    return None


def handoff_resume_seed(mission_id: str, root: Path | None = None, *,
                        verify: bool = True) -> HandoffSeed | None:
    """The seed a resumed mission's FIRST iteration starts from, or None.

    Verification comes BEFORE the narrative is handed on: a stale checkpoint
    reference raises :class:`HandoffReferenceStaleError` with the checkpoint
    feature's own message rather than seeding a context that describes a
    worktree nobody is standing on.
    """
    conflict = handoff_root_conflict(root)
    if conflict:
        _log.warning("mission %s: %s", mission_id, conflict)
    seed = latest_valid_handoff(mission_id, root)
    if seed is None:
        return None
    if verify:
        verify_handoff_references(seed.body)
    return seed


# ---------------------------------------------------------------------------
# T003 — the boundary recall eval: recall is MEASURED across the boundary
# ---------------------------------------------------------------------------

#: Where one mission's archived boundary-recall measurement lives — beside the
#: handoffs it measures, in the mission's own evidence area.
RECALL_REPORT_FILENAME = "handoff_recall_eval.md"

#: The threshold, inherited rather than invented: the dossier's own harness
#: documents it as "Open facts must all be answerable. Resolved ones MAY
#: compress away" (``mission_dossier.run_recall_harness`` docstring, pinned by
#: ``RecallResult.recalled_all_open`` and by
#: ``tests/orchestration/test_mission_dossier.py`` — the open/resolved
#: asymmetry). A handoff that carries the dossier forward inherits the same
#: bar: EVERY open fact, none missing.
RECALL_THRESHOLD_OPEN_ITEMS = 1.0


@dataclass(frozen=True)
class BoundaryRecallResult:
    """What survived a real boundary, per fact — never a single pass/fail word."""

    seed_path: Path
    report_path: Path
    #: Open facts findable in the handoff seed ALONE. The acceptance set.
    answerable: tuple[str, ...] = ()
    #: Open facts that are NOT findable. Any entry is a defect.
    missing: tuple[str, ...] = ()
    #: Resolved facts the dossier compressed away — allowed, and the point.
    compressed_away: tuple[str, ...] = ()

    @property
    def open_recall(self) -> float:
        total = len(self.answerable) + len(self.missing)
        return 1.0 if not total else len(self.answerable) / total


def run_boundary_recall_eval(mission_id: str, root: Path | None = None, *,
                             call_fn: Any = None,
                             facts: Any = None) -> BoundaryRecallResult:
    """Seed facts, cross a REAL boundary, and measure what a fresh context gets.

    The measurement reuses the dossier's harness verbatim —
    ``mission_dossier.run_recall_harness`` over ``RECALL_FIXTURE_FACTS``, and
    ``recall_report`` for the numbers — so this eval measures the HANDOFF, not
    a second opinion about dossiers. The harness produces the document; this
    function stores it as the mission's dossier, forces the boundary by
    building the handoff, and then asks the acceptance question: with nothing
    but the handoff seed a resumed context would receive, which seeded facts
    are still findable?

    Open facts must all survive; resolved ones may have compressed away (the
    dossier's own asymmetry — see :data:`RECALL_THRESHOLD_OPEN_ITEMS`). The
    report is archived in the mission's evidence area, where it is closure
    evidence rather than a number in a test log.
    """
    from packages.orchestration.mission_dossier import (
        RECALL_FIXTURE_FACTS,
        recall_report,
        run_recall_harness,
        save_dossier_state,
        write_dossier_version,
    )

    mission = find_mission_record(mission_id, root)
    if mission is None:
        raise MissionForHandoffNotFoundError(str(mission_id))
    seeded = tuple(facts if facts is not None else RECALL_FIXTURE_FACTS)

    measured = run_recall_harness(seeded, goal=mission.goal, call_fn=call_fn)
    write_dossier_version(mission.project_id, mission.id, measured.dossier, root)
    save_dossier_state(mission.project_id, mission.id, measured.dossier, root)

    build_handoff(mission.id, root)
    seed = handoff_resume_seed(mission.id, root)
    if seed is None:  # pragma: no cover — build_handoff just wrote one
        raise HandoffError(
            f"mission {mission.id} has no readable handoff after building one")

    open_ids = [f.id for f in seeded if not f.resolved]
    resolved_ids = [f.id for f in seeded if f.resolved]
    result = BoundaryRecallResult(
        seed_path=seed.path,
        report_path=mission_evidence_dir(mission.project_id, mission.id, root)
        / RECALL_REPORT_FILENAME,
        answerable=tuple(i for i in open_ids if i in seed.text),
        missing=tuple(i for i in open_ids if i not in seed.text),
        compressed_away=tuple(i for i in resolved_ids if i not in seed.text),
    )
    report = "\n".join([
        f"# Boundary recall eval — mission {mission.id}",
        "",
        f"seeded facts:    {len(seeded)} "
        f"({len(open_ids)} open, {len(resolved_ids)} resolved)",
        f"boundary:        {seed.path.name}",
        f"threshold:       {RECALL_THRESHOLD_OPEN_ITEMS:.0%} of OPEN items "
        f"(inherited from the dossier harness)",
        f"open recall:     {result.open_recall:.0%} "
        f"({', '.join(result.answerable) or 'none'})",
        f"open missing:    {len(result.missing)} "
        f"({', '.join(result.missing) or 'none'})",
        f"compressed away: {len(result.compressed_away)} "
        f"({', '.join(result.compressed_away) or 'none'})",
        "",
        "## The dossier the boundary carried",
        "",
        recall_report(measured),
    ]) + "\n"
    result.report_path.parent.mkdir(parents=True, exist_ok=True)
    result.report_path.write_text(report, encoding="utf-8")
    return result

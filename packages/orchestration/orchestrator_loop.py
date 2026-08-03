"""F070 — the orchestrator loop: Remedy running its own missions.

The external orchestrator's working style — read the state, decide the next
order, dispatch it, evaluate the result, write everything down — internalized.
Per iteration: assemble the context, take ONE schema-validated
:class:`~packages.orchestration.orchestrator_move_schema.OrchestratorMove` from
the orchestrator-role provider, execute it through Remedy's EXISTING verbs,
evaluate, update the mission, and append a ledger entry a human can audit.

**This module is a POLICY layer (Rule A6).** It sequences verbs; it does not
reimplement them. Every verb it calls is named in `.agent/decisions.md`'s F070
verb map: `mission_state.continue_mission` dispatches, `long_run_executor`
executes, `dod_gate` evaluates, `run_report` reports, `escalation` escalates,
`safe_points` stops. A diff here that grows its own intake, executor, DoD
mechanism, reporter or escalator is a defect, not a feature.

Remedy deliberately does NOT let this loop grant itself new goals. That is not
a rule written in the prompt — it is the shape of the move schema, which has no
kind for creating a mission or editing a goal. See
``orchestrator_move_schema`` for the boundary and why it lives there.

Three disciplines this module holds to:

* **Cache-stable prefix.** The dossier is assembled FIRST and is byte-stable
  while the mission does not change, so a provider's prompt cache survives
  across iterations. Volatile sections come after it, never before.
* **Human overrides win instantly.** A stop request and the mission's open
  decisions are read EVERY iteration, at the safe point between iterations —
  so a stop lands within one iteration rather than at the end of a run.
* **The ledger is the account.** One append-only entry per iteration carrying
  the iteration number, the context digest, the move, the outcome and the
  measured cost. Unmeasured cost is recorded as unmeasured; nothing is
  estimated into the record and passed off as an actual.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.mission_state import (
    MISSION_STATUS_ACHIEVED,
    mission_evidence_dir,
)
from packages.orchestration.orchestrator_move_schema import (
    ORCHESTRATOR_MOVE_SCHEMA_V,
)

# ---------------------------------------------------------------------------
# The protocol document — read, never written
# ---------------------------------------------------------------------------

#: Bump together with any change to what the protocol document ASKS the
#: orchestrator to do. Every ledger entry records the version it ran under, so
#: an audit can tell which contract a past decision was made against.
PROTOCOL_VERSION = "v1"

#: Where the protocol document lives, relative to the repo root. The location
#: is recorded in `.agent/decisions.md`; keeping it under ``docs/agents/``
#: puts the orchestrator's job description beside the human roles' own.
PROTOCOL_DOC_RELATIVE = "docs/agents/orchestrator_protocol.md"


def _repo_root() -> Path:
    """This repository's root, derived from this file's own location."""
    return Path(__file__).resolve().parents[2]


def protocol_document_path(repo_root: Path | None = None) -> Path:
    """Absolute path of the versioned protocol document."""
    return (repo_root or _repo_root()) / PROTOCOL_DOC_RELATIVE


def orchestrator_protocol_text(repo_root: Path | None = None) -> str:
    """The protocol document's text.

    Remedy deliberately does NOT provide a writer for this file. Runtime
    self-modification of the protocol is in F070's Do-not-touch list, so the
    absence of a write path here is the enforcement, not an omission: the loop
    reads its job description and cannot edit it.
    """
    return protocol_document_path(repo_root).read_text(encoding="utf-8")


def build_orchestrator_system_prompt(repo_root: Path | None = None) -> str:
    """The orchestrator role's system-prompt block, GENERATED from the document.

    Nothing about the orchestrator's instructions is authored in code — change
    the document and the prompt changes with it, as a reviewable diff.
    """
    return (
        f"# Orchestrator protocol {PROTOCOL_VERSION}\n"
        f"# Source: {PROTOCOL_DOC_RELATIVE} (versioned in the repository)\n\n"
        f"{orchestrator_protocol_text(repo_root)}"
    )


# ---------------------------------------------------------------------------
# Context assembly — dossier FIRST
# ---------------------------------------------------------------------------

#: Section headings, in assembly order. The dossier leads so the stable part of
#: the prompt is the prefix; everything after it may change every iteration.
SECTION_DOSSIER = "## Mission dossier"
SECTION_PLAN = "## Mission plan state"
SECTION_REPORT = "## Last report"
SECTION_DECISIONS = "## Open decisions"

#: What the stand-in dossier says about itself. F071 (Mission dossier) is not
#: built; ``Mission.dossier_ref`` is documented as RESERVED and is empty on
#: every record. Rather than invent that document here — which would be the
#: second mechanism A6 forbids — the loop renders the facts the mission record
#: ALREADY holds and labels the result for what it is.
DOSSIER_STANDIN_NOTE = (
    "(stand-in: rendered from the mission record. The maintained dossier "
    "document is F071 and does not exist yet.)")


def render_mission_dossier(mission: Any, *, done_milestones: Sequence[str] = ()) -> str:
    """The stand-in dossier: the mission's own facts, deterministically rendered.

    Deterministic on purpose — no clock, no disk, no randomness — because this
    text is the cache-stable prefix of every orchestrator prompt. The same
    mission state renders to the same bytes, so a provider's prompt cache is
    only invalidated when something actually changed.
    """
    from packages.orchestration.mission_compiler import mission_plan_of

    plan = mission_plan_of(mission)
    done = tuple(done_milestones)
    lines = [
        f"Mission: {getattr(mission, 'id', '')}",
        f"Status: {getattr(mission, 'status', '')}",
        f"Goal: {' '.join(str(getattr(mission, 'goal', '')).split())}",
    ]
    if plan is None:
        lines.append("Plan: not compiled yet.")
    else:
        lines.append(
            f"Plan: {len(plan.milestones)} milestone(s), origin {plan.origin}"
            f"{'' if plan.compiled else ' (degraded — no provider compiled it)'}"
            f"; {len(done)} done.")
        for ms in plan.milestones:
            deps = ", ".join(ms.depends_on) if ms.depends_on else "none"
            mark = "done" if ms.id in done else "open"
            lines.append(f"- {ms.id} [{mark}] depends_on: {deps} — {ms.goal}")
    lines.append(f"Jobs linked: {len(getattr(mission, 'job_links', ()) or ())}")
    lines.append(DOSSIER_STANDIN_NOTE)
    return "\n".join(lines)


def render_plan_state(mission: Any, *, done_milestones: Sequence[str] = ()) -> str:
    """Which milestones are reachable now, given what is already done."""
    from packages.orchestration.mission_compiler import mission_plan_of

    plan = mission_plan_of(mission)
    if plan is None:
        return "No compiled plan. Nothing can be dispatched."
    done = set(done_milestones)
    lines: list[str] = []
    for ms in plan.milestones:
        if ms.id in done:
            state = "done"
        elif set(ms.depends_on) - done:
            blocked = ", ".join(sorted(set(ms.depends_on) - done))
            state = f"blocked on {blocked}"
        else:
            state = "ready"
        lines.append(f"- {ms.id}: {state}")
    return "\n".join(lines) or "No milestones."


@dataclass(frozen=True)
class OrchestratorContext:
    """One iteration's assembled context plus the digest that identifies it."""

    text: str
    digest: str
    #: Section name -> body, in assembly order. Kept so a caller can inspect
    #: what went into the prompt without re-parsing the rendered text.
    sections: tuple[tuple[str, str], ...] = ()


def context_digest(text: str) -> str:
    """A stable identifier for one assembled context, for the ledger."""
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def assemble_context(
    mission: Any,
    *,
    done_milestones: Sequence[str] = (),
    dossier: Callable[[Any], str] | None = None,
    last_report: str = "",
    open_decisions: Iterable[Any] = (),
) -> OrchestratorContext:
    """Assemble one iteration's context: dossier FIRST, then the volatile parts.

    ``dossier`` is the seam F071 plugs into. Given one, it renders the mission's
    dossier; absent, :func:`render_mission_dossier` renders the stand-in from
    the mission record. A non-empty ``Mission.dossier_ref`` is reported so a
    reader can see which document a decision was made against.
    """
    if dossier is not None:
        dossier_text = dossier(mission)
    else:
        dossier_text = render_mission_dossier(
            mission, done_milestones=done_milestones)
    ref = str(getattr(mission, "dossier_ref", "") or "")
    if ref:
        dossier_text = f"Dossier ref: {ref}\n{dossier_text}"

    decisions = list(open_decisions)
    if decisions:
        decision_text = "\n".join(
            f"- {_decision_line(d)}" for d in decisions)
    else:
        decision_text = "None open."

    sections = (
        (SECTION_DOSSIER, dossier_text),
        (SECTION_PLAN, render_plan_state(
            mission, done_milestones=done_milestones)),
        (SECTION_REPORT, last_report.strip() or "No report yet."),
        (SECTION_DECISIONS, decision_text),
    )
    text = "\n\n".join(f"{name}\n\n{body}" for name, body in sections) + "\n"
    return OrchestratorContext(
        text=text, digest=context_digest(text), sections=sections)


def _decision_line(record: Any) -> str:
    """One open decision, rendered for the prompt."""
    if isinstance(record, dict):
        ident = record.get("id") or record.get("decision_id") or "?"
        question = record.get("question") or record.get("summary") or ""
        return f"{ident}: {' '.join(str(question).split())}".strip().rstrip(":")
    return " ".join(str(record).split())


def open_mission_decisions(mission: Any) -> list[dict[str, Any]]:
    """Every OPEN escalation across the mission's linked jobs, in chain order.

    Read fresh every iteration through the existing escalation verb — a human
    answering a decision between two iterations is picked up by the next one
    with no bookkeeping here.
    """
    from packages.orchestration.escalation import open_task_decisions
    from packages.orchestration.storage import load_job

    out: list[dict[str, Any]] = []
    for link in getattr(mission, "job_links", ()) or ():
        try:
            job = load_job(_as_uuid(link.job_id))
        except Exception:
            # A job that cannot be read cannot be asked about its decisions.
            # Recorded as absent rather than raised: one unreadable job must
            # not make the whole mission undecidable.
            continue
        out.extend(open_task_decisions(job))
    return out


def _as_uuid(raw: Any) -> Any:
    from uuid import UUID

    return raw if isinstance(raw, UUID) else UUID(str(raw))


# ---------------------------------------------------------------------------
# The decision ledger — append-only
# ---------------------------------------------------------------------------

#: One line per iteration, in the mission's own evidence area. JSONL because
#: the file is APPENDED to and must stay readable after a process dies
#: mid-write: a torn last line costs one entry, never the whole history.
LEDGER_FILENAME = "ledger.jsonl"

#: What ``cost.usage_source`` says when nothing measured the call. P6: an
#: unmeasured cost is reported as unmeasured, never estimated into an actual.
USAGE_UNMEASURED = "unmeasured"


def ledger_path(project_id: str, mission_id: str,
                root: Path | None = None) -> Path:
    """Where one mission's decision ledger lives."""
    return mission_evidence_dir(project_id, mission_id, root) / LEDGER_FILENAME


@dataclass(frozen=True)
class LedgerEntry:
    """One iteration's account. Everything a human needs to audit the decision."""

    iteration: int
    context_digest: str
    move: dict[str, Any]
    outcome: dict[str, Any]
    cost: dict[str, Any] = field(default_factory=dict)
    protocol_version: str = PROTOCOL_VERSION
    recorded_at: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "iteration": self.iteration,
            "context_digest": self.context_digest,
            "move": dict(self.move),
            "outcome": dict(self.outcome),
            "cost": dict(self.cost),
            "protocol_version": self.protocol_version,
            "recorded_at": self.recorded_at,
        }


def _utc_now_iso(now: datetime | None = None) -> str:
    return (now or datetime.now(timezone.utc)).isoformat()


def append_ledger_entry(project_id: str, mission_id: str, entry: LedgerEntry,
                        root: Path | None = None,
                        *, now: datetime | None = None) -> Path:
    """Append one entry. Never rewrites, never truncates, never reorders.

    Append-only is the point: a ledger a later iteration could edit would prove
    nothing about the iterations before it.
    """
    path = ledger_path(project_id, mission_id, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = entry.to_json()
    if not body["recorded_at"]:
        body["recorded_at"] = _utc_now_iso(now)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(body, sort_keys=True) + "\n")
    return path


def read_ledger(project_id: str, mission_id: str,
                root: Path | None = None) -> list[dict[str, Any]]:
    """Every entry, in order. A torn or unreadable line is SKIPPED, not raised.

    A ledger is forensic evidence: one bad line must not make the other
    entries unreadable. Skipped lines are visible by their absent iteration
    numbers, which is the honest signal.
    """
    path = ledger_path(project_id, mission_id, root)
    if not path.is_file():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        try:
            body = json.loads(text)
        except ValueError:
            continue
        if isinstance(body, dict):
            entries.append(body)
    return entries


def render_ledger(entries: Sequence[dict[str, Any]]) -> str:
    """The audit trail as a human reads it — every decision, without the code.

    The acceptance bar for this renderer is that a reader can reconstruct what
    the loop decided and why WITHOUT opening a source file, so every entry
    prints its move, its payload, its outcome and its cost.
    """
    if not entries:
        return "No ledger entries."
    lines: list[str] = []
    for body in entries:
        move = body.get("move") or {}
        outcome = body.get("outcome") or {}
        cost = body.get("cost") or {}
        lines.append(
            f"[{body.get('iteration', '?')}] {move.get('kind', 'unknown')} "
            f"-> {outcome.get('status', 'unknown')}")
        if move.get("rationale"):
            lines.append(f"    why: {move['rationale']}")
        payload = move.get("payload") or {}
        for key in sorted(payload):
            lines.append(f"    {key}: {payload[key]}")
        if outcome.get("detail"):
            lines.append(f"    outcome: {outcome['detail']}")
        usage = cost.get("usage")
        if usage:
            lines.append(
                f"    cost: {cost.get('calls', 0)} call(s), "
                f"{usage.get('input_tokens', 0)} in / "
                f"{usage.get('output_tokens', 0)} out tokens")
        else:
            lines.append(
                f"    cost: {cost.get('calls', 0)} call(s), tokens "
                f"{cost.get('usage_source', USAGE_UNMEASURED)}")
        lines.append(f"    context: {body.get('context_digest', '')}")
        lines.append(f"    protocol: {body.get('protocol_version', '')}"
                     f"  at {body.get('recorded_at', '')}")
    return "\n".join(lines)


def measure_call_cost(outcome: Any) -> dict[str, Any]:
    """Cost actuals for one orchestrator call, measured or honestly absent.

    ``outcome`` is a
    :class:`~packages.orchestration.structured_outputs.StructuredOutcome`. When
    the raw response carries a usage block (the claude CLI's JSON envelope), the
    EXISTING parser reads it; otherwise the entry says the tokens were not
    measured. Remedy never writes an estimate into a field named ``usage``.
    """
    from packages.orchestration.token_actuals import parse_cli_result

    raw = str(getattr(outcome, "last_text", "") or "")
    actuals = parse_cli_result(raw) if raw else None
    cost: dict[str, Any] = {
        "calls": int(getattr(outcome, "calls", 0) or 0),
        "parse_retried": bool(getattr(outcome, "parse_retried", False)),
        "response_chars": len(raw),
        "schema_v": str(getattr(outcome, "schema_v", ORCHESTRATOR_MOVE_SCHEMA_V)),
    }
    if actuals is None:
        cost["usage"] = None
        cost["usage_source"] = USAGE_UNMEASURED
        return cost
    cost["usage"] = {
        "input_tokens": actuals.input_tokens,
        "output_tokens": actuals.output_tokens,
        "cache_read": actuals.cache_read,
        "cache_creation": actuals.cache_creation,
        "total_cost_usd": actuals.total_cost_usd,
    }
    cost["usage_source"] = "measured"
    return cost


# ---------------------------------------------------------------------------
# Milestone bookkeeping — persisted through the EXISTING mission-plan writer
# ---------------------------------------------------------------------------

#: Key the persisted plan body carries for milestones the loop marked done.
#: Underscore-prefixed like the flight-plan precedent's ``_version`` /
#: ``_versions``, which ``mission_compiler.mission_plan_of`` already strips —
#: so this is ADDITIVE, needs no MissionPlan schema change and no
#: MISSION_SCHEMA_VERSION bump.
MILESTONES_DONE_KEY = "_milestones_done"


def done_milestones(mission: Any) -> tuple[str, ...]:
    """Which milestones of the persisted plan are recorded as done."""
    body = getattr(mission, "mission_plan", None)
    if not isinstance(body, dict):
        return ()
    done = body.get(MILESTONES_DONE_KEY) or []
    if not isinstance(done, list):
        return ()
    return tuple(str(m) for m in done)


def mark_milestone_done(project_id: str, mission_id: str, milestone_id: str,
                        root: Path | None = None) -> Any:
    """Record a milestone as done, through the existing ``set_mission_plan``.

    No second persistence mechanism (A6): the milestone list rides on the plan
    body the mission record already stores, so one writer owns the record.
    """
    from packages.orchestration.mission_state import load_mission, set_mission_plan

    mission = load_mission(project_id, mission_id, root)
    body = dict(mission.mission_plan or {})
    if not body:
        raise ValueError(
            f"mission {mission_id} has no compiled plan, so milestone "
            f"{milestone_id!r} cannot be marked done")
    done = [str(m) for m in (body.get(MILESTONES_DONE_KEY) or [])]
    if milestone_id not in done:
        done.append(milestone_id)
    body[MILESTONES_DONE_KEY] = done
    return set_mission_plan(project_id, mission_id, body, root)


def milestone_ids(mission: Any) -> tuple[str, ...]:
    """Every milestone id of the persisted plan, in plan order."""
    from packages.orchestration.mission_compiler import mission_plan_of

    plan = mission_plan_of(mission)
    return () if plan is None else tuple(m.id for m in plan.milestones)


def all_milestones_done(mission: Any) -> bool:
    """True when the plan has milestones and every one of them is done."""
    ids = milestone_ids(mission)
    return bool(ids) and set(ids) <= set(done_milestones(mission))


def mission_achieved(project_id: str, mission_id: str,
                     root: Path | None = None) -> Any:
    """Set the mission to achieved through the existing status writer."""
    from packages.orchestration.mission_state import set_mission_status

    return set_mission_status(project_id, mission_id, MISSION_STATUS_ACHIEVED,
                              root)

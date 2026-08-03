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
* **The ledger is the account.** One append-only entry per iteration — added
  in the next commit of this slice, together with the milestone bookkeeping.
"""
from __future__ import annotations

import hashlib
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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

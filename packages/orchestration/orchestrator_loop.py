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
#: Present only on the ONE re-prompt that follows a refused move. Last, so a
#: refusal never disturbs the stable prefix in front of it.
SECTION_FEEDBACK = "## Your previous move was refused"

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
    feedback: str = "",
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
    if feedback.strip():
        sections = (*sections, (SECTION_FEEDBACK, feedback.strip()))
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


#: Where the rendered dossier snapshot is refreshed, in the mission's own
#: evidence area beside its plan and its ledger.
DOSSIER_FILENAME = "dossier.md"


def update_mission_dossier(project_id: str, mission_id: str, mission: Any,
                           root: Path | None = None) -> Path:
    """Refresh the mission's dossier. Called EVERY iteration.

    Until F071 lands this writes the rendered stand-in — a snapshot of what the
    mission record already says, labeled as a stand-in. It is a real write of a
    real file, not a placeholder that pretends to be one, and it deliberately
    does not claim F071's maintained-document semantics (a curated, token-
    budgeted narrative). ``Mission.dossier_ref``, when F071 fills it, is what a
    caller passes through the loop's ``dossier`` seam instead.
    """
    path = mission_evidence_dir(project_id, mission_id, root) / DOSSIER_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_mission_dossier(
            mission, done_milestones=done_milestones(mission)) + "\n",
        encoding="utf-8")
    return path


def mission_achieved(project_id: str, mission_id: str,
                     root: Path | None = None) -> Any:
    """Set the mission to achieved through the existing status writer."""
    from packages.orchestration.mission_state import set_mission_status

    return set_mission_status(project_id, mission_id, MISSION_STATUS_ACHIEVED,
                              root)


# ---------------------------------------------------------------------------
# Limits
# ---------------------------------------------------------------------------

#: Config key for the iteration bound. Conservative on purpose — an unattended
#: loop that mis-decides is cheaper to stop early than to let run.
CONFIG_KEY_MAX_ITERATIONS = "orchestrator.max_iterations"

#: Used when no config is readable at all. Matches the key's own default.
DEFAULT_MAX_ITERATIONS = 10


@dataclass(frozen=True)
class LoopLimits:
    """What bounds one ``run_mission`` invocation."""

    max_iterations: int = DEFAULT_MAX_ITERATIONS


def loop_limits_from_config(config: Any = None, *,
                            iterations_flag: int | None = None) -> LoopLimits:
    """Flag beats config beats default — the same precedence the executor uses."""
    if iterations_flag is not None:
        requested = int(iterations_flag)
    else:
        if config is None:
            from packages.orchestration.config import get_config

            config = get_config()
        value = config.get(CONFIG_KEY_MAX_ITERATIONS)
        requested = DEFAULT_MAX_ITERATIONS if value is None else int(value)
    if requested < 1:
        raise ValueError(f"max_iterations must be >= 1, got {requested}")
    return LoopLimits(max_iterations=requested)


# ---------------------------------------------------------------------------
# Terminals — every one of them an honest status
# ---------------------------------------------------------------------------

#: The mission goal is met and the record says so.
TERMINAL_ACHIEVED = "achieved"
#: The orchestrator gave up and recorded why.
TERMINAL_ABORTED = "aborted"
#: A human has to answer something before anything else can happen.
TERMINAL_WAITING = "waiting_on_decisions"
#: A stop request was pending at a safe point.
TERMINAL_STOPPED = "stopped"
#: The iteration bound was reached. A NORMAL terminal, not a failure — the
#: mission is simply not finished, and the status says exactly that.
TERMINAL_ITERATION_LIMIT = "iteration_limit"
#: There is no provider, so there is no decision to execute.
TERMINAL_NO_PROVIDER = "no_provider"
#: The provider answered, twice, with something that is not a valid move.
TERMINAL_INVALID_MOVE = "invalid_move"
#: The mission record is not active (paused, achieved or abandoned already).
TERMINAL_NOT_ACTIVE = "mission_not_active"


@dataclass(frozen=True)
class MoveOutcome:
    """What executing one move produced."""

    status: str
    detail: str = ""
    terminal: bool = False
    job_id: str = ""

    def to_json(self) -> dict[str, Any]:
        body: dict[str, Any] = {"status": self.status, "detail": self.detail}
        if self.job_id:
            body["job_id"] = self.job_id
        return body


@dataclass
class MissionRunResult:
    """What one ``run_mission`` invocation did."""

    mission_id: str
    project_id: str
    terminal: str
    detail: str = ""
    iterations: int = 0
    entries: list[LedgerEntry] = field(default_factory=list)


def resolve_mission_project(mission_id: str, root: Path | None = None) -> str:
    """Which project holds this mission.

    ``run_mission`` is specified as ``run_mission(mission_id, limits)`` — no
    project argument — so the project is looked up from the mission area on
    disk through the existing listing verbs. A caller that already knows it
    passes it and skips this entirely.
    """
    from packages.orchestration.mission_state import (
        MissionNotFoundError,
        list_missions_safe,
        project_ids_with_missions,
    )

    for project_id in project_ids_with_missions(root):
        missions, _degraded, _skipped = list_missions_safe(project_id, root)
        for mission in missions:
            if mission.id == mission_id:
                return project_id
    raise MissionNotFoundError(
        f"no project holds a mission with id {mission_id!r}")


def build_orchestrator_prompt(context: OrchestratorContext,
                              repo_root: Path | None = None) -> str:
    """The full prompt for one iteration: the generated protocol, then the state.

    The protocol block leads because it never changes within a run; the
    dossier-first context follows. Both halves of the prefix are therefore
    stable, which is what makes the cache discipline worth having.
    """
    return (f"{build_orchestrator_system_prompt(repo_root)}\n\n"
            f"# Mission state\n\n{context.text}")


def run_mission(
    mission_id: str,
    limits: LoopLimits | None = None,
    *,
    project_id: str | None = None,
    call_fn: Callable[[str, int], str] | None = None,
    root: Path | None = None,
    dossier: Callable[[Any], str] | None = None,
    dispatch: Callable[..., Any] | None = None,
    last_report: Callable[[Any], str] | None = None,
    evidence: Callable[[str, str, str], MilestoneEvidence] | None = None,
    escalate: Callable[[str, str, str], str] | None = None,
    update_dossier: Callable[[str, str, Any], Any] | None = None,
    control_root_path: Path | None = None,
    repo_root: Path | None = None,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    now: datetime | None = None,
) -> MissionRunResult:
    """Run one mission until it terminates, its limits run out, or it is stopped.

    One iteration is: safe point -> assemble context -> ONE provider call for a
    schema-validated move -> execute that move through the existing verbs ->
    append a ledger entry. The safe point is evaluated BEFORE any work of an
    iteration begins, so a stop request lands within one iteration and a human
    override never waits for the run to finish.

    Every move that would ADVANCE the mission is evaluated before it is
    executed. A refused move is recorded with its reason and the loop
    re-prompts ONCE with that reason as feedback; a second refusal in a row
    escalates to a human through the existing escalation verb. There is no
    third attempt and no silent retry loop.

    Seams, all defaulting to the production path:
      ``dispatch``        how a job is created for a milestone
                          (``mission_state.continue_mission``)
      ``dossier``         how the mission's dossier renders (F071 plugs in here)
      ``update_dossier``  the dossier refresh, called every iteration
      ``evidence``        how a milestone's job state, DoD gate and handback are
                          observed (:func:`collect_milestone_evidence`)
      ``escalate``        how a twice-refused move reaches a human
      ``last_report``     the account of the most recent dispatched job
      ``call_fn``         the orchestrator provider call; ``None`` means there
                          is no provider, which is a terminal, not an exception

    Every iteration leaves a ledger entry — including the ones that end the
    run — so the audit trail has no gaps where a decision used to be.
    """
    from packages.orchestration.mission_state import (
        MISSION_STATUS_ACTIVE,
        load_mission,
    )
    from packages.orchestration.orchestrator_move_schema import OrchestratorMove
    from packages.orchestration.safe_points import consume_stop, stop_requested
    from packages.orchestration.structured_outputs import run_structured_call

    bounds = limits or loop_limits_from_config()
    pid = project_id or resolve_mission_project(mission_id, root)
    result = MissionRunResult(mission_id=mission_id, project_id=pid,
                              terminal=TERMINAL_ITERATION_LIMIT)
    observe = evidence or (
        lambda p, m, ms: collect_milestone_evidence(p, m, ms, root))
    refresh = update_dossier or (
        lambda p, m, mission: update_mission_dossier(p, m, mission, root))
    hand_over = escalate or (
        lambda p, m, reason: escalate_repeated_refusal(p, m, reason, root=root,
                                                       now=now))
    #: Empty until a move is refused; carried into exactly ONE re-prompt.
    feedback = ""

    def _record(iteration: int, digest: str, move: dict[str, Any],
                outcome: MoveOutcome, cost: dict[str, Any]) -> None:
        entry = LedgerEntry(iteration=iteration, context_digest=digest,
                            move=move, outcome=outcome.to_json(), cost=cost)
        append_ledger_entry(pid, mission_id, entry, root, now=now)
        result.entries.append(entry)

    for iteration in range(1, bounds.max_iterations + 1):
        # ── safe point: human overrides win before any work of this iteration
        signal = stop_requested(mission_id, control_root_path=control_root_path)
        if signal is not None:
            consume_stop(mission_id, control_root_path=control_root_path)
            outcome = MoveOutcome(
                status=TERMINAL_STOPPED,
                detail=f"stop requested: {getattr(signal, 'reason', '')}".strip(),
                terminal=True)
            _record(iteration, "", {}, outcome, {"calls": 0,
                                                 "usage": None,
                                                 "usage_source": USAGE_UNMEASURED})
            result.terminal, result.detail = TERMINAL_STOPPED, outcome.detail
            result.iterations = iteration - 1
            return result

        mission = load_mission(pid, mission_id, root)
        if mission.status != MISSION_STATUS_ACTIVE:
            result.terminal = TERMINAL_NOT_ACTIVE
            result.detail = f"mission status is {mission.status}"
            result.iterations = iteration - 1
            return result

        # The dossier is refreshed BEFORE the context is assembled, so the
        # prompt's first section and the mission's own dossier file describe
        # the same state rather than drifting an iteration apart.
        refresh(pid, mission_id, mission)

        context = assemble_context(
            mission,
            done_milestones=done_milestones(mission),
            dossier=dossier,
            last_report=last_report(mission) if last_report else "",
            open_decisions=open_mission_decisions(mission),
            feedback=feedback)
        result.iterations = iteration

        if call_fn is None:
            outcome = MoveOutcome(
                status=TERMINAL_NO_PROVIDER,
                detail="no orchestrator provider is configured, so no move "
                       "was decided",
                terminal=True)
            _record(iteration, context.digest, {}, outcome,
                    {"calls": 0, "usage": None,
                     "usage_source": USAGE_UNMEASURED})
            result.terminal, result.detail = TERMINAL_NO_PROVIDER, outcome.detail
            return result

        call = run_structured_call(
            OrchestratorMove,
            build_orchestrator_prompt(context, repo_root),
            call_fn,
            on_call=on_call,
            allow_parse_retry=True)
        cost = measure_call_cost(call)

        if not call.ok:
            outcome = MoveOutcome(
                status=TERMINAL_INVALID_MOVE,
                detail=f"parse-class failure: {call.hint}".strip(),
                terminal=True)
            _record(iteration, context.digest, {}, outcome, cost)
            result.terminal, result.detail = TERMINAL_INVALID_MOVE, outcome.detail
            return result

        move: OrchestratorMove = call.value
        refusal = evaluate_move(mission, move, observe=observe,
                                project_id=pid, mission_id=mission_id)

        if refusal:
            if not feedback:
                # First refusal: record it and re-prompt ONCE with the reason.
                _record(iteration, context.digest, move.model_dump(),
                        MoveOutcome(status=OUTCOME_REFUSED, detail=refusal),
                        cost)
                feedback = refusal
                continue
            # Second refusal in a row: a human decides, never another retry.
            handle = hand_over(pid, mission_id, refusal)
            outcome = MoveOutcome(
                status=TERMINAL_ESCALATED,
                detail=f"refused twice in a row ({refusal}); escalated: "
                       f"{handle}",
                terminal=True)
            _record(iteration, context.digest, move.model_dump(), outcome, cost)
            result.terminal, result.detail = TERMINAL_ESCALATED, outcome.detail
            return result

        feedback = ""
        outcome = execute_move(pid, mission_id, move, root=root,
                               dispatch=dispatch, now=now)
        _record(iteration, context.digest, move.model_dump(), outcome, cost)
        if outcome.terminal:
            result.terminal, result.detail = outcome.status, outcome.detail
            return result

    result.terminal = TERMINAL_ITERATION_LIMIT
    result.detail = (f"reached the {bounds.max_iterations}-iteration limit "
                     f"with the mission still active")
    return result


def execute_move(project_id: str, mission_id: str, move: Any, *,
                 root: Path | None = None,
                 dispatch: Callable[..., Any] | None = None,
                 now: datetime | None = None) -> MoveOutcome:
    """Execute ONE move through Remedy's existing verbs. No verb is reinvented here.

    The dispatch path goes through ``mission_state.continue_mission`` — which
    creates the job, builds its plan verify-first and links it to the mission —
    and then applies the audited unattended approval through
    ``flight_plan.auto_approve_flight_plan`` when the job has an open plan gate.
    """
    from packages.orchestration.mission_state import (
        MISSION_STATUS_ABANDONED,
        continue_mission,
        set_mission_status,
    )
    from packages.orchestration.orchestrator_move_schema import (
        MOVE_ABORT_WITH_REASON,
        MOVE_DECLARE_MILESTONE_DONE,
        MOVE_DECLARE_MISSION_ACHIEVED,
        MOVE_DISPATCH_JOB,
        MOVE_WAIT_ON_DECISIONS,
    )

    payload = dict(getattr(move, "payload", {}) or {})
    kind = getattr(move, "kind", "")

    if kind == MOVE_WAIT_ON_DECISIONS:
        return MoveOutcome(
            status=TERMINAL_WAITING,
            detail="the orchestrator is waiting on a human decision",
            terminal=True)

    if kind == MOVE_ABORT_WITH_REASON:
        set_mission_status(project_id, mission_id, MISSION_STATUS_ABANDONED,
                           root)
        return MoveOutcome(status=TERMINAL_ABORTED,
                           detail=payload.get("reason", ""), terminal=True)

    if kind == MOVE_DECLARE_MISSION_ACHIEVED:
        mission_achieved(project_id, mission_id, root)
        return MoveOutcome(status=TERMINAL_ACHIEVED,
                           detail="every milestone is done and the mission "
                                  "goal is met",
                           terminal=True)

    if kind == MOVE_DECLARE_MILESTONE_DONE:
        milestone_id = payload["milestone_id"]
        mark_milestone_done(project_id, mission_id, milestone_id, root)
        return MoveOutcome(status="milestone_done",
                           detail=f"milestone {milestone_id} recorded as done")

    if kind == MOVE_DISPATCH_JOB:
        create = dispatch or continue_mission
        job = create(project_id, mission_id, payload["step"], root=root,
                     now=now)
        approved = _auto_approve_if_gated(job)
        detail = f"job {job.id} dispatched for {payload['milestone_id']}"
        if approved:
            detail += " (plan auto-approved, audited)"
        return MoveOutcome(status="dispatched", detail=detail,
                           job_id=str(job.id))

    # Unreachable through the schema: `kind` is a closed Literal, so anything
    # else failed validation long before it reached here. Kept as a loud
    # failure rather than a silent no-op in case the two ever drift.
    raise ValueError(f"unknown orchestrator move kind: {kind!r}")


def _auto_approve_if_gated(job: Any) -> bool:
    """Apply the audited unattended approval when the job's plan gate is open.

    Unattended missions run under ``--yes`` semantics (feature file): every
    open clarification takes its documented default and the approval carries an
    audit record. The semantics are NOT reimplemented here — this calls the
    helper ``remedy do --yes`` uses.
    """
    from packages.orchestration.data_paths import job_evidence_export_dir
    from packages.orchestration.flight_plan import (
        auto_approve_flight_plan,
        flight_plan_approval_open,
    )
    from packages.orchestration.storage import save_job

    if not flight_plan_approval_open(job):
        return False
    job.flight_plan = auto_approve_flight_plan(
        dict(job.flight_plan or {}), job_evidence_export_dir(str(job.id)))
    save_job(job)
    return True


# ---------------------------------------------------------------------------
# T002 — the evaluate step
# ---------------------------------------------------------------------------

#: A move the evaluator refused. Not terminal on its own: the loop re-prompts
#: once with the reason, and only a SECOND refusal escalates.
OUTCOME_REFUSED = "refused"

#: A second refusal in a row reached a human through the escalation verb.
TERMINAL_ESCALATED = "escalated"

#: Job states that end a dispatched job's life. A milestone cannot be declared
#: done while its job is still running — "not finished" is not "met".
TERMINAL_JOB_STATES = ("completed", "failed", "cancelled")


@dataclass(frozen=True)
class MilestoneEvidence:
    """What the loop can observe about one milestone's dispatched work.

    ``gate_released`` is ``None`` when the job stored no DoD — the F061 gate is
    additive, and a job without a definition of done is not gated at all.
    """

    job_id: str = ""
    job_state: str = ""
    gate_released: bool | None = None
    gate_blocker: str = ""
    handback: Any = None


def dispatched_job_for(project_id: str, mission_id: str, milestone_id: str,
                       root: Path | None = None) -> str:
    """The job the loop last dispatched for this milestone, from its own ledger.

    The mission record attributes a job to the MISSION, not to a milestone
    (``MissionJobLink`` carries a job id, a role and a timestamp — F069 recorded
    why). The loop's own ledger DOES carry the attribution, because every
    ``dispatch_job`` entry stores the milestone id it was for beside the job id
    it produced. Reading it here means the attribution costs no change to job
    creation, which stays exactly as F056 left it.
    """
    job_id = ""
    for entry in read_ledger(project_id, mission_id, root):
        move = entry.get("move") or {}
        if move.get("kind") != "dispatch_job":
            continue
        if (move.get("payload") or {}).get("milestone_id") != milestone_id:
            continue
        job_id = str((entry.get("outcome") or {}).get("job_id", "") or "")
    return job_id


def collect_milestone_evidence(project_id: str, mission_id: str,
                               milestone_id: str,
                               root: Path | None = None) -> MilestoneEvidence:
    """Read a milestone's evidence through the existing job and gate verbs."""
    from packages.orchestration.dod_gate import load_gate_result
    from packages.orchestration.storage import load_job

    job_id = dispatched_job_for(project_id, mission_id, milestone_id, root)
    if not job_id:
        return MilestoneEvidence()

    state = ""
    handback: Any = None
    try:
        job = load_job(_as_uuid(job_id))
    except Exception:
        # An unreadable job is an ABSENT observation, never a passing one.
        return MilestoneEvidence(job_id=job_id)
    state = str(getattr(getattr(job, "state", ""), "value", getattr(job, "state", "")))
    handback = (getattr(job, "metadata", None) or {}).get("handback")

    gate = load_gate_result(job_id)
    if gate is None:
        return MilestoneEvidence(job_id=job_id, job_state=state,
                                 handback=handback)
    return MilestoneEvidence(
        job_id=job_id, job_state=state,
        gate_released=bool(gate.get("released")),
        gate_blocker=str(gate.get("error", "") or ""),
        handback=handback)


def evaluate_dispatch(mission: Any, milestone_id: str,
                      evidence: MilestoneEvidence | None = None) -> str:
    """Refusal reason for a proposed dispatch, or "" when it may proceed.

    The A9 edge lives here: a job proposed for an ALREADY-DONE milestone is
    refused with a recorded reason rather than quietly dispatched. So is work
    on a milestone whose dependencies are not met — the plan's DAG is a
    constraint, not a suggestion.
    """
    ids = milestone_ids(mission)
    if milestone_id not in ids:
        return (f"milestone {milestone_id!r} is not in this mission's plan "
                f"({', '.join(ids) or 'no milestones'})")
    done = set(done_milestones(mission))
    if milestone_id in done:
        return (f"milestone {milestone_id} is already done — a job for a "
                f"finished milestone is refused")
    unmet = _unmet_dependencies(mission, milestone_id, done)
    if unmet:
        return (f"milestone {milestone_id} depends on {', '.join(unmet)}, "
                f"which is not done yet")
    return _era_refusal(evidence)


def evaluate_milestone_done(mission: Any, milestone_id: str,
                            evidence: MilestoneEvidence | None = None) -> str:
    """Refusal reason for a ``declare_milestone_done`` claim, or "".

    A claim is checked, not believed: the dispatched job must have reached a
    terminal state, its Definition of Done must have been met where one exists,
    and its handback must be free of the era's known defects.
    """
    ids = milestone_ids(mission)
    if milestone_id not in ids:
        return (f"milestone {milestone_id!r} is not in this mission's plan "
                f"({', '.join(ids) or 'no milestones'})")
    done = set(done_milestones(mission))
    if milestone_id in done:
        return f"milestone {milestone_id} is already recorded as done"
    unmet = _unmet_dependencies(mission, milestone_id, done)
    if unmet:
        return (f"milestone {milestone_id} cannot be done while "
                f"{', '.join(unmet)} is not")

    ev = evidence or MilestoneEvidence()
    if not ev.job_id:
        return (f"no job was ever dispatched for milestone {milestone_id}, so "
                f"there is nothing whose outcome could meet its Definition of "
                f"Done")
    if ev.job_state not in TERMINAL_JOB_STATES:
        return (f"the job dispatched for milestone {milestone_id} is in state "
                f"{ev.job_state or 'unknown'!r}, which is not terminal")
    if ev.gate_released is False:
        return (f"the Definition of Done for milestone {milestone_id} is not "
                f"met: {ev.gate_blocker or 'the gate did not release'}")
    return _era_refusal(ev)


def _unmet_dependencies(mission: Any, milestone_id: str,
                        done: set[str]) -> list[str]:
    from packages.orchestration.mission_compiler import mission_plan_of

    plan = mission_plan_of(mission)
    if plan is None:
        return []
    for ms in plan.milestones:
        if ms.id == milestone_id:
            return sorted(set(ms.depends_on) - done)
    return []


def _era_refusal(evidence: MilestoneEvidence | None) -> str:
    """Refuse to advance on any handback carrying an era-class defect.

    The five classes are the external-orchestration era's own failure modes
    (see :mod:`packages.orchestration.era_integrity`). Each was caught by a
    human reviewer at the time; the loop has no human, so it refuses instead.
    """
    from packages.orchestration.era_integrity import (
        detect_era_defects,
        render_defects,
    )

    if evidence is None or evidence.handback is None:
        return ""
    defects = detect_era_defects(evidence.handback)
    if not defects:
        return ""
    return (f"the handback carries {len(defects)} integrity defect(s) from "
            f"known finding classes, so the loop refuses to advance: "
            f"{render_defects(defects)}")


def escalate_repeated_refusal(project_id: str, mission_id: str, reason: str, *,
                              root: Path | None = None,
                              now: datetime | None = None) -> str:
    """Hand a twice-refused move to a human through the EXISTING escalation verb.

    Never a silent loop: the second refusal in a row stops being the loop's
    problem and becomes a human decision. The decision is enqueued on the
    mission's most recent job, because that is the object
    ``escalation.enqueue_task_decision`` attaches to; a mission with no job yet
    has nowhere to attach one, and that is reported rather than papered over.
    """
    from packages.orchestration.escalation import enqueue_task_decision
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.storage import load_job, save_job

    mission = load_mission(project_id, mission_id, root)
    link = mission.latest_link()
    if link is None:
        return ("no job is linked to this mission, so the refusal cannot be "
                "attached to a decision — a human has to look at the mission")
    try:
        job = load_job(_as_uuid(link.job_id))
    except Exception as exc:
        return f"the mission's latest job could not be read to escalate: {exc}"
    tasks = list(getattr(job, "tasks", ()) or ())
    if not tasks:
        return (f"job {link.job_id} has no task to attach the decision to")
    record = enqueue_task_decision(
        job,
        task_id=tasks[0].id,
        question=(f"The orchestrator's move was refused twice in a row: "
                  f"{reason}. How should this mission proceed?"),
        options=("replan the mission", "abandon the mission"),
        impact="the mission cannot advance until this is answered",
        now=now or datetime.now(timezone.utc))
    save_job(job)
    return str(record.get("decision_id", ""))


def evaluate_move(mission: Any, move: Any, *, observe: Callable[..., Any],
                  project_id: str, mission_id: str) -> str:
    """Refusal reason for one move, or "" when it may be executed.

    Only the two ADVANCING moves are evaluated. ``wait_on_decisions``,
    ``abort_with_reason`` and ``declare_mission_achieved`` are the loop's ways
    of stopping, and refusing a stop would be the silent loop this feature
    exists to prevent — except that claiming the mission is achieved while
    milestones are still open is itself an advance, and is checked.
    """
    from packages.orchestration.orchestrator_move_schema import (
        MOVE_DECLARE_MILESTONE_DONE,
        MOVE_DECLARE_MISSION_ACHIEVED,
        MOVE_DISPATCH_JOB,
    )

    payload = dict(getattr(move, "payload", {}) or {})
    kind = getattr(move, "kind", "")

    if kind == MOVE_DISPATCH_JOB:
        milestone_id = payload.get("milestone_id", "")
        return evaluate_dispatch(
            mission, milestone_id,
            observe(project_id, mission_id, milestone_id))

    if kind == MOVE_DECLARE_MILESTONE_DONE:
        milestone_id = payload.get("milestone_id", "")
        return evaluate_milestone_done(
            mission, milestone_id,
            observe(project_id, mission_id, milestone_id))

    if kind == MOVE_DECLARE_MISSION_ACHIEVED:
        ids = milestone_ids(mission)
        # R-0170: no plan means no milestones, and "no milestones are open"
        # is not evidence that the goal is met — it is the absence of any
        # evidence at all. `all_milestones_done` already requires bool(ids)
        # for exactly this reason; the claim is held to the same bar.
        if not ids:
            return ("the mission has no compiled plan — nothing evidences "
                    "the goal, so it cannot be declared achieved "
                    "(compile a mission plan first)")
        open_ones = [m for m in ids if m not in set(done_milestones(mission))]
        if open_ones:
            return (f"the mission cannot be achieved while "
                    f"{len(open_ones)} milestone(s) are still open: "
                    f"{', '.join(open_ones)}")
    return ""

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
#: F079: present only on the FIRST iteration of a mission resumed from a
#: handoff, and only after the handoff's checkpoint reference verified. It
#: follows the live sections because it describes a boundary already passed.
SECTION_HANDOFF = "## Handoff from the previous context"
#: Present only on the ONE re-prompt that follows a refused move. Last, so a
#: refusal never disturbs the stable prefix in front of it.
SECTION_FEEDBACK = "## Your previous move was refused"
#: R-0193. A milestone whose job finished and whose Definition of Done RELEASED
#: is finished, and the only move that advances the mission is the claim. The
#: R-0191 guard already refuses a dispatch there — but a refusal costs an
#: iteration, so the context says it BEFORE the model spends one. Every line in
#: this section states a fact the evidence proves, never a suggestion.
SECTION_DIRECTIVES = "## Milestones ready to declare"

#: What the stand-in dossier says about itself. Since F071 the loop's prefix is
#: the MAINTAINED document (``mission_dossier``); this render remains as the
#: fallback for a mission that has no stored version yet — a context assembled
#: outside a run — and labels itself for what it is rather than passing for the
#: maintained document.
DOSSIER_STANDIN_NOTE = (
    "(stand-in: rendered from the mission record because this mission has no "
    "stored dossier version yet.)")


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
    directives: Sequence[str] = (),
    feedback: str = "",
    handoff_seed: str = "",
) -> OrchestratorContext:
    """Assemble one iteration's context: dossier FIRST, then the volatile parts.

    ``dossier`` is the seam F071 plugs into. Given one, it renders the mission's
    dossier; absent, :func:`render_mission_dossier` renders the stand-in from
    the mission record. A non-empty ``Mission.dossier_ref`` is reported so a
    reader can see which document a decision was made against.

    ``handoff_seed`` is F079's: the rendered handoff block a RESUMED mission
    starts its first iteration from. It sits behind the dossier because the
    dossier is the live document and the handoff is the account of a boundary
    that has already passed — a successor context reads what is true now, then
    what it was told at the boundary.
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
    if handoff_seed.strip():
        sections = (*sections, (SECTION_HANDOFF, handoff_seed.strip()))
    lines = [line for line in directives if line.strip()]
    if lines:
        sections = (*sections, (SECTION_DIRECTIVES, "\n".join(lines)))
    if feedback.strip():
        sections = (*sections, (SECTION_FEEDBACK, feedback.strip()))
    text = "\n\n".join(f"{name}\n\n{body}" for name, body in sections) + "\n"
    return OrchestratorContext(
        text=text, digest=context_digest(text), sections=sections)


def released_milestone_directives(mission: Any, observe: Callable[..., Any], *,
                                  project_id: str, mission_id: str) -> list[str]:
    """One line per milestone that is finished and proven, in plan order.

    The facts are the SAME ones the R-0191 dispatch guard reads — the latest
    job's state and ``dod_gate.load_gate_result``'s verdict — so the context
    and the guard can never disagree about which milestone is ready. Only
    ``gate_released is True`` produces a line: an absent verdict proves
    nothing and a blocked one is R-0190's business.

    Reading evidence costs no provider call. It is the same ``observe`` seam
    the evaluation step uses, so a test that substitutes it substitutes both.
    """
    done = set(done_milestones(mission))
    lines: list[str] = []
    for milestone_id in milestone_ids(mission):
        if milestone_id in done:
            continue
        try:
            evidence = observe(project_id, mission_id, milestone_id)
        except Exception:  # noqa: BLE001 — a directive is never worth a crash
            continue
        if evidence is None or evidence.job_state != "completed":
            continue
        if evidence.gate_released is not True:
            continue
        lines.append(
            f"- {milestone_id}: job {evidence.job_id} completed and its "
            f"Definition of Done RELEASED. The correct next move is "
            f"declare_milestone_done for {milestone_id}.")
    return lines


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


def next_iteration_index(project_id: str, mission_id: str,
                         root: Path | None = None) -> int:
    """The number the next iteration takes: one past the highest recorded.

    Iteration numbering belongs to the MISSION, not to one ``run_mission``
    invocation — the same lesson F047 learned for cycle numbering
    (``long_run_executor.next_cycle_index``). A second run that restarted at 1
    would leave a ledger reading 1,2,3,1,2 and a reader with no way to order
    it. Reading the highest number already on disk costs one file read and
    keeps the audit trail sequential across any number of runs.
    """
    numbers = [int(e.get("iteration", 0) or 0)
               for e in read_ledger(project_id, mission_id, root)]
    return (max(numbers) if numbers else 0) + 1


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
                           root: Path | None = None,
                           *, call_fn: Callable[[str, int], str] | None = None,
                           ) -> Path:
    """Refresh the mission's dossier. Called EVERY iteration.

    F071: this drives the MAINTAINED document. One
    :func:`~packages.orchestration.mission_dossier.refresh_mission_dossier`
    call appends the iteration's facts, enforces the token budget and stores
    the new ``dossier_v<N>.md`` version; the newest render is then written to
    the live file beside the ledger. ``call_fn`` is the COMPRESSION provider —
    omitted, an over-budget dossier keeps its honest flag rather than spending
    a call the loop's own budget never authorized.
    """
    from packages.orchestration.mission_dossier import (
        refresh_mission_dossier,
        render_dossier,
    )

    result = refresh_mission_dossier(project_id, mission_id, mission,
                                     root=root, call_fn=call_fn)
    path = mission_evidence_dir(project_id, mission_id, root) / DOSSIER_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_dossier(result.dossier), encoding="utf-8")
    return path


def maintained_dossier_text(project_id: str, mission_id: str, mission: Any,
                            root: Path | None = None) -> str:
    """The NEWEST stored dossier version — what the live prompt uses.

    Falls back to the stand-in render when a mission has no stored version
    yet, so ``assemble_context`` called outside a run still has a dossier. In
    a run the refresh precedes the assembly every iteration, so the fallback
    is not the path a real prompt takes.
    """
    from packages.orchestration.mission_dossier import newest_dossier_text

    return newest_dossier_text(project_id, mission_id, root) or \
        render_mission_dossier(mission, done_milestones=done_milestones(mission))


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
#: The iteration's own work RAISED — the provider call, the dispatch or the
#: dossier refresh threw rather than returning. Distinct from ``aborted`` (the
#: orchestrator decided to give up) and from ``invalid_move`` (the provider
#: answered with something unusable): here the work itself failed, and the run
#: says so instead of escaping with no account.
TERMINAL_ITERATION_FAILED = "iteration_failed"


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
    #: F079. Where the boundary handoff landed when this run paused for its
    #: limits or for a stop, "" when none was built.
    handoff_path: str = ""
    #: Why no handoff exists although one was attempted. A build failure is
    #: recorded HERE and nowhere else in the outcome: the terminal a run
    #: reached is a fact about the mission, and an artifact that could not be
    #: written must never overwrite it.
    handoff_error: str = ""
    #: The handoff this run's FIRST iteration was seeded from, "" when the
    #: mission started fresh or carried no readable handoff.
    resumed_from: str = ""


def build_boundary_handoff(result: MissionRunResult,
                           root: Path | None = None) -> MissionRunResult:
    """Compose a handoff for a run that PAUSED, recording failure honestly.

    F079: every pause is meant to be resumable by a fresh context, so the loop
    builds the artifact at the two terminals that mean "not finished, not
    broken" — its iteration limit and an operator stop. Building is a pure
    artifact and cannot change the mission, but it CAN fail (a disk that is
    gone, a source that will not read). A failure is recorded on the result
    and nothing else: the terminal the run actually reached is never masked by
    the state of its souvenir.
    """
    from packages.orchestration.handoff import build_handoff

    try:
        result.handoff_path = str(build_handoff(result.mission_id, root))
    except Exception as exc:  # noqa: BLE001 — the terminal outranks the artifact
        result.handoff_error = f"{type(exc).__name__}: {exc}"
    return result


def resume_seed_text(mission_id: str, root: Path | None = None) -> tuple[str, str]:
    """``(seed text, source name)`` for a resumed mission's first iteration.

    Returns ``("", "")`` when there is nothing to resume from. A handoff whose
    references no longer hold, or whose schema this build does not know, is
    NOT seeded — the refusal (the checkpoint feature's own message, or the
    schema refusal) is raised to the caller rather than silently downgraded to
    a run that starts from a narrative nobody verified.
    """
    from packages.orchestration.handoff import handoff_resume_seed

    seed = handoff_resume_seed(mission_id, root)
    if seed is None:
        return ("", "")
    return (seed.text, seed.path.name)


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
    execute: Callable[[Any], Any] | None = None,
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
      ``execute``         how a dispatched job is RUN; defaults to
                          :func:`execute_dispatched_job`, i.e. the existing
                          ``long_run_executor.run_cycles``
      ``dossier``         how the mission's dossier renders; defaults to the
                          newest stored version of the F071 maintained document
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
    # F071: the prefix is the MAINTAINED document's newest version, which
    # ``refresh`` stores at the top of every iteration before the context is
    # assembled. The stand-in remains only as the no-version fallback.
    prefix = dossier or (
        lambda mission: maintained_dossier_text(pid, mission_id, mission, root))
    hand_over = escalate or (
        lambda p, m, reason: escalate_repeated_refusal(p, m, reason, root=root,
                                                       now=now))
    #: Empty until a move is refused; carried into exactly ONE re-prompt.
    feedback = ""
    #: R-0190: consecutive gate-BLOCKED completions for one milestone. A
    #: milestone whose gate blocks twice in a row is not going to be argued
    #: green by a third identical dispatch — the loop escalates instead of
    #: spending the rest of its budget rediscovering the same blocker. The
    #: loop's own second-refusal rule is the precedent.
    blocked_milestone = ""
    blocked_blockers: list[str] = []
    #: R-0196: consecutive boundary-caught RETRYABLE failures for one
    #: milestone. One transient fault is worth another iteration; two in a row
    #: on the same milestone is a fault that is not passing, so a human hears
    #: about it instead of the budget draining into the same exception.
    boundary_milestone = ""
    boundary_failures: list[str] = []

    def _record(iteration: int, digest: str, move: dict[str, Any],
                outcome: MoveOutcome, cost: dict[str, Any]) -> None:
        entry = LedgerEntry(iteration=iteration, context_digest=digest,
                            move=move, outcome=outcome.to_json(), cost=cost)
        append_ledger_entry(pid, mission_id, entry, root, now=now)
        result.entries.append(entry)

    # Ledger numbering continues the MISSION's sequence; ``step`` counts this
    # invocation, which is what ``limits`` bounds.
    base = next_iteration_index(pid, mission_id, root)
    # F079 consumption: a mission that already has ledger history is being
    # RESUMED, so its first iteration is seeded from the newest handoff whose
    # references still verify. A mission on its first ever iteration has no
    # boundary behind it and is seeded from nothing.
    seed_text, seed_source = resume_seed_text(mission_id, root) if base > 1 \
        else ("", "")
    result.resumed_from = seed_source

    for step in range(1, bounds.max_iterations + 1):
        iteration = base + step - 1
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
            result.iterations = step - 1
            return build_boundary_handoff(result, root)

        mission = load_mission(pid, mission_id, root)
        if mission.status != MISSION_STATUS_ACTIVE:
            result.terminal = TERMINAL_NOT_ACTIVE
            result.detail = f"mission status is {mission.status}"
            result.iterations = step - 1
            return result

        # ── the iteration's own work, inside the boundary. A raise from the
        # provider call, from dispatch or from the dossier refresh becomes a
        # classified post-mortem, this iteration's ledger entry and an honest
        # terminal — never an escape that leaves the run with no account of
        # itself. `except Exception` deliberately does NOT catch
        # KeyboardInterrupt or SystemExit: an operator stopping Remedy is not
        # a failure to classify. Since R-0196 a RETRYABLE class costs the
        # iteration and the loop continues; every other class, unknown
        # included, still ends the run. No retry lives here either — transport
        # retries belong below call_fn (F001), and the next iteration decides
        # afresh rather than re-issuing the call that raised.
        digest = ""
        cost: dict[str, Any] = {"calls": 0, "usage": None,
                                "usage_source": USAGE_UNMEASURED}
        try:
            # The dossier is refreshed BEFORE the context is assembled, so the
            # prompt's first section and the mission's own dossier file describe
            # the same state rather than drifting an iteration apart.
            refresh(pid, mission_id, mission)

            context = assemble_context(
                mission,
                done_milestones=done_milestones(mission),
                dossier=prefix,
                last_report=last_report(mission) if last_report else "",
                open_decisions=open_mission_decisions(mission),
                directives=released_milestone_directives(
                    mission, observe, project_id=pid, mission_id=mission_id),
                feedback=feedback,
                # Only iteration one carries the boundary account; after that
                # the run has its own history and the seed would be noise.
                handoff_seed=seed_text if step == 1 else "")
            digest = context.digest
            result.iterations = step

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
                                   dispatch=dispatch, execute=execute, now=now)
            _record(iteration, context.digest, move.model_dump(), outcome, cost)
            if outcome.terminal:
                result.terminal, result.detail = outcome.status, outcome.detail
                return result
            # An iteration that decided and executed a move ends any
            # boundary-failure streak: the fault did not persist (R-0196).
            boundary_milestone, boundary_failures = "", []

            # R-0190: a gate that blocked twice in a row for the same milestone
            # is a human's problem, not a third identical dispatch.
            milestone, blocker = blocked_completion(move, outcome)
            if milestone and blocker:
                if milestone != blocked_milestone:
                    blocked_milestone, blocked_blockers = milestone, []
                blocked_blockers.append(blocker)
                if len(blocked_blockers) >= BLOCKED_COMPLETIONS_BEFORE_ESCALATION:
                    reason = (
                        f"milestone {milestone}: the Definition of Done blocked "
                        f"{len(blocked_blockers)} completed jobs in a row "
                        f"({'; '.join(blocked_blockers)}). A third dispatch "
                        f"would rediscover the same blocker and spend "
                        f"{bounds.max_iterations - step} more iteration(s) of "
                        f"this run's budget.")
                    handle = hand_over(pid, mission_id, reason)
                    escalated = MoveOutcome(
                        status=TERMINAL_ESCALATED,
                        detail=f"{reason} escalated: {handle}",
                        terminal=True)
                    _record(iteration, context.digest, {}, escalated, cost)
                    result.terminal = TERMINAL_ESCALATED
                    result.detail = escalated.detail
                    return result
            elif blocker == "" and _was_dispatch(move):
                # A released (or un-run) gate ends the streak.
                blocked_milestone, blocked_blockers = "", []
        except Exception as exc:
            failure_class, detail = record_iteration_failure(
                pid, mission_id, exc, root=root, iteration=iteration)
            result.iterations = step
            if not _is_retryable(failure_class):
                outcome = MoveOutcome(status=TERMINAL_ITERATION_FAILED,
                                      detail=detail, terminal=True)
                _record(iteration, digest, {}, outcome, cost)
                result.terminal, result.detail = TERMINAL_ITERATION_FAILED, detail
                return result

            # R-0196: a transient transport or machine fault costs this
            # iteration, not the mission. The failure is classified, its
            # post-mortem written and the iteration ledgered — then the loop
            # goes round again under the SAME budgets. Still no retry lives
            # here: the next iteration re-decides from a fresh context, which
            # is not the same thing as re-issuing a call (F001).
            milestone = working_milestone(mission)
            if milestone != boundary_milestone:
                boundary_milestone, boundary_failures = milestone, []
            boundary_failures.append(detail)
            if len(boundary_failures) >= BOUNDARY_FAILURES_BEFORE_ESCALATION:
                reason = (
                    f"milestone {milestone or '(none)'}: {len(boundary_failures)} "
                    f"caught iteration failures in a row "
                    f"({'; '.join(boundary_failures)}). Retrying a third time "
                    f"would spend {bounds.max_iterations - step} more "
                    f"iteration(s) of this run's budget on the same fault.")
                handle = hand_over(pid, mission_id, reason)
                escalated = MoveOutcome(
                    status=TERMINAL_ESCALATED,
                    detail=f"{reason} escalated: {handle}",
                    terminal=True)
                _record(iteration, digest, {}, escalated, cost)
                result.terminal, result.detail = TERMINAL_ESCALATED, escalated.detail
                return result
            _record(iteration, digest, {},
                    MoveOutcome(status=OUTCOME_ITERATION_RETRYING, detail=detail),
                    cost)
            continue

    result.terminal = TERMINAL_ITERATION_LIMIT
    result.detail = (f"reached the {bounds.max_iterations}-iteration limit "
                     f"with the mission still active")
    return build_boundary_handoff(result, root)


#: Job states that mean "this milestone's work has not been executed, or is
#: still executing". A second dispatch against one of these is the
#: six-identical-jobs loop campaign attempt 1 recorded (R-0184).
#:
#: ``paused`` is deliberately ABSENT. A paused job is one that asked a human
#: something, and the move schema has NO resume kind — dispatch_job,
#: wait_on_decisions, declare_milestone_done, declare_mission_achieved,
#: abort_with_reason. Refusing a dispatch there would leave the loop with no
#: legal move that advances the milestone once the decision is answered, i.e. a
#: deadlock in place of a defect. (Observation for the reviewer, deliberately
#: NOT fixed here: the absent resume verb is why re-dispatch is the only
#: forward path out of a paused job.)
IN_FLIGHT_JOB_STATES = ("pending", "planned", "running")

#: How many consecutive gate-blocked completions of ONE milestone the loop
#: tolerates before handing it to a human (R-0190). Two, matching the loop's
#: own refuse-once-then-escalate rule: the first block is a legitimate,
#: informed retry — the context already carries the blocker — and the second
#: says the retry did not work.
BLOCKED_COMPLETIONS_BEFORE_ESCALATION = 2

#: The failure classes a caught iteration may be retried on (R-0196). NARROW
#: and named on purpose: both mean "the machine or the transport hiccuped",
#: which is exactly the fault another iteration can get past. Everything else
#: — a config error, a fence violation, a parse defect, and above all
#: ``unknown`` — still ends the run, because retrying a fault Remedy does not
#: understand is how a budget disappears without an account of itself.
RETRYABLE_FAILURE_CLASSES: frozenset[str] = frozenset({
    "provider_unavailable", "io_failure"})

#: How many consecutive boundary-caught retryable failures on ONE milestone
#: the loop tolerates. Two, matching R-0190 and the refuse-once rule.
BOUNDARY_FAILURES_BEFORE_ESCALATION = 2


def _is_retryable(failure_class: Any) -> bool:
    """Membership by VALUE, so the loop never imports F010's enum at module
    scope and a class added there is not silently retried here."""
    return getattr(failure_class, "value",
                   str(failure_class)) in RETRYABLE_FAILURE_CLASSES


def working_milestone(mission: Any) -> str:
    """The milestone a failed iteration was working: the first not yet done.

    The exception may have been raised before any move existed, so the
    milestone cannot come from the move. It comes from the same plan order the
    loop itself follows, which is what makes "twice in a row on the SAME
    milestone" a statement about the work rather than about the exception.
    """
    done = set(done_milestones(mission))
    for milestone_id in milestone_ids(mission):
        if milestone_id not in done:
            return milestone_id
    return ""


def _was_dispatch(move: Any) -> bool:
    from packages.orchestration.orchestrator_move_schema import MOVE_DISPATCH_JOB

    return getattr(move, "kind", "") == MOVE_DISPATCH_JOB


def blocked_completion(move: Any, outcome: MoveOutcome) -> tuple[str, str]:
    """``(milestone_id, blocker)`` when a dispatch finished on a BLOCKED gate.

    ``("", "")`` when this move was not a dispatch. ``(milestone, "")`` when it
    was a dispatch whose gate did not block — which RESETS the counter, because
    the streak this guards against is a consecutive one.
    """
    from packages.orchestration.orchestrator_move_schema import MOVE_DISPATCH_JOB

    if getattr(move, "kind", "") != MOVE_DISPATCH_JOB:
        return "", ""
    milestone = str((getattr(move, "payload", {}) or {}).get("milestone_id", ""))
    detail = outcome.detail or ""
    if "gate=blocked" not in detail:
        return milestone, ""
    blocker = detail.split("gate=blocked", 1)[1].strip()
    return milestone, (blocker or "the gate did not release")


def attach_milestone_dod(project_id: str, mission_id: str, mission: Any,
                         milestone_id: str, job_id: str,
                         root: Path | None = None) -> bool:
    """Store the milestone's COMPILED DoD on the job it was dispatched for.

    The gate reads a job's own evidence area (``dod_gate.load_dod``), and until
    R-0188 nothing ever put anything there — ``store_dod`` had zero callers, so
    ``run_job_gate`` returned None for every job in existence and
    ``dod_blocking_green`` was unmeetable by construction.

    Nothing is compiled here. F069 already compiled every milestone's DoD into
    the mission's evidence area and recorded the filename in the milestone's
    ``dod_ref``; this copies that artifact onto the job. A milestone with no
    ``dod_ref``, or a file that will not parse, stores NOTHING and the gate
    stays un-run for that job — an honest absence the evaluator already knows
    how to report, never an invented definition of done.

    Returns whether a DoD was stored.
    """
    from packages.orchestration.dod_gate import store_dod
    from packages.orchestration.dod_schema import DoD
    from packages.orchestration.mission_compiler import mission_plan_of
    from packages.orchestration.mission_state import mission_evidence_dir

    plan = mission_plan_of(mission)
    if plan is None:
        return False
    milestone = next((m for m in plan.milestones
                      if getattr(m, "id", "") == milestone_id), None)
    ref = getattr(milestone, "dod_ref", "") if milestone is not None else ""
    if not ref:
        return False
    path = mission_evidence_dir(project_id, mission_id, root) / ref
    try:
        dod = DoD.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except Exception:  # noqa: BLE001 — an unusable DoD is no DoD, said by absence
        return False
    store_dod(job_id, dod)
    return True


@dataclass(frozen=True)
class JobExecution:
    """What running one dispatched job produced, as the loop reads it.

    A small carrier rather than the executor's own ``CycleLoopResult``, which
    is frozen: the loop needs the cycle resolution alongside the outcome so the
    run's evidence can record an over-cap run (R-0187). Test doubles expose the
    same attribute names, so the seam stays substitutable.
    """

    terminal_status: str = ""
    job_status: str = ""
    stop_reason: str = ""
    resolved_cycles: dict[str, Any] = field(default_factory=dict)
    #: The DoD gate's verdict for this job, or None when it stored no DoD.
    gate_released: bool | None = None
    gate_blocker: str = ""


def execute_dispatched_job(job: Any, *,
                           experiment_max_cycles: int | None = None,
                           worktree_root: Path | None = None
                           ) -> JobExecution:
    """Run a freshly dispatched job through the EXISTING multi-cycle executor.

    This is the step T1_F070's Design specified ("run it through the
    multi-cycle executor -> evaluate") and the build omitted, which is why
    campaign attempt 1 produced ten missions whose jobs all sat at ``planned``
    (R-0184). It reimplements nothing: the limits come from
    ``limits_from_config`` — so the F046 rollout cap still applies exactly as
    it does for ``remedy job run`` — the task pipeline is ``default_task_step``,
    and the budgets are the job's own.

    ``unattended=True`` because the gauntlet's whole premise is a run with no
    operator after the start command: a task decision carrying a safe default
    is answered from it and recorded in the escalation log (F051), and one
    without a safe default still waits.

    ``experiment_max_cycles`` (R-0187) is the order's own cycle budget, passed
    only by the gauntlet runner. Omitted — every other caller — the F046
    rollout cap applies exactly as before. The resolved cycles are returned on
    the result so the run's evidence can record what was actually allowed.

    ``worktree_root`` (R-0189) is the checkout the DoD checks run in: the
    gauntlet passes its run's OWN materialised copy of the sample project.
    Omitted, the gate falls back to the job's workspace.
    """
    from dataclasses import replace

    from packages.orchestration.config import get_config
    from packages.orchestration.long_run_executor import (
        default_task_step,
        limits_from_config,
        run_cycles,
    )
    from packages.orchestration.run_log import RunLogWriter
    from packages.providers.ollama_builder.provider import OllamaBuilder

    limits, resolved = limits_from_config(
        get_config(), experiment_max_cycles=experiment_max_cycles)
    limits = replace(limits, budgets=getattr(job, "budgets", None))
    result = run_cycles(job, limits, OllamaBuilder().build,
                        task_step=default_task_step,
                        log=RunLogWriter(job_id=job.id),
                        unattended=True)
    # Carried out rather than logged and forgotten: a run that went over the
    # rollout cap has to say so in its own evidence (R-0187).
    # R-0188: the gate runs at PRODUCTION job completion, here, once. It
    # persists its own verdict where load_gate_result reads it, so there is no
    # second store and the fixture-demo fulfillment spine stays untouched.
    released, blocker = run_gate_for_job(str(job.id), worktree_root)
    return JobExecution(terminal_status=result.terminal_status,
                        job_status=result.job_status,
                        stop_reason=result.stop_reason,
                        resolved_cycles=resolved.to_json(),
                        gate_released=released, gate_blocker=blocker)


def run_gate_for_job(job_id: str,
                     worktree_root: Path | None = None) -> tuple[bool | None, str]:
    """Evaluate a finished job's Definition of Done through the EXISTING gate.

    ``run_job_gate`` both evaluates and persists — one author for the verdict —
    so this adds no store of its own. ``None`` means the job carried no DoD and
    was therefore not gated at all, which is the gate's own additive contract.

    The checks run in the job's workspace: a gauntlet mission has no repository
    checkout, and pointing them at one would run a mission's checks against the
    operator's tree. A gate that cannot run its checks reports them red with a
    reason, which is an honest verdict rather than a missing one.
    """
    from packages.orchestration.data_paths import workspaces_dir
    from packages.orchestration.dod_gate import gate_blocker, run_job_gate

    root = worktree_root or (workspaces_dir() / job_id)
    root.mkdir(parents=True, exist_ok=True)
    result = run_job_gate(job_id, root)
    if result is None:
        return None, ""
    return result.released, gate_blocker(result)


def execute_move(project_id: str, mission_id: str, move: Any, *,
                 root: Path | None = None,
                 dispatch: Callable[..., Any] | None = None,
                 execute: Callable[[Any], Any] | None = None,
                 now: datetime | None = None) -> MoveOutcome:
    """Execute ONE move through Remedy's existing verbs. No verb is reinvented here.

    The dispatch path goes through ``mission_state.continue_mission`` — which
    creates the job, builds its plan verify-first and links it to the mission —
    then applies the audited unattended approval through
    ``flight_plan.auto_approve_flight_plan`` when the job has an open plan gate,
    and then RUNS the job through the existing multi-cycle executor
    (:func:`execute_dispatched_job`). Creating a job and walking away was
    R-0184: the milestone could never become done, so the loop re-dispatched
    until its iteration budget ran out.
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
        # R-0188: give the job its milestone's DoD before it runs, or the gate
        # has nothing to evaluate when it finishes.
        from packages.orchestration.mission_state import load_mission as _load

        if attach_milestone_dod(project_id, mission_id,
                                _load(project_id, mission_id, root),
                                payload["milestone_id"], str(job.id), root):
            detail += "; DoD attached"
        run = (execute or execute_dispatched_job)(job)
        # What execution PRODUCED, on the ledger entry, so the next iteration's
        # context shows why the milestone is or is not claimable.
        detail += (f"; executed: terminal={getattr(run, 'terminal_status', '')}"
                   f" job_status={getattr(run, 'job_status', '')}")
        stop_reason = getattr(run, "stop_reason", "")
        if stop_reason:
            detail += f" stop={stop_reason}"
        cycles = getattr(run, "resolved_cycles", None) or {}
        if cycles:
            detail += (f" cycles={cycles.get('max_cycles')}"
                       f"/{cycles.get('source')}"
                       f"{' OVER-CAP' if cycles.get('over_cap') else ''}")
        released = getattr(run, "gate_released", None)
        if released is None:
            detail += " gate=not-run"
        else:
            detail += f" gate={'released' if released else 'blocked'}"
            if not released and getattr(run, "gate_blocker", ""):
                detail += f" ({run.gate_blocker})"
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

#: An iteration the boundary caught on a RETRYABLE class (R-0196). An OUTCOME_
#: and deliberately NOT a TERMINAL_: the iteration is spent and accounted for,
#: the mission is not over. The ledger keeps it so a run that succeeded on the
#: second attempt still says out loud that the first one failed.
OUTCOME_ITERATION_RETRYING = "iteration_failed_retrying"

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

    A REFUSED dispatch is not a dispatch (R-0192). Its move kind is still
    ``dispatch_job`` and its milestone id still matches, but nothing was
    created, so its outcome carries no job id — and letting it through would
    overwrite the real answer with "". That is not hypothetical: the R-0191
    guard made refused dispatches common, and the very next ``declare`` move
    was refused with "no job was ever dispatched" for a milestone whose job had
    completed with a released gate. Only an entry that actually produced a job
    updates the answer.
    """
    job_id = ""
    for entry in read_ledger(project_id, mission_id, root):
        move = entry.get("move") or {}
        if move.get("kind") != "dispatch_job":
            continue
        if (move.get("payload") or {}).get("milestone_id") != milestone_id:
            continue
        produced = str((entry.get("outcome") or {}).get("job_id", "") or "")
        if not produced:
            continue
        job_id = produced
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
    # R-0186: one milestone, one job at a time. Campaign attempt 1 dispatched
    # six jobs for the same milestone because nothing refused a second one
    # while the first was still in flight. The refusal says what to do INSTEAD,
    # so the next move is an advance rather than the same move again.
    in_flight = _in_flight_refusal(milestone_id, evidence)
    if in_flight:
        return in_flight
    # R-0191: the third leg of the guard triad. In flight -> wait; blocked
    # twice -> escalate (R-0190); completed with a RELEASED gate -> there is
    # nothing left to dispatch, and the only move that advances the mission is
    # the claim itself.
    released = _released_gate_refusal(milestone_id, evidence)
    if released:
        return released
    return _era_refusal(evidence)


def _released_gate_refusal(milestone_id: str,
                           evidence: MilestoneEvidence | None) -> str:
    """Refuse a dispatch when the milestone's work is already done and proven.

    The verdict is the REAL one: ``collect_milestone_evidence`` reads it from
    ``dod_gate.load_gate_result`` for the LATEST job the ledger attributes to
    this milestone, so a newer un-released job supersedes an older released
    one by construction — nothing is re-derived here.

    Remedy deliberately does NOT declare the milestone itself. The claim is the
    model's move and carries the model's accountability; the loop's job is to
    refuse the move that cannot help and say which one can. The existing
    first-refusal re-prompt carries this sentence back to the model, and the
    second-refusal escalation already exists if it ignores it.
    """
    if evidence is None or not evidence.job_id:
        return ""
    if evidence.job_state != "completed":
        return ""
    if evidence.gate_released is not True:
        return ""
    return (f"milestone {milestone_id} is already finished: job "
            f"{evidence.job_id} completed and its Definition of Done "
            f"RELEASED. Another job would repeat work that is already proven. "
            f"Instead: declare_milestone_done for {milestone_id}")


def _in_flight_refusal(milestone_id: str,
                       evidence: MilestoneEvidence | None) -> str:
    """Refuse a second job for a milestone whose first one has not finished."""
    if evidence is None or not evidence.job_id:
        return ""
    if evidence.job_state not in IN_FLIGHT_JOB_STATES:
        return ""
    if evidence.gate_released:
        advice = (f"declare_milestone_done for {milestone_id} — its gate has "
                  f"already released")
    else:
        advice = ("wait_on_decisions, or declare_milestone_done once that job "
                  "finishes and its gate releases")
    return (f"milestone {milestone_id} already has job {evidence.job_id} in "
            f"flight (state {evidence.job_state}); a second job for it is "
            f"refused. Instead: {advice}")


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


def record_iteration_failure(project_id: str, mission_id: str,
                             exc: BaseException, *, root: Path | None = None,
                             iteration: int = 0) -> tuple[Any, str]:
    """Classify a raised iteration failure and write its F010 post-mortem.

    Returns ``(failure_class, detail)``. The class comes from
    :func:`failure_postmortem.classify` — the same pure classifier every other
    layer uses — and a class it cannot determine comes back as ``unknown``,
    said out loud rather than invented.

    Never raises. The boundary exists so a run ends honestly; a post-mortem
    that could not be written must not become a second, louder failure on top
    of the first. It is reported in the detail instead, so the run's own
    account still names what happened.

    Each iteration's record lives in its own sub-directory: ``write_postmortem``
    is create-only by design, and two failing iterations in one mission must not
    collide over the account of the first.
    """
    from packages.orchestration.failure_postmortem import (
        SCOPE_JOB,
        FailureSignals,
        PostmortemV1,
        classify,
        write_postmortem,
    )
    from packages.orchestration.mission_state import mission_evidence_dir

    text = f"{type(exc).__name__}: {exc}"
    verdict = classify(FailureSignals(exception=exc, error_text=text))
    detail = (f"iteration {iteration} failed: {text} "
              f"(class {verdict.failure_class.value})")
    try:
        evidence = mission_evidence_dir(project_id, mission_id, root)
        target = evidence / f"iteration_{iteration}"
        target.mkdir(parents=True, exist_ok=True)
        write_postmortem(target, PostmortemV1(
            failure_class=verdict.failure_class,
            signal_source=verdict.signal_source,
            job_id=mission_id,
            scope=SCOPE_JOB,
            raw_reason=f"iteration {iteration}: {text}",
            terminal_status=TERMINAL_ITERATION_FAILED,
        ), root=evidence)
    except Exception as write_exc:  # honest, never fatal
        detail += (f"; the post-mortem could not be written "
                   f"({type(write_exc).__name__}: {write_exc})")
    return verdict.failure_class, detail

"""F075 T001 — the gauntlet's pass definition, made mechanical.

Autonomy is earned with data, not granted on vibes (T1_F075.md): ten curated
missions must run FLAWLESSLY before multi-cycle defaults flip. "Flawlessly" is
worth nothing as a feeling, so this module is the definition written down as a
pure function over recorded evidence (:mod:`packages.orchestration.gauntlet_evidence`).
It never executes a mission, never calls a provider, and never touches the data
root it judges.

**A run is flawless when every criterion in :data:`PASS_CRITERIA` holds.**

* ``evidence_well_formed`` — evidence that cannot be read is not evidence. An
  unreadable run is NOT a passing run, and not an exception either.
* ``start_command_only`` — zero operator interventions after the start command.
* ``terminal_green`` — the mission reached ``achieved``. Every other honest
  terminal (``iteration_limit``, ``waiting_on_decisions``, ``stopped``, …) is a
  run that did not finish, which is exactly what it says.
* ``dod_blocking_green`` — no blocking DoD check is red (asked of
  :mod:`packages.orchestration.dod_gate`, never re-derived here).
* ``no_unknown_postmortems`` — every failure along the way was classified;
  ``FailureClass.UNKNOWN`` means Remedy did not understand its own failure.
* ``no_open_decisions`` — nothing was left hanging for a human.
* ``host_data_root_untouched`` — the operator's real data root hashes the same
  before and after. Earned 2026-07-23: during F081 both worker tests and
  reviewer verification wrote stray projects into the real registry. Any
  pollution, however small, disqualifies.
* ``no_era_defect_classes`` — none of the external-orchestration era's finding
  classes (R-0141/R-0143/R-0144/R-0145/R-0146/R-0147/R-0148, detectors in
  :mod:`packages.orchestration.era_integrity`) appeared. Operator addition
  2026-07-27.
* ``injections_degraded`` — every injected harness failure (provider API error
  mid-move, truncated model response, harness death mid-dispatch, harness death
  mid-write) degraded to a LEDGERED failure, a retry within budget, or an
  escalation. A silent success or a corrupted artifact accepted downstream is
  the failure this criterion exists to catch. Operator addition 2026-08-03.

Every criterion is falsifiable by construction: each one has a fixture that
flips it and a test that asserts the run stops being flawless. That is the
acceptance bar (T1_F075.md, Acceptance) — a pass definition nothing can fail is
not a pass definition.

**Remedy deliberately does NOT let this module run a mission.** Executing the
gauntlet is the CLI's job (``scripts/self_run_gauntlet.py``); judging it is
this module's, and that separation is what makes ``--dry-run`` against recorded
evidence a proof rather than a rehearsal.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.dod_gate import gate_blocker as _dod_blocker
from packages.orchestration.era_integrity import DEFECT_FINDING_CLASSES
from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.gauntlet_evidence import (
    DOD_RESULT_FILENAME,
    RunEvidence,
    load_run,
    run_dirs,
)
from packages.orchestration.orchestrator_loop import TERMINAL_ACHIEVED

#: The only green terminal. ``achieved``, or the mission did not finish.
TERMINAL_GREEN = (TERMINAL_ACHIEVED,)


# ---------------------------------------------------------------------------
# The pass criteria — the frozen definition, one id per checkable fact
# ---------------------------------------------------------------------------

CRITERION_EVIDENCE_WELL_FORMED = "evidence_well_formed"
CRITERION_START_COMMAND_ONLY = "start_command_only"
CRITERION_TERMINAL_GREEN = "terminal_green"
CRITERION_DOD_BLOCKING_GREEN = "dod_blocking_green"
CRITERION_NO_UNKNOWN_POSTMORTEMS = "no_unknown_postmortems"
CRITERION_NO_OPEN_DECISIONS = "no_open_decisions"
CRITERION_DATA_ROOT_UNTOUCHED = "host_data_root_untouched"
CRITERION_NO_ERA_DEFECTS = "no_era_defect_classes"
CRITERION_INJECTIONS_DEGRADED = "injections_degraded"

#: The pass definition, in report order. Changing this tuple changes what
#: "flawless" means and therefore needs an ADR (T1_F075.md, Do not touch).
PASS_CRITERIA: tuple[str, ...] = (
    CRITERION_EVIDENCE_WELL_FORMED,
    CRITERION_START_COMMAND_ONLY,
    CRITERION_TERMINAL_GREEN,
    CRITERION_DOD_BLOCKING_GREEN,
    CRITERION_NO_UNKNOWN_POSTMORTEMS,
    CRITERION_NO_OPEN_DECISIONS,
    CRITERION_DATA_ROOT_UNTOUCHED,
    CRITERION_NO_ERA_DEFECTS,
    CRITERION_INJECTIONS_DEGRADED,
)


# ---------------------------------------------------------------------------
# Harness-failure injection classes (operator addition 2026-08-03)
# ---------------------------------------------------------------------------

INJECTION_PROVIDER_API_ERROR_MID_MOVE = "provider_api_error_mid_move"
INJECTION_TRUNCATED_MODEL_RESPONSE = "truncated_model_response"
INJECTION_HARNESS_DEATH_MID_DISPATCH = "harness_death_mid_dispatch"
INJECTION_HARNESS_DEATH_MID_WRITE = "harness_death_mid_write"

#: The four classes the gauntlet injects. A run declaring a class outside this
#: set is malformed evidence, not a newly discovered failure mode.
INJECTION_CLASSES: tuple[str, ...] = (
    INJECTION_PROVIDER_API_ERROR_MID_MOVE,
    INJECTION_TRUNCATED_MODEL_RESPONSE,
    INJECTION_HARNESS_DEATH_MID_DISPATCH,
    INJECTION_HARNESS_DEATH_MID_WRITE,
)

#: What an injected failure is allowed to become — F051 semantics.
DISPOSITION_LEDGERED = "ledgered_failure"
DISPOSITION_RETRIED = "retry_within_budget"
DISPOSITION_ESCALATED = "escalated"
ACCEPTED_DISPOSITIONS: tuple[str, ...] = (
    DISPOSITION_LEDGERED,
    DISPOSITION_RETRIED,
    DISPOSITION_ESCALATED,
)

#: The two named ways an injection can go wrong. Named rather than lumped into
#: "other" because these two are what the operator asked to be able to see.
DISPOSITION_SILENT_SUCCESS = "silent_success"
DISPOSITION_CORRUPTED_ARTIFACT_ACCEPTED = "corrupted_artifact_accepted"
REJECTED_DISPOSITIONS: tuple[str, ...] = (
    DISPOSITION_SILENT_SUCCESS,
    DISPOSITION_CORRUPTED_ARTIFACT_ACCEPTED,
)


# ---------------------------------------------------------------------------
# Failure classes — what the evaluator can NAME when a run is not flawless
# ---------------------------------------------------------------------------

FAILURE_MALFORMED_EVIDENCE = "malformed_evidence"
FAILURE_OPERATOR_INTERVENTION = "operator_intervention"
FAILURE_TERMINAL_NOT_GREEN = "terminal_not_green"
FAILURE_DOD_BLOCKING_RED = "dod_blocking_red"
FAILURE_UNKNOWN_POSTMORTEM = "unknown_postmortem"
FAILURE_OPEN_DECISION = "open_decision"
FAILURE_DATA_ROOT_POLLUTED = "host_data_root_polluted"
FAILURE_ERA_DEFECT = "era_defect"
FAILURE_INJECTION_NOT_DEGRADED = "injection_not_degraded"

#: Every failure kind this evaluator can produce.
FAILURE_KINDS: tuple[str, ...] = (
    FAILURE_MALFORMED_EVIDENCE,
    FAILURE_OPERATOR_INTERVENTION,
    FAILURE_TERMINAL_NOT_GREEN,
    FAILURE_DOD_BLOCKING_RED,
    FAILURE_UNKNOWN_POSTMORTEM,
    FAILURE_OPEN_DECISION,
    FAILURE_DATA_ROOT_POLLUTED,
    FAILURE_ERA_DEFECT,
    FAILURE_INJECTION_NOT_DEGRADED,
)

#: Era finding class -> the R-ids it was extracted from, re-exported so a
#: caller can enumerate what the gauntlet is able to name without importing two
#: modules. The mapping itself has exactly one author: era_integrity.
ERA_FINDING_CLASSES: dict[str, str] = dict(DEFECT_FINDING_CLASSES)


@dataclass(frozen=True)
class GauntletFailure:
    """One named reason a run is not flawless.

    ``finding_class`` carries the era's R-ids when the kind is an era defect;
    ``injection_class`` names which injected harness failure was mishandled.
    Both stay empty rather than being filled with a plausible-looking guess.
    """

    kind: str
    criterion: str
    detail: str
    finding_class: str = ""
    injection_class: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "criterion": self.criterion,
            "detail": self.detail,
            "finding_class": self.finding_class,
            "injection_class": self.injection_class,
        }


@dataclass(frozen=True)
class RunVerdict:
    """The verdict for one run: the criteria table plus the named failures."""

    run_dir: str
    order_id: str
    flawless: bool
    criteria: dict[str, bool]
    failures: tuple[GauntletFailure, ...]
    evidence: RunEvidence

    def to_json(self) -> dict[str, Any]:
        return {
            "run_dir": self.run_dir,
            "order_id": self.order_id,
            "kind": self.evidence.kind,
            "flawless": self.flawless,
            "terminal_status": self.evidence.terminal_status,
            "wall_seconds": self.evidence.wall_seconds,
            "tokens_in": self.evidence.tokens_in,
            "tokens_out": self.evidence.tokens_out,
            "operator_interventions": list(self.evidence.operator_interventions),
            "criteria": {name: self.criteria[name] for name in PASS_CRITERIA},
            "failures": [f.to_json() for f in self.failures],
            "evidence_links": dict(sorted(self.evidence.evidence_links.items())),
        }


@dataclass(frozen=True)
class GauntletVerdict:
    """The whole campaign: every run, in evidence order, and whether it held."""

    evidence_dir: str
    runs: tuple[RunVerdict, ...]

    @property
    def flawless_count(self) -> int:
        return sum(1 for r in self.runs if r.flawless)

    @property
    def passed(self) -> bool:
        """A pass needs at least one run AND every recorded run flawless.

        An empty evidence directory passing vacuously is the single most likely
        way this gate would lie about 10/10, so it is refused explicitly.
        """
        return bool(self.runs) and self.flawless_count == len(self.runs)

    def failure_kinds(self) -> tuple[str, ...]:
        """Every failure kind present, deduplicated, in FAILURE_KINDS order."""
        seen = {f.kind for r in self.runs for f in r.failures}
        return tuple(kind for kind in FAILURE_KINDS if kind in seen)


# ---------------------------------------------------------------------------
# The judgement — one function per criterion, so each one can be flipped alone
# ---------------------------------------------------------------------------

def _check_operator_interventions(ev: RunEvidence) -> list[GauntletFailure]:
    return [
        GauntletFailure(
            kind=FAILURE_OPERATOR_INTERVENTION,
            criterion=CRITERION_START_COMMAND_ONLY,
            detail=f"operator intervened after start: {command}",
        )
        for command in ev.operator_interventions
    ]


def _check_terminal(ev: RunEvidence) -> list[GauntletFailure]:
    if ev.terminal_status in TERMINAL_GREEN:
        return []
    return [GauntletFailure(
        kind=FAILURE_TERMINAL_NOT_GREEN,
        criterion=CRITERION_TERMINAL_GREEN,
        detail=(f"terminal status {ev.terminal_status or '(none)'} is not "
                f"{'/'.join(TERMINAL_GREEN)}"),
    )]


class _GateResultView:
    """The three attributes ``dod_gate.gate_blocker`` reads, over stored JSON.

    The blocker line has exactly one author — the gate — and this adapter keeps
    it that way instead of re-deriving the string from the same fields here.
    """

    def __init__(self, body: dict[str, Any]) -> None:
        self.released = bool(body.get("released"))
        self.error = str(body.get("error", "") or "")
        raw = body.get("blocking_red")
        self.blocking_red = tuple(str(i) for i in raw) if isinstance(raw, list) else ()


def _check_dod(ev: RunEvidence) -> list[GauntletFailure]:
    """Blocking DoD checks, asked of the gate's own verdict rather than re-read.

    A run with no stored gate result never reached the gate; that is a red
    criterion with an honest reason, not a silent pass.
    """
    if ev.dod_result is None:
        return [GauntletFailure(
            kind=FAILURE_DOD_BLOCKING_RED,
            criterion=CRITERION_DOD_BLOCKING_GREEN,
            detail=f"no {DOD_RESULT_FILENAME}: the DoD gate never produced a verdict",
        )]
    view = _GateResultView(ev.dod_result)
    if view.released and view.error:
        # released=True with an error is a verdict at war with itself. The gate
        # never writes one, so seeing it means the evidence was edited or
        # truncated — reported as what it is, not resolved in either direction.
        return [GauntletFailure(
            kind=FAILURE_DOD_BLOCKING_RED,
            criterion=CRITERION_DOD_BLOCKING_GREEN,
            detail=f"the stored gate verdict contradicts itself: "
                   f"released with error {view.error}",
        )]
    if view.released:
        return []
    return [GauntletFailure(
        kind=FAILURE_DOD_BLOCKING_RED,
        criterion=CRITERION_DOD_BLOCKING_GREEN,
        detail=(_dod_blocker(view)  # type: ignore[arg-type]
                or "the DoD gate held the job without naming a blocker"),
    )]


def _check_postmortems(ev: RunEvidence) -> list[GauntletFailure]:
    failures: list[GauntletFailure] = []
    for record in ev.postmortems:
        failure_class = str(record.get("failure_class", "") or "")
        if failure_class and failure_class != FailureClass.UNKNOWN.value:
            continue
        scope = str(record.get("scope", "") or "(no scope)")
        failures.append(GauntletFailure(
            kind=FAILURE_UNKNOWN_POSTMORTEM,
            criterion=CRITERION_NO_UNKNOWN_POSTMORTEMS,
            detail=(f"postmortem ({scope}) has failure class "
                    f"{failure_class or '(absent)'} — the failure was not understood"),
        ))
    return failures


def _check_open_decisions(ev: RunEvidence) -> list[GauntletFailure]:
    return [
        GauntletFailure(
            kind=FAILURE_OPEN_DECISION,
            criterion=CRITERION_NO_OPEN_DECISIONS,
            detail=(f"decision {record.get('decision_id', '(no id)')} left open: "
                    f"{record.get('question', '(no question)')}"),
        )
        for record in ev.open_decisions
    ]


def _check_data_root(ev: RunEvidence) -> list[GauntletFailure]:
    before, after = ev.data_root_hash_before, ev.data_root_hash_after
    if not before or not after:
        return [GauntletFailure(
            kind=FAILURE_DATA_ROOT_POLLUTED,
            criterion=CRITERION_DATA_ROOT_UNTOUCHED,
            detail="the host data root was not hashed before and after the run",
        )]
    if before == after:
        return []
    return [GauntletFailure(
        kind=FAILURE_DATA_ROOT_POLLUTED,
        criterion=CRITERION_DATA_ROOT_UNTOUCHED,
        detail=f"host data root changed during the run: {before} -> {after}",
    )]


def _check_era_defects(ev: RunEvidence) -> list[GauntletFailure]:
    failures: list[GauntletFailure] = []
    for record in ev.era_defects:
        kind = str(record.get("kind", "") or "")
        failures.append(GauntletFailure(
            kind=FAILURE_ERA_DEFECT,
            criterion=CRITERION_NO_ERA_DEFECTS,
            detail=(f"era defect {kind or '(unnamed)'}: "
                    f"{record.get('detail', '(no detail)')}"),
            finding_class=ERA_FINDING_CLASSES.get(
                kind, str(record.get("finding_class", "") or "")),
        ))
    return failures


def _check_injections(ev: RunEvidence) -> list[GauntletFailure]:
    """Every injected harness failure must have degraded, not vanished."""
    failures: list[GauntletFailure] = []
    for record in ev.injections:
        injection_class = str(record.get("class", "") or "")
        disposition = str(record.get("disposition", "") or "")
        if injection_class not in INJECTION_CLASSES:
            failures.append(GauntletFailure(
                kind=FAILURE_INJECTION_NOT_DEGRADED,
                criterion=CRITERION_INJECTIONS_DEGRADED,
                detail=f"unknown injection class {injection_class or '(absent)'}",
                injection_class=injection_class,
            ))
            continue
        if disposition in ACCEPTED_DISPOSITIONS:
            continue
        named = ("a named mishandling" if disposition in REJECTED_DISPOSITIONS
                 else "an unclassified disposition")
        # The run's own account of what happened is carried through verbatim: a
        # reader chasing a silent success needs the sentence the harness wrote,
        # not only the class it fell into.
        recorded = str(record.get("detail", "") or "")
        failures.append(GauntletFailure(
            kind=FAILURE_INJECTION_NOT_DEGRADED,
            criterion=CRITERION_INJECTIONS_DEGRADED,
            detail=(f"{injection_class} ended as {disposition or '(absent)'} — "
                    f"{named}; expected one of {'/'.join(ACCEPTED_DISPOSITIONS)}"
                    + (f"; recorded: {recorded}" if recorded else "")),
            injection_class=injection_class,
        ))
    return failures


#: criterion id -> the predicate that can fail it. One entry per PASS_CRITERIA
#: member (asserted below) so a criterion can never be added without a check.
_CRITERION_CHECKS = {
    CRITERION_START_COMMAND_ONLY: _check_operator_interventions,
    CRITERION_TERMINAL_GREEN: _check_terminal,
    CRITERION_DOD_BLOCKING_GREEN: _check_dod,
    CRITERION_NO_UNKNOWN_POSTMORTEMS: _check_postmortems,
    CRITERION_NO_OPEN_DECISIONS: _check_open_decisions,
    CRITERION_DATA_ROOT_UNTOUCHED: _check_data_root,
    CRITERION_NO_ERA_DEFECTS: _check_era_defects,
    CRITERION_INJECTIONS_DEGRADED: _check_injections,
}
assert set(_CRITERION_CHECKS) | {CRITERION_EVIDENCE_WELL_FORMED} == set(PASS_CRITERIA)


def evaluate_run(ev: RunEvidence) -> RunVerdict:
    """Judge one recorded run against the whole pass definition.

    Malformed evidence short-circuits: every criterion is False, because a run
    whose evidence cannot be read has proven nothing, and reporting eight greens
    over an unreadable file would be the exact overclaim this gate forbids.
    """
    if ev.load_error:
        return RunVerdict(
            run_dir=ev.run_dir,
            order_id=ev.order_id,
            flawless=False,
            criteria={name: False for name in PASS_CRITERIA},
            failures=(GauntletFailure(
                kind=FAILURE_MALFORMED_EVIDENCE,
                criterion=CRITERION_EVIDENCE_WELL_FORMED,
                detail=ev.load_error,
            ),),
            evidence=ev,
        )

    criteria: dict[str, bool] = {CRITERION_EVIDENCE_WELL_FORMED: True}
    failures: list[GauntletFailure] = []
    for name in PASS_CRITERIA:
        if name == CRITERION_EVIDENCE_WELL_FORMED:
            continue
        found = _CRITERION_CHECKS[name](ev)
        criteria[name] = not found
        failures.extend(found)
    return RunVerdict(
        run_dir=ev.run_dir,
        order_id=ev.order_id,
        flawless=not failures,
        criteria=criteria,
        failures=tuple(failures),
        evidence=ev,
    )


def evaluate_evidence_dir(evidence_dir: Path, *,
                          only: int | None = None) -> GauntletVerdict:
    """Judge a whole recorded evidence directory — the ``--dry-run`` entry point.

    ``only`` is the 1-based index into the canonical run order, mirroring the
    CLI's ``--only <n>``: rerunning one order is cheap and expected, but a full
    pass must still be ten consecutive greens from one invocation.
    """
    dirs = run_dirs(evidence_dir)
    if only is not None:
        if only < 1 or only > len(dirs):
            raise IndexError(f"--only {only} is outside 1..{len(dirs)}")
        dirs = [dirs[only - 1]]
    return GauntletVerdict(
        evidence_dir=str(evidence_dir),
        runs=tuple(evaluate_run(load_run(d)) for d in dirs),
    )

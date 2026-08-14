"""F077 T001 — the autonomy watchdog's three tripwires, as pure functions.

The watchdog is the tripwire that is independent of the thing it watches. It
READS the orchestrator loop's decision ledger and answers one question per trip
class: is the loop repeating itself, is it burning tokens out of proportion to
its own history, is it working on something the mission plan never named.

Everything in this module is PURE. Nothing here reads a file, writes a file,
mutates a mission, or imports the loop it observes — a watchdog that could edit
the run it is judging would be judging its own work. The evaluators take a list
of ledger entries (plain dicts, exactly what ``read_ledger`` returns) and give
back :class:`Trip` records. Deciding what to DO about a trip — pausing the
mission, raising the decision — is deliberately NOT here; that is F077 T002.

A malformed entry is SKIPPED, never raised on. A ledger is forensic evidence
and ``read_ledger`` already tolerates torn lines, so an entry missing its
``move``, ``outcome`` or ``cost``, or carrying a non-dict where a dict belongs,
must not be able to make the other entries unreadable. A tripwire that crashes
on one bad line is a tripwire that is not watching.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from packages.orchestration.orchestrator_move_schema import (
    MOVE_DECLARE_MILESTONE_DONE,
    MOVE_DISPATCH_JOB,
)

# ---------------------------------------------------------------------------
# Trip kinds — one per class of thing that can go wrong unattended
# ---------------------------------------------------------------------------

#: The loop keeps dispatching the same milestone and never declares it done.
TRIP_NO_PROGRESS = "no_progress"
#: Recent iterations burn tokens far above the run's own measured baseline.
TRIP_BURN_ANOMALY = "burn_anomaly"
#: A job was dispatched for a milestone the mission plan does not contain.
TRIP_GOAL_DRIFT = "goal_drift"


#: One tripwire firing, with the evidence a human needs to judge it. A frozen
#: dataclass rather than a dict so the evidence triple cannot drift its keys
#: between the evaluator that builds it and the caller that reports it.
@dataclass(frozen=True)
class Trip:
    """What tripped, in one line, since when, and the numbers behind it."""

    kind: str
    what: str
    since_iteration: int
    numbers: dict[str, Any]

    #: The wire form. Exactly the four fields — a trip carries no hidden state.
    def to_json(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "what": self.what,
            "since_iteration": self.since_iteration,
            "numbers": dict(self.numbers),
        }


#: The config keys that name each threshold. Thresholds live in config, not in
#: code, because the right number depends on the mission, not on the release.
CONFIG_KEY_WATCHDOG_NO_PROGRESS_REPEATS = "watchdog.no_progress_repeats"
CONFIG_KEY_WATCHDOG_BURN_WINDOW = "watchdog.burn_window"
CONFIG_KEY_WATCHDOG_BURN_MIN_SAMPLES = "watchdog.burn_min_samples"
CONFIG_KEY_WATCHDOG_BURN_MULTIPLIER = "watchdog.burn_multiplier"


#: The four numbers every evaluator needs, resolved once and passed down.
@dataclass(frozen=True)
class WatchdogThresholds:
    """Conservative by default: a watchdog that cries wolf gets switched off."""

    no_progress_repeats: int = 3
    burn_window: int = 3
    burn_min_samples: int = 5
    burn_multiplier: float = 3.0


#: Config beats default, exactly as ``loop_limits_from_config`` resolves the
#: loop's own bound. ``get_config`` is imported INSIDE the function so this
#: module stays importable — and testable — with no config layer present.
def watchdog_thresholds_from_config(config: Any = None) -> WatchdogThresholds:
    """A key that reads ``None`` takes the dataclass default, never a guess."""
    if config is None:
        from packages.orchestration.config import get_config

        config = get_config()
    defaults = WatchdogThresholds()
    repeats = config.get(CONFIG_KEY_WATCHDOG_NO_PROGRESS_REPEATS)
    window = config.get(CONFIG_KEY_WATCHDOG_BURN_WINDOW)
    samples = config.get(CONFIG_KEY_WATCHDOG_BURN_MIN_SAMPLES)
    multiplier = config.get(CONFIG_KEY_WATCHDOG_BURN_MULTIPLIER)
    return WatchdogThresholds(
        no_progress_repeats=(defaults.no_progress_repeats if repeats is None
                             else int(repeats)),
        burn_window=(defaults.burn_window if window is None else int(window)),
        burn_min_samples=(defaults.burn_min_samples if samples is None
                          else int(samples)),
        burn_multiplier=(defaults.burn_multiplier if multiplier is None
                         else float(multiplier)),
    )


# ---------------------------------------------------------------------------
# Reading one entry — every accessor tolerates a torn line
# ---------------------------------------------------------------------------


def _sub_dict(entry: Any, key: str) -> dict[str, Any]:
    """The named sub-object, or an empty dict when the entry is malformed."""
    if not isinstance(entry, dict):
        return {}
    value = entry.get(key)
    return value if isinstance(value, dict) else {}


def _move_kind(entry: Any) -> str:
    """The move kind of one entry, or ``""`` when there is no readable move."""
    kind = _sub_dict(entry, "move").get("kind")
    return kind if isinstance(kind, str) else ""


def _milestone_id(entry: Any) -> str:
    """The milestone a move names, or ``""`` when the payload does not say."""
    payload = _sub_dict(entry, "move").get("payload")
    if not isinstance(payload, dict):
        return ""
    milestone_id = payload.get("milestone_id")
    return milestone_id if isinstance(milestone_id, str) else ""


def _iteration(entry: Any) -> int:
    """The entry's iteration number, carried into evidence for the human only.

    NEVER used as a window index: ``read_ledger`` skips torn lines and the
    numbering continues across runs, so the gap between two iteration numbers
    is not a distance.
    """
    if not isinstance(entry, dict):
        return 0
    try:
        return int(entry.get("iteration", 0) or 0)
    except (TypeError, ValueError):
        return 0


#: The entries that actually put a job into the world: a ``dispatch_job`` move
#: whose outcome carries a job id. A REFUSED dispatch is excluded — the loop's
#: own second-refusal escalation already owns that event (R-0192), and counting
#: it here would give one failure two independent alarms.
def dispatched_entries(
    entries: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Ledger order, preserved. Malformed entries are simply not dispatches."""
    out: list[dict[str, Any]] = []
    for entry in entries:
        if _move_kind(entry) != MOVE_DISPATCH_JOB:
            continue
        job_id = _sub_dict(entry, "outcome").get("job_id")
        if isinstance(job_id, str) and job_id:
            out.append(entry)
    return out


#: The tokens one iteration is KNOWN to have cost, or ``None`` when nothing
#: measured it. Remedy never writes an estimate into a field named ``usage``
#: (P6), so an unmeasured entry contributes nothing rather than a zero — a zero
#: would drag a baseline down and manufacture an anomaly out of missing data.
def measured_tokens(entry: Any) -> int | None:
    """``input_tokens + output_tokens``, each defaulting to 0, or ``None``."""
    usage = _sub_dict(entry, "cost").get("usage")
    if not isinstance(usage, dict):
        return None
    total = 0
    for key in ("input_tokens", "output_tokens"):
        value = usage.get(key, 0)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        total += int(value)
    return total


# ---------------------------------------------------------------------------
# The three tripwires
# ---------------------------------------------------------------------------


#: The loop is busy but going nowhere: N dispatches in a row on ONE milestone
#: with no ``declare_milestone_done`` between them. Progress is read off the
#: LEDGER rather than the plan body because nothing versions or timestamps the
#: mission's milestone-done set, so the plan cannot say WHEN it advanced.
def evaluate_no_progress(
    entries: Sequence[dict[str, Any]],
    *,
    repeats: int,
) -> Trip | None:
    """Fires on the entry that completes the run; the run's first one dates it."""
    if repeats < 1:
        return None
    run: list[dict[str, Any]] = []
    run_milestone = ""
    for entry in entries:
        if _move_kind(entry) == MOVE_DECLARE_MILESTONE_DONE:
            # Any claim of progress clears the run, whatever it was about.
            run = []
            run_milestone = ""
            continue
        if not dispatched_entries([entry]):
            continue
        milestone_id = _milestone_id(entry)
        if not milestone_id:
            continue
        if milestone_id != run_milestone:
            run = [entry]
            run_milestone = milestone_id
        else:
            run.append(entry)
        if len(run) >= repeats:
            return Trip(
                kind=TRIP_NO_PROGRESS,
                what=(f"{len(run)} dispatches in a row on milestone "
                      f"{milestone_id} with no milestone declared done "
                      f"between them"),
                since_iteration=_iteration(run[0]),
                numbers={
                    "repeats": len(run),
                    "threshold": repeats,
                    "milestone_id": milestone_id,
                },
            )
    return None


#: The run is burning far above its OWN history. The baseline is the same
#: mission's earlier measured iterations, not a global constant, so a big
#: mission is not permanently anomalous and a small one is not blind.
def evaluate_burn_anomaly(
    entries: Sequence[dict[str, Any]],
    *,
    window: int,
    min_samples: int,
    multiplier: float,
) -> Trip | None:
    """INERT below ``min_samples`` measured entries: thin data never trips."""
    if window < 1:
        return None
    measured: list[tuple[int, int]] = []
    for entry in entries:
        tokens = measured_tokens(entry)
        if tokens is None:
            # Unmeasured: contributes nothing and does not shrink the window.
            continue
        measured.append((_iteration(entry), tokens))
    if len(measured) < min_samples + window:
        return None
    baseline = measured[:-window]
    recent = measured[-window:]
    if not baseline:
        return None
    baseline_mean = sum(tokens for _, tokens in baseline) / len(baseline)
    window_mean = sum(tokens for _, tokens in recent) / len(recent)
    if not window_mean > multiplier * baseline_mean:
        return None
    return Trip(
        kind=TRIP_BURN_ANOMALY,
        what=(f"the last {len(recent)} measured iterations averaged "
              f"{window_mean:.1f} tokens against a baseline of "
              f"{baseline_mean:.1f} over {len(baseline)} iterations"),
        since_iteration=recent[0][0],
        numbers={
            "window_mean": window_mean,
            "baseline_mean": baseline_mean,
            "multiplier": multiplier,
            "baseline_samples": len(baseline),
        },
    )


#: A job was dispatched for a milestone the mission plan never named. Drift is
#: BINARY, not counted: one job on an invented goal is already the whole
#: failure, and waiting for a second one only spends more of the budget on it.
def evaluate_goal_drift(
    entries: Sequence[dict[str, Any]],
    *,
    milestone_ids: Sequence[str],
) -> Trip | None:
    """The FIRST unknown milestone trips; later ones add nothing to the case."""
    known = {str(m) for m in milestone_ids}
    for entry in dispatched_entries(entries):
        milestone_id = _milestone_id(entry)
        if not milestone_id:
            # No attribution at all is a torn entry, not evidence of drift.
            continue
        if milestone_id in known:
            continue
        return Trip(
            kind=TRIP_GOAL_DRIFT,
            what=(f"dispatched a job for milestone {milestone_id}, which is "
                  f"not one of the mission plan's {len(known)} milestones"),
            since_iteration=_iteration(entry),
            numbers={
                "milestone_id": milestone_id,
                "known_milestones": sorted(known),
            },
        )
    return None


#: Every tripwire, over one ledger, in a FIXED order. Stable order means a
#: caller can diff two watchdog runs without sorting, and a report reads the
#: same way every time.
def evaluate_ledger(
    entries: Sequence[dict[str, Any]],
    *,
    milestone_ids: Sequence[str],
    thresholds: WatchdogThresholds,
) -> list[Trip]:
    """no_progress, then burn_anomaly, then goal_drift. Non-trips are dropped."""
    candidates = (
        evaluate_no_progress(
            entries, repeats=thresholds.no_progress_repeats),
        evaluate_burn_anomaly(
            entries,
            window=thresholds.burn_window,
            min_samples=thresholds.burn_min_samples,
            multiplier=thresholds.burn_multiplier),
        evaluate_goal_drift(entries, milestone_ids=milestone_ids),
    )
    return [trip for trip in candidates if trip is not None]

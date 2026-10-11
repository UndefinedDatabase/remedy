"""F116 T002, first part — the job burn monitor: a job's own spend alarm.

A job's burn is measured in TOKENS, never dollars: one sample per provider
call the job runner counts, its amount the same ``input_tokens`` plus
``output_tokens`` sum ``run_job``'s own ``_accumulated_tokens`` already adds,
so the alarm and the token budget read one basis (DECISION F116 D3 (1)). A
provider call reports tokens far more often than it reports a price, and an
alarm that falls silent on every unpriced call protects nothing on those
runs — cost in dollars is not this module's unit.

This module reads no clock: :meth:`JobBurnMonitor.record_call` takes ``at``
from its caller and never reads ``datetime.now()`` or an equivalent itself:
the arithmetic that judges a reading lives in ``burn_detector``, which this
module calls and never reimplements, and that module's own deliberate
absences (no clock, no config, no file) hold here too.

Imports from ``burn_detector`` and the standard library only at its top;
``get_config`` is imported INSIDE :func:`job_burn_thresholds_from_config`,
``AUTO_APPROVAL_MODE`` INSIDE :func:`job_approved_unattended`, and the run log,
the pause control and the decision queue INSIDE :func:`record_burn_trip`, so
this module stays importable — and testable — with no config layer and no
``job_plan`` import present. ``run_job`` calls this module from its own safe
point (DECISION F116 D4 (1) to (4)): one ``JobBurnMonitor`` per run, a sample
recorded for every counted provider call and kept in the job's ``metadata``
under ``BURN_SAMPLES_KEY``, and :func:`record_burn_trip`, which keeps the
newest tripped reading on the job (R-1241).

Remedy deliberately does not throttle a job's parallel width on a trip,
because ``run_job`` runs one task and one provider call at a time, so there
is no width to narrow (DECISION F116 D7 (4)).
"""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any

from packages.orchestration.burn_detector import (
    RATE_UNIT_PER_HOUR,
    BurnReading,
    BurnSample,
    BurnThresholds,
    evaluate_burn_rate,
)

#: The config keys that name each threshold (DECISION F116 D3 (3)).
CONFIG_KEY_JOB_BURN_WINDOW = "job_burn.window"
CONFIG_KEY_JOB_BURN_MIN_SAMPLES = "job_burn.min_samples"
CONFIG_KEY_JOB_BURN_MULTIPLIER = "job_burn.multiplier"
CONFIG_KEY_JOB_BURN_MIN_SPEND_TOKENS = "job_burn.min_spend_tokens"
CONFIG_KEY_JOB_BURN_EXPECTED_TOKENS_PER_HOUR = "job_burn.expected_tokens_per_hour"

#: The alarm's one unit: tokens, never dollars (DECISION F116 D3 (1)).
JOB_BURN_UNIT = "tokens"

#: What a run-log write raises that must never stop a healthy job: the same tuple
#: ``pingpong_job._TASK_LOG_ERRORS`` names for the job's other run-log writes.
_EVENT_WRITE_ERRORS = (OSError, RuntimeError, ValueError, TypeError)


#: A call's amount in whatever ``usage_actuals`` reports, or ``None`` when it
#: cannot be trusted as a measurement (DECISION F116 D3 (2)): not a dict, or
#: either token field present but not a plain ``int`` (``bool`` excluded even
#: though it is an ``int`` subclass). A missing field counts 0.
def _call_amount(usage_actuals: Any) -> float | None:
    if not isinstance(usage_actuals, dict):
        return None
    total = 0
    for key in ("input_tokens", "output_tokens"):
        if key not in usage_actuals:
            continue
        value = usage_actuals[key]
        if isinstance(value, bool) or not isinstance(value, int):
            return None
        total += value
    return float(total)


#: Config beats default, exactly as ``watchdog_thresholds_from_config``
#: resolves the loop's own bound (DECISION F116 D3 (3)). ``get_config`` is
#: imported INSIDE the function so this module stays importable — and
#: testable — with no config layer present. The 20000-token floor is job
#: burn's own default, not ``BurnThresholds``' generic 0.0: a mission
#: iteration and a provider call differ in size by an order of magnitude.
def job_burn_thresholds_from_config(config: Any = None) -> BurnThresholds:
    """A key that reads ``None`` takes the dataclass default, never a guess."""
    if config is None:
        from packages.orchestration.config import get_config

        config = get_config()
    defaults = BurnThresholds(min_spend=20000.0)
    window = config.get(CONFIG_KEY_JOB_BURN_WINDOW)
    min_samples = config.get(CONFIG_KEY_JOB_BURN_MIN_SAMPLES)
    multiplier = config.get(CONFIG_KEY_JOB_BURN_MULTIPLIER)
    min_spend_tokens = config.get(CONFIG_KEY_JOB_BURN_MIN_SPEND_TOKENS)
    expected_per_hour = config.get(CONFIG_KEY_JOB_BURN_EXPECTED_TOKENS_PER_HOUR)
    return BurnThresholds(
        window=(defaults.window if window is None else int(window)),
        min_samples=(defaults.min_samples if min_samples is None
                     else int(min_samples)),
        multiplier=(defaults.multiplier if multiplier is None
                    else float(multiplier)),
        min_spend=(defaults.min_spend if min_spend_tokens is None
                   else float(min_spend_tokens)),
        expected_per_hour=(defaults.expected_per_hour if expected_per_hour is None
                           else float(expected_per_hour)),
    )


#: The wire form a job's reading is shown with: the detector's own ten keys
#: plus the one unit this module always reads in (DECISION F116 D3 (1)).
def job_burn_record(reading: BurnReading) -> dict[str, Any]:
    """``reading.to_json()`` plus ``"unit": JOB_BURN_UNIT`` — eleven keys."""
    record = reading.to_json()
    record["unit"] = JOB_BURN_UNIT
    return record


#: DECISION F116 D5 (1): unattended is exactly the audit `auto_approve_task_plan`
#: already stamps, never a guess about who is watching the run.
def job_approved_unattended(job: Any) -> bool:
    """True when *job*'s plan was approved with no person watching it."""
    from packages.orchestration.job_plan import AUTO_APPROVAL_MODE

    task_plan = getattr(job, "task_plan", None)
    if not isinstance(task_plan, dict):
        return False
    audit = task_plan.get("_approval_audit")
    if not isinstance(audit, dict):
        return False
    return audit.get("mode") == AUTO_APPROVAL_MODE


#: DECISION F116 D5 (2): the one marker a trip's decision question starts
#: with, so a re-trip finds and updates the same open record instead of
#: raising a second one.
BURN_DECISION_MARKER = "[burn_alarm]"

#: DECISION F116 D5 (2): the pause source an unattended trip's pause request
#: carries, read back off the job the same way every other pause source is.
BURN_PAUSE_SOURCE = "burn_alarm"


#: DECISION F116 D5 (2): the one sentence a person reads in the pause reason
#: and the decision question — plain, so it names no internal basis label.
def job_burn_sentence(record: dict[str, Any]) -> str:
    """The sentence for a TRIPPED ``job_burn_record`` — call only on one that trips."""
    if record["rate_unit"] == RATE_UNIT_PER_HOUR:
        return (
            f"The last {record['window_samples']} provider calls spent "
            f"{record['rate']:.1f} tokens per hour, more than "
            f"{record['multiplier']:g} times the {record['expectation']:.1f} "
            f"tokens per hour set in configuration (from call "
            f"{record['since_label']} on)."
        )
    return (
        f"The last {record['window_samples']} provider calls spent "
        f"{record['rate']:.1f} tokens each on average, more than "
        f"{record['multiplier']:g} times the {record['expectation']:.1f} "
        f"tokens per call this job spent before them (from call "
        f"{record['since_label']} on)."
    )


#: DECISION F116 D7 (1): the one reader every view a person reads uses. A
#: record loaded from disk may be torn or edited by hand, and a view must never
#: raise on one, so anything but a whole tripped record reads None.
def recorded_burn_sentence(record: Any) -> str | None:
    """``job_burn_sentence`` of a persisted ``burn_reading``, or None without a whole trip."""
    if not isinstance(record, dict) or record.get("tripped") is not True:
        return None
    try:
        return job_burn_sentence(record)
    except (KeyError, TypeError, ValueError):
        return None


#: R-1241 (DECISION F297 D12): the key of a job's ``metadata`` that keeps its
#: samples, so a job continued after a pause judges its next calls against
#: every call it made before, rather than against a baseline started at zero.
BURN_SAMPLES_KEY = "burn_samples"


#: One kept sample read back, or ``None`` for an entry that is not one: a
#: record loaded from disk may be torn or edited by hand, and the monitor
#: must never raise on one.
def _kept_sample(entry: Any) -> BurnSample | None:
    if not isinstance(entry, dict):
        return None
    amount, at, label = entry.get("amount"), entry.get("at"), entry.get("label")
    if isinstance(label, bool) or not isinstance(label, int):
        return None
    if amount is not None and (isinstance(amount, bool)
                               or not isinstance(amount, (int, float))):
        return None
    if at is not None and not isinstance(at, str):
        return None
    try:
        when = datetime.fromisoformat(at) if at is not None else None
    except ValueError:
        return None
    return BurnSample(amount=None if amount is None else float(amount), at=when,
                      label=label)


#: The job runner's own accumulator: one sample per counted provider call,
#: built once per run and read at ``run_job``'s safe point (DECISION F116
#: D4 (1) to (3)).
class JobBurnMonitor:
    """Appends ``BurnSample`` records and evaluates them with the detector."""

    def __init__(self, thresholds: BurnThresholds,
                 store: dict[str, Any] | None = None) -> None:
        """*store*, given, is the job's ``metadata``: the samples kept there
        are read back, and every call recorded is kept there too (R-1241)."""
        self._thresholds = thresholds
        self._store = store
        kept = store.get(BURN_SAMPLES_KEY) if store is not None else None
        read_back = (_kept_sample(entry) for entry in (kept if isinstance(kept, list) else []))
        self._samples: list[BurnSample] = [s for s in read_back if s is not None]

    #: One sample per call, labelled by its 1-based position among the calls
    #: recorded so far — never by ``at`` — exactly as the detector's own
    #: ``label`` is evidence for a caller and never an index.
    def record_call(self, usage_actuals: Any, *, at: datetime | None) -> None:
        """Reads no clock: ``at`` is the caller's; this module measures nothing."""
        label = len(self._samples) + 1
        sample = BurnSample(amount=_call_amount(usage_actuals), at=at, label=label)
        self._samples.append(sample)
        if self._store is not None:
            kept = self._store.get(BURN_SAMPLES_KEY)
            if not isinstance(kept, list):
                kept = self._store[BURN_SAMPLES_KEY] = []
            kept.append({"amount": sample.amount,
                         "at": at.isoformat() if at is not None else None,
                         "label": label})

    #: The job's current verdict — ``None`` while there is too little to judge.
    def reading(self) -> BurnReading | None:
        """``evaluate_burn_rate`` over every sample recorded so far."""
        return evaluate_burn_rate(self._samples, self._thresholds)


#: R-1241 (DECISION F297 D12): the trip handler of ``run_job``'s safe point (DECISION F116 D4 (3)),
#: moved here from ``run_job._stop_check``. A reading that does not trip, or that repeats the trip
#: already recorded, changes nothing, so the newest TRIPPED record stays the job's evidence even
#: once a later, untripped reading would otherwise erase it. A NEW trip is kept on the job and
#: written to its run log as one ``job_burn_tripped`` event (DECISION F116 D8 (1)); it pauses a job
#: approved to run with nobody watching and raises one [burn_alarm] decision carrying the
#: arithmetic, while an attended job keeps running on the recorded warning alone (DECISION F116 D5
#: (3)). ``now`` is the caller's, as this module reads no clock.
def record_burn_trip(job: Any, monitor: JobBurnMonitor, *, persist: Callable[[Any], None],
                     control_root: Any, now: datetime) -> str | None:
    """Keep a NEW trip of *monitor*'s reading on *job*; None, or the pause control's own error
    message when an unattended trip's pause could not be requested, which the caller answers."""
    reading = monitor.reading()
    if reading is None or not reading.tripped:
        return None
    record = job_burn_record(reading)
    if record == job.burn_reading:
        return None
    job.burn_reading = record
    persist(job)
    unattended = job_approved_unattended(job)
    # A ledger write must never stop a healthy job: a failure is logged, the trip stays recorded
    # on the job, and the run goes on.
    try:
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import append_run_event

        append_run_event(resolve_data_root(), job.job_id, event="job_burn_tripped",
                         metadata={**record, "unattended": unattended})
    except _EVENT_WRITE_ERRORS:
        import logging

        logging.getLogger(__name__).error(
            "job_burn_tripped event write FAILED for job %r; the trip stays recorded on the job "
            "and the run continues", job.job_id, exc_info=True)
    if not unattended:
        return None
    from packages.orchestration import pause_control
    from packages.orchestration.escalation import enqueue_task_decision, open_task_decisions
    from packages.orchestration.pingpong_job import TASK_PENDING, TASK_RUNNING

    sentence = job_burn_sentence(record)
    try:
        pause_control.request_pause(job.job_id, reason=f"burn_alarm: {sentence}",
                                    source=BURN_PAUSE_SOURCE, control_root_path=control_root)
    except pause_control.PauseControlError as exc:
        return str(exc)
    question = f"{BURN_DECISION_MARKER} {sentence}"
    # DECISION F116 D9 (1): the park consumes the pause request, so `remedy job unpause` has
    # nothing to lift; the relaunch is what continues the job, and answering only records.
    impact = (f"job {job.job_id} is paused; `remedy job run {job.job_id}` continues it, and "
              f"answering this question only records your choice")
    open_burn = next((r for r in open_task_decisions(job)
                      if str(r.get("question", "")).startswith(BURN_DECISION_MARKER)), None)
    if open_burn is not None:
        open_burn["question"] = question
        open_burn["impact"] = impact
    else:
        target = next((t for t in job.tasks if t.status in (TASK_PENDING, TASK_RUNNING)),
                      job.tasks[0])
        enqueue_task_decision(job, task_id=target.task_id, question=question,
                              options=("resume", "abandon"), safe_default="", impact=impact,
                              now=now)
    persist(job)
    return None

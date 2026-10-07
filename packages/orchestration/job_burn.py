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

Imports from ``burn_detector`` and the standard library only;
``get_config`` is imported INSIDE :func:`job_burn_thresholds_from_config` and
``AUTO_APPROVAL_MODE`` is imported INSIDE :func:`job_approved_unattended`, so
this module stays importable — and testable — with no config layer and no
``job_plan`` import present. ``run_job`` calls this module from its own safe
point (DECISION F116 D4 (1) to (4)): one ``JobBurnMonitor`` per run, a sample
recorded for every counted provider call, and the newest tripped reading kept
on the job.
"""
from __future__ import annotations

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


#: The job runner's own accumulator: one sample per counted provider call,
#: built once per run and read at ``run_job``'s safe point (DECISION F116
#: D4 (1) to (3)).
class JobBurnMonitor:
    """Appends ``BurnSample`` records and evaluates them with the detector."""

    def __init__(self, thresholds: BurnThresholds) -> None:
        self._thresholds = thresholds
        self._samples: list[BurnSample] = []

    #: One sample per call, labelled by its 1-based position among the calls
    #: recorded so far — never by ``at`` — exactly as the detector's own
    #: ``label`` is evidence for a caller and never an index.
    def record_call(self, usage_actuals: Any, *, at: datetime | None) -> None:
        """Reads no clock: ``at`` is the caller's; this module measures nothing."""
        label = len(self._samples) + 1
        self._samples.append(
            BurnSample(amount=_call_amount(usage_actuals), at=at, label=label))

    #: The job's current verdict — ``None`` while there is too little to judge.
    def reading(self) -> BurnReading | None:
        """``evaluate_burn_rate`` over every sample recorded so far."""
        return evaluate_burn_rate(self._samples, self._thresholds)

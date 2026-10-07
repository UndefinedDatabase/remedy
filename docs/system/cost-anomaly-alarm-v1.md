# Cost anomaly alarm (v1)

> F116. The burn alarm: where its one definition of expected spend lives, what it compares, when
> a job's alarm trips, what happens then, and where a person sees a trip.

## What it does

A run can spend far more than it should between two checkpoints without reaching any budget
limit, for example when a model starts looping on very large prompts. The burn alarm watches how
fast a run spends and compares that with what was expected. When the recent spend is far above
the expectation, the alarm trips.

There is one definition of expected spend: `evaluate_burn_rate` in
`packages/orchestration/burn_detector.py`. Two callers use it:

- the job runner, `run_job` in `packages/orchestration/pingpong_job.py`, through the job burn
  monitor in `packages/orchestration/job_burn.py`;
- the mission watchdog's `burn_anomaly` tripwire, `evaluate_burn_anomaly` in
  `packages/orchestration/watchdog.py`, described in [autonomy-watchdog-v1.md](autonomy-watchdog-v1.md).

## What it compares

The detector reads a list of spend samples and answers with a reading: the recent rate, the
expectation, the basis the expectation came from, the multiplier, and whether it tripped. A
reading trips when the recent window spent more than the minimum spend and its rate is strictly
more than the multiplier times the expectation. Every reading names its basis:

| Basis | Rate unit | Expectation |
|---|---|---|
| `trailing_baseline` | per sample | the mean of the run's own earlier measured samples |
| `class_default` | per hour | a configured number of tokens per hour |

A sample that was not measured contributes nothing and does not shrink the window. A negative or
non-finite amount is not a measurement. The detector reads no clock, no file and no
configuration.

## Job runs

A job's samples are its own provider calls: one sample per call the job runner counts, measured
in tokens, input plus output, the same sum its token budget adds. The test provider named `fake`
is never sampled. The thresholds come from five settings, listed with their defaults in
[the environment guide](../guides/environment.md): `job_burn.window`, `job_burn.min_samples`,
`job_burn.multiplier`, `job_burn.min_spend_tokens` and `job_burn.expected_tokens_per_hour`. With
no hourly expectation set, the basis is the run's own trailing baseline.

The job runner reads the monitor at every safe point where no stop fired, which includes the
point before every provider call. When a reading trips and differs from the trip the job already
holds, the runner:

1. saves the reading on the job as `burn_reading`;
2. writes one `job_burn_tripped` event to the job's run log, carrying the reading and whether the
   job runs unattended;
3. when the job's plan was approved to run with nobody watching, which is what
   `remedy do run --yes` records, asks for a pause of the job and raises one decision. Its
   question starts with `[burn_alarm]` and states the numbers in a sentence, its options are
   `resume` and `abandon`, and it has no safe default. A second trip updates that open decision
   instead of adding one. The job parks before its next provider call, and
   `remedy job run <job_id>` continues it; answering the decision records the person's
   choice and does not by itself continue or end the job. When the pause cannot be
   requested, the job is blocked rather than left to burn.

A job a person started keeps running, and the trip is a recorded warning.

## Where a person sees it

- `remedy job show <job_id>` prints a "Burn alarm" block with the sentence, and its JSON carries
  `burn_reading`.
- The report section of `remedy job show <job_id> --full` carries the sentence as `burn_alarm`
  and in its text.
- `remedy job budget <job_id>` prints the full numbers under "recorded burn alarm", whatever
  limits the job has, none included, described in
  [job-budget-enforcement-v0.md](job-budget-enforcement-v0.md).
- The job's run log holds one `job_burn_tripped` event per new trip.

A damaged `burn_reading` in a job file never makes these commands fail; they then show no
sentence.

## Deliberate absences

- Remedy deliberately does not measure the alarm in dollars, because a provider call reports
  tokens far more often than a price, and an alarm that is silent on every unpriced call protects
  nothing.
- Remedy deliberately does not throttle a job's parallel width on a trip, because a job runs one
  task and one provider call at a time.
- Remedy deliberately does not keep a job's samples across a stop and relaunch: a relaunched run
  judges only what it has measured itself, so a short run is never judged.
- Remedy deliberately does not read class expectation bands yet, because the feature that supplies
  them, F074, is not built; until then the hourly expectation is a setting.

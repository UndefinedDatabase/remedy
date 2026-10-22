# Estimate calibration v1: what tasks of each class really cost

> Status (F074, 2026-10-22): the distributions with their floor, their damping and their snapshot
> (T001), the shared estimator's source swap with one seam test per consumer (T002), and the trust
> view `remedy stats calibration` with the calibrated midpoint beside a band in
> `remedy job plan-show` (T003) are built. DECISIONs F074 D1 and D2 in `.agent/decisions.md`; the
> feature is `docs/roadmap/features/T3_F074.md`.

Remedy estimates what a task will cost before it runs: the flight plan's band prices in a job's
rehearsal, the predictive budget check that stops a job before its next task would break the money
limit, and the cost preview a subtree rerun shows before it asks to go on. All three read one shared
estimator. Until F074 that estimator knew only the documented class defaults
(`budget.class_default_tokens_low`, `_medium` and `_high`: 8000, 32000 and 120000 tokens), a stated
assumption per band. Calibration replaces the assumption with a measurement wherever there is enough
of one.

## What is measured
`packages/orchestration/estimate_calibration.py` reads the project's cost ledger,
`<data_root>/projects/<project_id>/ledger.sqlite`. It adds up each task's calls per role, tokens in
plus tokens out, and the cost where every call reported one. It finds the task's class, the routing
vocabulary of `docs/agents/model_routing_policy.md`, in the job's own record, `jobs/<job_id>/job.json`.
For every task class and role it keeps the number of samples and their 20th, 50th and 80th
percentiles, of tokens and of cost. The role `all` is the whole task, every role added up, and it is
the one an estimate reads.

- **The window.** A task counts when its latest call is no older than `budget.calibration_window_days`
  (default 90). Older tasks age out, so a model change shifts the distribution as its old rows leave.
- **The floor.** A class is calibrated once it has `budget.calibration_sample_floor` whole-task
  samples (default 20). Below the floor it keeps its default, class by class: one class can be
  calibrated while its neighbour is not.
- **The damping.** From three samples on, one value in twenty, and at least one, is cut from each
  end of a class's sorted values before the percentiles are taken, so one runaway task cannot pull a
  small class's P80 to itself.
- **What is never guessed.** A task whose job record is gone or names no class is counted as
  unclassified; a task whose calls did not all report their tokens is counted as unmeasured; the
  teacher's calls, which belong to no task, are not read. None of them is filled in.

The measurement is read-only on the ledger: it opens it the way every ledger query does, with
`mode=rw` and `PRAGMA query_only=1`, so it can neither create, migrate nor write it.

## The snapshot
The table is saved as `calibration_snapshot.json` beside the ledger and reused while it is younger
than `budget.calibration_snapshot_max_age_seconds` (default 3600) and was built with the same window
and floor. The next read after that measures the ledger again and replaces the file; nothing
refreshes it in the background. A project with no ledger gets an empty table and no file. A snapshot
that cannot be written leaves the fresh measurement in use.

## How the estimate changes
`resolve_predictive_budget_config` (`packages/orchestration/budget_resolution.py`), which every
consumer already calls with the job's repository, finds the registered project owning that
repository and attaches its table to the config as `calibration`. The consumers themselves change by
one argument, the task's class:

| Consumer | Default (thin class) | Calibrated (fat class) |
|---|---|---|
| A task's band price in a rehearsal, `estimate_cost_band` | the band's default, both ends | the class's P20 to P80 tokens, at the price basis |
| The whole job and a subtree rerun, `subtree_rerun_cost_estimate` | the sum of band defaults | the sum, each calibrated task at its class's range |
| The predictive stop and `remedy job budget`, `predict_next_task_cost` | the band's default | the class's P50 |

Every calibrated number carries the label `calibrated(n)`, `n` the class's sample count: at the
front of a band's basis, inside a subtree's basis beside each task it priced, and as the prediction's
`estimate_basis`. The plan's S, M, L and XL bands stay as they are; for a calibrated class they no
longer set the arithmetic. A class below the floor reads exactly what it read before F074.

The price basis, `budget.price_basis_usd_per_1k_tokens`, still turns tokens into dollars, and without
one nothing is priced. The measured costs are kept beside the tokens for the trust view; they do not
replace the price basis.

## The trust view
`remedy stats calibration` shows what the estimates of one project rest on (`--project` names it;
otherwise `REMEDY_PROJECT` or the working directory does). It prints the window, the floor, when the table
was measured and when the next read measures again, then one row per task class and role, the whole
task first: the tasks measured and their P20, P50 and P80 of tokens and cost, `unpriced` where a call
reported no cost, and in the whole task's row the basis an estimate wears, `calibrated(n)` or
`class default (n of floor)`. It ends with the tasks not counted and why. A project with no ledger,
and a ledger with nothing in the window, each say that every estimate stays on its class default.
`--json` carries the same table, the snapshot's age limit and the calibrated classes. The command
reads the snapshot as every estimate does, so it measures again when the snapshot is old; it never
writes the ledger or a job record.

## The plan's bands
`remedy job plan-show` keeps each task's band, S, M, L or XL, and for a task whose class is
calibrated adds the class, its label and its measured midpoint inside the same parenthesis, for
example `(band S, standard_build calibrated(20) midpoint 10,500 tokens; waits for nothing)`. The
midpoint is read when the plan is shown, so it follows the ledger. A class below the floor shows its
band alone, and the `--json` view of the plan is unchanged. The plan file written when a plan is
made, `plan.md`, is not annotated.

## Deliberate absences
- Remedy deliberately does not split a class by model: a model change ages out through the window.
  A model dimension is a later refinement, noted in the feature file and not built.
- Remedy deliberately does not calibrate a task injected into a running job: its draft carries a plan
  band but no class yet, so `injection_budget_check` keeps the band's default.
- Remedy deliberately does not refresh the snapshot in the background; a read does it when the
  snapshot is old.

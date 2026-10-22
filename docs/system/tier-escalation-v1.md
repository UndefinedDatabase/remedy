# Tier escalation v1: a failing cheaper model hands its next round one tier up

> Status (F296, 2026-10-22): the trigger, the step and the loop's call are built (T001), the record
> of an escalated call in the run's record, its cost booking, the run report and the job's event
> stream (T002a), and the outcome per task class and tier in the evidence and the cost ledger
> (T002b). No benchmark has compared starting cheap with the class tier yet, so the switch stays off
> by default until one does (T003, DECISION F296 D5). DECISIONs F296 D1 to D5 in
> `.agent/decisions.md`; the feature is `docs/roadmap/features/T3_F296.md`.

A task runs in rounds: a builder changes the code, the project's tests run, a reviewer reads the
change, and a repair round follows while the evidence asks for one. Without escalation every round
of a task runs on the models the task started with. With escalation switched on, a task whose
builder keeps failing on a cheaper model tier gets its next repair round on the next tier up, and
its reviewer is raised with it, so the reviewer is never weaker than the builder (the first hard
rule of `docs/agents/model_routing_policy.md`). The tiers are `cheap`, `mid` and `top`, in that
order.

## What moves a task up
Only the rounds the current tier served count, and each kind of evidence is read in this order:

- a test run that ran red because its execution guard stopped it at one of its limits moves the
  next round up at once;
- two red test runs in a row with the same failure move it up instead of ending the repair, which
  is what the repair loop otherwise does with an unchanged failure;
- `model_escalation.after_failures` failing rounds in a row — red tests, or a review that answered
  `needs_repair` or `fail` — move it up; the last round names the reason.

The step is one tier and never down. The run's round cap and repair cap still decide whether a next
round exists, and a stop the job's budget ordered stands. A task already on the top tier stays
there.

## What never moves a task up
A provider that cannot be reached never moves a task: that is model failover's
(`docs/system/model-failover-v1.md`), which keeps the tier and says what served the call.
A run whose builder or reviewer is not one of the configured tier models never escalates, because
its tier is not known; and when the next tier's model cannot be built, the run warns once and the
round's decision stands.

## The configuration

| Key | Default | Meaning |
|---|---|---|
| `model_escalation.enabled` | `false` | The one switch; off, no round moves to another tier |
| `model_escalation.after_failures` | `2` | Failing rounds in a row on one tier before the next round moves up; a value below 1 warns and reads 2 |
| `model_escalation.tiers` | none | Each tier's model: a table of exactly `provider` and `model` per tier; a table that cannot be read warns once and no task escalates |

```toml
[remedy.model_escalation]
enabled = true

[remedy.model_escalation.tiers.cheap]
provider = "ollama"
model = "qwen2.5-coder:7b"

[remedy.model_escalation.tiers.mid]
provider = "claude-cli"
model = "sonnet"
```

## What changes in a run
The escalated round's builder, and its reviewer when raised, are built new on the next tier's model
and start a fresh session: the cheaper model's session is never resumed by another model, and a task
relaunched after an interruption starts again on its configured models without resuming a session
an escalated model opened. A no-progress stop that became the escalated round records its repair
decision with the reason `tier_escalation:no_progress`, and a run that escalated no longer reads as
kept by one builder and one reviewer across its rounds.

Every call an escalated provider served says so in four places:

- the run's record: the call's entry under its round carries `escalation`, holding
  `escalated_from` and `tier` (the tiers the role came from and ran on), `reason`, `round` (the
  round the step began in), `provider` and `model`;
- the cost booking: the call is booked under the escalated tier's model, not the run's configured
  one;
- the run report: `remedy run show` prints one line per escalation after the reviewer, such as
  "Escalation: from round 3 the builder ran on the mid tier instead of cheap, because its tests kept
  failing; the reviewer was raised to mid with it.";
- the job's event stream: a `worker.escalated` event, carrying the same fields, comes before the
  events of the round the step began in.

## What each tier did, per task class
A run whose builder and reviewer both run on configured tier models carries `tier_ladder` in its
record, whether or not escalation is switched on: `enabled`, `builder_tier`, `reviewer_tier` and
`escalations`, one entry per step with its round, its reason and each role's tier before and after.

A job's evidence export turns that into `task_runs/<task>/tier_outcomes.json`, one row per tier the
task's builder ran on: the task's class, the tier and the reviewer's tier, the first and last round
it served, its rounds, the retries among its calls, its cost, and its outcome — `escalated`, with
the trigger as its reason, for a tier the task moved up from, and the run's final status for the
tier that ended it. A tier whose calls did not all report a cost has no cost and the basis
`unknown`; Remedy never invents one.

When the job's project has a cost ledger, the export also mirrors the file into the ledger's
`tier_outcomes` table in `ledger.sqlite`, the same way it mirrors each task's calls: the file is
written first and read back, a re-export replaces its own rows, and a mirror that fails never fails
the export. `query_tier_outcomes` in `packages/orchestration/tier_outcomes.py` answers one summary
per task class and tier — the task runs, how they ended, their rounds, retries and reported cost —
which is what a later trust score reads.

The routing policy itself is not changed by this: its seed table, its hard rules and its benchmark
rule for moving a task class to a cheaper tier still decide which tier a task class starts on;
escalation only decides which tier serves one task's next round.

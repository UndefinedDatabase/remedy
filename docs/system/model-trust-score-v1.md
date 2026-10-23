# Model trust score v1: a model's own record, per role

> Status (F133, 2026-10-23): the trust home `model_trust_score.py` with its four metrics, its
> window, floor and snapshot (T002), the trust view `remedy stats trust` with the matrix, the
> change against the prior window, the cost basis read from the ledger and the clear leader's
> recommendation line per role (T003, round 3), are built. Open: the informational routing note in
> `remedy job plan-show`, the one-home guard and the end-to-end (round 4). The per-tier summary
> beside `tier_outcomes.py` that T003's design sketched is WITHDRAWN (DECISION F133 D3 (3)): the
> per-tier record stays `tier_outcomes.py`'s own. DECISIONs F133 D1, D2 and D3 in
> `.agent/decisions.md`; the feature is `docs/roadmap/features/T7_F133.md`.

Remedy's provider-trust pair (`provider_trust.py`, `provider_trust_verification.py`) was deleted at
`0242c0a3b`: it gated an externally produced patch candidate, keyed by candidate and job, and
computed no metric of a model's own record. This is the replacement, the ONE trust home: for every
model and role a project's jobs have used inside a rolling window, how often its tasks passed, how
many repair rounds they needed, how often its answers could not be read, and what a passed task
cost.

## The model of a call
A ledger row's `calls.model` column is set only when the job path verified the model that actually
answered. In practice that is almost never: the job path never sets `actual_model_verified`, so the
column is empty on every real row today. Where it is empty, the call joins to the
`provider_attempts` entry of the same `seq` its own `call_id` names
(`<job_id>:<task_id>:<seq>`), read from the task run's `provider_evidence.json`, and takes that
entry's own `model`. A call that cannot be joined to an attempt with a non-empty model — an old
one-row-per-task-run row, or a missing evidence file — is counted as UNATTRIBUTED and never
guessed at.

The model that SERVED a role in a task is the model of that role's LAST call in that task (the
highest `seq`), because that call's answer is the one the task ended on; the role's whole cost
rides with the serving model, even when an earlier call in the same task used a different one. An
escalation-aware attribution is a later refinement, not built here.

## The four metrics
Each is a value and the sample count `n` it rests on; `n` is 0 and the value is absent when nothing
qualifies.

- **`pass_quota`** — passes over settled served tasks of that model and role.
- **`repair_need`** — the mean of `repair_rounds_used` over the same tasks.
- **`format_error_rate`** — format errors over EVERY call of that model and role in the window's
  tasks, keyed by each call's OWN model, settled or not. A call is a format error when a later call
  of the same task run, role and round has `is_parse_retry` true, or when it is the last call of
  its role in a task run whose streams hold a call-scope post-mortem of class `parse` for that
  role — each call counted once.
- **`cost_per_pass`** — that role's call cost over its settled served tasks, divided by passes,
  with a basis label that never claims a figure nothing reported, read from the ledger's own
  `cost_basis` column (DECISION F133 D3 (2)): a call is PRICED only when it has a cost figure and a
  basis other than `unknown`. When every call of the sum is priced, the label is the one basis they
  all share — `provider_reported` or `price_table` — and `mixed` when they share none; otherwise
  `tokens` (the value then being tokens per pass) when every call reported its tokens, else
  `unknown` with no value.

A task is SETTLED when its job record gives it a passing status (`TASK_DONE_STATUSES`) or a
failing one (`failed`, `blocked`); every other status — `pending`, `running`, `skipped`, `split`,
`vetoed` — and a task whose record is gone, is UNSETTLED and kept out of `pass_quota`,
`repair_need` and `cost_per_pass`; `format_error_rate` still counts its calls. A row whose settled
served tasks number fewer than the sample floor is marked THIN and is never a leader.

The measurement is read-only on the ledger, the job store and the evidence tree: it opens the
ledger the way every ledger query does, with `mode=rw` and `PRAGMA query_only=1`.

## The settings and the snapshot
Three settings, read through the config authority (env > `remedy.toml` > default), all under
`model_routing.*`: `trust_window_days` (90), `trust_sample_floor` (20) and
`trust_snapshot_max_age_seconds` (3600). The table is saved as `model_trust_snapshot.json` beside
the ledger and reused while it is younger than the age limit and was built with the same window
and floor; the next read after that measures the ledger again and replaces the file. A project
with no ledger gets an empty table and no file.

## The trust view
`remedy stats trust` shows one project's matrix (`--project` names it; otherwise `REMEDY_PROJECT`
or the working directory does). It prints the window, the floor, when the table was measured, then
one row per model and role: the settled tasks (marked `n/floor thin` below the floor), the pass
quota, the mean repair rounds, the format-error rate with its call count, the cost per pass with
its basis and the passes it rests on (R-1431 — e.g. `$0.0123 (provider_reported, 15 passes)`), and
the pass quota's change against the PRIOR window of the same length, signed (`+4pp`/`-4pp`) — `new`
when the model had no row there. Every absent value is a dash, never a zero. It ends with the
unattributed calls and the unsettled tasks, so a reader can see what the matrix could not place,
then one recommendation line per role shown (below). `--role` keeps one role's rows, in both the
text view and `--json`. `--json` carries the current table, the prior window's table, the per-row
change and the per-role recommendations, each with a payload version. A project with no ledger
says so. A malformed `model_routing.trust_*` setting exits 2 and measures nothing.

## The clear leader and its recommendation
DECISION F133 D3 (1). Among a role's rows that are not THIN and have a pass quota, the one with
the highest pass quota is that role's CLEAR LEADER when there are at least two such rows and it
leads the second-highest by at least `TRUST_LEADER_MARGIN`, ten percentage points (0.10);
`trust_leader(table, role)` answers it. A tie, a lead below the margin, or fewer than two eligible
rows means no leader. The view prints exactly one of three wordings, per role shown, after the
matrix:

- a leader: "Recommendation for \<role\>: consider routing it to \<leader\>, whose pass quota is
  \<P\>% over \<n\> settled tasks against \<Q\>% for \<runner-up\>, in the last \<W\> days. Adopt
  it through config and an ADR, as the promotion rule of `docs/agents/model_routing_policy.md`
  requires; trust never changes a route by itself."
- too few eligible rows: "No recommendation for \<role\>: fewer than two models have \<floor\>
  settled tasks in the last \<W\> days."
- no row clears the margin: "No recommendation for \<role\>: no model leads the next by 10 points
  in the last \<W\> days."

The JSON's `recommendations` carries the same answer per role shown: `role`, `leader`,
`runner_up`, the two pass quotas, the leader's settled tasks and the `reason`
(`leader`/`too_few_eligible`/`no_margin`); `leader` and `runner_up` are `null` whenever there is no
recommendation. This is a RECOMMENDATION for a human to read, never an automatic change: Remedy
does not change a route by itself, and adopting one still goes through config and an ADR under
`docs/agents/model_routing_policy.md`'s promotion rule. The informational routing note that reads
this signal inside `remedy job plan-show` ("trust suggests otherwise") is round 4's.

## Deliberate absences
- Remedy deliberately does not read `tier_outcomes.query_tier_outcomes` here: that function writes
  to the ledger on every call and keeps no window, so the per-tier record stays
  `tier_outcomes.py`'s own and this module computes nothing per tier (DECISION F133 D3 (3)) — no
  second aggregation of rounds, retries or cost exists.
- Remedy deliberately does not print an informational routing note in `remedy job plan-show` yet:
  it is round 4's, and until it lands a contradiction between trust and the configured route is
  visible only by reading this view directly.
- Remedy deliberately does not guess a model for an unjoinable call, count an unsettled task
  toward an outcome, or invent a cost basis nothing reported.
- Remedy deliberately does not refresh the snapshot in the background; a read does it when the
  snapshot is old.

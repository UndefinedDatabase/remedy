# Bounded Overnight Preparation v0

A **read-only** planning / readiness / stop-reason / morning-report layer for a
FUTURE bounded overnight run. This block is preparation only — there is **no
executor, no scheduler, no background worker**, and nothing applies code, runs
tests, proposes/applies repairs, calls a provider, or mutates the repo.

Commands (all read-only):

    remedy overnight readiness <job_id> --json
    remedy overnight plan <job_id> --json
    remedy overnight report <job_id> [--markdown] [--json]

## Readiness vs. actual overnight run

- **Readiness** answers: is this job *coherent* to assess, what would Remedy do
  next, what are the limits, what would stop it, what evidence exists/is missing,
  what does the morning checklist look like.
- **`can_run_unattended`** is the stricter question. Under the default
  `BoundedOvernightPolicy` it is **always `False`** — the default policy is
  report-only (`allow_apply=false`, `allow_repair_apply=false`, `allow_provider=
  false`, `allow_revert=false`, `max_cycles=0`). This block must never silently
  enable execution; a future executor block would supply a policy that permits it.

## Truth rules

- Readiness is derived from **durable truth only**: DurableApplyRecord + Snapshot
  Truth + Proof Chain + RunContract/RunUsage + RepairAttempt. **Event presence is
  never proof** — a `snapshot_create_completed` / `test_run_completed` /
  `proof_collected` event does not make the checklist "done".
- **Unknown stays unknown.** Token/cost usage is reported as `unknown`, never
  invented. Missing/stale evidence becomes a blocker or risk.
- Every checklist "done" item carries durable evidence (kind + id). No fake done.

## Stop reasons

Canonical taxonomy (used across readiness/report): human_approval_required,
contract_blocked, permission_missing, budget_exhausted, no_safe_action,
unknown_risk, medium_or_high_risk, snapshot_missing, snapshot_unverified,
evidence_incomplete, test_failed, repair_available, repair_pending_approval,
repair_unavailable, review_findings_open, integrity_failed, provider_unavailable,
unsupported_state, completed_verified.

## Next safe action

`select_overnight_next_action` returns exactly one best action whose command
exists in the command catalog. It never suggests approve unless a pending intent
exists, never suggests continue unless an approved intent + plausible gates exist,
never suggests repair propose unless a failure artifact exists, and never suggests
a provider action. When uncertain it returns a human-review action.

## No automation

This block does NOT: apply code, run tests, propose/apply repairs, revert, call a
provider, auto-approve, relax the contract, raise budgets, or start a background
worker/scheduler. The overnight commands do not mutate the repo or the job.

## How the executor uses this

The [Bounded Overnight Executor v0](bounded-overnight-executor-v0.md) consumes this
readiness report: it is foreground, runs at most one cycle, refuses to run when
execution is not explicitly permitted (`--allow-one-cycle` + an action flag) or a
blocker/PENDING-FAIL review exists, honours the `BoundedOvernightPolicy` limits and
stop reasons, and only ever acts through the existing approval-gated `do continue` /
repair paths — never a new apply bypass.

## See also

- [bounded-overnight-executor-v0.md](bounded-overnight-executor-v0.md) — the foreground one-step executor that acts on this report.
- [do-continue-v1.md](../guides/do-continue-v1.md) — the one-cycle path the executor reuses.
- [repair-loop-v1.md](../system/repair-loop-v1.md) — the approval-gated repair proposal/apply cycle.
- [snapshot-rollback-v1.md](../system/snapshot-rollback-v1.md) — durable snapshot truth.

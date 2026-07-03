# Bounded Overnight Executor v0

> **Status: DEPRECATED** — This document describes a future plan or deprecated subsystem.
> It is kept for historical context. See `docs/roadmap/ROADMAP.md` for current planning.

The first executor that *acts* on a [Bounded Overnight Preparation](bounded-overnight-prep-v0.md)
readiness report. It performs **at most one** bounded, **foreground**, reviewable
step when a human **explicitly** invokes it.

It is **not** a daemon, scheduler, watcher, background worker, or repeating loop.
Every invocation is one run, then it stops.

    remedy overnight run <job_id> [--json]
        [--allow-one-cycle]
        [--allow-apply | --allow-repair-propose | --allow-repair-apply]

## What one run does

    readiness check
      → select ONE catalog-backed safe action
      → (only if policy permits) execute exactly ONE allowed central-service action
      → persist a run record + per-phase checkpoints
      → recompute readiness
      → write a morning-style report
      → stop

Phases (each durably checkpointed): `requested → readiness_before →
policy_checked → action_selected → lease_acquired → action_started →
action_completed → readiness_after → report_written → stopped`.

## Report-only by default

Without `--allow-one-cycle` the run is **report-only**: it selects and reports the
next safe action but executes nothing. This is true even if an action flag is
passed — no flag combination and no config file can enable execution implicitly.

To execute, **both** are required:

1. `--allow-one-cycle` (turns on exactly one bounded cycle, `max_cycles == 1`), and
2. an explicit action flag for what may run.

## Allowed actions (v0)

| Action | Flag | Service | Effect |
|---|---|---|---|
| Apply an approved intent | `--allow-apply` / `--allow-repair-apply` | [`do continue`](../guides/do-continue-v1.md) | one snapshot→apply→test→proof cycle |
| Propose a repair for a failure | `--allow-repair-propose` | [Repair Loop v1](../system/repair-loop-v1.md) | docs-only proposal, **no apply** |
| Inspect / report | (none) | readiness/report | read-only |

There is **no provider/Ollama execution, no auto-approval, no auto-revert, no git
commit**. The executor never runs a generic command and never shells out — it
calls the central services directly, in-process.

## Gates (a run executes only if all pass)

- Policy permits execution (`--allow-one-cycle` + matching action flag, `max_cycles == 1`).
- The selected action is **catalog-backed** and the target **entity exists**.
- **Review findings**: the latest verdict in `.agent/live_review.md` is `PASS` or
  `PASS WITH RISKS` with **no open blocker/high** finding. `PENDING`, `FAIL`, an
  open blocker/high, or an unknown/malformed verdict **blocks** execution.
- For an apply: the test/loop **budget is not exhausted** and there is no open
  blocker/high risk. (A repair *proposal* consumes no test/loop budget, so it is
  gated only on blocker-severity integrity risks.)
- The central service re-checks every permission / approval / RunContract /
  snapshot / test gate. The executor never bypasses or reimplements them.

When a gate blocks, nothing is executed and the run stops with a canonical
**stop reason** (e.g. `human_approval_required`, `review_findings_open`,
`budget_exhausted`, `medium_or_high_risk`, `repair_pending_approval`,
`completed_verified`, `no_safe_action`, `unsupported_state`).

## Idempotency / retry

Re-running is safe. The underlying services are idempotent: a retry after a
successful apply does not re-apply or re-consume test budget, and a repeated
repair proposal returns the existing attempt without duplicating the Fix Task,
Repair Artifact, or Patch Intent. A retry after a blocked run returns the same
stop reason. Run records are append-only — each run has its own `run_id` directory
and is never overwritten.

## Persistence

    .data/workspaces/<job_id>/overnight_runs/<run_id>/record.json   # the run record
    .data/workspaces/<job_id>/overnight_runs/<run_id>/report.md     # morning report
    .data/workspaces/<job_id>/overnight_runs/<run_id>/checkpoints.json

Records and reports carry **safe summaries only** — no raw stdout/stderr, source,
diffs, artifact bodies, secrets, tracebacks, or absolute private paths.

## readiness vs plan vs report vs run

- `overnight readiness` — is this job safe to run unattended? (read-only)
- `overnight plan` — what *would* one bounded cycle do? (dry-run, read-only)
- `overnight report` — morning-style status from current evidence (read-only)
- `overnight run` — actually perform at most one step (report-only unless
  explicitly permitted).

## What it still cannot do (deferred)

- No provider-backed (source-rewriting) repair — the fixture builder is docs-only.
- No multi-cycle / scheduled / background overnight run.
- No automatic approval, revert, contract relaxation, or budget raise.

## See also

- [bounded-overnight-prep-v0.md](bounded-overnight-prep-v0.md) — the readiness layer this consumes.
- [do-continue-v1.md](../guides/do-continue-v1.md) — the one-cycle apply path the executor reuses.
- [repair-loop-v1.md](../system/repair-loop-v1.md) — the approval-gated repair proposal/apply cycle.
- [provider-trust-gate-v0.md](../system/provider-trust-gate-v0.md) — intake of UNTRUSTED external model output into a pending repair intent (no provider execution).
- [repair-request-builder-v0.md](../system/repair-request-builder-v0.md) — provider-agnostic repair request package for any external actor (output re-enters via provider intake).
- [self-dogfood-execution-v0.md](../system/self-dogfood-execution-v0.md) — foreground self-improvement execution; future self-overnight builds on this executor pattern.
- [local-model-advisor-v0.md](../system/local-model-advisor-v0.md) — optional loopback-only advisory critique behind orchestrator routing (advisory-only; never executes or applies).

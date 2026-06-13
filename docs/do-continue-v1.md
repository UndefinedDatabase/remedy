# remedy do --continue v1

One controlled, evidence-backed continuation cycle for an already-approved patch
intent. The user approves a patch, runs one command, and Remedy performs exactly
one development cycle and stops.

Canonical command:

    remedy do continue <job_id> [--intent-id <id>] [--json]

(`do continue` is the subcommand form used by the catalog-driven CLI parser.)

## What it does

A single cycle, in order:

    eligibility → verified snapshot → apply → real test → proof → safe final stop

- **eligibility** — gated by `evaluate_continue_eligibility` (see below).
- **snapshot** — the central `apply_patch_intent` path creates and verifies a
  durable `RepositorySnapshot` before any mutation. No alternate snapshot path.
- **apply** — the approved Markdown patch intent is applied through the central
  apply service. Exactly one `DurableApplyRecord` / `apply_id`.
- **test** — the central Test Execution Service runs the real discovered test
  command (budget-gated). Usage is recorded once.
- **proof** — the Proof Chain is rebuilt from authoritative snapshot truth.
- **final stop** — the cycle stops. No further automatic work.

## What it never does

- No automatic repair. No automatic revert. No multi-cycle / overnight loop.
- No real provider / Ollama execution. No UI, browser, git commit, MCP, or
  dependency changes.
- No `shell=True`, no `git reset/checkout/clean`, no force revert.
- No raw source, diff, snapshot blob, output, secrets, or tracebacks in any
  public surface (text or JSON).

## Eligibility

`remedy do continue` proceeds only when **all** of these hold; otherwise it stops
with `blocked_ineligible` and a real next-safe action:

- the job exists;
- exactly one approved intent, or an explicit `--intent-id` (multiple approved
  intents require `--intent-id` — implicit selection is refused);
- the intent is approved and not rejected;
- no conflicting unresolved apply from a different intent;
- `repo_generated_write` permission is granted;
- the persisted Run Contract allows the apply action (`patch_apply`);
- `stop_before_apply` is `false`;
- a safe target repository is attached (`remedy job attach-repo`);
- the patch structure is valid;
- `repo_test_run` permission is granted and `max_test_runs > 0`;
- no continuation is already active (lease free).

These gates live in central services (permissions, Run Contract, snapshot, test),
not only in the CLI.

## Stop reasons

| stop_reason | meaning | next safe action |
|---|---|---|
| `completed_verified` | applied, tested passed, proof verified | none |
| `test_failed_repair_available` | test failed/timed out | `remedy repair start <job> <failure_artifact_id> --json` |
| `evidence_incomplete` | apply may have succeeded but durable record / event / test evidence degraded | `remedy change proof <job> --json` |
| `test_blocked` | test could not run (no command / blocked) | `remedy test discover <job> --json` |
| `snapshot_failed` | snapshot could not be created/verified | `remedy snapshot inspect <job> --json` |
| `apply_failed` | apply blocked by a service gate | `remedy change proof <job> --json` |
| `blocked_ineligible` | an eligibility gate failed | gate-specific action |
| `lease_unavailable` | a continuation is already active | `remedy change proof <job> --json` |

A failed test never auto-repairs and never auto-reverts — it exposes the Failure
Artifact and the repair command. Degraded evidence can **never** return
`completed_verified`.

## Crash-safe and idempotent

Durable phase checkpoints (`workspaces/<job>/do_continue/checkpoints.json`) plus
authoritative snapshot truth make a retry resume rather than repeat:

- a retry after a successful apply does **not** apply again (no second snapshot,
  no second `DurableApplyRecord`);
- a retry after a completed test does **not** consume test budget again;
- a retry after a failure does **not** create a duplicate Failure Artifact or
  Fix Task.

A single `ContinuationLease` (keyed job → repo → intent, deterministic order,
released on every exit, stale-recoverable via `flock`) prevents two concurrent
continuations for the same job, repository, or intent.

## Surfaces

- **Events**: `do_continue_requested`, `do_continue_started`,
  `do_continue_snapshot_verified`, `do_continue_applied`,
  `do_continue_test_started`, `do_continue_test_completed`,
  `do_continue_proof_built`, `do_continue_stopped` — safe IDs/status only, with
  event-persistence status surfaced (no silent loss).
- **Progress Ledger**: continuation eligible, snapshot verified, apply completed,
  test passed/failed, proof verified, evidence incomplete.
- **Feature Planner**: test failure → repair; evidence incomplete → manual
  review; snapshot failure → snapshot investigation; test budget → contract
  review. No automatic action or policy relaxation.
- **Review Bundle**: `continuation_summary.json` (phase, checkpoints, apply/test/
  proof/evidence status, stop reason, next-action availability, safe IDs).

## Related

- [snapshot-rollback-v1](snapshot-rollback-v1.md) — snapshot truth, durable apply
  records, revert.
- [real-test-execution-v1](real-test-execution-v1.md) — the Test Execution Service.
- [run-contract-v1](run-contract-v1.md) — apply/test gates and budgets.
- [do-run-v1](do-run-v1.md) — the pre-apply `remedy do run` flow this continues.
- [repair-loop-v0](repair-loop-v0.md) — the legacy repair path.
- [bounded-overnight-prep-v0](bounded-overnight-prep-v0.md) — read-only readiness/
  report layer; a future executor reuses this one-cycle path under a bounded policy.
- [repair-loop-v1](repair-loop-v1.md) — the bounded, approval-gated repair
  proposal offered when a continuation test fails. An **approved repair intent**
  is applied through THIS same path: `remedy do continue <job_id> --intent-id
  <repair_intent_id>`. No repair apply bypass; after the cycle the repair attempt
  is reconciled (tested_passed/tested_failed) and the original failure is resolved
  only with a verified snapshot + linked passing test + proof (source_fix only).

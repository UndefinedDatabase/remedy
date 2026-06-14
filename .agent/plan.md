# Plan — Steps 1275-1304: Bounded Overnight Executor v0

## Goal
First Bounded Overnight Executor: Remedy may perform AT MOST ONE bounded,
foreground, reviewable step when EXPLICITLY invoked. Never a daemon, scheduler,
loop, or hidden background process. Answers: what would I do? am I allowed? did
I do it? why stop? what evidence? what next?

## Current Step
1276 — Executor models (overnight_executor.py)

## Steps
- [x] 1275: Mainline reconciliation + clean branch (PR #55 merged; scope→1275-1304)
- [ ] 1276: Executor models (Run Request/Result/Record/Checkpoint/Phase/Decision/Lease/Mode)
- [ ] 1277: Explicit execution policy (execution_enabled, max_cycles=1, --allow-one-cycle)
- [ ] 1278: Executor lease (foreground; same job/repo/intent; stale recoverable; release on exit)
- [ ] 1279: Run record persistence (atomic, append-only, no overwrite, no raw)
- [ ] 1280: Phase checkpoints (durable per phase; retry from durable truth)
- [ ] 1281: Action selection contract (only select_overnight_next_action; re-validate)
- [ ] 1282: Action adapters (do_continue, repair_propose, read-only report; no shell/subprocess)
- [ ] 1283: CLI overnight run (report-only default; --allow-one-cycle + explicit flags)
- [ ] 1284: Policy gate enforcement (central re-check, not readiness alone)
- [ ] 1285: Review-findings source (parse .agent/live_review.md; PENDING/FAIL block)
- [ ] 1286: Stop reason enforcement (canonical taxonomy)
- [ ] 1287: Morning report output (readiness report + executor record)
- [ ] 1288: Idempotency (retry never double-apply/test/propose/duplicate report)
- [ ] 1289: Progress Ledger integration
- [ ] 1290: Feature Planner integration (no auto policy relaxation)
- [ ] 1291: Review Bundle overnight_run_summary.json
- [ ] 1292: Cockpit integration (read-only; no buttons; no fake running state)
- [ ] 1293: CLI runtime tests (default report-only; flags gate; PENDING blocks)
- [ ] 1294: Executor unit tests
- [ ] 1295: Redaction tests
- [ ] 1296: Architecture guards (no subprocess/provider/scheduler/git/UI mutation)
- [ ] 1297: Documentation (bounded-overnight-executor-v0 + cross-links)
- [ ] 1298: Targeted tests + full pytest once
- [ ] 1299: Live review
- [ ] 1300: PR discipline
- [ ] 1301: Product readiness update
- [ ] 1302: Final handoff
- [ ] 1303: Merge recommendation (executor alone; no provider stacking)
- [ ] 1304: Hard completion criteria

## Hard rules
- Foreground, explicitly invoked ONLY. No daemon/scheduler/watch/background/loop.
- Default behavior report-only; execution requires --allow-one-cycle + explicit
  action flag (--allow-apply / --allow-repair-propose / --allow-repair-apply).
- max_cycles == 1 hard limit. Exactly one allowed service action per invocation.
- No provider/Ollama. No auto-approval. No auto-revert. No git commit.
- No subprocess/CLI for executing Remedy commands — call central services directly.
- No shell=True. No background pytest (scripts/remedy_pytest.sh; full suite once).
- Idempotent: retry never double-applies/tests/proposes or duplicates reports.
- Every next action catalog-backed + entity-backed. No event-only truth.
- No raw stdout/stderr/source/diff/artifact-body/secrets/tracebacks/abs paths.
- PENDING/FAIL review verdict or open blocker/high finding blocks execution.

## Next block
Provider-backed Repair Builder v0 OR Provider Trust Verification.

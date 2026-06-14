# Plan — Steps 1275-1304: Bounded Overnight Executor v0

## Goal
First Bounded Overnight Executor: Remedy may perform AT MOST ONE bounded,
foreground, reviewable step when EXPLICITLY invoked. Never a daemon, scheduler,
loop, or hidden background process. Answers: what would I do? am I allowed? did
I do it? why stop? what evidence? what next?

## Current Step
1298 — Full pytest once (post targeted green)
1297 — Documentation (then full suite 1298)

## Steps
- [x] 1275: Mainline reconciliation + clean branch (PR #55 merged; scope→1275-1304)
- [x] 1276: Executor models (Run Request/Result/Record/Checkpoint/Phase/Decision/Lease/Mode)
- [x] 1277: Explicit execution policy (executor_execution_permitted, max_cycles=1, --allow-one-cycle)
- [x] 1278: Executor lease (foreground; job + repo-when-mutating; stale recoverable; release on exit)
- [x] 1279: Run record persistence (atomic, append-only, no overwrite, no raw)
- [x] 1280: Phase checkpoints (durable per phase)
- [x] 1281: Action selection contract (select_overnight_next_action + re-validate catalog/entity/policy)
- [x] 1282: Action adapters (do_continue, repair_propose, read-only report; no shell/subprocess)
- [x] 1283: CLI overnight run (report-only default; --allow-one-cycle + explicit flags)
- [x] 1284: Policy gate enforcement (review/budget/risk gate; central re-check via services)
- [x] 1285: Review-findings source (parse .agent/live_review.md; PENDING/FAIL/unknown block)
- [x] 1286: Stop reason enforcement (canonical taxonomy via _canonical)
- [x] 1287: Morning report output (readiness report + executor record)
- [x] 1288: Idempotency (delegated services idempotent; append-only records)
- [x] 1289: Progress Ledger integration (overnight run items)
- [x] 1290: Feature Planner integration (run blockers; no auto relaxation)
- [x] 1291: Review Bundle overnight_run_summary.json (REQUIRED_SECTIONS 16)
- [x] 1292: Cockpit overnight_run section (read-only)

- [x] 1293: CLI runtime tests (report-only default; flag/review/budget gates)
- [x] 1294: Executor unit tests
- [x] 1295: Redaction tests
- [x] 1296: Architecture guards
- [x] 1297: Documentation (bounded-overnight-executor-v0 + cross-links)
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

# Plan — F018 Budgets & Stop Conditions — Full Implementation

## Goal
Complete F018 repair: wire budgets end-to-end from CLI through evaluation
to stop integration. Five logically scoped commits, fresh Evidence, one
READY_FOR_REVIEW ZIP.

## Scope 1 — Real budget persistence/config/CLI/RunManifest
- Remove private TOML/env authority from budget_resolution.py; route through config.py
- Wire _cmd_create_job() to consume budget flags, validate, resolve, persist Job(budgets=...)
- Wire _cmd_do() to consume budget flags for do run and dry-run
- Add budgets field to RunManifestV1 with schema/drift/round-trip tests
- Malformed config blocks (not silently returns None)
- Tests: extend test_job_budgets.py + test_run_manifest.py

## Scope 2 — Canonical actual-counter collection + budget authority consolidation
- Public pure aggregation from PingPongResult.provider_attempts / _aggregate_usage_actuals
- Closed counter contract validation: nonneg, no booleans, measured+unmeasured==provider_calls
- Wall-clock derivation from started_at+now instead of arbitrary elapsed_seconds
- RunContract.max_tokens → delegates to JobBudgets.max_total_tokens when both set
- RunContract.max_runtime_seconds → delegates to JobBudgets.max_wall_clock_minutes when both set
- One canonical authority, no contradictory answers
- Tests: extend test_budget_guard.py

## Scope 3 — Unified safe-point stop integration + decision idempotency
- should_stop() in safe_points.py: operator stop → budget → continue
- Three-call limit stops before call four
- Stop persistence via F011 path (StopSignal with budget reason)
- Decision queue entry (type="token_budget", extend/abandon)
- Past deadline at start refuses work
- Postmortem class BUDGET_EXHAUSTED wired
- Tests: test_budget_stop_integration.py

## Scope 4 — Budget display, regression proof, docs, final Evidence
- `remedy job budget <id>` CLI command (human + JSON output)
- Full test suites for all scopes
- Docs updates (T0_F018.md built state, STATUS.md)
- Fresh Evidence bundle + READY_FOR_REVIEW ZIP

## Current Step
Scope 1: wiring budget_resolution.py through config.py, CLI handlers, RunManifest.

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F017 [x]. F018 [~]. F146 [ ].

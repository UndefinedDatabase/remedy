# Plan — F018 Budgets & Stop Conditions — Full Rebuild

## Goal
Close all 9 external review blocking findings. Wire budgets end-to-end
from CLI through durable persistence, live intra-task counters, F011
stop integration, and RunManifest identity. Five scoped commits, fresh
Evidence, one READY_FOR_REVIEW ZIP.

## Scope 1 — Branch cleanup + durable budget persistence
- Backup current mixed branch, reset to implementation-only commits
- Add `budgets` field to `JobPlan` dataclass
- Wire budgets through `_export_job()` / `_import_job()`
- Wire `_cmd_do_pingpong()` → `run_pingpong()` budgets parameter
- Wire `run_job()` budgets parameter from `Job.budgets` to `JobPlan`
- Fail-closed config: malformed TOML/env raises BudgetConfigError
- BudgetCounters strict validation (reject bool elapsed_seconds,
  non-datetime evaluated_at, non-str actual_sources, started_at > evaluated_at)
- Tests for persistence round-trip, CLI wiring, config fail-closed

## Scope 2 — RunManifest budget identity + strict decoding
- Add `budgets` to `logical_input_projection()`
- Deserialize budgets in `from_trusted_json()`
- Add budgets to `_bind_artifact_refs()` if applicable
- Strict decoder validates closed JobBudgets schema on budgets dict
- Tests for identity inclusion, round-trip, schema validation

## Scope 3 — Live intra-task counters + F011 durable budget stops
- Mutable counter accumulator updated BEFORE each provider call
  (not after task) so pre-call safe points see all prior attempts
- Budget stops use `_stop_job()` F011 transaction (stop archive,
  postmortem, event, manifest, persist, acknowledge) instead of
  JOB_BLOCKED with job.error
- Past deadline blocks before first call (pre-work stop)
- Decision queue entry for budget exhaustion
- Tests: three-call-limit stops before call four, deadline-at-start,
  durable stop path, decision idempotency

## Scope 4 — Honest CLI + production E2E + docs
- `remedy job budget` typed display states: available/no_runs/
  partial/corrupt/unavailable (never invents zeros)
- `_collect_job_counters` handles real actuals from persisted runs
- JSON output: counters or explicit null, never structured zeros
- Real E2E tests (budget wiring, fail-closed config, honest display)
- Docs updates (T0_F018.md built state, STATUS.md)

## Scope 5 — Canonical Evidence + final package
- Three canonical manual-completion tasks (not five custom ones)
- Fresh token_truth.json with real test counts
- One READY_FOR_REVIEW ZIP
- Change provenance gate

## Current Step
Scope 4 — DONE. Next: Scope 5

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].

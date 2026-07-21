# Plan — F018 Runtime-Authority & Final-Packaging Round

## Goal
Close 9 external reproductions from the reviewed ZIP. All source fixes,
real production tests, truthful Evidence, one canonical full review ZIP.

## Status: IN PROGRESS

## Scope 1 — Final branch and package authority
- [x] Inspect branch, record base/HEAD/commit count
- [ ] Ensure clean tree before Evidence
- [ ] Full review ZIP via make_review_zip.sh pipeline

## Scope 2 — Immutable budget persistence and project context
- [x] _cmd_do_job_run: use persisted JobPlan budgets, do not re-read CWD
- [x] _cmd_create_job: pass project repo_path to resolve_job_budgets
- [x] _cmd_do: pass project_root=repo to resolve_job_budgets

## Scope 3 — Resumed Actuals and strict counters
- [x] run_job: seed accumulators from persisted budget_actuals on resume
- [x] run_job: persist budget_actuals before ALL stop paths
- [x] collect_counters_from_actuals: reject bool/float/string coercion
- [x] BudgetCounters: reject naive evaluated_at, empty source strings
- [x] closed source vocabulary (_VALID_SOURCES)

## Scope 4 — JobPlan Decision, display and stop identity
- [x] _cmd_job_budget: dual Core Job / JobPlan lookup
- [x] decision_queue: support JobPlan (has .job_id not .id)
- [x] Pre-work stop: allocate episode before computing budget identity

## Scope 5 — Real runtime verification, docs and canonical package
- [x] RunManifest: normalize deadline to UTC, empty dict → null
- [x] runtime_integration_gate: 8 real test bindings added
- [x] Replace inspect-only tests with real runtime tests (55 pass)
- [x] Update T0_F018.md
- [ ] Update context.md
- [ ] Canonical Evidence + full review ZIP

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].

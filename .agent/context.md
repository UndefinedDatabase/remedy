# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 425-434: Real local model quality — complete.

## Completed
- Timeline truth: removed fake 28-dot micro events
- Explicit model checks: --example flag, --ollama requires REMEDY_REAL_OLLAMA_EVAL=1
- Task set v2: 8 cases (missing_function, wrong_return, import_fix, test_repair, unsafe_path, stale, no_op, multi_file)
- Scorecard v2: expected outcome tracking, multi-file case
- Failure advice: prose/malformed/clean pattern detection
- Prompt trial: compare_profiles, export_trial_result_json
- Model profile: confidence tiers, fixture=low
- CLI report: --example/--ollama/--json with model_profile

## Resource-Safety Rules (permanent)
- Never run pytest in background
- Always use scripts/remedy_pytest.sh for pytest execution
- Full pytest tests/ at most once per worker block

## Constraints
- UI remains read-only
- No fake timeline events
- No raw content in reports

## Recommended Next Block
Steps 435-444 — Background Worker v1 And Job Lifecycle

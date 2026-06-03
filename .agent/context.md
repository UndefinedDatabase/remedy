# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 391-398: Real model quality loop — complete.

## Completed
- 3 real prompt profiles: strict_minimal, repair_aware, context_rich (genuinely different text)
- OllamaBuilder wired to accept prompt_profile parameter
- 7 task cases: missing_function, wrong_return, import_fix, test_failure_repair, unsafe_path, stale_context, no_change_needed
- Quality scorecard: usable_patch_rate, safe_rejection_rate, outcome_accuracy, avg_tokens, avg_latency
- Failure-pattern recommendations: prose, malformed, over-rejection, under-rejection, missing_patch
- Model profile recommendation: confidence tiers (low/medium/high), fixture vs real distinction
- Eval CLI: --fixture (simulated), --ollama (real when REMEDY_REAL_OLLAMA_EVAL=1)
- R-15002 fixed: over-rejection/under-rejection split correctly
- All exports: safe metadata only, redaction field on every record

## Resource-Safety Rules (permanent)
- Never run pytest in background
- Never run multiple pytest commands in parallel
- Always use scripts/remedy_pytest.sh for pytest execution
- Full pytest tests/ at most once per worker block

## Constraints
- UI remains read-only
- No real Ollama required for normal CI tests
- No raw content in eval records, scorecard, or recommendations
- source_apply requires permission + approved intent

## Recommended Next Block
Steps 399-406 — Project-Level Brain And Multi-Run Learning

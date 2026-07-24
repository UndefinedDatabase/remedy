# Handoff — F013 Job intake (repair round: R-0116..R-0117)

## State
- Branch: `feature/f013-job-intake`
- Last commit: `e97baf1` (R-0117)
- Total commits on branch: 18
- Both findings fixed: R-0116, R-0117

## Repair Commits — changed-files tables

### `693fb23` fix(f013): deduplicate intake provider onto OllamaPlanner.raw_call (R-0116)
| File | Change |
|------|--------|
| packages/providers/ollama_planner/provider.py | +`raw_call(prompt, *, schema, system=None)` — single config surface; `plan_raw` delegates to it |
| packages/orchestration/intake.py | `make_provider_call_fn` rewritten: instantiates OllamaPlanner, closes over `raw_call`; deleted duplicated host/model/timeout/fallback resolution |
| tests/test_ollama_provider.py | +7 tests (TestRawCall: delegation, system passthrough, options, env model) |
| tests/orchestration/test_intake.py | +1 test (env model reaches chat via make_provider_call_fn); refactored fake helper |
| .agent/decisions.md | Timeout removal decision recorded |

### `e97baf1` fix(f013): provider_error label says "provider error" not "unavailable" (R-0117)
| File | Change |
|------|--------|
| apps/cli/commands/do_cmd.py | Line 282: `"provider unavailable"` → `"provider error"` for `fallback_reason == "provider_error"` |
| tests/cli/test_golden_path.py | +1 test (`test_provider_error_label_distinct_from_unavailable`) |

## Verification

### R-0116 — post-commit test run
```
$ python3 -m pytest tests/test_ollama_provider.py tests/orchestration/test_intake.py \
    tests/cli/test_golden_path.py tests/schemas/test_job_intake.py tests/test_storage.py -q
1 failed, 131 passed in 16.49s
```
1 failure = pre-existing `test_fallback_to_default_when_no_env_vars` (env var bleed in test ordering — same on main, passes in isolation).

### R-0117 — post-commit test run (final)
```
$ python3 -m pytest tests/test_ollama_provider.py tests/orchestration/test_intake.py \
    tests/cli/test_golden_path.py tests/schemas/test_job_intake.py tests/test_storage.py -q
1 failed, 132 passed in 16.63s
```
Same 1 pre-existing failure.

### Test counts before/after this round
| Suite | Before | After |
|-------|--------|-------|
| test_ollama_provider.py | 12 | 19 (+7) |
| test_intake.py | 36 | 37 (+1) |
| test_golden_path.py | 38 | 39 (+1) |
| test_job_intake.py | 26 | 26 |
| test_storage.py | 12 | 12 |
| **Total** | **124** | **133** |

Note: prior round ended at 112 across 4 suites (did not include test_ollama_provider.py). This round adds test_ollama_provider.py to the verification set, hence 124 baseline (112 + 12).

### Ruff — touched files
```
$ python3 -m ruff check packages/providers/ollama_planner/provider.py \
    packages/orchestration/intake.py tests/test_ollama_provider.py \
    tests/orchestration/test_intake.py apps/cli/commands/do_cmd.py \
    tests/cli/test_golden_path.py
Exit 1 — 6 errors, ALL in do_cmd.py (main parity 6=6, zero new)
```

## Reused functions
- **Provider call**: `OllamaPlanner.raw_call()` in `packages/providers/ollama_planner/provider.py`
- **Intake provider factory**: `make_provider_call_fn()` in `packages/orchestration/intake.py` (now delegates to OllamaPlanner)
- **Evidence writer**: `build_trace_entry()` + `write_trace_jsonl()` from `packages/orchestration/prompt_trace.py`; `RunLogWriter` from `packages/orchestration/run_log.py`

## decisions.md entry
Added: "R-0116 — intake timeout removed; OllamaPlanner.raw_call is the single config surface" — timeout no longer hardcoded, Ollama default applies; if needed, use config (env var or toml) same as temperature/num_predict.

## Next Expected Action
Reviewer reviews repair round (R-0116..R-0117).

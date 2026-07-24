# Handoff — F013 Job intake (repair round: R-0111–R-0115)

## State
- Branch: `feature/f013-job-intake`
- Last commit: `e245edb` (R-0115)
- Total commits on branch: 14
- All 5 findings fixed: R-0112, R-0114, R-0113, R-0111, R-0115

## Repair Commits — changed-files tables

### `8cb5a28` fix(f013): wire LLM intake attempt with provider fallback + evidence (R-0112)
| File | Change |
|------|--------|
| apps/cli/commands/do_cmd.py | Wire `make_provider_call_fn()` → `run_intake()`, evidence via `write_trace_jsonl` |
| packages/orchestration/intake.py | +`make_provider_call_fn()`: Ollama-backed call_fn, `timeout=15.0`, `client.list()` health check |
| tests/cli/test_golden_path.py | +3 tests (TestLLMIntakeWiring), `_run_do` default `--no-llm`; 38 golden-path tests |
| tests/orchestration/test_intake.py | +2 tests (TestMakeProviderCallFn); 36 intake tests |

### `63261e3` fix(f013): force truncated_input=True when prompt was truncated (R-0114)
| File | Change |
|------|--------|
| packages/orchestration/intake.py | Post-parse override: force `truncated_input=True` when `_truncate_mission` truncated |
| tests/orchestration/test_intake.py | +3 tests (TestTruncatedInputOverride); 36 intake tests |

### `8db3162` fix(f013): use specified P6 intake labels + JSON fallback_reason (R-0113)
| File | Change |
|------|--------|
| apps/cli/commands/do_cmd.py | Labels: "intake: llm", "intake: heuristic (forced by --no-llm)", "intake: heuristic fallback (provider unavailable)"; JSON `intake.fallback_reason` |
| tests/cli/test_golden_path.py | Update probes to match P6 labels |

### `9c152e8` fix(f013): add human-readable intake block to job show (R-0111)
| File | Change |
|------|--------|
| apps/cli/commands/job.py | +`_print_intake_block()`: goal, context_refs, constraints, acceptance, clarifications, schema_v, truncated/dropped when nonzero |
| tests/cli/test_golden_path.py | +2 tests (intake block display, legacy silent); 38 golden-path tests |

### `e245edb` fix(f013): E731 lambda→def in job.py + ruff parity verified (R-0115)
| File | Change |
|------|--------|
| apps/cli/commands/job.py | `lambda s: print(s, …)` → `def p(s)` |

## Verification

### Final test run (all touched suites)
```
$ python3 -m pytest tests/orchestration/test_intake.py tests/cli/test_golden_path.py \
    tests/schemas/test_job_intake.py tests/test_storage.py -v --tb=short
112 passed in 19.18s
```

Test counts before/after repair round:
| Suite | Before | After |
|-------|--------|-------|
| test_intake.py | 31 | 36 (+5) |
| test_golden_path.py | 36 | 38 (+2) |
| test_job_intake.py | 26 | 26 |
| test_storage.py | 12 | 12 |
| **Total** | **105** | **112** |

### Ruff — all 18 touched files
```
$ python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/do_cmd.py \
    apps/cli/commands/job.py apps/cli/grouped.py packages/core/models.py \
    packages/orchestration/intake.py packages/orchestration/schemas/__init__.py \
    packages/orchestration/schemas/models.py tests/cli/test_golden_path.py \
    tests/orchestration/test_intake.py tests/schemas/__init__.py \
    tests/schemas/test_job_intake.py tests/test_storage.py
Exit 1 — 6 errors, ALL in do_cmd.py (main parity: 6=6, zero new)
```
do_cmd.py pre-existing (verified on main): I001@3, I001@611, UP037@1157, UP037@1334, UP037@2329, I001@2475.

## Reused functions
- **Provider call**: `make_provider_call_fn()` in `packages/orchestration/intake.py`
- **Evidence writer**: `build_trace_entry()` + `write_trace_jsonl()` from `packages/orchestration/prompt_trace.py`; `RunLogWriter` from `packages/orchestration/run_log.py`

## Next Expected Action
Reviewer reviews repair round (R-0111–R-0115).

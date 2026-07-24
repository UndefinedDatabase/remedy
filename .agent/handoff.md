# Handoff — F013 Job intake (T001–T003)

## State
- Branch: `feature/f013-job-intake`
- Status: T001–T003 complete, pushed, no PR yet
- Total commits on branch: 7

## Commits

### `d7e9bc0` chore(f013): claim + session reset
| File | Change |
|------|--------|
| docs/roadmap/STATUS.md | `[ ]` → `[~]` for F013 |
| .agent/live_review.md | Reset for F013 |
| .agent/plan.md | Reset for F013 |

### `0ab5496` feat(f013): JobIntake schema + job field + tests (T001)
| File | Change |
|------|--------|
| packages/orchestration/schemas/models.py | +JOB_INTAKE_SCHEMA_V, +IntakeClarification, +JobIntake, registry entry |
| packages/orchestration/schemas/__init__.py | Re-export JOB_INTAKE_SCHEMA_V, IntakeClarification, JobIntake |
| packages/core/models.py | +intake: dict[str, Any] \| None = None on Job |
| tests/schemas/__init__.py | New package init |
| tests/schemas/test_job_intake.py | 25 tests (round-trip, rejection, registry, schema size) |
| tests/test_storage.py | +2 tests (backward-compat without intake, roundtrip with intake) |

### `ebd54e8` chore(f013): T001 handoff with recon report
| File | Change |
|------|--------|
| .agent/handoff.md | T001 handoff with recon |

### `794d500` chore(f013): persist R-0110
| File | Change |
|------|--------|
| .agent/live_review.md | R-0110 finding persisted |

### `5739cf0` fix(f013): remove schema-level clarifications cap, add dropped count (R-0110)
| File | Change |
|------|--------|
| packages/orchestration/schemas/models.py | Remove max_length=5 from clarifications, +dropped_clarifications field |
| tests/schemas/test_job_intake.py | Replace rejection test with acceptance test for >5 clarifications (+1 test, 26 total) |

### `5121250` feat(f013): intake module with LLM + heuristic paths (T002)
| File | Change |
|------|--------|
| packages/orchestration/intake.py | New: run_intake, heuristic_intake, IntakeResult, truncation |
| tests/orchestration/test_intake.py | 31 tests (heuristic, LLM valid/retry/failure, truncation, hooks) |
| .agent/decisions.md | T002a extraction skip decision |

### `863f8c7` feat(f013): wire intake in do path + golden-path smoke (T003)
| File | Change |
|------|--------|
| apps/cli/commands/do_cmd.py | Wire heuristic_intake before plan_job, +no_llm param, intake in output |
| apps/cli/command_catalog.py | +--no-llm flag on do.run |
| apps/cli/grouped.py | --no-llm added to bare-allowed set |
| tests/cli/test_golden_path.py | +3 tests (--no-llm, intake persistence, context_refs), +2 assertions |
| .agent/plan.md | T001–T003 checked |

## Verification

### tests/orchestration/test_intake.py (31 tests — new)
```
python3 -m pytest tests/orchestration/test_intake.py -q
...............................                                          [100%]
31 passed
```

### tests/schemas/test_job_intake.py (26 tests)
```
python3 -m pytest tests/schemas/test_job_intake.py -q
..........................                                               [100%]
26 passed
```

### tests/test_storage.py (12 tests)
```
python3 -m pytest tests/test_storage.py -q
............                                                             [100%]
12 passed
```

### tests/orchestration/schemas/test_schemas.py (44 tests)
```
python3 -m pytest tests/orchestration/schemas/test_schemas.py -q
............................................                             [100%]
44 passed
```

### tests/cli/test_golden_path.py (36 tests — was 31, +5 assertions +3 new)
```
python3 -m pytest tests/cli/test_golden_path.py -q
....................................                                      [100%]
36 passed
```

### ruff (touched files)
```
python3 -m ruff check packages/orchestration/intake.py tests/orchestration/test_intake.py \
  apps/cli/grouped.py apps/cli/command_catalog.py tests/cli/test_golden_path.py
All checks passed!
```

## Key Decisions
- T002a (transport extraction of `_call_with_retry`) skipped: deeply coupled
  to PingPongResult/private helpers; `run_structured_call` is already importable
  and sufficient for intake. Decision in `.agent/decisions.md`.
- `--no-llm` flag whitelisted in bare-detection (grouped.py) so it stays on the
  golden path. Currently a no-op (heuristic is already the default with no LLM
  provider); ready for when LLM intake provider is wired.

## Open Findings
R-0110 persisted (status: Done: R-0110, reviewer pending).

## Next Expected Action
Reviewer reviews T001–T003 bundle.

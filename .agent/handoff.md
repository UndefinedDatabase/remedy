# Handoff — F013 T001 (Job intake schema)

## State
- Branch: `feature/f013-job-intake`
- Status: T001 complete, not pushed, no PR
- Total commits on branch: 2

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

## Schema Fields (as implemented)

**JobIntake** (`_Structured`, version `ji1`):
| Field | Type | Default |
|-------|------|---------|
| schema_v | Literal["ji1"] | (required) |
| goal | str | (required) |
| context_refs | list[str] | [] |
| constraints | list[str] | [] |
| acceptance_hints | list[str] | [] |
| truncated_input | bool | False |
| clarifications | list[IntakeClarification] | [] (max 5) |

**IntakeClarification** (`_Strict`):
| Field | Type |
|-------|------|
| question | str |
| default_answer | str |
| impact | str |

**Job.intake**: `dict[str, Any] | None = None` — stored as serialized dict,
not as a typed model (core layer stays independent of orchestration schemas).

## Verification

### tests/schemas/test_job_intake.py
```
$ python3 -m pytest tests/schemas/test_job_intake.py -q
.........................                                                [100%]
25 passed in 0.12s
```

### tests/test_storage.py
```
$ python3 -m pytest tests/test_storage.py -q
............                                                             [100%]
12 passed in 0.13s (was 10, +2 new)
```

### tests/orchestration/schemas/test_schemas.py
```
$ python3 -m pytest tests/orchestration/schemas/test_schemas.py -q
............................................                             [100%]
44 passed in 0.15s
```

### ruff (touched files)
```
$ python3 -m ruff check (all touched files)
All checks passed!
```

## Recon: Single-Shot Call Surface

**Function**: `run_structured_call` in `packages/orchestration/structured_outputs.py`

**Signature**:
```python
def run_structured_call(
    model_cls: type[BaseModel],
    base_prompt: str,
    call_fn: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    allow_parse_retry: bool = True,
    native_schema: bool = False,
) -> StructuredOutcome
```

**What it handles**:
- Schema instruction injection (prompt-embedded or native)
- Pydantic response validation
- One bounded parse retry (max 2 calls)
- Per-call evidence hook (`on_call`)
- Returns `StructuredOutcome` (ok, value, error_class, hint, calls, parse_retried)

**What it does NOT handle**:
- Provider transport (timeouts, subprocess — delegated to injected `call_fn`)
- Transport-level retries with backoff (handled by `_call_with_retry` in
  `pingpong_loop.py`, currently private)

**T002 verdict**: `run_structured_call` is directly importable. T002 needs
to supply its own `call_fn` wrapping the provider. If transport retry
with backoff is needed, `_call_with_retry` would need extraction from
`pingpong_loop.py` — or T002 can wrap a single provider call without
transport retry (intake is low-stakes, a single timeout falls through
to the heuristic path).

## Next expected action
Reviewer reviews T001 bundle.

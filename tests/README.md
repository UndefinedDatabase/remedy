# Test Suite Structure

Tests are organized by domain, not by implementation step number.

## Directory Layout

```
tests/
  orchestration/     Core engine: source_apply, approval_queue, autorun,
                     test_runner, command_discovery, autonomy, event_ledger,
                     project_brain
  ui_server/         HTTP API: dashboard contract, live state, brain view model,
                     auth/redaction
  cli/               CLI surface: command catalog, job commands, runtime wrappers
  ui_contracts/      Python-verifiable frontend contracts: graph architecture,
                     UX quality gates, responsive layout
  storage/           Persistence, hygiene, artifacts
  regression/        Named bug regressions (not step ranges)
```

## Test Categories (pytest markers)

| Marker | Meaning | Count |
|--------|---------|-------|
| `unit` | Pure logic, no I/O, no subprocess | (default) |
| `integration` | Temp files, storage, orchestration state | ~800 |
| `subprocess` | Spawns child processes (CLI, runtime) | ~1100 |
| `smoke` | Smoke contract tests for scripts | ~20 |
| `real_ollama` | Requires running Ollama server | ~80 |
| `ui_contract` | Python-verifiable UI contracts | ~400 |
| `safety` | Resource safety and process isolation | ~20 |
| `architecture` | Structural guards (imports, namespaces) | ~20 |
| `slow` | Tests >5s individually | (none yet) |

Markers are auto-assigned via `tests/conftest.py` based on file patterns.

## Recommended Commands

### Daily development (fast, ~30-60s)
```bash
scripts/remedy_test_fast.sh
```
Excludes subprocess, real_ollama, ui_contract, smoke, slow.

### Before merge (integration, ~2-3 min)
```bash
scripts/remedy_test_integration.sh
```
Runs smoke surfaces + full pytest minus real_ollama/slow.

### Smoke (targeted, ~15s each)
```bash
scripts/remedy_backend_basis_smoke.sh
scripts/remedy_runtime_wrapper_smoke.sh
scripts/remedy_process_isolation_smoke.sh
```

### Real providers (opt-in)
```bash
REMEDY_RUN_REAL_OLLAMA=1 scripts/remedy_test_real_providers.sh
```

### Full suite (once per handoff)
```bash
scripts/remedy_pytest.sh tests/ -q --cache-clear
```

## Naming Convention

- `test_<domain>.py` — one file per domain concern
- Test classes named by invariant, not step number
- No `test_steps_*.py` or `test_step_*.py` files (guard test enforces this)

## Resource Safety

- All pytest execution uses `scripts/remedy_pytest.sh` (flock + timeout).
- Never run pytest in background.
- Never run multiple pytest commands in parallel.
- Never run full `pytest tests/` more than once per work block.
- See `docs/reviewer-safety.md` for full policy.

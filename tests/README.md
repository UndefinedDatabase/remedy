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
  cli/               CLI surface: command catalog, job commands
  ui_contracts/      Python-verifiable frontend contracts: graph architecture,
                     UX quality gates, responsive layout
  storage/           Persistence, hygiene, artifacts
  regression/        Named bug regressions (not step ranges)
```

## Existing Domain Tests (root level)

Files like `test_storage.py`, `test_command_discovery.py`, `test_patch_apply.py`
etc. in `tests/` predate the domain directory structure. They remain at root
level and are not duplicated.

## Naming Convention

- `test_<domain>.py` — one file per domain concern
- Test classes named by invariant, not step number
- No `test_steps_*.py` or `test_step_*.py` files (guard test enforces this)

## Running Tests

All pytest execution by agents must use the guarded wrapper:

```bash
# Full suite (once only, near final handoff)
scripts/remedy_pytest.sh tests/ -q --cache-clear

# Single domain (preferred during development)
scripts/remedy_pytest.sh tests/orchestration/ -q --cache-clear

# Single file
scripts/remedy_pytest.sh tests/orchestration/test_source_apply.py -q
```

## Resource Safety

- Never run pytest in background.
- Never run multiple pytest commands in parallel.
- Never run full `pytest tests/` more than once per work block.
- The wrapper uses `flock -n` to prevent parallel runs and `timeout` to prevent runaways.
- See `docs/reviewer-safety.md` for full policy.

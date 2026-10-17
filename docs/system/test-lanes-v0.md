# Test Lanes v0

## Fast lane

**Script**: `scripts/remedy_test_fast.sh` (selection: `scripts/select_changed_tests.py`)
**Base**: changes since the merge base with `origin/main` (`REMEDY_FAST_BASE` overrides), plus
staged, unstaged and untracked files

Runs the owner tests of the change plus the core product spine. The selection, read from a
static AST index of `tests/` (no test is imported to build it):

| Changed | Selected |
|---------|----------|
| a module under `packages/` or `apps/` | every test file that imports it, in any import form |
| a module under `apps/cli/` | also the tests importing the dispatch (`apps.cli.grouped`, `apps.cli.commands.do_cmd`) |
| a file under `docs/` | every test file under `tests/docs/` |
| a test file | that file |
| any file | every test file naming its whole repository path, or its quoted file name when no other tracked file has that name |

Always run, the spine: `test_worker_facade_cmd.py`, `test_development_artifact_boundary.py`,
`test_product_spine.py` (128 tests, about 5 s). Selected owner tests may spawn subprocesses: the
lane proves the changed subsystem, not only its in-process part.

A change to the test machinery (`tests/conftest.py`, `tests/load_governor.py`, `pyproject.toml`,
`constraints.txt`, the pytest runner) has no owner selection: the lane exits 3 and names it, and
the full lane answers instead.

Measured on 2026-10-17 (selection takes about 2.5 s; CPU from the test load record): a change to
`pi_provider.py` selects 7 files (about 6 CPU s), `model_routing.py` 7 (21 s), `public_api.py`
4 (12 s), `final_verifier.py` 14 (19 s); the hub `pingpong_job.py` selects 325 files (590 CPU s,
over half of the suite) and a CLI handler about 110. Deliberately NOT followed: production
importers of the changed module. One such hop from almost any orchestration module reaches the
`pingpong_job` hub and selects 424 to 469 of 775 files, so the neighbours of a change are the full
suite, which stays the gate before a merge and at release.

**Does NOT prove**: anything outside the selection; a handler reached only through a CLI
subprocess by a test that imports neither it nor the dispatch.

**When to use**: during development and before committing. Not instead of the full lane.

## Runtime lane

**Script**: `scripts/remedy_test_runtime.sh`
**Expected runtime**: under about 60 seconds on a normal dev machine
**Tests**: ~57

Runs subprocess-based CLI integration tests. Subprocess-heavy suites
run per-node — each test gets its own bounded
pytest invocation with process-group isolation (`start_new_session=True`,
`killpg` on timeout). Other suites run as whole-file invocations.

Diagnostics: each node prints `START node:` / `END node:` markers with
wall-clock timing. Stale process check runs at end. If a node hangs,
the exact node ID is visible in output.

| Suite | Type | What it proves |
|-------|------|----------------|
| `test_command_catalog.py` | CLI integration | Catalog integrity, group definitions, handler wiring |
| `test_contract_runtime.py` | CLI integration | Allowed/denied actions, budget, contract evaluation |
| `test_config_cmd.py` | CLI integration | Config layer basics |

**When to use**: After CLI changes, before PR creation, when fast lane passes.

## Full lane

**Script**: `scripts/remedy_test_full.sh`
**Expected runtime**: 3-4 minutes
**Tests**: ~6860+

Runs all tests except known environment-sensitive chain-order test.
Proves everything the fast lane proves plus UI contracts, event replay,
brain graph, overnight planning, provider trust gate, tournament, and more.

**When to use**: Before creating a PR, after major changes, CI.

The excluded test (`test_full_chain_order`) depends on filesystem ordering
that varies between environments.

## UI contract lane

**Script**: `scripts/remedy_pytest.sh tests/ui_contracts/ tests/ui_server/ -q`
**Expected runtime**: 15-30 seconds
**Tests**: ~300+

Proves UI contract integrity, dashboard truth, timeline guards, auth
redaction, cockpit contract, and live state serialization.

**When to use**: After changing UI server code or dashboard models.

## Lint lane

**Script**: `scripts/remedy_lint.sh`
**Expected runtime**: 10-20 seconds

Runs ruff (import sort, unused imports, f-string issues) and mypy
(type checking across 191+ source files).

**When to use**: Before every commit. Required to pass for merge.

## What no lane proves

- Real provider execution (Claude, GPT, Ollama)
- Network connectivity or API availability
- Real git operations (commits, PRs, deployments)
- Production performance under load
- Secret management or authentication flows

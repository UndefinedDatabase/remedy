# Test Lanes v0

## Fast lane

**Script**: `scripts/remedy_test_fast.sh`
**Expected runtime**: under 10 seconds (depends on environment)
**Tests**: ~535

Pure in-process tests only. No subprocess calls. Proves the core product spine is
healthy without risk of environment-specific hangs.

| Suite | Type | What it proves |
|-------|------|----------------|
| `test_worker_facade_cmd.py` | unit | Worker add/doctor/disable, alias registry, catalog wiring |
| `test_dogfood_run.py` | unit | Mission run loop, morning report, 10 stop conditions, evidence |
| `test_managed_builder_execution.py` | unit | Command templates, approval, execution safety, placeholders |
| `test_main_builder_adapter.py` | unit | Adapter specs, enable/disable, mode management |
| `test_self_repair_proposal.py` | unit | Proposal lifecycle: create/approve/deny/edit/worker-prompt |
| `test_execution_approval_policy.py` | unit+integration | Policy model, evaluation, grant, real storage path truth |
| `test_development_artifact_boundary.py` | guard | Dev artifact vs product truth boundary enforcement |
| `test_product_spine.py` | unit | Operator command consistency, stale doc scanner, lane self-test |

**Does NOT prove**: CLI subprocess integration, UI rendering, overnight planning,
provider trust gate, tournament scoring, full event replay chain.

**When to use**: During development, before committing, quick health check.

## Runtime lane

**Script**: `scripts/remedy_test_runtime.sh`
**Expected runtime**: under about 60 seconds on a normal dev machine
**Tests**: ~57

Runs subprocess-based CLI integration tests. Subprocess-heavy suites
(`test_review_bundle_runtime.py`) run per-node — each test gets its own bounded
pytest invocation with process-group isolation (`start_new_session=True`,
`killpg` on timeout). Other suites run as whole-file invocations.

Diagnostics: each node prints `START node:` / `END node:` markers with
wall-clock timing. Stale process check runs at end. If a node hangs,
the exact node ID is visible in output.

| Suite | Type | What it proves |
|-------|------|----------------|
| `test_review_bundle_runtime.py` | CLI integration | Evidence safety, no raw leaks, progress summary |
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

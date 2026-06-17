# Test Lanes v0

## Fast lane

**Script**: `scripts/remedy_test_fast.sh`
**Runtime**: ~5-10 seconds
**Tests**: ~418

Proves the core product spine is healthy. Covers:

| Suite | What it proves |
|-------|----------------|
| `test_worker_facade_cmd.py` | Worker add/doctor/disable, alias registry, catalog wiring |
| `test_dogfood_run.py` | Mission run loop, morning report, 10 stop conditions, evidence |
| `test_managed_builder_execution.py` | Command templates, approval, execution safety, placeholders |
| `test_main_builder_adapter.py` | Adapter specs, enable/disable, mode management |
| `test_self_repair_proposal.py` | Proposal lifecycle: create/approve/deny/edit/worker-prompt |
| `test_review_bundle_runtime.py` | Evidence safety, no raw leaks, progress summary |
| `test_command_catalog.py` | Catalog integrity, group definitions, handler wiring |
| `test_contract_runtime.py` | Allowed/denied actions, budget, contract evaluation |
| `test_config_cmd.py` | Config layer basics |

**Does NOT prove**: UI rendering, subprocess isolation, overnight planning,
provider trust gate, tournament scoring, full event replay chain.

**When to use**: During development, before committing, quick health check.

## Full lane

**Script**: `scripts/remedy_pytest.sh -k "not test_full_chain_order"`
**Runtime**: ~3-4 minutes
**Tests**: ~6835

Runs all tests except known environment-sensitive chain-order test.
Proves everything the fast lane proves plus UI contracts, event replay,
brain graph, overnight planning, provider trust gate, tournament, and more.

**When to use**: Before creating a PR, after major changes, CI.

The excluded test (`test_full_chain_order`) depends on filesystem ordering
that varies between environments.

## UI contract lane

**Script**: `scripts/remedy_pytest.sh tests/ui_contracts/ tests/ui_server/ -q`
**Runtime**: ~15-30 seconds
**Tests**: ~300+

Proves UI contract integrity, dashboard truth, timeline guards, auth
redaction, cockpit contract, and live state serialization.

**When to use**: After changing UI server code or dashboard models.

## Lint lane

**Script**: `scripts/remedy_lint.sh`
**Runtime**: ~10-20 seconds

Runs ruff (import sort, unused imports, f-string issues) and mypy
(type checking across 191+ source files).

**When to use**: Before every commit. Required to pass for merge.

## What no lane proves

- Real provider execution (Claude, GPT, Ollama)
- Network connectivity or API availability
- Real git operations (commits, PRs, deployments)
- Production performance under load
- Secret management or authentication flows

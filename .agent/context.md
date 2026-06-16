# Context

## Active Branch
feature/steps-2146-2205-open-ended-dogfood-run-orchestrator-replay-analyzer-v0
(forked from clean main at 00ced0b after PR #77 merged Managed Execution Approval blocks).

## Scope
Steps 2146-2205: Open-Ended Dogfood Run Orchestrator + Replay Analyzer v0.
All 15 phases complete. Awaiting commit + reviewer verdict.

## New files
- packages/orchestration/dogfood_run.py — core module (~700L)
- apps/cli/commands/dogfood_cmd.py — 10 CLI handlers
- tests/orchestration/test_dogfood_run.py — 48 targeted tests
- docs/open-ended-dogfood-run-orchestrator-replay-analyzer-v0.md — architecture doc
- docs/dogfood-run-user-guide.md — user guide

## Modified files
- apps/cli/command_catalog.py — dogfood group + 10 entries
- apps/cli/commands/__init__.py — dogfood_cmd import
- apps/cli/grouped.py — --max-wall-minutes option
- packages/orchestration/run_contract.py — 6 dogfood actions
- packages/orchestration/progress_ledger.py — dogfood run items
- packages/orchestration/review_bundle.py — dogfood_run_summary.json section
- tests/orchestration/test_review_bundle.py — section count 36->37

## Carried residual risks
- Pre-existing deselected test_full_chain_order.
- Pre-existing test_resource_safety reads stale .agent/context.md.

## Status
Code + tests complete. 48 targeted + 18 catalog + 6551 full suite passed. Awaiting commit.

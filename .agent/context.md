# Context

## Active Branch
feature/steps-2656-2675-core-product-spine-fast-test-lane-v0
(forked from main at 9cbf170 after PR #87 merged).

## Scope
Steps 2656-2675: Core product spine documentation, fast test lane,
command taxonomy, docs update to product language, consistency tests.
Consolidation block — no new features.

## Reviewer findings (carry-forward)
- R-0153 (LOW): CLM table missing in context.md. Carry-forward.
- R-0154 (LOW): No CLM in final handoff. Carry-forward.

## Key architectural decisions
- `doctor.core` added as read-only product spine health check
- Fast test lane: targeted 9-file list instead of marker exclusions (420 tests, ~7s)
- Full test lane: thin wrapper over remedy_pytest.sh
- Product language in docs: Mission Run, Mission Report, Worker
- "dogfood" kept as internal CLI group for backwards compatibility
- test_test_categories.py updated for targeted fast lane approach

## Changed Line Map
| File | Lines | Symbols | Purpose | Risk |
|------|-------|---------|---------|------|
| worker_facade_cmd.py | +80 | _cmd_doctor_core, _try_import | Product spine health check | LOW |
| command_catalog.py | +11 | doctor GroupDef, doctor.core CommandEntry | Catalog entry | LOW |
| run_contract.py | +2 | DOCTOR_CORE ContractAction | Contract action | LOW |
| core-product-spine-v0.md | +130 (NEW) | — | Canonical flow map + taxonomy | LOW |
| test-lanes-v0.md | +75 (NEW) | — | Test lane documentation | LOW |
| simple-operator-quickstart-v0.md | rewrite | — | Updated entry point | LOW |
| controlled-claude-code-operator-path-v0.md | rewrite | — | Simple path primary | LOW |
| mission-run-loop-morning-report-v0.md | rewrite | — | Product language | LOW |
| remedy_test_fast.sh | rewrite | — | Targeted 9-file fast lane | LOW |
| remedy_test_full.sh | +11 (NEW) | — | Thin full lane wrapper | LOW |
| test_product_spine.py | +130 (NEW) | 20 tests | Spine consistency + stale scanner | LOW |
| test_worker_facade_cmd.py | +20 | TestDoctorCore | Doctor core tests | LOW |
| test_test_categories.py | rewrite | — | Updated for targeted fast lane | LOW |
| plan.md | rewrite | — | Builder metadata | LOW |
| context.md | rewrite | — | Builder metadata | LOW |

## Pre-existing test failures (not introduced by this change)
- tests/cli/test_self_dogfood_execution_cli.py (2 failures on main)
- tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.

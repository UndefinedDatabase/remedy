# Context

## Active Branch
feature/steps-1837-1876-overnight-mission-contract-review-repair-spine-v0 (forked from clean main at
4ddd59f after PR #71 merged Model/Route Tournament Harness v0). No drift.

## Mainline reconciliation (Step 1837)
- PR #71 MERGED → main. Current main commit: 4ddd59f. Tournament v0 reviewer verdict PASS @ b8f6ea8.
- Model/Route Tournament Harness v0 (1797-1836) landed: model_route_tournament.py (evidence-based
  route comparison; no fake winner; hard scoring ceilings). `remedy tournament report/show/list/
  integrity`.
- Carried risks reconciled below. No feature code before mainline closure.

## Scope
Steps 1837-1876: Overnight Mission Contract + Review/Repair Spine v0 — the first hard mission-contract
spine for Overnight Mode. A user gives Remedy a mission/prompt; Remedy tracks the CONTRACT until it is
fulfilled or safely blocked, evaluating satisfaction from DURABLE EVIDENCE (progress ledger, review
findings, tests/proof/snapshot gates, repair status, route/token/tournament readiness). Metadata +
state-machine + evaluation + reporting ONLY. NOT full overnight autonomy, NOT provider execution.

## Core principle
Workers execute. Remedy governs. The Mission Contract decides whether work is done — never from
builder self-report. The user must never feel lost: Remedy explains what happened, what is missing,
which review findings remain, and the next safe action. Reviewer verdict beats builder self-report;
a Done marker is NOT Resolved; open Blocker/High blocks satisfaction; missing required gates block
satisfaction; no fake overnight readiness.

## NOT MemPalace
MemPalace is an EXTERNAL long-term memory repository/tool that may later integrate as an adapter.
This block builds NO internal MemPalace memory, NO embeddings, NO vector DB. Deferred.

## Carried residual risks
- Mission spine is metadata/state-machine/evaluation only — no worker/provider/test/apply execution.
- Worker/provider/Claude/Pi/OpenCode/Ollama/cloud EXECUTION still not built (adapters future).
- Real test execution + snapshot/rollback proof not built (next block) — required gates report
  honestly as unavailable when missing.
- Token/cost are ESTIMATED bands; tournament evidence is shared route-tier granularity.
- MemPalace / durable project memory NOT built (external adapter, future).
- Regex/entropy scanning can miss novel secret formats (R-0083 lineage).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker.
- Legacy `worker` group (worker_adapters/worker_queue) and the registry coexist.

## Mission spine constraints (block 1837-1876)
- NO provider/Claude/Pi/OpenCode/Ollama/cloud/local execution, network, browser, subprocess, shell.
- NO worker execution, NO test run, NO apply/approve/reject, NO git/PR automation, NO auto-generation.
- NO MemPalace / internal memory / embeddings / vector DB; NO UI redesign; NO MCP; NO pricing sync.
- Contract satisfaction ONLY from durable evidence; never from builder self-report. Reviewer verdict
  beats self-report; Done marker != Resolved; open Blocker/High blocks satisfaction; missing required
  gates block satisfaction; if no next safe action → blocked; no fake overnight readiness.
- Required blockers (needed to satisfy the current contract) kept separate from optional future ideas.
- No raw prompts (beyond a scrubbed user_goal summary)/logs/diffs/secrets/abs paths in public surfaces.
- Every next_safe_action catalog-backed. NO PR unless asked (auto-merge on reviewer PASS).

## Foundation reused
- overnight_executor.parse_review_findings (verdict + open Blocker/High/Medium/Low counts; Step 1842).
- progress_ledger.build_progress_ledger; feature_planner.build_feature_plan; repair_loop status APIs;
  proof_chain.build_proof_chain; run_contract ContractAction.
- worker_registry / token_economy / model_route_tournament readiness hints (read-only).
- provider_trust._scrub_public/_safe_path_label; data_paths.resolve_data_root + atomic 0o600 storage.
- command_catalog/grouped CLI; review_bundle REQUIRED_SECTIONS; ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once at block
  end with `-k "not test_full_chain_order"`. No shell=True, no subprocess (except CLI runtime tests).

## Changed files (Steps 1837-1876) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/overnight_mission.py | NEW core: MissionContract/Cycle/Evaluation models + storage; create_mission_contract_from_job (conservative, needs-user-acceptance honest); review-findings-as-blockers (reuses parse_review_findings); evaluate_mission_contract (durable evidence; never self-report); mission_next_safe_actions (required vs optional); mission_state_machine; mission_readiness (honest, no fake autonomy); audit_evaluation_safety + mission_integrity | the mission-contract spine |
| packages/orchestration/run_contract.py | OVERNIGHT_MISSION_CREATE/EVALUATE/SHOW actions (default-allowed, non-exec) | contract gate |
| apps/cli/commands/overnight_mission_cmd.py | NEW handlers: contract-create/show/evaluate/next-action/cycles/contract-readiness/integrity | CLI surface |
| apps/cli/commands/__init__.py | register overnight_mission_cmd | wire handlers |
| apps/cli/command_catalog.py | 7 overnight mission entries (create/evaluate write_metadata; rest read_only; no may_execute); contract-readiness avoids collision with existing overnight.readiness | catalog-backed |
| packages/orchestration/progress_ledger.py | extract/merge_mission_items (LOAD-only, no recursion) + build wiring | surface mission status honestly |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 31→32 + _build_overnight_mission_summary | safe bundle summary |
| packages/orchestration/ui_server.py | _build_overnight_mission_section cockpit (live=false) | read-only cockpit |
| tests/orchestration/test_overnight_mission.py | NEW 23 tests (models/storage/creation/evaluation/state-machine/next-actions/integrity/audit/redaction/arch) | coverage |
| tests/orchestration/test_overnight_mission_integration.py | NEW 8 tests (ledger/bundle/cockpit) | integration coverage |
| tests/cli/test_overnight_mission_cli.py | NEW 8 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==32 + overnight assert | bundle test |
| docs/overnight-mission-contract-review-repair-spine-v0.md, docs/overnight-mission-user-guide-v0.md | NEW architecture + user docs | document spine + non-goals |
| .agent/context.md, .agent/plan.md | reconciliation + changed-files table | handoff |

## Status
Steps 1837-1876 builder work COMPLETE. Full pytest 6198 passed, 8 skipped, 1 deselected (exit 0;
first attempt was infra-killed/137 then re-run clean). mission integrity passed. Parallel reviewer
owns the live_review verdict (PENDING at handoff). Reviewer findings start at R-0102. Auto-merge on
reviewer PASS (honor hard gate; operator may override).

## Next block
Real Test Execution + Snapshot/Rollback Proof v1 (only after this block PASS).

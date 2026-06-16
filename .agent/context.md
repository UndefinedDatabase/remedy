# Context

## Active Branch
feature/steps-1917-1960-token-aware-repair-loop-v1-v2 (forked from clean main at 43197d9 after PR #73
merged Real Test Execution + Snapshot/Rollback Proof v1). No drift.

## Mainline reconciliation (Step 1917)
- PR #73 MERGED → main (auto-merge on reviewer PASS per merge-autonomy). Current main commit: 43197d9.
  Real Test Execution + Snapshot/Rollback Proof v1 reviewer verdict PASS @ 7230268 (R-0104 Resolved:
  command_id forwarded into the safe runner; reported == executed command identity).
- Real Test Execution v1 (1877-1916) landed: real_test_execution.py facade over the bounded safe runner
  (test_execution_service.execute_test_run); honest Snapshot/Rollback Proof (metadata-only, no fake
  restore); Mission Contract consumes test/snapshot/rollback gates.
- Carried risks reconciled below. No feature code before mainline closure.

## Scope
Steps 1917-1960: Token-Aware Repair Loop v1/v2 — the next core Overnight step after Real Test
Execution. Spine: Failure Artifact → Minimal Repair Context → Fix Candidate → Review → Re-Test.
Remedy decides what should happen next, tracks whether the contract is getting closer to done, and
prevents unbounded/expensive/unsafe repair attempts. This is orchestration/metadata/evaluation — NOT
model execution.

## Core principle
Workers execute. Remedy governs. The Repair Loop turns test failures + review findings into a
controlled, token-aware repair workflow: minimal context (safe summaries + output_ref, never raw
logs/diffs), route recommendation respecting Worker Registry/Route Policy/Token Economy/Tournament,
candidate intake that does NOT equal repaired, reviewer + re-test gates, mission consumption. No
overclaim of full autonomy. Unknown context / excessive token estimate → compression / context
inspection / human decision, never blind expensive routing.

## Reused existing infra (DO NOT reinvent)
- repair_loop.py (v0/v1): build_repair_context, evaluate_repair_eligibility, run_repair_attempt,
  reconcile_repair_after_continue, RepairStatus, load_repair_attempts. This block adds repair_loop_v2.py
  as a HIGHER-LEVEL token-aware orchestration layer (RepairLoopPolicy/RepairWorkItem/RepairAttempt v2/
  RepairLoopEvaluation) that consumes v0/v1 building blocks; it does NOT duplicate the apply-cycle.
- test_failure_artifact.py (safe failure summary + output_ref); real_test_execution.py (test runs +
  snapshot/rollback proofs); overnight_mission.py (gates + evidence); token_economy.py (estimates +
  routing_token_hint); worker_registry.py + builder_routing.py (route recommendation); candidate_quality
  .py + external_builder_sandbox.py + local_candidate_generator.py (candidate intake); proof_chain.py;
  progress_ledger/feature_planner/review_bundle/ui_server; run_contract; provider_trust scrub helpers.

## Carried residual risks
- Real rollback RESTORE still NOT implemented (Snapshot/Rollback Proof are honest metadata-only).
- Worker/provider/Claude/Pi/OpenCode/Ollama/cloud EXECUTION still NOT built. This block adds NO model
  execution; route recommendation produces package-create / human-decision next actions only.
- MemPalace remains a FUTURE external adapter / building block, NOT Remedy core. NOT built this block.
- No internal long-term memory / embeddings / vector DB.
- Token/cost estimated bands; tournament evidence shared-route granularity.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser blocker. Full-suite run occasionally infra-fragile (OOM).

## Block constraints (1917-1960)
- May create repair loop metadata, repair work items, repair context packages, route recommendations,
  external builder package suggestions, re-test recommendations, CLI surfaces, docs, integrity, tests.
- May call the EXISTING safe test execution path ONLY when explicitly allowed by contract/policy and
  bounded by max_test_runs. NO unbounded loop. NO background execution.
- NO provider/model/Claude/Pi/OpenCode/Ollama execution; NO direct worker execution; NO automatic
  candidate generation by model; NO auto-apply; NO auto-approval; NO autonomous repair mutation; NO
  auto-PR/git; NO real rollback restore; NO MemPalace; NO internal memory; NO embeddings/vector DB;
  NO UI redesign; NO MCP; NO shell=True; NO arbitrary command execution.
- Repair context minimal + token-aware (safe failure summary, output_ref, minimal file refs, test
  command id, compact reproduction summary, relevant review findings, token estimate, context pack
  recommendation, route policy limits). Unknown/oversized → compression or human decision.
- Candidate received ≠ repaired; quality pass ≠ applied; reviewer PASS + re-test green required per
  policy. Done marker ≠ reviewer Resolved. No fake repaired. next_safe_action catalog-valid.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh`; full suite once at block end with
  `-k "not test_full_chain_order"`. CLI runtime tests use the approved runner only.

## Changed files (Steps 1917-1960) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/repair_loop_v2.py | NEW token-aware orchestration: RepairLoopPolicy/RepairWorkItem/RepairAttempt/RepairLoopEvaluation + statuses + storage (atomic/corruption-aware/idempotent) + failure→item + review→item (Done≠Resolved) + build_repair_context_pack (token-aware; unknown→decision, oversized→compress) + recommend_repair_route (local/external-package/human; no exec) + review/retest gates + evaluate_repair_loop state machine (no fake repaired; bounded) + integrity + mission signal | bounded, token-aware repair spine |
| packages/orchestration/run_contract.py | REPAIR_ITEM_CREATE/REPAIR_LOOP_EVALUATE/REPAIR_LOOP_POLICY_SET/REPAIR_LOOP_SHOW (default-allowed; no exec) | contract gate |
| apps/cli/commands/repair_loop_v2_cmd.py | NEW handlers: repair item-create-from-failure/review, item-show/list, context-pack, route-recommend, evaluate, attempts, policy-show/set, integrity | CLI surface |
| apps/cli/commands/__init__.py | register repair_loop_v2_cmd | wire handlers |
| apps/cli/command_catalog.py | 11 repair-group entries (read_only/write_metadata; no may_execute) | catalog-backed |
| packages/orchestration/overnight_mission.py | _gather_mission_evidence consumes repair_loop_mission_signal (required repair blocks; abandoned/blocked → user decision) | mission consumes repair state |
| packages/orchestration/progress_ledger.py | extract/merge_repair_loop_items (RISK/DONE; no double-count) + build wiring | honest progress surface |
| packages/orchestration/feature_planner.py | repair-loop-open/blocked/retest-failed required-blocker rules (Impact/Effort; separate from roadmap) | evidence-based required blockers |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 33→34 + _build_repair_loop_summary (repair_loop_summary.json) | safe bundle summary |
| packages/orchestration/ui_server.py | _build_repair_loop_section cockpit (live=false; no mutation) | read-only cockpit |
| tests/orchestration/test_repair_loop_v2.py | NEW unit + arch guards | coverage |
| tests/cli/test_repair_loop_v2_cli.py | NEW CLI subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==34 + repair_loop_summary assert | bundle test |
| docs/token-aware-repair-loop-v1-v2.md, docs/token-aware-repair-loop-user-guide-v1.md | NEW architecture + user docs | document + honesty |
| .agent/context.md, .agent/plan.md | reconciliation + changed-files table | handoff |

## Status
Steps 1917-1960 IN PROGRESS. Mainline closed (PR #73 → main 43197d9). Building token-aware repair loop.
Parallel reviewer owns the live_review verdict. Reviewer findings start at R-0105.

## Next block
Main Builder Adapter v0: Claude/Pi/OpenCode Worker Control Plane (only after this block PASS).

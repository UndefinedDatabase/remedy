# Context

## Active Branch
feature/steps-1961-2025-main-builder-adapter-v0-token-controlled-session-rail (forked from clean
main at 719a4de after PR #74 merged Token-Aware Repair Loop v1/v2 + R-0105). No drift.

## Mainline reconciliation (Step 1961)
- PR #74 MERGED → main (auto-merge on reviewer PASS per merge-autonomy). Current main commit: 719a4de.
  Token-Aware Repair Loop v1/v2 reviewer verdict PASS @ 789c331 (R-0105 Resolved: three defense-in-
  depth integrity codes added to audit_evaluation_safety).
- Repair Loop v2 (1917-1960) landed: repair_loop_v2.py orchestration facade (RepairLoopPolicy/
  RepairWorkItem/RepairAttempt/RepairLoopEvaluation); token-aware context packs; route recommendation
  (never executes); bounded state machine; mission/progress/feature/review/cockpit integration; CLI
  surface (11 commands); integrity checks with all eight dedicated codes.
- Carried risks reconciled below. No feature code before mainline closure.

## Scope
Steps 1961-2025: Main Builder Adapter v0 + Token-Controlled External Session Rail — the next core
step after the Repair Loop. Controlled external builder session rail: adapter types (Claude Code /
Pi.dev / OpenCode / generic CLI / fixture), token-aware request packages, session lifecycle, fixture
builder for deterministic tests, External Builder Sandbox integration, Repair Loop / Mission / Token
Economy / Tournament / Worker Registry consumption. This is metadata/policy/evaluation/reporting —
NOT model execution.

## Core principle
Workers execute. Remedy governs. Builder output is UNTRUSTED until sandbox intake, trust/quality
checks, review, apply proof, and re-test gates pass. No provider monopoly — all adapter types
replaceable and user-selectable. Token reduction is first-class.

## Reused existing infra (DO NOT reinvent)
- external_builder_sandbox.py (safe ingress, quarantine, intake_provider_repair, submission state)
- worker_registry.py (WorkerSpec, RoutePolicy, WorkerKind, evaluate_worker_selection)
- builder_routing.py (BuilderRoutingTier/Decision, routing policy/traces)
- token_economy.py (estimates, budget profiles, routing_token_hint, context_pack recommendations)
- model_route_tournament.py (tournament specs/competitors/reports, routing_tournament_hint)
- candidate_quality.py (CandidateQualityEvaluation, scorecards, route_quality_feedback)
- repair_loop_v2.py (RepairLoopPolicy/WorkItem/Attempt/Evaluation, context packs, route reco)
- overnight_mission.py (mission gates, evidence gathering, satisfaction)
- real_test_execution.py (bounded safe test runner)
- proof_chain.py (Goal→Job→Task→Artifact→PatchIntent→Approval→Apply→Test→Proof)
- provider_trust (_scrub_public, _safe_path_label) for redaction
- progress_ledger / feature_planner / review_bundle / ui_server for integration surfaces
- run_contract (ContractAction, _DEFAULT_ALLOWED_ACTIONS) for action gating
- command_catalog (CATALOG, GROUPS, CommandEntry, ArgDef) for CLI registration

## Carried residual risks
- Real rollback RESTORE still NOT implemented (Snapshot/Rollback Proof are honest metadata-only).
- Worker/provider/Claude/Pi/OpenCode/Ollama/cloud EXECUTION still NOT built. This block adds NO
  model execution; adapters produce request packages and session metadata only.
- Real adapters are NOT configured yet — all disabled by default, no secrets committed.
- MemPalace remains a FUTURE external adapter / building block, NOT Remedy core. NOT built this block.
- No internal long-term memory / embeddings / vector DB.
- Token/cost estimated bands; tournament evidence shared-route granularity.
- Full overnight autonomy still requires safe worker execution + approval/apply gates (future).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser blocker.

## Block constraints (1961-2025)
- May create builder adapter metadata, request packages, session records, fixture builder output,
  intake results, CLI surfaces, integrity checks, docs, tests.
- May call the EXISTING External Builder Sandbox intake path for fixture/test builder output.
- NO provider/model/Claude/Pi/OpenCode/Ollama execution; NO direct worker execution; NO automatic
  candidate generation by model; NO auto-apply; NO auto-approval; NO autonomous mutation; NO
  auto-PR/git; NO real rollback restore; NO MemPalace; NO internal memory; NO embeddings/vector DB;
  NO UI redesign; NO MCP; NO shell=True; NO arbitrary command execution.
- Builder adapter output is ALWAYS untrusted: goes through External Builder Sandbox / Trust Gate /
  Candidate Quality / review / re-test gates. No direct repo write in v0.
- All real adapters disabled by default. Fixture adapter only in explicit test/fixture mode.
- No provider SDK imports. No secrets/env tokens stored. No hardcoded provider monopoly.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh`; full suite once at block end with
  `-k "not test_full_chain_order"`. CLI runtime tests use the approved runner only.

## Changed files (Steps 1961-2025) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/main_builder_adapter.py | NEW core module: BuilderAdapterKind/Mode/SessionStatus + BuilderAdapterSpec/RequestPackage/SessionRecord + storage + registry (defaults, save/load) + build_builder_request_package + session lifecycle (create/wait/start/output/blocked/intake) + fixture builder + recommend_builder_adapter + builder_adapter_mission_signal + integrity (audit_adapter/session) | controlled external builder session rail |
| packages/orchestration/run_contract.py | BUILDER_ADAPTER_SHOW/ENABLE, BUILDER_PACKAGE_CREATE, BUILDER_SESSION_CREATE/SHOW/INTAKE (default-allowed; no exec) | contract gate |
| apps/cli/commands/main_builder_adapter_cmd.py | NEW handlers: builder adapter-list/show/enable, package-create, session-create/show/list/record-output/intake, integrity | CLI surface |
| apps/cli/commands/__init__.py | register main_builder_adapter_cmd | wire handlers |
| apps/cli/command_catalog.py | 10 builder-group entries (read_only/write_metadata; no may_execute) + builder group def | catalog-backed |
| packages/orchestration/overnight_mission.py | _gather_mission_evidence consumes builder_adapter_mission_signal (blocked→user decision) | mission consumes builder state |
| packages/orchestration/progress_ledger.py | extract/merge_builder_adapter_items (blocked/waiting/running/candidate/intake) + build wiring | honest progress surface |
| packages/orchestration/feature_planner.py | builder-adapter-blocked/waiting/candidate required-blocker rules (Impact/Effort) | evidence-based required blockers |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 34→35 + _build_main_builder_adapter_summary | safe bundle summary |
| packages/orchestration/ui_server.py | _build_main_builder_adapter_section cockpit (live=false unless durable running; no mutation) | read-only cockpit |
| tests/orchestration/test_main_builder_adapter.py | NEW unit + arch guards (51 tests) | coverage |
| tests/cli/test_main_builder_adapter_cli.py | NEW CLI subprocess tests (10 tests) | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==35 + main_builder_adapter_summary assert | bundle test |
| docs/main-builder-adapter-v0-token-controlled-session-rail.md | NEW architecture doc | document + honesty |
| docs/main-builder-adapter-user-guide-v0.md | NEW user guide | user-facing |
| .agent/context.md, .agent/plan.md, .agent/live_review.md | reconciliation + changed-files table | handoff |

## Status
Steps 1961-2025 IN PROGRESS. Mainline closed (PR #74 → main 719a4de). Building Main Builder
Adapter v0. Parallel reviewer owns the live_review verdict. Reviewer findings start at R-0106.

## Next block
Managed External Builder Execution v1 OR Ollama Cheap-Task Adapter v0 (only after this block PASS).

# Context

## Active Branch
feature/steps-1797-1836-model-route-tournament-harness-v0 (forked from clean main at 6a81b8f after
PR #70 merged Token Economy + Context Budget Optimizer v0). No drift.

## Mainline reconciliation (Step 1797)
- PR #70 MERGED → main (operator override: reviewer's last logged verdict was FAIL @ 729d44c
  pre-fix; R-0098/R-0099/R-0100 fixed + builder-verified @ 5d75b1c; operator explicitly accepted the
  override to merge). Current main commit: 6a81b8f.
- Token Economy + Context Budget Optimizer v0 (1757-1796) landed: token_economy.py (TokenBudgetProfile,
  ContextBudgetEstimate, ContextPackRecommendation, TokenEconomyDecision, estimate helpers,
  unknown-context approval floor, audit_decision_safety, integrity). `remedy token budget-show/set/
  estimate/economy-report`, `remedy context-pack recommend`. Full suite 6111 passed.
- Carried risks reconciled below. No feature code before merge closure.

## Scope
Steps 1797-1836: Model/Route Tournament Harness v0 — an EVIDENCE-BASED comparison layer for Remedy's
worker routes. Compares durable evidence (Candidate Quality, Token Economy, Worker Registry metadata,
route policy, trust/verification outcomes, approval states, proof/test state, submission history) to
recommend which route is best for which task type. NOT provider execution, NOT model calling, NOT
auto-generation, NOT running workers.

## Core principle
Workers execute. Remedy governs. Tournament compares and recommends — it does not run workers. No
self-claim becomes truth; unknown evidence stays unknown; insufficient evidence never yields a fake
winner; cheap cost never beats failed trust/verification. The user must always understand the
recommendation — Tournament makes Remedy feel smarter, not more mysterious.

## Carried residual risks
- Tournament is evidence/reporting only — no route is executed; recommendations are read-only.
- Worker/provider/Ollama/cloud EXECUTION still not built (placeholders remain non-executable).
- Token/cost are ESTIMATED bands — no real pricing, no pricing sync.
- MemPalace / durable project memory NOT built (next block).
- Broader source patch materialization deferred (apply path .md-only).
- Regex/entropy scanning can miss novel secret formats (R-0083 lineage).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker.
- Legacy `worker` group (worker_adapters/worker_queue) and the new registry coexist.

## Tournament constraints (block 1797-1836)
- NO provider/model/Ollama/cloud/local execution, network, browser, subprocess, shell=True.
- NO new candidate generation, NO external builder auto-calls, NO apply/approve/reject/test/git/PR.
- NO MemPalace, NO real pricing sync, NO UI redesign, NO MCP activation.
- Evidence absence is `insufficient_evidence`, never failure; never trust model self-claims; never use
  raw candidate/prompt/output/diff/log content; unknown stays unknown.
- Scoring hard ceilings: no proof/test → not excellent; rejected/unverified → blocked/weak; unknown →
  insufficient_evidence/usable-at-most; high-risk without approval → blocked; unknown context/budget →
  approval required; placeholder executable claim → blocked; cheaper token cost cannot override failed
  trust/verification. No winner without sufficient evidence.
- No raw prompts/candidates/diffs/logs/secrets/abs paths in any public surface; next_safe_action
  catalog-backed. NO PR unless asked (auto-merge on reviewer PASS).

## Foundation reused
- worker_registry: load_worker_registry/load_route_policy/evaluate_worker_selection/get_worker_spec/
  is_placeholder/hard_safety_requires_approval; WorkerKind/CostTier/RiskTier.
- token_economy: token_economy_report/compute_token_economy_decision/routing_token_hint.
- candidate_quality: load_candidate_quality_evaluations/build_candidate_scorecards/route_quality_feedback.
- external_builder_sandbox: load_external_submissions. builder_routing: load_builder_routing_traces.
- provider_trust._scrub_public/_safe_path_label; data_paths.resolve_data_root + atomic 0o600 storage.
- run_contract ContractAction; command_catalog/grouped CLI; progress_ledger.merge_*, feature_planner,
  review_bundle REQUIRED_SECTIONS, ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once at block
  end with `-k "not test_full_chain_order"`. No shell=True, no subprocess (except CLI runtime tests).

## Changed files (Steps 1797-1836) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/model_route_tournament.py | NEW core: Spec/Competitor/Evidence/Score/Report models; competitor discovery from registry+policy; safe evidence gathering (candidate quality/token/external submissions); deterministic scoring with hard ceilings; report generation (no fake winner); atomic storage; audit_report_safety + tournament_integrity; routing_tournament_hint | evidence-based route comparison layer |
| packages/orchestration/run_contract.py | TOURNAMENT_REPORT/SHOW/LIST/INTEGRITY actions (default-allowed, non-exec) | contract gate |
| apps/cli/commands/tournament_cmd.py | NEW handlers: tournament report/show/list/integrity | CLI surface |
| apps/cli/commands/__init__.py | register tournament_cmd | wire handlers |
| apps/cli/command_catalog.py | tournament group + 4 entries (report write_metadata; rest read_only; no may_execute) | catalog-backed |
| packages/orchestration/builder_routing.py | tournament field on decision via routing_tournament_hint (read-only; no winner without evidence) | routing exposes comparison hint |
| packages/orchestration/progress_ledger.py | extract/merge_tournament_items + build wiring | surface comparison honestly (no fake winner) |
| packages/orchestration/feature_planner.py | item-id driven tournament suggestions (gather evidence / tighten policy) | evidence-based, user-choice |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 30→31 + _build_model_route_tournament_summary | safe bundle summary |
| packages/orchestration/ui_server.py | _build_model_route_tournament_section cockpit (live=false) | read-only cockpit |
| tests/orchestration/test_model_route_tournament.py | NEW 26 tests (models/discovery/scoring ceilings/report/storage/integrity/audit/redaction/arch) | coverage |
| tests/orchestration/test_model_route_tournament_integration.py | NEW 9 tests (routing/ledger/planner/bundle/cockpit) | integration coverage |
| tests/cli/test_tournament_cli.py | NEW 6 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==31 + tournament assert | bundle test |
| docs/model-route-tournament-harness-v0.md, docs/model-route-tournament-user-guide-v0.md | NEW architecture + user docs | document layer + non-goals |
| .agent/context.md, .agent/plan.md | reconciliation + changed-files table | handoff |

## Status
Steps 1797-1836 builder work COMPLETE. Full pytest 6160 passed, 8 skipped, 1 deselected (exit 0).
tournament integrity passed. Parallel reviewer owns the live_review verdict (PENDING at handoff).
Reviewer findings start at R-0101. Auto-merge on reviewer PASS (honor hard gate; operator may override).

## Next block
MemPalace Project Memory v0 (only after this block PASS).

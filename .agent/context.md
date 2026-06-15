# Context

## Active Branch
feature/steps-1757-1796-token-economy-context-budget-optimizer-v0 (forked from clean main at
c8f4fa5 after PR #69 merged Worker Registry + Route Policy v0). No drift.

## Mainline reconciliation (Step 1757)
- PR #69 MERGED → main (user: auto-merge on reviewer PASS). Current main commit: c8f4fa5.
- Worker Registry + Route Policy v0 (1717-1756) landed: worker_registry.py (replaceable WorkerSpec
  registry + per-job RoutePolicy + evaluate_worker_selection + hard_safety_requires_approval floor +
  integrity). `remedy worker registry-list/show/integrity`, `remedy route-policy show/set/evaluate`.
  Reviewer verdict PASS @ 32e480f. Full suite 6039 passed.
- Carried risks reconciled below. No feature code before merge closure.

## Scope
Steps 1757-1796: Token Economy + Context Budget Optimizer v0 — the first structured layer that
ESTIMATES token cost + context budget, recommends context packs (minimal/focused/balanced/full/
defer), surfaces budget warnings, and integrates with the Worker Registry route policy. Helps Remedy
answer: how expensive is this task, how much context it needs, can a cheaper/local route handle it
later, what context can be compressed, what should become durable memory, when to ask the user.

## Core principle
Workers execute. Remedy governs. Token reduction + context retention are core product pillars. All
costs/tokens are ESTIMATED bands unless configured evidence exists — never invented exact pricing,
never a pricing call. Unknown stays unknown (never cheap). Expensive/unknown/high-risk/placeholder
routes always require human-facing approval. The user must never feel lost; every budget warning is
understandable + actionable.

## Carried residual risks
- Token/cost are ESTIMATES (bands) — no real pricing, no provider pricing sync, no web calls.
- Worker/provider/Ollama/cloud EXECUTION still not built (metadata + policy + estimates only).
- MemPalace / durable project memory NOT built — memory_candidates are suggestions only.
- Model/Route Tournament still deferred (now has budget/context signals to build on after this block).
- Broader source patch materialization deferred (apply path .md-only).
- Regex/entropy scanning can miss novel secret formats (R-0083 lineage).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).
- Legacy `worker` group (worker_adapters/worker_queue) and the new registry coexist.

## Token Economy + Context Budget constraints (block 1757-1796)
- NO provider/model/Ollama/cloud/local-model calls, network, browser, subprocess, shell=True.
- NO apply/approve/reject/test-run/git/PR/merge; NO automatic generation/repair; NO worker execution.
- NO invented exact pricing / no provider pricing sync — estimates labeled `estimated` only.
- Unknown token/cost estimate never treated as cheap. Context pack never includes protected paths or
  raw content; missing context → warning, not fake zero. memory_candidates = suggestions only.
- Expensive/unknown/high-risk/placeholder routes always require human approval (reuse
  worker_registry.hard_safety_requires_approval). Ollama/cloud placeholders never appear executable.
- No raw prompts/context/source dumps/secrets/abs paths in any public surface (CLI JSON, bundle,
  cockpit). Every next_safe_action catalog-backed + entity-backed.
- Tests via scripts/remedy_pytest.sh; full suite once. NO PR unless user asks (auto-merge on PASS).

## Foundation reused
- context_inspector.inspect_context (safe included/excluded paths + estimated_tokens, bytes/4) for
  context budget estimates + pack recommendation basis; context_pack token convention (bytes/4).
- worker_registry: WorkerSpec/RoutePolicy/evaluate_worker_selection/hard_safety_requires_approval/
  load_worker_registry/load_route_policy; provider_trust._scrub_public/_safe_path_label redaction.
- data_paths.resolve_data_root + atomic-write 0o700/0o600 private storage pattern.
- builder_routing.select_builder_routing_decision (token/context recommendation layered read-only).
- run_contract ContractAction; command_catalog/grouped CLI; progress_ledger.merge_*, feature_planner,
  review_bundle REQUIRED_SECTIONS, ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once at block
  end with `-k "not test_full_chain_order"`. No shell=True, no subprocess (except CLI runtime tests).

## Changed files (Steps 1757-1796) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/token_economy.py | NEW core: TokenBudgetProfile/ContextBudgetEstimate/ContextPackRecommendation/TokenEconomyDecision; estimate helpers (chars/4); profile storage (atomic 0o600, floors); context pack recommender (reuses inspect_context; excludes protected; memory candidates suggestions-only); routing_token_hint; token_economy_report; token_economy_integrity | the estimate/budget layer |
| packages/orchestration/run_contract.py | TOKEN_BUDGET_SHOW/SET, TOKEN_ESTIMATE, TOKEN_ECONOMY_REPORT, CONTEXT_PACK_RECOMMEND actions (default-allowed, non-exec) | contract gate |
| apps/cli/commands/token_cmd.py | NEW handlers: token budget-show/set/estimate/economy-report + context-pack recommend | CLI surface |
| apps/cli/commands/__init__.py | register token_cmd | wire handlers |
| apps/cli/command_catalog.py | token + context-pack groups + 5 entries (budget-set write_metadata; rest read_only; no may_execute) | catalog-backed |
| packages/orchestration/builder_routing.py | token_economy field on decision via routing_token_hint (read-only estimate metadata; no-op-safe) | routing exposes budget/context hint |
| packages/orchestration/progress_ledger.py | extract/merge_token_economy_items + build wiring | surface budget/pack honestly (estimates) |
| packages/orchestration/feature_planner.py | item-id driven token-economy suggestions (optimizer/approval/ollama/mempalace/savings); claim generic ids to avoid double-emit | evidence-based, user-choice, no auto-build |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 29→30 + _build_token_economy_summary | safe bundle summary |
| packages/orchestration/ui_server.py | _build_token_economy_section cockpit (live=false; no buttons; no pricing) | read-only cockpit |
| tests/orchestration/test_token_economy.py | NEW 28 tests (helpers/profile/estimate/pack/decision/hint/integrity/redaction/arch) | coverage |
| tests/orchestration/test_token_economy_integration.py | NEW 14 tests (routing/ledger/planner/bundle/cockpit/placeholder) | integration coverage |
| tests/cli/test_token_cli.py | NEW 7 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==30 + token_economy assert | bundle test |
| docs/token-economy-context-budget-optimizer-v0.md, docs/token-economy-user-guide-v0.md | NEW architecture + user docs (anti-goals explicit) | document layer + non-goals |
| .agent/context.md, .agent/plan.md | reconciliation + changed-files table | handoff |

## Status
Steps 1757-1796 builder work COMPLETE. Full pytest 6102 passed, 8 skipped, 1 deselected (exit 0).
token + worker registry integrity passed (0 violations). Parallel reviewer owns the live_review
verdict (PENDING at handoff). Reviewer findings start at R-0098. Auto-merge on reviewer PASS.

## Next block
Model/Route Tournament Harness v0 (only after this block PASS — budget/context signals now exist).

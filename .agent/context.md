# Context

## Active Branch
feature/steps-1717-1756-worker-registry-route-policy-v0 (forked from clean main at a290238 after
PR #68 merged External Builder Sandbox v0). No drift.

## Mainline reconciliation (Step 1717)
- PR #68 MERGED → main (user-confirmed: "PR + merge, then branch"). Current main commit: a290238.
- External Builder Sandbox v0 (1681-1716) landed: external_builder_sandbox.py (safe request-package
  export + bounded/protected untrusted candidate ingress → existing Trust/Verification pipeline;
  raw_storage_ref never public). `remedy external-builder package-create/show/list/submit/
  submission-show/list/evaluate/integrity`. Reviewer verdict PASS @ 993781f. Full suite 5973 passed.
- Carried risks reconciled below. No feature code committed before merge closure.

## Scope
Steps 1717-1756: Worker Registry + User-Selectable Route Policy v0 — the modular Baukasten layer
that models workers as REPLACEABLE specs and lets the user constrain/select routes (workers,
cost tier, risk tier, local/Ollama-first preference). Metadata + policy + routing recommendation +
safety + CLI visibility ONLY. NOT worker/provider/model/Ollama execution.

## Core principle
Workers execute. Remedy governs. Users choose or constrain workers/routes. Cheap work prefers
local/Ollama-capable routes when safe; expensive models need evidence-based justification. Every
worker output stays UNTRUSTED until verified. No route silently starts work. Token + context
retention are first-class product concerns.

## Existing-system reconciliation (important — read before coding)
There is a PRE-EXISTING `worker` CLI group backed by `worker_adapters.py`
(`WorkerProviderSpec`: provider_id/display_name/supported_roles/execution_mode/status) +
`worker_recommend.py` + `worker_queue.py` (the legacy provider-catalog + execution-ish layer;
`worker run` executes a local loop). That taxonomy describes PROVIDERS.
This block adds a DISTINCT, richer route-policy taxonomy in `worker_registry.py`
(`WorkerSpec` with kind/cost/risk/execution-mode/token/context/output-contract + `RoutePolicy`).
To avoid breaking the existing `worker list`/`worker show` (and their tests), the new registry is
surfaced as NON-colliding subcommands `worker registry-list` / `worker registry-show` plus the new
`route-policy` group. The two worker views coexist intentionally; a future block may unify them.
Model/Route Tournament is DEFERRED until this Worker Registry exists.

## Carried residual risks
- Worker/provider/Ollama/cloud EXECUTION still not built (this block is metadata + policy only).
- External builder EXECUTION not built (ingress only, from 1681-1716).
- Token/cost figures are ESTIMATED bands only — no real pricing, no provider pricing calls.
- Broader source patch materialization deferred (apply path .md-only).
- Regex/entropy scanning can miss novel secret formats (R-0083 lineage).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).
- Legacy `worker` group (worker_adapters/worker_queue) and the new registry coexist (see above).

## Worker Registry + Route Policy constraints (block 1717-1756)
- NO provider/model/Ollama/cloud calls, network, browser, subprocess, shell=True.
- NO apply/approve/reject/test-run/git/PR/merge; NO automatic generation/repair.
- NO worker execution: registry/policy are metadata; routing emits recommendation + next_safe_action.
- Disabled/blocked workers can never be recommended/selected. Unknown cost is never treated as cheap.
- Expensive/cloud/unknown route requires explicit human-facing justification.
- local/Ollama preference cannot override safety or missing capability.
- No raw prompts/secrets/abs paths/raw model output in any public surface (CLI JSON, bundle, cockpit).
- Every next_safe_action catalog-backed + entity-backed. NO PR unless the user explicitly asks.
- Ollama/cloud workers are PLACEHOLDERS — metadata-only, clearly non-executable.

## Foundation reused
- provider_trust._scrub_public / _safe_path_label for redaction; data_paths.resolve_data_root;
  atomic-write + 0o700/0o600 private-storage pattern (mirrors external_builder_sandbox.py).
- builder_routing.select_builder_routing_decision (registry-aware constraints layered in, read-only).
- candidate_quality.route_quality_feedback (read-only confidence) reused unchanged.
- run_contract ContractAction + _DEFAULT_ALLOWED_ACTIONS; command_catalog/grouped CLI;
  progress_ledger.merge_*, feature_planner, review_bundle REQUIRED_SECTIONS, ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once at block
  end with `-k "not test_full_chain_order"`. No shell=True, no subprocess (except CLI runtime tests).

## Changed files (Steps 1717-1756) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/worker_registry.py | NEW core: WorkerSpec/RoutePolicy models + enums; deterministic built-in registry (7 specs); safe policy storage (atomic 0o600); evaluate_worker_selection (read-only); token/cost ESTIMATE band helpers; worker_registry_integrity | the Baukasten registry + policy layer |
| packages/orchestration/run_contract.py | WORKER_REGISTRY_SHOW / ROUTE_POLICY_SHOW/SET/EVALUATE actions (default-allowed, non-exec) | contract gate |
| apps/cli/commands/route_policy_cmd.py | NEW handlers: worker registry-list/show/integrity + route-policy show/set/evaluate | CLI surface |
| apps/cli/commands/__init__.py | register route_policy_cmd (import + loop) | wire handlers |
| apps/cli/command_catalog.py | route-policy group + worker registry-list/show/integrity + route-policy show/set/evaluate entries (read_only/write_metadata; no may_execute) | catalog-backed |
| apps/cli/grouped.py | store_true branches for the 3 route-policy flags | arg parsing |
| packages/orchestration/builder_routing.py | _route_policy_blocks_tier + _route_policy_cmd; local/external finalize escalate to human review when a user policy blocks/reselects the worker (no-op under default) | user route policy honored read-only |
| packages/orchestration/progress_ledger.py | extract/merge_worker_registry_items + build_progress_ledger wiring | surface registry/policy honestly (no fake running) |
| packages/orchestration/feature_planner.py | item-id driven worker-registry suggestions (tournament/ollama/expensive/token) | evidence-based, user-choice, no auto-build |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 28→29 + _build_worker_registry_summary | safe bundle summary |
| packages/orchestration/ui_server.py | _build_worker_registry_section cockpit (live=false; no buttons) | read-only cockpit |
| tests/orchestration/test_worker_registry.py | NEW 30 tests (model/builtins/policy/selection/token/integrity/redaction/arch-guards) | coverage |
| tests/orchestration/test_worker_route_integration.py | NEW 10 tests (routing constraint/ledger/planner/bundle/cockpit) | integration coverage |
| tests/cli/test_route_policy_cli.py | NEW 11 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==29 + worker_registry assert | bundle test |
| tests/ui_server/test_dashboard_cockpit_truth.py | test_worker_registry_section_present | cockpit test |
| docs/worker-registry-route-policy-v0.md, docs/worker-route-policy-user-guide-v0.md | NEW architecture + user-facing docs (anti-goals explicit) | document layer + non-goals |
| .agent/context.md, .agent/plan.md | reconciliation + changed-files table | handoff |

## Status
Steps 1717-1756 builder work COMPLETE. Full pytest 6033 passed, 8 skipped, 1 deselected (exit 0).
worker registry-integrity passed (0 violations). Parallel reviewer owns the live_review verdict
(PENDING at handoff). Reviewer findings start at R-0095. NO PR until the user explicitly asks.

## Next block
Token Economy + Context Budget Optimizer v0 — or Model/Route Tournament Harness v0 if the registry
reveals enough route evidence (only after this block PASS).

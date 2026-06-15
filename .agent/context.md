# Context

## Active Branch
feature/steps-1573-1608-expensive-builder-routing-v0 (forked from clean main at d22e1dd
after PR #64 merged Provider Trust Verification v1). No drift.

## Mainline reconciliation (Step 1573)
- PR #64 MERGED → main. Current main commit: d22e1dd.
- Provider Trust Verification v1 landed: provider_trust_verification.py (second-stage SAFE
  check; verify-before-materialize; unverified candidates create no intent; overclaim/
  unrelated/repeated-failed/secret caught; no execution/SDK/network). `remedy provider
  verify/verification-show`. Reviewer NIT (dead _INTENT_OK_RE) resolved pre-merge.
  Full suite 5812 passed, 8 skipped, 1 deselected.

## Scope
Steps 1573-1608: Expensive Builder Routing v0 — local-first, budgeted, anti-loop ROUTING/POLICY
for when to use deterministic logic / local advisory / local candidate gen / external builder gen.

## Core principle
LLMs advise or build candidates. The orchestrator controls. Evidence is truth. Local first when
useful. Expensive builders only when targeted, budgeted, bounded. No loops. NO execution in v0.

## Carried residual risks
- Automated candidate generation NOT built (this block only routes/plans; never generates).
- Direct provider/external builder EXECUTION not built (routing produces a plan, not a call).
- Broader source patch materialization deferred (apply path .md-only).
- Self overnight not built; cleanup/retention automation not built.
- Regex/entropy scanning can miss novel secret formats (R-0083 lineage).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Expensive Builder Routing constraints (block 1573-1608)
- Routing/policy/planning ONLY. No routing result executes anything; none creates Patch Intent/ProposedTask.
- NO external provider/cloud execution, automated candidate generation, network, browser, subprocess (except CLI runtime tests), provider SDK.
- NO auto apply/approval/repair-loop/PR/merge/git-commit-gate/background orchestration/UI mutation/MCP/dep upgrades.
- External builder route NEVER without: request package ready + Trust Gate available + Verification available + budget allowed + loop risk not high + no pending approval/intent.
- Local first; deterministic first; local advisor before external builder; no repeated expensive route without new evidence.
- Unknown external cost stays unknown and BLOCKS external by default. Local unavailable does NOT imply external allowed.
- No raw prompt/response/source/diff/stdout/stderr/artifact-body/secrets/tracebacks/abs paths in public surfaces.
- Every next_safe_action catalog-backed + entity-backed.
- NO PR unless the user explicitly asks (Step 1608).

## Foundation reused
- orchestrator_brain (build_orchestrator_situation/_gather_signals/select_orchestrator_decision/
  RoutingTier/StopReason/list_decisions; LoopGuardStatus). provider_trust._scrub_public (redaction).
- provider_trust/provider_trust_verification/repair_request_builder/provider_patch_material loaders (safe summaries).
- local_model_advisor (load_local_advisor_config/list runs — availability only, no call).
- run_contract (ensure_contract/evaluate_run_action/ContractAction; ALL_KNOWN auto-derived; add builder_routing_decide/report).
- data_paths.resolve_data_root; storage.load_job; command_catalog/grouped CLI.
- progress_ledger.merge_*, feature_planner, review_bundle (REQUIRED_SECTIONS +builder_routing_summary.json), ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once
  at block end with `-k "not test_full_chain_order"`. No shell=True, no subprocess.

## Product readiness — Expensive Builder Routing v0 (Step 1604)
CAN: decide WHEN builder help is justified via `remedy builder-routing decide/report` and a
persisted safe trace. Local-first order: deterministic (approve/continue/verify/propose) →
local advisor (only if untried for this evidence) → local candidate generator (if enabled +
budgeted) → external candidate generator (only if explicitly enabled + ALL hard preconditions)
→ human review / no safe route. Anti-loop: no repeated expensive route without new evidence;
repeated rejection → human review. Budget: unknown external cost blocks external by default;
local≠external. Surfaced in Progress/Feature/Review(25)/Cockpit; safe trace 0o600, idempotent
by evidence fingerprint.
CANNOT (by design): execute any builder/model/provider; generate candidates; call network/
subprocess/SDK; apply/approve/test/PR/git; create Patch Intents/ProposedTasks; recommend
external without request package + Trust Gate + Verification + budget + low loop risk + no
pending approval/intent; loop on repeated failed generation; emit fake next actions; leak raw
prompt/response/source/diff/log/secrets/paths. Readiness ~85% (routing rail complete; actual
local/external generators deferred).

## Changed files (Steps 1573-1608) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/builder_routing.py | NEW core: models/tiers/policy/inputs/need-detector/local-first rules/justification/budget/loop-governor/selector/trace persistence | the routing rail |
| packages/orchestration/run_contract.py | BUILDER_ROUTING_DECIDE/REPORT actions (allowed by default, non-exec) | contract gate |
| apps/cli/commands/builder_routing_cmd.py | NEW `builder-routing decide/report` handlers | CLI surface |
| apps/cli/commands/__init__.py | register builder_routing_cmd | wire handlers |
| apps/cli/grouped.py | `--user-requested` flag | CLI plumb |
| apps/cli/command_catalog.py | builder-routing group + decide(write_metadata)/report(read_only) entries | catalog-backed commands |
| packages/orchestration/progress_ledger.py | extract/merge_builder_routing_items (fixed item_ids) | surface routing, no raw |
| packages/orchestration/feature_planner.py | 4 routing repair rules | suggestions, no auto-exec |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 24→25 + _build_builder_routing_summary | bundle safe routing summary |
| packages/orchestration/ui_server.py | _build_builder_routing_section cockpit | read-only, no buttons |
| tests/orchestration/test_builder_routing.py | NEW 18 unit/integration/redaction/arch tests | coverage |
| tests/cli/test_builder_routing_cli.py | NEW 7 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==25 + assert | bundle test |
| tests/ui_server/test_dashboard_cockpit_truth.py | test_builder_routing_section_present | cockpit test |
| docs/expensive-builder-routing-v0.md + 4 doc updates | NEW + cross-refs | docs |

## Status
Steps 1573-1608 COMPLETE. Full pytest 5846 passed, 8 skipped, 1 deselected (exit 0).
Builder self-run counts; parallel reviewer owns the live_review verdict. NO PR (Step 1608).

## Next block
Automated Local Candidate Generator Adapter v0 OR Provider Execution Sandbox v0.

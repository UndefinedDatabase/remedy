# Context

## Active Branch
feature/steps-1465-1498-main-orchestrator-brain-v0 (forked from clean main at 38df37d
after PR #61 merged Self-Dogfood Execution v0). No drift.

## Mainline reconciliation (Step 1465)
- PR #61 MERGED → main. Current main commit: 38df37d.
- Self-Dogfood Execution v0 landed: self_dogfood_execution.py (approved self ProposedTask
  → bounded SelfImprovementAttempt → request → Provider Trust Gate → materialize →
  approve → do continue → reconcile; deterministic provider-label correlation; COMPLETED
  only from verified proof). `remedy self execute/status/reconcile/integrity`. Full suite
  5689 passed, 8 skipped, 1 deselected.

## Scope
Steps 1465-1498: Main Orchestrator Brain v0 — Decision Engine, Anti-Loop Guard, Model
Routing Plan. Read state from SAFE summaries → Situation → Options → score → loop guard
→ routing plan → ONE Decision with rationale. Planning/decision ONLY.

## Core principle
LLMs are advisors/builders. The orchestrator is the controller. Evidence is truth.

## Carried residual risks
- Direct provider execution NOT built; local model advisory NOT built.
- Provider Trust Verification v1 NOT built.
- Broader source patch materialization deferred (apply path .md-only).
- Cleanup/retention automation not built; self-overnight not built.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Orchestrator Brain constraints (block 1465-1498)
- READ-ONLY or metadata-only. NO action execution from the brain.
- NO Ollama/provider/API/network/subprocess/browser. Model routing is a PLAN, never a call.
- NO apply/test, NO source_apply/patch_apply, NO approval, NO PR/git/main mutation, NO Job.tasks.
- Model output never truth; never bypass approval; never retry a model indefinitely.
- Anti-loop: repeated failed action → warn/block/human_review; no infinite "try again".
- Open blocker/high review → human_review_required; budget exhaustion blocks exec-like options.
- Every next_safe_action catalog-backed + real entities; no fake commands / missing entities.
- No raw source/diff/stdout/stderr/artifact-body/secrets/tracebacks/absolute private paths.
- NO PR unless the user explicitly asks (Step 1495/1498).

## Foundation reused (read-only evidence sources)
- self_dogfood (inspection), self_dogfood_execution (list_attempts), overnight_readiness/
  overnight_executor (readiness/run + parse_review_findings + review_findings_block_execution),
  progress_ledger (build_progress_ledger), feature_planner (build_feature_plan),
  provider_trust/provider_patch_material/repair_request_builder summaries, repair_loop
  (load_repair_attempts), run_contract (ensure_contract/load_usage/evaluate_run_action),
  proof_chain/snapshot truth, do_run.validate_next_safe_action_command, command_catalog.
- proposed_tasks for self-task options.
- Review Bundle REQUIRED_SECTIONS currently 21; add orchestrator_decision_summary.json → 22.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once
  at block end. No shell=True, no subprocess.

## Next block
Local Model Advisor Adapter v0 OR Provider Trust Verification v1.

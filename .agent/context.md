# Context

## Active Branch
feature/steps-1499-1536-local-model-advisor-v0 (forked from clean main at 5d4cdf4
after PR #62 merged Main Orchestrator Brain v0). No drift.

## Mainline reconciliation (Step 1499)
- PR #62 MERGED → main. Current main commit: 5d4cdf4.
- Main Orchestrator Brain v0 landed: orchestrator_brain.py (situation → deterministic
  options → score → anti-loop guard → model routing PLAN → ONE decision + safe trace;
  idea intake). `remedy orchestrator inspect/decide/report/idea`. R-0086 resolved.
  Full suite 5723 passed, 8 skipped, 1 deselected.

## Scope
Steps 1499-1536: Local Model Advisor Adapter v0 — optional Ollama-compatible local-model
advisory layer for orchestrator decisions. Loopback-only, disabled by default, advisory-only.

## Core principle
LLMs advise. The orchestrator controls. Evidence is truth. Local cheap advisor first.

## Carried residual risks
- Local model advisor NOT built before this block (this block builds it, advisory-only).
- External/provider builder EXECUTION not built (plan-only routing).
- Provider Trust Verification v1 not built.
- Broader source patch materialization deferred (apply path .md-only).
- Self overnight not built; cleanup/retention automation not built.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Local Model Advisor constraints (block 1499-1536)
- OPTIONAL + DISABLED by default. Missing/unavailable Ollama never breaks deterministic flow.
- Loopback only (127.0.0.1 / localhost / ::1); external host, https-external, file://, redirects rejected.
- Stdlib HTTP only; NO provider/cloud SDK imports; NO subprocess for model exec; NO shell=True; NO browser.
- Short timeout; response size bounded; max 1-2 retries (no retry storm).
- Safe prompt only (phase/options/refs/counts/loop/routing); NO raw source/diff/logs/secrets/abs paths.
- JSON response required; unparseable → advisor_unparseable; code/diff in response → high concern, not accepted.
- Model output never truth; never next_safe_action/ProposedTask/Patch Intent/approval/apply/PR/job.
- Model influence limited to: lower confidence, safe missing-evidence hints, escalate weak evidence to human.
- Cannot override blocker/high review, contract, budget; cannot mark evidence complete/success/failure.
- Raw prompt/response stored PRIVATELY only if enabled (0o700 dir / 0o600 files); never public.
- Local advisor budget separate from external provider budget; exhausted → blocks advisor, not deterministic.
- No raw prompt/response/source/diff/stdout/stderr/artifact-body/secrets/tracebacks/abs paths in public surfaces.
- NO PR unless the user explicitly asks (Step 1536).

## Foundation reused
- orchestrator_brain (build_orchestrator_situation/select_orchestrator_decision/export_decision_json,
  list_decisions, RoutingTier, OrchestratorModelRoutingPlan).
- provider_trust._scrub_public / scan_secrets / _SECRET_PATTERNS / _ABS_PATH_RE / _TRACEBACK_RE (redaction).
- run_contract (ensure_contract/evaluate_run_action/ContractAction; add local_advisor_status/run).
- data_paths.resolve_data_root; storage.load_job; command_catalog/grouped CLI; do_run.validate_next_safe_action_command.
- progress_ledger.merge_*, feature_planner, review_bundle (REQUIRED_SECTIONS 22→23), ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once
  at block end with `-k "not test_full_chain_order"`. No shell=True, no subprocess.

## Product readiness — Local Model Advisor Adapter v0 (Step 1530)
CAN: optionally consult a local advisor (loopback Ollama; `remedy orchestrator decide
--use-local-advisor`, `remedy local-advisor status/run`). The advisor critiques a SAFE
decision summary and may lower confidence, add missing-evidence hints, or escalate weak+high-
risk evidence to human review. The deterministic orchestrator remains the controller; the
final next_safe_action stays deterministic + catalog-backed; a missing/unavailable advisor
never blocks deterministic operation. Surfaced in Progress/Feature/Review(23)/Cockpit; private
run storage (0o700/0o600) holds raw, public surfaces hold hashes/counts/labels only.
CANNOT (by design): be enabled by default; reach a non-loopback host; import a provider/cloud
SDK; run a subprocess for model exec; let model output become a command/entity/approval/apply/
PR/job; override contract/budget/review blockers; mark evidence complete/success/failure;
strengthen confidence; loop endlessly (reuse by prompt_hash + suppress after repeated
unavailability). Readiness ~90% (advisory rail complete; real external builder routing deferred).
FUTURE: Provider Trust Verification v1; Expensive Builder Routing v0.

## Status
Steps 1499-1536 COMPLETE. Full pytest 5777 passed, 8 skipped, 1 deselected (exit 0); integrity
fail_count=0; live review verdict PASS, zero findings. Branch pushed; NO PR (Step 1536).

## Next block
Provider Trust Verification v1 OR Expensive Builder Routing v0.

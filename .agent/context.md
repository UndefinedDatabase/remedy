# Context

## Active Branch
feature/steps-1429-1464-self-dogfood-execution-v0 (forked from clean main at fa8ebe2
after PR #60 merged Self-Dogfood Planner v0). No drift.

## Mainline reconciliation (Step 1429)
- PR #60 MERGED → main. Current main commit: fa8ebe2.
- Self-Dogfood Planner v0 landed: self_dogfood.py (inspect own evidence → Self
  ImprovementItems → Plan → metadata-only ProposedTasks via existing approval flow);
  `remedy self inspect/plan/propose/report`. No code edits/apply/approval/PR/git.
  Full suite 5662 passed, 8 skipped, 1 deselected.

## Scope
Steps 1429-1464: Self-Dogfood Execution v0. After a human approves a self-dogfood
ProposedTask, create+track a bounded SelfImprovementAttempt routed through EXISTING
gates (request package → Provider Trust Gate → materialization → approval →
do continue → snapshot/apply/test/proof). Orchestrator/tracking rail; bypasses no gate.

## Carried residual risks
- Self execution was NOT built before this block (this block builds the tracking rail).
- Automated provider execution NOT built; Provider Trust Verification v1 NOT built.
- Broader source patch materialization deferred (apply path .md-only).
- Quarantine/material/request cleanup not automated.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Self-Dogfood Execution constraints (block 1429-1464)
- Orchestrator/tracking rail; bypasses NO existing gate.
- NO code edits / direct source_apply/patch_apply; apply ONLY via approved `do continue`.
- NO approval / PR / merge / main|master mutation / git ops / direct Job.tasks insertion.
- NO provider/model/network/subprocess/browser. Candidate output enters via existing
  Provider Trust Gate + Materialization.
- Mutation-capable phase refused on main/master or unknown branch (branch read from
  .git/HEAD, no subprocess).
- pending intent ≠ completed; approved ProposedTask ≠ success; no test/proof overclaim.
- Idempotent by item fingerprint + candidate hash. No raw leaks.
- NO PR unless the user explicitly asks (Step 1457/1464).

## Foundation reused
- self_dogfood: SelfImprovementItem (fingerprint), build_self_dogfood_inspection.
- proposed_tasks: ProposedTask (task_type=self_dogfood, origin_recommendation_id=
  self_dogfood:<fp>, status PROPOSED/APPROVED_FOR_BUILD…); load_proposed_tasks/get_proposed_task.
- repair_request_builder: request package patterns (build a self request without a FailureArtifact).
- provider_trust.intake_provider_repair (failure_artifact_id OPTIONAL → generic candidate
  intake works; .md candidate → accepted → materialized pending intent).
- do_continue.run_do_continue (approved intent → snapshot/apply/test/proof; idempotent).
- run_contract ContractAction (ALL_KNOWN_ACTIONS auto-derived); _DEFAULT_ALLOWED_ACTIONS.
- Review Bundle REQUIRED_SECTIONS currently 20; add self_execution_summary.json → 21.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite
  once at block end. No shell=True, no subprocess.

## Next block
Provider Trust Verification v1 OR Self-Dogfood Overnight v0.

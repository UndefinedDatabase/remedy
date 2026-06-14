# Context

## Active Branch
feature/steps-1399-1428-self-dogfood-planner-v0 (forked from clean main at ce18aeb
after PR #59 merged Provider-Agnostic Repair Request Builder v0). No drift.

## Mainline reconciliation (Step 1399)
- PR #59 MERGED → main. Current main commit: ce18aeb.
- Repair Request Builder v0 landed: repair_request_builder.py (safe provider-agnostic
  request package from FailureArtifact; output re-enters via provider intake-repair;
  interface-only candidate generator adapter, execute raises). `remedy repair request
  / request-show`. Full suite 5627 passed, 8 skipped, 1 deselected.

## Scope
Steps 1399-1428: Self-Dogfood Readiness + Self-Improvement Planner v0. Remedy
inspects its OWN evidence and proposes safe self-improvement work as ProposedTasks
through the existing approval flow. NOT autonomous self-modification.

## Carried residual risks
- Automated provider execution NOT built.
- Provider Trust Verification v1 NOT built (regex scan may miss novel formats).
- Broader source patch materialization deferred (apply path .md-only).
- Quarantine/material/request cleanup not automated (manual; documented).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Self-Dogfood constraints (block 1399-1428)
- READ-ONLY or metadata-only. NO code edits/apply/approval/PR/git ops/main mutation;
  NO direct Job.tasks insertion; NO scheduled/background self-run.
- Self-proposed tasks enter the EXISTING ProposedTask flow (evaluate→approve→materialize).
- NO provider SDK/network/subprocess (except existing CLI runtime tests); NO browser.
- NO raw source/diff/stdout/stderr/secrets/tracebacks/absolute private paths in any surface.
- No arbitrary code scanning — known summaries/registries only.
- PENDING/FAIL/open blocker/high review → self-improvement BLOCKER.
- Idempotent by stable item fingerprint (no duplicate items or ProposedTasks).

## Foundation reused
- proposed_tasks: ProposedTask(BaseModel) + add_proposed_task/load_proposed_tasks;
  source enum USER/REVIEWER/ORCHESTRATOR/MODEL; fields task_type + origin_recommendation_id
  (use ORCHESTRATOR + task_type="self_dogfood" + fingerprint in origin_recommendation_id).
- overnight_executor.parse_review_findings → ReviewFindings (verdict + open counts).
- progress_ledger / feature_planner / review_bundle / ui_server integration patterns.
- overnight_readiness / integrity_gate / repair_loop / provider_trust / provider_patch_material
  / repair_request_builder summaries as read-only evidence sources.
- Review Bundle REQUIRED_SECTIONS currently 19; add self_dogfood_summary.json → 20.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite
  once at block end. No shell=True, no subprocess.

## Next block
Self-Dogfood Execution v0 OR Provider Trust Verification v1.

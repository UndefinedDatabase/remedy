# Context

## Active Branch
feature/steps-1681-1716-external-builder-sandbox-v0 (forked from clean main at 7cec21c after
PR #67 merged Local Candidate Quality Evaluation v1). No drift.

## Mainline reconciliation (Step 1681)
- PR #67 MERGED → main (user-confirmed). Current main commit: 7cec21c.
- Local Candidate Quality Evaluation v1 landed: candidate_quality.py (evidence-based scorecards;
  no success without proof; routing feedback read-only). `remedy candidate-quality evaluate/show/
  scorecard/report/integrity`. Reviewer verdict PASS @ 600304e. Full suite 5927 passed.

## Scope
Steps 1681-1716: External Builder Sandbox v0 — first SAFE ingress for EXTERNAL builder work:
safe request-package export + quarantined untrusted-candidate intake + bridge into existing
Trust/Verification/Candidate-Quality seams. NOT an external agent runner / provider integration.

## Core principle
External builder output is untrusted input. Worker execute, Remedy governs. No execution in
Remedy. Routing feedback is read-only confidence only. Approval + apply stay separate.

## Carried residual risks
- External builder EXECUTION still not built (this block is INGRESS only; no runner/provider).
- Cloud provider execution not built.
- Broader source patch materialization deferred (apply path .md-only).
- Self overnight not built; cleanup/retention automation not built.
- Regex/entropy scanning can miss novel secret formats (R-0083 lineage).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## External Builder Sandbox constraints (block 1681-1716)
- NO provider/model calls, network, browser, subprocess, shell=True.
- NO apply/approve/reject/test-run/git/PR/merge; NO automatic generation/repair.
- External output ALWAYS untrusted → quarantined privately → same Trust Gate + Verification +
  Materialization + human Approval + do_continue path as local candidates. Raw candidate never rendered.
- Routing feedback only influences confidence/recommendation; never starts work.
- No raw prompt/candidate/diff/stdout/stderr/traceback/secrets/abs paths in public reports/bundles/
  scorecards/UI/CLI JSON. Bounded candidate size; symlink/traversal/protected/binary rejected safely.
- Every next_safe_action catalog-backed + entity-backed. NO PR unless user explicitly asks.

## Foundation reused
- provider_trust.intake_provider_repair (quarantine→trust→verification→materialize) via provider
  label `external_builder:<source_label>`; _scrub_public for redaction; read_intake_input bounds.
- candidate_quality.evaluate_candidate_quality (+ optional model/route override for external source).
- builder_routing.route_quality_feedback (read-only confidence).
- local_candidate_generator private-storage/CLI patterns; run_contract; command_catalog/grouped CLI.
- progress_ledger.merge_*, feature_planner, review_bundle (REQUIRED_SECTIONS +external_builder_summary.json), ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once
  at block end with `-k "not test_full_chain_order"`. No shell=True, no subprocess (except CLI runtime tests).

## Changed files (Steps 1681-1716) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/external_builder_sandbox.py | NEW core: request-package + submission models, safe export (idempotent), private storage, bounded/protected intake → existing trust/verification bridge, integrity | the untrusted ingress rail |
| packages/orchestration/run_contract.py | external_builder_package/submit/show actions (default-allowed, non-exec) | contract gate |
| apps/cli/commands/external_builder_cmd.py | NEW package-create/show/list, submit, submission-show/list, evaluate, integrity handlers | CLI surface |
| apps/cli/commands/__init__.py | register external_builder_cmd | wire handlers |
| apps/cli/command_catalog.py | external-builder group + 8 entries (create/submit/evaluate write_metadata; rest read_only; no may_execute) | catalog-backed |
| packages/orchestration/candidate_quality.py | evaluate_candidate_quality model_label/route_tier overrides for external source | external submissions scored by external route/source |
| packages/orchestration/builder_routing.py | external branch consults route_quality_feedback → escalate on poor external history (read-only; no auto-run) | external routing feedback |
| packages/orchestration/progress_ledger.py | extract/merge_external_builder_items (fixed item_ids) | surface ingress, no fake "running" |
| packages/orchestration/feature_planner.py | 3 external-builder rules (approve/route-contract-review) | evidence-based suggestions, no new exec |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 27→28 + _build_external_builder_summary | bundle safe summary |
| packages/orchestration/ui_server.py | _build_external_builder_section cockpit (live=false) | read-only, no buttons/run-button |
| tests/orchestration/test_external_builder_sandbox.py | NEW 26 tests (package/submission/quality/integrity/smoke/arch/redaction-torture) | coverage |
| tests/cli/test_external_builder_cli.py | NEW 7 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==28 + assert | bundle test |
| tests/ui_server/test_dashboard_cockpit_truth.py | test_external_builder_section_present | cockpit test |
| docs/external-builder-sandbox-v0.md, docs/external-builder-worker-contract-v0.md | NEW docs (scope contract + worker contract) | document rail + anti-goals |
| .agent/context.md, .agent/plan.md | reconciliation + readiness + changed-files table | handoff |

## Status
Steps 1681-1716 COMPLETE (builder). Full pytest 5969 passed, 8 skipped, 1 deselected (exit 0).
Builder self-run counts; parallel reviewer owns the live_review verdict (PENDING). NO PR.

## Next block
Model/Route Tournament Harness v0 (only if this block PASS).

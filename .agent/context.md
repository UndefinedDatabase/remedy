# Context

## Active Branch
feature/steps-1645-1680-local-candidate-quality-evaluation-v1 (forked from clean main at
3641618 after PR #66 merged Automated Local Candidate Generator v0). No drift.

## Mainline reconciliation (Step 1645)
- PR #66 MERGED → main. Current main commit: 3641618.
- Automated Local Candidate Generator v0 landed: local_candidate_generator.py (loopback model
  generation, disabled by default, routing-gated, output→quarantine→trust→verification→
  materialize→pending approval). `remedy local-candidate status/generate`. Reviewer verdict PASS.
  Full suite 5887 passed, 8 skipped, 1 deselected.

## Scope
Steps 1645-1680: Local Candidate Quality Evaluation v1 — evidence-based scorecards for candidate-
generation outcomes (was it useful, not just safe?). Evaluation/reporting/routing-feedback only.

## Core principle
Evidence, not model confidence, determines quality. No score claims success without linked
proof/test evidence. Candidate quality feeds future routing. No automatic execution.

## Carried residual risks
- External builder EXECUTION not built (next block: External Builder Sandbox v0).
- Cloud provider execution not built.
- Candidate quality evaluation NOT built before this block (this block builds it).
- Broader source patch materialization deferred (apply path .md-only).
- Self overnight not built; cleanup/retention automation not built.
- Regex/entropy scanning can miss novel secret formats (R-0083 lineage).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Candidate Quality Evaluation constraints (block 1645-1680)
- Evaluation/reporting/routing-feedback ONLY. No generation, no model/provider calls, no approval/apply/test/PR/git/mutation.
- No score claims success without linked proof/test evidence; pending approval ≠ completed; model confidence ≠ truth.
- Score ≤ medium if verification missing; not high if human decision unknown; not excellent without proof_verified; rejected/trust-failed → low.
- Routing feedback NEVER triggers automatic generation.
- Reports = safe IDs/hashes/counts/statuses/evidence refs only; no raw prompt/output/candidate/diff/source/stdout/stderr/secrets/tracebacks/abs paths.
- No token/cost invention. Every next_safe_action catalog-backed + entity-backed.
- NO PR unless the user explicitly asks (Step 1680).

## Foundation reused (read-only evidence sources)
- local_candidate_generator.list_local_candidate_runs (generation manifests: status + trust/verification/material/intent linkage + model_name).
- provider_trust.load_trust_reports; provider_trust_verification.load_verification_reports;
  provider_patch_material.load_materials; approval_queue.list_patch_intents (state pending/approved/rejected).
- proof_chain.build_proof_chain + repair_loop._load_events_safe (ProofChange per intent: approval/apply/test/proof_status).
- builder_routing.load_builder_routing_traces; provider_trust._scrub_public (redaction).
- run_contract (add candidate_quality_evaluate/show/scorecard/report); data_paths/storage; command_catalog/grouped CLI.
- progress_ledger.merge_*, feature_planner, review_bundle (REQUIRED_SECTIONS +candidate_quality_summary.json), ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once
  at block end with `-k "not test_full_chain_order"`. No shell=True, no subprocess (except CLI runtime tests).

## Product readiness — Local Candidate Quality Evaluation v1 (Step 1673)
CAN: evaluate a generated candidate's OUTCOME from durable evidence (`remedy candidate-quality
evaluate/show/scorecard/report/integrity`): outcome classification + 11 score dimensions with
invariant ceilings (≤medium w/o verification, not high w/o human decision, not excellent w/o
proof_verified, rejected→low, pending≠completed); idempotent by evidence fingerprint; model/route
scorecards (rates/counts, no cost invention). Builder Routing consumes feedback (repeated poor
quality → human review; proof-verified → raise; unknown never promotes expensive). Surfaced in
Progress/Feature/Review(27)/Cockpit; private 0o600 evaluation storage.
CANNOT (by design): generate candidates; call models/providers/network/subprocess/SDK; approve/
apply/test/PR/git/mutate; claim success without proof/test evidence; treat pending approval as
completed or model confidence as truth; trigger automatic generation via routing feedback; leak raw
prompt/output/candidate/diff/source/secrets/paths. Readiness ~85% (evaluation rail complete;
tournament harness + external builder sandbox deferred).

## Changed files (Steps 1645-1680) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/candidate_quality.py | NEW core: models/taxonomy, evidence gather, scoring+invariant ceilings, outcome classification, idempotent evaluate, scorecards, route feedback, integrity | the evaluation rail |
| packages/orchestration/run_contract.py | candidate_quality_evaluate/show/scorecard/report actions (default-allowed, non-exec) | contract gate |
| apps/cli/commands/candidate_quality_cmd.py | NEW evaluate/show/scorecard/report/integrity handlers | CLI surface |
| apps/cli/commands/__init__.py | register candidate_quality_cmd | wire handlers |
| apps/cli/command_catalog.py | candidate-quality group + 5 entries (evaluate write_metadata; rest read_only) | catalog-backed |
| packages/orchestration/builder_routing.py | local-candidate branch consults route_quality_feedback → escalate on poor quality (read-only, no auto-gen) | routing feedback |
| packages/orchestration/progress_ledger.py | extract/merge_candidate_quality_items (fixed item_ids) | surface quality, no raw |
| packages/orchestration/feature_planner.py | 5 candidate-quality repair rules | suggestions, no auto-exec |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 26→27 + _build_candidate_quality_summary | bundle safe summary |
| packages/orchestration/ui_server.py | _build_candidate_quality_section cockpit | read-only, no buttons |
| tests/orchestration/test_candidate_quality.py | NEW 24 tests (scoring/invariants/feedback/integrity/integration/redaction/arch) | coverage |
| tests/cli/test_candidate_quality_cli.py | NEW 7 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==27 + assert | bundle test |
| tests/ui_server/test_dashboard_cockpit_truth.py | test_candidate_quality_section_present | cockpit test |
| docs/candidate-quality-evaluation-v1.md, docs/model-route-tournament-future.md | NEW docs | document rail + future |
| docs/{local-candidate-generator-v0,expensive-builder-routing-v0,provider-trust-verification-v1,orchestrator-brain-v0}.md | cross-ref updates | document the new stage |

## Status
Steps 1645-1680 COMPLETE. Full pytest 5927 passed, 8 skipped, 1 deselected (exit 0).
Builder self-run counts; parallel reviewer owns the live_review verdict. NO PR (Step 1680).

## Next block
External Builder Sandbox v0 OR Model/Route Tournament Harness v0.

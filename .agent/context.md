# Context

## Active Branch
feature/steps-1609-1644-automated-local-candidate-generator-v0 (forked from clean main at
4d4d7ad after PR #65 merged Expensive Builder Routing v0). No drift.

## Mainline reconciliation (Step 1609)
- PR #65 MERGED → main. Current main commit: 4d4d7ad.
- Expensive Builder Routing v0 landed: builder_routing.py (local-first routing/policy; planning
  only; external disabled by default; gated behind request package + trust + verification +
  budget + low loop risk + no pending). `remedy builder-routing decide/report`. R-0088/R-0089
  (unrunnable next_safe_action shapes) + R-0090 (handoff table) resolved; reviewer verdict PASS.
  Full suite 5852 passed, 8 skipped, 1 deselected.

## Scope
Steps 1609-1644: Automated Local Candidate Generator Adapter v0 — the FIRST adapter that calls
an explicitly-configured local loopback model to generate candidate output, which immediately
enters the untrusted intake pipeline (quarantine → Trust Gate → Verification → Materialization
→ pending approval).

## Core principle
Local model may generate candidates. The orchestrator controls. Trust + Verification judge.
Human approves. do_continue applies. Model output is UNTRUSTED.

## Carried residual risks
- External builder EXECUTION not built (next block: External Builder Sandbox v0).
- Cloud provider execution not built.
- Local candidate generator NOT built before this block (this block builds it).
- Broader source patch materialization deferred (apply path .md-only).
- Self overnight not built; cleanup/retention automation not built.
- Regex/entropy scanning can miss novel secret formats (R-0083 lineage).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Local Candidate Generator constraints (block 1609-1644)
- DISABLED by default; explicit env opt-in; loopback only; external/file:///redirects rejected.
- No cloud/provider SDK; no external network; no subprocess for model exec; no shell=True; no browser.
- Model output UNTRUSTED → quarantined before parsing → Trust Gate + Verification before materialization.
- No candidate output creates an intent directly; no approval/apply/test/PR/git from this adapter.
- Only runs if Builder Routing selected local_candidate_generator + policy/contract allow + request
  package + no pending intent + trust/verification available + budget + low loop risk + no open blocker/high.
- Missing local model never breaks deterministic flow.
- No raw prompt/output/source/diff/stdout/stderr/artifact-body/secrets/tracebacks/abs paths in public surfaces.
- NO PR unless the user explicitly asks (Step 1644).

## Foundation reused
- local_model_advisor: _validate_endpoint / _stdlib_transport / _extract_generate_text / Transport
  seam / _LOOPBACK_HOSTS / private-run-storage pattern (loopback client, disabled-by-default config).
- provider_trust.intake_provider_repair: the intake bridge (quarantine→trust→verification→materialize),
  called with provider_name=`local_candidate_generator:<model>`; _scrub_public for redaction.
- builder_routing.select_builder_routing_decision: routing gate (must select local_candidate_generator).
- repair_request_builder.get_request_package / render_request_markdown: safe prompt source.
- run_contract (add local_candidate_generator_status/local_candidate_generate).
- data_paths.resolve_data_root; storage.load_job; command_catalog/grouped CLI.
- progress_ledger.merge_*, feature_planner, review_bundle (REQUIRED_SECTIONS +local_candidate_summary.json), ui_server cockpit.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once
  at block end with `-k "not test_full_chain_order"`. No shell=True, no subprocess (except CLI runtime tests).

## Product readiness — Automated Local Candidate Generator v0 (Step 1637)
CAN: generate a repair/self candidate via a routing-gated, explicitly-configured LOOPBACK model
(`remedy local-candidate generate --request-package-id … --json`) and IMMEDIATELY route the
UNTRUSTED output through quarantine → Trust Gate → Verification → Materialization → pending
approval. Disabled by default; loopback only; idempotent by (request_package_id, model,
prompt_hash); attempt-capped; private 0o600 run storage. Surfaced in Progress/Feature/
Review(26)/Cockpit; Builder Routing emits the generate command for the local_candidate_generator
tier. Reuses local_model_advisor endpoint validation + transport seam (no real Ollama in CI).
CANNOT (by design): be enabled by default; reach a non-loopback host; import provider/cloud SDK;
subprocess/shell for model exec; bypass Builder Routing; create an intent before Trust Gate +
Verification; approve/apply/test/PR/git; loop generation without new evidence; break deterministic
flow when the model is missing; leak raw prompt/output/secrets/paths. Readiness ~85% (generation
rail complete; quality evaluation + external builder sandbox deferred).

## Changed files (Steps 1609-1644) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/local_candidate_generator.py | NEW core: config/policy, safe prompt builder, loopback client (reuses advisor utils), private run storage, intake bridge, routing gate, budget/idempotency, exports | the generation rail |
| packages/orchestration/run_contract.py | LOCAL_CANDIDATE_GENERATOR_STATUS/GENERATE actions (default-allowed, non-cloud) | contract gate |
| apps/cli/commands/local_candidate_cmd.py | NEW `local-candidate status/generate` handlers | CLI surface |
| apps/cli/commands/__init__.py | register local_candidate_cmd | wire handlers |
| apps/cli/command_catalog.py | local-candidate group + status(read_only)/generate(write_metadata) entries | catalog-backed |
| packages/orchestration/builder_routing.py | local_candidate route emits `local-candidate generate` next action (entity-backed) | orchestrator/routing wiring |
| packages/orchestration/progress_ledger.py | extract/merge_local_candidate_items (fixed item_ids) | surface generation state, no raw |
| packages/orchestration/feature_planner.py | 5 local-candidate repair rules | suggestions, no auto-retry |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 25→26 + _build_local_candidate_summary | bundle safe summary |
| packages/orchestration/ui_server.py | _build_local_candidate_section cockpit | read-only, no buttons |
| tests/orchestration/test_local_candidate_generator.py | NEW 20 tests (config/endpoint/routing/trust-pipeline/idempotency/redaction/arch) | coverage |
| tests/cli/test_local_candidate_cli.py | NEW 6 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==26 + assert | bundle test |
| tests/ui_server/test_dashboard_cockpit_truth.py | test_local_candidate_section_present | cockpit test |
| docs/local-candidate-generator-v0.md, docs/external-builder-sandbox-future.md | NEW docs | document rail + future |
| docs/{expensive-builder-routing-v0,local-model-advisor-v0,provider-trust-verification-v1,repair-request-builder-v0,self-dogfood-execution-v0}.md | cross-ref updates | document the new stage |

## Status
Steps 1609-1644 COMPLETE. Full pytest 5887 passed, 8 skipped, 1 deselected (exit 0).
Builder self-run counts; parallel reviewer owns the live_review verdict. NO PR (Step 1644).

## Next block
External Builder Sandbox v0 OR Local Candidate Quality Evaluation v1.

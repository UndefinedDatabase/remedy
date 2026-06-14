# Context

## Active Branch
feature/steps-1365-1398-repair-request-builder-v0 (forked from clean main at 871fb8d
after PR #58 merged Provider Patch Materialization v0). No drift.

## Mainline reconciliation (Step 1365)
- PR #58 MERGED → main. Current main commit: 871fb8d.
- Provider Patch Materialization v0 landed: provider_patch_material.py (private
  material, unified-diff/JSON-ops → single .md create/modify, verification,
  idempotent materialize); intake materializes accepted candidates → applyable
  pending Repair Patch Intent; approve → do continue → snapshot → apply →
  completed_verified proven. No provider SDK/network/subprocess. Full suite 5599
  passed, 8 skipped, 1 deselected.

## Scope
Steps 1365-1398: Provider-Agnostic Repair Request Builder v0. From a FailureArtifact,
build a SAFE structured RepairRequestPackage for ANY external worker/model/human.
External output re-enters ONLY via existing `provider intake-repair`. Define an
interface-only candidate generator adapter boundary (no execution in v0).

## Architecture principle (load-bearing)
Provider-/worker-/model-/subscription-/IDE-/account-AGNOSTIC. NEVER depend on or
require: Claude Max, subscription tiers, a specific IDE, browser/account automation,
or any single provider as infrastructure. Providers appear ONLY as example external
untrusted candidate generators.

## Carried residual risks
- Automated provider execution NOT built (this block: request packaging + adapter
  interface only; next block could add an Automated Candidate Generator Adapter v0).
- Broader source patch materialization deferred (apply path stays .md-only).
- Regex secret scan may miss novel formats (defense-in-depth: scrub + scan in gate).
- Quarantine/material retention documented; cleanup automation not built.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Request Builder constraints (block 1365-1398)
- NO provider/SDK/API/network/subprocess/browser/IDE/agent. NO apply/test execution.
- NO Patch Intent creation from request generation; NO direct provider-intake call.
- Request packages SAFE to share with an untrusted external actor: no raw stdout/
  stderr/source/diff/artifact-body/secrets/tracebacks/absolute private paths.
- External output re-enters ONLY via `remedy provider intake-repair`.
- Adapter execute() raises CandidateGeneratorExecutionUnavailable in v0.
- Idempotent request packages; `--new` to force a fresh one.
- Every next safe action catalog-backed + references real entities.
- DO NOT create a PR unless the user explicitly asks (Step 1398).

## Foundation reused
- repair_loop.build_repair_context(job_id, fa_id, data_dir) → RepairContextSummary
  (safe: safe_summary, changed_files_safe, proof_status, snapshot_status, failure_kind,
  test_run_id/task_id/intent_id/apply_id). find_repair_attempt / save_repair_attempt /
  RepairAttempt.
- provider_trust intake (`remedy provider intake-repair <job> --failure-artifact-id
  <id> --input <file> --provider <label> --json`) → Trust Gate → materialization.
- run_contract ContractAction (ALL_KNOWN_ACTIONS auto-derived); _DEFAULT_ALLOWED_ACTIONS.
- Review Bundle REQUIRED_SECTIONS currently 18; add repair_request_summary.json → 19.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite
  once at block end. No shell=True, no subprocess.

## Next block
Provider Trust Verification v1 OR Automated Candidate Generator Adapter v0.

# Context

## Active Branch
feature/steps-1335-1364-provider-patch-materialization-v0 (forked from clean main at
b38cf94 after PR #57 merged Provider Trust Gate v0). No drift.

## Mainline reconciliation (Step 1335)
- PR #57 MERGED → main. Current main commit: b38cf94.
- Provider Trust Gate + External Repair Intake v0 landed: provider_trust.py
  (quarantine private, parser, secret/path/patch/failure validation, trust decision,
  ProviderTrustReport, accepted→pending intent placeholder). `remedy provider
  intake-repair|trust-show`. No provider execution/network/subprocess. Full suite
  5568 passed, 8 skipped, 1 deselected.

## Scope
Steps 1335-1364: Trusted Provider Patch Materialization v0 — turn ACCEPTED provider
candidates into REAL applyable Repair Patch Intents (flow through approval →
do continue → snapshot → apply → test → proof), raw diff/output stays private.

## Key constraint (apply path)
`apply_patch_intent` is `.md`-only: create writes a markdown file from a "Proposed
Changes:" section (`  - line` entries) in the artifact content; modify appends a
section; no arbitrary diff application, no source files. So a materialized intent is
genuinely apply-compatible ONLY for a single `.md` target. Source/binary/delete/
rename/multi-file candidates → `unsupported_patch_shape` (accepted but no intent).

## Carried residual risks
- Provider-backed builder NOT built (next block wires real builders behind the gate).
- Materialization is conservative v0: single .md create/modify only; source patches
  are accepted-but-not-materialized (apply path cannot apply source files yet).
- Regex-based secret scanning can miss novel formats (defense-in-depth: scrub + scan).
- Quarantine/material retention: private workspace only, manual cleanup future (doc 1352).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Materialization constraints (block 1335-1364)
- NO provider/Ollama/Claude SDK, NO network, NO subprocess, NO shell=True.
- Raw patch material ONLY in `.data/workspaces/<job>/provider_patch_material/<id>/`
  (0o700/0o600, atomic, hashed). NEVER exported publicly.
- No raw diff/source/stdout/stderr/artifact-body/secrets/tracebacks/abs paths public.
- Patch Intent exposes safe metadata only; apply ONLY via approved `do continue`.
- accepted ≠ materialized ≠ applied ≠ verified. No auto-apply/approval.
- Idempotent by candidate_hash; no duplicate Fix Task / Repair Artifact / Intent.
- Every next safe action catalog-backed + entity-backed; no fake intent IDs.

## Foundation reused
- apply_patch_intent (.md create/modify; "Proposed Changes:" `  - line` format;
  _validate_target_path .md-only; snapshot mandatory).
- approval_queue: intents = patch_intent_explanations on Artifact metadata, keyed
  make_intent_id(art.id, idx); get_patch_intent/list_patch_intents/set_approval_state.
- provider_trust.py: ProviderTrustReport, quarantine, _scrub_public, scan_secrets,
  validate_paths/patch_shape. do_continue (snapshot→apply→test→proof, idempotent).
- run_contract ContractAction (ALL_KNOWN_ACTIONS auto-derived); _DEFAULT_ALLOWED_ACTIONS.
- Review Bundle REQUIRED_SECTIONS currently 17; add provider_material_summary.json → 18.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite
  once at block end. No shell=True, no subprocess.

## Product readiness — Provider Patch Materialization v0 (Step 1360)
CAN: an accepted external-provider candidate (single `.md` create/modify) is now
MATERIALIZED into a real, applyable pending Repair Patch Intent that flows through
`remedy patch approve` → `remedy do continue` → snapshot → apply → test → proof via
the EXISTING apply path (no special provider apply). Raw diff stays in private
workspace storage; public surfaces carry safe metadata only. Idempotent by candidate
hash. Surfaced in Progress/Feature/Review(18)/Cockpit; verifiable via material-show.
CANNOT (by design): NO provider execution/network/subprocess; NO auto-apply/approval;
source/multi-file/delete/rename/binary candidates → unsupported_patch_shape (no
intent — apply path is .md-only in v0). accepted ≠ materialized ≠ applied ≠ verified.
Next block (Provider-backed Repair Builder v0) can wire a real local-first gated
builder BEHIND this gate to PRODUCE candidates (the trust+materialization boundary
stays); extending the applyable surface beyond .md is separate future work.

## Next block
Provider-backed Repair Builder v0.

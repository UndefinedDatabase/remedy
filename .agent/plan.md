# Plan — F012 Round 40 — Package-Authority Closure

Round-39 contracts FROZEN. External review returned five authority findings. Round 40 closes
exactly these five. No broadening.

## Scope 1 — manual-completion identity and operator attestation

Round 39's Evidence claims `manual_operator_repair` / `operator_attested_complete` in task
manifests and provider evidence, but the final verifier reports `manual_completion=false` /
`operator_attested_tasks=[]` because task directories lack complete manual-attestation
artifacts (manual_repair_provenance.json with correct fields, operator-attested review.json).

Fix:
- Create `validate_manual_completion_identity(evidence_view)` in build_review_manifest.py —
  a fail-closed function that identifies ANY manual claim in the bundle and requires the
  COMPLETE manual contract when one is found. Mixed identity blocks.
- Integrate into `_build_manifest()` so READY blocks on a manual-claiming bundle that fails
  manual validation.
- Ensure `validate_evidence_candidate()` does not allow a manual-claiming bundle to bypass
  the manual path.
- Generate fresh R40 Evidence through `create_manual_completion_bundle` so the FVR reports
  `manual_completion=true`, `operator_attested_tasks=[all]`, `human_final_reviewer_required=true`.
- Test: a mixed-identity bundle blocks.

## Scope 2 — unconditional commit-patch byte/chain verification

Round 39's packaged patches were generated with `git format-patch` while the chain's
`patch_sha256` values come from `git diff-tree -p` (the canonical producer). All 9 mismatch.

Fix:
- Regenerate all patch files using the canonical `commit_patch_bytes()` producer.
- Verify every packaged patch matches its `patch_sha256` from the chain.
- The existing `_verify_commit_patches()` in build_review_manifest.py already checks this —
  it was just the Evidence that had wrong bytes.
- Test: add a test that forges one patch body and verifies it blocks.

## Scope 3 — complete ProviderTokenEvidenceV1 preservation/rejection contract

Round 39's validator accepts and silently discards trust-bearing fields like `task_id`
mismatch, `provider_attempts`, `actual_provider_available=true`, `prompt_trace_available=true`,
`completion_provider_call_count=999`, `reviewer_provider` on manual, `cli_versions` typed wrong.

Fix:
- In `provider_token_evidence.py`: add cross-field validation for manual mode:
  - `completion_provider_call_count` must be 0 or absent
  - `provider_attempts` must be absent or empty list
  - `actual_provider_available` must be false or absent
  - `prompt_trace_available` must be false
  - `reviewer_provider` must be "operator" or absent
  - `cli_versions` must be dict or absent
  - `task_id` must match containing directory (validated in token_truth.py)
- In `token_truth.py`: validate `task_id` in PE matches directory name.
- Test: the exact combined reproduction from the finding produces TokenEvidenceError.

## Scope 4 — package-enforced diagnostic and verification Evidence

Round 39's diagnostic_broad_run.json references HEAD 03e6e206 (stale), not current HEAD
9cee26d. Package construction does not validate or block on stale diagnostics.

Round 39's verification_matrix.py is not invoked by package construction.

Fix:
- For diagnostics: do NOT package a stale diagnostic. Remove stale `diagnostic_broad_run.json`
  from Evidence. The package does not require it for READY. If present, validate it.
- For verification: define the F012 required suite contract as a production constant.
  Package construction validates verification_tests.json completeness.
- Test: missing required verification run blocks.

## Scope 5 — manifest-bound publication capability with capability-aware tests

Round 39's coordinator probes capability but the root manifest doesn't bind it.

Fix:
- In build_review_manifest.py: record publication_capability in the root manifest with
  status/primitive/checked_at fields, bound into the package hash chain.
- Ensure capability-aware tests work on both supported and unsupported paths.
- No new named-path fallback.

## Commits (in order)

1. `fix(evidence): manual-completion identity contract and canonical Evidence`
2. `fix(evidence): canonical commit-patch bytes from repository producer`
3. `fix(evidence): complete ProviderTokenEvidenceV1 cross-field contract`
4. `fix(evidence): package-enforced diagnostic and verification authority`
5. `fix(evidence): manifest-bound publication capability`
6. `docs(f012): truthful Round-40 documentation and operator state`

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local
commits, never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked to
prior `r39_closed_pe_diagnostic_verification_capability`, VERIFIED_EQUAL, git OK; one READY ZIP;
then stop.

# Plan — Steps 12961-13160 — F012 hardening round 27 (REAL TOKEN SHAPES, COMPLETE VERIFICATION TYPING, SAFE ACQUISITION/DIRTY/DECODER BOUNDARIES)

## Round 27 binding decision

Reviewed `remedy-review-20260718-213237-READY_FOR_REVIEW.zip`
(SHA `9bfe1e5abdedc8d004164b7101cb7c111bef967607cca858c9a8cb11384dd850`, Evidence job
`ebe675ec74f20c1a`, linked prior `a67d0c3f0513bd11`, HEAD `7fa4466`). Verdict FINDINGS; F012 `[~]`.

1. **Real token summary schema** — `_ACTUAL_TOKEN_SUMMARY` matches the real
   `final_verifier._token_measurement_summary` (17 fields, mostly nullable); reused for
   token_measurement.actual_summary + top-level token_actual_summary; measurement notes nullable;
   top-level projection must equal the nested block. Non-overlapping scope: token schema only.
2. **Full VerificationTestsV1 typing** — aligned to `job_evidence._run_verifications`: typed
   command/timestamp/run_id/stdout_summary, nonnegative per-run counts, safe sorted unique test
   paths, unique run ids/commands, metadata scan. Scope: validate_verification_tests only.
3. **Acquisition overflow never absence** — `_StagedArtifacts.load` charges from a trusted anchored
   lstat size before reading; overflow raises ArchivePlanError; absence/symlink/torn distinguished.
   Scope: build_review_zip _StagedArtifacts only.
4. **Exact packaging-output identity** — `_is_packaging_output` requires a repo-ROOT path + exact
   `make_review_zip.sh` filename grammar. Scope: _is_packaging_output only.
5. **Strict decode at every trust boundary** — job_flow/manual_repair_provenance/manifest/NO_EVIDENCE
   via the shared strict decoder. Scope: the four remaining bare json.loads sites.

## Constraints (unchanged)

No provider calls; no Evidence job-flow/job-run; no database; no LLM rerun; no network. Small local
commits, never amend/squash Round 26. Do not push, PR, merge, or begin F017. Fresh Evidence linked
`ebe675ec74f20c1a`; one READY_FOR_REVIEW ZIP; then stop. Preserve every accepted F012 behavior.

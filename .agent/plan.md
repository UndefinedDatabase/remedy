# Plan — Steps 12761-12960 — F012 hardening round 26 (FULLY TYPED GATE SHAPES + FAIL-CLOSED VERIFICATION TOTAL + BOUNDED ACQUISITION)

## Round 26 binding decision

Reviewed `remedy-review-20260718-201125-READY_FOR_REVIEW.zip`
(SHA `2250e8cb8d82cecc3b37721ab81a6a5d61816cba7d55634e0d7f80d778374674`, Evidence job
`a67d0c3f0513bd11`, linked prior `041261b92c134f5b`, HEAD `78cbb9b`). Verdict FINDINGS; F012 `[~]`.

1. **Fully typed gate shapes** — no `ANY`. `_Nullable(node)` for null-able producer fields,
   `_OneOf(...)` for closed unions, `_HASH_MISMATCH`/`_FINDING`/`_MODELS` exact records, and two
   distinct `_TOKEN_STATUS` (25 fields) / `_TOKEN_MEASUREMENT` (16 fields) shapes. bool rejected
   where an int/number is required.
2. **Required nested fields** — `_Obj(fields, optional=...)`; a required field absent blocks. Full
   producer shape required for every gate and nested object (token blocks, stream/worktree sections,
   test_status, evidence_freshness/validity, integrity notes).
3. **Strict fail-closed VerificationTestsV1** — exact version {"1.0.0"}, exact top-level + per-run
   field sets, real-int exit_code/passed/failed (bool rejected, NO int() coercion), exit_code==0,
   failed==0, passed>=1, unique run ids, totals==sum of runs, test_files==union. Used by the gate
   matrix AND validate_manual_completion. Missing/invalid/mismatch blocks; FV total must equal it.
4. **One shared acquisition budget** — `packages/common/acquisition_budget.AcquisitionBudget`
   (per-member/aggregate/count/duplicate), charged by `_view_from_dir` AND `_StagedArtifacts`;
   exceed BLOCKS (raises); a cached re-read does not recharge.
5. **One shared strict JSON decoder** — `packages/common/strict_json.py`; both scripts import it,
   no private object_pairs_hook copy.
6. **Packaging output disposition** — `.review_zip_manifest.json`, `remedy-review-*.zip[.sha256]`
   get an explicit `packaging_generated_outputs` disposition; clean branch stays clean; real dirty
   stays dirty; a source lookalike is never hidden.

## Constraints (unchanged)

No provider calls; no Evidence job-flow/job-run; no database; no LLM rerun; no network. Small local
commits, never amend/squash. Do not push, PR, merge, or begin F017. Fresh Evidence linked
`a67d0c3f0513bd11`; one READY_FOR_REVIEW ZIP; then stop.

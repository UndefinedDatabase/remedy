# Plan — Steps 12561-12760 — F012 hardening round 25 (RECURSIVE GATE SCHEMA + SAFE SNAPSHOT ACQUISITION)

## Round 25 binding decision

Reviewed `remedy-review-20260718-190112-READY_FOR_REVIEW.zip`
(SHA `d40e2454dbfe0e576412bdc257ad7da4aede484256f694d1437f33b44afa0cb9`, Evidence job
`041261b92c134f5b`, linked prior `14f211210d044bfb`, HEAD `3d11fc9`). Verdict FINDINGS; F012 `[~]`.

1. **Exact recursive gate schemas** — a typed `_GATE_SCHEMA` (_Obj/_Map/_Arr/_Scalar) closes every
   NESTED object's field set, types every element, and enforces a dynamic-map KEY grammar (task IDs
   `^T\d{3,}$`, gate names, safe relative file/artifact paths). An unknown nested field, a wrong
   type, or a bad key blocks. bool is rejected where an integer is required.
2. **Complete gate semantics** — FV: all evidence_completeness true, spec/scratch/change/alignment
   PASS, token_cost_has_critical false, token_cost_risk_findings empty, test_status.passed a
   nonnegative int == recorded verification total. Fresh: current_job_id == evidence_job_id and the
   three step ranges equal. Artifact: exact CORE_ARTIFACTS required-key set; applicable stream/
   worktree PASS or exact NOT_APPLICABLE. Change: covered == source-excluded == evidence_covered ==
   ContentProof authority; current_hashes == evidence_hashes == ContentProof file hashes (ONE
   authority model, decoded by the same loader).
3. **Metadata key safety** — the recursive scanner walks dictionary KEYS as well as values; secret/
   local-path/control/over-length/credential-name keys block; dynamic keys satisfy their grammar.
4. **Exact commit-gate issues** — blocked_gates, non_pass_gates AND issues derived from gate_checks
   by the writer's rule; empty/unrelated/extra issues block.
5. **Duplicate-key decoder** — one dependency-free object_pairs_hook rejects duplicate keys at any
   depth for every gate/subject/proof/chain decode in build_review_manifest and build_review_zip.
6. **One secure staged-byte acquisition seam** — `_StagedArtifacts.load` and `_view_from_dir`
   acquire every member through anchored O_NOFOLLOW secure_fs reads; never os.path.isfile/os.walk/
   open by name; per-member and aggregate size limits enforced; a symlink is never followed.

## Constraints (unchanged)

No provider calls; no Evidence job-flow/job-run; no database; no LLM rerun; no network. Small local
commits, never amend/squash. Do not push, PR, merge, or begin F017. Fresh Evidence linked
`041261b92c134f5b`; one READY_FOR_REVIEW ZIP; then stop.

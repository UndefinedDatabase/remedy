# Plan — Steps 14161-14360 — F012 Final Publication & Token-Contract Repair Round 33

Reviewed `remedy-review-20260719-215803-READY_FOR_REVIEW.zip` (SHA `3149a10e...7b64`, Evidence
`453aab97e0fc3b01`, prior `2d1e749dcff40512`, base `fbbd584`, HEAD `13cd5a5d`). Accepted and preserved:
final-verifier reproducibility, total gate eval, git-status snapshot, patchset identity, integration
termination, manual token-truth regeneration/equality, producer-reproducible FV. Four bounded findings,
one commit each. No broadening.

1. **Atomic no-clobber publication lifecycle (F1).** `safe_publish.publish_atomically(src_bytes_path,
   final_path, repo_root)`: build+verify the ZIP at a private same-filesystem temp path, then publish
   through ONE no-replace primitive (`os.link` then unlink temp, or `O_CREAT|O_EXCL` link) so exactly
   one concurrent invocation wins; a loser returns a controlled collision error, never success.
   `build_review_zip_from_snapshot` stops unlinking `out_path`. The coordinator builds to a private temp
   then publishes atomically; the shell calls the SAME publication (no second weaker `mv`). No failure
   path leaves an empty reservation or partial public ZIP; the private temp is always cleaned.
2. **Fail-closed Git tracked-status (F2).** `safe_publish` interprets `git ls-files --error-unmatch`
   by EXACT exit code: 0→TRACKED (block), 1→UNTRACKED (allow), anything else / timeout / missing exec
   → GIT_FAILED/GIT_TIMED_OUT/GIT_UNAVAILABLE → block with a bounded diagnostic. A repo/index/permission
   failure never becomes "untracked".
3. **Shared token producer/validator schema (F3).** `token_truth` exposes the canonical measurement
   source/confidence enums + schema version; `token_authority` imports them (no duplicated strings).
   Supported sources = exactly what `build_token_truth` emits: `character_heuristic`, `provider_actuals`,
   `mixed_provider_actuals_and_heuristic` (drop `provider_api`). Complete state invariants for
   low/high/mixed/zero-provider/no-actual/incomplete-cost/complete. A meta-regression runs every real
   producer fixture through the validator.
4. **Real manual-Evidence operator entry (F4).** Expose a concrete supported entry
   (`job_evidence.create_manual_completion_bundle` / CLI) that an operator invokes to create a manual
   bundle end-to-end (subject/proof/chain/patches/gates + attestation + canonical token truth) through
   `write_manual_completion_evidence`; an integration test EXECUTES it in a temp repo (not source
   inspection); packaging only validates. Zero provider calls, deterministic.

5. **Truthful Round-33 docs + operator state.** F1/F5/F6/F7 + patchset accepted; Round 32 did not close
   the atomic publication lifecycle and had producer/validator drift; Round 33 closes only these four.
   F012 `[~]`, F017 `[ ]`.

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local commits,
never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked `453aab97e0fc3b01`
through the real operator entry, VERIFIED_EQUAL, git OK, atomic publish; one READY ZIP; then stop.

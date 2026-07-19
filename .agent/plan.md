# Plan — Steps 13961-14160 — F012 Final Authority & Packaging Closure Round 32

Reviewed `remedy-review-20260719-203437-READY_FOR_REVIEW.zip` (SHA `b47226e1...b0363e`, Evidence
`2d1e749dcff40512`, prior `3316418eb96477f9`, base `095506b`, HEAD `fbbd584`). F1A/F1B and F6
(gate-totality) accepted — preserve. Remaining authority/packaging block, one commit each:

1. **Canonical token-truth regeneration + root-vs-task equality (F2).** Root `token_truth.json` must
   equal `token_truth.build_token_truth(staged)` (which aggregates provider_call/actual/cost counts and
   model identities from the per-task token_accounting/provider_evidence) or BLOCK. The manual producer
   writes the regenerated truth. A forged root (provider_call_count=1 while tasks say 0, forged model)
   no longer matches → blocked. token_authority closes unknown fields.
2. **Complete manual-completion typed cross-artifact contract (F3).** One normalized contract; typed
   linked-prior summary counts (string "0" blocks); required-when-absent; the canonical
   `manual_attestation` producer gains a real production entry (operator CLI subcommand) + doc.
3. **Shared no-clobber publication (F4).** A single Python coordinator resolves/reserves the exact final
   status-bearing path, refuses tracked/symlink/dir/FIFO/device/foreign collisions, creates exclusively,
   publishes atomically; the shell cannot bypass via `mv`.
4. **Fail-closed single Git-status snapshot (F5).** `_git_status_snapshot()` returns typed
   {status ∈ OK|FAILED|TIMED_OUT|UNAVAILABLE|MALFORMED, records, diagnostic}; only OK is clean; every
   other blocks READY and is recorded; dirty+untracked derive from ONE snapshot; malformed NUL blocks.
5. **Whole-file integration termination (F7).** Diagnose + fix the stall in
   test_review_package_full_integration.py; add order/repetition regression; leave no subprocess.
6. **Exact path/commit/hash-bound patchset identity (F6-patch).** Select only
   `evidence/current/review_commit_patches/*.patch`; expected paths derive from review_commit_chain;
   exactly one patch per commit, no extra; bind ordered (commit, path, sha) records. An unrelated source
   filename containing `commit_patch` never affects identity. Same derivation in plan/expectation/
   manifest/verifier.
7. **Truthful Round-32 docs + operator state.** F1A/F1B/F6 closed; F2/F3 were NOT closed by R31; document
   the cross-artifact authority + publication contracts. F012 `[~]`, F017 `[ ]`.

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local commits,
never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked `2d1e749dcff40512`
through the canonical producer, VERIFIED_EQUAL, git-status OK; one READY ZIP; then stop.

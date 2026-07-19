# Live Review — Steps 13961-14160 — F012 Final Authority & Packaging Closure Round 32

## Verdict (reviewer-owned)
**PENDING** — F2/F3/F4/F5/F6-patch/F7 closed this round; F1A/F1B and F6 (gate totality) preserved from
Round 31. Not externally accepted.

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-31 contract preserved.

External review of `remedy-review-20260719-203437-READY_FOR_REVIEW.zip` (SHA `b47226e1...b0363e`,
Evidence `2d1e749dcff40512`, prior `3316418eb96477f9`, base `095506b`, HEAD `fbbd584`) accepted
F1A/F1B and F6, and returned the remaining authority/packaging block.

### Closed this round
- **F2** — root token_truth regenerated from task/provider Evidence via `token_truth.build_token_truth`
  and required equal (`_token_truth_authority`); a forged root count/model or unknown field blocks.
  The manual producer writes the canonical aggregate.
- **F3** — linked-prior summary counts typed (string "0" blocks); the canonical `manual_attestation`
  producer gains a production caller `job_evidence.write_manual_completion_evidence`.
- **F4** — `safe_publish.assert_publishable` is the shared no-clobber boundary for the direct Python
  coordinator and the shell final path; tracked/symlink/dir/FIFO/device/foreign refused, bytes
  preserved; `mv -n` + post-check.
- **F5** — one typed `_git_status_snapshot()` (OK/FAILED/TIMED_OUT/UNAVAILABLE/MALFORMED); only OK is
  clean; a non-OK status blocks READY and is recorded; dirty+untracked from one snapshot.
- **F6-patch** — `commit_patchset_identity` binds ordered (commit, path, sha) from the commit chain;
  an unrelated `commit_patch`-named file never enters; missing/extra blocks.
- **F7** — the full-integration mini repo uses an intentional PYTHONPATH (not a curated partial
  packages copy) and terminates in one invocation; repetition regression added.

## Verification

- New/affected suites pass: test_review_token_truth_authority, test_review_no_clobber_publish,
  test_review_git_status_snapshot, test_review_patchset_identity, test_review_package_full_integration,
  test_review_manual_completion_shapes, test_review_authoritative_e2e, test_do_job_flow. The full
  acceptance matrix is re-run before packaging; counts recorded in verification_tests.json. The stream
  E2E also passes with the parent PYTHONPATH unset.

## Status

F012 `[~]` — not externally accepted. F017 `[ ]` not started. Branch locally committed, unpushed,
unmerged. Authority: staged Evidence bytes → real producers → regenerated final verifier + token truth
→ gates → archive plan → immutable ZIP; a supplied final-verifier/token-status JSON is never authority.

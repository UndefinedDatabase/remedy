# Live Review — Steps 6021-6080 — F006 — Worktree isolation per run

Reviewer: external final reviewer (independent; owns verdict).

## Verdict

**PASS_WITH_RISKS — ACCEPTED** (external, final).
Accepted job `7fa740042a7e4561`; ZIP
`remedy-review-20260712-000713-READY_FOR_REVIEW.zip`
sha256 `76dbd7f042ea2bda0b6c2511e8dac57440025f7a361f78ac470f0855e0374aed`;
24 content-proof files; 1558 evidence tests; 0 completion provider calls.
F006 is ready to commit, push, PR and merge. F007 starts only after the merge.
F008 read, explicitly NOT started (Tier-5 SSE; depends on the missing F146).

## Branch / Base

- Branch: `feature/f006-worktree-isolation`
- Base: `367a26b` (main after the F005 merge)

## Scope

Every run gets its own git worktree `.remedy-wt/<job-id>` on branch
`remedy/<job-id>`. The main checkout is never mutated. The hand-off is a branch
plus a deterministic, repository-relative `result.diff` (hashed and sized) — never
an automatic merge. fcntl locks prevent double claims. An interrupted run leaves a
recoverable worktree; recovery never creates a different branch, and physical
cleanup keeps the result branch.

## Task scopes (manual completion, non-overlapping)

- T001 worktree manager + tests + ignore rule (3 files).
- T002 loop integration: worktree replaces the copy-based primary run path (1).
- T003 parallel isolation / interrupted-run recovery tests + roadmap note (2).

## Verification

- F006 — 224 passed (11 files; the accepted ten still total 190).
- Affected production suites, file by file — 1001 passed.
- F001–F005 regression, file by file — 648 passed.
- compileall, `bash -n scripts/make_review_zip.sh`, `git diff --check` clean.
- Zero provider calls; temporary git repositories, fake providers and
  monkeypatching only.
- Pre-existing, unrelated doc-existence failures, identical on the untouched tree.

## Status

Accepted. Closing out: commit → push → PR → merge. Nothing else in scope.

# Plan — Steps 6021-6080 — F006 — Worktree isolation per run

## Goal
Every run executes in its own git worktree `<repo>/.remedy-wt/<job-id>` on branch
`remedy/<job-id>`. The normal checkout stays clean. The result is handed back as
branch + base commit + worktree HEAD + deterministic `result.diff` with hashes.
There is NEVER an automatic merge into main.

## Current Step
**F006 ACCEPTED externally: `PASS_WITH_RISKS — ACCEPTED`. Closing out: commit,
push, PR, merge. F007 (Runtime harness) starts only after the merge. F008 read but
NOT started (Tier-5 SSE; depends on F146, which does not exist).**

## Accepted package
- External verdict: **PASS_WITH_RISKS — ACCEPTED**.
- Manual-completion Job ID `7fa740042a7e4561`.
- ZIP `remedy-review-20260712-000713-READY_FOR_REVIEW.zip`
  sha256 `76dbd7f042ea2bda0b6c2511e8dac57440025f7a361f78ac470f0855e0374aed`.
- Hidden evidence `.data/evidence_exports/7fa740042a7e4561`.
- 24 content-proof files; 1558 evidence tests; 0 provider calls in the completion.
- Gates: package READY_FOR_REVIEW, evidence_authoritative true, bundle integrity
  PASS, alignment PASS, final_audit PASS_WITH_RISKS, final_verifier
  PASS_WITH_RISKS, final_job_review PASS, artifact_contract PASS,
  change_provenance PASS, fresh_evidence PASS, runtime_integration PASS,
  commit_execution NEEDS_HUMAN_APPROVAL. hash mismatches [], missing proofs [],
  uncovered files [].

## Delivered
- T001 `worktrees.py` — WorktreeHandle + create/snapshot/diff/remove/recover.
  Job ids are validated (no traversal, no ref injection); a worktree or branch
  belonging to another job is refused, never silently reused; creation is
  idempotent only for the SAME job in the SAME repository; `remove()` keeps the
  result branch by default; `.remedy-wt/` is ignored via `.git/info/exclude`, so
  the ignore rule itself never dirties the checkout it protects.
  fcntl locks under `<data>/projects/<project-id>/locks/<job>.lock` prevent two
  processes claiming a worktree, two jobs claiming a branch, and cleanup while
  another process owns it.
- T002 loop integration — `_create_staging` now creates a worktree for a git
  target (no full copy; the copy path remains only as the non-git fallback).
  Provider cwd is the worktree; the main checkout is never mutated. The run
  records isolation_mode, worktree branch/relative path/base commit/HEAD/lock id,
  cleanup status, and `result.diff` sha256+size. Cleanup releases the physical
  worktree while keeping the result branch.
- T003 isolation — two fake-provider jobs on one repo: distinct worktrees and
  branches, same filename written independently, per-job result diffs, no
  collision, lock collision blocks a duplicate claim, cleanup leaves
  `git worktree list --porcelain` clean, branches remain, no auto-merge.
  Interrupted run: worktree survives, `recover()` reopens the same branch, the
  diff survives, physical cleanup is safe and keeps the result branch.

## Tests
F006 — 224 passed (11 files: the ten accepted files still total 190;
`test_job_promote_consistency.py` grew from 21 to 34).
Affected production suites, file by file — job promote 74, job evidence 90,
artifact contract 27, do-job-flow 168, pingpong 33, pingpong-cli 172, integration
10, promote 70, run-log CLI 61, job task runner 191, repair attest 37, provider
mode 24, manual completion 44 (1001).
F001–F005 regression, file by file — 648 passed.
compileall / `bash -n` / `git diff --check` clean. Zero provider calls.
Pre-existing, unrelated: doc-existence failures in `tests/cli` and
`test_job_fulfillment.py`, identical on the untouched tree.

## Next
F006 committed, pushed, PR'd and merged; then F007 Runtime harness on a new branch.
F008 is NOT in scope.

## Hard Rules
No Fable; no Remedy self-build; no nested Builders/Reviewers/subagents; no
`job-flow`/`job-run`; no provider calls. Do not touch F007. No auto-merge, ever.

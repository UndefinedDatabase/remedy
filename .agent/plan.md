# Plan

## Goal
Step 8.5: Repo Applicator Rule Hardening.

## Status
COMPLETE

## What Was Done
1. [x] Narrow _REPO_PATH_RULES: removed implementation/prepare/define/summarize/summary; added changelog/guide
2. [x] Add stale repo path re-validation in run-next-task-local (warn + skip, no crash)
3. [x] Fix misleading test_boundary_violation_raises; add ineligible-type tests; add TestStaleRepoPath class
4. [x] Update decisions.md + context.md; 249 tests passing; commit + push

## Key Decisions
- Continue on feature/step8-repo-attachment (PR Continuity Rule — in-scope refinement)
- Removed 5 broad keywords (implementation, prepare, define, summarize, summary)
- Added changelog, guide as clearly documentation-oriented keywords
- Stale path check in CLI: warn stderr + skip; never fail task completion

## Branch
feature/step8-repo-attachment

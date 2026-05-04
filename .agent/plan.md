# Plan

## Goal
Step 18: Cockpit v1 — decision-oriented job status view.

## Prior step
Step 17 (+ 17.1/17.2/17.3) delivered Timeline v1 and terminal-event invariant hardening.

## Status
COMPLETE — 766 tests pass. Ready to commit and open PR.

## Steps
1. [x] Create packages/orchestration/cockpit.py with summarize_cockpit
2. [x] Add _cmd_cockpit to apps/cli/main.py + "cockpit" subparser
3. [x] Create tests/test_cockpit.py (~50 tests)
4. [x] Run tests and fix failures (1 failure: repo_generated_write default vs explicit deny)
5. [x] Run full suite (766 pass)
6. [x] Update docs/architecture.md — Cockpit v1 section
7. [x] Update .agent files
8. [ ] Commit all Step 18 changes
9. [ ] Push to feature/step18-cockpit-v1
10. [ ] Create PR for Step 18

## Branch
feature/step18-cockpit-v1

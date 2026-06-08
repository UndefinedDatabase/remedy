# Plan — Steps 925-939: remedy do v1 Truth Closure

## Goal
Make `remedy do v1` truthful enough to be the foundation for Test Failure Artifact + Repair Loop v0.

## Current Step
939 — Final handoff

## Steps
- [x] 925: Handoff setup
- [x] 926: Full next_safe_action catalog validation helper
- [x] 927: Replace group-only test with full validation
- [x] 928: Context failure stops run (not skipped)
- [x] 929: Command catalog metadata truth (do.run flags)
- [x] 930: Consolidate contract truth with RunContract
- [x] 931: Enforce max_loops honestly
- [x] 932: Autonomy level truth (requested vs effective)
- [x] 933: Approval gate regression tests
- [x] 934: Runtime CLI contract tests
- [x] 935: Docs update
- [x] 936-937: Review + targeted tests (81 targeted, 4751 full suite)
- [x] 938-939: Final handoff

## Pre-existing Issue
`test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.

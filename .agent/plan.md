# Plan — F146 Project Identity & Repo Autodetection (REPAIR R3)

## Goal
Fix 4 exact blocking findings from R2 external review.

## Status: COMPLETE

## T001 — Additive Registry compatibility and truthful read-only commands
- [x] Auto-derive slug in save_project() when slug is None
- [x] Existing 5 registry tests pass without modification
- [x] Add additive assertions: stored JSON contains non-null valid slug
- [x] Add byte/mtime proof: save_project(slug=None) writes disk
- [x] Fix read_only action-class truth: project list/show use readonly functions
- [x] Add test: project list does not write (mtime guard)

## T002 — Review-feature propagation and exact F146 Runtime Evidence
- [x] Add feature_id param to build_manual_completion_gates
- [x] Add feature_id param to create_manual_completion_bundle
- [x] Add E2E test: feature_id="f146" excludes F018 checks
- [x] Verify refresh_review_evidence.py (global gate, acceptable)

## T003 — Complete regression matrix, final tracked state, canonical ZIP
- [x] Run full test matrix (189 tests passed)
- [x] Update docs/roadmap/features/T0_F146.md Built State for R3
- [x] Update agent state files
- [ ] Commit in 5 logical commits
- [ ] Generate fresh Evidence
- [ ] Run scripts/make_review_zip.sh once
- [ ] Produce mandatory handoff

# Plan — F017 Scope Fences — T001

## Goal
Implement the pure FenceSpec + path checker with exhaustive tests (T001 block).
Do not touch the applicator (T002) or add CLI/config keys (T003).

## Current Step
T001 implementation complete. Committing.

## Done
- [x] Read T0_F017.md spec
- [x] Inspect applicator choke point (patch_apply, source_apply, repo_applicator)
- [x] Implement `packages/orchestration/scope_fences.py`
- [x] Implement `tests/orchestration/test_fences.py` — 78 tests pass
- [x] Update T0_F017.md with built state and T002 choke point
- [x] Update STATUS.md to `[~]` for F017
- [ ] Commit: FenceSpec + pure checker
- [ ] Commit: tests + docs/state

## Constraints
- Do not push, create PR, or merge
- Do not touch applicator beyond documenting T002 choke point
- Do not modify worktree creation, git internals, STATUS semantics, Flight Plan schema

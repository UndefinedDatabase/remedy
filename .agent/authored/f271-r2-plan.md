# Plan — F271 No more legacy: ownership, reachability, replace-is-delete

Branch: feature/f271-no-more-legacy, cut from `main` at `a4f79a94` (the
merge commit of pull request 258, F270's closure).

## Goal

Every command group names its owning feature and its reach, a test
refuses an unreached module, the closure protocol demands deletion on
replacement, and `remedy doctor core` lists dead commands
(`docs/roadmap/features/T2_F271.md`).

## Current Step

Round 2 books round 1's verdict, resolves R-0893 by naming its
production importer, registers R-0980 to R-0982, lands DECISION F271
D2, deletes three unreached modules with their tests, and adds
`tests/test_no_orphan_modules.py` with its `ALLOWED_UNWIRED` list,
registered in `ARCHITECTURE_FILES` and the `budgets` CI stage.

## Next Steps

1. T002: closure precondition 7 citing the AGENTS.md rule, and a
   `doctor core` test that plants a dead command and sees it listed.
2. R-0982: `patch_revert.py` deleted with the tests that exist only for
   it, each reader of `patch_intent_reverted` ruled on.
3. Closure sequence.

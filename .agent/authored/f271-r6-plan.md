# Plan — F271 No more legacy: ownership, reachability, replace-is-delete

Branch: feature/f271-no-more-legacy, cut from `main` at `a4f79a94` (the
merge commit of pull request 258, F270's closure).

## Goal

Every command group names its owning feature and its reach, a test
refuses an unreached module, the closure protocol demands deletion on
replacement, and `remedy doctor core` lists dead commands
(`docs/roadmap/features/T2_F271.md`).

## Current Step

Closed at round 6: STATUS `[x]` at PASS, README 85 of 281, SU-022
consumed by F271, the ledger rotated, and the pull request into `main`
opened and left unmerged.

## Next Steps

1. The Open PR Gate merges F271's pull request once its hosted CI
   passes; the next feature is then claimed under Rule A5, and its
   first commit books round 6's verdict.

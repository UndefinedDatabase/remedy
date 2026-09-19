# Plan — F271 No more legacy: ownership, reachability, replace-is-delete

Branch: feature/f271-no-more-legacy, cut from `main` at `a4f79a94` (the
merge commit of pull request 258, F270's closure).

## Goal

Every command group names its owning feature and its reach, a test
refuses an unreached module, the closure protocol demands deletion on
replacement, and `remedy doctor core` lists dead commands
(`docs/roadmap/features/T2_F271.md`).

## Current Step

Round 5 is closure round A: it books round 4's verdict, runs the
self-use item to its approval gate (closure precondition 6), records
the integrity check (precondition 3), and builds the evidence job and
the review zip (algorithm steps 1 and 2).

## Next Steps

1. Closure round B: ledger rotation, the closure commit (STATUS `[x]`,
   README, the self-use item consumed), and the pull request into
   `main`, never merged by this session.

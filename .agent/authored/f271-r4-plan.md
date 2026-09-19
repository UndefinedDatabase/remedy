# Plan — F271 No more legacy: ownership, reachability, replace-is-delete

Branch: feature/f271-no-more-legacy, cut from `main` at `a4f79a94` (the
merge commit of pull request 258, F270's closure).

## Goal

Every command group names its owning feature and its reach, a test
refuses an unreached module, the closure protocol demands deletion on
replacement, and `remedy doctor core` lists dead commands
(`docs/roadmap/features/T2_F271.md`).

## Current Step

Round 4 is the integration gate: it books round 3's verdict, gives
T2_F273.md the Acceptance lines for R-0980 and R-0981 that round 2's
`Owner: F273` owed (amend0911-feedback rule A), appends the Built State
section to T2_F271.md, and runs the full suite once (operator
amendment amend0917-throughput), committing its transcript.

## Next Steps

1. A red closure suite is repaired under amend0917-throughput (2),
   strictly shrinking the bad set, at most three rounds.
2. Closure sequence: evidence job, review zip, self-use item, ledger
   rotation, STATUS line, pull request.

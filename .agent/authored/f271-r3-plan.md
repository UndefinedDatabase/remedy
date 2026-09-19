# Plan — F271 No more legacy: ownership, reachability, replace-is-delete

Branch: feature/f271-no-more-legacy, cut from `main` at `a4f79a94` (the
merge commit of pull request 258, F270's closure).

## Goal

Every command group names its owning feature and its reach, a test
refuses an unreached module, the closure protocol demands deletion on
replacement, and `remedy doctor core` lists dead commands
(`docs/roadmap/features/T2_F271.md`).

## Current Step

Round 3 books round 2's verdict and lands DECISION F271 D3. It
resolves R-0982 by deleting `patch_revert.py` with the tests that
exist only for it, lands T002's planted-dead-command tests for
`doctor core`, and appends closure precondition 7 citing the AGENTS.md
rule "Replacing is deleting".

## Next Steps

1. Integration-gate round: the Built State section of T2_F271.md, and
   the full suite run once (amend0917-throughput).
2. Closure sequence: evidence job, review zip, self-use item, ledger
   rotation, STATUS line, pull request.

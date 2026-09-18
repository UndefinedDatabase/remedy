# Plan — F271 No more legacy: ownership, reachability, replace-is-delete

Branch: feature/f271-no-more-legacy, cut from `main` at `a4f79a94` (the
merge commit of pull request 258, F270's closure).

## Goal

Every command group names its owning feature and its reach, a test
refuses an unreached module, the closure protocol demands deletion on
replacement, and `remedy doctor core` lists dead commands
(`docs/roadmap/features/T2_F271.md`).

## Current Step

Round 1 claims F271, books F270 round 8's verdict and R-0979's
resolution, lands DECISION F271 D1, builds T001 (`feature` and `reach`
on every `GroupDef`, refused by a catalog test) and deletes
`builder_eval.py` with its test and script under DECISION
amend0911-feedback D6.

## Next Steps

1. The orphan-module test `tests/test_no_orphan_modules.py` and the
   modules it names resolved: wired, deleted, or allowed with a reason.
2. T002: closure precondition 7 citing the AGENTS.md rule, and a
   `doctor core` test that plants a dead command and sees it listed.
3. R-0893: `agent_run_trace.py` deleted with its tests, its allowlist
   line and the catalog keys only it sources, or its importer named.
4. Closure sequence.

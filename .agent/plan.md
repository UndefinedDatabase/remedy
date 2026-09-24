# Plan — F015 Interactive plan editing

Branch: feature/f015-interactive-plan-editing, cut from `main` at
`fce49ce0`, the merge commit of pull request 273 (F267 List commands v2
completion).

## Goal

The human reshapes a job's task plan before approving it: six edit
commands, valid only while the plan's approval is open, each revalidated
and logged, reachable through the write channel and `remedy job plan-*`,
and execution follows the edited plan exactly, proven by hash
(`docs/roadmap/features/T5_F015.md`). Open findings: 4, all owned by F284.

## Current Step

ROUND 7: book round 6's FAIL, whose cause was the reviewer's leftover
research worktrees, and finish the first repair round of DECISION F015
D5 — its tests, its red proofs and the full suite again over the two
repairs round 6 landed.

## Next Steps

1. The closure sequence's evidence half: the evidence job built against
   the fork point, and the fresh review package.
2. The closing round: book the evidence round, rotate the ledger, flip
   F015's STATUS line with its README pins, and open the pull request.

## Risks

- A bad node the re-run still lists takes another repair round, at most
  two more, under operator amendment amend0917-throughput rule 2.

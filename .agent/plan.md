# Plan — F019 Live node materialization

Branch: feature/f019-live-node-materialization, cut from `main` at
`92b7f5f1`, the merge commit of pull request 274 (F015 Interactive plan
editing).

## Goal

The brain graph comes alive: the stream's frames materialize nodes and
links as a job runs, through a pure reducer whose goldens are the contract,
rendered on the committed stage-1 stack, and recovered from gaps through
the snapshot path without ghosts (`docs/roadmap/features/T5_F019.md`).

## Current Step

ROUND 8, THE CLOSURE SEQUENCE'S EVIDENCE HALF: book round 7's PASS, whose
one full suite is green, then build the evidence bundle against the fork
point and the fresh review package. T001, T002 and T003 are built.

## Next Steps

1. The closing round: the booking of round 8, the ledger rotation, the
   STATUS line with the README counters in the same commit, and the pull
   request.

## Risks

The stream carries no run id and no outcome for test and repair runs, so
those draw no node yet (DECISION F019 D1, operator note Q2). Prompt dots
show only in the simple view (DECISION F019 D3, operator note Q3). Open
findings: 4, all owned by F284.

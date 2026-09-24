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

ROUND 9, THE CLOSING ROUND: book round 8's PASS, rotate the ledger, accept
F019 in STATUS with its README pins, and open the pull request. T001, T002
and T003 are built; the package is READY_FOR_REVIEW.

## Next Steps

1. The next session's Open PR Gate merges this feature's pull request.
2. Rule A5 then claims the first unchecked feature in
   `docs/roadmap/STATUS.md`.

## Risks

The stream carries no run id and no outcome for test and repair runs, so
those draw no node yet (DECISION F019 D1, operator note Q2). Prompt dots
show only in the simple view (DECISION F019 D3, operator note Q3). Open
findings: 4, all owned by F284.

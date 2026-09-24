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

ROUND 5: book round 4's PASS, record DECISION F019 D5, and land T003's
first half: the stage folds the complete prefix of a ledger merged from
`events-since` pages and the live stream's ring, and fills a hole by paging
from its first missing seq. T001 and T002 are built.

## Next Steps

1. The rest of T003 (DECISION F019 D5 (1)): the end-to-end run of a live
   fake job compared against the demo recording, and the performance
   fixture's measurement against the stage-1 budget.
2. The closure sequence.

## Risks

The stream carries no run id and no outcome for test and repair runs, so
those draw no node yet (DECISION F019 D1, operator note Q2). Prompt dots
show only in the simple view (DECISION F019 D3, operator note Q3). The
performance budget is measured in a browser, which the next round must
reach. Open findings: 4, all owned by F284.

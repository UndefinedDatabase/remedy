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

ROUND 4: book round 3's PASS, record DECISION F019 D4, and finish T002:
remove the old decorative dashboard builder with its source pins, and
commit the demo recording, a captured fake-provider job, with its
hand-derived golden. T001 and T002 are then built.

## Next Steps

1. T003: the live wiring from the stream hook through the reducer to the
   renderer, gap and snapshot recovery by paging `events-since`, the
   performance fixture and the end-to-end run on a live fake job compared
   against the demo recording.
2. The closure sequence.

## Risks

The stream carries no run id and no outcome for test and repair runs, so
those draw no node yet (DECISION F019 D1, operator note Q2). Prompt dots
show only in the simple view (DECISION F019 D3, operator note Q3). Open
findings: 4, all owned by F284.

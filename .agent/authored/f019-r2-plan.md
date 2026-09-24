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

ROUND 2: book round 1's PASS, record DECISION F019 D2, and land T002's pure
half — `buildBrainLayout` in `buildForceBrainModel.ts`, the birth schedule
in `brainMotion.ts`, the two birth-motion tokens and their guard. T001 is
built.

## Next Steps

1. T002's painted half: the renderer that paints the layout, its mount in
   `BrainGraphStage.tsx` fed by the reducer's model seeded from the
   dashboard, the replacement of the dashboard builder it supersedes, and
   the demo recording (DECISION F019 D2).
2. T003: the live wiring from the stream hook through the reducer to the
   renderer, gap and snapshot recovery by paging `events-since`, the
   performance fixture and the end-to-end run on a live fake job.
3. The closure sequence.

## Risks

The stream carries no run id and no outcome for test and repair runs, so
those draw no node yet (DECISION F019 D1, operator note Q2). Open
findings: 4, all owned by F284.

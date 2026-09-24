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

ROUND 1: claim F019, re-head the live review record with F015's round 10
verdict and R-1047's resolution, record DECISION F019 D1 and the operator
note it implies, and land T001 — `brainOntology.ts` and `brainReducer.ts`
under `apps/ui/src/components/graph/`, with the fixture streams, the
goldens, idempotence per seq, the snapshot rebuild and the cluster view.

## Next Steps

1. T002: render the reducer's model on react-force-graph-2d, extending
   `buildForceBrainModel.ts` to read it — layout, glyph slots for the
   lifecycle feature, the motion tokens, and the demo recording.
2. T003: the live wiring from the stream hook through the reducer to the
   renderer, gap and snapshot recovery by paging `events-since`, the
   performance fixture and the end-to-end run on a live fake job.
3. The closure sequence.

## Risks

The stream carries no run id and no outcome for test and repair runs, so
those draw no node yet (DECISION F019 D1, operator note Q2). Open
findings after this round: 4, all owned by F284.

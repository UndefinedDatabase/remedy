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

ROUND 6: book round 5's PASS, record DECISION F019 D6, and finish T003: a
live fake job checked against the demo recording in the suite, the
committed performance fixture at exactly 200 and 500 nodes, and the
stage-1 frame budget measured on it in headless Chrome. T001, T002 and
T003 are then built.

## Next Steps

1. The closure sequence (`docs/roadmap/STATUS_closure_protocol.md`): the
   verdict booking, the ledger rotation, the one full-suite run, the
   evidence package and review zip, the STATUS flip and the pull request.

## Risks

The stream carries no run id and no outcome for test and repair runs, so
those draw no node yet (DECISION F019 D1, operator note Q2). Prompt dots
show only in the simple view (DECISION F019 D3, operator note Q3). The
frame reading shows no dropped frame at 60 Hz, not the headroom beyond it
(DECISION F019 D6). Open findings: 4, all owned by F284.

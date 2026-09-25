# Plan — F025 Pause/resume (global & per node)

Branch: feature/f025-pause-resume, cut from `main` at `49624d5c`, the
merge commit of pull request 279 (F024 Phase timeline with scrubber).

## Goal

Calm control over a running job: a job pause halts the whole run and a
task pause halts one branch, each taking effect before the next provider
call while running calls finish, and the relaunch resumes exactly where
things stood, with no process left waiting
(`docs/roadmap/features/T5_F025.md`).

## Current Step

ROUND 9, the closure sequence's first half: book round 8, write the
Built State, consolidate the checklist, generate and run the closure's
self-use item, and run this feature's one full suite.

## Next Steps

1. The closure's second half: book round 9, register what the self-use
   run and the suite ask for, the evidence bundle and the review package.
2. The closing round: the ledger rotation, the STATUS flip with its
   README pins, and the pull request.

## Risks

A pause must never strand a job it cannot resume. Open findings: 2 —
R-1008 and R-1055, both owned by F285.

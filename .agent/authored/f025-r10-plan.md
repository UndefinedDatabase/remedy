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

ROUND 10, the closure sequence's evidence half: book round 9, register
R-1057 and R-1058 for F285, build the evidence bundle against the fork
point and the fresh review package.

## Next Steps

1. The closing round: the ledger rotation, the STATUS flip with its
   README pins and the self-use item's `consumed_by`, and the pull
   request.

## Risks

A pause must never strand a job it cannot resume. Open findings: 4 —
R-1008, R-1055, R-1057 and R-1058, all owned by F285.

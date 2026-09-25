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

ROUND 11, the closing round: book round 10, rotate the ledger, accept
F025 in STATUS with its README pins and the self-use item's
`consumed_by`, and open the pull request.

## Next Steps

1. The next feature's session merges this pull request at the Open PR
   Gate, then claims the first unchecked feature in STATUS.

## Risks

Open findings: 4 — R-1008, R-1055, R-1057 and R-1058, all owned by F285.

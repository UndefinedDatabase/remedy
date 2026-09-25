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

ROUND 8, the repair of R-1056 (DECISION F025 D6): a park records the
episode it ends under the new manifest status `paused`, so a relaunched
job writes its run manifest; the end-to-end test then compares the
manifest's error too.

## Next Steps

1. The closure sequence.

## Risks

A pause must never strand a job it cannot resume. Open findings: 3 —
R-1008 and R-1055, owned by F285, and R-1056, owned by F025 and
repaired this round.

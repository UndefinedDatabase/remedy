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

ROUND 6, T003's second part (DECISION F025 D4): the pause request
module that reads the door's answer, the pure pause view, the pause
banner in the graph's chrome, the NowCard's "Paused by you", and the
pause and resume buttons for the job and for a task.

## Next Steps

1. T003's end-to-end: pause mid-build, resume, and a final state equal
   to an unpaused control run's, with the session evidence.
2. The closure sequence.

## Risks

A pause must never strand a job it cannot resume. Open findings: 1 —
R-1008, owned by F285.

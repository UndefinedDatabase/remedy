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

ROUND 5, T003's first part: repair R-1051 and R-1052, then the pause on
the page — the dashboard's `pause` object and the graph's `paused` node
state with its treatment, mark, reducer cases and seed (DECISION F025
D3).

## Next Steps

1. T003's second part: the door client, the stage banner, the NowCard's
   "Paused by you" line, and the pause and resume buttons for the job
   and for a task.
2. T003's end-to-end: pause mid-build, resume, and a final state equal
   to an unpaused control run's, with the session evidence.
3. The closure sequence.

## Risks

A pause must never strand a job it cannot resume. Open findings: 3 —
R-1008, owned by F285, and R-1051 and R-1052, owned by F025 and
repaired this round.

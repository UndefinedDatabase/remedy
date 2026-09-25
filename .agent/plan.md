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

ROUND 4, T002: `job.pause` and `job.unpause` in the catalog, the CLI
verbs and the write door, each with an optional task, the task pause
events, the door's audit and import guard, and live fake-job tests of
both scopes through the real door (DECISION F025 D2, operator question
Q4).

## Next Steps

1. T003: the paused states, the banner, the NowCard line and the
   browser's pause and resume, with the end-to-end against an unpaused
   control run.
2. The closure sequence.

## Risks

A pause must never strand a job it cannot resume; the park writes the
state before it archives the request. Open findings: 1 — R-1008, owned
by F285.

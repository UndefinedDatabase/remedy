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

ROUND 1: claim F025, re-head the live review record, book F024's round
9 and R-1048's resolution, record DECISION F025 D1, and land the first
half of T001 — `packages/orchestration/pause_control.py`, the job and
task pause control files and the mask arithmetic, with unit tests.

## Next Steps

1. T001's second half: the pause at the linear runner's and the cycle
   executor's safe points and ready sets — park, relaunch, stop beats
   pause, the deadline counting through a pause.
2. T002: the channel commands with their audit, the CLI verbs, and live
   fake-job tests of both scopes.
3. T003: the paused states, the banner, the NowCard line, and the
   end-to-end against an unpaused control run.
4. The closure sequence.

## Risks

A pause must never strand a job it cannot resume; the park writes the
state before it archives the request. Open findings: 1 — R-1008, owned
by F285.

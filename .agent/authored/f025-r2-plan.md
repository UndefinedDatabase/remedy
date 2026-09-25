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

ROUND 2: the pause in the linear runner, `run_job` — the job pause and
the task mask read at its safe points after every stop, the park that
persists `paused` with a pause record before it archives the request,
the relaunch that lifts it, a stop beating a pause, and the deadline
counting through one, each row of DECISION F025 D1's table tested.

## Next Steps

1. The same pause in the cycle executor, `run_cycles`: the mask as a
   third withheld seed, the job pause as a terminal, and the evidence.
2. T002: the channel commands with their audit, the CLI verbs, and live
   fake-job tests of both scopes.
3. T003: the paused states, the banner, the NowCard line, and the
   end-to-end against an unpaused control run.
4. The closure sequence.

## Risks

A pause must never strand a job it cannot resume; the park writes the
state before it archives the request. Open findings: 1 — R-1008, owned
by F285.

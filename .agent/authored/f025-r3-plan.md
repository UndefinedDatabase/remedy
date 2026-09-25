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

ROUND 3: repair round 2's two findings — R-1049, the blind handler that
reddens the BLE001 ratchet, and R-1050, the pause events that fail
without a trace — then bring the same pause to the cycle executor,
`run_cycles`: the job pause at its safe points and before each task
pick, the task mask as a third withheld seed with its evidence, the
park and the lift through the linear runner's own record and events.

## Next Steps

1. T002: the channel commands with their audit, the CLI verbs, and live
   fake-job tests of both scopes.
2. T003: the paused states, the banner, the NowCard line, and the
   end-to-end against an unpaused control run.
3. The closure sequence.

## Risks

A pause must never strand a job it cannot resume; the park writes the
state before it archives the request. Open findings: 3 — R-1008, owned
by F285, and R-1049 and R-1050, owned by F025 and repaired this round.

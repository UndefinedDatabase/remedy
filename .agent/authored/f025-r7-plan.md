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

ROUND 7: repair R-1053 and R-1054 in the task popover's control, then
T003's end-to-end (DECISION F025 D5): both scopes paused through the
door on a live job, relaunched through `remedy job run`, and compared
with an unpaused control run; R-1055 goes to F285.

## Next Steps

1. The closure sequence.

## Risks

A pause must never strand a job it cannot resume. Open findings: 4 —
R-1008 and R-1055, owned by F285, and R-1053 and R-1054, owned by F025
and repaired this round.

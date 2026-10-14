# Plan — F308 The run manifest survives a task split

## Goal
A task the run splits leaves the job's run manifest written and valid, with the split recorded as
Remedy's own change, while an edit of the task list from outside is still refused
(docs/roadmap/features/T2_F308.md; DECISIONs F308 D1 and D2).

## Current Step
Session 1, round 2 on `feature/f308-run-manifest-task-split`: round 1 booked; DECISION F308 D2
writes the split record's shape; T001 and T002 land in `packages/orchestration/run_task_list.py`
and in line-neutral edits of `packages/orchestration/run_manifest.py`, and T003's tests prove them.

## Next Steps
1. The record of the built state: a section on the split in `docs/roadmap/features/T0_F012.md`,
   and the Built State of `docs/roadmap/features/T2_F308.md`.
2. The closure sequence: the one full suite, the self-use run, the evidence and the pull request.

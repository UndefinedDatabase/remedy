# Plan — F308 The run manifest survives a task split

## Goal
A task the run splits leaves the job's run manifest written and valid, with the split recorded as
Remedy's own change, while an edit of the task list from outside is still refused
(docs/roadmap/features/T2_F308.md; DECISIONs F308 D1 and D2).

## Current Step
Session 1, round 3 on `feature/f308-run-manifest-task-split`: round 2 booked with R-1314 and
R-1315 registered; both repaired in `packages/orchestration/run_task_list.py` with their tests;
the run manifest's design document gains its section on the split.

## Next Steps
1. The closure sequence: the one full suite, the self-use run, the evidence, the Built State,
   the resolutions of R-1252, R-1314 and R-1315, and the pull request.

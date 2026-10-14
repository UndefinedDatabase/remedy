# Plan — F308 The run manifest survives a task split

## Goal
A task the run splits leaves the job's run manifest written and valid, with the split recorded as
Remedy's own change, while an edit of the task list from outside is still refused
(docs/roadmap/features/T2_F308.md; DECISION F308 D1).

## Current Step
Session 1, round 1 on `feature/f308-run-manifest-task-split`: claim F308, book F306's round 12,
and take the three structural steps into `packages/orchestration/run_task_list.py` that DECISION
F308 D1 orders, each changing no behaviour.

## Next Steps
1. DECISION F308 D2 writes the split record's shape; T001 (the split record), T002 (the F7 check,
   the task statuses, the decoder and the check across episodes) and T003 (the proof through the
   real split path) land with their red-proofs.
2. The closure sequence: the one full suite, the self-use run, the evidence and the pull request.

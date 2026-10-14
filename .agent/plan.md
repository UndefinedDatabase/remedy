# Plan — F308 The run manifest survives a task split

## Goal
A task the run splits leaves the job's run manifest written and valid, with the split recorded as
Remedy's own change, while an edit of the task list from outside is still refused
(docs/roadmap/features/T2_F308.md; DECISIONs F308 D1 and D2).

## Current Step
Session 1, round 6 on `feature/f308-run-manifest-task-split`, the closing round: round 5 booked,
R-1252, R-1314 and R-1315 resolved, the Built State written; then the ledger rotation, F308's
STATUS line with the README sync and SU-063's `consumed_by`, and the pull request, left unmerged.

## Next Steps
1. The next session: the Open PR Gate merges F308's pull request, books round 6's verdict in the
   next feature's first commit, and Rule A5 picks the next unchecked STATUS line.

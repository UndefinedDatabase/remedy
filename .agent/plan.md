# Plan — amend1016s (operator order remedy-lab-prep, a stop of a job that never started)

## Goal
`remedy job stop` and the supervisor's forwarded `job.stop` end a job that never started
(`planned`, no first run time, no episode) at once as a first-class stop, and finalize a request
left pending on such a job. A started job keeps the request path. Branch
feature/stop-unstarted-job. Finding R-1333, DECISION amend1016s D1.

## Current Step
Done: `packages/orchestration/job_stop_now.py`, both callers, the `remedy do` walk's guard, the
docs paragraph in serve-daemon-v1.md, the tests, R-1333 and the decision.

## Next Steps
- None in this branch. The next operator order of the session removes the tracked `.data/`
  files on its own branch.

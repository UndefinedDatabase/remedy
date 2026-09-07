# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 15 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 and T002 are
COMPLETE: the run re-key, the eight administrative fields, the widened
`RunState`, the `state` rename and retype, the cockpit's two settled states, and
the Mission record's order and contract.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the classic
runner, T005 the reachability test and the cluster deletion.

## Current Step

T003's first consumer, and a defect found while re-grepping the consumer list:
`apps/cli/commands/job_stop_cmd.py` still reads `job.status`, a field the round 9
rename moved to `state`, on the branch that emits the completed-job error JSON.
Registered as R-0822, fixed and guarded in the same round with the JSON sibling
test the file never had.

## Next Steps

1. The rest of T003's consumers, re-grepped rather than taken from F260's
   2026-09-05 list: `teach_cmd.py`, `ui_server.py`, `job_context_cmd.py` and the
   `_JobPlanTaskAdapter` shim, each with a test on a ping-pong-created job.
2. T004, the classic runner and the resolver collapse, which is where
   `_CoreJobAdapter` dies with the classic store it exists to adapt.
3. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- The five tests.md ids named in this feature's Acceptance (R-0803, R-0804,
  R-0807, R-0810, R-0812) were routed to F273 by the 2026-09-06 triage. Whether
  F272's Acceptance still requires them is UNSETTLED and must be ruled before
  closure, or the feature cannot be closed self-consistently.

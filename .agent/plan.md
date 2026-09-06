# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1, 3, 4, 5, 6 and 7 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE, and
T002's eight pure-addition administrative fields landed in round 7.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

The `state` collapse, move one. `JobPlan` spells the lifecycle field `status:
str` while the classic `Job` already spells it `state: RunState`, and the two
vocabularies differ in both directions: `blocked` and `stopped` have no `RunState`
member. This round widens `RunState` with those two, pins the coverage with a
test that is red at its own base, and rules the whole collapse as DECISION F272
D5 so the next round can execute it in one atomic move. It also records DECISION
F272 D4, which rules that `job_id` stays the one required key of a job record.

## Next Steps

1. The collapse itself: replace `JobPlan.status: str` with `state: RunState`
   across every call site in ONE commit, exporting `job.state.value` into the
   unchanged `"status"` JSON key so records already on disk load unchanged.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each with a test that proves it works on a job created
   through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- Widening an enum is safe only while nothing enumerates it; that was measured
  at `b5cde726` and must be re-measured before any further member is added.
- The collapse cannot be staged by caller: an intermediate commit would leave
  both spellings alive and the suite red, so it is one commit or none.

# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 10 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE;
T002 has landed the eight administrative fields, widened `RunState`, and renamed
`JobPlan.status` to `state` at the 234 measured sites of DECISION F272 D7.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Repair R-0821, the two cockpit modules round 8's `RunState` widening never
reached. `blocked` and `stopped` are in no partition of `digestVisibility.ts`
and have no key in `digestCardCopy.ts`, so the hero card calls both "State not
recorded" and two `tests/ui_contracts/` tests have been red on this branch since
round 8. This round gives them their place and rules it as DECISION F272 D8.

## Next Steps

1. Move three of the `state` collapse: retype `JobPlan.state` to `RunState` and
   make the six `JOB_*` constants `RunState` members, with `.value` at every
   boundary leaving the record. The rendering guard round 10 shipped in
   `tests/orchestration/test_job_state_field.py` is what that move must keep
   green, and D7's probe is the method for finding its site set.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A `RunState` member added without a matching cockpit entry is invisible to
  every gate this feature has run so far; `tests/ui_contracts/` is the suite
  that sees it and it belongs in the gate list of any round touching the enum.

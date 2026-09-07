# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 11 PASSED;
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

Land R-0821's fix. Round 11 ruled the placement as DECISION F272 D8 and then
measured that a third guard, an arity pin in
`tests/ui_contracts/test_digest_hero_card.py`, reddens the moment the label map
widens; DECISION F272 D9 rules that guard a FLOOR, as its two siblings already
are. This round frees the guard, then gives `blocked` and `stopped` their place
in `digestVisibility.ts` and `digestCardCopy.ts`.

## Next Steps

1. Move three of the `state` collapse: retype `JobPlan.state` to `RunState` and
   make the six `JOB_*` constants `RunState` members, with `.value` at every
   boundary leaving the record. The rendering guard round 10 shipped in
   `tests/orchestration/test_job_state_field.py` is what that move must keep
   green, D7's probe is the method for finding its site set, and R-0821's clause
   puts `tests/ui_contracts/` in that round's gate list.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A vacuity guard written as an equality pins an arity nobody meant to pin, and
  goes stale exactly when a vocabulary grows. Two more sit in this suite over
  zoom levels; both are genuine fixed arities and neither is F272's business.

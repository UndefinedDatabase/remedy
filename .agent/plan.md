# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 9 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE;
T002 has landed the eight administrative fields and widened `RunState` to cover
every value the job lifecycle field can hold.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

The `state` collapse, move two of the three DECISION F272 D6 stages. Round 9
proved the site set cannot be derived from receiver names, so this round
measures it by running the suites against a raising `status` property and
renames exactly what that probe reports, plus the two structural stand-ins. The
measurement lands as an inventory beside the rename, and a new test pins the
field, the unchanged stored key, the old-record path and the rendering.

## Next Steps

1. Move three: retype `JobPlan.state` to `RunState` and make the six `JOB_*`
   constants `RunState` members, with `.value` at every boundary leaving the
   record. `RunState`'s `str()` is `'RunState.X'` while its f-string is the
   value, so move two's rendering guard is what that move must keep green.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- The rename cannot be staged by caller: an intermediate commit leaves both
  names live and the suite red, so it is one commit or none.
- `.status` is polymorphic here; a site is renamed only on evidence, never
  because its receiver reads like a job.

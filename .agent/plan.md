# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 14 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE.
T002 has landed the eight administrative fields, widened `RunState`, renamed
`JobPlan.status` to `state`, retyped that field onto `RunState`, given `blocked`
and `stopped` their place in the cockpit, and now completes the Mission record.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the classic
runner, T005 the reachability test and the cluster deletion.

## Current Step

The Mission extension, T002's last item: `Mission.order` and `Mission.contract`,
the two fields of DECISION F260 D1 that had no counterpart on the record. Both
are ADDITIVE and OPTIONAL on the terms `mission_plan` already set, so
`MISSION_SCHEMA_VERSION` does not move and every mission record already written
stays byte-identical. The contract lands RESERVED and empty for F269, per
DECISION amend0905-vocab D9, which DECISION F272 D11 resolves the feature files'
"D9 shape" reference to.

## Next Steps

1. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
2. T004, the classic runner and the resolver collapse.
3. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- T002 completes here, so the next round opens T003, whose eleven consumers are
  measured in F260's file by line citation rather than listed here. Read that
  list from `T2_F260.md` before scoping, never from memory: DECISION F272 D7
  records what a site set inferred rather than measured cost this branch.

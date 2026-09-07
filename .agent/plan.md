# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 12 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE;
T002 has landed the eight administrative fields, widened `RunState`, renamed
`JobPlan.status` to `state` at the 234 measured sites of DECISION F272 D7, and
given `blocked` and `stopped` their place in the cockpit.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Readiness for move three. The measurements that round need — what a str-Enum
retype does and does not change, the counted rendering hazard, the three record
boundaries, the six constants and their blast radius — land as
`.agent/f272_retype_readiness.md`, and R-0821 is resolved. The retype itself is
the next session's first round, authored from that file.

## Next Steps

1. Move three: retype `JobPlan.state` to `RunState`, make the six `JOB_*`
   constants `RunState` members keeping their names and values, and put `.value`
   at the two record boundaries `.agent/f272_retype_readiness.md` names. Gate it
   on that file's readings, on round 10's rendering guard, and on
   `tests/ui_contracts/` per R-0821's clause.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A str-Enum changes `str()` and `%s` and nothing else; both are counted in the
  readiness file, and the count is what makes move three a bounded change rather
  than the open-ended one D5 assumed.

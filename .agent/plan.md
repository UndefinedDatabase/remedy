# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 13 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE;
T002 has landed the eight administrative fields, widened `RunState`, renamed
`JobPlan.status` to `state`, given `blocked` and `stopped` their place in the
cockpit, and now retypes the field itself.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the classic
runner, T005 the reachability test and the cluster deletion.

## Current Step

Move three of DECISION F272 D6: `JobPlan.state` is retyped to `RunState`, the six
`JOB_*` constants become `RunState` members keeping their names and values, and
`__post_init__` coerces every construction path so one type describes the field.
Two record boundaries emit the plain value, and the two `str(getattr(job,
"state", …))` sites that would otherwise silently stop checking are fixed.

## Next Steps

1. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
2. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
3. T004, the classic runner and the resolver collapse.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- A str-Enum changes `str()` and `%s` and nothing else, but the SITE SET of those
  renderings is wider than a bare-attribute predicate sees: `getattr(job,
  "state", …)` hid two, one an integrity check that passed by not looking.

# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 25 PASSED except round 2
(premise corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round
22). T001, T002 and T003 are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Record that T004's remaining work is ONE ATOMIC record flip and not the
per-caller sequence DECISION F272 D14 assumed. `Job` and `JobPlan` now differ in
only `id` and `name`; `.id` sits on helpers with six and seven callers each, so
moving one consumer closes over the whole graph, and a helper taking both records
is the compatibility reader AGENTS.md forbids. DECISION F272 D15 carries it.

## Next Steps

1. SESSION 12 REACHES THE SOFT LIMIT of 12 sessions. Its first obligation is the
   SCOPE REPORT, then the amend0905-throughput split-and-close default executed
   on the session's own authority — register the remainder as a new feature
   placed directly after F272 per amend0906-split-placement, and close F272 at a
   self-consistent scope through the normal closure sequence.
2. The figures that report needs are already measured: 60 production and 127 test
   files migrate, twelve cluster-bound consumers never do, and the `.id` flip has
   an upper bound of 468 production and 1545 test reads. See
   `.agent/f272_t004_staging.md` and DECISIONs F272 D14 and D15.
3. `job.run-next`, `job.run` and F114's cost-preview carrier all sit BEHIND that
   flip and are named in D13, D14 and this plan's predecessor; none is startable
   before the record boundary moves.
4. T005 is never split and stays last, whichever feature ends up owning it.

## Risks

- The flip exceeds the DECISION F104 D1 cap of 500 insertions for one commit and
  cannot be split without a red tree, so it needs a ruling this feature's budget
  cannot buy. That is the scope report's central question.
- A half-performed deletion is the state the Orchestrator brief forbids, so every
  deletion round ends with the full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 11
  and round 25 the feature is inside it; session 12 reaches it.

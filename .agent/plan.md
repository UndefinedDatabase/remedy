# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 23 PASSED except round 2
(premise corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round
22). T001, T002 and T003 are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Settle how T004 is staged, which the deletion inventory deliberately left open
and which round 23's session had to re-derive from scratch. DECISION F272 D14
and `.agent/f272_t004_staging.md` record it: 60 production files migrate rather
than 72, the staging is BY CALLER, and `job.run-next` dies with the rail modules
rather than ahead of them.

## Next Steps

1. Migrate the classic-store consumers that feed the next-action rails, by
   caller, one consumer per commit range where the diff allows. Six of the eight
   rail modules never open the store; what blocks them is the record type their
   callers hand them.
2. Delete `job.run-next` and its sixteen advertisements in the commit range that
   migrates the last module advertising it, per DECISION F272 D13 and D14.
3. Name F114's cost-preview carrier BEFORE `job.run` goes. Measured at
   `67515ab7`: `apps/cli/commands/job.py:726` is the ONLY call site of
   `confirm_cost_preview` in the product and it sits inside the handler being
   deleted. `do.job-run` carries neither `is_expensive` nor `--yes`, and wiring
   the helper as-is would exit 2 on every non-tty run, so this needs a DECISION.
4. T005, the reachability test and the cluster deletion, which is never split.
   The twelve cluster-bound store consumers are NOT migrated; they wait for it.

## Risks

- 60 production and 127 test files still migrate. That does not fit the rounds
  F272 has left, so the session that reaches the soft limit executes the
  amend0905 split-and-close default from the scope report D14's figures supply.
- A half-performed deletion is the state the Orchestrator brief forbids, so every
  deletion round ends with the full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 11
  and round 24 the feature is inside it and no scope report is owed yet.

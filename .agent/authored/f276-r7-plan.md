# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 7 is the closure sequence's first half. It books round 6's verdict as
PASS and registers R-1006, repairs R-1006 where T004 left the disk floor out
of the `remedy job budget` limits listing, writes the feature file's Built
State paragraph for all four slices, and runs the integration gate — this
feature's ONE full suite run, by the worker, in the primary checkout, with
its transcript committed as `.agent/authored/f276-closure-suite.txt`.
T001 to T004 are built.

## Next Steps

1. The closure sequence's second half: `remedy integrity check --json`, the
   self-use item precondition 6 requires (the queue holds no pending item, so
   the generator runs first), the evidence job and a fresh review package,
   the ledger rotation, the re-assignment of every open finding to F282, and
   the one consolidation pass of the §3 checklist, which must come out at 35
   items or fewer.
2. Then the STATUS `[x]` flip with the README counters and the
   `consumed_by` edit in one commit, and the pull request into `main`, which
   the next session's Open PR Gate merges.
3. R-1004 and R-1005 stay open and are re-assigned to F282; R-0984's
   hosted-CI reading is answered by the first CI run of this feature's own
   pull request.

## Risks

A red closure suite is handled by amend0917-throughput rule 2 — at most three
repair rounds, each strictly shrinking the bad set — and not by weakening a
test.

# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 8 books round 7's verdict as PASS and resolves R-1006, then does the
two things the closure cannot be built on top of: the integration gate's ONE
repair run under amend0917-throughput rule 2, against an `apps/ui` built
BEFORE the run so the cold-checkout race DECISION F276 D9 diagnoses cannot
recur, replacing `.agent/authored/f276-closure-suite.txt` with a transcript
that states the previous bad set beside its own; and the self-use item
closure precondition 6 requires, which the generator must supply first
because the queue holds no pending item. T001 to T004 are built and R-1003
and R-1006 are resolved.

## Next Steps

1. The closure's last round: `remedy integrity check --json`, the ledger
   rotation as its own commit, the re-assignment of every still-open finding
   to F282 after that rotation, the one §3 checklist consolidation pass —
   which must come out at 35 items or fewer — and the evidence job with a
   fresh review package.
2. Then the STATUS `[x]` flip with the README counters and the `consumed_by`
   edit in one commit, as the last commit on the branch, and the pull request
   into `main`, which the next session's Open PR Gate merges.
3. R-1004 and R-1005 and F273's three closure candidates R-0998, R-0999 and
   R-1000 stay open and are re-assigned, never resolved; R-0984's hosted-CI
   reading is answered by the first CI run of this feature's own pull request.

## Risks

A second red closure suite is not repaired by weakening a test: amend0917
rule 2 allows three repair rounds, this is the first, and an `xfail` is
reserved for what survives all three.

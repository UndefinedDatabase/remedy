# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 9 books round 8's verdict as PASS, registers R-1007 from the self-use
run that closure precondition 6 consumed, and performs the three closure
steps that must precede the package: the one §3 checklist consolidation pass
this feature is allowed, which merges item 17 into item 15 and leaves the
list at 34; the ledger rotation as its own commit; and the re-assignment of
every still-open finding to F282, which follows the rotation for the reason
DECISION F276 D10 records. T001 to T004 are built, the integration gate is
green, and R-1003 and R-1006 are resolved.

## Next Steps

1. The closure's last round: `remedy integrity check --json` reading PASS, the
   evidence job through `job_evidence.create_manual_completion_bundle`, and a
   FRESH review package whose `base_commit` is the branch's FORK POINT
   `43d14817` — checked by the two `rev-list` readings agreeing — with its
   name, SHA-256 and archived path recorded.
2. Then the closure commit, which is the LAST commit on the branch: the
   STATUS `[x]` line, the README counters, SU-024's `consumed_by`, and the
   final `.agent/` state; then the pull request into `main`, which the next
   session's Open PR Gate merges.
3. R-1004, R-1005, R-1007 and F273's three closure candidates R-0998, R-0999
   and R-1000 stay open and are re-assigned, never resolved; R-0984's
   hosted-CI reading is answered by the first CI run of this feature's own
   pull request.

## Risks

The package is the one closure step that can fail late: an abbreviated
`base_commit`, a node-id list that is not from `--collect-only`, or a
directory where a file path belongs each surface only at zip time.

# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 6, round 24: the closure sequence's integration-gate round. Book round 23's PASS and
register the self-use run's defects as R-1156 and R-1157 (owned by F297); run the feature's one
full suite in the primary checkout, then `scripts/closure_suite_cost.py` once, and commit the
transcript `.agent/authored/f295-closure-suite.txt` as read.

## Next Steps
1. Book round 24; on a red suite, a repair round naming every bad node id (amend0917-throughput
   rule 2); on a green one, the evidence bundle and the review zip, with the staging copies
   reclaimed.
2. The ledger rotation, the open findings re-assigned to F297, the STATUS line with the README
   and the self-use entry's `consumed_by`, and the pull request.

## Risks
- R-1138, R-1139, R-1143, R-1149, R-1156 and R-1157 (Low) stay open, owned by F297.
- F295 reaches its soft limit of 25 rounds inside the closure sequence; the handoff then carries
  the scope report, and the closure is the self-consistent close.

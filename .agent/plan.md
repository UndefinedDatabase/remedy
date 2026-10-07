# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 7, round 25: book round 24's verdict, DECISION F295 D20 and one prose slip; run the
feature's one full suite again on the shipped tree, with the HEAD reflog read before and after,
then `scripts/closure_suite_cost.py` once, and commit the new transcript at
`.agent/authored/f295-closure-suite.txt` (DECISION F295 D20).

## Next Steps
1. Book round 25; on a red suite, a repair round naming every bad node id (amend0917-throughput
   rule 2); on a green one with identical reflog lines, the evidence bundle and the review zip,
   with the staging copies reclaimed.
2. The ledger rotation, the open findings re-assigned to F297, the STATUS line with the README
   and the self-use entry's `consumed_by`, and the pull request.

## Risks
- R-1138, R-1139, R-1143, R-1149, R-1156 and R-1157 (Low) stay open, owned by F297.
- F295 is at its soft limit of 25 rounds and 7 sessions; the closure is the self-consistent close
  and no split is proposed (scope report in the handoff).
- Another actor switched the primary checkout during round 24 (operator question Q6); a second
  switch during the run ends the session again.

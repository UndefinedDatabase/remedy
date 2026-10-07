# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 5, round 23: the closure sequence's first round. Book round 22's PASS; run the closure's
self-use item (docs/roadmap/STATUS_closure_protocol.md precondition 6) to its approval gate through
`run_next_self_use_item`, never applied. The generator supplies `SU-045`, "Refresh the pinned
toolchain", from its order tier; the builder may only edit files in its own job workspace.

## Next Steps
1. Book round 23 and register every defect the self-use run reports (precondition 6).
2. The integration-gate round: the one full suite, its transcript and its cost lines.
3. The evidence bundle and the review zip, with the staging copies reclaimed.
4. The ledger rotation, the open findings re-assigned to F297, the STATUS line with the README
   and the self-use entry's `consumed_by`, and the pull request.

## Risks
- R-1138, R-1139, R-1143 and R-1149 (Low) stay open, owned by F297.
- F295 reaches its soft limit of 25 rounds inside the closure sequence; the handoff then carries
  the scope report, and the closure is the self-consistent close.
- The self-use run spends real money, at most its order's declared budget of $10.00.

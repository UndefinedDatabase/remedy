# Plan — F298 Machine client contract v1.1: what a client can rely on

## Goal
One document generated from the code names every operation, field, word, token and exit code a
program meets when it drives Remedy, and the machine client page is its rendering
(docs/roadmap/features/T12_F298.md, T001). F298 closes at T001's scope; T002 to T007 moved to F304
(DECISION F298 D21).

## Current Step
Session 5, round 24: the closure's self-use item is generated and run to its approval gate, never
applied, its record saved under `.agent/selfuse_f298/` (docs/roadmap/STATUS_closure_protocol.md
precondition 6); round 23's verdict is booked.

## Next Steps
1. Register every defect the self-use run reports, then the one full suite and its CPU cost
   (precondition 2, amend0917-throughput).
2. The checklist's consolidation pass, the evidence bundle and review zip, the ledger rotation,
   the STATUS line with the README sync and the self-use queue's `consumed_by`, and the pull
   request.

## Risks
- F298 reaches its soft limit of 25 rounds inside the closure sequence; the split it owes was
  executed by DECISION F298 D21, and the handoff that reaches 25 carries the scope report.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.

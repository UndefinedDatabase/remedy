# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 4, round 20, the integration gate (closure precondition 2): `apps/ui` built, then the
closure's one full suite in the primary checkout on the tree that ships, and its CPU cost; the
self-use run of round 19 reported no defect.

## Next Steps
1. A green suite: the checklist's consolidation pass for F304; a red one: a repair round naming
   every bad node id, under amend0917-throughput rule 2.
2. The evidence bundle and the fresh review zip, with the staging-copy reclaim.
3. The ledger rotation, the STATUS line with the README sync and the self-use queue, the PR.

## Risks
- A selector that names no single project still fails in the init step instead of before any step
  (DECISION F268 D16 (4), kept by DECISION F304 D2).
- The operator's own data root holds 13,481 open decisions, so its digest stays about 10 MB
  under the window (DECISION F304 D16).
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.

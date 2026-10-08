# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 4, round 16, T007's last part (DECISION F304 D17): a small change to an existing
repository needs no contract template of its own; the page says what an order is held to, and
two tests pin it. T002 to T007 are complete with this round.

## Next Steps
1. The hardening stage of operator amendment amend0930b-slow-cap: a fresh auditor, given only
   the feature file and the repository, names for every Acceptance and Goal & Done statement the
   test that fails without it and proves it by one mutation, one proof through the command line.
2. Repair every gap it finds in reviewed rounds, at most three, then repeat the audit for them.
3. The closure sequence (docs/roadmap/STATUS_closure_protocol.md); its one full suite builds
   `apps/ui` first (DECISION F304 D5 (7)).

## Risks
- A selector that names no single project still fails in the init step instead of before any step
  (DECISION F268 D16 (4), kept by DECISION F304 D2).
- The operator's own data root holds 13,481 open decisions, so its digest stays about 10 MB
  under the window (DECISION F304 D16).
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.

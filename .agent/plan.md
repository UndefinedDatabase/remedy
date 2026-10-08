# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 4, round 17, the hardening stage's repair: the acceptance audit at `bfe69f3f6`
(`.agent/f304_acceptance_audit.md`) proved 38 of 40 claims and found one gap, R-1185: the second
gate test does not drive an order naming its project nor a declined result. This round adds both
paths to `tests/cli/test_machine_client_paths.py`.

## Next Steps
1. Repeat the audit for the two claims that had gaps, rows 3 and 7, with a fresh auditor.
2. The closure sequence (docs/roadmap/STATUS_closure_protocol.md): its first round books this
   round's verdict, R-1185's resolution and the repeated audit, and the Built State paragraph of
   amend0930b-slow-cap rule 4; its one full suite builds `apps/ui` first (DECISION F304 D5 (7)).

## Risks
- A selector that names no single project still fails in the init step instead of before any step
  (DECISION F268 D16 (4), kept by DECISION F304 D2).
- The operator's own data root holds 13,481 open decisions, so its digest stays about 10 MB
  under the window (DECISION F304 D16).
- R-1185 (Low) is owned by F304. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156,
  R-1157, R-1158, R-1162, R-1172, R-1176 (Low) stay open, owned by F297.

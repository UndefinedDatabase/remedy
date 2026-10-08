# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 2, round 7, T004's second part (DECISION F304 D7): the second gate test drives a merge
with its history and a push to a bare upstream, an order of two jobs, and one order file started
twice, through the command line alone; R-1184 is registered.

## Next Steps
1. R-1184's repair: `remedy job run` answers a run that does not end `completed` with `ok` false,
   one token for its end state and a non-zero exit.
2. T005, T006, T007; then the hardening stage; then the closure sequence.

## Risks
- A selector that names no single project still fails in the init step instead of before any step
  (DECISION F268 D16 (4), kept by DECISION F304 D2).
- Round 5 changed `apps/ui/src`, so the closure's one full suite builds `apps/ui` first (DECISION
  F304 D5 (7)).
- R-1184 (Medium) is open, owned by F304. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149,
  R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 (Low) stay open, owned by F297.

# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 3, round 9, T005's first part (DECISION F304 D10): each completed job in the digest
carries an `approval_card` read from its record alone, with its changed files (a count and the
first twenty), its test command and its tasks' verdicts, repair rounds and test answers.

## Next Steps
1. T005's second part: the blocking criteria of the job's mission contract with status and text,
   one recommendation word and one risk word derived by rules the page states, and a card that
   says when no check ran.
2. T006, T007; then the hardening stage; then the closure sequence.

## Risks
- A selector that names no single project still fails in the init step instead of before any step
  (DECISION F268 D16 (4), kept by DECISION F304 D2).
- Round 5 changed `apps/ui/src`, so the closure's one full suite builds `apps/ui` first (DECISION
  F304 D5 (7)); a live test's UI server rebuilds a stale `dist` by itself, gitignored.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.

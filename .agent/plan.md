# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 1, round 1, the claim: claim F304, re-head the review record, book F298's round 30 and
R-1182's resolution, and record DECISION F304 D1 (F298's claim measurement stands; DECISION F298
D1's slice order).

## Next Steps
1. T002 — an order runs in the repository of the project it names, or is refused before any step;
   one command registers a repository for a client and leaves its working copy clean.
2. T003 — honest refusals under `--approve --json`, and a command that declines a result.
3. T004 — the second gate test: commit and push to a local bare upstream, an order of two jobs, one
   order file started twice.
4. T005, T006, T007; then the hardening stage; then the closure sequence.

## Risks
- T002 changes where an order runs; a client standing below another repository must not change it
  (F298's inventory, the `plain` probe).
- F304 owns no open finding. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172, R-1176 (Low) stay open, owned by F297.

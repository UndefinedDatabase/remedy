# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 1, round 3, T002's second part (DECISION F304 D3): R-1183's repair, then
`remedy project register --repo <path>`, which registers a repository for a client and writes
nothing `git status` shows, added to the interface before `do.run`.

## Next Steps
1. T003 — honest refusals under `--approve --json`, and a command that declines a result.
2. T004 — the second gate test: commit and push to a local bare upstream, an order of two jobs, one
   order file started twice.
3. T005, T006, T007; then the hardening stage; then the closure sequence.

## Risks
- A selector that names no single project still fails in the init step instead of before any step
  (DECISION F268 D16 (4), kept by DECISION F304 D2).
- R-1183 (Low) is owned by F304 until the next round books its resolution. R-1160 (Medium) and
  R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 (Low) stay open,
  owned by F297.

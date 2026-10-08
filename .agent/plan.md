# Plan — F304 Machine client contract v1.1, part two: what a client can rely on

## Goal
A client's real paths work through the command line and are written down: an order runs in the
repository of the project it names, a refused apply says so, a result can be declined, an order of
several jobs and an order started twice behave, a program sees what changed and what it cost, and
the digest stays small (docs/roadmap/features/T12_F304.md, T002 to T007, carried from F298).

## Current Step
Session 4, round 14, T006's last part (DECISION F304 D15): the page says what the call and token
budgets count, and a test provider that reports usage proves that an order capped only by calls
or by total tokens is stopped at its cap and that the digest names its calls and tokens by kind.

## Next Steps
1. T007: the default digest lists every job that still needs something and the jobs that ended
   inside a window, names the window and how many jobs it left out, and a flag widens it; the
   first step measures the operator's own data root and a scratch root of 1,000 settled jobs.
2. T007's template question: does a small change to an existing repository need its own
   template.
3. The hardening stage of operator amendment amend0930b-slow-cap; then the closure sequence.

## Risks
- A selector that names no single project still fails in the init step instead of before any step
  (DECISION F268 D16 (4), kept by DECISION F304 D2).
- Round 5 changed `apps/ui/src`, so the closure's one full suite builds `apps/ui` first (DECISION
  F304 D5 (7)); a live test's UI server rebuilds a stale `dist` by itself, gitignored.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297.

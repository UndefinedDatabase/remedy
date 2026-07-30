# Plan — F052 Self-healing test rounds

## Goal
Trivial test breakage no longer kills unattended cycles: on a cycle
verify failure, up to cycles.repair_rounds (default 2) bounded
auto-repair rounds run through the EXISTING repair loop, verify
re-runs after each round, healed cycles record "healed after N
repair rounds" visibly, stubborn breaks fail after exactly two
rounds with the existing test-failure classification and linked
repair evidence, and repair cost lands on the job budget. DONE per
docs/roadmap/features/T1_F052.md: a one-line break heals in round
one; a stubborn break stops after exactly two rounds with an honest
trail; costs attributed via actuals.

## Next Steps
- R1 (LARGE): DONE — inspect report, T001 (trigger + cap + healed
  path) and T002 (stubborn + budget + stop + A9 edges) landed in
  four green commits; all four gates green; awaiting reviewer.
- Then: integration gate round; closure its own round (never
  bundled).

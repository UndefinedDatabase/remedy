# Plan — amend0930-test-load (operator amendment, 2026-09-30)

## Goal
Cap the test load (worker cap, priority, run record), stop repeated runs, register the test diet feature.
Branch: feature/amend0930-test-load. Not a loop feature; decisions are `DECISION amend0930 D<n>`.

## Current Step
Parts B and C (tests/load_governor.py, conftest wiring, config keys, red-proofs) committed as C1.

## Next Steps
- D1 vitest cap + UI contract; D2 Chrome/GPU measurement
- E protocol rules, build-remedy-self.md clause, budget figures, DECISIONs D1-D4
- F feature F293 registered thin (STATUS first unmarked line, TOTAL_FEATURES, README), findings
- G targeted pass, one measured full-suite run, PR, merge
- H handback to ~/.remedy-loop/amend0930-test-load.handback.md

## Risks
- Full suite under the cap takes longer; budget figures move to ~25 min.

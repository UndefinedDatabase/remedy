# Plan — amend0930-test-load (operator amendment, 2026-09-30)

## Goal
Cap the test load (worker cap, priority, run record), stop repeated runs, register the test diet feature.
Branch: feature/amend0930-test-load. Not a loop feature; decisions are `DECISION amend0930 D<n>`.

## Current Step
All parts built and verified (targeted pass green, full suite green under the cap: 21,082 passed in 448.7 s, 1,288 CPU s). PR open; waiting for hosted checks, then merge.

## Next Steps
- G4/G6: confirm no open PR, restore the original branch state
- H: handback to ~/.remedy-loop/amend0930-test-load.handback.md

## Risks
- Full suite under the cap takes longer; budget figures move to ~25 min.

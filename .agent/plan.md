# Plan — amend1016 (operator order amend1016-stabilization, Remedy's half)

## Goal
Correct the roadmap so that it matches the finished face migration: Remedy has no native frontend.
F309 "Cockpit v2" is withdrawn (never built) and leaves the executable queue; F303's cockpit
acceptance is read for the public API only; nothing can make Rule A5 propose a cockpit rebuild.
Branch feature/amend1016-f309-withdrawn. No feature of the queue is started.

## Current Step
Done. D1 (F309 withdrawn: `[!]` in Package 2, banner in its file, R-1321, R-1322 and R-1324
resolved by deletion, the guard tests/docs/test_no_native_face.py, the docs suite's STATUS pattern
accepts `[!]`) and D2 (F303 narrowed to the public API).

## Steps
- [x] S1 — STATUS: F309 moves to Package 2 as `[!]` withdrawn; feature files T5_F309 and T12_F303 annotated.
- [x] S2 — The decision amend1016 D1 and D2, and the three findings closed by deletion.
- [x] S3 — The guard test, failing on the old STATUS and passing now; the docs suite counts `[!]`.
- [x] S4 — Gates: targeted tests, `remedy roadmap next` (F078), integrity, ruff, the full lane.

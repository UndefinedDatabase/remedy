# Plan — F296 Evidence-triggered tier escalation (routing v2)

## Goal
A task that fails on a cheaper tier gets its next repair round on the next tier up, for reasons
the evidence names and never for provider unavailability, recorded in evidence, report, events and
ledger, off by default (docs/roadmap/features/T3_F296.md; DECISION F296 D1).

## Current Step
Round 1 (session 1): claim F296, re-head the finding record, book F307's round 32, write the slice
list, and take step (1) of `run_pingpong`'s boundary (T001a).

## Next Steps
1. Round 2: T001b and T001c — the pure escalation module with its configuration keys, and the
   loop's call with the provider swap, proved by a fixture job.
2. T002a and T002b, the record; T003, the benchmark and the default.
3. The closure sequence.

## Risks
- `run_pingpong` and `pingpong_loop.py` are held by the structure ratchet; every edit of them is
  line-neutral or offset by a structural step, and new logic goes into a new module.
- A no-progress stop exists already (two red runs with one fingerprint end the repair); the
  escalation must take its place only when a step up is available and the key is on.

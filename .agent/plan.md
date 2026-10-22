# Plan — F296 Evidence-triggered tier escalation (routing v2)

## Goal
A task that fails on a cheaper tier gets its next repair round on the next tier up, for reasons
the evidence names and never for provider unavailability, recorded in evidence, report, events and
ledger, off by default (docs/roadmap/features/T3_F296.md; DECISIONs F296 D1 and D2).

## Current Step
Round 2 (session 1): T001b and T001c — the three `model_escalation` keys, `TaskTierLadder` in
`packages/orchestration/tier_escalation.py`, `run_pingpong`'s two calls of it, line-neutral, the
fixture runs of the first and third Acceptance lines, and `docs/system/tier-escalation-v1.md`.

## Next Steps
1. T002a: the escalation in the call evidence, the run report's line and the `worker.escalated`
   event.
2. T002b: the outcome, cost, rounds and retries per task class and tier in the cost ledger.
3. T003, the benchmark and the default; then the closure sequence.

## Risks
- `run_pingpong` and `pingpong_loop.py` are held by the structure ratchet; every edit of them is
  line-neutral or offset by a structural step, and new logic goes into a new module.
- The ladder knows a role's tier only from the configured tier models; a run on other models
  never escalates, by design.

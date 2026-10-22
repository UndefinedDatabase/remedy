# Plan — F296 Evidence-triggered tier escalation (routing v2)

## Goal
A task that fails on a cheaper tier gets its next repair round on the next tier up, for reasons
the evidence names and never for provider unavailability, recorded in evidence, report, events and
ledger, off by default (docs/roadmap/features/T3_F296.md; DECISIONs F296 D1 to D3).

## Current Step
Round 3 (session 1): T002a — `EscalatedProvider` stamps every escalated call with an
`EscalatedCall`, which the round entry, the cost booking, the relaunch session guard, the run
report's line and the job's `worker.escalated` event read.

## Next Steps
1. T002b: the outcome, cost, rounds and retries per task class and tier in the cost ledger.
2. T003, the benchmark and the default; then the closure sequence.

## Risks
- `run_pingpong`, `pingpong_loop.py` and `pingpong_job.py` are held by the structure ratchet;
  every edit of them is line-neutral or offset by a structural step.
- The ladder knows a role's tier only from the configured tier models; a run on other models
  never escalates, by design.

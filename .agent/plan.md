# Plan — F296 Evidence-triggered tier escalation (routing v2)

## Goal
A task that fails on a cheaper tier gets its next repair round on the next tier up, for reasons
the evidence names and never for provider unavailability, recorded in evidence, report, events and
ledger, off by default (docs/roadmap/features/T3_F296.md; DECISIONs F296 D1 to D4).

## Current Step
Round 4 (session 1): T002b — the run record's `tier_ladder`, `tier_outcomes.json` per task run
from the job's evidence export, its mirror in the ledger's `tier_outcomes` table, and
`query_tier_outcomes` for F133.

## Next Steps
1. T003: the benchmark on the F082 corpus, cheap-first with escalation against the class tier,
   and the default with the feature file's Amendment.
2. The closure sequence.

## Risks
- `run_pingpong`, `pingpong_loop.py`, `pingpong_job.py`, `job_evidence.py` and `token_ledger.py`
  are held by the structure ratchet; every edit of them is line-neutral.
- A benchmark with paid providers may not be affordable inside the feature; the default then stays
  off and the Amendment says so, as the Acceptance allows.

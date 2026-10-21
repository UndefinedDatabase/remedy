# Plan — F311 The insight: what runs now, what the worker does, why it hangs

## Goal
A client asks Remedy over HTTP what runs now, looks into one job's worker, and learns why it hangs
and what the operator can do, in closed words (`docs/roadmap/features/T12_F311.md`, DECISIONs
F311 D1 to D4).

## Current Step
Round 2 (session 1): book round 1, register R-1383; two private helpers become public for the
reader (structural); the reader `packages/orchestration/job_insight.py` with the `now` and
`insight` answers of D1, the phase, stall reading and advice of D3, the threshold key
`insight.stall_seconds`, and the model server probe of D4; and R-1383's test.

## Next Steps
1. T003, first half: the twins `client.now` and `client.insight` in the catalog and the machine
   client interface, with their answer keys and the new words; the reader's unwired entry goes.
2. T003, second half: the two routes, the client token's project scope, the release matrix and
   the generated pages.
3. The closure: the one full suite, the self-use run, the evidence, STATUS, the PR.

## Risks
- `pingpong_job.py`, `pingpong_loop.py`, `pingpong_provider.py` and `config.py` sit at their
  structure rows: every hook and key lives outside them (DECISION F311 D2).
- `apps/cli/client_interface.py` sits at the 1,000-line file limit: new interface constants go to a
  module of their own.
- No test may reach the operator's model server: the probe's one fetcher is refused in tests.

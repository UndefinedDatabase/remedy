# Plan — F311 The insight: what runs now, what the worker does, why it hangs

## Goal
A client asks Remedy over HTTP what runs now, looks into one job's worker, and learns why it hangs
and what the operator can do, in closed words (`docs/roadmap/features/T12_F311.md`, DECISIONs
F311 D1 to D4).

## Current Step
Round 1 (session 1): claim F311, re-head the ledger, DECISIONs F311 D1 to D4, operator question
Q21, and the first half of T001: `packages/orchestration/worker_pulse.py`, its path helper in
`data_paths`, the binding in `pi_provider.bind_job_clock`, and each Pi call writing its role,
model, round, last output and stream entries into the job's pulse.

## Next Steps
1. The reader of T001 and the stall reading of T002: `packages/orchestration/job_insight.py`
   answering the `now` and `insight` shapes of D1, the phase, stall reason and advice of D3, the
   threshold key `insight.stall_seconds`, and the model server probe of D4.
2. T003, first half: the twins `client.now` and `client.insight` in the catalog and the machine
   client interface, with their answer keys and the new words.
3. T003, second half: the two routes, the client token's project scope, the release matrix and
   the generated pages.
4. The closure: the one full suite, the self-use run, the evidence, STATUS, the PR.

## Risks
- `pingpong_job.py`, `pingpong_loop.py` and `pingpong_provider.py` sit at their structure rows:
  every hook lives outside them (DECISION F311 D2).
- `apps/cli/client_interface.py` sits at the 1,000-line file limit: new interface constants go to a
  module of their own.

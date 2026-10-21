# Plan — F311 The insight: what runs now, what the worker does, why it hangs

## Goal
A client asks Remedy over HTTP what runs now, looks into one job's worker, and learns why it hangs
and what the operator can do, in closed words (`docs/roadmap/features/T12_F311.md`, DECISIONs
F311 D1 to D5).

## Current Step
Round 3 (session 1): book round 2, resolve R-1383, register R-1384 to R-1388, D3's second addendum
and D5; repair R-1384 to R-1388; move `DIGEST_KEY_TREE` out of `apps/cli/client_interface.py`
(structure step); and the first half of T003: the twins `client.now` and `client.insight`, their
answer keys and the interface's `insight` key, with T004's proofs for them.

## Next Steps
1. T003, second half: the routes `GET /api/v1/now` and `GET /api/v1/jobs/{job}/insight`, the
   client token's project scope, the release matrix and the generated pages.
2. The closure: the one full suite, the self-use run, the evidence, STATUS, the PR.

## Risks
- `pingpong_job.py`, `pingpong_loop.py`, `pingpong_provider.py` and `config.py` sit at their
  structure rows: every hook and key lives outside them (DECISION F311 D2).
- `apps/cli/client_interface.py` sits at the 1,000-line file limit: the structure step makes room
  and every new constant goes to a module of its own.
- No test may reach the operator's model server: the probe's one fetcher is refused in tests.

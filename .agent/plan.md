# Plan — F311 The insight: what runs now, what the worker does, why it hangs

## Goal
A client asks Remedy over HTTP what runs now, looks into one job's worker, and learns why it hangs
and what the operator can do, in closed words (`docs/roadmap/features/T12_F311.md`, DECISIONs
F311 D1 to D6).

## Current Step
Round 4 (session 1): book round 3, resolve R-1384 to R-1388, DECISION F311 D6; and the second half
of T003: the routes `GET /api/v1/now` and `GET /api/v1/jobs/{job}/insight` with the client
token's project scope, `job_insight.insight_lines`, the release matrix, the generated API page and
the guide's section, with T004's proofs for the routes.

## Next Steps
1. The closure: the one full suite, the self-use run, the Built State, the evidence, STATUS, the
   PR.

## Risks
- `pingpong_job.py`, `pingpong_loop.py`, `pingpong_provider.py` and `config.py` sit at their
  structure rows: every hook and key lives outside them (DECISION F311 D2).
- No test may reach the operator's model server: the probe's one fetcher is refused in tests.
- The public API's version stays `1.21` until F313 (DECISION F311 D6).

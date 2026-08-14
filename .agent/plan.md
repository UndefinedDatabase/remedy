# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0369. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368 — R-0365 and R-0366 were resolved at R3.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T002 — the governor itself, built this round in
`packages/orchestration/rate_governor.py`: per-provider cooldown state fed by
`RateLimitSignal`, `acquire()` with an injected clock and a budget deadline,
stop-beats-wait ordering, and wait events. Nothing calls it yet; the seam is
T003. Awaiting the reviewer's gate.

## Next Steps
1. T003 — seam integration in `_call_with_retry`
   (`packages/orchestration/pingpong_loop.py:2142`, which already carries
   `stop_check`), ordered stop, then budget, then acquire; wait evidence; the
   report line; the limit-emitting fixture end-to-end.
2. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Stop-beats-wait is the acceptance criterion most likely to be faked by a
  comment. It is pinned by two tests and a mutation red-proof this round.
- `is_rate_limit_error` still has no precedence rule against the existing
  transport predicates. T003 decides it with evidence; nothing depends on it yet.

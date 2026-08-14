# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0368. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367 —
R-0365 and R-0366 are RESOLVED by reviewer-authored `Done:` text at R3.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as they do today.

## Current Step
T001 is DONE, reviewed and PASSed over rounds R1-R3: signal normalization lives
in `packages/orchestration/rate_governor.py` with 46 unit tests, an inventory of
the five real evidence shapes, and no wiring into any caller. The session closed
here at its own capacity limit, not at a blocker.

## Next Steps
1. T002 — the governor: per-provider cooldown state fed by `RateLimitSignal`,
   `acquire(provider, role)` with a deadline taken from budgets, an INJECTED
   clock (no real sleeps in unit tests), exponential cooldown with a documented
   cap when the provider gave no `retry_after_s`, and a wait event
   {provider, waited_s, reason}. Stop must beat wait: a stop request during a
   wait interrupts it immediately, so acquire polls in slices rather than
   sleeping once. Design the interface for N concurrent acquirers; implement
   single-flight. Multi-process runs share nothing in v1 — document it.
2. T003 — seam integration in `_call_with_retry`
   (`packages/orchestration/pingpong_loop.py:2142`, which already carries
   `stop_check`), ordered stop, then budget, then acquire; wait evidence; the
   report line; the limit-emitting fixture end-to-end.
3. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The stop-beats-wait ordering is the acceptance criterion most likely to be
  faked by a comment. It needs its own test with an injected clock.
- `is_rate_limit_error` still has no precedence rule against the existing
  transport predicates. T003 decides it with evidence; nothing depends on it yet.

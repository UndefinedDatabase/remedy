# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0374. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368, R-0369, R-0371, R-0372, R-0373 — R-0365, R-0366 and R-0370 are resolved.
R-0372 and R-0373 are fixed on disk this round and stay OPEN until a reviewer
verdict closes them; only reviewer-authored text may.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T003 repair. The governor is wired at all THREE `_call_with_retry` call sites,
and a rate-limit error is retryable at that seam so the governor is actually
reached — without touching the transport policy in provider_timeouts.py, which
the feature file forbids.

## Next Steps
1. T003 part 2, the report surfaces: `rate_limit_waits` in
   `export_pingpong_json`, the "waited Ns on provider rate limits this run"
   line in `summarize_pingpong` from `total_waited_s`, and the limit-emitting
   fixture end-to-end the feature's Acceptance section requires — the fixture
   should emit a BARE rate limit, which is what R-0373 made reachable.
2. Integration gate per docs/agents/integration_gate.md, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The seam now decides retryability for one error class. The 294-test
  regression gate is what proves the pre-F057 path did not move; run it on
  every round that touches `_call_with_retry`.
- A permanently rate-limited provider now consumes MAX_RETRIES instead of
  failing at once. That is the intended trade, and `next_backoff` still bounds
  it, but the report line in part 2 is what makes the cost visible.

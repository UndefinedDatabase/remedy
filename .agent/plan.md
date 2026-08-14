# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0372. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368, R-0369, R-0371 — R-0365, R-0366 and R-0370 are resolved.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T003 part 1: the governor is wired into `_call_with_retry` in
`packages/orchestration/pingpong_loop.py` — observe on a failed call, acquire
before the first call and before every retry, waits recorded on
`PingPongResult.rate_limit_waits` — with the seam tests in
`tests/orchestration/test_provider_retry.py`. DECISIONS F057 D3, D4 and D5
record the three choices the feature file left open.

## Next Steps
1. T003 part 2: the report surfaces — `rate_limit_waits` in
   `export_pingpong_json`, the "waited Ns on provider rate limits this run"
   line in `summarize_pingpong` from `total_waited_s`, and the limit-emitting
   fixture end-to-end that the feature's Acceptance section requires.
2. Integration gate per docs/agents/integration_gate.md, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The seam now runs on every provider call. Its whole cost when no governor is
  passed and when the provider is falsy must stay zero, which is what the
  294-test regression gate exists to prove.
- `is_rate_limit_error` and the transport predicates still have no precedence
  rule against each other. The seam observes AFTER `should_retry` has already
  decided, so nothing is contradicted today, but F049 will need one.

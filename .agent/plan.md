# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e after
PR #198 merged. Next free finding id: R-0363. Open findings: R-0361, R-0362.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as they do today.

## Current Step
R1 — claim F057, reset the review record carrying R-0361 forward, register
R-0362, record DECISION F057 D1, and build T001: one place that turns the
rate-limit signal shapes this repo really emits into a normalized signal, with
unit tests over samples extracted from evidence that already exists. Nothing
calls the new module yet.

## Next Steps
1. T002 — the governor itself: per-provider cooldown state, `acquire()` with a
   deadline taken from budgets, an injected clock, and the stop-beats-wait
   ordering. No real sleeps in unit tests.
2. T003 — seam integration at the provider-call choke point
   (`_call_with_retry`), wait evidence, the report line, and the
   limit-emitting fixture end-to-end.
3. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The seam is shared with the safe-point check. The ordering stop, then budget,
  then acquire is load-bearing and gets its own test in T002 rather than a
  comment.
- `is_rate_limit_error` must not swallow strings the existing transport
  predicates already own. T001 adds no wiring at all, so that precedence is
  settled with evidence in T003 and is not guessed now.

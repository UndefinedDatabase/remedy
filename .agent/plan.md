# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e after
PR #198 merged. Next free finding id: R-0367.
Open findings: R-0361, R-0362, R-0363, R-0364, R-0365, R-0366

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as they do today.

## Current Step
R2 — DONE. R1 was reviewed PASS; that verdict and findings R-0363 to R-0366 are
persisted in `.agent/live_review.md`. Two of the four were fixable here and are
fixed: R-0365 (the `is_rate_limit_error` docstring claimed a call graph the
module does not have) and R-0366 (the frozen-dataclass test asserted a bare
`Exception`). R-0363 and R-0364 are reviewer-side and stay open. No governor,
no `acquire`, no clock landed this round. Next: T002.

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

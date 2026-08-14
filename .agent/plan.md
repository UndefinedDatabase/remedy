# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0371. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368, R-0369, R-0370 — R-0365 and R-0366 were resolved at R3. R-0370 carries a
`Landed:` line this round; only reviewer-authored text may close it.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T001 and T002 are built and PASSed. This round records the R4 verdict, registers
R-0369 and R-0370, closes R-0370's coverage gap with one test, and confirms the
T003 seam on disk in `.agent/f057_t003_seam_inventory.md` without touching
`packages/orchestration/pingpong_loop.py`. No production code changed.

## Next Steps
1. T003 — seam integration in `_call_with_retry`
   (`packages/orchestration/pingpong_loop.py`, which already carries
   `stop_check`), ordered stop, then budget, then acquire; wait evidence; the
   report line; the limit-emitting fixture end-to-end. Start from the C3
   inventory: it names the call site, the ordering gap, the deadline conversion
   and the regression tests that must stay green.
2. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The deadline conversion is T003's real work: `acquire` wants an absolute
  monotonic value and the loop's budgets are unlikely to be in that form. The
  inventory names what exists; T003 must not invent a scale.
- Wiring the governor makes `is_rate_limit_error` live for the first time, and
  it still has no precedence rule against the existing transport predicates.
  T003 decides it with evidence.

# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0379. Open findings, recomputed from `.agent/live_review.md` and
not carried over from the previous plan: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378 — thirteen.
R-0365, R-0366, R-0370, R-0372 and R-0373 are resolved. `.agent/live_review.md`
is the source of truth for this ledger; this file is a mirror of it and nothing
else.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T003 part 2, item 1: the end-to-end test that pins the reviewer parse-retry call
site, which R-0374 registered as wired but unpinned. The governor wiring itself
is already on disk at all three `_call_with_retry` call sites; this step adds no
production code.

## Next Steps
1. The report surfaces: `rate_limit_waits` in `export_pingpong_json`, and the
   "waited Ns on provider rate limits this run" line in `summarize_pingpong`
   built from the recorded waits.
2. Integration gate per docs/agents/integration_gate.md, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The seam decides retryability for one error class. The 294-test regression
  gate is what proves the pre-F057 path did not move; run it on every round that
  touches `_call_with_retry`.
- A reviewer rate limit reaches the governor only when its error carries the
  `provider_error:` prefix, because `ReviewerOutput.verdict` defaults to
  `"blocked"` and the reject rule would otherwise swallow it. R-0378 tracks that
  this coupling is undocumented in the code.

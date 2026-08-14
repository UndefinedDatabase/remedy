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
T003 is COMPLETE on disk: the governor is wired at all three `_call_with_retry`
call sites, a rate limit is retryable at that seam, the reviewer parse-retry site
is pinned end to end, and both report surfaces — the exported `rate_limit_waits`
key and the `Rate limits:` summary line — are live and red-proved.

## Next Steps
1. The integration gate per docs/agents/integration_gate.md: full-suite branch
   run and base run, compared. It is a whole round; the base worktree needs the
   node_modules/dist parity that file's step 2 describes.
2. Closure per docs/roadmap/STATUS_closure_protocol.md, which is also where the
   thirteen open findings above are registered or resolved rather than dropped.

## Risks
- Thirteen open findings is the largest carry this feature has held. Closure is
  the round that must account for every one of them, not the round that inherits
  them quietly.
- A reviewer rate limit reaches the governor only when its error carries the
  `provider_error:` prefix, because `ReviewerOutput.verdict` defaults to
  `"blocked"`. R-0378 tracks that this coupling is undocumented in the code.

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
R12 is the integration gate per docs/agents/integration_gate.md: the full-suite
branch run, the full-suite base run at merge base 21c8148e in a throwaway
worktree with UI artifact parity restored by content, the comm comparison, and a
per-id attribution for every branch-only and every base-only failure. R11 passed
its gate; T003 is complete on disk and no code changes this round.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH
   review zip, the authored STATUS line committed last, then the PR. The thirteen
   open findings above are registered or resolved there rather than dropped.

## Risks
- A reproducible branch-only failure coupled to F057 code is a BLOCKER and its
  own reviewer-gated round, never a fix folded into this one.
- The base worktree's dist is stale by construction after `cp -a` (F105 R49):
  the checkout stamps src at checkout time while the copy preserves dist's older
  mtime, so parity is restored by content AND by touching dist after the copy,
  and any surviving base-only id is attributed per id.

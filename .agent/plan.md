# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0380. Open findings, recomputed from `.agent/live_review.md` and
not carried over from the previous plan: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379 —
fourteen, three Medium and eleven Low, none High. R-0365, R-0366, R-0370, R-0372
and R-0373 are resolved. `.agent/live_review.md` is the source of truth for this
ledger; this file is a mirror of it and nothing else.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
R13 records the R12 integration-gate verdict, registers R-0379, and lands the
feature file's Built State section, which closure precondition 4 requires to be
current BEFORE the closure commit. The integration gate PASSED at R12: the
branch and base full-suite runs are both green and both comm lists are empty.

## Next Steps
1. R14, closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH
   review zip, the reviewer-authored STATUS line and the README capability sync
   in one final commit, then the PR. The PR is NOT merged in this session; it
   merges at the next feature's start via the Open PR Gate.
2. The fourteen open findings close as documented Medium/Low risks — the verdict
   is PASS_WITH_RISKS — since none is High and the integrity check reports no
   open blocker/high findings.

## Risks
- Fourteen open findings is the largest carry this feature has held, and most of
  them are reviewer gate defects rather than product defects. Closure must name
  them as accepted risks, not inherit them quietly.
- A reviewer rate limit reaches the governor only when its error carries the
  `provider_error:` prefix, because `ReviewerOutput.verdict` defaults to
  `"blocked"`. R-0378 tracks that this coupling is undocumented in the code.

# Plan — F258 Self-use track v2 (CLOSED)

Branch: feature/f258-self-use-v2, cut from `main` at the merge commit of pull
request 225. F258 is CLOSED: `docs/roadmap/STATUS.md` carries its `[x]` line
and the pull request is open and UNMERGED.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger. DONE.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001/T002/T003, integration gate | done | rounds 2-7 |
| all six closure preconditions | done | rounds 8-10 |
| the evidence bundle and the review zip | done | round 11, READY_FOR_REVIEW |
| the closure commit | done | this round, Rule A4's last commit |
| the pull request | done | opened and NOT merged |

## Next Steps
1. Nothing further on this branch. The next feature's Open PR Gate merges
   this pull request, or the operator merges it manually at any time.
2. Rule A5 selects the next feature in a fresh session.

## Risks
- THE SELF-USE QUEUE HOLDS TWO PENDING ITEMS after this close (SU-003,
  SU-004) — not exhausted, unlike F257's close. No generator action is
  needed at the next feature's close.
- R-0570 (Low) and R-0736 (Medium) stay registered and unrepaired, both
  outside F258's own surface. R-0757 (Medium) IS F258's own defect (the
  self-use runner's silent fake-provider default) and is deliberately not
  repaired on this branch — a follow-up round, not a closure blocker.
  Together these are the documented risks behind the PASS_WITH_RISKS
  verdict.

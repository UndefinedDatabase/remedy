# Plan — F257 Self-use track (CLOSED)

Branch: feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220. F257 is CLOSED: `docs/roadmap/STATUS.md` carries its `[x]` line and
the pull request is open and UNMERGED.

## Goal
Remedy is used on Remedy on a schedule that cannot be skipped: a curated queue of
small maintenance jobs, exactly one consumed per feature close, run through
`do job-plan` and `do job-run` against this repository and taken to the normal
approval gate. DONE.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the queue, the loader, the job-path seam | done | rounds 2-5, 36 tests |
| the integration gate | done | round 6, 18186 passed 0 failed |
| the feature file's Built State | done | round 7, precondition 4 |
| plan SU-001 and stop at the approval gate | done | round 8, precondition 6 |
| three tests survive their own feature's close | done | round 10, R-0737 |
| the evidence bundle and the review zip | done | round 11, READY_FOR_REVIEW |
| the closure commit | done | this round, Rule A4's last commit |
| the pull request | done | opened and NOT merged |

## Next Steps
1. Nothing further on this branch. The next feature's Open PR Gate merges this
   pull request, or the operator merges it manually at any time.
2. Rule A5 selects F033 — Hunk-level diff approval — as the next feature, in a
   fresh session.

## Risks
- THE SELF-USE QUEUE IS NOW EXHAUSTED. SU-001 is consumed by F257 and no pending
  item remains, so the next feature's close records
  `self-use NONE (queue exhausted)` until an operator curates more items into
  `scripts/self_use_queue.json`. That is the track asking for curation, and
  closure precondition 6 explicitly does not treat it as a blocker.
- R-0734 and R-0736 stay registered and unrepaired, both outside F257's surface.
  They are the documented Medium risks behind the PASS_WITH_RISKS verdict.

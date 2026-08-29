# Plan — F257 Self-use track

Branch: feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220. F257 was claimed by Rule A5 as the first unchecked line in
`docs/roadmap/STATUS.md` after F256.

## Goal
Remedy is used on Remedy on a schedule that cannot be skipped: a curated queue
of small maintenance jobs, exactly one consumed per feature close, run through
`do job-plan` and `do job-run` against this repository and taken to the normal
approval gate.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the queue file and its read-only loader | done | round 2, 18 tests |
| render a queue item and plan it on the real job path | done | round 3 |
| refuse a job file written outside its destination | done | round 4, R-0733 |
| consume exactly one item per feature close | done | round 4, precondition 6 |
| refuse an id that is not one file name | done | round 5, R-0735 |
| document the format where a reader looks | done | round 5 |
| the integration gate | done | round 6, PASSED, 18186 passed 0 failed |
| the feature file's Built State | done | round 7, precondition 4 |
| plan SU-001 and stop at the approval gate | done | round 8, precondition 6 |
| the evidence bundle and the review zip | done | this round, closure steps 1-2 |
| the closure commit and the PR | open | next, and it is the last round |

## Next Steps
1. The closure commit, in ONE commit: the `[x]` flip on line 85 of
   `docs/roadmap/STATUS.md`, the README capability sync that may never disagree
   with it, the `scripts/self_use_queue.json` `consumed_by` edit that marks SU-001
   consumed by F257, and the final `.agent/` state.
2. Open the pull request. It is NOT merged in this session — the gap is the
   operator's manual-review window, and the next feature's Open PR Gate merges it.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 and R-0736 are registered and deliberately NOT repaired on this branch;
  both are outside F257's surface.

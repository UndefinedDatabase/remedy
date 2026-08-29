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
| the evidence bundle and the review zip | superseded | round 9; the head moves |
| three tests survive their own feature's close | done | this round, R-0737 |
| rebuild the bundle and the zip at the new head | open | next |
| the closure commit and the PR | open | after the rebuilt zip |

## Next Steps
1. Rebuild the evidence bundle and the review zip at the repaired head; the
   package from round 9 recorded `506bbab5` as the accepted HEAD and a content
   commit has landed since, so it no longer covers the head being closed.
2. The closure commit, in ONE commit: the `[x]` flip on `docs/roadmap/STATUS.md`,
   the README accepted count, its `Next:` clause, the tier-5 Done cell, the README
   capability paragraph, the `scripts/self_use_queue.json` `consumed_by` edit and
   the final `.agent/` state. Then the PR, unmerged.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 and R-0736 are registered and deliberately NOT repaired on this branch;
  both are outside F257's surface.
- The queue holds ONE item, so F257's own close EXHAUSTS it. The next feature's
  close records `self-use NONE (queue exhausted)` until an operator curates more.

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
| the feature file's Built State | done | this round, precondition 4 |
| the closure sequence | open | next, and it must satisfy precondition 6 |

## Next Steps
1. Satisfy closure precondition 6 for F257 itself: plan the pending self-use item
   through `packages.orchestration.self_use_job` and take it to the approval gate.
   F257 is the FIRST feature that must consume an item at its own close.
2. Build the evidence bundle and the review zip from a clean tree.
3. The closure commit — STATUS, README, `scripts/self_use_queue.json`
   `consumed_by`, and the final `.agent/` state — then the PR.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 and R-0736 are registered and deliberately NOT repaired on this branch;
  both are outside F257's surface.

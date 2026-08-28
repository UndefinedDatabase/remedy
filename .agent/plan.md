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
| claim F257 and retarget the state | done | round 1 |
| rule the queue format and the consumption point | done | DECISIONS F257 D1 and D2 |
| the queue file and its read-only loader | done | round 2, 18 tests |
| render a queue item and plan it on the real job path | done | round 3, 7 tests |
| refuse a job file written outside its destination | done | this round, R-0733 |
| consume exactly one item per feature close | done | this round, precondition 6 |
| document the format where a reader looks | open | acceptance item 1 |

## Next Steps
1. Document the queue format and the job-file format where a reader would look,
   and register the page in `docs/README.md`.
2. Run the integration gate and build the closure package.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 is registered against `tests/ui_server/` and is deliberately NOT
  repaired on this branch; it is unrelated to F257's scope.

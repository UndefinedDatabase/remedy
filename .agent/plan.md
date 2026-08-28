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
| claim F257 and retarget the state | done | this round |
| rule the queue format and the consumption point | done | DECISIONS F257 D1 and D2 |
| the queue file and its read-only loader | open | next round, against D2 |
| render a queue item into a job file and plan it | open | needs the loader first |
| consume exactly one item per feature close | open | the closure-protocol edit |
| document the format where a reader looks | open | acceptance item 1 |

## Next Steps
1. Build `scripts/self_use_queue.json` and its read-only loader
   `packages/orchestration/self_use_queue.py`, with tests, against DECISION
   F257 D2.
2. Render a pending queue item into a job file and plan it through
   `plan_job_from_file`, so the queue reaches the real job path.
3. Wire the consumption point into the closure sequence, so exactly one item is
   consumed per feature close and the track cannot rot.

## Risks
- A job must never mark its own queue item consumed; the loader will ship no
  writer and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.

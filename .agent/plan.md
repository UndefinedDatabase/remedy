# Plan — F272 One world completion

Branch: feature/f272-one-world-completion, cut from `main` at
`b18fad576252f7f2739a5807b6408031da8fcde6`, the merge commit of pull request
242. F260 is accepted; this feature carries the scope DECISION F260 D8 split
off it, and its Acceptance list IS F260's, unchanged.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 1 claims F272 in the roadmap ledger, cuts the branch, re-points this file
and `.agent/context.md`, re-heads `.agent/live_review.md`, and lands the FIRST
half of T001: `JobPlan.run_refs`, the ordered ids of the runs one job produced,
persisted through the job record and populated where a task's run is recorded,
with the tests that prove it on a job created through the ping-pong path.

## Next Steps

1. The run re-key: `run_log_dir` and `pingpong_run_dir` collapse onto the one
   `run_dir` keyed by RUN id, together with the test-side spelling sweep
   DECISION F260 D6 declined and this feature inherits. `run_refs` lands first
   because a reader needs a job able to name its runs before the directory
   stops being keyed by the job.
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows (T003).

## Risks

- The re-key consumes its own observer: the tests that hand-spell the old path
  are the only reason such a round can go red at all, so the sweep needs its
  pre-sweep and post-sweep pair rather than one commit.
- `<data_root>/runs/` is occupied today by the job-keyed run log, so both
  function bodies must move together or two directories merge under one key.

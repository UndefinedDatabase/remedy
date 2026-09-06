# Plan — F272 One world completion

Branch: feature/f272-one-world-completion, cut from `main` at
`b18fad576252f7f2739a5807b6408031da8fcde6`. Round 1 is reviewed and PASSED.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 2 completes the FIRST move of the re-key. `<data_root>/runs/` is occupied
today by the job-keyed run log, so nothing can be keyed there by RUN id until
that log moves out. This round books round 1's verdict, records DECISION F272 D1
— which rules the staging from the reviewer's measurement of 74 reader and 35
writer call sites — moves the run log to `<data_root>/job_logs/<job_id>` and the
ping-pong run store to `<data_root>/runs/<run_id>`, each one function body, and
sweeps the three test files that hand-spell those paths.

## Next Steps

1. The name collapse DECISION F272 D1 places next: `pingpong_runs_dir` and
   `pingpong_run_dir` are DELETED in favour of `runs_dir` and `run_dir` at every
   call site, with no alias and no attic, per AGENTS.md "Replacing is deleting".
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit where
   the diff allows (T003).

## Risks

- The run log's directory moves while its API does not. Every one of the 74
  readers and 35 writers keeps working only because they all resolve through
  `data_paths.run_log_dir`; a caller that hand-spells the path instead would
  break silently, which is why the three test files that do exactly that are
  swept in the same commit and are the round's red proof.
- Old `.data` content becomes unreadable at this move. That is DECISION D-A
  working as ruled — no migration, no compatibility reader — not a regression.

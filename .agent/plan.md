# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 PASSED. Round 2 FAILED
its gate: its production change was right, but DECISION F272 D1 sized the change
set from a three-file search and 24 test files observed the move. Round 3 swept
those 24 and took the tip from 207 failures to 2. Round 4 clears the last 2.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 4 finishes T001's re-key. It books the round 2 and round 3 verdicts, moves
the ONE job-keyed run-log path that lives outside `tests/` —
`scripts/remedy_runtime_cli_smoke.py`, which both CLI runtime smoke tests shell
out to — and lands DECISION F272 D2, whose consequence is stated over the whole
repository rather than over `tests/`, because scoping it to `tests/` is the
error D2 exists to correct. No finding id is minted: the second instance belongs
to R-0818, which stays open until its fix is reviewed.

## Next Steps

1. The name collapse DECISION F272 D1 places next: `pingpong_runs_dir` and
   `pingpong_run_dir` are DELETED in favour of `runs_dir` and `run_dir` at every
   call site, with no alias and no attic, per AGENTS.md "Replacing is deleting".
   Measured at `385d3b16`: about 170 sites across roughly 35 files, so it is
   split by module group across several commits.
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit where
   the diff allows (T003).

## Risks

- The name collapse is a pure rename: `pingpong_run_dir` and `run_dir` return
  the same path today, which `tests/test_data_paths.py` pins. A rename that
  large still needs a red-proof pair rather than a mutation, because moving one
  accessor moves reader and writer in lockstep and no observer can see it.

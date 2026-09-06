# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1, 3 and 4 PASSED; round 2
FAILED on a premise DECISION F272 D2 has now corrected. The run re-key is
finished and the tip is green: the 25-file observer set is 1125 passed.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 5 is the production half of DECISION F272 D1's "move two": all 41
production callers of `pingpong_run_dir` and `pingpong_runs_dir` move onto
`run_dir` and `runs_dir`. Seven of them assign a local of that very name, so
those reach the function through `data_paths` instead of importing it, which
DECISION F272 D3 rules and explains. The two functions are NOT deleted yet and
nothing under `tests/` is touched.

## Next Steps

1. The test half of the same move — 132 occurrences in 27 files — and then the
   deletion of `pingpong_runs_dir` and `pingpong_run_dir` from `data_paths.py`
   in that round's last commit, with the alias test that pins them deleted
   alongside, its four properties already being pinned for the real names at
   `tests/test_data_paths.py` lines 79, 102, 376 and 396.
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit where
   the diff allows (T003).

## Risks

- A token swap shadows the imported function wherever a local is already called
  `run_dir`, and in `pingpong_loop.py` that is `UnboundLocalError` rather than a
  style problem. The shape rule exists for that and the gate counts the shadows
  to zero.
- A rename cannot be proved by mutating the accessor, because reader and writer
  move together. The proof is a before/after pair over tests that never name the
  old spelling.

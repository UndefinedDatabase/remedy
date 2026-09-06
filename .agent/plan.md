# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1, 3, 4 and 5 PASSED; round 2
FAILED on a premise DECISION F272 D2 has corrected. Round 6 finishes T001: the
test half of the name collapse and the deletion of the two ping-pong spellings.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 6 moves the 132 test-side callers onto `run_dir` and `runs_dir` by the two
shapes DECISION F272 D3 rules, choosing between them with an AST scope test
rather than an assignment regex, and then DELETES `pingpong_runs_dir` and
`pingpong_run_dir` in the round's last code commit. The test that exists only to
pin those two is deleted with them; its four properties are already pinned for
the real names in the same file. When this round ends, T001 is complete.

## Next Steps

1. T002, the rest of the unified record: the eleven administrative fields, eight
   of which have no counterpart in `JobPlan`, and the Mission extension — the
   order, the contract, the mission plan and the ordered job references.
2. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each with a test that proves it works on a job created
   through the ping-pong path.
3. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A missed caller is invisible until the deletion commit, where it becomes an
  `ImportError`. That is why the deletion is last and why the suites run after
  it rather than before.
- The shadowing hazard is a property of the enclosing SCOPE, not of the line
  being edited. Round 5 found three sites an assignment regex could not see.

# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 88 ROUTES THE JOB-STORE LOADS UNDER `packages/` AWAY FROM `UUID(...)`. A new disk-free
`normalize_job_id` returns a UUID in canonical form or a sixteen-hex job id unchanged, and
raises `JobIdInvalid` for anything else. The parses that hand a job id to `load_job`,
`load_job_safe` or `_lj` go through it, except in `ui_server._load_job` and `execute_test_run`,
which keep theirs for reasons the guard names. A guard test pins the census by shape, one
behaviour test pins `run_job_fulfill`'s load, and the round books the round 87 verdict and
its prose slips.

## Next Steps

1. THE NEXT RESIDUE GROUPS OF THE FLIP'S DRY RUN, each a pre-flip production round or a
   transform rule: the task-id parses that feed `TaskEntry`, the `UUID` values
   `pingpong_job._persist_job` cannot serialise, and `ui_server`'s which-store loader and its
   adapter.
2. THE FLIP'S DRY RUN AGAIN after them, read for what remains.
3. THE FLIP, carrying DECISION F275 D48's obligations, as a series of commits each under the
   500-insertion cap inside one round, unless the operator allows one more oversized commit.
   The stale test double at `packages/orchestration/project_registry.py:856` moves with it.
4. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: flipped on this round's candidate the full suite has 752 bad nodes.
- MOST ROUTED LOADS ARE PINNED BY A SHAPE GUARD ALONE; only `run_job_fulfill`'s first load
  also has a behaviour test.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.

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

ROUND 89 CLEARS TWO RESIDUE GROUPS THE FLIP'S DRY RUN NAMED, BOTH INVISIBLE BEFORE THE FLIP.
`run_job_fulfill` stops passing a task id it wrote itself through `UUID(...)` and back, and the
tests that hand a job-store load or `append_run_event` a `UUID(...)` parse of a job id take
`normalize_job_id` instead. Before the flip both changes are value-identical, so they are proved
in flipped trees: the touched test files flipped at the base and at the change, and the round
trip restored inside the flipped change. The round books the round 88 verdict and its slip.

## Next Steps

1. THE NEXT RESIDUE GROUPS OF THE FLIP'S DRY RUN, each a pre-flip production round, a
   transform rule or a flip-time edit: `ui_server`'s which-store loader and its adapter;
   members the unified records lack, such as `TaskEntry`'s `acceptance_checks` and
   `JobPlan`'s `model_dump_json`; `UUID` values reaching the unified record; and what is left
   of the classic runner under `job resume`.
2. THE FLIP'S DRY RUN AGAIN after them, read for what remains.
3. THE FLIP, carrying DECISION F275 D48's obligations, as a series of commits each under the
   500-insertion cap inside one round, unless the operator allows one more oversized commit.
   The stale test double at `packages/orchestration/project_registry.py:856` moves with it.
4. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: DECISION F275 D62's flipped full suite had 752 bad nodes.
- A CHANGE PROVED ONLY IN A FLIPPED TREE depends on the generator and transform staying
  reproducible from round 77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.

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

ROUND 99 ADDS THE FLIP'S TENTH OVERLAY, on top of the first nine, under DECISION F275 D64's
method. The checkpoint writer measures a job's snapshot at the unified record's own path,
tests that touch a job's record on disk use that path, the mission command tests build their
jobs as unified records, and the layout guard stops pinning the checkpoint module to the
classic store. The diff is carried in a carrier, so no path under `packages/`, `apps/` or
`tests/` moves; the round books the round 98 verdict and its prose slip.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it:
   production code that hands a `JobPlan` a `JobBudgets` model where the record holds its
   serialized dict; the self-dogfood runtimes; the classic-shaped tests of routed handlers in
   `tests/test_data_paths.py`; and what is left of the classic runner under `job resume`,
   whose kill-and-resume fixture still builds a classic job.
2. THE FLIP: the transform, then every overlay in round order, landed as a series of commits
   each under the 500-insertion cap inside one round, carrying DECISION F275 D48's obligations
   and registering the structured acceptance form DECISION F275 D22 leaves to it, unless the
   operator allows one more oversized commit.
3. Then the classic store, with the which-store branches and adapters the overlays leave
   unreached, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: many test nodes still fail in the flipped tree, and a test that starts
  the command line from a directory outside that tree runs this checkout's code instead.
- AN OVERLAY IS A DIFF AGAINST A FIXED TREE: it holds only while the production tree stays at
  `844a7f21`, and it depends on the generator and transform staying reproducible from round
  77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.

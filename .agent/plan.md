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

ROUND 94 ADDS THE FLIP'S FIFTH OVERLAY, on top of the first four, under DECISION F275 D64's
method. A task record built without an id mints one, as the classic `Task` did; a task id is
read as a string wherever code parsed it as a `UUID`; the classic `acceptance_checks` list
becomes acceptance text; no pydantic call is made on a task record; and the proposed-task
tests point the data root at their own directory. The diff is carried in consecutive
carriers, so no path under `packages/`, `apps/` or `tests/` moves; the round books the round
93 verdict and its slip.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it: tests
   that still redirect the classic store's `_DATA_DIR`; handlers resolving a minted job id no
   store holds; the pydantic calls made on a `JobPlan`, such as `model_dump_json`; the mission
   end-to-end fixture that never reaches its decision job; what is left of the classic runner
   under `job resume`; and duck-typed test doubles, such as the `_FakeJob` behind a ruled site
   in `packages/orchestration/project_registry.py`.
2. THE FLIP: the transform, then every overlay in round order, landed as a series of commits
   each under the 500-insertion cap inside one round, carrying DECISION F275 D48's obligations
   and registering the structured acceptance form DECISION F275 D22 leaves to it, unless the
   operator allows one more oversized commit.
3. Then the classic store, with the which-store branches and adapters the overlays leave
   unreached, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: many test nodes still fail in the flipped tree.
- AN OVERLAY IS A DIFF AGAINST A FIXED TREE: it holds only while the production tree stays at
  `844a7f21`, and it depends on the generator and transform staying reproducible from round
  77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.

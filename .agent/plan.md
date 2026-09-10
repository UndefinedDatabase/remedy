# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE.

## Current Step

ROUND 34 finishes the classic runner's COMMAND SURFACE. DECISION F275 D19 amends D18: the
`--unattended` and `--yes` flags are INHERITED by `job.resume` rather than lost, because
losing them would delete F114's cost-preview contract along with them. So `job.resume` gains
both flags and the `is_expensive` mark, and the `job.run` entry, its dispatch line and all
its advertisements are then retired. The handler `_cmd_job_run_cycles` survives as the
internal execution path behind the one remaining door.

## Next Steps

1. The flip DECISION F275 D17 sized, as the one declared-oversize commit AGENTS.md permits
   per feature, re-deriving the site set at its own base.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — together with the
   classic store, which is the same commit range by that decision's own terms.
3. DECISION F260 D3, the deletion paragraph naming every deleted module and the feature that
   inherited its idea, which T001 still owes.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- A catalog id that is a PREFIX of a model attribute cannot be migrated by substring. Round
  34 proved this on `job.run` against `job.run_refs` and `job.run_manifest_*`; the token-safe
  regex is recorded in that round's block and in `.agent/prose_slips.md`.
- The open set is 87 by distinct id at this round's base `bc77c7ac`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.

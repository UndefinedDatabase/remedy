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

ROUND 48 finishes the id-shape migration DECISION F275 D26 placed before the flip.
`Artifact.task_id` and `PatchIntentSet.task_id` become `str` in ONE commit, because
`derive_patch_intents` assigns the first to the second and widening either alone leaves the
two spellings straddling that assignment. With round 47's `TaskExecutionContext`, all four
fields the flip feeds now hold one spelling. The reviewer measured the result at
`05631ba3`: 18371 passed, the base's own figure.

## Next Steps

1. RE-RUN THE FLIP DRY RUN against a tree whose id shape is one spelling, and re-classify
   the residue `.agent/f275_t003_flip_residue.md` records at 2714 failures. The 256
   hexadecimal-UUID failures and the 369 model-validation failures should be gone; the
   remaining classes — 867 splat constructions, 493 attribute errors, 271 path operands —
   are transform rules and are enumerated in section 3 of that artefact.
2. THE FLIP itself, still as the one declared-oversize commit AGENTS.md permits per
   feature, declared with its inseparability reason before review.
3. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 stands at 48 rounds and 19 sessions against the operator's soft limit of 60 rounds
  and 20 sessions. The NEXT session is the twentieth and owes a scope report under
  amend0908-f275-finish rule 1, which also forbids the split-and-close default here.
- A dry run of a change this size must be COMMITTED inside its worktree before its suite is
  read: `tests/ui_contracts/test_ux_quality.py` asks the repository for its own changed-file
  count and a dirty worktree reddens it. DECISION F275 D28 records the instance.
- The open set is 86 by distinct id. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's, per DECISION F272 D12.

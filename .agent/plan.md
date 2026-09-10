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

ROUND 41 performs the WIDEN DECISION F275 D22 ruled: `TaskEntry` gains `output_artifact_ids`
and a per-task `budget`, both carried symmetrically through `_export_job` and `_import_job`,
with a test class pinning the defaults, the round trip through `json.dumps`, the defaulted
read of a record written before this round, and the real writer and reader. It is green by
construction — nothing reads the new fields yet — and it takes 427 lines out of the flip.

## Next Steps

1. The flip itself, applied from the round 36 site enumeration, the round 38 seam list and
   the round 40 task-pair list, as the one declared-oversize commit AGENTS.md permits per
   feature, with the inseparability reason AND the real size stated in the handback BEFORE
   review. It registers `Task.acceptance_checks`'s structured form as a finding naming the
   feature that owns acceptance criteria, per amend0908-f275-finish rule 4.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take, and each round that
  measures it has found it larger: DECISION F275 D17 sized it at 1766 changed lines, D21 at
  3771 across 263 files, and D22 added a type pair worth 427 more, which this round removes.
- The open set is 86 by distinct id at this round's base `bbede92f`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.

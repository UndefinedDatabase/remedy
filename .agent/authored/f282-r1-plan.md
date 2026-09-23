# Plan — F282 Findings paydown v2

Branch: feature/f282-findings-paydown-v2, cut from `main` at
`b8fa02ba`, the merge commit of pull request 269 (amend0923-selfuse-write).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F282.md`). The open set at the claim is 30 by
distinct id, and the feature file lists every one under a slice.

## Current Step

ROUND 1 claims F282, re-heads the live review record with F263's round 9
verdict, writes the slice list, resolves R-0984 by its hosted reading and
lands T001: `_check_live_review_verdict` reads the last `Gate:` record
through the ledger's own reader (R-0998), with its tests and red proofs.

## Next Steps

1. T002's remaining evidence resolutions — R-1009, R-1043, R-1044, R-0880 —
   with T003, R-1041 in `packages/orchestration/block_lint.py`.
2. T004 and T005, the budget readings: R-1040 and R-1005.
3. T006 to T011 in the feature file's order, several to a round.
4. T012 to T018, then T019 in the closure's consolidation pass.
5. The closure sequence, whose self-use run is R-1008's only proof.

## Risks

T014, T015 and T018 may not fit one round each; what does not fit is
carried by name to the next paydown feature at this closure.

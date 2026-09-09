# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 21 prepares the last deletion instead of performing it. The five redaction names that
seven SURVIVING modules import from the dying `provider_trust.py` — `_scrub_public`,
`_safe_path_label` and the three patterns they read — move BYTE-IDENTICALLY into the new
`packages/common/public_text_redaction.py` under DECISION F275 D10, and nine importers
repoint. Nothing is deleted. The round also discharges R-0862's fix clause with a positive
pin on the human-review routing tier and R-0855's clause on `token_economy.py`, and books
round 20's PASS verdict.

## Next Steps

1. The `provider_trust` / `provider_trust_verification` pair itself, the last component of
   `.agent/f275_deletion_order.md`. Its first commit is a dated DECISION on the self-dogfood
   external-candidate rail, which loses its only entry point when `provider intake-repair`
   dies.
2. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it. That round
   also discharges R-0843, R-0858, R-0859, R-0860 and R-0864.
3. T002, the atomic record flip, alone, because every later commit's size depends on it.
4. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 88 by distinct id at this round's base `3949f3c6`. This round registers
  none and resolves R-0862. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's
  rather than this feature's, per DECISION F272 D12.
- Worst on this round: seven surviving production modules keep a redaction call whose
  definition moves, so a silent breakage removes masking from public strings. The mutation
  red-proof over the moved definition is ordered in full and its STOP condition blocks the
  push.
- The full suite runs SERIALLY in the PRIMARY checkout. A fresh worktree has a cold
  `apps/ui/node_modules` and reddens the vitest foundation test on a first pass only.

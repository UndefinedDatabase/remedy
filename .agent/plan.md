# Plan — amendment amend0923-selfuse-write

Branch: feature/amend0923-selfuse-write, cut from `origin/main` at
`64cffc44`, the merge commit of pull request 268 (F263's closure).

## Goal

Make the self-use track able to DELIVER — its builder gets a write tool,
its per-call timeout fits a real call, and an order file may declare the
budget it needs — and clean the repository root, so reviewer scratch can
neither sit there nor be packaged.

## Current Step

Part 1 is done: R-1043, R-1044 and R-1045 are registered in
`.agent/live_review.md`, and R-1016, R-1035 and R-0829 carry one new
measured evidence sentence each. Next is Part 2A/B, the runner's write
mode and timeout, each with its own red proof.

## Next Steps

1. Part 2 A/B/C/D/E — the self-use fixes, each with a red proof.
2. Part 4 — repo-root hygiene: move the leftovers out, then make them
   impossible in the packer and the integrity gate; closes R-0829.
3. Part 5 — gates, a real package, the pull request and the merge.

## Risks

Part 2E changes a product default and Part 4.4 turns two lenient packer
tests into refusals; every test either touches is listed in the handback.

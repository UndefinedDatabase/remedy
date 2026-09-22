# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 8 books round 7's PASS, resolves R-1036 and records DECISION F278 D7,
repairs R-1037 and R-1038, narrows one handler, marks the last group of
blind handlers, and turns BLE001 on with the ratchet test; T003 is then
complete and every Acceptance line of T2_F278.md has its evidence.

## Next Steps

1. The closure sequence, first half: resolve R-1037 and R-1038, write the
   Built State, run the one checklist pass, the self-use item, and the
   feature's one full suite.
2. The closure sequence, second half: the evidence job and the review
   package, then the rotation, the accepted STATUS line and the PR.

## Risks

None known beyond the closure's own; the frozen count of excused handlers
is 290 and only falls from here.

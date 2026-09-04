# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 18 books round 17's PASS verdict (RECORD17 — the evidence bundle
and review zip, algorithm steps 1-2) and records one reviewer-authoring
slip (SLIPF114R18), then runs the closure commit itself: the `[x]` flip
on docs/roadmap/STATUS.md, the README capability sync, and
`scripts/self_use_queue.json`'s `consumed_by=F114` edit on SU-008 — one
commit, per docs/roadmap/STATUS_closure_protocol.md algorithm step 5.
The pull request follows in this same round.

## Next Steps

None — F114 closes with this round's pull request. The next session
claims the next feature per Rule A5.

## Risks

- The README's derived numerals (the accepted count and the Tier 3
  Done cell) move mechanically the moment STATUS.md flips to `[x]`;
  both are re-derived and edited in the SAME commit as the flip, per
  F112 R30's own lesson (a closure commit that skipped this went red
  on `tests/docs/` and needed a repair commit).
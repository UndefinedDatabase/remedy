# Plan — F043 Explanation layer

Branch: feature/f043-explanation-layer, cut from `main` at `21bfc188`,
the merge commit of pull request 299 (F291 Self-use sources v2).

## Goal

Nothing in the cockpit is jargon without a hand to hold: one catalog
explains every term, one component shows it on hover and focus, an audit
proves no term lacks an entry and no entry is dead, a first-run tour
introduces the shell, and '?' opens the catalog as a searchable panel
(`docs/roadmap/features/T5_F043.md`, DECISIONS F043 D1 to D4).

## Current Step

ROUND 4: book round 3 and register R-1115, record DECISION F043 D4, repair
R-1115, and land the first-run tour on `TourFrame`, the overlay engine the
result tour now shares, with its spotlight, its once-per-browser record
and its relaunch from the Terms panel.

## Next Steps

1. The end-to-end run over the real shell, with the audit read from the
   real page.
2. The closure sequence.

## Risks

Open findings: R-1115, repaired by this round. A term whose defining
feature has not shipped gets no entry until that feature builds it
(DECISION F043 D1 (5)).

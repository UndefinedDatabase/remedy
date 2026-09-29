# Plan — F043 Explanation layer

Branch: feature/f043-explanation-layer, cut from `main` at `21bfc188`,
the merge commit of pull request 299 (F291 Self-use sources v2).

## Goal

Nothing in the cockpit is jargon without a hand to hold: one catalog
explains every term, one component shows it on hover and focus, an audit
proves no term lacks an entry and no entry is dead, a first-run tour
introduces the shell, and '?' opens the catalog as a searchable panel
(`docs/roadmap/features/T5_F043.md`, DECISIONS F043 D1 and D2).

## Current Step

ROUND 2: book round 1, record DECISION F043 D2, and carry the terms to
the right panel's cards, the six plain metrics and the graph's SCRUBBED
badge, with a term inside a button taking no focus and two descendant
rules of the panel's sheet narrowed to direct children.

## Next Steps

1. The token and cost tiles onto the term's tooltip with their breakdown,
   the estimate basis as the basis golden, and the '?' panel.
2. The first-run tour on an overlay card shared with the result tour, with
   skip and never-show kept in local storage.
3. The end-to-end run over the real shell.
4. The closure sequence.

## Risks

Open findings: 0. A term whose defining feature has not shipped gets no
entry until that feature builds it (DECISION F043 D1 (5)).

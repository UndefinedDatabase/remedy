# Plan — F043 Explanation layer

Branch: feature/f043-explanation-layer, cut from `main` at `21bfc188`,
the merge commit of pull request 299 (F291 Self-use sources v2).

## Goal

Nothing in the cockpit is jargon without a hand to hold: one catalog
explains every term, one component shows it on hover and focus, an audit
proves no term lacks an entry and no entry is dead, a first-run tour
introduces the shell, and '?' opens the catalog as a searchable panel
(`docs/roadmap/features/T5_F043.md`, DECISIONS F043 D1 to D3).

## Current Step

ROUND 3: book round 2, record DECISION F043 D3, move the token and cost
tiles' breakdown into their labels' terms, and add the '?' panel with its
search, its Terms button and the place of every entry.

## Next Steps

1. The first-run tour on an overlay card shared with the result tour, with
   skip and never-show kept in local storage, re-launchable from the panel.
2. The end-to-end run over the real shell.
3. The closure sequence.

## Risks

Open findings: 0. A term whose defining feature has not shipped gets no
entry until that feature builds it (DECISION F043 D1 (5)).

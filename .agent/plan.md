# Plan — F043 Explanation layer

Branch: feature/f043-explanation-layer, cut from `main` at `21bfc188`,
the merge commit of pull request 299 (F291 Self-use sources v2).

## Goal

Nothing in the cockpit is jargon without a hand to hold: one catalog
explains every term, one component shows it on hover and focus, an audit
proves no term lacks an entry and no entry is dead, a first-run tour
introduces the shell, and '?' opens the catalog as a searchable panel
(`docs/roadmap/features/T5_F043.md`, DECISION F043 D1).

## Current Step

ROUND 1: claim F043, re-head the live review record, book F291's round 6,
record DECISION F043 D1, and land the catalog, the `Term` component and the
term audit over the live-status pill and the phase timeline, with a render
harness in a real browser.

## Next Steps

1. The terms of the remaining shell surfaces: the metrics bar, the decision
   inbox, the activity feed and its NowCard, the task list and the graph's
   scrubbed banner, with the product's words from the vocabulary page.
2. The first-run tour on an overlay card shared with the result tour, with
   skip and never-show kept in local storage.
3. The '?' panel and the end-to-end run over the real shell.
4. The closure sequence.

## Risks

Open findings: 0. A term whose defining feature has not shipped gets no
entry until that feature builds it (DECISION F043 D1 (5)).

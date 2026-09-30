# Plan — F044 Command palette, keyboard, performance budget

Branch: feature/f044-command-palette, cut from `main` at `33f66862`,
the merge commit of pull request 300 (F043 Explanation layer).

## Goal

One bar reaches everything: the command bar grows a palette over the
write door's commands, a fuzzy jump to any task, the projects and the
help, with a routing rule that sends questions to the chat; one keymap
drives the cockpit from the keyboard; and CI enforces the bundle, first
paint and frame-rate budgets (`docs/roadmap/features/T5_F044.md`,
DECISION F044 D1).

## Current Step

ROUND 1: claim F044, re-head the live review record, book F043's round
9, record DECISION F044 D1, and land the palette's four pure rules (the
fuzzy match, the command list, the routing rule and the node jump)
against the reviewer's tests.

## Next Steps

1. The bar's dropdown sheet: sections, highlighted matches, recent
   items, the jump, projects and help rows, and the tour's palette stop.
2. The commands' execution: argument flows, surfaces, disabled states
   with their reasons, and the route to the chat.
3. The form entries' structured flows: the plan edits and the hunks.
4. The keymap module and its cheat overlay.
5. The three budgets in CI with their recorded numbers.
6. The closure sequence.

## Risks

Open findings: 0.

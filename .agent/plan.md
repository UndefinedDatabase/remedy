# Plan — F044 Command palette, keyboard, performance budget

Branch: feature/f044-command-palette, cut from `main` at `33f66862`,
the merge commit of pull request 300 (F043 Explanation layer).

## Goal

One bar reaches everything: the command bar grows a palette over the
write door's commands, a fuzzy jump to any task, the projects and the
help, with a routing rule that sends questions to the chat; one keymap
drives the cockpit from the keyboard; and CI enforces the bundle, first
paint and frame-rate budgets (`docs/roadmap/features/T5_F044.md`,
DECISIONS F044 D1 to D9).

## Current Step

ROUND 8: book round 7, fix finding R-1116 (a wrong DECISION citation in
two shipped comments), record DECISION F044 D9, and enforce the
first-paint budget (< 1.5s, built bundle, cold) in the `budgets` CI
stage.

## Next Steps

1. The 60fps p95 budget at 200 nodes (trace-metric measured) in CI,
   and the `budgets` stage's wall-clock re-measurement the Chrome
   harness now earns.
2. `docs/system/ci-self-check-v1.md`'s stage and budget tables, then
   the closure sequence.

## Risks

Open findings: 0 (R-1116 fixed same round, Done: at the next gate).
Operator questions open: 0.

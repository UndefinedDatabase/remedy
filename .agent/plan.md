# Plan — F044 Command palette, keyboard, performance budget

Branch: feature/f044-command-palette, cut from `main` at `33f66862`,
the merge commit of pull request 300 (F043 Explanation layer).

## Goal

One bar reaches everything: the command bar grows a palette over the
write door's commands, a fuzzy jump to any task, the projects and the
help, with a routing rule that sends questions to the chat; one keymap
drives the cockpit from the keyboard; and CI enforces the bundle, first
paint and frame-rate budgets (`docs/roadmap/features/T5_F044.md`,
DECISIONS F044 D1 to D8).

## Current Step

ROUND 7: book round 6, record DECISION F044 D8, and enforce the
bundle-size budget (baseline plus 10%) in the `budgets` CI stage.

## Next Steps

1. The first-paint budget (< 1.5s, built bundle, cold) in CI.
2. The 60fps p95 budget at 200 nodes (trace-metric measured) in CI,
   and the `budgets` stage's wall-clock re-measurement the Chrome
   harness earns.
3. `docs/system/ci-self-check-v1.md`'s stage and budget tables, then
   the closure sequence.

## Risks

Open findings: 0. Operator questions open: 0.

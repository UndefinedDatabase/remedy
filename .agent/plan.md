# Plan — F044 Command palette, keyboard, performance budget

Branch: feature/f044-command-palette, cut from `main` at `33f66862`,
the merge commit of pull request 300 (F043 Explanation layer).

## Goal

One bar reaches everything: the command bar grows a palette over the
write door's commands, a fuzzy jump to any task, the projects and the
help, with a routing rule that sends questions to the chat; one keymap
drives the cockpit from the keyboard; and CI enforces the bundle, first
paint and frame-rate budgets (`docs/roadmap/features/T5_F044.md`,
DECISIONS F044 D1 to D10).

## Current Step

ROUND 9: book round 8, record DECISION F044 D10, and enforce the last
of T003's three CI budgets — 60fps p95 at 200 nodes — over a new
committed harness, `apps/ui/perf/`, measured with Chrome's own
`PipelineReporter` trace events rather than a JS-side
`requestAnimationFrame` timer. The `budgets` CI stage's wall-clock,
re-measured with this test included, reads 44.2s against its existing
300s timeout, so the timeout is unchanged.

## Next Steps

1. `docs/system/ci-self-check-v1.md`'s stage and budget tables (all
   three budgets now land: bundle size, first paint, frame-pipeline
   p95), then the closure sequence.

## Risks

Open findings: 0.
Operator questions open: 0.

# Plan — F023 Semantic zoom L0–L3

Branch: feature/f023-semantic-zoom-l0-l3, cut from `main` at `441f4e8e`,
the merge commit of pull request 277 (F020 Node lifecycle & glyph
language).

## Goal

One mental model from organism to evidence: a zoom state machine
{level, focusId} drives L0 to L3 through wheel thresholds with
hysteresis, clicks, breadcrumbs and Escape, with cluster expansion and
the stage-1 performance budget (`docs/roadmap/features/T5_F023.md`).

## Current Step

ROUND 3, THE NAMED PREREQUISITE OF THE L2 RUN DETAIL: book round 2's
PASS, record DECISION F023 D3, and land the read route
`/api/jobs/<job>/task-runs/<task_id>/rounds` with its builder
`packages/orchestration/run_rounds_view.py`, the client path and decoder
`apps/ui/src/api/taskRunRounds.ts`, the `loadTaskRunRounds` door, and
their guards.

## Next Steps

1. T002's second half: the L2 run popover anchored to its node, reading
   the rounds door, with diff, why and rerun buttons that work or say
   honestly when they will.
2. T003: the L3 evidence panel with lazy tabs, deep links, cluster
   expansion, the 500-node performance fixture and the live end-to-end.
3. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

A task that ran twice shows its latest run's rounds only, and the
reviewer's tokens are not recorded by the run report. Open findings: 1,
owned by F285.

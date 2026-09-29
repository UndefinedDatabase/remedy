# Plan — F042 Multi-project cockpit

Branch: feature/f042-multi-project-cockpit, cut from `main` at
`4e643440`, the merge commit of pull request 295 (F041 Artifact preview).

## Goal

Give the daily multi-repo reality a home in the cockpit: a grid of project
cards, a project switcher in the header, and deep links that carry
`?project=` (`docs/roadmap/features/T5_F042.md`, DECISION F042 D1).

## Current Step

ROUND 1: claim F042, re-head the live review record, book F041's round 9,
register R-1107, record DECISION F042 D1, and land T001: the project list
and the per-project summary in `packages/orchestration/project_cockpit.py`
with `/api/projects` and `/api/projects/<id>/summary`.

## Next Steps

1. T002: the client's project context, the loaders keyed by project, the
   header switcher and the switch-mid-fetch fixtures.
2. T003: the home grid, the cards, the empty and single-project states,
   deep links and the end-to-end run.
3. The closure sequence.

## Risks

Open findings: 1 (R-1107, owned by F290).

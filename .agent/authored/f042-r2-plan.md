# Plan — F042 Multi-project cockpit

Branch: feature/f042-multi-project-cockpit, cut from `main` at
`4e643440`, the merge commit of pull request 295 (F041 Artifact preview).

## Goal

Give the daily multi-repo reality a home in the cockpit: a grid of project
cards, a project switcher in the header, and deep links that carry
`?project=` (`docs/roadmap/features/T5_F042.md`, DECISION F042 D1).

## Current Step

ROUND 2: book round 1, record DECISION F042 D2, and land T002's seam: the
server's `/api/jobs/<id>/project`, the pure client module
`apps/ui/src/api/projectScope.ts` with its switch gate, and the project
doors in `apps/ui/src/api/remedyApi.ts`, against the reviewer's tests.

## Next Steps

1. Mount the seam: the project provider in `RemedyApp.tsx`, the shell
   re-keyed by project and job, and the header switcher.
2. T003: the home grid, the cards, the empty and single-project states,
   deep links and the end-to-end run.
3. The closure sequence.

## Risks

Open findings: 1 (R-1107, owned by F290).

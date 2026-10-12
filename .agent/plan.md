# Plan — F206 Repo dependency catalog

## Goal
A hand-written catalog of the operator's repositories says which depends on which; Remedy
validates it, shows a cycle's path, orders an order's jobs over several repositories by it and
cites the edge, warns when a lockfile shows an edge the catalog lacks, and offers
`remedy project catalog-check` and `remedy project catalog-show`
(docs/roadmap/features/T13_F206.md; DECISIONS F206 D1 to D4).

## Current Step
Round 3 on `feature/f206-repo-dependency-catalog`, session 1: book round 2 and the resolution of
R-1253, DECISIONS F206 D3 and D4; the structural step that moves the `project` group to
`apps/cli/command_catalog_project.py`; T003, the lockfile plausibility check; and T004, the two
commands with their handler, tests and the user page.

## Next Steps
1. The closure sequence per docs/roadmap/STATUS_closure_protocol.md: the closure's one full
   suite and the self-use item, then the evidence and the review package, then the STATUS line.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- `apps/cli/command_catalog.py` is a row of the structure page and may not grow; the commands
  live in the `project` group's own module (DECISION F206 D4).
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).

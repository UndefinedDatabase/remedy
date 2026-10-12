# Plan — F206 Repo dependency catalog

## Goal
A hand-written catalog of the operator's repositories says which depends on which; Remedy
validates it, shows a cycle's path, orders an order's jobs over several repositories by it and
cites the edge, warns when a lockfile shows an edge the catalog lacks, and offers
`remedy org catalog-check` and `remedy org catalog-show`
(docs/roadmap/features/T13_F206.md; DECISIONS F206 D1 and D2).

## Current Step
Round 2 on `feature/f206-repo-dependency-catalog`, session 1: book round 1 and R-1253, DECISION
F206 D2, and T002 — the jobs of an order over several projects follow the catalog's order and
each edge is cited — with the repair of R-1253.

## Next Steps
1. T003: the lockfile plausibility check.
2. T004: the structural step in `apps/cli/command_catalog.py`, then the `org` group with
   `catalog-check` and `catalog-show`, and the user page.
3. The closure sequence per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; R-1253 by F206.
- `apps/cli/command_catalog.py` and `_add_command_args` are rows of the structure page and may
  not grow; T004 makes room first.
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).

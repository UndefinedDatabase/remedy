# Plan — F206 Repo dependency catalog

## Goal
A hand-written catalog of the operator's repositories says which depends on which; Remedy
validates it, shows a cycle's path, orders an order's jobs over several repositories by it and
cites the edge, warns when a lockfile shows an edge the catalog lacks, and offers
`remedy org catalog-check` and `remedy org catalog-show`
(docs/roadmap/features/T13_F206.md; DECISION F206 D1).

## Current Step
Round 1 on `feature/f206-repo-dependency-catalog`, session 1: claim F206, re-head the finding
ledger and book F305's round 5, DECISION F206 D1 with the feature file's amendment, and T001 —
`packages/orchestration/repo_catalog.py` with its tests and the data root's `org` class.

## Next Steps
1. T002: the planner coupling in `packages/orchestration/do_targets.py`, the edges cited in the
   init step's detail and each job's order text.
2. T003: the lockfile plausibility check.
3. T004: the structural step in `apps/cli/command_catalog.py`, then the `org` group with
   `catalog-check` and `catalog-show`, and the user page.
4. The closure sequence per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- `apps/cli/command_catalog.py` and `_add_command_args` are rows of the structure page and may
  not grow; T004 makes room first.
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).

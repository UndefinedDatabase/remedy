# Plan — F206 Repo dependency catalog

## Goal
A hand-written catalog of the operator's repositories says which depends on which; Remedy
validates it, shows a cycle's path, orders an order's jobs over several repositories by it and
cites the edge, warns when a lockfile shows an edge the catalog lacks, and offers
`remedy project catalog-check` and `remedy project catalog-show`
(docs/roadmap/features/T13_F206.md; DECISIONS F206 D1 to D4).

## Current Step
Round 4 on `feature/f206-repo-dependency-catalog`, session 1, the closure's first round: book
round 3 with R-1254, R-1255 and R-1256, repair all three, the checklist's consolidation pass,
the closure's self-use item run to its approval gate, and the feature's one full suite with its
CPU cost.

## Next Steps
1. The evidence bundle and the review package, after the reviewer books round 4.
2. The closing round: the Built State, the rotation, the STATUS line with the README sync, and
   the pull request.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- `apps/cli/command_catalog.py` is a row of the structure page and may not grow; the commands
  live in the `project` group's own module (DECISION F206 D4).
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).

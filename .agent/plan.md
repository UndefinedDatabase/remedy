# Plan — F206 Repo dependency catalog

## Goal
A hand-written catalog of the operator's repositories says which depends on which; Remedy
validates it, shows a cycle's path, orders an order's jobs over several repositories by it and
cites the edge, warns when a lockfile shows an edge the catalog lacks, and offers
`remedy project catalog-check` and `remedy project catalog-show`
(docs/roadmap/features/T13_F206.md; DECISIONS F206 D1 to D4).

## Current Step
Round 5 on `feature/f206-repo-dependency-catalog`, session 1, the closure's evidence round: book
round 4, the resolutions of R-1254, R-1255 and R-1256 and the recurrence of R-1252, then the
staging reclaim, the evidence job and the review package on the accepted head.

## Next Steps
1. The closing round: the Built State, the rotation, the self-use entry's `consumed_by`, the
   STATUS line with the README sync, and the pull request, left unmerged.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).

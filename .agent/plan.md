# Plan — F206 Repo dependency catalog

## Goal
A hand-written catalog of the operator's repositories says which depends on which; Remedy
validates it, shows a cycle's path, orders an order's jobs over several repositories by it and
cites the edge, warns when a lockfile shows an edge the catalog lacks, and offers
`remedy project catalog-check` and `remedy project catalog-show`
(docs/roadmap/features/T13_F206.md; DECISIONS F206 D1 to D4).

## Current Step
Round 6 on `feature/f206-repo-dependency-catalog`, session 1, the closing round: book round 5,
the Built State, the ledger's rotation, F206 accepted in STATUS with the README sync and the
self-use entry `SU-058`'s `consumed_by`, and the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F206's pull
   request, then the next feature's first commit books round 6's verdict.
2. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci); the local evidence in
  the pull request's body is the record.

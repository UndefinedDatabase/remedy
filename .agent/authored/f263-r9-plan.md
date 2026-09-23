# Plan — F263 Human-change absorption (absorb)

Branch: feature/f263-human-change-absorption, cut from `main` at
`54a23101`, the merge commit of pull request 267 (F279's closure).

## Goal

A human who edits the target repository while a job runs is the authority:
the edit is detected, certified into the job's evidence as a human change
record, and the job re-bases onto it instead of failing on drift
(`docs/roadmap/features/T2_F263.md`, DECISION D-E).

## Current Step

ROUND 9 closes F263. It books round 8's PASS, rotates the finding ledger
into its archive, accepts F263 in `docs/roadmap/STATUS.md` with the README's
pinned counts and the self-use item's `consumed_by` in the same commit, and
opens the pull request, which this session never merges.

## Next Steps

1. The next session's Open PR Gate merges this pull request, then Rule A5
   claims the first unchecked feature in `docs/roadmap/STATUS.md`.

## Risks

One suite node that fails only under parallel runs is recorded against
R-0950, and the self-use run's provider timeout against R-1035.

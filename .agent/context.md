# Context — operator amendment amend1027b-v1

## Active Branch
`feature/amend1027b-v1`, from `main` at `dba7a1f62` (no open pull request).

## Scope
Parts A and B of the operator's order of 2026-10-27: three truth defects of the story and the
digest, contract 1.32, Remedy v1 (V1.md, STATUS.md Package 3, README, CHANGELOG 1.0.0) and one
guard in the loop helpers of ~/Repos/system (its own commit there).

## Do not touch
The non-human content policy; ROADMAP.md; the rest of ~/Repos/system.

## Active assumptions
- The operator deleted every job and order of the data root; no old job id exists.
- Rule A5 reads Package 1 only: Package 2 already rests until moved back, Package 3 by this order.

## Constraints
- At most 500 insertions per commit; no leading-slash tokens in commit subjects.
- One full pytest run at the end, then review and repair until green. No measurement series.

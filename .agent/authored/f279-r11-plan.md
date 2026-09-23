# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 11 closes F279. It books round 10's PASS, rotates the finding ledger
into its archive, accepts F279 in `docs/roadmap/STATUS.md` with the README's
pinned counts and the self-use item's `consumed_by` in the same commit, and
opens the pull request, which this session never merges.

## Next Steps

1. The next session's Open PR Gate merges this pull request, then Rule A5
   claims the first unchecked feature in `docs/roadmap/STATUS.md`.

## Risks

Hosted CI first runs the new install steps on this pull request. Two known
flaky suite nodes and the findings R-1040 and R-1041 are carried to F282.

# Plan — F015 Interactive plan editing

Branch: feature/f015-interactive-plan-editing, cut from `main` at
`fce49ce0`, the merge commit of pull request 273 (F267 List commands v2
completion). Pull request 274 into `main` is open.

## Goal

The human reshapes a job's task plan before approving it: six edit
commands, valid only while the plan's approval is open, each revalidated
and logged, reachable through the write channel and `remedy job plan-*`,
and execution follows the edited plan exactly, proven by hash
(`docs/roadmap/features/T5_F015.md`). F015 is accepted in STATUS.

## Current Step

ROUND 10, a repair of pull request 274's hosted CI under the Open PR
Gate: the supervisor tests' `_mark` helper writes its marker under a
private name and renames it into place, so a test never reads a marker
before its text is there (R-1047). Test code only; no production file.

## Next Steps

1. The reviewer gates this round, waits for the pull request's hosted CI
   on the pushed commit, and merges pull request 274 at the Open PR Gate
   when it is green.
2. The next feature's first commit books this round's verdict and
   resolves R-1047, then Rule A5 claims the next feature.

## Risks

Open findings: 5 — R-0499, R-0950, R-1008 and R-1046, owned by F284, and
R-1047, owned by F015 and repaired by this round.

# Plan — F299 Acceptance checks on a repository that is not Remedy's own

## Goal
A mission on a repository that is not Remedy's own gets acceptance checks that can pass there:
they run the project's own test command in the project's own environment, and a project with no
tests is told so instead of being judged red (docs/roadmap/features/T7_F299.md, and DECISIONs
F299 D1 and D2, which fix the order and the shape).

## Current Step
Round 8 on `feature/f299-acceptance-checks-other-repos`, the closure's evidence round: book
round 7 (PASS) with R-1231's resolution; save the evidence script; then the staging reclaim, the
evidence job and the review package on the accepted head.

## Next Steps
1. The closing round: the ledger's rotation, the STATUS line, the README, the self-use entry's
   `consumed_by`, and the pull request, left for the next session's Open PR Gate.

## Risks
- A job's worktree holds no `.venv` and no `node_modules`; the check finds them in the
  repository's own checkout, so a project whose environment lives elsewhere names its command in
  `.remedy/config.toml`.
- A project whose tests are not in a `tests` folder and that has no `test` script reads
  `unchecked` until it names its command.
- A blocking `project_tests` check that finds no command holds no job (DECISION F299 D2 (3)).
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196,
  R-1219, R-1220, R-1225, R-1230 (Low) and R-1160 (Medium) are open, all owned by F297.

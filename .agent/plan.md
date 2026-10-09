# Plan — F299 Acceptance checks on a repository that is not Remedy's own

## Goal
A mission on a repository that is not Remedy's own gets acceptance checks that can pass there:
they run the project's own test command in the project's own environment, and a project with no
tests is told so instead of being judged red (docs/roadmap/features/T7_F299.md, and DECISION
F299 D1, which fixes the order and the shape).

## Current Step
Round 2 on `feature/f299-acceptance-checks-other-repos` (round 1 stopped at its first gate, on the
reviewer's stale reference file): claim F299, book F253's round 38 and round 1, save T001's
measurement as `.agent/f299_inventory.md`, and land T002: the check kind `project_tests`,
its finder module, the environment parameter of the guard's check seam, and the contract's
default check moved onto the new kind.

## Next Steps
1. T003: a criterion state that reads "no check ran" for a project with no test command, its
   words on every surface that shows a criterion, and its push rule, decided and tested.
2. T004: the page under `docs/system/` and the three targets as `remedy do` tests.
3. The closure sequence.

## Risks
- A job's worktree holds no `.venv` and no `node_modules`; the check finds them in the
  repository's own checkout, so a project whose environment lives elsewhere names its command in
  `.remedy/config.toml`.
- A project whose tests are not in a `tests` folder and that has no `test` script is told it has
  no test command until it names one.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196,
  R-1219, R-1220, R-1225 (Low) and R-1160 (Medium) are open, all owned by F297.

# Plan — F299 Acceptance checks on a repository that is not Remedy's own

## Goal
A mission on a repository that is not Remedy's own gets acceptance checks that can pass there:
they run the project's own test command in the project's own environment, and a project with no
tests is told so instead of being judged red (docs/roadmap/features/T7_F299.md, and DECISIONs
F299 D1 and D2, which fix the order and the shape).

## Current Step
Round 9 on `feature/f299-acceptance-checks-other-repos`, the closing round: book round 8, rotate
the ledger, accept F299 in STATUS with the README sync and SU-051's `consumed_by`, and open the
pull request, left unmerged.

## Next Steps
1. The next session's Open PR Gate merges F299's pull request after reading its hosted checks;
   round 9's verdict is booked in the next feature's first commit.
2. Rule A5: the next unchecked line of `docs/roadmap/STATUS.md`.

## Risks
- A job's worktree holds no `.venv` and no `node_modules`; the check finds them in the
  repository's own checkout, so a project whose environment lives elsewhere names its command in
  `.remedy/config.toml`.
- A blocking `project_tests` check that finds no command holds no job (DECISION F299 D2 (3)).
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196,
  R-1219, R-1220, R-1225, R-1230 (Low) and R-1160 (Medium) are open, all owned by F297.

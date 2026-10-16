# Plan — amend1015c (operator order amend1015-final-closure, Remedy's half)

## Goal
Close the face migration on the backend side: Phase A verified with evidence, the defects the
order names repaired with a failing regression test first. Branch feature/amend1015-final-closure,
brought into PR #342's branch feature/amend1015-face-migration by the orchestrator.

## Current Step
Done. D1 (tomli below 3.11), S1 to S3 (ledger steps), D2 (client read scope, interface 1.16), D3
(a failed story offers no retry), D5 (the diff route), D6 (the fake writes its task's deliverable),
D8 (a job at an open question has no diff yet), D9 (a declined job is never applied). E6 and E7
needed no change in Remedy (the story's checking step already says no_test_command).

## Gates (commit 45d80dbfd)
scripts/remedy_test_full.sh (REMEDY_PYTEST_TIMEOUT_SEC=6000): 21299 passed, 11 skipped, 0 failed;
remedy_lint.sh ruff clean; integrity check 6/6; wheel without UI files, fresh venv, remedy
--version prints the commit, HTTP smoke (interface 1.16, 401 without token, 404 unknown job).

## Next Steps
1. After this order: F078 resumes on feature/f078-autonomy-levels.
2. R-1325's resolution of a plain word stays F307's; R-1332 (a blocked job keeps no finish time)
   stays open, pingpong_job.py being a listed file.

## Risks
- .agent/STOP untracked and untouched (decodeux's stop of the autonomous loop).

# Plan — amend1015c (operator order amend1015-final-closure, Remedy's half)

## Goal
Close the face migration on the backend side: verify the Phase A claims with evidence, then repair
the defects the order names, each with a failing regression test first. Branch
`feature/amend1015-final-closure` from `feature/amend1015-face-migration` (PR #342); the
orchestrator brings it into PR #342's branch. No push, no merge, no tag from this worktree.

## Current Step
Gates. Done: D1 (tomli), S1 to S3 (ledger steps), D2 (client read scope, 1.16), D3 (a failed
story offers no retry), D5 (the diff route), D6 (the command line's fake writes its task's
Markdown deliverable). E6 and E7 needed no change (see the handback).

## Next Steps
1. A5/A6: a client token reads only its projects' jobs on every job route (proof, run, orders,
   digest, changes, diff); tests prove it.
2. E2: a retry of a job that ended blocked really runs again, or the story offers no retry;
   R-1332 (a blocked job keeps a finish time) if small.
3. E3: `GET /api/v1/jobs/{job}/diff` (interface 1.16) from git, its twin `remedy client diff`,
   docs (public-http-api-v1, http-clients guide), tests.
4. E5: README.md vs docs/README.md (R-1325): fixture or resolver; narrow fix.
5. E6: budgets enforced in the backend; retry cannot reset them; unknown cost stays null.
6. E7: the story's verification words distinguish no test command / not run / passed / failed.
7. Gates: full pytest, ruff, integrity, structure ratchet, wheel + fresh install + CLI and HTTP smoke.
8. After this order: F078 resumes on `feature/f078-autonomy-levels`; R-1325's resolution of a plain
   word ("die readme" in a repository of several files) stays F307's; R-1332 (a blocked job keeps
   no finish time) stays open, `pingpong_job.py` being a listed file.

## Risks
- `.agent/STOP` untracked and untouched (decodeux's stop of the autonomous loop).
- `public_api.py` and `client_story.py` are near the structure limits; new code goes in new modules.

# Plan — F298 Machine client contract v1.1: what a client can rely on

## Goal
One document generated from the code names every operation, field, word, token and exit code a
program meets when it drives Remedy, and the machine client page is its rendering
(docs/roadmap/features/T12_F298.md, T001). F298 closes at T001's scope; T002 to T007 moved to F304
(DECISION F298 D21).

## Current Step
Session 7, round 30, the Open PR Gate's repair: pull request 315's first hosted run is red on
Python 3.12 in one test assertion (R-1182). Book round 29's verdict, register R-1182, repair the
assertion so that it no longer depends on how one Python version prints source, and push; that
push starts the one re-run (DECISION F298 D24).

## Next Steps
1. Green hosted run: the Open PR Gate merges pull request 315; the next feature's first commit books
   round 30's verdict and resolves R-1182; Rule A5 claims F304 — Machine client contract v1.1, part
   two.
2. Red hosted run: nothing is merged; an operator question is written and the session stops.

## Risks
- T001's sentence that the document only grows inside one major version is a rule for whoever
  changes it; no test holds it.
- R-1182 (Low) is owned by F298 until the hosted run is green. R-1160 (Medium) and R-1138, R-1139,
  R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 (Low) stay open, owned by F297.

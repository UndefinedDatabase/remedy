# Plan — F300 Structure ledger and size ratchet

## Goal
Remedy's structure has a measure, a ledger and a ratchet: a product command that measures any
repository, a page and a test that let each of Remedy's recorded sizes fall and never rise and
refuse a new function or file above the limit, a rule that pays the debts down every fifth
feature, and the first step, `run_job`'s safe points in one function
(docs/roadmap/features/T2_F300.md; DECISIONs F300 D1 and D2).

## Current Step
Round 3 on `feature/f300-structure-ledger-size-ratchet`: book round 2 and resolve R-1232, then
T004 — R-1160's repair with its red-proof in a commit of its own, then `run_job`'s safe points
drawn into one function, `_settle_safe_point`, each commit lowering the ledger's rows and pins it
shrinks.

## Next Steps
1. Closure: the Built State, the checklist consolidation and the self-use item, then the one full
   suite, the evidence package, and the STATUS line with the pull request.

## Risks
- The structural step changes no behaviour and no test's expectation: only the ratchet's pins
  change under `tests/` in its commit.
- The ratchet holds every round: a commit that lengthens a listed function is red until it is cut
  back, so R-1160's repair is written without lengthening `run_job`.
- R-1160 (Medium) is owned by F300; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158,
  R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230 (Low) are owned by F297.

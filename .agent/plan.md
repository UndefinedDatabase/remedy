# Plan — F300 Structure ledger and size ratchet

## Goal
Remedy's structure has a measure, a ledger and a ratchet: a product command that measures any
repository, a page and a test that let each of Remedy's recorded sizes fall and never rise and
refuse a new function or file above the limit, a rule that pays the debts down every fifth
feature, and the first step, `run_job`'s safe points in one function
(docs/roadmap/features/T2_F300.md; DECISIONs F300 D1 and D2).

## Current Step
Round 6 on `feature/f300-structure-ledger-size-ratchet`, the closing round: book round 5, bring
the Built State current with the closure's readings, rotate the ledger, accept F300 in STATUS with
the README sync and SU-052's `consumed_by`, and open the pull request, left unmerged.

## Next Steps
1. The next session's Open PR Gate merges F300's pull request after reading its hosted checks;
   round 6's verdict is booked in the next feature's first commit.
2. Rule A5: the next unchecked line of `docs/roadmap/STATUS.md`.

## Risks
- The ratchet now holds every later round: a change that grows a listed function or adds one
  above 100 lines is red until it is cut back.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297.

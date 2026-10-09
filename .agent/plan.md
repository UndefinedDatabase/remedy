# Plan — F300 Structure ledger and size ratchet

## Goal
Remedy's structure has a measure, a ledger and a ratchet: a product command that measures any
repository, a page and a test that let each of Remedy's recorded sizes fall and never rise and
refuse a new function or file above the limit, a rule that pays the debts down every fifth
feature, and the first step, `run_job`'s safe points in one function
(docs/roadmap/features/T2_F300.md; DECISIONs F300 D1 and D2).

## Current Step
Round 2 on `feature/f300-structure-ledger-size-ratchet`: book round 1 and register R-1232, repair
R-1232 with the tests it names, and land T002 and T003: the ledger page
`docs/system/structure-ledger-v1.md`, the ratchet `tests/test_structure_ratchet.py`, and the
section "The structure rule" of `docs/agents/self_drive_protocol.md`.

## Next Steps
1. T004: R-1160's repair with its red-proof in its own commit, then `run_job`'s safe points drawn
   into one function, its row and the ratchet's pins lowered in the same commit.
2. Closure: the one full suite, the self-use item, the evidence package, the STATUS line.

## Risks
- The ratchet holds every round from here on: a round that grows a listed function or adds one
  above 100 lines is red until it is cut back.
- A structural step changes no behaviour and no test's expectation; R-1160's repair is the one
  behaviour change and lands alone, before it.
- R-1160 (Medium) and R-1232 (Low) are owned by F300; R-1138, R-1139, R-1143, R-1149, R-1156,
  R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230 (Low) are
  owned by F297.

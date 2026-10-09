# Plan — F300 Structure ledger and size ratchet

## Goal
Remedy's structure has a measure, a ledger and a ratchet: a product command that measures any
repository, a page and a test that let each of Remedy's recorded sizes fall and never rise and
refuse a new function or file above the limit, a rule that pays the debts down every fifth
feature, and the first step, `run_job`'s safe points in one function
(docs/roadmap/features/T2_F300.md; DECISION F300 D1 fixes the measure and its limits).

## Current Step
Round 1 on `feature/f300-structure-ledger-size-ratchet`: claim F300, book F299's round 9, save
the claim's measurement as `.agent/f300_inventory.md`, move R-1160 to F300, and land T001, the
module `packages/orchestration/structure_measure.py` and `remedy integrity structure`.

## Next Steps
1. T002 and T003: the ledger page under `docs/system/`, the ratchet test with its record of
   Remedy's sizes, and the rule in `docs/agents/self_drive_protocol.md`.
2. T004: R-1160's repair with its red-proof in its own commit, then `run_job`'s safe points drawn
   into one function and its record lowered.
3. Closure: the one full suite, the self-use item, the evidence package, the STATUS line.

## Risks
- The command reads only; a test proves the measured tree is unchanged.
- A structural step changes no behaviour and no test's expectation; R-1160's repair is the one
  behaviour change and lands alone, before it.
- R-1160 (Medium) is owned by F300; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158,
  R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230 (Low) are owned by F297.

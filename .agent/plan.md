# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval, cut from `main` at the merge of pull request
#218, which closed F037. `.agent/decisions.md` carries the F033 decisions.

## Goal
Surgical consent over changes. Hunks get STABLE content-hash ids, an
`approve_hunks` command applies the approved set atomically to the job branch,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in the viewer, on the node and
in the report. `docs/roadmap/features/T5_F033.md` holds Goal & Done, the task
slicing, the acceptance criteria and the Do-not-touch list.

## Current Step
R1 is the CLAIM AND INVENTORY round. It merges F037's pull request at the Open
PR Gate, cuts this branch, flips F033 to `[~]`, resets this record's header
carrying every finding forward, books the F037 R27 verdict, and puts the F033
source inventory on disk. No production code is touched.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the STATUS claim | ordered | `[ ]` becomes `[~]` |
| C3 the record header and the F037 R27 gate | ordered | record before work |
| C4 the source inventory | ordered | the questions, answered from code |
| C5 the handback | ordered | last commit of the round |

## Next Steps
1. Book the R1 verdict and plan T001 against the inventory.
2. T001 stable-id hashing, the stability property tests, the viewer JSON
   version bump and the shared-helper consolidation with `diff_repair`.
3. T002 the `approve_hunks` command, its validation, subset-apply atomicity
   and the hunk ledger.
4. T003 rejection-to-repair injection, the verbatim-quote trace proof and
   partial-state rendering across viewer, node and report.

## Risks
- T001 moves hunk identity out of `diff_repair`; that module's regression suite
  is the safety net the feature file names in its Orchestrator brief.
- `R-0714` stays open as a documented Medium risk inherited across the reset.

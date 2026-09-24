# Plan — F015 Interactive plan editing

Branch: feature/f015-interactive-plan-editing, cut from `main` at
`fce49ce0`, the merge commit of pull request 273 (F267 List commands v2
completion).

## Goal

The human reshapes a job's task plan before approving it: six edit
commands, valid only while the plan's approval is open, each revalidated
and logged, reachable through the write channel and `remedy plan edit`,
and execution follows the edited plan exactly, proven by hash
(`docs/roadmap/features/T5_F015.md`). Open findings: 4, all owned by F284.

## Current Step

ROUND 1: claim F015 and land T001, the editing backend
`packages/orchestration/plan_editing.py` with its tests, under DECISION
F015 D1.

## Next Steps

1. T002: the write-channel door for the six commands with their argument
   checks, the edit window closed atomically by the approval under the
   plan-edit lock, the approval race and stale-version tests, and
   `remedy plan edit` wrappers; the backend's `ALLOWED_UNWIRED` line goes.
2. T003: the plan's content hash recorded at approval and asserted when
   the job starts, `plan.md` revision goldens, and the end-to-end run of
   an edited plan.
3. The closure sequence.

## Risks

- The approval door and the edit backend must share one lock, or an edit
  can land after an approval read the plan (T002).

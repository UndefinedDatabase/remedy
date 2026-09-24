# Plan — F015 Interactive plan editing

Branch: feature/f015-interactive-plan-editing, cut from `main` at
`fce49ce0`, the merge commit of pull request 273 (F267 List commands v2
completion).

## Goal

The human reshapes a job's task plan before approving it: six edit
commands, valid only while the plan's approval is open, each revalidated
and logged, reachable through the write channel and `remedy job plan-*`,
and execution follows the edited plan exactly, proven by hash
(`docs/roadmap/features/T5_F015.md`). Open findings: 4, all owned by F284.

## Current Step

ROUND 2: book round 1's PASS and land T002's first half under DECISION
F015 D2 — the approval consumed under the plan-edit lock at both doors,
and `remedy job plan-show` with the six `job plan-*` edit commands.

## Next Steps

1. T002's second half: the write door's six plan-edit commands with
   their argument checks, exposed and dispatched through
   `edit_plan`, with their refusals and stale-version conflicts.
2. T003: the plan's content hash recorded at approval and asserted when
   the job starts, `plan.md` revision goldens, and the end-to-end run of
   an edited plan.
3. The closure sequence.

## Risks

None open inside this feature.

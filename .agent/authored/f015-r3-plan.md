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

ROUND 3: book round 2's PASS and land T002's second half under DECISION
F015 D3 — the write door exposes the six `job.plan-*` edits, each run
through `edit_plan` with a required `expected_version`.

## Next Steps

1. T003: the plan's content hash recorded when the approval is consumed
   and asserted when the job starts, the `plan.md` revision goldens, and
   the end-to-end run of an edited plan.
2. The closure sequence.

## Risks

None open inside this feature.

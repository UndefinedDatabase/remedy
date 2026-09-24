# Context — F015 Interactive plan editing

## Active Branch
feature/f015-interactive-plan-editing, cut from `main` at `fce49ce0`
(the merge commit of pull request 273, F267 List commands v2 completion).

## Scope
F015 (Tier 5): the human edits a job's task plan while its approval is
open — edit, delete, reorder, merge and split tasks and edit acceptance
criteria — each edit revalidated, versioned and logged, through the write
channel and `remedy plan edit`, and the executed task set hash-matches the
edited plan, as `docs/roadmap/features/T5_F015.md` specifies. T001 is the
backend, T002 the door and the edit window, T003 execution fidelity.

## Do not touch
Approval semantics, clarification immutability, granularity's automatic
pass and executor scheduling (the feature file's Do-not-touch list).

## Active assumptions
- One edit is one locked transaction on the job record's stored plan,
  revalidated by the planner's own checks, with `_version` and the
  whole-list `_edits` log in the same write (DECISION F015 D1).

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.

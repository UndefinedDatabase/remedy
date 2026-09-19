# Context — F276 Data-root hygiene & disk budget

## Active Branch
feature/f276-data-root-hygiene, cut from `main` at `43d14817` (the merge
commit of pull request 260, F273's closure).

## Scope
F276 (Tier 2). Per `docs/roadmap/features/T2_F276.md`: T001 the class
registry and `remedy data usage`; T002 `remedy data reclaim`, dry run by
default; T003 the copy-mode staging lifecycle; T004 a disk floor that
behaves like every other budget. The feature file's Orchestrator brief
fixes that order.

## Do not touch
F166's evidence retention, and the worktree cleanup path of
`packages/orchestration/pingpong_job.py` ("The ONE cleanup path for a
job-owned worktree"), which already works and is not this feature's to
re-route.

## Constraints
- Never read, list or write the operator's `.data/` by hand: a measurement
  of the real data root is `remedy data usage`, which this feature builds.
  Every test measures a tmp root through `REMEDY_DATA_DIR`.
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff. A resource
  or timing reading belongs to the round that measured it.
- No finding is resolved by deleting a test, weakening an assertion or
  raising a ceiling.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.

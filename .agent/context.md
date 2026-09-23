# Context — F263 Human-change absorption (absorb)

## Active Branch
feature/f263-human-change-absorption, cut from `main` at `54a23101`
(the merge commit of pull request 267, F279's closure).

## Scope
F263 (Tier 2), registered 2026-08-31 by operator order
amend0831-vocab-registrations. T001 detects a human change against the
job's last known state of the target checkout and certifies it into the
job's evidence as a human change record, written before any re-base
(DECISION F263 D1). T002 adds the explicit command `remedy absorb`
(DECISION F259 D1). T003 absorbs at every safe point of a run and before
every apply, and deletes the drift error it replaces (DECISION D-E).

## Do not touch
The approval gate, the scope-fence deny list (F017), and the kill switch's
own safe-point definition: this feature uses the safe points and adds none.

## Active assumptions
- A git target is measured by one tree object taken through a private
  index; a non-git target keeps the existing file-walk guard until T003.
- A human change is never reverted by Remedy, under any circumstance.

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A new module under `packages/` reachable from the entry points is added to
  `tests/orchestration/import_reachability_allowlist.txt` in the same commit.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff.
- No finding is resolved by deleting a test, weakening an assertion or
  raising a ceiling.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.

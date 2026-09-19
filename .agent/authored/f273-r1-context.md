# Context — F273 Findings paydown v1

## Active Branch
feature/f273-findings-paydown-v1, cut from `main` at `80f7c529` (the merge
commit of pull request 259, F271's closure).

## Scope
F273 (Tier 2). Per `docs/roadmap/features/T2_F273.md`: every finding its
slices T001 to T016 name, and every finding its Acceptance names by id, is
repaired as its own text specifies and carries a resolution line with the
evidence that discharged it. The finding text is the spec; where it names a
fix, that fix binds. Operator amendment amend0911-feedback rule B: a
paydown feature's soft limit is 8 sessions; at the limit it closes with what
is resolved and carries the rest to the next paydown feature.

## Do not touch
The 204 process-only resolutions and the 39 fixed ones the 2026-09-06 triage
wrote, the `.agent/prose_slips.md` class lines, and
`.agent/triage_2026-09-06.md` (an audit trail, never rewritten).

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- Destructive verification runs only inside a disposable git worktree
  under `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full
  pytest suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff.
- No finding is resolved by deleting a test, weakening an assertion or
  raising a ceiling; each repair is owed a mutation that now dies.

This feature is NOT UI work — no design-reference binding applies, except
where a T006 round touches `apps/ui/`.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.

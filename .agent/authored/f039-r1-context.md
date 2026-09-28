# Context — F039 Story/replay mode

## Active Branch
feature/f039-story-replay-mode, cut from `main` at `4d60eb84`
(the merge commit of pull request 292, F038 Grounded chat & intent dispatch).

## Scope
F039 (Tier 5): story/replay mode — chapters from the phases and key events
of a job's event ledger, narration cards with autoplay synced to the scrub
position, and one self-contained HTML export, as
`docs/roadmap/features/T5_F039.md` and DECISION F039 D1 specify.

## Do not touch
The cockpit bundle (the export is a subset build), event formats, and the
narration vocabulary sources.

## Active assumptions
- A chapter is a phase the phase bar reads over the whole ledger, and its
  title names the phase, never the outcome (DECISION F039 D1).
- The findings paydown F286 waits behind F039 while no finding is open
  (DECISION F039 D2).

## Constraints
- Every pytest run in a round is targeted and serial; the resource and
  pytest budgets of `tests/regression/test_resource_safety.py` apply.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.

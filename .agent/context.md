# Context — amend0831-vocab-registrations (registration of F259-F266)

## Active Branch
feature/amend0831-vocab-registrations, cut from `origin/main` at `de8a58b1`
(the merge of PR #228, whose red CI this session repaired first).

## Scope
Registration only, per operator order amend0831-vocab-registrations of
2026-08-31. Eight feature detail files under `docs/roadmap/features/` —
`T2_F259.md` vocabulary & concept model, `T2_F260.md` job/execution marriage,
`T2_F261.md` CLI vocabulary v2, `T2_F262.md` list commands v2, `T2_F263.md`
human-change absorption, `T5_F264.md` steering channel, `T5_F265.md` teacher
learning UI v1, `T4_F266.md` `remedy study` — eight `- [ ]` lines in
`docs/roadmap/STATUS.md` Package 1, and the ledger counters moved 258 -> 266.

## Do not touch
Implementing anything the eight files describe. No command is renamed, no job
store is merged, no list gains a flag, no memory card is written. The README's
ACCEPTED count stays 66 — registering a feature accepts nothing. `.agent/STOP`
(untracked, empty) is left exactly where it is. STATUS grammar is unchanged:
every new line is `- [ ] Fxxx — Title`, and no `[~]` was created or altered.

## Assumptions
- The eight ids F259-F266 were unused before this round; verified by grep over
  `docs/roadmap/STATUS.md` and by `remedy plan status --json` reporting
  feature_count 258 with no inconsistencies at the base commit.
- Rule A5 keeps proposing F108: all six amend0830 cost-first lines stand above
  the eight new ones, and the new lines are all `[ ]`.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never
  in the primary checkout, which satisfies `git status --porcelain` empty at
  every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract
  those readers hold over the three state files, so a rewrite is checked
  against it directly: this file carries `## Active Branch`, a `feature/`
  branch name, a roadmap feature id matching `\bF\d{3}\b`, the word `Steps`
  and the word `pytest` (the resource-safety reader); `.agent/plan.md` carries
  `## Goal`, `## Next Steps` and a feature id; `.agent/live_review.md` carries
  `Steps`.
- A new module under `packages/orchestration/` is swept by repo-wide guards
  that name no path: the `REMEDY_DATA_DIR` single-reader invariant, the
  path-utils single-implementation invariant, the bare-`except: pass` ban,
  and the development-artifact boundary.

Constraint specific to this round: a STATUS line's tier is derived from its
enclosing `## Tier <n>` heading, and
`tests/docs/test_docs_consistency.py::TestFeatureLedger::test_the_filename_tier_matches_the_status_tier`
pins it against the `T<tier>_F<id>.md` filename — which is why the eight lines
carry three tier headings rather than sitting bare under the amend0830
cost-first block's `Tier 3` heading.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for this round lives in the `## Current Step` section of
`.agent/plan.md`. This file deliberately does not restate it.

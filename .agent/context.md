# Context — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

## Active Branch
feature/f277-machine-contracts, cut from `main` at `f2494c02` (the merge
commit of pull request 262, F276's closure).

## Scope
F277 (Tier 2), CLOSING AT A SPLIT SCOPE. Per `docs/roadmap/features/T2_F277.md`
as amended by DECISION F277 D10: T001 the event vocabulary and T002 the JSON
envelope and the dispatch error boundary are COMPLETE and are what F277 ships;
T003 the `fail()` helper and the JSON gaps is APPLIED IN PART — the helper and
nine of twenty-eight CLI modules — and its remainder, together with T004 the
exit-code taxonomy and the contract sweep whole, moves to F283. This session's
remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md`, not another slice.

## Do not touch
The event names themselves: this feature declares the vocabulary that exists,
it does not rename it. The catalog's command SET, which F261 owns.
`progress_ledger.py`, which F275 already deleted — its dead reader is history,
not work, and must not be re-created. F283's scope: no further group is
migrated on this branch, because a slice registered to another feature is not
this feature's to spend a closure round on.

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A new module under `packages/` reachable from the entry points must be added
  to `tests/orchestration/import_reachability_allowlist.txt` in the same
  commit, or `tests/orchestration/test_import_reachability.py` goes red.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff. A resource
  or timing reading belongs to the round that measured it.
- The feature ledger is ATOMIC: a `TOTAL_FEATURES` pin, the README counters,
  the STATUS line and the feature file of a registration land in ONE commit.
- No finding is resolved by deleting a test, weakening an assertion or
  raising a ceiling.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.

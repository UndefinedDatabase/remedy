# Context — amend0831-vocab-registrations

## Scope
Registration only. Eight feature detail files under `docs/roadmap/features/`,
eight `- [ ]` lines in `docs/roadmap/STATUS.md` Package 1, and the ledger
counters (`TOTAL_FEATURES` in `tests/docs/test_docs_consistency.py`, the README
accepted line and the README tier-table Total column).

## Explicitly out of scope
Implementing anything the eight files describe. No command is renamed, no job
store is merged, no list gains a flag, no card is written. The README's ACCEPTED
count stays 66 — registering a feature accepts nothing.

## Constraints
- No history rewrite, no force push.
- `.agent/STOP` (untracked, empty) is left exactly where it is.
- STATUS grammar unchanged: every new line is `- [ ] Fxxx — Title`; no `[~]`
  was created or altered.
- Assertions may not be weakened; only pinned expected values move to the new
  truth.

## Current branch context
`feature/amend0831-vocab-registrations`, cut from `origin/main` at `de8a58b1`
(the merge of PR #228, whose red CI this session repaired first).

# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 6
PASSED the reviewer's gate; the round-6 verdict is booked in
`.agent/live_review.md` by round 7's own C2. All four task slices are built.

## Goal

`docs/system/vocabulary.md` is the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
the per-word meaning table, and D2–D10 plus F259 D1/D2 as dated DECISION
paragraphs. `tests/docs/test_vocabulary.py` pins it in planned mode against the
shipped `apps/cli/command_catalog.py`; the same diagram stands in `README.md`,
byte-equal and pinned; the page is registered in `docs/README.md`. No other
code: F259 decides words, F260 and F261 spend them.

## Current Step

Round 7 is the INTEGRATION GATE — the full suite on this branch and at the merge
base 25961794, compared, with every branch-only id attributed, per
docs/agents/integration_gate.md. The base worktree's parity obeys the fix clause
of the open finding R-0736: after copying `apps/ui/dist`, its mtimes are set
newer than the newest file under `apps/ui/src`, because the mtime relation is
what `_frontend_is_stale` reads and content parity alone manufactures 114 false
base failures. `apps/ui/node_modules` is copied with `symlinks=True` so the 23
`.bin` shims are not dereferenced.

## Next Steps

- The closure sequence per docs/roadmap/STATUS_closure_protocol.md: the evidence
  job, a FRESH review zip, the ledger rotation, the §3 checklist consolidation
  pass, the reviewer-authored STATUS line committed last, and the pull request —
  which is NOT merged in this session but at the next feature's Open PR Gate.

## Risks

- A branch-only failure coupled to this feature's code is a blocker and gets its
  own reviewer-gated repair round; the gate round never fixes what it finds.
- The suite is large and both runs are full runs, so this round is the session's
  longest by wall clock.

# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 9
PASSED the reviewer's gate. Round 7 was the integration gate — the full suite
green on the branch and at the merge base, zero branch-only and zero base-only
failures. Rounds 8 and 9 were closure parts 1 and 2; the package is built and
READY_FOR_REVIEW.

## Goal

`docs/system/vocabulary.md` is the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
the per-word meaning table, and D2–D10 plus F259 D1/D2 as dated DECISION
paragraphs. `tests/docs/test_vocabulary.py` pins it in planned mode against the
shipped `apps/cli/command_catalog.py`; the same diagram stands in `README.md`,
byte-equal and pinned; the page is registered in `docs/README.md`. No other
code: F259 decides words, F260 and F261 spend them.

## Current Step

Round 10 is CLOSURE PART 3 — the last round. One commit flips the STATUS line to
accepted, syncs the README's counters and its Tier 2 accepted list, marks the
self-use item consumed and rewrites the handback; it is the last commit on the
branch. Then the pull request is opened and left UNMERGED, which is the
operator's review window.

## Next Steps

- The operator reviews the package at their own pace.
- The next feature's session merges this pull request at its Open PR Gate, then
  claims the next unchecked line in the DECISION amend0905-vocab D12 order,
  which is F260 — one world: mission, job, run.

## Risks

- The README and the STATUS ledger must never disagree in any committed state,
  which is why one commit carries both. A split would leave a state where the
  README claims an acceptance the ledger does not.
- The pull request must not be merged in this session. Merging it here would
  close the operator's review window before it opened.

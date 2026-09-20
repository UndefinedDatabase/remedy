# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`). F277 closes on the first two complete
and the third half applied; DECISION F277 D10 moved the rest to F283, which
is registered and placed directly after F277.

## Current Step

Round 13 is FAIL and round 14 is its repair. Generating the closure's
self-use item wrote a ledger paragraph carrying a retired word into
`scripts/self_use_queue.json`, so the branch tip is red on
`tests/docs/test_retired_promote_word.py`. Round 14 registers that as
`R-1015` and the run's own blocked strings as `R-1016`, lands the
`KEPT_BY_SENSE` stopgap the guard's sense `H` already provides for, and then
runs the integration gate — the full suite ONCE, transcript committed.

## Next Steps

1. Any closure-suite repair the shrinking rule of amend0917 rule 2 orders:
   each repair round strictly shrinks the bad set with no node newly bad, at
   most three, then `xfail(strict=True)` and a follow-up feature for the rest.
2. The evidence job (`create_manual_completion_bundle`, feature-scoped) and a
   FRESH review zip. `base_commit` is the branch's FORK POINT, `f2494c02`,
   and the two `rev-list` counts must agree or the base is wrong.
3. The §3 consolidation pass, where `R-1014`'s fix clause lands merged into
   an existing item and never appended. Then the ledger rotation, then the
   owner re-assignment of every open finding F277 did not resolve.
4. The STATUS `[x]` flip with the README capability sync and the `SU-025`
   `consumed_by` edit in the SAME commit, last on the branch under Rule A4,
   then the pull request.

## Risks

Round 12's mirror commit spent this feature's one permitted oversize commit
at 661 insertions, so every later mirror must stay under 500. Three wrong
expected-insertion counts in two rounds share one cause — a number about the
tree produced by hand — and from round 14 every such number comes from the
script that measures the payload digests.

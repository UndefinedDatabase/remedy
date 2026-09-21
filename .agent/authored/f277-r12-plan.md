# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`). F277 closes on the first two complete
and the third half applied; DECISION F277 D10 moves the rest to F283.

## Current Step

THE SEVEN-SESSION SOFT LIMIT IS REACHED AT ROUND 11 OF 25, on the handoff
chain's own session numbering, so the closure sequence has started. Round 12
books round 11's PASS, records DECISION F277 D10 and the operator question it
owes, registers F283 in one ledger-atomic commit, and gives F277's file the
Built State its closure precondition 4 requires.

## Next Steps

1. The closure preconditions: the self-use item of precondition 6 planned and
   run to the approval gate with its `describe_self_use_run_defects()` output
   registered, `integrity check` green, then the integration gate — the full
   suite ONCE, by the worker, in the primary checkout, its transcript
   committed as `.agent/authored/f277-closure-suite.txt`.
2. Any closure-suite repair the shrinking rule of amend0917 rule 2 orders, at
   most three rounds, then the marks and the follow-up that rule names.
3. The evidence job (`create_manual_completion_bundle`, feature-scoped) and a
   FRESH review zip. `base_commit` is the branch's FORK POINT, `f2494c02`, and
   the two `rev-list` counts must agree or the base is wrong.
4. The §3 consolidation pass, where `R-1014`'s fix clause lands merged into an
   existing item and never appended — the list comes out at 34 items or fewer.
   Then the ledger rotation, then the owner re-assignment of every open finding
   F277 did not resolve.
5. The STATUS `[x]` flip with the README capability sync in the SAME commit,
   last on the branch under Rule A4, then the pull request.

## Risks

Four rounds of this feature lost a number to one cause: a value measured
before an edit and used after it. The counter-measure held in round 11 — every
number in a block came from one script run last — and it stays in force for
the closure, where the evidence pipeline reads a stale digest silently.

# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). F277's STATUS line is
already `[x]` at `3d59a870`; pull request 263 is open and carries the whole
feature.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`). F277 closed on the first two complete
and the third half applied; DECISION F277 D10 moved the rest to F283.

## Current Step

THE CI REPAIR ROUND, ordered by operator amendment amend0820-gate-autonomy:
CI run 35552041486 at `3d59a870` ended RED on both matrix legs, so repairing
this branch is the session's work order and commits on the open pull
request's branch are explicitly allowed for it. One node failed and no other:
`tests/cli/test_worker.py::TestAWorkerRefusalIsShapedLikeTheCaller::test_unload_without_a_target_names_both_flags`,
which reaches F277's `missing_argument` refusal only on a machine that has
`ollama` on PATH. This round books round 18's PASS, registers R-1018 for the
test and R-1019 for the product ordering it uncovered, and pins the probe in
the idiom the same module already uses. No production line changes.

## Next Steps

1. CI re-runs on the push; the gate reads it before anything else.
2. The Open PR Gate merges pull request 263 once the run is green — that
   merge is the next session's first action and it precedes any new branch.
3. Rule A5 then proposes F283, which stands directly behind F277 in the
   ledger, and which now owns R-1019 as well as R-1014.
4. F283's FIRST reviewed round resolves and empties `.agent/candidates.md`,
   which still holds three entries; a non-empty candidates file is a block
   condition at feature-claim time.

## Risks

Twenty-four findings are open after this round's two registrations. R-1018 is
fixed by the same round that registers it, so its `Done:` line is owed to the
first commit of the next round under amend0827 rule 1; it is not lost, and the
handoff names it. R-1019 is deliberately not fixed here: moving the argument
check changes user-visible CLI behaviour and belongs to F283's refusal sweep.

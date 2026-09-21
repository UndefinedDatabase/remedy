# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`). F277 closes on the first two complete
and the third half applied; DECISION F277 D10 moved the rest to F283.

## Current Step

Round 14 is PASS and the integration gate is RED at exactly one node. Round
15 is the first repair round under the shrinking rule of amend0917 rule 2:
`command_discovery_completed` got its writer in round 3 and never got the
matching entry in the UI's humanize catalog, so a Python emitter and a
TypeScript catalog have drifted apart. The repair is one catalog line. The
suite is then re-run and its transcript replaced, on the standing answer to
operator question Q1 — the one run belongs to the code actually shipped.

## Next Steps

1. If the re-run is green, the bad set has shrunk from one to zero with no
   node newly bad and the shrinking rule is satisfied in one round of the
   three it allows. If it is red, round 16 is the second repair round.
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

Round 12's mirror commit spent this feature's one permitted oversize commit,
so every later mirror must stay under 500. Four numerals the reviewer wrote
by hand across three rounds were wrong and the worker caught every one; from
round 14 the tree numbers come from a script, and the one that still slipped
was a count of the block's own prose, which no script reads.

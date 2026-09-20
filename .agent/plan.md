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

The closure sequence is running. Round 13 books round 12's PASS and three
reviewer slips, repairs the one Built State clause that landed inaccurate,
and satisfies closure precondition 6: the self-use queue holds no pending
item, so the generator appends one — a dry run at `4f335b03` shows it would
mint `SU-025` against finding `R-0820` — and the runner takes it to the
normal approval gate under the `self_use` role, which resolves to the
`claude-cli` provider.

## Next Steps

1. Register every string `describe_self_use_run_defects()` returns for the
   run's own plan as a normal R-id finding, with the reviewer authoring the
   text; an empty tuple means nothing to register, not nothing checked.
2. The integration gate: `remedy integrity check --json` at PASS, then the
   full suite ONCE, by the worker, in the primary checkout, its transcript
   committed as `.agent/authored/f277-closure-suite.txt`. Any repair follows
   the shrinking rule of amend0917 rule 2, at most three rounds.
3. The evidence job (`create_manual_completion_bundle`, feature-scoped) and a
   FRESH review zip. `base_commit` is the branch's FORK POINT, `f2494c02`,
   and the two `rev-list` counts must agree or the base is wrong.
4. The §3 consolidation pass, where `R-1014`'s fix clause lands merged into
   an existing item and never appended. Then the ledger rotation, then the
   owner re-assignment of every open finding F277 did not resolve.
5. The STATUS `[x]` flip with the README capability sync and the `SU-025`
   `consumed_by` edit in the SAME commit, last on the branch under Rule A4,
   then the pull request.

## Risks

The block-mirror commit of round 12 spent this feature's one permitted
oversize commit at 661 insertions. Every later round must keep that commit
under 500, and the counter-measure is a smaller payload set, not a second
declaration — a second oversize commit in one feature is a Medium finding.

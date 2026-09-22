# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure); `main`
was merged in again at `5ca50335` (DECISION amend0921-operator-feedback D8).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 22, the closure sequence's first half. It books round 21's PASS and
resolves R-1033, writes the feature file's Built State, folds this feature's
one prose lesson into the reviewer checklist without lengthening it, runs the
closure's self-use item to its approval gate, and runs the feature's one full
suite, committing the transcript.

## Next Steps

1. The closure sequence's second half: register whatever the self-use run's
   own defect reader reports, the evidence job, a fresh review zip, the ledger
   rotation, the STATUS line with the README counters in the same commit, and
   the pull request, which is never merged in the session that opens it.

## Risks

Twenty-five findings are open after this round's resolution and none is this
feature's own. Twenty-two rounds are spent of the soft limit of 25; the
closure's second half is the twenty-third, which leaves two rounds for a
repair the full suite or the packaging may still ask for.

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

ROUND 21. It books round 20's PASS, corrects the round 19 entry's verdict
token and resolves R-1032, registers R-1033 and R-1034, records DECISION F283
D13, lands T002's sweep and the catalog-to-dispatch parity in
`tests/cli/test_json_contract.py`, and makes `stats report --json` answer in
the envelope.

## Next Steps

1. The closure sequence: the Built State and Acceptance of
   `docs/roadmap/features/T2_F283.md`, the evidence job and a fresh review zip,
   the STATUS line, the pull request. Its one full suite runs on the merged
   tree (DECISION amend0921-operator-feedback D1).

## Risks

Twenty-six findings are open after this round's registrations. R-1033 is this
feature's own and its repair lands in this round, to be resolved on the record
at the next gate; R-1034 belongs to the next paydown feature. Twenty-one rounds
are spent of the soft limit of 25, in the fifth of 7 sessions; the closure
must fit the four rounds left.

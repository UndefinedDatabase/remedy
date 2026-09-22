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

ROUND 20. It books round 19's PASS, records DECISION F283 D12 (the exit-code
taxonomy), adds `apps/cli/exit_codes.py` and the catalog's `exit_codes` field
with its test, writes the guide `docs/guides/exit-codes.md`, and makes
`job resume --checkpoint` refuse where it did not resume.

## Next Steps

1. T002's sweep: `tests/cli/test_json_contract.py`, in which every
   `supports_json` command reachable without a positional argument answers a
   parseable envelope on success and on an invalid argument, and
   catalog-to-dispatch parity is asserted.
2. The closure sequence, whose one full suite runs on the merged tree.

## Risks

Twenty-four findings are open and none is this feature's own. Twenty rounds
are spent of the soft limit of 25, in the fifth of 7 sessions; the sweep and
the closure must fit the five rounds left.

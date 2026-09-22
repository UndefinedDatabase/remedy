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

ROUND 19. It books round 18's PASS, resolves R-1031 on the record, records
DECISION F283 D11, pins `patch revert`'s failure token, and converts the last
six modules' success documents to the envelope under DECISION F283 D10:
`job`, `mission`, `self`, `project`, `config` and `worker`.

## Next Steps

1. T002's last slice: the exit-code taxonomy under `docs/guides/` asserted
   from the catalog, catalog-to-dispatch parity, and the sweep in
   `tests/cli/test_json_contract.py`.
2. The closure sequence, whose one full suite runs on the merged tree.

## Risks

Twenty-four findings are open and none is this feature's own. Nineteen rounds
are spent of the soft limit of 25, in the fourth of 7 sessions; the sweep and
the closure must fit the six rounds left.

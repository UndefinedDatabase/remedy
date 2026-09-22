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

ROUND 18. It books round 17's PASS, registers and repairs R-1031, resolves
R-1030 on the record, and converts the success documents of eight modules to
the envelope under DECISION F283 D10: `runtime`, `do`, `test`, `event`,
`memory`, `patch`, `stats` and `brain`.

## Next Steps

1. T002's success half, last batch: `job`, `mission`, `self`, `project`,
   `config` and `worker`, leaving the ratchet at the text-branch survivors.
2. T002's last slice: the exit-code taxonomy under `docs/guides/` asserted
   from the catalog, catalog-to-dispatch parity, and the sweep in
   `tests/cli/test_json_contract.py`.
3. The closure sequence, whose one full suite runs on the merged tree.

## Risks

Twenty-five findings are open and one of them, R-1031, is this feature's own.
Eighteen rounds are spent of the soft limit of 25, in the fourth of 7
sessions; the closure needs its own rounds, so the last batch and the sweep
must each fit one round.

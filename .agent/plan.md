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

ROUND 17. It books round 16's PASS, registers and repairs R-1030, pins what
round 16's review found unpinned, records DECISION F283 D10 and lands its
ratchet, then converts the success documents of twenty of the smaller command
modules to the envelope.

## Next Steps

1. T002's success half, second batch: the fourteen modules with the most
   raw-document sites, `job`, `mission`, `self`, `project`, `config`,
   `worker`, `brain`, `do`, `test`, `runtime`, `event`, `memory`, `patch` and
   `stats`, leaving the ratchet at the text-branch survivors.
2. T002's last slice: the exit-code taxonomy under `docs/guides/` asserted
   from the catalog, catalog-to-dispatch parity, and the sweep in
   `tests/cli/test_json_contract.py`.
3. The closure sequence, whose one full suite runs on the merged tree.

## Risks

Twenty-five findings are open and one of them, R-1030, is this feature's own.
Seventeen rounds are spent of the soft limit of 25, in the fourth of 7
sessions; the closure needs its own rounds, so the second batch and the sweep
must each fit one round.

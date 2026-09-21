# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 13. It books round 12's PASS and records DECISION F283 D8. Then, one
commit each: `runtime_cmd.py`'s `_fail` is replaced by refusals through
`fail()` keyed on the error class; and its four result-shaped failure exits
answer one envelope under `--json`.

## Next Steps

1. T001's catalog half: the read-only commands without `supports_json`, and
   the catalog test asserting that set is empty.
2. T002: success envelopes, the exit-code taxonomy under `docs/guides/`, and
   `tests/cli/test_json_contract.py`'s sweep.
3. The closure sequence.

## Risks

Twenty-two findings are open and none is this feature's own. Thirteen rounds
are spent of the soft limit of 25, in the third of 7 sessions; the
success-envelope half of T002 is the largest piece left, and the runtime
suites flake under xdist, so they run serially.

# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 12. It books round 11's PASS and records DECISION F283 D7. Then, one
commit each: the `patch`, `snapshot`, `real_test_execution` and `self`
refusals move onto `fail()`; `config`, `project current`, `mission run` and
the cost-preview confirmation follow under D7; and the three `stats`
refusals round 11 left unpinned gain their tests.

## Next Steps

1. `runtime_cmd.py`, its own round.
2. T001's catalog half: the read-only commands without `supports_json`, and
   the catalog test asserting that set is empty.
3. T002: success envelopes, the exit-code taxonomy under `docs/guides/`, and
   `tests/cli/test_json_contract.py`'s sweep.

## Risks

Twenty-two findings are open and none is this feature's own. Twelve rounds
are spent of the soft limit of 25, in the third of 7 sessions; the
success-envelope half of T002 is the largest piece left.

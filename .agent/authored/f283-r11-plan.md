# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 11. It books round 10's PASS and resolves R-1026. Then, one commit
each: the `stats` refusals in `stats_ledger_cmd.py`, `bench_cmd.py` and
`failure_stats_cmd.py` move onto `fail()`, the exiting helpers taking the
caller's `json_output`; `job stop`'s refusals do the same; and the two
refusals round 10 left untested gain their tests.

## Next Steps

1. The rest of the tail: `patch`, `config`, `real_test_execution`,
   `snapshot`, `self`, `worker_facade`, the cost-preview confirmation, and
   the unprefixed refusals of `--json` handlers.
2. `runtime_cmd.py`, its own round.
3. T001's catalog half: the read-only commands without `supports_json`, and
   the catalog test asserting that set is empty.
4. T002: success envelopes, the exit-code taxonomy under `docs/guides/`, and
   `tests/cli/test_json_contract.py`'s sweep.

## Risks

Twenty-two findings are open after this round's booking and none is this
feature's own. Eleven rounds are spent of the soft limit of 25, in the third
of 7 sessions; the success-envelope half of T002 is the largest piece left.

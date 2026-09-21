# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 10. It books round 9's PASS, registers R-1026 and records DECISIONs
F283 D5 and D6. Then, one commit each: `remedy do --json` answers in one
envelope, a failed walk carrying its result document (D5); the parser's usage
refusals in `apps/cli/grouped.py` answer in the envelope under `--json` (D6);
the `test` group's refusals move onto `fail()`; and the three refusals R-1026
names pass `job_not_found`.

## Next Steps

1. The tail of the refusal sweep: `patch`, `config`, `real_test_execution`,
   `ui`, `self`, `decision`, `snapshot`, `worker_facade`, the cost-preview
   confirmation, the `stats`, `bench`, `failure_stats` and `job stop`
   `SystemExit` sites, and the unprefixed refusals of `--json` handlers.
2. `runtime_cmd.py`, its own round.
3. T001's catalog half: the read-only commands without `supports_json`, and
   the catalog test asserting that set is empty.
4. T002: success envelopes, the exit-code taxonomy under `docs/guides/`, and
   `tests/cli/test_json_contract.py`'s sweep.

## Risks

Twenty-three findings are open after this round's booking, one of them this
feature's own (R-1026, repaired in this round). Ten rounds are spent of the
soft limit of 25, in the third of 7 sessions; the success-envelope half of
T002 is the largest piece left.

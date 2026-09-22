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

ROUND 14. It books round 13's PASS and a prose slip, and records DECISION
F283 D9. Then T001's catalog half begins: `init run`, `dev status`, `dev
smoke-help`, the `memory` store and card commands, `blocker resolve` and the
three `patch` commands declare `supports_json` and answer in the envelope, and
a ratchet pins the commands still missing it.

## Next Steps

1. The catalog half's second group: `decision resolve`, `decision explain`,
   `job plan` and the seven `brain` commands.
2. The catalog half's last group: the five `ui` and five `project` commands,
   with the ratchet asserting the set empty.
3. T002: success envelopes, the exit-code taxonomy under `docs/guides/`, and
   `tests/cli/test_json_contract.py`'s sweep.
4. The closure sequence, whose one full suite runs on the merged tree.

## Risks

Twenty-four findings are open and none is this feature's own. Fourteen rounds
are spent of the soft limit of 25, in the fourth of 7 sessions; T002's success
half is the largest piece left, and the runtime suites flake under xdist, so
they run serially.

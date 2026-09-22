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

ROUND 16. It books round 15's PASS and a prose slip, pins what round 15's
review found unpinned, and lands the catalog half's last group under DECISION
F283 D9: the five `ui` and five `project` commands declare `supports_json` and
answer in the envelope, and the ratchet asserts the read-only set is empty.
T001 is then complete.

## Next Steps

1. T002: success envelopes for the `supports_json` commands that still print a
   raw document, the exit-code taxonomy under `docs/guides/`, and
   `tests/cli/test_json_contract.py`'s sweep.
2. The closure sequence, whose one full suite runs on the merged tree.

## Risks

Twenty-four findings are open and none is this feature's own. Sixteen rounds
are spent of the soft limit of 25, in the fourth of 7 sessions; T002's success
half is the largest piece left, and the runtime suites flake under xdist, so
they run serially.

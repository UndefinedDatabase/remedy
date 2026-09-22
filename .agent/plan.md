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

ROUND 24, the closure. It books round 23's PASS, rotates the finding ledger as
its own commit, then flips the STATUS line to accepted with the README's three
pinned places and the self-use entry's `consumed_by` in that same commit, and
opens the pull request, which this session never merges.

## Next Steps

1. Nothing on this branch. The pull request waits for the operator's review
   window and is merged at the next feature's Open PR Gate; the next session
   claims the next unchecked feature under Rule A5.

## Risks

Twenty-six findings are open and none is this feature's own. Twenty-four rounds
are spent of the soft limit of 25, and the work left after this round is the
merge, which belongs to another session.

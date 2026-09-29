# Plan — F291 Self-use sources v2

Branch: feature/f291-self-use-sources-v2, cut from `main` at
`aa5defde`, the merge commit of pull request 298 (F042 Multi-project cockpit).

## Goal

Give the self-use generator two sources that almost always have real work,
so a closure's self-use reading is rarely "queue exhausted"
(`docs/roadmap/features/T5_F291.md`, DECISION F291 D1).

## Current Step

ROUND 1: claim F291, re-head the live review record, book F042's round 11,
record DECISION F291 D1, and land T001 (Tier 4, the excused blind
handlers) and T002 (Tier 5, the test-less modules) against the reviewer's
tests, with the generator's half of T003.

## Next Steps

1. The run half of T003: a Tier 4 item run to the approval gate under the
   default budget by a test, and both tiers documented in
   `docs/system/self-use-track-v1.md` and the closure protocol.
2. The closure sequence: Built State, the self-use run, the one full suite,
   the evidence bundle and the pull request.

## Risks

Open findings: 0.

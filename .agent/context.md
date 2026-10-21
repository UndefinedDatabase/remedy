# Context — F303 The face on the public API

## Active Branch
`feature/f303-face-public-api`, from `main` at `2621bbe2e` (the merge commit of pull request 375,
which carried F060).

## Scope
F303 (Tier 12), as `docs/roadmap/features/T12_F303.md`, narrowed by DECISION amend1016 D2 to the
public API, and DECISION F303 D1 state it: the inventory, the contract's proofs, the steering-note
route (R-1329), and the MCP facet of DECISION F253 D1.

## Do not touch
F253's binding shape and security constraints. No page, bundle, static file or browser test is
added to this repository (DECISION amend1016 D2). The socket's command door stays as it is.

## Active assumptions
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
- No file under `.agent/` gains this machine's absolute paths; the commit hook refuses them.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.

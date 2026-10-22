# Context — F113 Local models for side roles

## Active Branch
`feature/f113-local-side-roles`, from `main` at `3af211790` (the merge commit of pull request 378,
which carried F296).

## Scope
F113 (Tier 3), as `docs/roadmap/features/T3_F113.md` and DECISION F113 D1 state it: named local
endpoints for the cheap-tier side roles, the refusal of every core role, the fallback, the quality
gate with its flip, and the cost basis `local_zero`.

## Do not touch
Core-role routing and its shipped defaults; model downloads and management; GPU or host
provisioning; F058's failover walk.

## Active assumptions
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation.
- No test reaches a live model server: every probe and call in the tests goes to a fake client.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
- No file under `.agent/` gains this machine's absolute paths; the commit hook refuses them.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.

# Context — F074 Estimate calibration

## Active Branch
`feature/f074-estimate-calibration`, from `main` at `148a1c386` (the merge commit of pull request
379, which carried F113).

## Scope
F074 (Tier 3), as `docs/roadmap/features/T3_F074.md` and DECISION F074 D1 state it: per task class
and role distributions from the cost ledger, the sample floor, the damping, the snapshot, the shared
estimator's source swap in its three consumers, and the trust view.

## Do not touch
The S, M, L and XL band vocabulary; consumer behaviour below the floor; the pricing tables and the
price basis.

## Active assumptions
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation.
- The measurement never writes the ledger; the only file it writes is the snapshot beside it.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; edits there stay line-neutral.
- No file under `.agent/` gains this machine's absolute paths; the commit hook refuses them.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.

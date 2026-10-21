# Context — F307 Findings paydown v9

## Active Branch
`feature/f307-findings-paydown-v9`, from `main` at `eeed13064` (the merge commit of pull request
376, which carried F303).

## Scope
F307 (Tier 2), the ninth rolling findings paydown, as `docs/roadmap/features/T2_F307.md` and
DECISION F307 D1 state it: 85 of the 88 open findings, in 21 slices; the finding text is the spec.

## Do not touch
The resolutions earlier paydowns landed; the record is append-only.

## Active assumptions
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
- No file under `.agent/` gains this machine's absolute paths; the commit hook refuses them.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.

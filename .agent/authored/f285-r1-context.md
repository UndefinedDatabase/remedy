# Context — F285 Findings paydown v4

## Active Branch
feature/f285-findings-paydown-v4, cut from `main` at `83d3bb95`
(the merge commit of pull request 281, F026 Task edit at runtime).

## Scope
F285 (Tier 2, the rolling findings paydown): R-1058's Acceptance and
defect check (T001), R-1057's derived self-use cost cap (T002), R-1055's
provider-session resume across a relaunch (T003), R-1064 as the
closure's self-use item, and R-1008 through that run, as
`docs/roadmap/features/T2_F285.md` and DECISION F285 D1 specify.

## Do not touch
The resolutions F284 landed; the record is append-only.

## Active assumptions
- The self-use track is repaired before the closure uses it, and the
  closure's self-use run is aimed at R-1064 (DECISION F285 D1).

## Constraints
- Every pytest run in a round is targeted and serial; the resource and
  pytest budgets of `tests/regression/test_resource_safety.py` apply.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.

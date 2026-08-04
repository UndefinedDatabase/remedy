# Context — F075 MILESTONE GATE: 10 flawless self-runs

## Active Branch
feature/f075-self-run-gauntlet (from main after the Open PR Gate
merged PR #178, the F071 closure)

## Scope
Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
harness + evaluator + matrix report + frozen ten-order set + their
tests. The harness adds no product code paths; product fixes found
by the campaign go through normal orders with their own tests.

## Constraints
- Round gate = scoped pytest command(s) authored in the step
  block; canary per handback:
  python3 -m pytest tests/cli/test_golden_path.py -q. Docs-round
  gate applies to any commit touching docs/roadmap/**:
  python3 -m pytest tests/docs/ -q. Full-suite pytest -n auto only
  at the integration gate; the resource-safety rules of
  tests/regression apply.
- Commits < 500 lines; authored texts applied byte-exact from
  .agent/authored/f075-r1-<n>.md after sha256 verification.
- Gauntlet runs use an ISOLATED data root, never the operator's
  real one; gate run logs live outside the repo during a run
  (docs/agents/integration_gate.md, R-0176).
- Do-not-touch: the pass definition once frozen, config defaults
  by machine, order-set edits mid-campaign.

## Steps
R1 done (PASS) → R2 T003a live runner + campaign attempt 1
(current) → R3+ iterations → integration gate →
closure.

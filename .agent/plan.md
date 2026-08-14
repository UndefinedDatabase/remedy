# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0404. Open findings: thirty-three — the thirty-two carried from F077 plus
R-0403 registered this round. `.agent/live_review.md` is the source of truth for
that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R1 is done: F082 claimed, this record reset carrying the F077 open set forward,
R-0403 registered.

## Next Steps
1. R2 — the T001 inventory, read-only, no production edit: what the six
   gauntlet modules under `packages/orchestration/` and
   `scripts/self_run_gauntlet.py` already provide, which pieces the bench
   reuses versus copies, and where the record schema and the history file
   belong under the data root. Every answer carries a file-and-symbol
   citation, into `.agent/f082_inventory.md`.
2. R3 — T001 the factoring, the five frozen orders, the record schema and a
   dry run against recorded fixture evidence.
3. R4 — T002 history append, trend computation, regression rules and goldens.
4. R5 — T003 CLI, model-context recording and a fake-provider bench run.

## Risks
- The factoring in T001 is the feature file's own named risk: the gauntlet's
  seven test files must stay green UNMODIFIED, so R2 establishes what may move
  before anything moves.
- Thirty-three open findings is the largest carry any feature has started with.

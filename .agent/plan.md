# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0429. Open findings: fifty-eight — the thirty-two carried from F077, plus
R-0403 to R-0428 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R16 records the R15 gate, registers R-0427 and R-0428, and pins F082's last
unpinned acceptance criterion — "the bench never runs implicitly" — as an
allowlist of modules permitted to call the bench's write entry points, EMPTY
today, under DECISION F082 D9. It writes no production code.

## Next Steps
1. R17 — the fake-provider bench run end to end, clearing R11's Q6 four
   blockers: the missing entry point, the local-Ollama reach through
   `RunnerDeps.plan_call_fn`/`::move_call_fn`/`::execute_fn`, the
   `time.monotonic()` call in `::run_order`, and history resolving through
   `data_paths.projects_dir` to the operator's real root. It adds one name to
   the D9 allowlist and repairs R-0427's docstring in the module it touches.
2. R18 the integration gate, R19 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure may
  not quote five, and DECISION F082 D3 binds the recovery to a bench-owned
  fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the criterion whole.
- The builder's model stays unobservable: making it visible means reaching into
  `orchestrator_loop.py::execute_dispatched_job`. Closure states that absence
  rather than implying three roles were recorded.
- R17 is the largest remaining slice and the only one that runs a campaign. Its
  four blockers are named in the feature file's Q6, not rediscovered.
- Reviewer defects remain the dominant finding class. Eleven standing
  counter-measures now bind every block: R-0417 staleness, R-0418 Fortschritt,
  R-0419 grep-every-writer, R-0420 measure-the-block, R-0421 count-the-list,
  R-0422 composite-property, R-0423 measure-the-slice, R-0424
  count-your-own-contribution, R-0425 read-back-the-line-number, R-0427
  name-the-quantified-set, R-0428 re-derive-the-base-at-delegation.

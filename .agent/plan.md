# Plan — Steps 383-390

## Goal
Fix pytest wrapper exit-code bug, add behavioral tests, build eval harness for builder prompt quality.

## Current Step
All steps complete.

## Steps
- [x] Step 383: Fix pytest wrapper exit-code propagation (set +e pattern)
- [x] Step 384: Wrapper behavior tests (6 tests: pass/fail/nonexistent/timeout/lock)
- [x] Step 385: Clean handoff truth
- [x] Step 386: Builder eval harness (EvalRecord, EvalMetrics, EvalReport)
- [x] Step 387: Prompt variants + structured output metrics (9 standard cases)
- [x] Step 388: Small-repo eval set, Ollama opt-in (4 fixtures + unsafe scenario)
- [x] Step 389: Eval CLI script (scripts/remedy_builder_eval.sh)
- [x] Step 390: Guarded baseline (3968 passed, 8 skipped via fixed wrapper)

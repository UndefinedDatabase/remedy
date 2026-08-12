# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0272. R3 reviewed PASS at ef64cf72.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R4 — T002 signature extractors: Python headers and docstring first lines via
ast, TS/JS exported-line rendering, the per-file inline size cap that decides
full content against signatures, and a suffix dispatcher, all added to
packages/orchestration/context_compiler.py with per-language goldens in
tests/orchestration/test_context_compiler.py. The T001 layer is frozen. The
round also clears finding R-0271 (ruff UP035 in the same module).

## Next Steps
1. T003 — tiered selector + budget demotion + omissions writer +
   integration on a fixture repo.
2. T004 — segment integration + the `remedy job context` CLI view +
   an end-to-end fixture task with a size comparison in evidence.
3. Integration gate per docs/agents/integration_gate.md.
4. Closure per docs/roadmap/STATUS_closure_protocol.md.

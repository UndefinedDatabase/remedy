# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0272. R4 reviewed PASS at 2c75bddf.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R5 — T003 tiered selector: assign tiers 1-4 from the fenced paths outward,
render tier 1/2 full and tier 2/3 as signatures, enforce a total token budget
by demoting tier 2 first and never truncating mid-file, and record every
demotion and omission with a reason and an outcome, all added to
packages/orchestration/context_compiler.py with fixture-tree tests in
tests/orchestration/test_context_compiler.py. T001 and T002 are frozen. The
round also resolves finding R-0271.

## Next Steps
1. T004 — segment integration + the `remedy job context` CLI view +
   an end-to-end fixture task with a size comparison in evidence.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

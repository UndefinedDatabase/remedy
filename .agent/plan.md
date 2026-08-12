# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0271. R1 reviewed PASS at d2b962af.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R2 — T001 import-neighbor graphs: Python via ast, TS/JS via the
documented line-level scanner, in
packages/orchestration/context_compiler.py, with unit tests on fixture
trees (cycles, relative imports, index files) in
tests/orchestration/test_context_compiler.py.

## Next Steps
1. T002 — signature extractors for both languages + size caps + goldens.
2. T003 — tiered selector + budget demotion + omissions writer +
   integration on a fixture repo.
3. T004 — segment integration + the `remedy job context` CLI view +
   an end-to-end fixture task with a size comparison in evidence.
4. Integration gate, then closure per STATUS_closure_protocol.md.

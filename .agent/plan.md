# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0274. R6 reviewed PASS at 861eb371.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R7 — repair round for finding R-0273 (DECISION D-F107-2): carry the effective
signature line cap on CompiledContext and render from it, so a context
compiled at a custom `line_cap` can no longer be rendered at the module
default and the budget's figures always describe the text that would actually
be sent. Change set is packages/orchestration/context_compiler.py and
tests/orchestration/test_context_compiler.py. T001-T003 behavior is otherwise
frozen and the T004 part 1 segment layer keeps its public names.

## Next Steps
1. R8 — T004 part 2: the `remedy job context` CLI view, an end-to-end fixture
   task solved by the fake provider, and the size comparison in evidence.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

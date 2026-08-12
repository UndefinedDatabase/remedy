# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0273. R5 reviewed PASS at 54bc56c2.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R6 — T004 part 1, the SEGMENT layer: render a CompiledContext into segment
text, register that text into a PromptSegmentRegistry at rank JOB_CONTEXT so
the compiled context enters a prompt as a ranked segment instead of ad hoc
concatenation, name the omissions filename once, and add the whole-file size
comparison the feature's Acceptance requires — all appended to
packages/orchestration/context_compiler.py, with tests in
tests/orchestration/test_context_compiler.py. T001-T003 are frozen.

## Next Steps
1. R7 — T004 part 2: the `remedy job context` CLI view, an end-to-end fixture
   task solved by the fake provider, and the size comparison in evidence.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

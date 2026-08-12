# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0275. R7 reviewed PASS at 6acb3f04.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R8 — T004 part 2, NOT YET STARTED: the `remedy job context <id> --task <tid>`
CLI view that renders what a task received and what was omitted, an end-to-end
fixture task solved by the fake provider using the compiled context, and the
whole-file size comparison recorded in evidence. `compare_context_size` and
`OMITTED_CONTEXT_FILENAME` already exist for it. T001-T004-part-1 are frozen.
Note for whoever plans it: `context_compiler.py` still has NO caller outside
its own tests, so R8 is the round that makes F107 a feature rather than a
library.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md.
2. Closure per docs/roadmap/STATUS_closure_protocol.md.
3. The branch has no PR yet; it is created at closure, never merged same-session.

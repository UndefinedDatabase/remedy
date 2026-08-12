# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0282. R10 reviewed PASS at c50080e0.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R11 — T004 part 2b-ii, the feature's DONE condition: `run_pingpong` gains an
OPT-IN compiled-context path, default off and byte-identical when unused, so a
fixture task runs on the compiled selection instead of the whole-file context
pack; the end-to-end test proves the fake provider still solves it and that the
context measurably shrank, and both records are written where the caller points.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md — the full suite, twice
   per feature, this being the first of the two.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the authored STATUS line, then the PR. The branch has no PR yet
   and it is never merged in the session that creates it.

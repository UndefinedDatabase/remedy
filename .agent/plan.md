# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0285. R11 reviewed PASS at 04154822.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R12 — repair and session close: the DONE-condition end-to-end test is pinned to
the compiler's own output so a bypass can no longer satisfy it (finding
R-0283), the R11 verdict and three findings are persisted, and the handoff
closes the session. T004 is complete: the CLI view, the records and the
end-to-end run all exist and were re-measured by the reviewer.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md — the full suite, the
   first of the two runs a feature gets.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the authored STATUS line, then the PR. The branch has no PR yet
   and it is never merged in the session that creates it.

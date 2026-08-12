# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0280. R9 reviewed PASS at f86bda87.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R10 — T004 part 2b-i: the size comparison gets the writer its omissions
sibling already has (`write_context_size_comparison_json`), and the
`remedy job context` view shipped in R9 gets the docs AGENTS.md requires —
a user guide plus its two rows in the `docs/README.md` index (finding
R-0279). No behaviour of the compiler's selection changes this round.

## Next Steps
1. R11 — T004 part 2b-ii: the end-to-end fixture task solved by the fake
   provider with the compiled context as its JOB_CONTEXT segment, writing
   both records into the task's evidence directory.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md; the branch has no PR
   yet, it is created at closure and never merged in the same session.

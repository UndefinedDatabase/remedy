# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0277. R8-close reviewed PASS at 7acb406d.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R9 — T004 part 2a, the FIRST CALLER: `remedy job context <id> --task <tid>`,
a read-only view that compiles the task's context and renders what it received
and what was omitted. New module `apps/cli/commands/job_context_cmd.py` owns
the repo listing the compiler deliberately does not do. This is the round that
turns F107 from a library into something a user can run.

## Next Steps
1. R10 — T004 part 2b: the end-to-end fixture task solved by the fake provider
   using the compiled context, plus the whole-file size comparison recorded in
   evidence via `compare_context_size`.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md; the branch has no PR
   yet, it is created at closure and never merged in the same session.

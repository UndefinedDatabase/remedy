# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 2, T001 under DECISION F162 D2: the `sandbox_profiles` module, the three built-in profile
files, the per-dimension preorder and the tighten-only refusal, with table tests.

## Next Steps
1. T002: process-level enforcement per dimension through the exec guard and the tool sandbox, the
   per-platform honesty record, and fixture processes proving each limit; the module is wired into
   a spawn seam and leaves the orphan list.
2. T003: adapter defaults, the project's choice in `remedy.toml` and run evidence; the optional
   container stage with its ADR; the honesty document with its row-to-test walk; the end-to-end.
3. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- Two enforcers already exist; a profile that names a limit neither applies would be a false
  promise, so every dimension is mapped to the code that enforces it or marked unenforced.

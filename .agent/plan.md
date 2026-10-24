# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 1: claim F162, re-head the review record and book F152's round 10, DECISION F162 D1, and the
findings pass — the exec guard's limits, the tool sandbox's boundary, the worker spawn paths, the
adapter contract, configuration, the container tools, evidence, doctor and the guards — committed
as `.agent/f162_inventory.md` for review.

## Next Steps
1. T001: the profile schema, the built-in profiles, the tighten-only comparator and its refusals
   with table tests, with the shape frozen from the reviewed inventory by DECISION F162 D2.
2. T002: process-level enforcement per dimension through the exec guard and the tool sandbox, the
   per-platform honesty record, and fixture processes proving each limit.
3. T003: adapter defaults and run evidence; the optional container stage with its ADR; the honesty
   document with its row-to-test walk; the end-to-end.
4. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- Two enforcers already exist; a profile that names a limit neither applies would be a false
  promise, so every dimension is mapped to the code that enforces it or marked unenforced.

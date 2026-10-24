# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 7, T003 under DECISION F162 D7: the container runner (`sandbox_container.py`), its flags,
gating and record, the fixtures shared with the process runner, and ADR 0003; R-1467, the runner's
configuration key, is registered for F246.

## Next Steps
1. T003: the honesty document `docs/system/sandbox-model.md`, generated from the profiles and both
   runners' records, with its row-to-test walk, and the end-to-end.
2. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- An allowlist profile shares the host's network under both runners; the records say so.
- The container fixtures need a local `python:3.12-slim`; where it is absent they skip, NOT VERIFIED.

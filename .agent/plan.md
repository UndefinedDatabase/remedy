# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 3, T002 under DECISION F162 D3: the tool sandbox's `share_network` field, the profile's
compiler onto the exec guard, the runner that attributes a sandboxed CPU trip, the per-platform
enforcement record, and the fixture processes proving each limit.

## Next Steps
1. T003: adapter defaults wired into the worker spawn seams (the module leaves the orphan list),
   the project's choice in `remedy.toml`, and the run evidence.
2. T003: the optional container stage with its ADR; the honesty document with its row-to-test
   walk; the end-to-end.
3. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- An allowlist profile shares the host's network: the record must say so wherever it is shown.

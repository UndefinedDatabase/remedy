# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 6: repair R-1466, then T003 under DECISION F162 D6 — the `claude_cli.sandbox_profile` key,
the tighten-only resolver the calls, the evidence and the doctor share, and `worker doctor`'s
sandbox check with its warnings.

## Next Steps
1. T003: the optional container stage with its ADR.
2. T003: the honesty document with its row-to-test walk, and the end-to-end.
3. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- An allowlist profile shares the host's network: the record must say so wherever it is shown.
- A project that names strict or standard for claude-cli denies its network; the key says so.

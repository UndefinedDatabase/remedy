# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 4, T003 under DECISION F162 D4: the `WorkerSandboxDefault` declaration and the protocol's
`sandbox_default()` member, the claude-cli default, the kit's sandbox dimension, the test doubles,
the orphan entry deleted, and the contract page.

## Next Steps
1. T003: the declaration compiled onto both claude-cli spawn policies, the run evidence, a
   project's choice in `remedy.toml`, and the doctor's warnings for unenforced dimensions.
2. T003: the optional container stage with its ADR.
3. T003: the honesty document with its row-to-test walk, and the end-to-end.
4. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- An allowlist profile shares the host's network: the record must say so wherever it is shown.
- A limit set on the claude-cli process reaches every real call; only `nofile` is set, at 1024.

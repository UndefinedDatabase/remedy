# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 5: repair R-1465, then T003 under DECISION F162 D5 — the declared default compiled onto both
claude-cli spawn policies outside the tool sandbox, and one `worker_sandbox.jsonl` line per
claude-cli provider build.

## Next Steps
1. T003: a project's choice in `remedy.toml`, tightened against the adapter's default, and the
   doctor's warnings for unenforced dimensions.
2. T003: the optional container stage with its ADR.
3. T003: the honesty document with its row-to-test walk, and the end-to-end.
4. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- An allowlist profile shares the host's network: the record must say so wherever it is shown.
- A limit set on the claude-cli process reaches every real call; only `nofile` is set, at 1024.

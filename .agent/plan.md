# Plan — operator amendment amend1027-green-builds

## Goal
A claude-cli build order whose change is right ends green: the builder may run the project's
tests, the harness counts that run, no call dies after 120 seconds, and every project has its
own slug (2026-10-27). F319 closed with two real orders (universe-chat, remedy-edition).

## Current Step
Parts A to F are done: F319 accepted with order 2318f04b3a65e952 (universe-chat, job
967b13a7bbb44b9c) and order 67f912f1e5b9ab21 (remedy-edition, job 98c1f2692d004e3e), both
awaiting the operator's apply. The closing step: the last full suite, the merge, the push, the
supervisor restart and the handback `~/.remedy-loop/amend1027-green-builds.handback.md`.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then Rule A5, which reads F316 (findings
   paydown v11) as the next line.

## Risks
- universe-chat's `main` is red on three tests of its own (DECISION amend1027 D1); its
  `.remedy/config.toml` and remedy-edition's are untracked files the operator keeps.
- The repo's settings deny reading `.data/**`; evidence is read through `remedy` commands.

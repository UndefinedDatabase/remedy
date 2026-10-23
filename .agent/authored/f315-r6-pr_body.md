## What

F315 — The loop runs through the adapter. Every claude-cli call a job makes now takes its command
line from the installed claude-cli adapter (`ClaudeCliReferenceAdapter`, F151), and a call that is
not streamed takes its usage from the adapter's `map_usage`.

- `packages/orchestration/worker_adapter_slot.py` (new): the installed adapters by adapter
  reference; `install_worker_adapters`, `installed_worker_adapter`, `adapter_cli_argv`,
  `adapter_usage_actuals`. It imports only the contract, so the import guard stays green.
- `apps/cli/grouped.py` `main` installs the adapter registry before any command runs;
  `tests/conftest.py` installs it for tests that call the loop directly.
- `ClaudeCliProvider` builds the command line of its builder, free-text reviewer, structured
  reviewer and streamed calls through the slot, and reads the usage of a call that is not streamed
  there. An empty slot is a provider error, never a fallback.
- The `build_claude_cli_args` re-export is deleted from `pingpong_provider.py`; its five test
  readers and the claude planner import it from `claude_cli_command.py` (import lines only).
- `docs/system/worker-adapter-contract-v2.md` gains the slot's section and states what stays with
  the loop's evidence.

## Why

F151 built the worker adapter contract and its reference adapter, but no job used them: the loop
still called the CLI provider directly. Every later vendor adapter needs the loop to call an
adapter; this feature makes the first one do it.

## Key decisions

- DECISION F315 D2: a slot filled by the wiring layer, not a parameter threaded through `run_job`
  and `run_pingpong` (both structure-ledger rows that would grow, and a supervisor job starts a new
  process a parameter cannot cross).
- DECISION F315 D3: the stream's events stay with the evidence capture and a failed call's class
  with the failure post-mortem, both per-call evidence the loop owns; `map_usage` answers no reason,
  so the shared envelope reader names it only when the adapter maps none.
- The reviewer's write mode is the adapter's rule, read-only, which `create_role_provider` already
  gave every reviewer.

## How to review and test

- `python3 -m pytest -q tests/orchestration/test_worker_adapter_slot.py` replaces the installed
  adapter and sees the provider and a whole `run_pingpong` on `claude-cli` spawn its command line.
- The closure's one full suite on `9e91d122a`: `23762 passed, 11 skipped, 1 warning in 341.00s`,
  exit 0 (`.agent/authored/f315-closure-suite.txt`); CPU 1255.17 s, 3.5 % below F151's.
- Evidence job `f315r5e1001` on `f00589e35`: `12681 passed, 6 skipped`, exit 0; package
  `remedy-review-20261023-225932-READY_FOR_REVIEW.zip`, SHA-256
  `801509f8c8e53b5beb75a15c42cb3fb057af2091779ee7490e60243ed2c6b0bd`.
- Every production behaviour was red-proofed by the reviewer: 13 mutations in round 2, 5 in round 3.

## Changed files

| Area | Files |
|---|---|
| Production | `packages/orchestration/worker_adapter_slot.py` (new), `packages/orchestration/pingpong_provider.py`, `apps/cli/grouped.py`, `packages/providers/claude_planner/provider.py`, `packages/providers/adapters/claude_cli_reference.py`, `packages/orchestration/worker_adapters.py` |
| Tests | `tests/orchestration/test_worker_adapter_slot.py` (new), `tests/conftest.py`, the allowlist, the structure ratchet, five import lines |
| Docs | `docs/system/worker-adapter-contract-v2.md`, `docs/system/structure-ledger-v1.md`, the checklist's consolidation paragraph, the feature file, STATUS, README |
| Records | `.agent/` |

## Verdict

Latest live review: PASS for every round; the feature closes PASS_WITH_RISKS because the closure's
self-use run raised R-1442 (the self-use generator offers a deliberate catch-all handler), owned by
F314. Open findings: 12, all owned by F314.

## Runtime actuals

One session, six delegated rounds. The self-use run made four priced provider calls, each measured
by the job's own ledger; the evidence job's pytest took 1137 s and the full suite 341 s. Token
counts of the planner and worker sessions are not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

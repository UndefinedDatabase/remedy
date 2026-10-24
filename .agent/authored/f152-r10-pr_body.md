## What

F152 — Worker config isolation. A worker tool's personal configuration no longer reaches a run:
every adapter declares how it keeps it out, the call path applies the declaration, and each build
records what it applied.

- `packages/contracts/adapter_contract.py`: `WorkerIsolation` (method, record reference, flags,
  environment allowlist, throwaway home, applies) with construction-time validation;
  `isolation()` returns it.
- `packages/providers/adapters/claude_cli_reference.py`: the claude-cli declaration — `tool_flag`,
  `--setting-sources project,local` and `--strict-mcp-config` appended to every command line, an
  allowlisted environment, the operator's home kept for the login; off while
  `claude_cli.customizations` is true.
- `packages/orchestration/worker_isolation.py` (new): the child environment, its redacted digest,
  the evidence record and its writer, the throwaway-home pair, `declared_isolation`, the A/B proof
  utility `run_isolation_ab`, and the doctor's checks.
- `packages/orchestration/worker_adapter_slot.py`, `pingpong_provider.py`,
  `role_provider_factory.py`: both claude-cli spawn policies take their environment from the
  declaration; each build writes one `worker_isolation.jsonl` line beside the run's evidence.
- `packages/contracts/adapter_conformance_kit.py`: the isolation dimension requires the record and
  the declared flags on the command line. `apps/cli/commands/worker.py`: `worker doctor` checks
  each worker's isolation.
- `docs/adr/0002-claude-cli-worker-isolation.md` (new): the research record, with its verified and
  unverified claims; `docs/README.md` indexes it.

## Why

A worker started by Remedy inherited the operator's whole shell environment and personal tool
configuration — instructions files, MCP servers, plugins — so two operators' runs were not
comparable and a run could carry settings nobody reviewed.

## Key decisions

- DECISION F152 D2: the research comes before the contract; an isolation record needs no human
  apply step; the real-binary A/B waits for the operator's permission (operator question Q26).
- DECISION F152 D3: the claude-cli worker isolates by the tool's own flags and a cleaned
  environment, not by a throwaway home, because its login lives in the operator's home.
- DECISION F152 D4: an adapter without a declaration is refused; the A/B utility runs an adapter's
  own command line twice against a poisoned throwaway home.
- DECISION F152 D5: the kit requires the record and the declared flags; `worker doctor` checks the
  declaration, the record, the home and the flags against the tool's help.

## How to review and test

- `python3 -m pytest -q tests/orchestration/test_worker_isolation.py tests/orchestration/test_worker_adapter_slot.py tests/contracts/ tests/cli/test_worker.py`
  — the A/B proof against a stand-in `claude`, with its red controls, and the doctor's fixtures.
- The closure's one full suite on `7d328380b`: `23941 passed, 11 skipped, 1 warning in 411.37s`,
  exit 0 (`.agent/authored/f152-closure-suite.txt`); CPU 1526.77 s, 8.0 % above F157's.
- Evidence job `f152r9e1001` on `ab327e93f`: `12935 passed, 6 skipped`, exit 0; package
  `remedy-review-20261024-111421-READY_FOR_REVIEW.zip`, SHA-256
  `47ab419b8fe89aa50ff6106679c1089930649a4a1bebccfe6af6e6324dd30319`.
- The closure's self-use run made the first real claude-cli calls through the declared flags and
  the cleaned environment; both authenticated and finished (`.agent/selfuse_f152/`).
- The reviewer ran 21 mutations of the production code; the one survivor became a finding and was
  repaired with a test it then turned red.

## Changed files

| Area | Files |
|---|---|
| Production | `packages/orchestration/worker_isolation.py` (new), `packages/contracts/adapter_contract.py`, `packages/contracts/adapter_conformance_kit.py`, `packages/providers/adapters/claude_cli_reference.py`, `packages/orchestration/worker_adapter_slot.py`, `packages/orchestration/pingpong_provider.py`, `packages/orchestration/role_provider_factory.py`, `apps/cli/commands/worker.py` |
| Tests | `tests/orchestration/test_worker_isolation.py` (new), `tests/contracts/test_adapter_contract.py`, `tests/contracts/test_adapter_conformance_kit.py`, `tests/contracts/test_claude_cli_reference.py`, `tests/orchestration/test_worker_adapter_slot.py`, `tests/orchestration/test_claude_cli_exec_guard.py`, `tests/orchestration/test_role_provider_factory.py`, `tests/orchestration/test_capability_routes.py`, `tests/cli/test_worker.py`, the allowlist |
| Docs | `docs/adr/0002-claude-cli-worker-isolation.md` (new), `docs/README.md`, `docs/system/worker-adapter-contract-v2.md`, the checklist's consolidation paragraph, the feature files of F152 and F316, STATUS, README |
| Records | `.agent/` |

## Verdict

Latest live review: PASS_WITH_RISKS. F152's nine findings raised against its own rounds (R-1455 to
R-1463) are all resolved inside the feature. R-1464, the real-binary A/B, is carried to F316. Open
findings: 9, all owned by F316.

## Runtime actuals

One session, ten delegated rounds. The self-use run made two priced provider calls, measured by the
job's own ledger; the evidence job's pytest took 1874 s and the full suite 411 s. Token counts of
the planner and worker sessions are not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

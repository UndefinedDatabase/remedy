## What

F162 — Sandbox profiles per adapter. What a worker process may touch becomes a named, testable
profile; each adapter declares its default, a project may only tighten it, every run records which
limits are enforced, and a generated page says honestly what each profile does and does not prevent.

- `packages/orchestration/sandbox_profiles.py` (new): the profile schema and TOML parser, the
  built-ins `strict`, `standard` and `net-local` (`packages/orchestration/sandbox_profile_files/`),
  the per-dimension preorder and the tighten-only refusal naming the minimum, the compiler onto the
  exec guard and the tool sandbox, the per-platform enforcement record, the `worker_sandbox.jsonl`
  writer, the project's choice and the doctor's check.
- `packages/orchestration/tool_sandbox.py`: `SandboxSpec.share_network` for an allowlist profile.
- `packages/contracts/adapter_contract.py`, `adapter_conformance_kit.py`: `WorkerSandboxDefault`
  and `sandbox_default()`; the kit's `sandbox` dimension refuses a default that does not parse.
- `packages/providers/adapters/claude_cli_reference.py`: the claude-cli default — an allowlist naming
  `api.anthropic.com`, `nofile` 1024, run outside the tool sandbox because the login lives in the
  operator's home.
- `packages/orchestration/worker_adapter_slot.py`, `pingpong_provider.py`,
  `role_provider_factory.py`: both claude-cli spawn policies compile the effective profile; each
  build writes one `worker_sandbox.jsonl` line.
- `packages/orchestration/config_keys_claude.py`: `claude_cli.sandbox_profile`;
  `apps/cli/commands/worker.py`: `worker doctor` warns about every unenforced dimension.
- `packages/orchestration/sandbox_container.py` (new): the optional container runner, podman or
  docker when installed, never pulling an image; `docs/adr/0003-sandbox-container-runner.md` (new).
- `scripts/render_sandbox_model.py` (new) generates `docs/system/sandbox-model.md` (new), whose
  every row names its proving test; `tests/docs/test_sandbox_model_doc.py` walks the rows.

## Why

A worker's limits were scattered over the exec guard and the tool sandbox with no name, no record of
what was enforced, and no rule against a project loosening them. The air-gap and plugin features
need one declarative profile to build on.

## Key decisions

- DECISION F162 D2: every unlimited value is spelled out; the order is a per-dimension preorder; a
  looser request is refused, never clamped.
- DECISION F162 D3: an allowlist shares the host's network and the record says hosts are not
  filtered; binaries and the tmp quota are recorded unenforced on the process runner.
- DECISION F162 D4 and D5: the claude-cli worker runs outside the tool sandbox, because the sandbox
  hides the login; its declared default is still compiled and recorded.
- DECISION F162 D6: a project's choice may only tighten; the doctor's warnings pass, a refused choice
  does not.
- DECISION F162 D7: the container runner ships without a configuration key, because no process
  Remedy runs today can use it; F246 owns the key (R-1467).
- DECISION F162 D8 and D9: the honesty page is generated and walked row by row to its tests; an
  unlimited dimension reads "no limit declared".

## How to review and test

- `python3 -m pytest -q tests/orchestration/test_sandbox_profiles.py tests/orchestration/test_sandbox_container.py tests/docs/test_sandbox_model_doc.py`
  — the table tests, the fixture processes under both runners (the container ones need a local
  `python:3.12-slim` and skip as NOT VERIFIED without it), and the page's walk.
- The closure's one full suite on `2fa84a217`: `24116 passed, 11 skipped, 1 warning in 403.19s`,
  exit 0 (`.agent/authored/f162-closure-suite.txt`); CPU 1453.59 s, 4.8 % below F152's.
- Evidence job `f162r11e1001` on `09b67feb1`: `13108 passed, 6 skipped`, exit 0; package
  `remedy-review-20261024-161429-READY_FOR_REVIEW.zip`, SHA-256
  `3aeabf2ebddca081b88766a65fa5431b19675ddedfa025062fff2ef159397d01`.
- The closure's self-use run made two real claude-cli calls, and both recorded the claude-cli
  default profile on the process runner (`.agent/selfuse_f162/worker_sandbox.txt`).
- The reviewer ran 80 mutations of the production code; the three survivors became findings and
  were repaired with tests they then turned red.

## Changed files

| Area | Files |
|---|---|
| Production | `packages/orchestration/sandbox_profiles.py` (new), `packages/orchestration/sandbox_container.py` (new), the three built-in profile files (new), `packages/orchestration/tool_sandbox.py`, `packages/contracts/adapter_contract.py`, `packages/contracts/adapter_conformance_kit.py`, `packages/providers/adapters/claude_cli_reference.py`, `packages/orchestration/worker_adapter_slot.py`, `packages/orchestration/pingpong_provider.py`, `packages/orchestration/role_provider_factory.py`, `packages/orchestration/config_keys_claude.py`, `apps/cli/commands/worker.py`, `scripts/render_sandbox_model.py` (new) |
| Tests | `tests/orchestration/test_sandbox_profiles.py` (new), `tests/orchestration/test_sandbox_container.py` (new), `tests/docs/test_sandbox_model_doc.py` (new), `tests/orchestration/test_worker_adapter_slot.py`, `tests/orchestration/test_claude_cli_exec_guard.py`, `tests/orchestration/test_role_provider_factory.py`, `tests/orchestration/test_tool_sandbox.py`, `tests/orchestration/test_capability_routes.py`, `tests/contracts/`, `tests/cli/test_worker.py`, the reachability allowlist, the orphan list |
| Docs | `docs/system/sandbox-model.md` (new, generated), `docs/adr/0003-sandbox-container-runner.md` (new), `docs/README.md`, `docs/system/worker-adapter-contract-v2.md`, `docs/system/tool-sandbox-v1.md`, `docs/guides/environment.md`, the checklist's consolidation paragraph, the feature files of F162 and F246, STATUS, README |
| Records | `.agent/`, `scripts/self_use_queue.json` |

## Verdict

Latest live review: PASS_WITH_RISKS. F162's five findings raised against its own rounds (R-1465,
R-1466, R-1468, R-1469 and R-1470) are all resolved inside the feature. R-1467, the container
runner's configuration key, is owned by F246. Open findings: 10, nine owned by F316 and one by F246.

## Runtime actuals

Two sessions, twelve delegated rounds. The self-use run made two priced provider calls, measured by
the job's own ledger; the evidence job's pytest took 1861 s and the full suite 403 s. Token counts of
the planner and worker sessions are not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

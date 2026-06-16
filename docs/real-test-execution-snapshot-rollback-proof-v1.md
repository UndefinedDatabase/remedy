# Real Test Execution + Snapshot/Rollback Proof v1 (Steps 1877-1916)

## Why this exists

The Overnight Mission Contract already knows tests/snapshot/proof can be required gates. This block
provides safe, bounded, evidence-backed **test execution** and honest **snapshot/rollback proof** the
contract can consume.

> Workers execute. Remedy governs. Tests and rollback proof become durable gates.

This block is bounded, command-discovered, policy-gated, evidence-backed — never uncontrolled
automation.

## Allowed test execution model

`real_test_execution.py` is a SAFE FACADE. It does NOT implement subprocess execution itself — it
reuses the existing single safe entry point `test_execution_service.execute_test_run`, which is
contract-gated, leased, sandboxed (sanitized env, isolated process group), output-capped, and uses an
argv list (NO `shell=True`). `run_allowed_test` first resolves the command via
`resolve_allowed_command` (must be a discovered **test**-purpose command; shell metacharacters and
destructive/forbidden programs — rm/dd/sudo/git/curl/pip/npm/… — are rejected) before any execution.

## Dynamic command discovery relationship

Commands come from `command_discovery.discover_commands` (Makefile/justfile/Taskfile/package.json/
pyproject/constitution detectors) as `CommandCandidate` with an immutable argv tuple. No arbitrary
user command strings are ever executed.

## Run contract relationship

Execution stays on the existing `RUN_TEST` action through `execute_test_run`, which enforces the
job's run contract (`max_test_runs`, budgets, lease). By default `max_test_runs == 0`, so a test run
is `blocked_by_contract` until the operator raises it — nothing runs uninvited.

## Snapshot proof concept

`SnapshotProof` (v1) is an HONEST metadata snapshot: a bounded inventory hash (`(rel_path, size)`
pairs; no file contents read) + a dirty-file count. It records a snapshot POINT. It does **not**
capture recovery content, so `restore_available` is always `False`.

## Rollback proof concept

`RollbackProof` is honest: v1 performs **no revert** and `restore_tested` is always `False`.
`restore_available` is `True` only when apply-scoped recovery material is verified (via
`repository_snapshot.build_snapshot_truth`); a metadata-only snapshot yields `restore_available =
False` with explicit `limitations`. The mission gate distinguishes `snapshot_recorded` from
`rollback_restore_available`.

## Failure artifact relationship

On `failed`/`timeout`, `execute_test_run` creates a safe Test Failure Artifact (no raw output) linked
to the `test_run_id`; the next safe action points at repair. Raw stdout/stderr stays private
(referenced by `output_ref`); public surfaces get safe summaries only.

## Mission contract gate relationship

`overnight_mission` consumes: latest real test run (`tests_green` only from a real `passed` + exit 0),
`snapshot_recorded` (gate `snapshot_before_apply`), and `rollback_restore_available` (gate
`rollback_restore_available`). A failing latest test or a missing required gate blocks satisfaction.

## CLI

```
remedy test run <job_id> ...        # existing safe runner (contract-gated; execute_test_run)
remedy test result <test_run_id> --json
remedy test list <job_id> --json
remedy test integrity --json
remedy snapshot create <job_id> --json
remedy snapshot show <snapshot_id> --json
remedy rollback proof <job_id> --snapshot-id <id> --json
remedy rollback show <rollback_proof_id> --json
```

`snapshot create` / `rollback proof` are `write_metadata`; result/list/show/integrity are read-only.
None carry `may_execute_commands` (execution stays on the existing `test run`).

## What is not automated yet

- No real rollback **restore** — v1 is honest metadata; `restore_available`/`restore_tested` are
  False unless verified apply-scoped recovery exists.
- No provider/model/Claude/Pi/OpenCode/Ollama/worker execution.
- No auto-apply, auto-approval, autonomous repair execution, or auto-PR/git.
- No MemPalace/embeddings, no UI redesign, no MCP.

## Anti-goals (explicit)

- Allowed test execution ONLY, through the approved bounded runner; no shell, no arbitrary/
  destructive/network/install/git-write commands.
- No fake test pass (pass requires runner `passed` + exit 0). No fake rollback restore. Raw output
  never appears in public surfaces.

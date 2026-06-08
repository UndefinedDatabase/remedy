# remedy do v1 — Cohesive Flow

> How `remedy do` runs a phased, fixture-only pipeline that stops before apply.

## Overview

`remedy do` is the primary entry point for guided work. In v1 it runs a
fixture-only flow: no real LLM calls, no Ollama, no file mutations, no
external command execution. The flow creates real Job/Task/Artifact records,
inspects context, builds a fixture proposal, creates a patch intent, and
stops at an approval gate.

v1 writes only to the Remedy data store (Job/Task/Artifact). It does **not**
mutate repo files or execute external commands.

## Usage

```
remedy do "add a safe docs change" --repo . --autonomy-level 3 --json
```

Flags:
- `--repo` — target repository path (default `.`)
- `--autonomy-level` — 0-7 accepted, capped at 3 in v1
- `--max-cycles` — max loops (v1 caps to 1, single pass)
- `--json` — structured JSON output
- `--dry-run` — plan-only mode (no records created)

## Phased Flow

```
init → plan → context → build → patch_intent → approval_required → stop
```

| Phase | What happens |
|-------|-------------|
| `init` | Create Job with user prompt, attach repo via Artifact metadata |
| `plan` | Create Task from goal |
| `context` | Run context inspector; stop if BLOCKED or on error |
| `build` | Create fixture builder proposal (safe summary, no raw content) |
| `patch_intent` | Create intent ID via `make_intent_id()` |
| `approval_required` | Flow stops — approval needed before apply |
| `proof` | Build proof chain (expected incomplete before apply) |

### Context Failure Stops the Run

If the context inspector raises an unexpected error, the flow stops with
`context_error`. No build phase, no patch intent. The `next_safe_action`
points to `remedy context inspect` for diagnosis.

## Run Contract

Source: `do_v1_minimal` (simplified, consolidation with `RunContract` in v2).

| Field | Default | Notes |
|-------|---------|-------|
| `autonomy_level` | 2 | Capped at 3 |
| `stop_before_apply` | `True` | Always true in v1 |
| `max_loops` | 1 | Single pass in v1 (input capped to 1) |
| `allowed_actions` | plan, build_artifact, create_patch_intent | |
| `denied_actions` | apply_patch, arbitrary_shell, network_fetch | |

The run contract is visible in `--json` output under the `run_contract` key.

## Autonomy Truth

JSON output exposes both requested and effective autonomy:

- `autonomy_level` — effective (capped at 3)
- `requested_autonomy_level` — what the user asked for
- `autonomy_capped` — boolean, true if capped
- `cap_reason` — why the cap was applied

## max_loops Truth

- `--max-cycles 0` → `invalid_input` stop, no job created
- `--max-cycles 1` → normal single pass
- `--max-cycles 3` → still single pass (v1 caps to 1), contract shows `max_loops: 1`

## JSON Output Contract

Top-level keys in `--json` output:

```
version, job_id, task_id, artifact_ids, patch_intent_id,
proof_status, phases, stop_reason, next_safe_action,
autonomy_level, requested_autonomy_level, autonomy_capped, cap_reason,
repo_path_safe, context_summary, generated_at, run_contract
```

- `stop_reason.reason` — `approval_required`, `context_blocked`, `context_error`, `invalid_input`
- `next_safe_action.command` — a fully validated catalog command (group.subcommand)
- `repo_path_safe` — basename only, no absolute paths
- No raw file content, secrets, or diffs in output

## Next Safe Action

All `next_safe_action.command` values are validated against the command catalog
using `validate_next_safe_action_command()`. This checks the full
`remedy <group> <subcommand>` maps to a real `<group>.<subcommand>` catalog entry.

## Approval Gate

v1 always stops before apply. The `next_safe_action` tells the user what
command to run next:

- Normal stop: `remedy patch approve <job_id> <intent_id>`
- Context blocked/error: `remedy context inspect <job_id> <task_id> --json`
- No patch intent: `remedy job show <job_id> --json`

## Safety Guarantees

- No file mutations in v1
- No external command execution
- No `shell=True` anywhere
- No secrets or `.env` content in output
- No absolute paths in JSON
- Output size bounded (< 50 KB)
- Autonomy capped at level 3
- Context failure stops the run (no silent continue)
- Catalog metadata: `may_mutate_repo=False`, `may_execute_commands=False`

## Source Files

- `packages/orchestration/do_run.py` — core flow + export + validation
- `apps/cli/commands/do_cmd.py` — CLI wiring
- `tests/orchestration/test_do_run.py` — 67 unit tests
- `tests/cli/test_do_runtime.py` — 14 subprocess tests

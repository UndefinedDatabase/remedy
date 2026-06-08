# remedy do v1 — Cohesive Flow

> How `remedy do` runs a phased, fixture-only pipeline that stops before apply.

## Overview

`remedy do` is the primary entry point for guided work. In v1 it runs a
fixture-only flow: no real LLM calls, no Ollama, no file mutations. The flow
creates real Job/Task/Artifact records, inspects context, builds a fixture
proposal, creates a patch intent, and stops at an approval gate.

## Usage

```
remedy do "add a safe docs change" --repo . --autonomy-level 3 --json
```

Flags:
- `--repo` — target repository path (default `.`)
- `--autonomy-level` — 1-3, capped at 3 in v1
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
| `context` | Run context inspector; stop if readiness is BLOCKED |
| `build` | Create fixture builder proposal (safe summary, no raw content) |
| `patch_intent` | Create intent ID via `make_intent_id()` |
| `approval_required` | Flow stops — approval needed before apply |
| `proof` | Build proof chain (expected incomplete before apply) |

## Run Contract

| Field | Default | Notes |
|-------|---------|-------|
| `autonomy_level` | 2 | Capped at 3 |
| `stop_before_apply` | `True` | Always true in v1 |
| `max_loops` | 1 | Single pass in v1 |

## JSON Output Contract

Top-level keys in `--json` output:

```
version, job_id, task_id, artifact_ids, patch_intent_id,
proof_status, phases, stop_reason, next_safe_action,
autonomy_level, repo_path_safe, context_summary, generated_at
```

- `stop_reason.reason` — `approval_required` or `context_blocked`
- `next_safe_action.command` — a real catalog command (e.g. `remedy patch approve`)
- `repo_path_safe` — basename only, no absolute paths
- No raw file content, secrets, or diffs in output

## Approval Gate

v1 always stops before apply. The `next_safe_action` tells the user what
command to run next:

- Normal stop: `remedy patch approve <intent_id>`
- Context blocked: `remedy context inspect <job_id>`
- Proof incomplete: `remedy job show <job_id>`

## Safety Guarantees

- No file mutations in v1
- No `shell=True` anywhere
- No secrets or `.env` content in output
- No absolute paths in JSON
- Output size bounded (< 50 KB)
- Autonomy capped at level 3

## Source Files

- `packages/orchestration/do_run.py` — core flow + export
- `apps/cli/commands/do_cmd.py` — CLI wiring
- `tests/orchestration/test_do_run.py` — 34 unit tests
- `tests/cli/test_do_runtime.py` — 10 subprocess tests

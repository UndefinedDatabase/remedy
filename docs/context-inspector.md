# Context Inspector

The Context Inspector answers: **"What will the worker see, what will it not see, and why?"**

## CLI Usage

```
remedy context inspect <job_id> [task_id] [--budget 4000] [--json]
```

Text output shows readiness, budget, included/excluded paths, and policy gates.
JSON output includes structured inspection data with no raw file content.

## Readiness Statuses

| Status | Meaning |
|---|---|
| **ready** | Enough context to proceed, no warnings |
| **ready_with_warnings** | Context available but with warnings (over budget, no manifests, etc.) |
| **blocked** | Cannot proceed — no included files |
| **unknown** | Cannot determine readiness |

## Budget Statuses

| Status | Meaning |
|---|---|
| **within_budget** | Estimated tokens <= 80% of budget |
| **near_budget** | Estimated tokens between 80-100% of budget |
| **over_budget** | Estimated tokens exceed budget |
| **unknown_budget** | Budget is zero or cannot be determined |

Token estimation is heuristic: `ceil(bytes / 4)`. This is a rough approximation.

## Included Paths

Files are included by reason:
- **manifest_file** — `pyproject.toml`, `package.json`, etc.
- **documentation_file** — `README.md`, `AGENTS.md`, `CLAUDE.md`
- **task_target_path** — file referenced in task inputs
- **patch_intent_target** — file targeted by a patch intent
- **related_test_file** — test files by naming convention
- **source_file** — `.py`, `.ts`, `.js`, etc.
- **config_file** — `.yaml`, `.json`, `.toml`, etc.

## Excluded Paths

Files are excluded by reason:
- **protected_path** — `.env`, `.data/`, `.git/`, secrets
- **unsupported_extension** — binary, image, archive, key files
- **symlink_excluded** — symlinks excluded by default
- **over_size_limit** — file exceeds 100KB
- **empty_file** — zero-byte file
- **path_traversal** — path contains `..` or starts with `/`
- **unknown_file_type** — unrecognized extension

## Safety

Context Inspector output contains **path metadata only**:
- No raw source content or file bodies
- No secrets, `.env` values, or credentials
- No MCP config content (only server counts)
- No stdout/stderr, diffs, or tracebacks
- No absolute home/user paths
- Repo root shown as basename only

## Policy Gates

All gates are enforced by default:
- `protected_paths_enforced` — secrets/protected dirs excluded
- `token_budget_enforced` — budget limits context size
- `raw_content_redaction` — output is metadata only
- `no_shell_true` — no shell execution
- `no_mutation_from_inspect` — inspection is read-only
- `source_apply_requires_approval` — changes require approval
- `mcp_inactive_by_default` — MCP servers inactive

## Tooling Awareness

Reports presence (not content) of agent tooling:
- `.pi/` directory
- `.claude/` directory
- `.mcp.json` with active server count
- `.vscode/mcp.json` with active server count

# remedy.toml Configuration System v0

## Problem

Remedy configuration is scattered across environment variables read in multiple
modules (`data_paths.py`, `ollama_builder/provider.py`, `ollama_planner/provider.py`).
Each module independently calls `os.environ.get(...)` with its own defaults and
parsing logic. There is no central inventory, no way for operators to list or
inspect active configuration, and no file-based config option for values that
are not secrets.

## Solution

A centralized configuration system backed by `remedy.toml` files with a strict
source precedence hierarchy:

```
env var  >  project config  >  user config  >  built-in default
```

### Source precedence

| Priority | Source | Path | Purpose |
|----------|--------|------|---------|
| 1 (highest) | Environment variable | `$REMEDY_*` | CI overrides, secrets, ephemeral config |
| 2 | Project config | `./remedy.toml` | Per-project settings, checked into repo |
| 3 | User config | `~/.config/remedy/remedy.toml` | User-wide defaults |
| 4 (lowest) | Built-in default | Hard-coded | Safe fallback values |

### Security boundaries

- **No secret storage**: API keys, tokens, passwords must remain in environment
  variables or external secret managers. `remedy.toml` must never contain secrets.
- **Secret-like keys**: Config keys marked `env_only=True` are never read from
  TOML files and never written by `config set`. They appear in `config list`
  with source `env` or `default` only.
- **Redaction**: Values for secret-like keys are masked in `config show` output.
  The review bundle `config_summary.json` section redacts secret-like values.

### Config keys (v0)

| Key | Type | Env var | Default | env_only |
|-----|------|---------|---------|----------|
| `data_dir` | path | `REMEDY_DATA_DIR` | `<repo>/.data` | no |
| `ollama.host` | url | `REMEDY_OLLAMA_HOST` | `http://localhost:11434` | no |
| `ollama.model` | string | `REMEDY_OLLAMA_MODEL` | `qwen3-coder-next` | no |
| `ollama.builder.model` | string | `REMEDY_OLLAMA_BUILDER_MODEL` | (falls back to `ollama.model`) | no |
| `ollama.builder.temperature` | float | `REMEDY_OLLAMA_BUILDER_TEMPERATURE` | (none) | no |
| `ollama.builder.num_predict` | int | `REMEDY_OLLAMA_BUILDER_NUM_PREDICT` | (none) | no |
| `ollama.planner.model` | string | `REMEDY_OLLAMA_PLANNER_MODEL` | (falls back to `ollama.model`) | no |
| `ollama.planner.temperature` | float | `REMEDY_OLLAMA_PLANNER_TEMPERATURE` | (none) | no |
| `ollama.planner.num_predict` | int | `REMEDY_OLLAMA_PLANNER_NUM_PREDICT` | (none) | no |
| `ui.host` | string | `REMEDY_UI_HOST` | `127.0.0.1` | no |
| `ui.port` | int | `REMEDY_UI_PORT` | `8765` | no |
| `tests.pytest_timeout_seconds` | int | `REMEDY_PYTEST_TIMEOUT_SECONDS` | `300` | no |
| `quality.coverage_fail_under` | int | `REMEDY_COVERAGE_FAIL_UNDER` | (none) | no |
| `logging.level` | string | `REMEDY_LOG_LEVEL` | `WARNING` | no |
| `claude_enabled` | bool | `REMEDY_CLAUDE_ENABLED` | `false` | yes |
| `opencode_enabled` | bool | `REMEDY_OPENCODE_ENABLED` | `false` | yes |
| `pi_dev_enabled` | bool | `REMEDY_PI_DEV_ENABLED` | `false` | yes |
| `external_memory_enabled` | bool | `REMEDY_EXTERNAL_MEMORY_ENABLED` | `false` | yes |

### TOML file format

```toml
# remedy.toml
[remedy]
data_dir = ".data"

[remedy.ollama]
host = "http://localhost:11434"
model = "qwen3-coder-next"

[remedy.ollama.builder]
model = "qwen3-coder-next"
temperature = 0.3

[remedy.ollama.planner]
model = "qwen3-coder-next"
temperature = 0.2
```

All keys live under the `[remedy]` table to avoid collisions with other tools
that may also use `remedy.toml`.

### CLI surface

| Command | Action | Description |
|---------|--------|-------------|
| `remedy config list` | read_only | List all known config keys with current values and sources |
| `remedy config show` | read_only | Alias for `config list` |
| `remedy config get <key>` | read_only | Show value and source for one key |
| `remedy config sources` | read_only | Show which config files are loaded and their paths |
| `remedy config init [--path P]` | write_metadata | Create a `remedy.toml` template (default: `./remedy.toml`) |
| `remedy config set <key> <value> [--path P]` | write_metadata | Set a key (refuses unknown/env_only/secret keys) |
| `remedy config validate [--path P]` | read_only | Validate config against key specs |

### Module architecture

```
packages/orchestration/config.py    — core: ConfigSource, ConfigValue, ConfigKeySpec,
                                      RemedyConfig, load/resolve/get API
apps/cli/commands/config_cmd.py     — CLI handlers for config group
apps/cli/command_catalog.py         — catalog entries for config commands
```

### Resolver migration

Existing modules migrate from direct `os.environ.get()` to config lookups:
- `data_paths.py`: `resolve_data_root()` reads `data_dir` from config
- `ollama_builder/provider.py`: `_resolve_model()` and constructor read from config
- `ollama_planner/provider.py`: `_resolve_model()` and constructor read from config

Backward compatibility: env vars always win (source priority 1), so existing
deployments with `REMEDY_DATA_DIR` or `REMEDY_OLLAMA_*` set continue to work
without changes.

### Review bundle integration

A new `config_summary.json` section in the review bundle captures:
- All resolved config values with sources (secret values redacted)
- Which config files were loaded
- Any validation warnings

### What is intentionally not included in v0

- Hot-reload or file watching
- Config schema versioning
- Plugin/provider config registration (keys are hard-coded in registry)
- Config locking or atomic writes
- Config inheritance between projects
- Profile/environment switching (e.g., `[remedy.dev]` vs `[remedy.prod]`)

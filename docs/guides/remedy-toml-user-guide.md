# remedy.toml User Guide

## Quick start

```bash
# Create a config file in your project
remedy config init

# Set a value
remedy config set ollama.host http://myserver:11434

# See all current config
remedy config list

# Check a specific key
remedy config get data_dir
```

## Config file locations

Remedy reads config from two TOML files (in priority order):

| File | Purpose |
|------|---------|
| `./remedy.toml` | Project-specific config (check into version control) |
| `~/.config/remedy/remedy.toml` | User-wide defaults |

Environment variables always override both files.

## Precedence

When the same key is set in multiple places, the highest-priority source wins:

1. **Environment variable** (`REMEDY_*`) — always wins
2. **Project config** (`./remedy.toml`) — per-project overrides
3. **User config** (`~/.config/remedy/remedy.toml`) — personal defaults
4. **Built-in default** — safe fallback

## File format

All keys live under the `[remedy]` table:

```toml
[remedy]
data_dir = "/path/to/data"

[remedy.ollama]
host = "http://localhost:11434"
model = "<your-ollama-model>"

[remedy.ollama.builder]
model = "codellama"
temperature = 0.3
num_predict = 4096

[remedy.ollama.planner]
model = "<your-ollama-model>"
temperature = 0.2
```

## Available keys

| Key | Env var | Type | Default | Description |
|-----|---------|------|---------|-------------|
| `data_dir` | `REMEDY_DATA_DIR` | path | `<repo>/.data` | Root directory for Remedy data |
| `ollama.host` | `REMEDY_OLLAMA_HOST` | url | `http://localhost:11434` | Ollama server URL |
| `ollama.model` | `REMEDY_OLLAMA_MODEL` | string | the `ollama-default` alias | Default model for all Ollama roles |
| `ollama.builder.model` | `REMEDY_OLLAMA_BUILDER_MODEL` | string | (falls back to `ollama.model`) | Model for builder role |
| `ollama.builder.temperature` | `REMEDY_OLLAMA_BUILDER_TEMPERATURE` | float | (none) | Sampling temperature for builder |
| `ollama.builder.num_predict` | `REMEDY_OLLAMA_BUILDER_NUM_PREDICT` | int | (none) | Max tokens for builder |
| `ollama.planner.model` | `REMEDY_OLLAMA_PLANNER_MODEL` | string | (falls back to `ollama.model`) | Model for planner role |
| `ollama.planner.temperature` | `REMEDY_OLLAMA_PLANNER_TEMPERATURE` | float | (none) | Sampling temperature for planner |
| `ollama.planner.num_predict` | `REMEDY_OLLAMA_PLANNER_NUM_PREDICT` | int | (none) | Max tokens for planner |

## CLI commands

| Command | Description |
|---------|-------------|
| `remedy config list` | List all keys with values and sources |
| `remedy config list --json` | Same, as JSON |
| `remedy config get <key>` | Show value, source, env var, type for one key |
| `remedy config sources` | Show which config files are loaded |
| `remedy config init` | Create a `remedy.toml` template |
| `remedy config set <key> <value>` | Set a key in `./remedy.toml` |
| `remedy config validate` | Validate config against key specs |

## Migration from environment variables

Existing deployments that use `REMEDY_DATA_DIR` or `REMEDY_OLLAMA_*` environment
variables continue to work without changes. Environment variables always take
precedence over config files.

To migrate a value from env to config:

```bash
# Instead of: export REMEDY_OLLAMA_HOST=http://myserver:11434
remedy config set ollama.host http://myserver:11434

# Verify
remedy config get ollama.host
# ollama.host = http://myserver:11434
#   source: project
```

## Security

- **Never put secrets in remedy.toml.** API keys, tokens, and passwords
  must remain in environment variables or external secret managers.
- Keys marked `env_only` cannot be set via `config set`.
- The review bundle `config_summary.json` section redacts secret values.

## Review bundle integration

Every review bundle includes a `config_summary.json` section showing:
- All resolved config values with sources
- Which config files were loaded
- Any validation warnings

This aids debugging when reviewing bundles from other machines or CI.

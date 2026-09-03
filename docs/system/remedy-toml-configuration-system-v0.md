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
| `ollama.model` | string | `REMEDY_OLLAMA_MODEL` | the `ollama-default` alias | no |
| `ollama.builder.model` | string | `REMEDY_OLLAMA_BUILDER_MODEL` | (falls back to `ollama.model`) | no |
| `ollama.builder.temperature` | float | `REMEDY_OLLAMA_BUILDER_TEMPERATURE` | (none) | no |
| `ollama.builder.num_predict` | int | `REMEDY_OLLAMA_BUILDER_NUM_PREDICT` | (none) | no |
| `ollama.planner.model` | string | `REMEDY_OLLAMA_PLANNER_MODEL` | (falls back to `ollama.model`) | no |
| `ollama.planner.temperature` | float | `REMEDY_OLLAMA_PLANNER_TEMPERATURE` | (none) | no |
| `ollama.planner.num_predict` | int | `REMEDY_OLLAMA_PLANNER_NUM_PREDICT` | (none) | no |
| `planning.granularity.enabled` | bool | `REMEDY_PLANNING_GRANULARITY_ENABLED` | `true` | no |
| `planning.granularity.split_band` | string | `REMEDY_PLANNING_GRANULARITY_SPLIT_BAND` | `XL` | no |
| `planning.granularity.max_acceptance` | int | `REMEDY_PLANNING_GRANULARITY_MAX_ACCEPTANCE` | `3` | no |
| `planning.granularity.merge_group_size` | int | `REMEDY_PLANNING_GRANULARITY_MERGE_GROUP_SIZE` | `3` | no |
| `cycles.max_cycles` | int | `REMEDY_CYCLES_MAX_CYCLES` | `1` | no |
| `cycles.batch_size` | int | `REMEDY_CYCLES_BATCH_SIZE` | `1` | no |
| `cycles.verify_command` | string | `REMEDY_CYCLES_VERIFY_COMMAND` | (none) | no |
| `model_routing.task_class_tiers` | table | (TOML only) | (none) | no |

The table above is not exhaustive — later features added their own keys
(`scope.*`, `budget.*`, `postmortem.*`). The key registry
`_CONFIG_KEY_SPECS` in `packages/orchestration/config.py` is the source of
truth; `remedy config list` prints the resolved set.

The `planning.granularity.*` keys drive Flight-Plan task-granularity
normalization (F016): oversized planned tasks are split, runs of trivial
neighbors are merged, and every transformation is listed in a
**Normalization** section of the generated `plan.md` before a human
approves it. Setting `planning.granularity.enabled = false` passes the
planner's task list through untouched.

The `cycles.*` keys bound the multi-cycle loop (F046) that
`remedy job run <id> [--cycles N]` drives. `cycles.max_cycles` defaults to
`1` — an unconfigured run is still a single pass. The F075 milestone gate
raised `CYCLE_SAFETY_CAP` in `packages/orchestration/long_run_executor.py`
from 1 to 8 (ADR-0001, applied 2026-08-07), so the config value and the
`--cycles` flag are now honored up to 8 and trimmed above it, and the
command reports a trimmed number instead of silently honoring it. `cycles.verify_command` is
recorded on every cycle evidence record; a cycle that ran no verification
records `not_run` and never claims a pass.

### Table-valued keys: `model_routing.task_class_tiers`

Most keys carry a scalar. `model_routing.task_class_tiers` (F110) carries a
whole TOML sub-table, resolved as **one value** through the same precedence
chain. It maps a task class to the model tier this project wants that class
routed to, laid over the shipped seed mapping:

```toml
[remedy.model_routing.task_class_tiers]
summarize = "mid"
extract = "cheap"
```

**TOML only.** An environment variable cannot carry a table, so this key has no
usable env override; a string arriving on that path is reported as a shape
fault by `remedy config validate` rather than read as a table.

**The hard rules win.** The rules in `docs/agents/model_routing_policy.md` are
enforced in code, so a map that breaks one — demoting an orchestration class
below the top tier, routing a reviewer weaker than the worker it reviews, or
promoting a class to a cheaper tier without benchmark evidence — is **refused
whole**, with the violated rule named in a warning, and the shipped table is
used instead. Nothing is silently dropped and nothing is partially applied. The
seed mapping itself lives in `docs/agents/model_routing_policy.md` and in
`packages/orchestration/model_routing.py`; it is deliberately not restated here.

### TOML file format

```toml
# remedy.toml
[remedy]
data_dir = ".data"

[remedy.ollama]
host = "http://localhost:11434"
model = "<your-ollama-model>"

[remedy.ollama.builder]
model = "<your-ollama-model>"
temperature = 0.3

[remedy.ollama.planner]
model = "<your-ollama-model>"
temperature = 0.2
```

All keys live under the `[remedy]` table to avoid collisions with other tools
that may also use `remedy.toml`.

### CLI surface

| Command | Action | Description |
|---------|--------|-------------|
| `remedy config list` | read_only | List all known config keys with current values and sources |
| `remedy config get <key>` | read_only | Show value and source for one key |
| `remedy config sources` | read_only | Show which config files are loaded and their paths |
| `remedy config init` | write_metadata | Create a `remedy.toml` template in the current directory |
| `remedy config set <key> <value>` | write_metadata | Set a key in `./remedy.toml` (refuses env_only keys) |
| `remedy config validate` | read_only | Validate loaded config against key specs |

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

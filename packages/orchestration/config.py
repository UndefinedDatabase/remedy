"""
Centralized configuration for Remedy — remedy.toml + env var precedence.

Source precedence (highest to lowest):
  1. Environment variable (REMEDY_*)
  2. Project config (./remedy.toml)
  3. User config (~/.config/remedy/remedy.toml)
  4. Built-in default

Public API::

    ConfigSource: enum of config sources
    ConfigValue: resolved value + metadata
    ConfigKeySpec: typed key definition
    RemedyConfig: main config object
    get_config() -> RemedyConfig
    load_config(project_path=None, user_path=None) -> RemedyConfig
"""

from __future__ import annotations

import enum
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore[assignment]


class ConfigSource(enum.Enum):
    """Where a config value came from."""

    ENV = "env"
    PROJECT = "project"
    USER = "user"
    DEFAULT = "default"


@dataclass(frozen=True)
class ConfigValue:
    """A resolved config value with its source."""

    key: str
    value: Any
    source: ConfigSource
    raw_value: str | None = None

    @property
    def is_default(self) -> bool:
        return self.source == ConfigSource.DEFAULT


@dataclass(frozen=True)
class ConfigKeySpec:
    """Definition of one config key.

    value_type supports: str, int, float, bool, list.
    When value_type is list, values are list-of-strings. Env var values
    are split on commas. TOML arrays are used as-is.
    """

    key: str
    env_var: str
    description: str
    value_type: type = str
    default: Any = None
    env_only: bool = False
    secret: bool = False
    fallback_key: str | None = None


# ---------------------------------------------------------------------------
# Key registry (v0)
# ---------------------------------------------------------------------------

_CONFIG_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
    ConfigKeySpec(
        key="postmortem.llm_summary",
        env_var="REMEDY_POSTMORTEM_LLM_SUMMARY",
        description=(
            "Generate an LLM summary for failure post-mortems (F010). "
            "Disabled by default: v1 post-mortems are fully deterministic and make "
            "zero provider calls; no generated prose is ever passed off as analysis."
        ),
        value_type=bool,
        default=False,
    ),
    ConfigKeySpec(
        key="data_dir",
        env_var="REMEDY_DATA_DIR",
        description="Root directory for Remedy data storage",
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="ollama.host",
        env_var="REMEDY_OLLAMA_HOST",
        description="Ollama server URL",
        value_type=str,
        default="http://localhost:11434",
    ),
    ConfigKeySpec(
        key="ollama.model",
        env_var="REMEDY_OLLAMA_MODEL",
        description="Default Ollama model for all roles",
        value_type=str,
        default="qwen3-coder-next",
    ),
    ConfigKeySpec(
        key="ollama.builder.model",
        env_var="REMEDY_OLLAMA_BUILDER_MODEL",
        description="Ollama model for builder role",
        value_type=str,
        default=None,
        fallback_key="ollama.model",
    ),
    ConfigKeySpec(
        key="ollama.builder.temperature",
        env_var="REMEDY_OLLAMA_BUILDER_TEMPERATURE",
        description="Sampling temperature for builder",
        value_type=float,
        default=None,
    ),
    ConfigKeySpec(
        key="ollama.builder.num_predict",
        env_var="REMEDY_OLLAMA_BUILDER_NUM_PREDICT",
        description="Max tokens for builder",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="ollama.planner.model",
        env_var="REMEDY_OLLAMA_PLANNER_MODEL",
        description="Ollama model for planner role",
        value_type=str,
        default=None,
        fallback_key="ollama.model",
    ),
    ConfigKeySpec(
        key="ollama.planner.temperature",
        env_var="REMEDY_OLLAMA_PLANNER_TEMPERATURE",
        description="Sampling temperature for planner",
        value_type=float,
        default=None,
    ),
    ConfigKeySpec(
        key="ollama.planner.num_predict",
        env_var="REMEDY_OLLAMA_PLANNER_NUM_PREDICT",
        description="Max tokens for planner",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="ui.host",
        env_var="REMEDY_UI_HOST",
        description="UI server bind host",
        value_type=str,
        default="127.0.0.1",
    ),
    ConfigKeySpec(
        key="ui.port",
        env_var="REMEDY_UI_PORT",
        description="UI server port",
        value_type=int,
        default=8765,
    ),
    ConfigKeySpec(
        key="tests.pytest_timeout_seconds",
        env_var="REMEDY_PYTEST_TIMEOUT_SECONDS",
        description="Default pytest timeout in seconds",
        value_type=int,
        default=300,
    ),
    ConfigKeySpec(
        key="quality.coverage_fail_under",
        env_var="REMEDY_COVERAGE_FAIL_UNDER",
        description="Minimum test coverage percentage",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="logging.level",
        env_var="REMEDY_LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
        value_type=str,
        default="WARNING",
    ),
    ConfigKeySpec(
        key="claude_enabled",
        env_var="REMEDY_CLAUDE_ENABLED",
        description="Enable Claude provider (env-only flag)",
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="opencode_enabled",
        env_var="REMEDY_OPENCODE_ENABLED",
        description="Enable OpenCode provider (env-only flag)",
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="pi_dev_enabled",
        env_var="REMEDY_PI_DEV_ENABLED",
        description="Enable Pi dev provider (env-only flag)",
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="external_memory_enabled",
        env_var="REMEDY_EXTERNAL_MEMORY_ENABLED",
        description="Enable external memory integration (env-only flag)",
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="scope.allow",
        env_var="REMEDY_SCOPE_ALLOW",
        description="Glob patterns for allowed write paths (F017 scope fences)",
        value_type=list,
        default=None,
    ),
    ConfigKeySpec(
        key="scope.deny",
        env_var="REMEDY_SCOPE_DENY",
        description="Glob patterns for denied write paths (F017 scope fences)",
        value_type=list,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.max_total_tokens",
        env_var="REMEDY_BUDGET_MAX_TOTAL_TOKENS",
        description="Maximum total tokens for a job (F018 budgets)",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.max_provider_calls",
        env_var="REMEDY_BUDGET_MAX_PROVIDER_CALLS",
        description="Maximum provider calls for a job (F018 budgets)",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.max_wall_clock_minutes",
        env_var="REMEDY_BUDGET_MAX_WALL_CLOCK_MINUTES",
        description="Maximum wall-clock minutes for a job (F018 budgets)",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.deadline",
        env_var="REMEDY_BUDGET_DEADLINE",
        description="UTC deadline for a job as ISO 8601 string (F018 budgets)",
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="smoke.enabled",
        env_var="REMEDY_SMOKE_ENABLED",
        description=(
            "Contribute the product-smoke DoD block for projects that have a "
            "runnable app (F062). A project with no runtime is reported as "
            "not applicable either way — this switch does not make it green."
        ),
        value_type=bool,
        default=True,
    ),
    ConfigKeySpec(
        key="smoke.paths",
        env_var="REMEDY_SMOKE_PATHS",
        description=(
            "Override the core_paths_respond probe set (F062). When set, these "
            "paths REPLACE the extracted ones; the configured health path is "
            "still probed first."
        ),
        value_type=list,
        default=None,
    ),
    ConfigKeySpec(
        key="smoke.error_patterns",
        env_var="REMEDY_SMOKE_ERROR_PATTERNS",
        description=(
            "ADDITIONAL case-sensitive console error markers for clean_console "
            "(F062). Config extends the documented base list; it never "
            "replaces it, so the base guarantees cannot be configured away."
        ),
        value_type=list,
        default=None,
    ),
    ConfigKeySpec(
        key="smoke.ready_timeout_s",
        env_var="REMEDY_SMOKE_READY_TIMEOUT_S",
        description=(
            "Readiness window for the smoke's app_starts check (F062). Unset "
            "means the runtime spec's own ready_timeout_s is used."
        ),
        value_type=float,
        default=None,
    ),
    ConfigKeySpec(
        key="planning.granularity.enabled",
        env_var="REMEDY_PLANNING_GRANULARITY_ENABLED",
        description=(
            "Normalize Flight-Plan task granularity — split oversized tasks, "
            "merge trivial neighbors (F016). Disable for byte-identical "
            "pass-through of the planner's task list."
        ),
        value_type=bool,
        default=True,
    ),
    ConfigKeySpec(
        key="planning.granularity.split_band",
        env_var="REMEDY_PLANNING_GRANULARITY_SPLIT_BAND",
        description=(
            "Token band at and above which a planned task is split "
            "(S, M, L, XL) (F016)"
        ),
        value_type=str,
        default="XL",
    ),
    ConfigKeySpec(
        key="planning.granularity.max_acceptance",
        env_var="REMEDY_PLANNING_GRANULARITY_MAX_ACCEPTANCE",
        description=(
            "Acceptance-criteria count above which a planned task is split "
            "(F016)"
        ),
        value_type=int,
        default=3,
    ),
    ConfigKeySpec(
        key="cycles.max_cycles",
        env_var="REMEDY_CYCLES_MAX_CYCLES",
        description=(
            "Maximum cycles one multi-cycle run may execute (F046). "
            "DEFAULT 1 — the rollout rule: Remedy stays single-pass until the "
            "F075 milestone gate raises the cap. Both this key and "
            "'remedy job run --cycles' are capped by that safety default."
        ),
        value_type=int,
        default=1,
    ),
    ConfigKeySpec(
        key="cycles.batch_size",
        env_var="REMEDY_CYCLES_BATCH_SIZE",
        description="Maximum tasks executed per cycle (F046)",
        value_type=int,
        default=1,
    ),
    ConfigKeySpec(
        key="cycles.verify_command",
        env_var="REMEDY_CYCLES_VERIFY_COMMAND",
        description=(
            "Per-cycle verify command override (F046). Unset means the "
            "cycle's verify step is whatever the caller injected; no "
            "verification is ever claimed that did not run."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="cycles.repair_rounds",
        env_var="REMEDY_CYCLES_REPAIR_ROUNDS",
        description=(
            "Bounded auto-repair rounds a FAILED cycle verify may spend before "
            "the cycle keeps its failure (F052). DEFAULT 2. Rounds run through "
            "the existing repair loop and obey the same fences, budgets and "
            "stop requests as any other provider work; 0 disables self-healing. "
            "A verify that failed for a non-test reason (missing command, bad "
            "config) is classified and never repaired."
        ),
        value_type=int,
        default=2,
    ),
    ConfigKeySpec(
        key="cycles.checkpoint_retention",
        env_var="REMEDY_CYCLES_CHECKPOINT_RETENTION",
        description=(
            "How many per-cycle checkpoints to keep for a job (F047). "
            "The FIRST and the LATEST checkpoint are always kept on top of "
            "this count, and a checkpoint that does not verify is never "
            "pruned — it is forensic evidence."
        ),
        value_type=int,
        default=5,
    ),
    ConfigKeySpec(
        key="queue.executor_binding",
        env_var="REMEDY_QUEUE_EXECUTOR_BINDING",
        description=(
            "Let an idle multi-cycle run take the next entry from its project's "
            "queue and turn it into a normal job (F048). OFF by default: with it "
            "off the executor behaves exactly as it did before the queue existed. "
            "A queued goal still stops at a PLANNED job and still meets the "
            "operator's approval gate — the binding never implies --yes."
        ),
        value_type=bool,
        default=False,
    ),
    ConfigKeySpec(
        key="queue.reclaim_ttl_minutes",
        env_var="REMEDY_QUEUE_RECLAIM_TTL_MINUTES",
        description=(
            "How old a queue claim must be before `remedy queue reclaim` will "
            "re-offer it (F048). Age alone is never enough: the owning consumer "
            "must ALSO be verifiably gone — same host, dead pid — because a slow "
            "consumer is not an absent one, and there are no silent takeovers."
        ),
        value_type=int,
        default=60,
    ),
    ConfigKeySpec(
        key="orchestrator.model",
        env_var="REMEDY_ORCHESTRATOR_MODEL",
        description=(
            "Model for the mission orchestrator role (F070). Quality at the "
            "decision layer is the point, so this is where a top-tier model is "
            "named. Unset means the role resolves exactly like every other one "
            "— this key is the ONLY orchestrator-specific routing surface, and "
            "docs/agents/model_routing_policy.md is unchanged by it."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="orchestrator.max_iterations",
        env_var="REMEDY_ORCHESTRATOR_MAX_ITERATIONS",
        description=(
            "How many iterations one `remedy mission run` may take (F070). "
            "Conservative by default: an unattended loop that mis-decides is "
            "cheaper to stop early than to let run. Reaching the limit is a "
            "NORMAL terminal with an honest status, never a failure and never "
            "a silent continuation."
        ),
        value_type=int,
        default=10,
    ),
    ConfigKeySpec(
        key="dossier.max_tokens",
        env_var="REMEDY_DOSSIER_MAX_TOKENS",
        description=(
            "Hard token budget for a mission's dossier (F071). Conservative by "
            "default: the dossier is the PREFIX of every orchestrator prompt, "
            "so its size is a cost the mission pays once per iteration. Over "
            "budget the dossier is rewritten by compression, never truncated — "
            "a compression that fails leaves an honest over-budget flag."
        ),
        value_type=int,
        default=3000,
    ),
    ConfigKeySpec(
        key="planning.granularity.merge_group_size",
        env_var="REMEDY_PLANNING_GRANULARITY_MERGE_GROUP_SIZE",
        description=(
            "Maximum number of consecutive trivial tasks merged into one "
            "(F016)"
        ),
        value_type=int,
        default=3,
    ),
)

_KEY_SPEC_MAP: dict[str, ConfigKeySpec] = {s.key: s for s in _CONFIG_KEY_SPECS}


def get_key_spec(key: str) -> ConfigKeySpec | None:
    return _KEY_SPEC_MAP.get(key)


def all_key_specs() -> tuple[ConfigKeySpec, ...]:
    return _CONFIG_KEY_SPECS


# ---------------------------------------------------------------------------
# TOML loading
# ---------------------------------------------------------------------------

_DEFAULT_PROJECT_PATH = Path("remedy.toml")
_DEFAULT_USER_PATH = Path.home() / ".config" / "remedy" / "remedy.toml"


def _load_toml(path: Path, diagnostics: list[str] | None = None,
               *, fail_closed_for_budgets: bool = False) -> dict[str, Any]:
    """Load a TOML file and return the parsed dict. Returns {} if missing.

    When *fail_closed_for_budgets* is True AND the file exists but cannot be
    parsed, a ``BudgetConfigError`` is raised instead of silently returning {}.
    """
    if tomllib is None:
        if diagnostics is not None and path.is_file():
            diagnostics.append(f"TOML parser unavailable (install tomli for Python <3.11): {path}")
        return {}
    if not path.is_file():
        return {}
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception as exc:
        if fail_closed_for_budgets:
            from packages.orchestration.budget_resolution import BudgetConfigError
            raise BudgetConfigError(
                f"Malformed TOML in {path}: {exc}") from exc
        if diagnostics is not None:
            diagnostics.append(f"Malformed TOML in {path}: {exc}")
        return {}


def _extract_remedy_table(parsed: dict[str, Any]) -> dict[str, Any]:
    """Extract the [remedy] table from parsed TOML."""
    return parsed.get("remedy", {})


def _flatten_toml(d: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten nested TOML dict into dotted keys.

    {"ollama": {"host": "x"}} -> {"ollama.host": "x"}
    """
    result: dict[str, Any] = {}
    for k, v in d.items():
        full_key = f"{prefix}{k}" if prefix else k
        if isinstance(v, dict):
            result.update(_flatten_toml(v, f"{full_key}."))
        else:
            result[full_key] = v
    return result


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


def _coerce_value(raw: str, spec: ConfigKeySpec) -> Any:
    """Coerce a string value to the spec's type."""
    if spec.value_type is float:
        return float(raw)
    if spec.value_type is int:
        return int(raw)
    if spec.value_type is bool:
        return raw.lower() in ("1", "true", "yes")
    if spec.value_type is list:
        return [s.strip() for s in raw.split(",") if s.strip()]
    return raw


def _resolve_key(
    spec: ConfigKeySpec,
    project_flat: dict[str, Any],
    user_flat: dict[str, Any],
    *,
    all_specs: dict[str, ConfigKeySpec] | None = None,
) -> ConfigValue:
    """Resolve one key through the precedence chain."""
    env_val = os.environ.get(spec.env_var)
    if env_val is not None:
        try:
            coerced = _coerce_value(env_val, spec)
        except (ValueError, TypeError):
            coerced = env_val
        return ConfigValue(key=spec.key, value=coerced, source=ConfigSource.ENV, raw_value=env_val)

    if not spec.env_only:
        if spec.key in project_flat:
            raw = project_flat[spec.key]
            return ConfigValue(key=spec.key, value=raw, source=ConfigSource.PROJECT, raw_value=str(raw))

        if spec.key in user_flat:
            raw = user_flat[spec.key]
            return ConfigValue(key=spec.key, value=raw, source=ConfigSource.USER, raw_value=str(raw))

    if spec.fallback_key and all_specs:
        fallback_spec = all_specs.get(spec.fallback_key)
        if fallback_spec:
            fallback_val = _resolve_key(fallback_spec, project_flat, user_flat)
            if not fallback_val.is_default:
                return ConfigValue(
                    key=spec.key, value=fallback_val.value,
                    source=fallback_val.source, raw_value=fallback_val.raw_value,
                )

    return ConfigValue(key=spec.key, value=spec.default, source=ConfigSource.DEFAULT)


def _redact_abs_path(raw: str | None) -> str | None:
    """Replace absolute private paths with ~ prefix for public export."""
    if raw is None:
        return None
    p = Path(raw)
    if not p.is_absolute():
        return raw
    try:
        relative = p.relative_to(Path.home())
        return f"~/{relative}"
    except ValueError:
        return "<absolute-path-redacted>"


# ---------------------------------------------------------------------------
# RemedyConfig
# ---------------------------------------------------------------------------


@dataclass
class ConfigLoadReport:
    """Metadata about which config files were loaded."""

    project_path: str | None = None
    project_loaded: bool = False
    user_path: str | None = None
    user_loaded: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass
class RemedyConfig:
    """Main configuration object — resolved values for all known keys."""

    values: dict[str, ConfigValue] = field(default_factory=dict)
    load_report: ConfigLoadReport = field(default_factory=ConfigLoadReport)

    def get(self, key: str) -> Any:
        """Get the resolved value for a key. Returns None if unknown."""
        cv = self.values.get(key)
        return cv.value if cv is not None else None

    def get_value(self, key: str) -> ConfigValue | None:
        """Get the full ConfigValue for a key."""
        return self.values.get(key)

    def get_source(self, key: str) -> ConfigSource | None:
        """Get the source of a resolved key."""
        cv = self.values.get(key)
        return cv.source if cv is not None else None

    def to_summary_dict(self) -> dict[str, Any]:
        """Export config as safe summary dict for review bundle / diagnostics.

        Absolute paths are redacted with ~ prefix or tag to avoid leaking
        private filesystem layout.
        """
        entries = []
        for spec in _CONFIG_KEY_SPECS:
            cv = self.values.get(spec.key)
            if cv is None:
                continue
            val_display = cv.value
            if spec.secret or spec.env_only:
                val_display = "[REDACTED]" if cv.value is not None else None
            entries.append({
                "key": spec.key,
                "value": val_display,
                "source": cv.source.value,
                "env_var": spec.env_var,
                "is_default": cv.is_default,
            })
        return {
            "config_version": 0,
            "keys": entries,
            "load_report": {
                "project_path": _redact_abs_path(self.load_report.project_path),
                "project_loaded": self.load_report.project_loaded,
                "user_path": _redact_abs_path(self.load_report.user_path),
                "user_loaded": self.load_report.user_loaded,
                "warnings": self.load_report.warnings,
            },
        }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_CACHED_CONFIG: RemedyConfig | None = None


def load_config(
    project_path: Path | None = None,
    user_path: Path | None = None,
) -> RemedyConfig:
    """Load and resolve all config from TOML files + env vars.

    Args:
        project_path: Path to project remedy.toml. Default: ./remedy.toml.
        user_path: Path to user remedy.toml. Default: ~/.config/remedy/remedy.toml.
    """
    p_path = project_path or _DEFAULT_PROJECT_PATH
    u_path = user_path or _DEFAULT_USER_PATH

    diagnostics: list[str] = []

    project_raw = _load_toml(p_path, diagnostics, fail_closed_for_budgets=True)
    user_raw = _load_toml(u_path, diagnostics, fail_closed_for_budgets=True)

    project_flat = _flatten_toml(_extract_remedy_table(project_raw))
    user_flat = _flatten_toml(_extract_remedy_table(user_raw))

    for key in project_flat:
        if key not in _KEY_SPEC_MAP:
            if key.startswith("budget."):
                from packages.orchestration.budget_resolution import BudgetConfigError
                raise BudgetConfigError(
                    f"Unknown budget config key in {p_path}: {key!r}")
            diagnostics.append(f"Unknown key in {p_path}: {key}")
    for key in user_flat:
        if key not in _KEY_SPEC_MAP:
            if key.startswith("budget."):
                from packages.orchestration.budget_resolution import BudgetConfigError
                raise BudgetConfigError(
                    f"Unknown budget config key in {u_path}: {key!r}")
            diagnostics.append(f"Unknown key in {u_path}: {key}")

    report = ConfigLoadReport(
        project_path=str(p_path),
        project_loaded=bool(project_raw),
        user_path=str(u_path),
        user_loaded=bool(user_raw),
        warnings=diagnostics,
    )

    values: dict[str, ConfigValue] = {}
    for spec in _CONFIG_KEY_SPECS:
        values[spec.key] = _resolve_key(spec, project_flat, user_flat, all_specs=_KEY_SPEC_MAP)

    config = RemedyConfig(values=values, load_report=report)
    return config


def get_config() -> RemedyConfig:
    """Get or load the cached global config."""
    global _CACHED_CONFIG
    if _CACHED_CONFIG is None:
        _CACHED_CONFIG = load_config()
    return _CACHED_CONFIG


def reset_config() -> None:
    """Clear the cached config — forces reload on next get_config() call."""
    global _CACHED_CONFIG
    _CACHED_CONFIG = None


def write_toml_template(path: Path) -> None:
    """Write a remedy.toml template file."""
    template = """\
# Remedy Configuration
# See: docs/remedy-toml-configuration-system-v0.md

[remedy]
# data_dir = ".data"

[remedy.ollama]
# host = "http://localhost:11434"
# model = "qwen3-coder-next"

# [remedy.ollama.builder]
# model = "qwen3-coder-next"
# temperature = 0.3
# num_predict = 4096

# [remedy.ollama.planner]
# model = "qwen3-coder-next"
# temperature = 0.2
# num_predict = 4096

[remedy.ui]
# host = "127.0.0.1"
# port = 8765

[remedy.tests]
# pytest_timeout_seconds = 300

[remedy.quality]
# coverage_fail_under = 80

[remedy.logging]
# level = "WARNING"
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template, encoding="utf-8")


def set_config_value(path: Path, key: str, value: str) -> None:
    """Set a key in a remedy.toml file.

    Creates the file if it does not exist. Rejects unknown keys, secret keys,
    and env-only keys.
    """
    spec = get_key_spec(key)
    if spec is None:
        raise ValueError(f"Unknown config key: {key!r}. Use 'config list' to see valid keys.")
    if spec.env_only:
        raise ValueError(f"Key {key!r} is env-only and cannot be set in config files")
    if spec.secret:
        raise ValueError(f"Key {key!r} is secret and cannot be stored in config files")

    existing = _load_toml(path)
    remedy_table = existing.setdefault("remedy", {})

    parts = key.split(".")
    target = remedy_table
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value

    lines = ["# Remedy Configuration\n\n"]
    _serialize_toml(existing, lines, depth=0)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")


def _serialize_toml(d: dict[str, Any], lines: list[str], depth: int, prefix: str = "") -> None:
    """Minimal TOML serializer for remedy config (no external dependency)."""
    for k, v in d.items():
        if isinstance(v, dict):
            table_key = f"{prefix}{k}" if prefix else k
            lines.append(f"\n[{table_key}]\n")
            _serialize_toml(v, lines, depth + 1, f"{table_key}.")
        elif isinstance(v, bool):
            lines.append(f"{k} = {'true' if v else 'false'}\n")
        elif isinstance(v, int):
            lines.append(f"{k} = {v}\n")
        elif isinstance(v, float):
            lines.append(f"{k} = {v}\n")
        else:
            lines.append(f'{k} = "{v}"\n')


def validate_config(config: RemedyConfig) -> list[str]:
    """Validate config values against key specs. Returns list of warnings."""
    warnings: list[str] = []
    for spec in _CONFIG_KEY_SPECS:
        cv = config.values.get(spec.key)
        if cv is None:
            continue
        if cv.value is None:
            continue
        if spec.value_type is float:
            try:
                float(str(cv.value))
            except (ValueError, TypeError):
                warnings.append(f"{spec.key}: expected float, got {type(cv.value).__name__}")
        elif spec.value_type is int:
            try:
                int(str(cv.value))
            except (ValueError, TypeError):
                warnings.append(f"{spec.key}: expected int, got {type(cv.value).__name__}")
    return warnings

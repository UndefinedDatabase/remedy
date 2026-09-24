"""
Centralized configuration for Remedy — remedy.toml + env var precedence.

Source precedence (highest to lowest):
  1. Environment variable (REMEDY_*)
  2. Project config (./remedy.toml)
  3. User config (~/.config/remedy/remedy.toml)
  4. Built-in default

TABLE-VALUED KEYS. A key registered with ``value_type is dict`` resolves to a
WHOLE TOML SUB-TABLE as ONE value, through the same precedence chain every other
key uses, instead of being flattened into one unregistered key per entry. The
set of such keys is DERIVED FROM THE REGISTRY ITSELF (see ``_TABLE_VALUED_KEYS``)
and is never hand-listed, so registering a second table key is one registry entry
and no second edit. An environment variable cannot carry a table, so a
table-valued key is configured in TOML only — its ``env_var`` exists for the
uniform spec shape, and a string arriving through it is reported as a shape fault
by :func:`validate_config` rather than silently read as a table. Such a key also
DECLARES WHAT ITS ENTRIES HOLD, through ``ConfigKeySpec.entry_type`` — ``str``
for a flat map, ``dict`` for a table of records, ``None`` for entries left
unchecked — because one entry-shape rule cannot serve both kinds of table.

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
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.model_aliases import resolve_model_alias

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

    value_type supports: str, int, float, bool, list, dict.
    When value_type is list, values are list-of-strings. Env var values
    are split on commas. TOML arrays are used as-is.
    When value_type is dict the key is TABLE-VALUED: the whole TOML sub-table
    named by ``key`` resolves as one value (see the module docstring), and TOML
    is the only source that can carry it.

    ``entry_type`` names the type each ENTRY of such a table holds — ``str`` for
    a flat map of strings, ``dict`` for a table of RECORDS — and defaults to
    ``None``, which means the entries are not shape-checked at all. IT IS A
    PER-KEY DECLARATION AND NOT ONE RULE FOR EVERY TABLE, because both kinds of
    table are well formed: checking every table's entries as strings reports a
    perfectly good record table as a fault, and hard-coding a key NAME inside
    :func:`validate_config` would put routing policy in this, the lower, layer.
    """

    key: str
    env_var: str
    description: str
    value_type: type = str
    entry_type: type | None = None
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
    # The built-in Ollama default. Resolved from the single alias table
    # (packages/orchestration/model_aliases.py) so no concrete model id is
    # spelled out here; an upgrade repoints the alias, not this registry.
    ConfigKeySpec(
        key="ollama.model",
        env_var="REMEDY_OLLAMA_MODEL",
        description="Default Ollama model for all roles",
        value_type=str,
        default=resolve_model_alias("ollama-default"),
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
        key="ui.command_rate_limit_per_minute",
        env_var="REMEDY_UI_COMMAND_RATE_LIMIT_PER_MINUTE",
        description=(
            "Commands the UI write door accepts for one token fingerprint and "
            "one job per minute (DECISION F009 D9). The excess is refused with "
            "429 rather than made to wait, because an inbound request is "
            "holding a connection. 30 is the default because a human cockpit "
            "stays an order of magnitude below it — an operator clicking a "
            "control manages a few commands a minute — while a client stuck in "
            "a retry loop is stopped inside two seconds of real traffic."
        ),
        value_type=int,
        default=30,
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
    # F279 T001 (DECISION F279 D2): every REMEDY_ name production code reads is registered
    # here, so the entries below are the env-only variables that were read before they were
    # listed. tests/orchestration/test_env_registry.py holds the line.
    ConfigKeySpec(
        key="agent_dir",
        env_var="REMEDY_AGENT_DIR",
        description=(
            "Directory of the .agent state files the self-dogfood inspection reads; the "
            "inspection also sets it for its own children (env-only)"
        ),
        value_type=str,
        default=".agent",
        env_only=True,
    ),
    ConfigKeySpec(
        key="claude_planner.model",
        env_var="REMEDY_CLAUDE_PLANNER_MODEL",
        description=(
            "Model for the Claude CLI planner; beats planner.model and the alias table's "
            "default (env-only)"
        ),
        value_type=str,
        default=None,
        env_only=True,
    ),
    ConfigKeySpec(
        key="claude_planner.timeout_seconds",
        env_var="REMEDY_CLAUDE_PLANNER_TIMEOUT",
        description=(
            "Per-call wall timeout of the Claude CLI planner, in whole seconds (env-only)"
        ),
        value_type=int,
        default=300,
        env_only=True,
    ),
    ConfigKeySpec(
        key="planner.freetext",
        env_var="REMEDY_PLANNER_FREETEXT",
        description=(
            "Legacy free-text planner parsing instead of the structured plan schema "
            "(env-only flag)"
        ),
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="reviewer.freetext",
        env_var="REMEDY_REVIEWER_FREETEXT",
        description=(
            "Legacy free-text reviewer parsing instead of the structured review schema "
            "(env-only flag)"
        ),
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="project",
        env_var="REMEDY_PROJECT",
        description=(
            "Registered project a command acts on, as UUID or slug, before cwd "
            "autodetection (env-only)"
        ),
        value_type=str,
        default=None,
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.runner_timeout_seconds",
        env_var="REMEDY_PYTEST_TIMEOUT_SEC",
        description=(
            "Wall budget of one scripts/remedy_pytest_runner.py run, which every CI stage "
            "goes through; a different budget from tests.pytest_timeout_seconds (env-only)"
        ),
        value_type=int,
        default=600,
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.runner_python",
        env_var="REMEDY_PYTHON",
        description=(
            "Python interpreter scripts/remedy_pytest_runner.py runs pytest under; the "
            "runner's own interpreter when unset (env-only)"
        ),
        value_type=str,
        default=None,
        env_only=True,
    ),
    ConfigKeySpec(
        key="review.base",
        env_var="REMEDY_REVIEW_BASE",
        description=(
            "Git base the review subject is diffed against; an invalid base is refused, "
            "never ignored (env-only)"
        ),
        value_type=str,
        default=None,
        env_only=True,
    ),
    ConfigKeySpec(
        key="runtime.log_max_bytes",
        env_var="REMEDY_RUNTIME_LOG_MAX",
        description=(
            "Byte cap on a supervised runtime's captured log; uncapped when unset "
            "(env-only)"
        ),
        value_type=int,
        default=None,
        env_only=True,
    ),
    ConfigKeySpec(
        key="runtime.port",
        env_var="REMEDY_RUNTIME_PORT",
        description=(
            "Port a supervised runtime is started on, overriding the one its spec declares "
            "(env-only)"
        ),
        value_type=int,
        default=None,
        env_only=True,
    ),
    ConfigKeySpec(
        key="events.strict_names",
        env_var="REMEDY_STRICT_EVENT_NAMES",
        description=(
            "Refuse a run-log event whose name is not declared; tests only, a job never "
            "fails a ledger write on it (env-only flag)"
        ),
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="ui.allow_legacy_fallback",
        env_var="REMEDY_UI_ALLOW_LEGACY_FALLBACK",
        description=(
            "Serve the legacy app shell when the built UI is missing, with a warning "
            "(env-only flag)"
        ),
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="ui.demo_mode",
        env_var="REMEDY_UI_DEMO_MODE",
        description=(
            "Label the cockpit's synthetic placeholder data as demo data (env-only flag)"
        ),
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="ui.no_auto_build",
        env_var="REMEDY_UI_NO_AUTO_BUILD",
        description="Skip the UI server's automatic npm build of apps/ui (env-only flag)",
        value_type=bool,
        default=False,
        env_only=True,
    ),
    # F279 T001 (DECISION F279 D3): the names the shell scripts under scripts/ read, and the two
    # opt-ins an operator sets to run the real-Ollama tests, so `remedy doctor core` never calls a
    # variable Remedy itself reads unknown.
    ConfigKeySpec(
        key="tests.runtime_node_timeout_seconds",
        env_var="REMEDY_NODE_TIMEOUT_SEC",
        description=(
            "Outer wall timeout of each node scripts/remedy_test_runtime.sh runs, in "
            "seconds (env-only)"
        ),
        value_type=int,
        default=90,
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.pytest_lock_file",
        env_var="REMEDY_PYTEST_LOCK",
        description=(
            "Lock file scripts/remedy_pytest.sh and scripts/remedy_coverage.sh hold so two "
            "suite runs never overlap (env-only)"
        ),
        value_type=str,
        default="/tmp/remedy-pytest.lock",
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.pytest_lock_wait_seconds",
        env_var="REMEDY_PYTEST_LOCK_WAIT",
        description=(
            "Seconds scripts/remedy_pytest.sh waits for that lock; 0 refuses at once "
            "(env-only)"
        ),
        value_type=int,
        default=0,
        env_only=True,
    ),
    ConfigKeySpec(
        key="review.package_dir",
        env_var="REMEDY_REVIEW_DIR",
        description=(
            "Directory scripts/make_review_zip.sh writes review packages to; a relative "
            "path is read from the repository root, and $HOME/Repos/remedy-history/zips is "
            "used when unset (env-only)"
        ),
        value_type=str,
        default=None,
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.run_real_ollama",
        env_var="REMEDY_RUN_REAL_OLLAMA",
        description=(
            "Run scripts/remedy_test_real_providers.sh against a real Ollama server instead "
            "of skipping (env-only flag)"
        ),
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.smoke_repo",
        env_var="REMEDY_SMOKE_REPO",
        description=(
            "Scratch repository scripts/remedy_smoke.sh builds and drives (env-only)"
        ),
        value_type=str,
        default="/tmp/remedy-target-repo",
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.smoke_unload_models",
        env_var="REMEDY_SMOKE_UNLOAD_MODELS",
        description=(
            "Unload the Ollama models scripts/remedy_smoke.sh loaded when it ends (env-only "
            "flag)"
        ),
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.real_ollama_smoke",
        env_var="REMEDY_REAL_OLLAMA_SMOKE",
        description=(
            "Opt in to the real-Ollama smoke tests, which need a running Ollama server with "
            "a model (env-only flag)"
        ),
        value_type=bool,
        default=False,
        env_only=True,
    ),
    ConfigKeySpec(
        key="tests.smoke_ollama",
        env_var="REMEDY_SMOKE_OLLAMA",
        description="Opt in to the real-Ollama builder bridge smoke test (env-only flag)",
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
        key="budget.max_cost_usd",
        env_var="REMEDY_BUDGET_MAX_COST_USD",
        description="Maximum cost in USD for a job (F104 budgets)",
        value_type=float,
        default=None,
    ),
    # F276 T004. The default is None — no floor — for the reason DECISION F276 D7
    # records: every other budget key defaults to None, `resolve_job_budgets`
    # returns None when they all do, and a number here would hand a JobBudgets to
    # every job that has none today.
    ConfigKeySpec(
        key="budget.min_free_disk_bytes",
        env_var="REMEDY_BUDGET_MIN_FREE_DISK_BYTES",
        description=(
            "Free bytes that must remain on the data root's filesystem for a job "
            "to start and to pass a safe point (F276 disk floor)"
        ),
        value_type=int,
        default=None,
    ),
    # F104 predictive inputs. The price basis has NO default on purpose
    # (DECISION F104 D4): an invented price would make every prediction a
    # fabrication, so with it unset the predictive path is inert.
    ConfigKeySpec(
        key="budget.price_basis_usd_per_1k_tokens",
        env_var="REMEDY_BUDGET_PRICE_BASIS_USD_PER_1K_TOKENS",
        description=(
            "Provisional USD price per 1000 tokens used for cost predictions "
            "(F104; provisional until calibration)"
        ),
        value_type=float,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.class_default_tokens_low",
        env_var="REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_LOW",
        description=(
            "Expected tokens for a low-band task "
            "(F104; provisional until calibration)"
        ),
        value_type=int,
        default=8000,
    ),
    ConfigKeySpec(
        key="budget.class_default_tokens_medium",
        env_var="REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_MEDIUM",
        description=(
            "Expected tokens for a medium-band task "
            "(F104; provisional until calibration)"
        ),
        value_type=int,
        default=32000,
    ),
    ConfigKeySpec(
        key="budget.class_default_tokens_high",
        env_var="REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_HIGH",
        description=(
            "Expected tokens for a high-band task "
            "(F104; provisional until calibration)"
        ),
        value_type=int,
        default=120000,
    ),
    ConfigKeySpec(
        key="cost_preview.confirm_above_usd",
        env_var="REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD",
        description=(
            "USD threshold above which an expensive command's cost preview "
            "requires operator confirmation before it runs (F114)"
        ),
        value_type=float,
        default=0.5,
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
            "Normalize Task-Plan task granularity — split oversized tasks, "
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
            "'remedy job resume --cycles' are capped by that safety default."
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
        key="self_use.provider",
        env_var="REMEDY_SELF_USE_PROVIDER",
        description=(
            "Provider for BOTH the builder and the reviewer of a self-use run "
            "(operator amendment amend0920-selfuse-real, DECISION D2). Unset "
            "means `claude-cli`: a self-use run repairs THIS repository, which "
            "is frontier work, and five consecutive runs on the local model "
            "(SU-019 to SU-023) landed nothing. Set it to `ollama` to put the "
            "track back on the local model."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="self_use.model",
        env_var="REMEDY_SELF_USE_MODEL",
        description=(
            "Model for both roles of a self-use run (operator amendment "
            "amend0920-selfuse-real, DECISION D2). Unset means the alias "
            "table's Sonnet alias, which the run's cost bound of at most 8 "
            "provider calls and 1.00 USD per closure is written for."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="planner.provider",
        env_var="REMEDY_PLANNER_PROVIDER",
        description=(
            "Which service does the structured planning: `ollama` or "
            "`claude-cli` (operator amendment amend0920-selfuse-real, DECISION "
            "D1). Read by `packages.orchestration.intake.make_structured_call_fn` "
            "when no `--planner-provider` was given. Unset means `ollama`, the "
            "only planner Remedy had before the second one existed, so an "
            "unconfigured repository plans exactly as it always did."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="planner.model",
        env_var="REMEDY_PLANNER_MODEL",
        description=(
            "Model for the planner role, whichever service serves it (operator "
            "amendment amend0920-selfuse-real, DECISION D1). Unset lets the "
            "selected planner resolve its own default — the `ollama-default` "
            "alias for Ollama, which also honours `ollama.planner.model`, and "
            "the `claude-workhorse` alias for the Claude CLI."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="teacher.model",
        env_var="REMEDY_TEACHER_MODEL",
        description=(
            "Model for the teacher role (F255). The teacher reads and explains "
            "and never writes, so this key buys explanation quality and nothing "
            "else. Unset means the role resolves exactly like every other one. "
            "Stage 1 narration is deterministic and spends nothing, so nothing "
            "reads this key until the Stage 2 question path exists (T004) — a "
            "declared key with no reader yet, not a forgotten wiring."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="teacher.lessons",
        env_var="REMEDY_TEACHER_LESSONS",
        description=(
            "Write a lesson from the real diff after every completed task (F265). "
            "Off by default: each lesson is one teacher model call, and a run makes "
            "no call the operator did not switch on."
        ),
        value_type=bool,
        default=False,
    ),
    ConfigKeySpec(
        key="teacher.lesson_max_calls",
        env_var="REMEDY_TEACHER_LESSON_MAX_CALLS",
        description=(
            "The teacher's budget pot per job, in calls (F265): once the job's "
            "teacher calls reach it, a completed task gets an empty lesson that "
            "says the pot is spent."
        ),
        value_type=int,
        default=30,
    ),
    ConfigKeySpec(
        key="teacher.lesson_max_tokens",
        env_var="REMEDY_TEACHER_LESSON_MAX_TOKENS",
        description=(
            "The teacher's budget pot per job, in the tokens its calls reported "
            "(F265); a call that reports none still counts against the call limit."
        ),
        value_type=int,
        default=300000,
    ),
    ConfigKeySpec(
        key="watchdog.no_progress_repeats",
        env_var="REMEDY_WATCHDOG_NO_PROGRESS_REPEATS",
        description=(
            "How many dispatches in a row on ONE milestone, with no milestone "
            "declared done between them, count as no progress (F077). "
            "Conservative by default: three identical attempts is already a "
            "loop arguing with itself, and the watchdog only ever pauses the "
            "mission for a human — it never repairs what it stopped."
        ),
        value_type=int,
        default=3,
    ),
    ConfigKeySpec(
        key="watchdog.burn_window",
        env_var="REMEDY_WATCHDOG_BURN_WINDOW",
        description=(
            "How many of the most recent MEASURED iterations form the burn "
            "window the watchdog compares against the mission's own baseline "
            "(F077). Conservative by default: three smooths a single "
            "expensive iteration without hiding a sustained run-away. The "
            "tripwire stays inert below watchdog.burn_min_samples."
        ),
        value_type=int,
        default=3,
    ),
    ConfigKeySpec(
        key="watchdog.burn_min_samples",
        env_var="REMEDY_WATCHDOG_BURN_MIN_SAMPLES",
        description=(
            "How many measured iterations must sit BEFORE the window before "
            "the burn tripwire is allowed to fire at all (F077). "
            "Conservative by default: a baseline of five is the smallest one "
            "worth comparing to. Below it the tripwire is inert — thin data "
            "produces no trip, never a trip on thin data."
        ),
        value_type=int,
        default=5,
    ),
    ConfigKeySpec(
        key="watchdog.burn_multiplier",
        env_var="REMEDY_WATCHDOG_BURN_MULTIPLIER",
        description=(
            "How many times the baseline mean the window mean must STRICTLY "
            "exceed before the burn tripwire fires (F077). Conservative by "
            "default: 3x tolerates the normal spread between a cheap and an "
            "expensive iteration, so an alarm means something. The tripwire "
            "is inert below watchdog.burn_min_samples whatever this reads."
        ),
        value_type=float,
        default=3.0,
    ),
    ConfigKeySpec(
        key="doctor.dead_models",
        env_var="REMEDY_DOCTOR_DEAD_MODELS",
        description=(
            "ADDITIONAL known-dead model ids for the doctor's model check "
            "(F254). Config EXTENDS the shipped list in scripts/dead_models.json; "
            "it never replaces it, so an id Remedy already ships as dead cannot "
            "be configured away. The list is operator-maintained data — Remedy "
            "never probes a provider to build it."
        ),
        value_type=list,
        default=None,
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
    # F110's per-project override map, and the first TABLE-VALUED key in this
    # registry. The DEFAULT IS None AND NOT AN EMPTY TABLE on purpose: "no
    # override configured" and "an override table that is explicitly empty" are
    # different operator statements, and collapsing them would lose the one the
    # routing layer reports on.
    ConfigKeySpec(
        key="model_routing.task_class_tiers",
        env_var="REMEDY_MODEL_ROUTING_TASK_CLASS_TIERS",
        description=(
            "Per-project TASK CLASS to MODEL TIER map (F110). The whole "
            "[remedy.model_routing.task_class_tiers] sub-table resolves as ONE "
            "value and is laid over the shipped seed mapping in "
            "packages/orchestration/model_routing.py. The hard rules of "
            "docs/agents/model_routing_policy.md still win: a map that breaks "
            "one is REFUSED with the rule named and the shipped table is used. "
            "Configured in TOML only — an env var cannot carry a table."
        ),
        value_type=dict,
        entry_type=str,
        default=None,
    ),
    # F110's PROMOTION-EVIDENCE table, and the first table of RECORDS in this
    # registry: every entry is itself a sub-table, so it declares entry_type
    # dict where its sibling above declares str. THE READER NOW EXISTS: it is
    # role_config.resolve_promotion_evidence, which landed at 8efa2330 in
    # packages/orchestration/role_config.py beside the one that already reads
    # the tiers table. It is registered first, on purpose, so the schema is
    # pinned before routing behaviour moves against it.
    ConfigKeySpec(
        key="model_routing.promotion_evidence",
        env_var="REMEDY_MODEL_ROUTING_PROMOTION_EVIDENCE",
        description=(
            "Per-project TASK CLASS to BENCHMARK RUN map (F110). Each entry of "
            "the [remedy.model_routing.promotion_evidence] sub-table is itself a "
            "table: the documented run that LICENSES A CHEAPER TIER for that "
            "class, as docs/agents/model_routing_policy.md's 'Promotion rule' "
            "describes it. Whether a run clears the promotion bars is decided in "
            "packages/orchestration/model_routing.py, never here. Configured in "
            "TOML only — an env var cannot carry a table."
        ),
        value_type=dict,
        entry_type=dict,
        default=None,
    ),
    # F112's per-class input-token cap table and its global fallback scalar.
    # Reuses the shared task-class vocabulary TASK_CLASS_TIERS declares
    # (packages/orchestration/model_routing.py) — the floor and vocabulary
    # checks specific to this feature live in
    # packages/orchestration/prompt_budget.py, not here (DECISION F110 D5
    # precedent: policy-level validation stays out of config.py).
    ConfigKeySpec(
        key="prompt_budget.task_class_caps",
        env_var="REMEDY_PROMPT_BUDGET_TASK_CLASS_CAPS",
        description=(
            "Per-task-class input token cap overrides (F112). Each entry's "
            "basis is class_default until F074 calibration ships measured "
            "caps. Configured in TOML only — an env var cannot carry a "
            "table."
        ),
        value_type=dict,
        entry_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="prompt_budget.default_cap",
        env_var="REMEDY_PROMPT_BUDGET_DEFAULT_CAP",
        description=(
            "Global fallback input token cap (F112) for a task class "
            "carrying no configured per-class cap. Falls back further to "
            "packages.orchestration.prompt_budget.DEFAULT_FALLBACK_CAP_TOKENS "
            "when unset."
        ),
        value_type=int,
        default=None,
    ),
    # DECISION F270 D3 (7): registered here, read only by push_after_mission_enabled.
    ConfigKeySpec(
        key="apply.push_after_mission",
        env_var="REMEDY_APPLY_PUSH_AFTER_MISSION",
        description=(
            "Push the branch a mission's commit landed on to its configured "
            "upstream at the end of the mission, exactly as --push would (F270)."
        ),
        value_type=bool,
        default=False,
    ),
)

_KEY_SPEC_MAP: dict[str, ConfigKeySpec] = {s.key: s for s in _CONFIG_KEY_SPECS}

#: The TABLE-VALUED keys, DERIVED FROM THE REGISTRY rather than hand-listed: a
#: key is table-valued when, and only when, its spec says ``value_type is dict``.
#: :func:`_flatten_toml` stops recursing at one of these, so its sub-table
#: survives as a single value. Deriving it here is what makes registering a
#: SECOND table key a one-line change to the registry above and nothing else —
#: a hand-written list would be a second place to forget.
_TABLE_VALUED_KEYS: frozenset[str] = frozenset(
    spec.key for spec in _CONFIG_KEY_SPECS if spec.value_type is dict
)


def get_key_spec(key: str) -> ConfigKeySpec | None:
    return _KEY_SPEC_MAP.get(key)


def all_key_specs() -> tuple[ConfigKeySpec, ...]:
    return _CONFIG_KEY_SPECS


# ---------------------------------------------------------------------------
# The environment against the registry (F279 T001, DECISION F279 D3)
# ---------------------------------------------------------------------------

#: The values a boolean variable reads as True. :func:`_coerce_value` reads every other value as
#: False, so only the words below say what they mean; anything else is reported unparsable.
BOOL_TRUE_WORDS: tuple[str, ...] = ("1", "true", "yes")
BOOL_FALSE_WORDS: tuple[str, ...] = ("0", "false", "no", "")
ENV_PREFIX = "REMEDY_"

#: How each declared type is named to a person, in the guide and in `remedy doctor core`.
_TYPE_WORDS: dict[type, str] = {
    int: "a whole number",
    float: "a number",
    bool: "yes or no (1, true, yes / 0, false, no)",
    list: "a comma-separated list",
    dict: "a table, which only remedy.toml can carry",
    str: "text",
}


def type_words(spec: ConfigKeySpec) -> str:
    return _TYPE_WORDS[spec.value_type]


def env_value_parses(raw: str, spec: ConfigKeySpec) -> bool:
    """Whether `raw` reads as `spec`'s declared type the way :func:`_coerce_value` reads it."""
    if spec.value_type is int:
        try:
            int(raw)
        except ValueError:
            return False
        return True
    if spec.value_type is float:
        try:
            float(raw)
        except ValueError:
            return False
        return True
    if spec.value_type is bool:
        return raw.lower() in BOOL_TRUE_WORDS + BOOL_FALSE_WORDS
    if spec.value_type is dict:
        return False
    return True


_ENV_SPEC_MAP: dict[str, ConfigKeySpec] = {spec.env_var: spec for spec in _CONFIG_KEY_SPECS}


def env_value(name: str, environ: Mapping[str, str] | None = None) -> Any:
    """The registered variable `name`, read from the LIVE environment as its declared type.

    Live, and never through the cached :func:`get_config`, because every caller reads a value
    the process or a test may set after the configuration was first loaded. When the variable
    is unset, an env-only variable answers its spec's default, and any other answers None so
    that its caller goes on to the next source, `remedy.toml`. A boolean reads as yes only for
    the words in ``BOOL_TRUE_WORDS``, exactly as :func:`_coerce_value` reads it. A whole number
    or a number that does not parse raises ValueError naming the variable and the type it must
    be, rather than guessing. A name no spec registers raises KeyError: a read the registry
    cannot see is the drift F279 T001 ends (DECISION F279 D4).
    """
    spec = _ENV_SPEC_MAP.get(name)
    if spec is None:
        raise KeyError(f"{name} is not a registered Remedy variable")
    raw = (os.environ if environ is None else environ).get(name)
    if raw is None:
        return spec.default if spec.env_only else None
    if spec.value_type is bool:
        return raw.lower() in BOOL_TRUE_WORDS
    if spec.value_type in (int, float):
        try:
            return spec.value_type(raw)
        except ValueError:
            raise ValueError(
                f"Environment variable {name} must be {type_words(spec)} (got {raw!r})") from None
    if spec.value_type is list:
        return [part.strip() for part in raw.split(",") if part.strip()]
    if spec.value_type is dict:
        raise ValueError(f"Environment variable {name} cannot carry a table; set it in remedy.toml")
    return raw


def unknown_env_variables(environ: Mapping[str, str]) -> list[tuple[str, str | None]]:
    """Every `REMEDY_` name set in `environ` that no spec registers, with its closest registered name.

    Names are compared after the shared prefix, which every candidate carries and which would
    otherwise make every name look close to every other.
    """
    import difflib

    registered = {spec.env_var for spec in _CONFIG_KEY_SPECS}
    suffixes = {name[len(ENV_PREFIX):]: name for name in registered}
    found: list[tuple[str, str | None]] = []
    for name in sorted(environ):
        if not name.startswith(ENV_PREFIX) or name in registered:
            continue
        close = difflib.get_close_matches(name[len(ENV_PREFIX):], sorted(suffixes), n=1, cutoff=0.6)
        found.append((name, suffixes[close[0]] if close else None))
    return found


def unparsable_env_variables(environ: Mapping[str, str]) -> list[tuple[str, ConfigKeySpec]]:
    """Every registered variable set in `environ` whose value does not read as its declared type."""
    return [(spec.env_var, spec) for spec in sorted(_CONFIG_KEY_SPECS, key=lambda s: s.env_var)
            if spec.env_var in environ and not env_value_parses(environ[spec.env_var], spec)]


ENVIRONMENT_GUIDE_PATH = "docs/guides/environment.md"


def _guide_default(spec: ConfigKeySpec) -> str:
    if spec.default is None:
        return "none"
    if spec.value_type is bool:
        return "yes" if spec.default else "no"
    return f"`{spec.default}`"


def render_environment_guide() -> str:
    """`docs/guides/environment.md`, rendered from the registry; the committed file must equal it."""
    lines = [
        "# Environment Variables",
        "",
        "> GENERATED from the key registry in `packages/orchestration/config.py` by",
        "> `render_environment_guide()`. Do not edit it by hand:",
        "> `tests/docs/test_environment_guide.py` fails whenever the registry and this file differ.",
        "> Regenerate it from the repository root with",
        "> `python3 -c \"from packages.orchestration.config import write_environment_guide; "
        "write_environment_guide()\"`.",
        "",
        "Every environment variable Remedy reads is listed here, once. A variable set in the",
        "environment wins over the same setting in `remedy.toml`, and `remedy.toml` wins over the",
        "built-in default. A variable marked env-only has no `remedy.toml` key and can only be set",
        "in the environment. `remedy doctor core` warns about a `REMEDY_` variable that is not in",
        "this list, naming the closest one that is, and about a listed variable whose value does",
        "not read as its type; neither warning stops Remedy from running.",
        "",
        "| Variable | Type | Default | remedy.toml key | Description |",
        "|---|---|---|---|---|",
    ]
    for spec in sorted(_CONFIG_KEY_SPECS, key=lambda s: s.env_var):
        key = "env-only" if spec.env_only else f"`{spec.key}`"
        description = " ".join(spec.description.split()).replace("|", "\\|")
        lines.append(f"| `{spec.env_var}` | {type_words(spec)} | {_guide_default(spec)} | {key} "
                     f"| {description} |")
    return "\n".join(lines) + "\n"


def write_environment_guide(root: Path | None = None) -> Path:
    """Write the rendered guide under `root` (the repository root by default) and return its path."""
    base = root if root is not None else Path(__file__).resolve().parents[2]
    path = base / ENVIRONMENT_GUIDE_PATH
    path.write_text(render_environment_guide(), encoding="utf-8")
    return path


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


def _flatten_toml(
    d: dict[str, Any],
    prefix: str = "",
    table_valued_keys: frozenset[str] = _TABLE_VALUED_KEYS,
) -> dict[str, Any]:
    """Flatten nested TOML dict into dotted keys.

    {"ollama": {"host": "x"}} -> {"ollama.host": "x"}

    THE RECURSION STOPS at a key in ``table_valued_keys`` — by default the keys
    :data:`_TABLE_VALUED_KEYS` derived from the registry. Such a sub-table is
    carried through WHOLE, as one value under its own dotted key, instead of
    becoming one dotted key per entry. Without that stop, every entry of a
    project's table would be an unregistered key and ``load_config`` would
    report one "Unknown key in ..." diagnostic per entry for a config that is
    perfectly well formed.

    The set is a PARAMETER so a caller — a test above all — can flatten against
    a different registry without monkeypatching a module constant.
    """
    result: dict[str, Any] = {}
    for k, v in d.items():
        full_key = f"{prefix}{k}" if prefix else k
        if isinstance(v, dict) and full_key not in table_valued_keys:
            result.update(_flatten_toml(v, f"{full_key}.", table_valued_keys))
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
        return raw.lower() in BOOL_TRUE_WORDS
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


def push_after_mission_enabled(config: RemedyConfig | None = None) -> bool:
    """True only when the operator set ``apply.push_after_mission`` to a true value.

    DECISION F270 D3 (7). A TOML boolean is read as it is; a string — the env
    var, a quoted TOML value — is true only for ``1``, ``true`` or ``yes``, so
    the string ``"false"`` is false. Any other value is false: Remedy never
    pushes on a value it cannot read. ``job apply`` never calls this.
    """
    value = (config if config is not None else get_config()).get("apply.push_after_mission")
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes")
    return False


def write_toml_template(path: Path) -> None:
    """Write a remedy.toml template file."""
    template = """\
# Remedy Configuration
# See: docs/remedy-toml-configuration-system-v0.md

[remedy]
# data_dir = ".data"

[remedy.ollama]
# host = "http://localhost:11434"
# model = "<your-ollama-model>"

# [remedy.ollama.builder]
# model = "<your-ollama-model>"
# temperature = 0.3
# num_predict = 4096

# [remedy.ollama.planner]
# model = "<your-ollama-model>"
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
    """Validate config values against key specs. Returns list of warnings.

    A TABLE-VALUED key is validated for SHAPE ONLY: that the value is a mapping,
    that every key in it is a string, and that every value in it matches the
    ENTRY TYPE its own spec declares (``ConfigKeySpec.entry_type``). A key that
    declares none has its entries left unchecked. WHETHER a task class exists,
    whether a tier exists, whether an override breaks a hard rule and whether a
    benchmark run meets the promotion bars are all POLICY questions, and they are
    answered where the policy lives —
    ``packages.orchestration.model_routing.validate_task_class_tier_overrides``.
    This module is the LOWER layer and is deliberately policy-free: it must not
    import model_routing to learn what a task class is (DECISION F110 D5,
    rejected alternative 4).
    """
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
        elif spec.value_type is dict:
            if not isinstance(cv.value, Mapping):
                warnings.append(
                    f"{spec.key}: expected table, got {type(cv.value).__name__}")
            elif spec.entry_type is not None:
                for entry_key, entry_value in cv.value.items():
                    if isinstance(entry_key, str) and isinstance(
                            entry_value, spec.entry_type):
                        continue
                    warnings.append(
                        f"{spec.key}: expected {spec.entry_type.__name__} "
                        f"entries, got {entry_key!r} = {entry_value!r}")
    return warnings

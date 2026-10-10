"""The Claude CLI's keys of the config registry (F302, DECISION F302 D2).

The two `claude_planner` keys moved unchanged out of `packages/orchestration/config.py`, whose
`_CONFIG_KEY_SPECS` splices `CLAUDE_KEY_SPECS` in at the keys' own place, so the registry and the
guide it renders keep their order.
"""

from __future__ import annotations

from packages.orchestration.config_key_spec import ConfigKeySpec

CLAUDE_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
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
)

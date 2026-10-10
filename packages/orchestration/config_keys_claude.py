"""The Claude CLI's keys of the config registry (F302, DECISION F302 D2).

The two `claude_planner` keys moved unchanged out of `packages/orchestration/config.py`, whose
`_CONFIG_KEY_SPECS` splices `CLAUDE_KEY_SPECS` in at the keys' own place, so the registry and the
guide it renders keep their order. The two `claude_cli` keys after them turn back on what a
claude-cli worker no longer loads by default.
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
    ConfigKeySpec(
        key="claude_cli.all_tools",
        env_var="REMEDY_CLAUDE_CLI_ALL_TOOLS",
        description=(
            "Start a claude-cli worker with every built-in tool of Claude Code. Unset or false, a "
            "worker gets only the tools its role uses: Read, Glob and Grep, and Edit, Write and "
            "MultiEdit for a builder that may write; a builder started with dangerous-skip keeps "
            "every tool (F302, DECISION F302 D2)."
        ),
        value_type=bool,
        default=False,
    ),
    ConfigKeySpec(
        key="claude_cli.customizations",
        env_var="REMEDY_CLAUDE_CLI_CUSTOMIZATIONS",
        description=(
            "Start a claude-cli worker with the operator's and the project's customizations: "
            "CLAUDE.md, skills, plugins, hooks, MCP servers and auto memory. Unset or false, the "
            "worker starts in Claude Code's safe mode, which loads none of them (F302, "
            "DECISION F302 D2)."
        ),
        value_type=bool,
        default=False,
    ),
)

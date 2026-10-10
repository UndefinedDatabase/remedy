"""The mission orchestrator's keys of the config registry (F301, DECISION F301 D2).

Moved unchanged out of `packages/orchestration/config.py`, whose `_CONFIG_KEY_SPECS` splices
`MISSION_KEY_SPECS` in at the keys' own place, so the registry and the guide it renders keep their
order.
"""

from __future__ import annotations

from packages.orchestration.config_key_spec import ConfigKeySpec

MISSION_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
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
)

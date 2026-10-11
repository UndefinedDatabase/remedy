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
    ConfigKeySpec(
        key="mission.upkeep_every",
        env_var="REMEDY_MISSION_UPKEEP_EVERY",
        description=(
            "After how many completed jobs of a mission its next job is an upkeep job that "
            "Remedy plans from the project's upkeep ledger: the findings earlier jobs left open, "
            "the largest code over the structure limits, and the files replaced and not deleted "
            "(F301, DECISION F301 D1). A whole number of at least 1; it counts jobs, never time."
        ),
        value_type=int,
        default=5,
    ),
    ConfigKeySpec(
        key="mission.upkeep_max_findings",
        env_var="REMEDY_MISSION_UPKEEP_MAX_FINDINGS",
        description=(
            "How many of the project's open findings one upkeep job carries at most, oldest first; "
            "the rest wait for the next upkeep job (R-1239). A whole number of at least 1."
        ),
        value_type=int,
        default=5,
    ),
    ConfigKeySpec(
        key="mission.upkeep_function_lines",
        env_var="REMEDY_MISSION_UPKEEP_FUNCTION_LINES",
        description=(
            "The length in lines above which an upkeep job's structure measure names a Python "
            "function of the project's repository (R-1239). A whole number of at least 1."
        ),
        value_type=int,
        default=100,
    ),
    ConfigKeySpec(
        key="mission.upkeep_file_lines",
        env_var="REMEDY_MISSION_UPKEEP_FILE_LINES",
        description=(
            "The length in lines above which an upkeep job's structure measure names a code file "
            "of the project's repository (R-1239). A whole number of at least 1."
        ),
        value_type=int,
        default=1000,
    ),
)

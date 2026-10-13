"""The logging keys of the config registry (F203, structure-ledger step (5) of config.py).

Moved unchanged out of `packages/orchestration/config.py`, whose `_CONFIG_KEY_SPECS` splices
`LOGGING_KEY_SPECS` in at the keys' own place, so the registry and the guide it renders keep their
order.
"""

from __future__ import annotations

from packages.orchestration.config_key_spec import ConfigKeySpec

LOGGING_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
    ConfigKeySpec(
        key="logging.level",
        env_var="REMEDY_LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
        value_type=str,
        default="WARNING",
    ),
)

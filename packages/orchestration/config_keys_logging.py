"""The logging keys of the config registry (F203, DECISION F203 D1).

The module began as structure-ledger step (5) of `packages/orchestration/config.py`, which moved
the first key here unchanged; F203 added the keys after the first. `_CONFIG_KEY_SPECS` splices
`LOGGING_KEY_SPECS` in at the keys' own place, so the registry and the guide it renders keep their
order.
"""

from __future__ import annotations

from packages.orchestration.config_key_spec import ConfigKeySpec

LOGGING_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
    ConfigKeySpec(
        key="logging.level",
        env_var="REMEDY_LOG_LEVEL",
        description=(
            "The lowest level written to Remedy's operations log under <data root>/logs/ "
            "(DEBUG, INFO, WARNING, ERROR, CRITICAL); an unknown name falls back to INFO. "
            "The terminal keeps showing warnings and errors whatever this says "
            "(DECISION F203 D1)."
        ),
        value_type=str,
        default="INFO",
    ),
    ConfigKeySpec(
        key="logging.json_lines",
        env_var="REMEDY_LOG_JSON_LINES",
        description=(
            "Write the operations log as one JSON object per line; false writes one plain "
            "text line per record (DECISIONs F203 D1 and D6)."
        ),
        value_type=bool,
        default=True,
    ),
    ConfigKeySpec(
        key="logging.max_bytes",
        env_var="REMEDY_LOG_MAX_BYTES",
        description=(
            "The size in bytes at which the operations log is rotated (DECISION F203 D1)."
        ),
        value_type=int,
        default=10_000_000,
    ),
    ConfigKeySpec(
        key="logging.backup_count",
        env_var="REMEDY_LOG_BACKUP_COUNT",
        description=(
            "How many rotated operations logs are kept beside the current one "
            "(DECISION F203 D1)."
        ),
        value_type=int,
        default=5,
    ),
)

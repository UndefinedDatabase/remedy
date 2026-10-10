"""One config key's definition, `ConfigKeySpec` (F301, DECISION F301 D2).

Moved unchanged out of `packages/orchestration/config.py`, which imports it back by name, so
`from packages.orchestration.config import ConfigKeySpec` keeps working. A group of the registry
whose keys live in a module of their own imports it from here, which is what lets a group leave
`config.py` without an import cycle.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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


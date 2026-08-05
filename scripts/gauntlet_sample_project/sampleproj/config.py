"""Configuration with three sources and one precedence rule.

Explicit argument beats environment beats file default. g02 asks for tests of
exactly that order; g04 asks for a README section documenting it and every
environment variable read here.
"""
from __future__ import annotations

import os
from pathlib import Path

from .errors import MSG_NOT_AN_INT, MSG_UNKNOWN_KEY, ConfigError

#: Every setting, with the value used when nothing else supplies one.
DEFAULTS: dict[str, int] = {
    "max_records": 100,
    "retry_attempts": 3,
    "report_width": 72,
}

#: setting name -> the environment variable that overrides its file default.
ENV_VARS: dict[str, str] = {
    "max_records": "SAMPLEPROJ_MAX_RECORDS",
    "retry_attempts": "SAMPLEPROJ_RETRY_ATTEMPTS",
    "report_width": "SAMPLEPROJ_REPORT_WIDTH",
}

#: Where the file defaults are read from when no path is given.
DEFAULT_CONFIG_FILENAME = "sampleproj.conf"


def _as_int(key: str, value: str | int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ConfigError(MSG_NOT_AN_INT.format(key=key, value=value)) from None


def read_config_file(path: Path | str) -> dict[str, int]:
    """``key = value`` lines; blanks and ``#`` comments ignored."""
    settings: dict[str, int] = {}
    text = Path(path).read_text(encoding="utf-8") if Path(path).is_file() else ""
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, raw = line.partition("=")
        key = key.strip()
        if key not in DEFAULTS:
            raise ConfigError(MSG_UNKNOWN_KEY.format(key=key))
        settings[key] = _as_int(key, raw.strip())
    return settings


def resolve(key: str, *, explicit: int | None = None,
            config_path: Path | str | None = None,
            env: dict[str, str] | None = None) -> int:
    """One setting, resolved: explicit > environment > file > built-in default."""
    if key not in DEFAULTS:
        raise ConfigError(MSG_UNKNOWN_KEY.format(key=key))
    if explicit is not None:
        return _as_int(key, explicit)

    environ = os.environ if env is None else env
    raw = environ.get(ENV_VARS[key])
    if raw is not None and raw != "":
        return _as_int(key, raw)

    if config_path is not None:
        from_file = read_config_file(config_path)
        if key in from_file:
            return from_file[key]
    return DEFAULTS[key]

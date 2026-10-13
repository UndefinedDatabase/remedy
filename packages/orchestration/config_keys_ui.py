"""The UI server's first keys of the config registry (finding R-1264).

Moved unchanged out of `packages/orchestration/config.py`, whose `_CONFIG_KEY_SPECS` splices
`UI_KEY_SPECS` in at the keys' own place, so the registry and the guide it renders keep their
order.
"""

from __future__ import annotations

from packages.orchestration.config_key_spec import ConfigKeySpec

UI_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
    ConfigKeySpec(
        key="ui.host",
        env_var="REMEDY_UI_HOST",
        description=(
            "UI server bind host. Loopback values keep the cockpit on 127.0.0.1; "
            "a LAN host or wildcard binds on all IPv4 interfaces and records both "
            "the loopback URL and LAN URLs, still protected by the per-session token."
        ),
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
)

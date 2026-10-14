"""The autonomy keys of the config registry (F078, DECISION F078 D1).

The module began as structure-ledger step (6) of `packages/orchestration/config.py`, which moved
the autonomy watchdog's keys (F077) here unchanged; F078 adds the keys of the autonomy level after
them. `_CONFIG_KEY_SPECS` splices `AUTONOMY_KEY_SPECS` in at the keys' own place, so the registry
and the guide it renders keep their order.
"""

from __future__ import annotations

from packages.orchestration.config_key_spec import ConfigKeySpec

AUTONOMY_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
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
)

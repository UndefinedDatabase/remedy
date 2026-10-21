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
    ConfigKeySpec(
        key="autonomy.level",
        env_var="REMEDY_AUTONOMY_LEVEL",
        description=(
            "Who may start work on Remedy's own initiative: L2, every start is your own command; L3, the "
            "mission loop may also start the next job of a mission you started; L4, order files may also be "
            "started without you; L5, idea drafts may also be started, within their caps. Every approval, "
            "fence, budget and watchdog applies at every level. L3 and higher need "
            "autonomy.gauntlet_evidence, and every change needs autonomy.change_adr; set it in remedy.toml, "
            "never in the environment (DECISION F078 D1)."
        ),
        value_type=str,
        default="L2",
    ),
    ConfigKeySpec(
        key="autonomy.gauntlet_evidence",
        env_var="REMEDY_AUTONOMY_GAUNTLET_EVIDENCE",
        description=(
            "The matrix.json of a gauntlet attempt that passed; a level of L3 or higher is refused without "
            "it. A relative path is read from the folder of the config file that sets it (DECISION F078 D1)."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="autonomy.change_adr",
        env_var="REMEDY_AUTONOMY_CHANGE_ADR",
        description=(
            "The file that records why the autonomy level was last changed; a change of autonomy.level is "
            "refused without it. A relative path is read from the folder of the config file that sets it "
            "(DECISION F078 D1)."
        ),
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="autonomy.idea_max_effort",
        env_var="REMEDY_AUTONOMY_IDEA_MAX_EFFORT",
        description=(
            "The largest effort band (low, medium or high) of an idea draft that autonomy level L5 may "
            "start on its own; a larger one waits for you (DECISION F078 D3)."
        ),
        value_type=str,
        default="low",
    ),
    ConfigKeySpec(
        key="autonomy.idea_starts_per_day",
        env_var="REMEDY_AUTONOMY_IDEA_STARTS_PER_DAY",
        description=(
            "How many idea drafts autonomy level L5 may start on its own per day, counted in UTC; the "
            "next one waits for you (DECISION F078 D3)."
        ),
        value_type=int,
        default=1,
    ),
    ConfigKeySpec(
        key="autonomy.idea_usd_per_day",
        env_var="REMEDY_AUTONOMY_IDEA_USD_PER_DAY",
        description=(
            "How many dollars of estimated cost the idea drafts autonomy level L5 starts on its own may "
            "add up to per day, counted in UTC; one that would pass it waits for you (DECISION F078 D3)."
        ),
        value_type=float,
        default=1.0,
    ),
    ConfigKeySpec(
        key="autonomy.allow_push",
        env_var="REMEDY_AUTONOMY_ALLOW_PUSH",
        description=(
            "Whether Remedy may push to a project's remote at all. When false, every push is refused "
            "at every autonomy level; when true, every push still needs your approval of that one "
            "push, such as the push flag of your own command. Set it in remedy.toml, never in the "
            "environment (DECISION F141 D1)."
        ),
        value_type=bool,
        default=True,
    ),
)

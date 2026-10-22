"""The budget keys of the config registry (F310, DECISION F310 D2).

The module began as structure-ledger step (6) of `packages/orchestration/config.py`, which moved
the budget group here unchanged; F310 added the profile keys after it. `_CONFIG_KEY_SPECS` splices
`BUDGET_KEY_SPECS` in at the group's own place, so the registry and the guide it renders keep their
order.
"""

from __future__ import annotations

from packages.orchestration.config_key_spec import ConfigKeySpec

BUDGET_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
    ConfigKeySpec(
        key="budget.max_total_tokens",
        env_var="REMEDY_BUDGET_MAX_TOTAL_TOKENS",
        description="Maximum total tokens for a job (F018 budgets)",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.max_provider_calls",
        env_var="REMEDY_BUDGET_MAX_PROVIDER_CALLS",
        description="Maximum provider calls for a job (F018 budgets)",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.max_wall_clock_minutes",
        env_var="REMEDY_BUDGET_MAX_WALL_CLOCK_MINUTES",
        description="Maximum wall-clock minutes for a job (F018 budgets)",
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.max_cost_usd",
        env_var="REMEDY_BUDGET_MAX_COST_USD",
        description="Maximum cost in USD for a job (F104 budgets)",
        value_type=float,
        default=None,
    ),
    # F276 T004. The default is None — no floor — for the reason DECISION F276 D7
    # records: every other budget key defaults to None, `resolve_job_budgets`
    # returns None when they all do, and a number here would hand a JobBudgets to
    # every job that has none today.
    ConfigKeySpec(
        key="budget.min_free_disk_bytes",
        env_var="REMEDY_BUDGET_MIN_FREE_DISK_BYTES",
        description=(
            "Free bytes that must remain on the data root's filesystem for a job "
            "to start and to pass a safe point (F276 disk floor)"
        ),
        value_type=int,
        default=None,
    ),
    # F104 predictive inputs. The price basis has NO default on purpose
    # (DECISION F104 D4): an invented price would make every prediction a
    # fabrication, so with it unset the predictive path is inert.
    ConfigKeySpec(
        key="budget.price_basis_usd_per_1k_tokens",
        env_var="REMEDY_BUDGET_PRICE_BASIS_USD_PER_1K_TOKENS",
        description=(
            "Provisional USD price per 1000 tokens used for cost predictions "
            "(F104; provisional until calibration)"
        ),
        value_type=float,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.class_default_tokens_low",
        env_var="REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_LOW",
        description=(
            "Expected tokens for a low-band task "
            "(F104; provisional until calibration)"
        ),
        value_type=int,
        default=8000,
    ),
    ConfigKeySpec(
        key="budget.class_default_tokens_medium",
        env_var="REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_MEDIUM",
        description=(
            "Expected tokens for a medium-band task "
            "(F104; provisional until calibration)"
        ),
        value_type=int,
        default=32000,
    ),
    ConfigKeySpec(
        key="budget.class_default_tokens_high",
        env_var="REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_HIGH",
        description=(
            "Expected tokens for a high-band task "
            "(F104; provisional until calibration)"
        ),
        value_type=int,
        default=120000,
    ),
    # F074 estimate calibration (DECISION F074 D1 (3)): a class with this many measured tasks
    # replaces the defaults above for its own tasks; the defaults equal
    # `packages/orchestration/estimate_calibration.py`'s DEFAULT_CALIBRATION_* constants.
    ConfigKeySpec(
        key="budget.calibration_sample_floor",
        env_var="REMEDY_BUDGET_CALIBRATION_SAMPLE_FLOOR",
        description=(
            "Measured tasks a task class needs in the cost ledger before its estimates are "
            "calibrated from them instead of the class defaults (F074)"
        ),
        value_type=int,
        default=20,
    ),
    ConfigKeySpec(
        key="budget.calibration_window_days",
        env_var="REMEDY_BUDGET_CALIBRATION_WINDOW_DAYS",
        description=(
            "Days of the cost ledger an estimate calibration reads; older tasks age out (F074)"
        ),
        value_type=int,
        default=90,
    ),
    ConfigKeySpec(
        key="budget.calibration_snapshot_max_age_seconds",
        env_var="REMEDY_BUDGET_CALIBRATION_SNAPSHOT_MAX_AGE_SECONDS",
        description=(
            "Seconds a saved estimate calibration is used before the ledger is measured "
            "again on the next read (F074)"
        ),
        value_type=int,
        default=3600,
    ),
    ConfigKeySpec(
        key="cost_preview.confirm_above_usd",
        env_var="REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD",
        description=(
            "USD threshold above which an expensive command's cost preview "
            "requires operator confirmation before it runs (F114)"
        ),
        value_type=float,
        default=0.5,
    ),
    ConfigKeySpec(
        key="budget.deadline",
        env_var="REMEDY_BUDGET_DEADLINE",
        description="UTC deadline for a job as ISO 8601 string (F018 budgets)",
        value_type=str,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.profile.local.max_total_tokens",
        env_var="REMEDY_BUDGET_PROFILE_LOCAL_MAX_TOTAL_TOKENS",
        description=(
            "Default token limit of a job whose roles all run on a model Ollama serves on this "
            "machine, when neither the job nor budget.max_total_tokens sets one (F310 profiles)"
        ),
        value_type=int,
        default=1500000,
    ),
    ConfigKeySpec(
        key="budget.profile.local.max_provider_calls",
        env_var="REMEDY_BUDGET_PROFILE_LOCAL_MAX_PROVIDER_CALLS",
        description=(
            "Default provider-call limit of a local job, when neither the job nor "
            "budget.max_provider_calls sets one (F310 profiles)"
        ),
        value_type=int,
        default=200,
    ),
    ConfigKeySpec(
        key="budget.profile.local.max_wall_clock_minutes",
        env_var="REMEDY_BUDGET_PROFILE_LOCAL_MAX_WALL_CLOCK_MINUTES",
        description=(
            "Default wall-clock limit in minutes of a local job, when neither the job nor "
            "budget.max_wall_clock_minutes sets one (F310 profiles)"
        ),
        value_type=int,
        default=480,
    ),
    ConfigKeySpec(
        key="budget.profile.paid.max_total_tokens",
        env_var="REMEDY_BUDGET_PROFILE_PAID_MAX_TOTAL_TOKENS",
        description=(
            "Default token limit of a job any of whose roles runs on a paid or remote model, when "
            "neither the job nor budget.max_total_tokens sets one; unset means no limit (F310 "
            "profiles)"
        ),
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.profile.paid.max_provider_calls",
        env_var="REMEDY_BUDGET_PROFILE_PAID_MAX_PROVIDER_CALLS",
        description=(
            "Default provider-call limit of a paid job, when neither the job nor "
            "budget.max_provider_calls sets one; unset means no limit (F310 profiles)"
        ),
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.profile.paid.max_wall_clock_minutes",
        env_var="REMEDY_BUDGET_PROFILE_PAID_MAX_WALL_CLOCK_MINUTES",
        description=(
            "Default wall-clock limit in minutes of a paid job, when neither the job nor "
            "budget.max_wall_clock_minutes sets one; unset means no limit (F310 profiles)"
        ),
        value_type=int,
        default=None,
    ),
    ConfigKeySpec(
        key="budget.profile.paid.max_cost_usd",
        env_var="REMEDY_BUDGET_PROFILE_PAID_MAX_COST_USD",
        description=(
            "Default cost limit in USD of a paid job, when neither the job nor "
            "budget.max_cost_usd sets one; unset means no limit (F310 profiles)"
        ),
        value_type=float,
        default=None,
    ),
)

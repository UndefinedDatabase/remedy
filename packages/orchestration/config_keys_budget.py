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
)

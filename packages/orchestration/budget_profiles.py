"""Budget profiles per provider class (F310, DECISIONs F310 D1 and D2).

A job is `local` when every role that runs it uses a model Ollama serves on this machine, and
`paid` otherwise. Each class has a profile of default limits, configuration under
`budget.profile.<class>.*`. `run_job` reads a job's limits through `effective_job_budgets`: the
job's own budgets first, then the configured `budget.*` values, then the profile of its class.
A profile's value is never written into the job's record.
"""
from __future__ import annotations

from typing import Any

from packages.core.models import JobBudgets
from packages.orchestration.budget_resolution import parse_budget_limit, resolve_job_budgets
from packages.orchestration.model_failover import LOCAL_PROVIDERS

# The class of a job whose roles all run on a model served on this machine.
PROVIDER_CLASS_LOCAL = "local"
# The class of every other job, the test provider included.
PROVIDER_CLASS_PAID = "paid"

# The limits each class's profile carries; the local profile has no money limit (no price is reported).
BUDGET_PROFILE_LIMITS: dict[str, tuple[str, ...]] = {
    PROVIDER_CLASS_LOCAL: ("max_total_tokens", "max_provider_calls", "max_wall_clock_minutes"),
    PROVIDER_CLASS_PAID: ("max_total_tokens", "max_provider_calls", "max_wall_clock_minutes",
                          "max_cost_usd"),
}


# One provider and model is local only when Ollama serves it here; a `-cloud` model is remote.
def provider_class(provider: str, model: str | None = None) -> str:
    """`local` for an Ollama-served provider and model, `paid` for any other."""
    if provider in LOCAL_PROVIDERS and not (model or "").endswith(("-cloud", ":cloud")):
        return PROVIDER_CLASS_LOCAL
    return PROVIDER_CLASS_PAID


# A job is local only when every role that runs it is; no execution config means paid.
def job_provider_class(job: Any) -> str:
    """The class of a job, from the builder, the reviewer and a repair provider when one is set."""
    config = getattr(job, "execution_config", None)
    if config is None:
        return PROVIDER_CLASS_PAID
    roles = [(config.builder, config.builder_model), (config.reviewer, config.reviewer_model)]
    if config.repair_provider:
        roles.append((config.repair_provider, config.repair_model))
    if all(provider_class(provider, model) == PROVIDER_CLASS_LOCAL for provider, model in roles):
        return PROVIDER_CLASS_LOCAL
    return PROVIDER_CLASS_PAID


# The profile's values come from the registry, its default included, because a profile key's default IS a limit.
def resolve_budget_profile(
    class_name: str, *, project_root: str | None = None,
) -> dict[str, int | float | None]:
    """The limits of one class's profile; None means no limit. A malformed value raises."""
    from pathlib import Path

    from packages.orchestration.config import load_config

    if project_root:
        cfg = load_config(project_path=Path(project_root) / "remedy.toml")
    else:
        cfg = load_config()
    profile: dict[str, int | float | None] = {}
    for limit in BUDGET_PROFILE_LIMITS[class_name]:
        cv = cfg.get_value(f"budget.profile.{class_name}.{limit}")
        raw = None if cv is None else cv.value
        profile[limit] = None if raw is None else parse_budget_limit(limit, raw)  # type: ignore[assignment]  # numeric limits only
    return profile


# What the execution offer names: both profiles with their numbers, read now.
def budget_profiles_offer(
    *, project_root: str | None = None,
) -> dict[str, dict[str, int | float | None]]:
    """Both profiles, `local` then `paid`, as the execution offer shows them."""
    return {
        class_name: resolve_budget_profile(class_name, project_root=project_root)
        for class_name in (PROVIDER_CLASS_LOCAL, PROVIDER_CLASS_PAID)
    }


# The one place a run's limits are decided: job, then `budget.*`, then the class's profile.
def effective_job_budgets(job: Any) -> JobBudgets | None:
    """The limits a run is judged against, or None when every one is unset. Writes nothing to `job`."""
    own = None
    if job.budgets is not None:
        own = JobBudgets.model_validate(job.budgets)
    root = job.repo_path or None
    configured = resolve_job_budgets(project_root=root)
    profile = resolve_budget_profile(job_provider_class(job), project_root=root)
    values: dict[str, Any] = {}
    for field in JobBudgets.model_fields:
        for layer in (own, configured):
            value = None if layer is None else getattr(layer, field)
            if value is not None:
                values[field] = value
                break
        else:
            if profile.get(field) is not None:
                values[field] = profile[field]
    return JobBudgets(**values) if values else None

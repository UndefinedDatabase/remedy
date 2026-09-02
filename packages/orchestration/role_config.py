"""
Role-based runtime configuration for Remedy.

Resolves the runtime settings (provider, model, effort) for each orchestration
role. Values come from three sources, highest precedence first:

  1. CLI args      — per-invocation overrides
  2. Config file   — persisted project/user preferences
  3. Provider-aware built-in defaults

Provider-aware defaults: the default model depends on which provider is
selected. Claude providers default to Opus; Ollama keeps its own default.

Public API::

    KNOWN_ROLES: tuple of recognised role names
    RoleConfig: resolved provider/model/effort for one role
    resolve_role_config(role, cli_args=None, config_file=None) -> RoleConfig
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass

from packages.orchestration.model_aliases import resolve_model_alias

# ---------------------------------------------------------------------------
# Defaults (provider-aware)
# ---------------------------------------------------------------------------

DEFAULT_PROVIDER = "ollama"
DEFAULT_EFFORT = "medium"

#: Which ROLE a provider's built-in default model plays. The concrete ids live
#: in packages/orchestration/model_aliases.py — the single source — so an
#: upgrade repoints one alias there instead of editing this table.
_PROVIDER_DEFAULT_MODELS: dict[str, str] = {
    "ollama": resolve_model_alias("ollama-default"),
    "claude-cli": resolve_model_alias("claude-flagship"),
    "claude": resolve_model_alias("claude-flagship"),
    "fake": resolve_model_alias("fake"),
    "fixture": resolve_model_alias("fixture"),
}

DEFAULT_MODEL = _PROVIDER_DEFAULT_MODELS[DEFAULT_PROVIDER]

#: Roles that Remedy knows how to configure.
#:
#: ``orchestrator`` (F070) is the mission loop's decision layer. It is listed
#: here so the loop's calls resolve without the unknown-role warning — and for
#: nothing else: its built-in defaults are deliberately the SAME as every other
#: role's, because raising the orchestrator to a top-tier model is a
#: CONFIGURATION act (`orchestrator.model`), not a change to the routing policy
#: in docs/agents/model_routing_policy.md.
#: ``teacher`` (F255) narrates a running mission and answers operator questions.
#: It is listed here so its calls resolve without the unknown-role warning. It is
#: read-only by construction and never influences a run, which is why it carries
#: no CLI override flags and no per-role budget limit (DECISION F255 D1 and D3).
#: ``summary`` (F108 T002) is the schema-validated generation-call role behind
#: ``generate_artifact_summary`` (packages/orchestration/artifact_summary.py). It
#: is registered here so F110 (model routing by task class) has a named target
#: for its routing table, per docs/roadmap/features/T3_F108.md's Orchestrator
#: brief. It carries no CLI override flags or per-role budget limit of its
#: own. ``summary_call_fn`` (packages/orchestration/artifact_summary.py,
#: F108 T003a) is the one production caller of ``resolve_role_config`` for
#: this role, feeding the resolved model into ``make_structured_call_fn``;
#: ``generate_artifact_summary`` itself still takes ``call_fn`` as a direct
#: parameter and never resolves through this module directly.
KNOWN_ROLES: tuple[str, ...] = (
    "builder",
    "reviewer",
    "repair",
    "design_worker",
    "test_worker",
    "final_verifier",
    "orchestrator",
    "teacher",
    "summary",
)

#: Resolvable fields on a RoleConfig, in declaration order.
_FIELDS: tuple[str, ...] = ("provider", "model", "effort")


def default_model_for_provider(provider: str) -> str:
    """Return the default model for a given provider name."""
    return _PROVIDER_DEFAULT_MODELS.get(provider, DEFAULT_MODEL)


@dataclass(frozen=True)
class RoleConfig:
    """Resolved runtime configuration for a single role."""

    role: str
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL
    effort: str = DEFAULT_EFFORT


def _role_section(source: object, role: str) -> dict:
    """Extract the override mapping for ``role`` from a config source.

    A source may be either:
      * role-scoped and flat — ``{"provider": ..., "model": ...}``, or
      * nested by role — ``{"builder": {"provider": ...}, ...}``.

    Returns an empty dict when the source is missing or has no entry for the role.
    """
    if not isinstance(source, dict):
        return {}
    nested = source.get(role)
    if isinstance(nested, dict):
        return nested
    return source


def resolve_role_config(
    role: str,
    cli_args: object | None = None,
    config_file: object | None = None,
) -> RoleConfig:
    """Resolve the runtime configuration for ``role``.

    Precedence (highest first): ``cli_args`` > ``config_file`` > provider-aware
    defaults.

    When the provider is resolved but no model is explicitly set, the model
    defaults to the provider-specific default (e.g. Opus for claude-cli,
    the configured local default for ollama).

    Args:
        role: The role name (see :data:`KNOWN_ROLES`).
        cli_args: Optional per-invocation overrides — either a flat mapping of
            ``provider``/``model``/``effort`` or a mapping keyed by role.
        config_file: Optional persisted overrides, same shape as ``cli_args``.

    Unknown roles emit a warning (rather than raising) and still resolve against
    the supplied overrides, falling back to the built-in defaults.
    """
    if role not in KNOWN_ROLES:
        warnings.warn(
            f"Unknown role {role!r}; using default runtime configuration. "
            f"Known roles: {', '.join(KNOWN_ROLES)}.",
            stacklevel=2,
        )

    cli = _role_section(cli_args, role)
    cfg = _role_section(config_file, role)

    resolved: dict[str, str] = {}
    for field in _FIELDS:
        value = cli.get(field)
        if value is None:
            value = cfg.get(field)
        if value is not None:
            resolved[field] = value

    # Provider-aware model default: if provider is set but model is not,
    # use the provider's default model instead of the global default.
    if "model" not in resolved:
        provider = resolved.get("provider", DEFAULT_PROVIDER)
        resolved["model"] = default_model_for_provider(provider)

    return RoleConfig(role=role, **resolved)

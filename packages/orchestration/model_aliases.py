"""F254 — the single source of Remedy's BUILT-IN default model ids.

Built-in defaults used to rot in place: the same dated model id was retyped
into every module that needed a fallback, so nobody could answer "which ids
does this repo ship?" without a full-text search, and upgrading one meant
finding all of them.  This module is the one table.  Every other module names
a logical alias (``claude-flagship``) and asks for the concrete id; nothing
outside this file spells a concrete id itself.

Dependency-free on purpose: it imports nothing from ``packages.orchestration``,
so any module in the package can route its default through it without risking
an import cycle.

Public API::

    MODEL_ALIASES: logical alias -> concrete model id
    resolve_model_alias(alias) -> str      # raises KeyError on an unknown alias
    known_model_aliases() -> tuple[str, ...]
    builtin_model_ids() -> tuple[str, ...]

Deliberate absences:
  * Remedy deliberately does not read configuration here.  This table holds
    BUILT-IN defaults only; a configured override comes from
    ``get_config().get("orchestrator.model")`` and outranks anything below.
  * Remedy deliberately does not probe a provider for its live model list.
    Live provider probing is a Non-goal of F254 (docs/roadmap/features/
    T2_F254.md), so this module touches no network and reads no file — it is
    a static table plus accessors.
  * Remedy deliberately does not modernise the ids here as a side effect of
    relocating them.  Choosing NEW ids is F232's job (the model upgrade
    playbook); at relocation time this table's values were exactly the strings
    the repo already shipped.  Operator decisions since then repoint entries
    in place — see the dated comments in the table.
"""

from __future__ import annotations

#: Logical alias -> the concrete model id Remedy falls back to when nothing
#: else is configured.  Aliases describe the ROLE a model plays, so an upgrade
#: repoints one line here instead of touching every caller.
MODEL_ALIASES: dict[str, str] = {
    # Top-tier Claude model: the built-in default for both Claude providers.
    # Operator decision 2026-08-25 (dogfooding): repointed off the retired
    # claude-opus-4-20250514, which `remedy doctor` warned about from the
    # shipped dead-model list. Maintenance of a dead value, not a routing
    # strategy — F232 still owns the upgrade playbook.
    "claude-flagship": "claude-opus-4-8",
    # Mid-tier Claude model: the built-in default for the direct-API provider.
    # Operator decision 2026-08-25 (dogfooding): repointed off the retired
    # claude-sonnet-4-20250514, for the reason on the line above.
    "claude-workhorse": "claude-sonnet-4-6",
    # The local Ollama default, and Remedy's global default model.
    # Operator decision 2026-08-13: Muse Glimmer is the local default.
    "ollama-default": "muse-glimmer:latest",
    # Deterministic test providers — no network, no cost.
    "fake": "fake-model",
    "fixture": "fixture-model",
}


def resolve_model_alias(alias: str) -> str:
    """Return the concrete model id registered for ``alias``.

    Raises:
        KeyError: when ``alias`` is not in :data:`MODEL_ALIASES`.  An unknown
            alias is a programming error, never a reason to guess: silently
            falling back would ship a model nobody chose, which is exactly the
            drift this table exists to stop.  The message names the unknown
            alias and lists the known ones.
    """
    try:
        return MODEL_ALIASES[alias]
    except KeyError:
        raise KeyError(
            f"Unknown model alias {alias!r}. "
            f"Known aliases: {', '.join(known_model_aliases())}."
        ) from None


def known_model_aliases() -> tuple[str, ...]:
    """The registered alias names, sorted — for callers that enumerate."""
    return tuple(sorted(MODEL_ALIASES))


def builtin_model_ids() -> tuple[str, ...]:
    """Every concrete model id in the table, sorted and de-duplicated.

    Two aliases may point at the same id, so the doctor check that compares
    Remedy's built-in defaults against a known-dead list wants the SET of ids,
    not one entry per alias.
    """
    return tuple(sorted(set(MODEL_ALIASES.values())))

"""Per-task-class input token budget resolution and floor validation (F112).

Reuses the task-class vocabulary ``TASK_CLASS_TIERS`` declares
(packages/orchestration/model_routing.py) rather than inventing a second
one — a cap for a class routing does not recognize is refused outright.
Compiler wiring and the ``cannot_fit`` outcome are T002; this module ships
the config schema's reader, the resolver and the floor validation only.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING

from packages.orchestration.model_routing import TASK_CLASS_TIERS

if TYPE_CHECKING:
    from packages.orchestration.config import RemedyConfig

#: The only estimate basis this module can honestly claim until F074 ships
#: measured caps: every cap below, whichever layer resolved it, originates
#: from a config default rather than from a benchmark.
PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT = "class_default"

#: Global fallback input-token cap, used when a task class carries neither
#: an operator-configured per-class cap nor an operator-configured global
#: override. Matches context_compiler.DEFAULT_CONTEXT_TOKEN_BUDGET (F107):
#: the compiler's existing whole-context budget, unchanged as the floor a
#: class falls back to until it earns a narrower one.
DEFAULT_FALLBACK_CAP_TOKENS = 24000

#: A cap below this is refused outright, regardless of what the fenced set
#: at compile time actually contains: tier-1 content is never demoted
#: (docs/roadmap/features/T3_F112.md Design), so a cap this small could not
#: hold even a single minimal fenced file's full text and is a
#: misconfiguration by construction, not a runtime condition to detect.
MIN_TASK_CLASS_CAP_TOKENS = 2000

TASK_CLASS_CAPS_CONFIG_KEY = "prompt_budget.task_class_caps"
DEFAULT_CAP_CONFIG_KEY = "prompt_budget.default_cap"


@dataclass(frozen=True)
class TaskClassCapResolution:
    """The resolved cap for one task class, with its provenance."""

    task_class: str
    cap_tokens: int
    source: str  # "configured_class" | "configured_default" | "shipped_default"
    estimate_basis: str


def resolve_task_class_cap(task_class: str) -> TaskClassCapResolution:
    """Resolve the input-token cap for ``task_class`` against live config.

    Raises ``ValueError`` for a class outside ``TASK_CLASS_TIERS`` — the one
    class vocabulary this feature and routing share
    (docs/roadmap/features/T3_F112.md "How it fits"). A per-class configured
    cap wins over a configured global default, which wins over the shipped
    fallback; every resolution carries basis ``class_default`` until F074
    ships measured caps.

    ``get_config`` is imported inside the body, mirroring
    :func:`packages.orchestration.role_config.resolve_effective_task_class_tiers`:
    this module has no module-level import of config.
    """
    if task_class not in TASK_CLASS_TIERS:
        raise ValueError(
            f"task class {task_class!r} is not part of the shared vocabulary "
            "in packages.orchestration.model_routing.TASK_CLASS_TIERS"
        )
    from packages.orchestration.config import get_config

    config = get_config()
    class_caps = config.get(TASK_CLASS_CAPS_CONFIG_KEY)
    if isinstance(class_caps, Mapping) and task_class in class_caps:
        return TaskClassCapResolution(
            task_class=task_class,
            cap_tokens=int(class_caps[task_class]),
            source="configured_class",
            estimate_basis=PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT,
        )
    default_cap = config.get(DEFAULT_CAP_CONFIG_KEY)
    if isinstance(default_cap, int):
        return TaskClassCapResolution(
            task_class=task_class,
            cap_tokens=default_cap,
            source="configured_default",
            estimate_basis=PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT,
        )
    return TaskClassCapResolution(
        task_class=task_class,
        cap_tokens=DEFAULT_FALLBACK_CAP_TOKENS,
        source="shipped_default",
        estimate_basis=PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT,
    )


def validate_prompt_budget_config(config: RemedyConfig) -> list[str]:
    """Return floor and vocabulary violations in ``config``'s prompt_budget keys.

    Empty list means the configured table (if any, or its absence) is
    valid. The generic per-entry TYPE check
    (:func:`packages.orchestration.config.validate_config`) is not
    duplicated here; this checks only what that function cannot know: the
    floor value and the shared vocabulary.
    """
    errors: list[str] = []
    class_caps = config.get(TASK_CLASS_CAPS_CONFIG_KEY)
    if isinstance(class_caps, Mapping):
        for task_class, cap in class_caps.items():
            if task_class not in TASK_CLASS_TIERS:
                errors.append(
                    f"{TASK_CLASS_CAPS_CONFIG_KEY} names unknown task class "
                    f"{task_class!r}; must be one of "
                    f"{sorted(TASK_CLASS_TIERS)}"
                )
                continue
            if isinstance(cap, int) and cap < MIN_TASK_CLASS_CAP_TOKENS:
                errors.append(
                    f"{TASK_CLASS_CAPS_CONFIG_KEY}.{task_class} is {cap}, "
                    f"below the floor of {MIN_TASK_CLASS_CAP_TOKENS} tokens "
                    "— too small to ever hold a single tier-1 fenced file"
                )
    default_cap = config.get(DEFAULT_CAP_CONFIG_KEY)
    if isinstance(default_cap, int) and default_cap < MIN_TASK_CLASS_CAP_TOKENS:
        errors.append(
            f"{DEFAULT_CAP_CONFIG_KEY} is {default_cap}, below the floor of "
            f"{MIN_TASK_CLASS_CAP_TOKENS} tokens — too small to ever hold a "
            "single tier-1 fenced file"
        )
    return errors

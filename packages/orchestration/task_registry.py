"""
Task Type Registry v1 for Remedy.

Central, extensible semantic catalogue of known task types.

Design:
  - task_type is NOT a closed enum — LLM-generated task types remain valid.
  - Known task types get structured TaskTypeSpec metadata.
  - Unknown task types fall back to a safe, conservative spec: no repo writes,
    verifier_profile="generic", capabilities=frozenset({"unknown_task_type"}).
  - The registry uses keyword-backed matching internally (v1): the first
    keyword that is a case-insensitive substring of task_type wins.
  - Ordering matters: more specific keywords precede their substrings
    (e.g. "plan" before "doc", "documentation" before "doc").

Public API:
  get_task_type_spec(task_type)  → TaskTypeSpec  (single source of routing truth)
  is_known_task_type(task_type)  → bool
  iter_task_type_specs()         → tuple[TaskTypeSpec, ...]

This registry is the intended single source of truth for:
  - repo routing (replaces _REPO_PATH_RULES / _INTENT_RULES)
  - verifier profiles (Step 13+)
  - suggested agent roles (Step 13+)
  - autonomy-mode decisions (Step 14+)
  - context selection (future)
  - MemPalace integration (future)
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Path sanitization
# Mirrors _sanitize_path_component in task_runner.py, patch_intent.py, and
# repo_applicator.py.  Kept local to avoid importing a private helper.
# ---------------------------------------------------------------------------

_SAFE_PATH_RE = re.compile(r"[^a-zA-Z0-9_-]")
_MAX_PATH_COMPONENT_LENGTH = 48


def _sanitize_path_component(value: str) -> str:
    """Replace unsafe characters and truncate for safe use in a path component."""
    sanitized = _SAFE_PATH_RE.sub("_", value)
    sanitized = sanitized[:_MAX_PATH_COMPONENT_LENGTH].strip("_")
    return sanitized or "unknown"


# ---------------------------------------------------------------------------
# TaskTypeSpec
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TaskTypeSpec:
    """Structured metadata for a (possibly unknown) task type.

    name:
        The queried task_type string (for get_task_type_spec), or the matching
        keyword string (for iter_task_type_specs entries).
    description:
        Short human-readable summary of the task type's purpose.
    allowed_outputs:
        Artifact kinds this task type is permitted to produce.
    repo_route:
        Fully-resolved repo-relative path for the primary output file,
        or None if this task type does not route to the user repo.
        Never contains {safe_type} — substitution is done at lookup time.
    verifier_profile:
        Verifier profile name (Step 13+).  "generic" for all types in v1.
    suggested_agent_role:
        Role hint for the builder agent (Step 13+).
    capabilities:
        Frozenset of capability tokens for this type.
        Unknown types carry frozenset({"unknown_task_type"}) as a conservative
        signal for future autonomy modes — do NOT treat this as low-risk.
    """

    name: str
    description: str
    allowed_outputs: tuple[str, ...]
    repo_route: str | None
    verifier_profile: str
    suggested_agent_role: str
    capabilities: frozenset[str]


# ---------------------------------------------------------------------------
# Internal route rules
#
# Ordered list of (keyword, description, repo_route_template) entries.
# The FIRST keyword that is a case-insensitive substring of task_type wins.
#
# repo_route_template may contain {safe_type} which is substituted with the
# sanitized task_type (or keyword, for iter_task_type_specs) at lookup time.
#
# Ordering rules (same semantics as the former _INTENT_RULES/_REPO_PATH_RULES):
#   1. "readme" first — avoids spurious docs/ routing for readme tasks.
#   2. docs/remedy/ keywords before docs/ keywords — "plan" before "doc".
#   3. "documentation" before "doc" — "doc" is a substring of "documentation".
# ---------------------------------------------------------------------------

_ROUTE_RULES: list[tuple[str, str, str | None]] = [
    # (keyword, description, repo_route_template)
    (
        "readme",
        "Writes or updates README.md.",
        "README.md",
    ),
    # docs/remedy/ route — planning, spec, requirement, acceptance, analysis
    (
        "plan",
        "Writes a planning document into docs/remedy/.",
        "docs/remedy/{safe_type}.md",
    ),
    (
        "spec",
        "Writes a specification document into docs/remedy/.",
        "docs/remedy/{safe_type}.md",
    ),
    (
        "requirement",
        "Writes a requirements document into docs/remedy/.",
        "docs/remedy/{safe_type}.md",
    ),
    (
        "acceptance",
        "Writes acceptance criteria into docs/remedy/.",
        "docs/remedy/{safe_type}.md",
    ),
    (
        "analysis",
        "Writes an analysis document into docs/remedy/.",
        "docs/remedy/{safe_type}.md",
    ),
    # docs/ route — changelog, architecture, design, guide, documentation, doc
    (
        "changelog",
        "Writes a changelog file into docs/.",
        "docs/{safe_type}.md",
    ),
    (
        "architecture",
        "Writes an architecture document into docs/.",
        "docs/{safe_type}.md",
    ),
    (
        "design",
        "Writes a design document into docs/.",
        "docs/{safe_type}.md",
    ),
    (
        "guide",
        "Writes a guide or how-to document into docs/.",
        "docs/{safe_type}.md",
    ),
    (
        "documentation",
        "Writes general documentation into docs/.",
        "docs/{safe_type}.md",
    ),
    (
        "doc",
        "Writes a documentation file into docs/.",
        "docs/{safe_type}.md",
    ),
]

_KNOWN_ALLOWED_OUTPUTS: tuple[str, ...] = ("workspace_artifact",)
_UNKNOWN_ALLOWED_OUTPUTS: tuple[str, ...] = ("workspace_artifact",)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_task_type_spec(task_type: str) -> TaskTypeSpec:
    """Return the TaskTypeSpec for task_type.

    Matches task_type (case-insensitive) against the internal route rules.
    Returns the first matching spec with repo_route fully resolved (no
    {safe_type} placeholder in the returned value).

    If no keyword matches, returns a conservative unknown fallback spec:
      repo_route=None, capabilities=frozenset({"unknown_task_type"}).

    This is the single source of truth for routing, verifier profiles, and
    agent role suggestions.  Both repo_applicator and patch_intent delegate
    to this function — there is no independent routing table in either module.
    """
    lower = task_type.lower()
    safe_type = _sanitize_path_component(task_type)
    for keyword, description, route_template in _ROUTE_RULES:
        if keyword in lower:
            return TaskTypeSpec(
                name=task_type,
                description=description,
                allowed_outputs=_KNOWN_ALLOWED_OUTPUTS,
                repo_route=(
                    route_template.format(safe_type=safe_type)
                    if route_template is not None
                    else None
                ),
                verifier_profile="generic",
                suggested_agent_role="generic_builder",
                capabilities=frozenset(),
            )
    # Unknown fallback — conservative, no repo writes.
    return TaskTypeSpec(
        name=task_type,
        description="Unknown task type — conservative fallback.",
        allowed_outputs=_UNKNOWN_ALLOWED_OUTPUTS,
        repo_route=None,
        verifier_profile="generic",
        suggested_agent_role="generic_builder",
        capabilities=frozenset({"unknown_task_type"}),
    )


def is_known_task_type(task_type: str) -> bool:
    """Return True if task_type is known to the registry.

    In v1 this is equivalent to get_task_type_spec(task_type).repo_route is not None
    because every registered task type has a repo_route.  The implementation uses
    the keyword match directly rather than constructing a full spec.

    Future note: if non-repo known types are added (e.g. code-generation tasks with
    a verifier profile but no repo_route), the definition will need a stronger
    registry marker than repo_route presence.  At that point callers that rely on
    the repo_route equivalence should be audited.
    """
    lower = task_type.lower()
    return any(keyword in lower for keyword, _, _ in _ROUTE_RULES)


def iter_task_type_specs() -> tuple[TaskTypeSpec, ...]:
    """Return a snapshot of all known route specs in registry order.

    Each entry uses the keyword itself as the spec name with repo_route
    resolved using the sanitized keyword as the safe_type placeholder.
    Useful for introspection, documentation generation, and tests.
    """
    specs: list[TaskTypeSpec] = []
    for keyword, description, route_template in _ROUTE_RULES:
        safe_type = _sanitize_path_component(keyword)
        specs.append(
            TaskTypeSpec(
                name=keyword,
                description=description,
                allowed_outputs=_KNOWN_ALLOWED_OUTPUTS,
                repo_route=(
                    route_template.format(safe_type=safe_type)
                    if route_template is not None
                    else None
                ),
                verifier_profile="generic",
                suggested_agent_role="generic_builder",
                capabilities=frozenset(),
            )
        )
    return tuple(specs)

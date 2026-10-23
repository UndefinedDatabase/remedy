"""R-1326: a project's own choice of builder, reviewer and planner provider, read from the
`[roles]` table of its `.remedy/config.toml` (DECISION F314 D4).

`read_project_roles` is the one place that table is read. `resolve_job_execution_config` in
`execution_config.py` reads it for the builder and the reviewer this round; `resolve_planner_target`
in `intake.py` reads it for the planner the next round. The table sits above the product default
and below an explicit option or a continued job's own persisted record.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.runtimes.runtime_config import CONFIG_RELPATH

try:                                   # Python >= 3.11
    import tomllib
except ModuleNotFoundError:            # Python 3.10 with the tomli backport
    import tomli as tomllib  # type: ignore[no-redef]

#: The only keys a `[roles]` table may name (DECISION F314 D4).
PROJECT_ROLES_KEYS = ("builder", "reviewer", "planner")


class ProjectRolesError(ValueError):
    """The `[roles]` table of `.remedy/config.toml` cannot be used."""


def read_project_roles(repo_root: str | Path | None) -> dict[str, str]:
    """The `[roles]` table of `<repo_root>/.remedy/config.toml`, or `{}`.

    `{}` when `repo_root` is falsy, the file is absent, or it has no `roles` key: a project that
    says nothing about its roles changes nothing downstream. Raises :class:`ProjectRolesError`,
    each message naming the file's relative path `.remedy/config.toml` and the table `[roles]`
    and saying what to write instead, when: the file cannot be read or parsed; `roles` is not a
    table; a key is not one of `PROJECT_ROLES_KEYS`; a value is not a non-empty string; `builder`
    or `reviewer` names a provider outside `ROLE_PROVIDER_NAMES`; `builder` names a provider
    `non_writing_provider_refusal` refuses; or `planner` names a provider outside
    `PLANNER_PROVIDERS`.

    The three name sets are imported here rather than at module level: `PLANNER_PROVIDERS` lives
    on `intake.py` and `non_writing_provider_refusal` on `do_role_guards.py`, and a module-level
    import of either risks a cycle with a caller that imports this module for the resolution it
    holds.
    """
    if not repo_root:
        return {}
    path = Path(repo_root) / CONFIG_RELPATH
    if not path.is_file():
        return {}
    try:
        data: dict[str, Any] = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ProjectRolesError(
            f"{CONFIG_RELPATH} is not readable TOML: {exc}") from exc

    table = data.get("roles")
    if table is None:
        return {}
    if not isinstance(table, dict):
        raise ProjectRolesError(
            f"{CONFIG_RELPATH}: [roles] must be a table, got {type(table).__name__}")

    from packages.orchestration.do_role_guards import non_writing_provider_refusal
    from packages.orchestration.intake import PLANNER_PROVIDERS
    from packages.orchestration.provider_names import ROLE_PROVIDER_NAMES

    result: dict[str, str] = {}
    for key, value in table.items():
        if key not in PROJECT_ROLES_KEYS:
            raise ProjectRolesError(
                f"{CONFIG_RELPATH}: [roles] names {key!r}; write builder, reviewer or planner "
                f"instead")
        if not isinstance(value, str) or not value:
            raise ProjectRolesError(
                f"{CONFIG_RELPATH}: [roles].{key} must be a non-empty string naming a provider, "
                f"got {value!r}")
        if key in ("builder", "reviewer") and value not in ROLE_PROVIDER_NAMES:
            raise ProjectRolesError(
                f"{CONFIG_RELPATH}: [roles].{key} names {value!r}, which is not a provider; "
                f"write one of {', '.join(sorted(ROLE_PROVIDER_NAMES))} instead")
        if key == "builder":
            refusal = non_writing_provider_refusal("builder", value)
            if refusal:
                raise ProjectRolesError(
                    f"{CONFIG_RELPATH}: [roles].builder names {value!r}, which cannot write "
                    f"files; write a provider that can, such as pi, instead")
        if key == "planner" and value not in PLANNER_PROVIDERS:
            raise ProjectRolesError(
                f"{CONFIG_RELPATH}: [roles].planner names {value!r}, which is not a planner; "
                f"write one of {', '.join(PLANNER_PROVIDERS)} instead")
        result[key] = value
    return result

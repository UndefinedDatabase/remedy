"""F045 T001 — loop definitions: the spec model, config loading and validation.

A LOOP is user-authored, versionable configuration that names a trigger, a
scope, an action, budgets and stop rules. This module owns the shape and the
validation only; it executes nothing. Materializing a loop as an ordinary
job/mission with ``loop_ref`` provenance is T002, and the CLI is T003.

DECISION F045 D1 — WHERE loops live. ``[[loop]]`` is a TOP-LEVEL array of
tables in ``remedy.toml``, NOT ``[[remedy.loop]]``, and NOT a new dotted
directory convention. ``load_config`` in
:mod:`packages.orchestration.config` reads only ``parsed["remedy"]``
(``_extract_remedy_table``), flattens that table to dotted keys, and appends
``"Unknown key in <path>: <key>"`` to ``load_report.warnings`` for every key
absent from ``_KEY_SPEC_MAP``. ``_flatten_toml`` does not recurse into lists,
so ``[[remedy.loop]]`` would arrive as the flat key ``loop`` and make every
config load emit a spurious unknown-key warning. Keeping the table top-level
leaves the existing config system byte-for-byte unchanged and lets this module
own its own table. Alternatives considered: a ``[[remedy.loop]]`` table
(rejected — the warning above), a ``.remedy/loops/`` directory (rejected — the
feature file's Orchestrator brief explicitly forbids inventing a second config
location). Reverse it by moving the table key and teaching ``config.py`` to
ignore it. ``tests/orchestration/test_loop_spec.py`` pins this decision with a
test that goes red if the table is moved under ``[remedy]``.

DECISION F045 D2 — deadline validation is NOT imported. ``LoopBudgets.deadline``
is validated here by ``datetime.fromisoformat`` plus a REQUIRED ``tzinfo``,
deliberately mirroring the contract of the private
``budget_resolution._parse_deadline`` rather than importing a private helper or
widening ``budget_resolution.py``, which belongs to F018/F104. Reverse it by
promoting that helper to public API in its own round.

Model conventions follow :mod:`packages.orchestration.dod_schema`: every model
derives from ``_Strict``, whose ``extra="forbid"`` IS the feature's
"unknown fields rejected" requirement.

Remedy deliberately does not execute, schedule or watch loops here. Schedule
and event triggers are parsed and VALIDATED but inert until the scheduler
feature; ``LoopSpec.is_inert`` plus ``INERT_TRIGGER_NOTICE`` is how T002/T003
say so honestly instead of silently behaving like a manual trigger.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import ValidationError

from packages.orchestration.structured_base import _Strict

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore[assignment]

#: The TOML key loops live under. Top-level by DECISION D1 — never under [remedy].
LOOP_TABLE_KEY = "loop"

#: Trigger kinds that parse and validate but cannot fire yet (no scheduler).
INERT_TRIGGER_KINDS = frozenset({"schedule", "event"})

#: The honest sentence an inert trigger gets when it is run by hand instead.
INERT_TRIGGER_NOTICE = "scheduler not yet available; ran on demand"

#: The only variables a goal template may reference. Anything else fails
#: VALIDATION rather than surfacing as a runtime KeyError (feature file, A9).
LOOP_TEMPLATE_VARS = frozenset({"project", "date"})

#: Where loops are read from when the caller names no path.
_DEFAULT_LOOP_CONFIG_PATH = Path("remedy.toml")

#: Matches one ``{placeholder}`` at a time; nested braces are not a template.
_TEMPLATE_VAR_RE = re.compile(r"\{([^{}]*)\}")


class LoopSpecError(ValueError):
    """A loop spec is unusable. ``str()`` is the full, user-facing message.

    ``loop_name`` is the offending loop's name when the entry had a usable one
    (``None`` for an unnamed entry or a file-level failure), and ``field`` names
    the offending field when one is identifiable, so a caller can group errors
    without re-parsing the message text.
    """

    def __init__(self, message: str, *, loop_name: str | None = None,
                 field: str | None = None) -> None:
        super().__init__(message)
        self.loop_name = loop_name
        self.field = field


class LoopTrigger(_Strict):
    """What starts a loop. ``manual`` is the only kind that can fire today."""

    kind: Literal["manual", "schedule", "event"] = "manual"
    schedule: str | None = None
    event: str | None = None


class LoopScope(_Strict):
    """Optional narrowing: paths become fences later, queue binds the work."""

    paths: list[str] | None = None
    queue: str | None = None


class LoopAction(_Strict):
    """What the loop does — an ordinary job or an ordinary mission, nothing new."""

    kind: Literal["job", "mission"]
    goal_template: str | None = None
    mission: str | None = None


class LoopBudgets(_Strict):
    """The standard budget fields, spelled exactly as ``budget_resolution._CONFIG_KEYS``.

    Same names on purpose: a loop's budgets must be handed to the existing
    resolver without a translation layer that could drift.
    """

    max_total_tokens: int | None = None
    max_provider_calls: int | None = None
    max_wall_clock_minutes: int | None = None
    max_cost_usd: float | None = None
    deadline: str | None = None


class LoopStopRules(_Strict):
    """When a loop stops repeating. Failing stops it unless told otherwise."""

    max_runs: int | None = None
    stop_on_failure: bool = True


class LoopSpec(_Strict):
    """One declarative loop, as authored in a ``[[loop]]`` table."""

    name: str
    trigger: LoopTrigger = LoopTrigger()
    scope: LoopScope | None = None
    action: LoopAction
    budgets: LoopBudgets | None = None
    stop: LoopStopRules | None = None
    unattended: bool = False
    report: bool = False
    notify: bool = False

    @property
    def is_inert(self) -> bool:
        """True when this loop's trigger cannot fire until the scheduler exists."""
        return self.trigger.kind in INERT_TRIGGER_KINDS


def load_loop_specs(project_path: Path | None = None) -> tuple[LoopSpec, ...]:
    """Load every loop from *project_path*, raising on the FIRST error.

    A missing file is not an error — it yields ``()``. Use
    :func:`validate_loop_specs` when you want every error at once instead of
    only the first.
    """
    entries, _path = _read_loop_entries(project_path)
    specs: list[LoopSpec] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        spec, errors = _validate_entry(entry, index, seen)
        if errors:
            raise errors[0]
        assert spec is not None  # no errors means the model was built
        specs.append(spec)
        seen.add(spec.name)
    return tuple(specs)


def validate_loop_specs(project_path: Path | None = None) -> list[str]:
    """Return EVERY error message from *project_path*, in file order.

    Never raises: a spec-level error becomes a message, and so does a
    file-level one (unparseable TOML, a ``loop`` key that is not an array of
    tables), because ``remedy loop validate`` must be able to report a broken
    config rather than crash on it. A missing file yields ``[]``.
    """
    try:
        entries, _path = _read_loop_entries(project_path)
    except LoopSpecError as exc:
        return [str(exc)]
    messages: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        spec, errors = _validate_entry(entry, index, seen)
        messages.extend(str(err) for err in errors)
        name = entry.get("name") if isinstance(entry, dict) else None
        if isinstance(name, str) and name.strip():
            seen.add(name)
    return messages


def _read_loop_entries(project_path: Path | None) -> tuple[list[Any], Path]:
    """Parse the config file and return its raw ``[[loop]]`` entries."""
    path = Path(project_path) if project_path is not None else _DEFAULT_LOOP_CONFIG_PATH
    if not path.is_file():
        return [], path
    if tomllib is None:
        raise LoopSpecError(
            f"{path}: TOML parser unavailable (install tomli for Python <3.11)")
    try:
        with open(path, "rb") as handle:
            parsed = tomllib.load(handle)
    except Exception as exc:
        raise LoopSpecError(f"{path}: malformed TOML: {exc}") from exc
    raw = parsed.get(LOOP_TABLE_KEY)
    if raw is None:
        return [], path
    if not isinstance(raw, list) or not all(isinstance(item, dict) for item in raw):
        raise LoopSpecError(f"{path}: '{LOOP_TABLE_KEY}' must be an array of tables",
                            field=LOOP_TABLE_KEY)
    return raw, path


def _entry_label(entry: Any, index: int) -> tuple[str | None, str]:
    """Return the entry's usable name and the prefix every message carries."""
    name = entry.get("name") if isinstance(entry, dict) else None
    if isinstance(name, str) and name.strip():
        return name, f"loop '{name}'"
    return None, f"loop #{index} (no name)"


def _validate_entry(entry: Any, index: int,
                    seen: set[str]) -> tuple[LoopSpec | None, list[LoopSpecError]]:
    """Validate one raw entry; return its model (when buildable) and its errors."""
    name, label = _entry_label(entry, index)
    errors: list[LoopSpecError] = []
    # Locs already reported by hand, so pydantic's version of them is not repeated.
    reported: set[tuple[Any, ...]] = set()

    def fail(detail: str, field: str | None = None) -> None:
        errors.append(LoopSpecError(f"{label}: {detail}", loop_name=name, field=field))

    if name is None:
        fail("name is required", "name")
        reported.add(("name",))
    elif name in seen:
        fail("duplicate loop name", "name")
    if not isinstance(entry, dict) or "action" not in entry:
        fail("action is required", "action")
        reported.add(("action",))

    if not isinstance(entry, dict):
        return None, errors

    try:
        spec = LoopSpec.model_validate(entry)
    except ValidationError as exc:
        for detail in exc.errors():
            loc = tuple(detail["loc"])
            if loc in reported:
                continue
            if detail["type"] == "extra_forbidden":
                key = ".".join(str(part) for part in loc)
                fail(f"unknown key '{key}'", key)
            else:
                where = ".".join(str(part) for part in loc) or "<root>"
                fail(f"{where}: {detail['msg']}", where)
        return None, errors

    errors.extend(_semantic_errors(spec, label))
    return (None if errors else spec), errors


def _semantic_errors(spec: LoopSpec, label: str) -> list[LoopSpecError]:
    """Rules pydantic cannot express: cross-field requirements and value ranges."""
    errors: list[LoopSpecError] = []

    def fail(detail: str, field: str) -> None:
        errors.append(LoopSpecError(f"{label}: {detail}", loop_name=spec.name, field=field))

    if spec.action.kind == "job" and not spec.action.goal_template:
        fail("action.goal_template is required for a job action", "action.goal_template")
    if spec.action.kind == "mission" and not spec.action.mission:
        fail("action.mission is required for a mission action", "action.mission")

    if spec.trigger.kind == "schedule" and not spec.trigger.schedule:
        fail("trigger.schedule is required for a schedule trigger", "trigger.schedule")
    if spec.trigger.kind == "event" and not spec.trigger.event:
        fail("trigger.event is required for an event trigger", "trigger.event")

    if spec.budgets is not None:
        for field_name in ("max_total_tokens", "max_provider_calls",
                           "max_wall_clock_minutes"):
            value = getattr(spec.budgets, field_name)
            if value is not None and value <= 0:
                fail(f"budgets.{field_name} must be a positive integer",
                     f"budgets.{field_name}")
        if spec.budgets.max_cost_usd is not None and spec.budgets.max_cost_usd <= 0:
            fail("budgets.max_cost_usd must be a positive number", "budgets.max_cost_usd")
        if spec.budgets.deadline is not None and not _has_tz_aware_timestamp(spec.budgets.deadline):
            fail("budgets.deadline must be an ISO 8601 timestamp with a timezone",
                 "budgets.deadline")

    if spec.stop is not None and spec.stop.max_runs is not None and spec.stop.max_runs <= 0:
        fail("stop.max_runs must be a positive integer", "stop.max_runs")

    if spec.action.goal_template:
        for var in _undefined_template_vars(spec.action.goal_template):
            fail(f"goal_template references undefined variable '{var}'",
                 "action.goal_template")

    # DECISION F045 D4: action.mission is an operator-authored goal TEMPLATE
    # too, so the same placeholders fail VALIDATION here rather than surfacing
    # as a run-time error (feature file, A9).
    if spec.action.mission:
        for var in _undefined_template_vars(spec.action.mission):
            fail(f"action.mission references undefined variable '{var}'",
                 "action.mission")

    return errors


def _has_tz_aware_timestamp(raw: str) -> bool:
    """DECISION D2: mirror ``budget_resolution._parse_deadline`` without importing it."""
    try:
        parsed = datetime.fromisoformat(raw.strip())
    except (ValueError, TypeError):
        return False
    return parsed.tzinfo is not None


def _undefined_template_vars(goal_template: str) -> list[str]:
    """Distinct ``{placeholders}`` outside LOOP_TEMPLATE_VARS, first-seen order."""
    undefined: list[str] = []
    for var in _TEMPLATE_VAR_RE.findall(goal_template):
        if var not in LOOP_TEMPLATE_VARS and var not in undefined:
            undefined.append(var)
    return undefined

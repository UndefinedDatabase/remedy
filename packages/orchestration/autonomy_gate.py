"""Who may START work on Remedy's own initiative, and at which level (F078, DECISION F078 D1).

Every approval, fence, budget and watchdog still applies at every level; this module only answers
who may BEGIN a job, never what that job may then do.

Its levels are spelled `L2` to `L5`, and they are NOT the 0 to 7 readiness scale of
`packages.orchestration.autonomy_readiness`, which measures infrastructure readiness — a
different question entirely.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from packages.orchestration.data_paths import data_class_dir, resolve_data_root

if TYPE_CHECKING:  # import-light at runtime: config.py's types are only named here
    from packages.orchestration.config import ConfigSource, RemedyConfig

# F078's levels, spelled with their L — never autonomy_readiness's 0 to 7 scale.
AUTONOMY_LEVELS: tuple[str, ...] = ("L2", "L3", "L4", "L5")

# The level Remedy runs at until an operator configures otherwise.
AUTONOMY_DEFAULT_LEVEL = "L2"

# The mission loop's terminal when the configured level refuses its next start (DECISION F078 D2
# (2)): the run ends honestly, with no job created, rather than pretending nothing was asked.
TERMINAL_AUTONOMY_DEFERRED = "deferred_by_autonomy"

# The four places a start can come from; a seam names one of these when it calls the gate.
START_ORIGIN_MANUAL = "manual"
START_ORIGIN_ORCHESTRATOR = "orchestrator"
START_ORIGIN_ORDER_FILE = "order-file"
START_ORIGIN_IDEA = "idea"

# Every value autonomy_may_start accepts as an origin, in the matrix's own column order.
START_ORIGINS: tuple[str, ...] = (
    START_ORIGIN_MANUAL,
    START_ORIGIN_ORCHESTRATOR,
    START_ORIGIN_ORDER_FILE,
    START_ORIGIN_IDEA,
)

# The one table every starting seam calls through autonomy_may_start (DECISION F078 D1 (3)):
# manual at every level; the loop from L3; an order file from L4; an idea draft only at L5.
AUTONOMY_START_MATRIX: dict[tuple[str, str], bool] = {
    (START_ORIGIN_MANUAL, "L2"): True,
    (START_ORIGIN_MANUAL, "L3"): True,
    (START_ORIGIN_MANUAL, "L4"): True,
    (START_ORIGIN_MANUAL, "L5"): True,
    (START_ORIGIN_ORCHESTRATOR, "L2"): False,
    (START_ORIGIN_ORCHESTRATOR, "L3"): True,
    (START_ORIGIN_ORCHESTRATOR, "L4"): True,
    (START_ORIGIN_ORCHESTRATOR, "L5"): True,
    (START_ORIGIN_ORDER_FILE, "L2"): False,
    (START_ORIGIN_ORDER_FILE, "L3"): False,
    (START_ORIGIN_ORDER_FILE, "L4"): True,
    (START_ORIGIN_ORDER_FILE, "L5"): True,
    (START_ORIGIN_IDEA, "L2"): False,
    (START_ORIGIN_IDEA, "L3"): False,
    (START_ORIGIN_IDEA, "L4"): False,
    (START_ORIGIN_IDEA, "L5"): True,
}

# The words each origin's sentence names, in autonomy_may_start's reason text.
_ORIGIN_WORDS: dict[str, str] = {
    START_ORIGIN_MANUAL: "your own command",
    START_ORIGIN_ORCHESTRATOR: "the mission loop",
    START_ORIGIN_ORDER_FILE: "an order file started without you",
    START_ORIGIN_IDEA: "an idea draft",
}


# autonomy_may_start's answer: whether the start is allowed, and a plain sentence saying why.
@dataclass(frozen=True)
class AutonomyStartVerdict:
    allowed: bool
    origin: str
    level: str
    reason: str


# The ONE check every starting seam calls (DECISION F078 D1 (3)). An unknown origin or level is a
# programming error, not a policy question, so it raises instead of silently denying the start.
def autonomy_may_start(origin: str, level: str) -> AutonomyStartVerdict:
    if origin not in START_ORIGINS:
        raise ValueError(f"not a known autonomy start origin: {origin!r}")
    if level not in AUTONOMY_LEVELS:
        raise ValueError(f"not a known autonomy level: {level!r}")
    words = _ORIGIN_WORDS[origin]
    allowed = AUTONOMY_START_MATRIX[(origin, level)]
    if allowed:
        reason = f"Autonomy level {level} lets Remedy start work that comes from {words}."
    else:
        first = next(lvl for lvl in AUTONOMY_LEVELS if AUTONOMY_START_MATRIX[(origin, lvl)])
        reason = (
            f"Autonomy level {level} does not let Remedy start work that comes from {words}; "
            f"that needs level {first} or higher."
        )
    return AutonomyStartVerdict(allowed=allowed, origin=origin, level=level, reason=reason)


# A configured autonomy level, or one of its two supporting keys, cannot be used as given
# (DECISION F078 D1 (4)): every sentence names exactly what is wrong and what to do about it.
class AutonomyConfigError(ValueError):
    pass


# load_autonomy_policy's answer: the level in force, the file it came from, its two supporting
# keys resolved, and whether loading it just recorded a change.
@dataclass(frozen=True)
class AutonomyPolicy:
    level: str
    config_path: str | None
    gauntlet_evidence: str | None
    change_adr: str | None
    changed_from: str | None


# One line per accepted level change lives here, under the durable "autonomy" data class
# (DECISION F078 D1 (4)), keyed by the config file that recorded it.
AUTONOMY_CHANGES_FILENAME = "level_changes.jsonl"

# One line per start the mission loop asked for and could not take, and one closing it when the
# operator's next command takes the grant instead (DECISION F078 D2 (3)); kept beside the change
# record, under the same durable data class.
AUTONOMY_DEFERRED_FILENAME = "deferred_starts.jsonl"

# The two events AUTONOMY_DEFERRED_FILENAME ever carries.
_EVENT_DEFERRED = "deferred"
_EVENT_TAKEN = "taken"


def _resolve_relative_path(value: str | None, source: ConfigSource,
                            project_path: str | None, user_path: str | None) -> str | None:
    """VALUE resolved to one absolute path: against the folder of the config file of its OWN
    source when relative, and through ``Path.resolve()`` either way (R-1321), so the result is
    always the same canonical string and never a second spelling of the same file."""
    if value is None:
        return None
    if Path(value).is_absolute():
        return str(Path(value).resolve())
    from packages.orchestration.config import ConfigSource

    base = project_path if source == ConfigSource.PROJECT else user_path
    return str((Path(base).parent / value).resolve())


def _reject_env_sourced_keys(cfg: RemedyConfig) -> None:
    """(a) none of the three keys may come from the environment.

    A level change must leave a file edit behind, which is the paper trail the feature exists
    to keep.
    """
    from packages.orchestration.config import ConfigSource

    for key, env_var in (
        ("autonomy.level", "REMEDY_AUTONOMY_LEVEL"),
        ("autonomy.gauntlet_evidence", "REMEDY_AUTONOMY_GAUNTLET_EVIDENCE"),
        ("autonomy.change_adr", "REMEDY_AUTONOMY_CHANGE_ADR"),
    ):
        if cfg.get_source(key) == ConfigSource.ENV:
            raise AutonomyConfigError(
                f"{key} is set by the environment variable {env_var}, and the autonomy level is "
                f"changed only by editing a config file. Unset {env_var} and set {key} in "
                "remedy.toml."
            )


def _check_gauntlet_evidence(level: str, evidence: str | None, path: str | None) -> None:
    """(d) L3 and higher let Remedy start work unattended, so the gauntlet that proved it can be
    trusted to do that must be named, must exist, and must have actually passed.
    """
    if level == "L2":
        return
    if evidence is None:
        raise AutonomyConfigError(
            f"Autonomy level {level} in {path} lets Remedy start work on its own, so it "
            "needs the gauntlet that proved it can: set autonomy.gauntlet_evidence to the "
            "matrix.json of a gauntlet attempt that passed."
        )
    evidence_path = Path(evidence)
    if not evidence_path.is_file():
        raise AutonomyConfigError(f"The gauntlet evidence {evidence} does not exist.")
    try:
        parsed = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        # R-1321's second, smaller defect: a read failure or bytes that are not UTF-8
        # (UnicodeDecodeError, a ValueError) reads the same refusal as evidence that is not JSON —
        # never an uncaught crash out of this loader.
        parsed = None
    if not isinstance(parsed, dict):
        raise AutonomyConfigError(
            "The gauntlet evidence " + evidence + " is not a gauntlet matrix Remedy can read."
        )
    if parsed.get("passed") is not True:
        raise AutonomyConfigError(
            f"The gauntlet evidence {evidence} records a gauntlet that did not pass."
        )


def _previous_level(changes_path: Path, path: str | None) -> str:
    """The `to` of the LAST change line recorded for this config file, or the default."""
    old = AUTONOMY_DEFAULT_LEVEL
    if not changes_path.is_file():
        return old
    for raw_line in changes_path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        try:
            record = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if (isinstance(record, dict) and isinstance(record.get("config_path"), str)
                and isinstance(record.get("to"), str) and record["config_path"] == path):
            old = record["to"]
    return old


def _record_change(
    changes_dir: Path, changes_path: Path, *, path: str | None, config_path: str | None,
    old: str, new: str, change_adr: str | None, source: str, when: datetime,
) -> None:
    """(e) check the decision record and append one change line, creating the folder.

    PATH is the config file as the report holds it, named in both refusal sentences below.
    CONFIG_PATH is that same file resolved to one absolute string (R-1321): the only form the
    written record, and AutonomyPolicy.config_path, ever carry.
    """
    if change_adr is None:
        raise AutonomyConfigError(
            f"The autonomy level in {path} changed from {old} to {new}, and every change needs "
            "its decision record: set autonomy.change_adr to the file that records why."
        )
    if not Path(change_adr).is_file():
        raise AutonomyConfigError(
            f"The decision record {change_adr} for the change from {old} to {new} does not "
            "exist."
        )
    changes_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "at": when.isoformat(), "config_path": config_path, "from": old, "to": new,
        "change_adr": change_adr, "source": source,
    }
    with changes_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def load_autonomy_policy(
    config: RemedyConfig | None = None,
    *,
    root: Path | None = None,
    now: datetime | None = None,
) -> AutonomyPolicy:
    """The autonomy level in force, validated, with its supporting keys and any change recorded.

    See DECISION F078 D1 (4) for the five checks this performs, in order: no key may come from
    the environment; a level from no file is the default and reads or writes nothing; the level
    must be one of AUTONOMY_LEVELS; L3 and higher need gauntlet evidence that actually passed;
    and a level that differs from the last one recorded for this config file needs a decision
    record, which is then appended to <data root>/autonomy/level_changes.jsonl.
    """
    from packages.orchestration.config import ConfigSource, get_config

    cfg = config if config is not None else get_config()
    data_root = root if root is not None else resolve_data_root()
    when = now if now is not None else datetime.now(timezone.utc)

    _reject_env_sourced_keys(cfg)

    level_value = cfg.get_value("autonomy.level")

    # (b) no config file set a level: the built-in default, reading and writing nothing.
    if level_value.source == ConfigSource.DEFAULT:
        return AutonomyPolicy(AUTONOMY_DEFAULT_LEVEL, None, None, None, None)

    level = level_value.value
    report = cfg.load_report
    path = report.project_path if level_value.source == ConfigSource.PROJECT else report.user_path

    # (c) a level outside L2 to L5 is not one Remedy can run at.
    if not isinstance(level, str) or level not in AUTONOMY_LEVELS:
        raise AutonomyConfigError(
            f"The autonomy level {level!r} in {path} is not one of L2, L3, L4 or L5."
        )

    evidence_value = cfg.get_value("autonomy.gauntlet_evidence")
    change_adr_value = cfg.get_value("autonomy.change_adr")
    evidence = _resolve_relative_path(
        evidence_value.value, evidence_value.source, report.project_path, report.user_path)
    change_adr = _resolve_relative_path(
        change_adr_value.value, change_adr_value.source, report.project_path, report.user_path)

    _check_gauntlet_evidence(level, evidence, path)

    # R-1321: the record is keyed by the level's config file RESOLVED to one absolute path, never
    # by the string the report holds — a relative `load_config(project_path=...)` call (the
    # unconfigured default included) can hand that same string back from two different folders.
    # The refusal sentences above and below keep naming the file as the report holds it; only the
    # key and AutonomyPolicy.config_path take the resolved form.
    resolved_path = str(Path(path).resolve()) if path is not None else None

    # (e) every accepted level is one line in <data root>/autonomy/level_changes.jsonl, keyed by
    # the config file it came from, so two projects at two levels never read as changing each other.
    changes_dir = data_class_dir("autonomy", data_root)
    changes_path = changes_dir / AUTONOMY_CHANGES_FILENAME
    old = _previous_level(changes_path, resolved_path)

    if old == level:
        return AutonomyPolicy(level, resolved_path, evidence, change_adr, None)

    _record_change(
        changes_dir, changes_path, path=path, config_path=resolved_path, old=old, new=level,
        change_adr=change_adr, source=level_value.source.value, when=when,
    )
    return AutonomyPolicy(level, resolved_path, evidence, change_adr, old)


# ---------------------------------------------------------------------------
# T002: the mission loop's own starts (DECISION F078 D2)
# ---------------------------------------------------------------------------


@dataclass
class _AutonomyScope:
    """The active `autonomy_start_scope`'s level and how many manual starts it still holds."""

    level: str
    manual_starts: int


# None outside `autonomy_start_scope`; the running loop's own grant while inside one. A ContextVar
# rather than a module global so two missions running at once never see each other's scope.
_ACTIVE_SCOPE: ContextVar[_AutonomyScope | None] = ContextVar("_autonomy_active_scope", default=None)


@contextmanager
def autonomy_start_scope(policy: AutonomyPolicy, *, manual_starts: int):
    """Grant the caller MANUAL_STARTS starts of its own before the mission loop's own apply.

    `remedy mission run` opens one around its whole `run_mission` call, with `manual_starts=1`:
    its own command is the start of the first job the run dispatches, and every further dispatch
    in the same run is the loop's own (DECISION F078 D2 (1)). Reset on exit, including on an
    exception, so a crashed run never leaves a stale scope for the next one in the same process.
    """
    token = _ACTIVE_SCOPE.set(_AutonomyScope(level=policy.level, manual_starts=manual_starts))
    try:
        yield
    finally:
        _ACTIVE_SCOPE.reset(token)


def _deferred_path(root: Path | None) -> Path:
    data_root = root if root is not None else resolve_data_root()
    return data_class_dir("autonomy", data_root) / AUTONOMY_DEFERRED_FILENAME


def _deferred_records(path: Path) -> list[dict[str, Any]]:
    """Every object line of PATH that parses as one; a line that is not one is skipped."""
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        try:
            record = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def _open_by_mission(path: Path) -> dict[tuple[Any, Any], list[dict[str, Any]]]:
    """Every deferred line not yet closed by a later taken line of the same project and mission."""
    open_lines: dict[tuple[Any, Any], list[dict[str, Any]]] = {}
    for record in _deferred_records(path):
        key = (record.get("project_id"), record.get("mission_id"))
        if record.get("event") == _EVENT_DEFERRED:
            open_lines.setdefault(key, []).append(record)
        elif record.get("event") == _EVENT_TAKEN:
            open_lines[key] = []
    return open_lines


def claim_loop_start(
    project_id: str, mission_id: str, milestone_id: str, *,
    root: Path | None = None, now: datetime | None = None,
) -> AutonomyStartVerdict | None:
    """Answer whether THIS start may proceed; None outside any `autonomy_start_scope`.

    Inside one (DECISION F078 D2 (2)), a manual start left in the scope is spent first and
    answers `autonomy_may_start("manual", level)` — the operator's own command, which closes any
    open deferral of this mission with one `taken` line. Once the grant is spent, every further
    start in the scope asks `autonomy_may_start("orchestrator", level)`; a refusal writes one
    `deferred` line and the caller ends the run without creating a job.
    """
    scope = _ACTIVE_SCOPE.get()
    if scope is None:
        return None
    when = now if now is not None else datetime.now(timezone.utc)
    path = _deferred_path(root)

    if scope.manual_starts > 0:
        scope.manual_starts -= 1
        verdict = autonomy_may_start(START_ORIGIN_MANUAL, scope.level)
        if _open_by_mission(path).get((project_id, mission_id)):
            path.parent.mkdir(parents=True, exist_ok=True)
            record = {
                "event": _EVENT_TAKEN, "at": when.isoformat(),
                "project_id": project_id, "mission_id": mission_id,
            }
            with path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")
        return verdict

    verdict = autonomy_may_start(START_ORIGIN_ORCHESTRATOR, scope.level)
    if not verdict.allowed:
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "event": _EVENT_DEFERRED, "at": when.isoformat(), "origin": START_ORIGIN_ORCHESTRATOR,
            "level": scope.level, "project_id": project_id, "mission_id": mission_id,
            "milestone_id": milestone_id,
        }
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    return verdict


def open_deferred_starts(root: Path | None = None) -> list[dict[str, Any]]:
    """Every deferred start not yet closed by a taken line of the same project and mission."""
    path = _deferred_path(root)
    return [record for records in _open_by_mission(path).values() for record in records]


def deferral_detail(
    verdict: AutonomyStartVerdict, project_id: str, mission_id: str, milestone_id: str,
) -> str:
    """The run's detail when a start is deferred: the verdict's reason, and how to start it by hand."""
    return (
        f"{verdict.reason} The next job of milestone {milestone_id} waits for you: run "
        f"`remedy mission run {mission_id} --project {project_id}` to start it yourself."
    )

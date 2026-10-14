"""Who may START work on Remedy's own initiative, and at which level (F078, DECISION F078 D1).

Every approval, fence, budget and watchdog still applies at every level; this module only answers
who may BEGIN a job, never what that job may then do.

Its levels are spelled `L2` to `L5`, and they are NOT the 0 to 7 readiness scale of
`packages.orchestration.autonomy_readiness`, which measures infrastructure readiness — a
different question entirely.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from packages.orchestration.data_paths import data_class_dir, resolve_data_root

if TYPE_CHECKING:  # import-light at runtime: config.py's types are only named here
    from packages.orchestration.config import ConfigSource, RemedyConfig

# F078's levels, spelled with their L — never autonomy_readiness's 0 to 7 scale.
AUTONOMY_LEVELS: tuple[str, ...] = ("L2", "L3", "L4", "L5")

# The level Remedy runs at until an operator configures otherwise.
AUTONOMY_DEFAULT_LEVEL = "L2"

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


def _resolve_relative_path(value: str | None, source: ConfigSource,
                            project_path: str | None, user_path: str | None) -> str | None:
    """Resolve VALUE against the folder of the config file of its OWN source; keep it if absolute."""
    if value is None:
        return None
    if Path(value).is_absolute():
        return value
    from packages.orchestration.config import ConfigSource

    base = project_path if source == ConfigSource.PROJECT else user_path
    return str(Path(base).parent / value)


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
    except json.JSONDecodeError:
        parsed = None
    if not isinstance(parsed, dict):
        raise AutonomyConfigError(
            f"The gauntlet evidence {evidence} is not a gauntlet matrix Remedy can read."
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
    changes_dir: Path, changes_path: Path, *, path: str | None, old: str, new: str,
    change_adr: str | None, source: str, when: datetime,
) -> None:
    """(e) check the decision record and append one change line, creating the folder."""
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
        "at": when.isoformat(), "config_path": path, "from": old, "to": new,
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

    # (e) every accepted level is one line in <data root>/autonomy/level_changes.jsonl, keyed by
    # the config file it came from, so two projects at two levels never read as changing each other.
    changes_dir = data_class_dir("autonomy", data_root)
    changes_path = changes_dir / AUTONOMY_CHANGES_FILENAME
    old = _previous_level(changes_path, path)

    if old == level:
        return AutonomyPolicy(level, path, evidence, change_adr, None)

    _record_change(
        changes_dir, changes_path, path=path, old=old, new=level, change_adr=change_adr,
        source=level_value.source.value, when=when,
    )
    return AutonomyPolicy(level, path, evidence, change_adr, old)

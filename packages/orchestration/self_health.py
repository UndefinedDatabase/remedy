"""F199 — Remedy's own health: the checks `remedy doctor health` runs.

DECISION F199 D1 fixes the shape: every check answers one `HealthCheckResult`
(PASS, WARN or FAIL, a detail and a hint that names what to do). No check
repairs, moves or deletes anything, and no check calls a provider; each one
only reads. Round 2 wires these checks into the command.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.budget_guard import free_disk_bytes
from packages.orchestration.budget_resolution import resolve_min_free_disk_bytes
from packages.orchestration.config import RemedyConfig, get_config, validate_config
from packages.orchestration.data_paths import projects_dir, resolve_data_root
from packages.orchestration.data_reclaim import reclaim_preview_bytes
from packages.orchestration.token_ledger import LEDGER_FILENAME

# The three levels a check can answer, in rising severity.
HEALTH_PASS = "PASS"
HEALTH_WARN = "WARN"
HEALTH_FAIL = "FAIL"
HEALTH_LEVELS: tuple[str, ...] = (HEALTH_PASS, HEALTH_WARN, HEALTH_FAIL)


# One check's answer; `as_json` is the shape the command prints under --json.
@dataclass(frozen=True)
class HealthCheckResult:
    check: str
    level: str
    detail: str
    hint: str = ""

    def as_json(self) -> dict[str, str]:
        return {
            "check": self.check,
            "level": self.level,
            "detail": self.detail,
            "hint": self.hint,
        }


# A detail must not leak the operator's home folder into a pasted report.
def home_relative_text(text: str, home: Path | None = None) -> str:
    home_text = str(home if home is not None else Path.home())
    if home_text == "/":
        return text
    return text.replace(home_text, "~")


def _result(check: str, level: str, detail: str, hint: str = "") -> HealthCheckResult:
    return HealthCheckResult(check, level, home_relative_text(detail), hint)


def _first_three(items: list[str]) -> str:
    text = "; ".join(items[:3])
    if len(items) > 3:
        text += f"; and {len(items) - 3} more"
    return text


# The one next step for a configuration problem.
CONFIG_HINT: str = (
    "run `remedy config validate` to list every problem, then correct the "
    "named key in remedy.toml or its environment variable"
)


# Check `config`: the settings are readable and every value has its declared type.
def check_config_coherence(config: RemedyConfig | None = None) -> HealthCheckResult:
    try:
        resolved = config if config is not None else get_config()
    except (OSError, ValueError) as error:
        return _result(
            "config", HEALTH_FAIL,
            f"the configuration could not be read: {error}", CONFIG_HINT)
    problems = validate_config(resolved)
    if problems:
        return _result(
            "config", HEALTH_FAIL,
            f"{len(problems)} configured values do not have their declared type: "
            f"{_first_three(problems)}", CONFIG_HINT)
    warnings = list(resolved.load_report.warnings)
    if warnings:
        return _result(
            "config", HEALTH_WARN,
            f"{len(warnings)} warnings while reading the configuration: "
            f"{_first_three(warnings)}", CONFIG_HINT)
    return _result("config", HEALTH_PASS, "every configured value has its declared type")


# The one next step for a damaged ledger: set it aside, never delete it.
LEDGER_HINT: str = (
    "move the named ledger aside, for example to ledger.sqlite.bad; Remedy "
    "starts an empty ledger at the next run, and the moved file keeps the old cost history"
)


def _ledger_problem(path: Path) -> str:
    """The integrity problem of one ledger, or "" when SQLite finds none.

    Opens with `mode=rw` and `query_only`, so the check can neither create nor
    write the file; see `token_ledger._connect_readonly` for why `mode=rw` and
    not `mode=ro`. The handle is always closed.
    """
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(
            f"{path.resolve().as_uri()}?mode=rw", uri=True, timeout=5)
        connection.execute("PRAGMA query_only=1")
        rows = connection.execute("PRAGMA integrity_check").fetchall()
        if rows == [("ok",)]:
            return ""
        return "; ".join(str(row[0]) for row in rows[:3])
    except sqlite3.DatabaseError as error:
        return str(error)
    finally:
        if connection is not None:
            connection.close()


# Check `ledgers`: every project's token ledger passes SQLite's own integrity check.
def check_ledger_integrity(root: Path | None = None) -> HealthCheckResult:
    projects = projects_dir(root)
    ledgers = sorted(projects.glob(f"*/{LEDGER_FILENAME}"))
    if not ledgers:
        return _result("ledgers", HEALTH_PASS, "no token ledger exists yet")
    data_root = projects.parent
    bad: list[str] = []
    for ledger in ledgers:
        problem = _ledger_problem(ledger)
        if problem:
            bad.append(f"{ledger.relative_to(data_root).as_posix()} ({problem})")
    if bad:
        return _result(
            "ledgers", HEALTH_FAIL,
            f"{len(bad)} of {len(ledgers)} token ledgers failed SQLite's integrity check: "
            + "; ".join(bad), LEDGER_HINT)
    return _result(
        "ledgers", HEALTH_PASS,
        f"{len(ledgers)} of {len(ledgers)} token ledgers passed SQLite's integrity check")


# The one next step for large leftover staging copies.
RECLAIM_HINT: str = (
    "preview them with `remedy data reclaim --orphans`, then free them with "
    "`remedy data reclaim --orphans --apply`"
)


# Check `staging_copies`: leftover working copies have not grown past the warning level.
def check_staging_copies(
    root: Path | None = None, warn_gb: int | None = None,
) -> HealthCheckResult:
    try:
        size = reclaim_preview_bytes(root if root is not None else resolve_data_root())
        level_gb = warn_gb if warn_gb is not None else int(
            get_config().get("data.reclaim_warn_gb"))
    except (OSError, ValueError, TypeError) as error:
        return _result(
            "staging_copies", HEALTH_WARN,
            f"the staging copies could not be measured: {error}", RECLAIM_HINT)
    gb = size / 1024 ** 3
    if size >= level_gb * 1024 ** 3:
        return _result(
            "staging_copies", HEALTH_WARN,
            f"{gb:.1f} GB of staging copies can be freed, at or above the "
            f"warning level of {level_gb} GB", RECLAIM_HINT)
    return _result(
        "staging_copies", HEALTH_PASS,
        f"{gb:.1f} GB of staging copies can be freed, below the warning level of {level_gb} GB")


# The one next step for a disk under its configured floor.
DISK_HINT: str = (
    "free disk space under the data root, or lower budget.min_free_disk_bytes; "
    "`remedy data reclaim --orphans` previews what Remedy's own staging copies would free"
)


# Check `disk`: the free disk is at or above the configured floor.
def check_disk_floor(probe: Callable[[], int] | None = None) -> HealthCheckResult:
    try:
        free = free_disk_bytes(probe)
        floor = resolve_min_free_disk_bytes()
    except (OSError, ValueError) as error:
        return _result(
            "disk", HEALTH_WARN, f"the free disk could not be read: {error}", CONFIG_HINT)
    if floor is None:
        return _result(
            "disk", HEALTH_PASS,
            f"{free} bytes free; no floor is configured (budget.min_free_disk_bytes)")
    if free < floor:
        return _result(
            "disk", HEALTH_FAIL,
            f"{free} bytes free, below the configured floor of {floor} bytes", DISK_HINT)
    return _result("disk", HEALTH_PASS, f"{free} bytes free; the floor is {floor} bytes")


# The fixed order `remedy doctor health` prints the checks in.
def run_health_checks(root: Path | None = None) -> tuple[HealthCheckResult, ...]:
    return (
        check_config_coherence(),
        check_ledger_integrity(root),
        check_staging_copies(root),
        check_disk_floor(),
    )


# The worst level among the results; an empty set is healthy.
def health_verdict(results: tuple[HealthCheckResult, ...] | list[HealthCheckResult]) -> str:
    worst = HEALTH_PASS
    for result in results:
        if HEALTH_LEVELS.index(result.level) > HEALTH_LEVELS.index(worst):
            worst = result.level
    return worst


# Only a FAIL makes the command exit non-zero; a WARN is told, not enforced.
def health_exit_code(results: tuple[HealthCheckResult, ...] | list[HealthCheckResult]) -> int:
    return 1 if any(result.level == HEALTH_FAIL for result in results) else 0

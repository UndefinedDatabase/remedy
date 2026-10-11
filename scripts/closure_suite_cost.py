#!/usr/bin/env python3
"""The closure suite's CPU cost, read from the test load record, against the previous closure's.

F293 T003 (DECISION F293 D9). The integration-gate round of every closure runs the full suite
once, ``python3 -m pytest -n auto -q``, and ``tests/conftest.py`` appends one line for that run to
the test load record. This script finds the newest line for exactly that command and prints one
``Test load:`` line, which the worker copies into ``.agent/authored/f<id>-closure-suite.txt``. It
then reads every other closure transcript under ``.agent/authored/`` for its own ``Test load:``
line, takes the newest one recorded before this run, and says whether this closure costs more than
10 percent above it. More than 10 percent means the closure registers a finding owned by the
rolling findings paydown, and the exit code is 1, so the step cannot pass by being read quickly.

Since R-1139 each line of the record carries the CPU seconds of every test module, and the script
names the modules whose time rose most since the previous closure's run, read from that run's own
line, so a closure can say where a rise lies without a second run.

Exit codes: 0 within the limit, or no earlier closure to compare with; 1 above the limit; 2 the
record cannot be read or holds no line for the full-suite command.

Usage: python3 scripts/closure_suite_cost.py --feature F293 --record ~/.remedy-loop/test_load.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

#: The command field ``tests/conftest.py`` records for ``python3 -m pytest -n auto -q``.
FULL_SUITE_COMMAND = "pytest -n auto -q"
#: A closure costing more than this many percent above the previous one registers a finding.
LIMIT_PERCENT = 10.0
TRANSCRIPT_GLOB = "f*-closure-suite.txt"
#: How many modules the report of a rise names (R-1139).
TOP_MODULES = 10
LINE = re.compile(
    r"^Test load: (?P<cpu>\d+(?:\.\d+)?) CPU seconds, .* recorded "
    r"(?P<utc>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)$", re.MULTILINE)


def newest_full_suite_run(record: Path) -> dict | None:
    """The newest line of the record for the full-suite command, or None."""
    newest = None
    for raw in record.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = json.loads(raw)
            if row.get("command") != FULL_SUITE_COMMAND:
                continue
            run = {"utc": str(row["utc"]), "cpu_seconds": float(row["cpu_seconds"]),
                   "wall_seconds": float(row["wall_seconds"]), "collected": int(row["collected"]),
                   "exit_status": int(row["exit_status"]),
                   "modules": dict(row.get("module_cpu_seconds") or {})}
        except (ValueError, TypeError, KeyError, AttributeError):
            continue
        if LINE.fullmatch(transcript_line(run)) and (newest is None or run["utc"] >= newest["utc"]):
            newest = run
    return newest


def transcript_line(run: dict) -> str:
    return (f"Test load: {run['cpu_seconds']:.2f} CPU seconds, {run['wall_seconds']:.2f} wall "
            f"seconds, {run['collected']} tests collected, exit status {run['exit_status']}, "
            f"recorded {run['utc']}")


def previous_closure(authored: Path, feature: str, before_utc: str) -> dict | None:
    """The newest ``Test load:`` line of another feature's transcript recorded before ``before_utc``."""
    own = f"{feature.lower()}-closure-suite.txt"
    best = None
    for path in sorted(authored.glob(TRANSCRIPT_GLOB)):
        if path.name == own:
            continue
        for match in LINE.finditer(path.read_text(encoding="utf-8", errors="replace")):
            utc = match["utc"]
            if utc < before_utc and (best is None or utc > best["utc"]):
                best = {"feature": path.name.split("-", 1)[0].upper(), "utc": utc,
                        "cpu_seconds": float(match["cpu"])}
    return best


def compare(cpu_seconds: float, previous: dict | None) -> tuple[str, int]:
    """One plain sentence about this closure's cost against the previous one, and the exit code."""
    if previous is None:
        return ("No earlier closure transcript carries a Test load line, so there is nothing to "
                "compare this closure with.", 0)
    before = previous["cpu_seconds"]
    percent = (cpu_seconds - before) / before * 100 if before > 0 else 0.0
    direction = "more" if percent >= 0 else "less"
    head = (f"This closure's suite used {cpu_seconds:.2f} CPU seconds, {abs(percent):.1f} percent "
            f"{direction} than {previous['feature']}'s {before:.2f}")
    if percent > LIMIT_PERCENT:
        return (head + f"; that is above the {LIMIT_PERCENT:.0f} percent limit, so this closure "
                "registers a finding owned by the rolling findings paydown.", 1)
    return head + f", within the {LIMIT_PERCENT:.0f} percent limit.", 0


def full_suite_modules_at(record: Path, utc: str) -> dict | None:
    """The module CPU seconds of the full-suite line recorded at UTC, or None when it has none."""
    for raw in record.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = json.loads(raw)
        except ValueError:
            continue
        if (isinstance(row, dict) and row.get("command") == FULL_SUITE_COMMAND
                and row.get("utc") == utc and row.get("module_cpu_seconds")):
            return dict(row["module_cpu_seconds"])
    return None


def module_rises(now: dict, before: dict, top: int = TOP_MODULES) -> list[str]:
    """The modules whose CPU seconds rose most from BEFORE to NOW, largest first, one line each."""
    rises = sorted(((float(now[m]) - float(before.get(m, 0.0)), m) for m in now),
                   key=lambda pair: (-pair[0], pair[1]))
    return [f"  +{rise:.2f} s  {module} ({float(before.get(module, 0.0)):.2f} -> {float(now[module]):.2f})"
            for rise, module in rises[:top] if rise > 0]


def module_report(record: Path, run: dict, previous: dict | None) -> list[str]:
    """What the record can say about where this closure's time went, against the previous closure."""
    if previous is None:
        return []
    if not run["modules"]:
        return ["This run recorded no CPU time per test module, so no module is named."]
    before = full_suite_modules_at(record, previous["utc"])
    if before is None:
        return [f"{previous['feature']}'s closure run recorded no CPU time per test module, so no "
                "module is named."]
    rises = module_rises(run["modules"], before)
    if not rises:
        return [f"No test module's CPU time rose since {previous['feature']}'s closure run."]
    return [f"The test modules whose CPU time rose most since {previous['feature']}'s closure run:",
            *rises]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--feature", required=True, help="the closing feature's id, e.g. F293")
    parser.add_argument("--record", required=True, type=Path, help="the test load record file")
    parser.add_argument("--authored", type=Path, default=Path(".agent/authored"),
                        help="the folder holding the closure transcripts")
    args = parser.parse_args(argv)
    try:
        run = newest_full_suite_run(args.record)
    except OSError as exc:
        print(f"The test load record {args.record} cannot be read: {exc.strerror or exc}.")
        return 2
    if run is None:
        print(f"The test load record {args.record} holds no line for `{FULL_SUITE_COMMAND}`, so "
              "this closure's cost is unknown.")
        return 2
    previous = previous_closure(args.authored, args.feature, run["utc"])
    sentence, code = compare(run["cpu_seconds"], previous)
    print(transcript_line(run))
    print(sentence)
    for line in module_report(args.record, run, previous):
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())

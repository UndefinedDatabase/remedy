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
                   "exit_status": int(row["exit_status"])}
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
    sentence, code = compare(run["cpu_seconds"],
                             previous_closure(args.authored, args.feature, run["utc"]))
    print(transcript_line(run))
    print(sentence)
    return code


if __name__ == "__main__":
    sys.exit(main())

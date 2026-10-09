"""F300 T002, DECISION F300 D2 — the structure ratchet.

The two tables at the end of `docs/system/structure-ledger-v1.md` — "Functions above 100 lines"
and "Files above 1,000 lines" — are Remedy's own record of its structural debts. This test
re-measures the same scope and fails on: a function or file whose size rose past its row; a new
function or file above its limit with no row; a size that fell without its row lowered in the same
commit; a row whose entry is no longer above the limit; and a pin (`MAX_FUNCTION_ROWS`,
`MAX_FUNCTION_LINES`, `MAX_FILE_ROWS`, `MAX_FILE_LINES`) raised without the table it pins actually
matching it. The rule that pays these debts down is the section "The structure rule" of
`docs/agents/self_drive_protocol.md`.
"""
from __future__ import annotations

import functools
import re
from pathlib import Path

from packages.orchestration.structure_measure import (
    DEFAULT_FILE_LIMIT,
    DEFAULT_FUNCTION_LIMIT,
    StructureMeasure,
    measure_repository,
)

REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "docs/system/structure-ledger-v1.md"

#: The scope Remedy's own ledger covers: tracked files under these roots, without the one file
#: npm writes and no person edits.
SCOPE = ("packages", "apps", "scripts", ":(exclude)apps/ui/package-lock.json")

#: The row count of "Functions above 100 lines" when the ledger was built (DECISION F300 D2).
#: Equals the record; only ever falls, and is raised only by the DECISION rule 5 of the
#: structure rule requires.
MAX_FUNCTION_ROWS = 162
#: The summed `Lines` column of "Functions above 100 lines" when the ledger was built.
#: Equals the record; only ever falls, and is raised only by the DECISION rule 5 of the
#: structure rule requires.
MAX_FUNCTION_LINES = 31229
#: The row count of "Files above 1,000 lines" when the ledger was built (DECISION F300 D2).
#: Equals the record; only ever falls, and is raised only by the DECISION rule 5 of the
#: structure rule requires.
MAX_FILE_ROWS = 39
#: The summed `Lines` column of "Files above 1,000 lines" when the ledger was built.
#: Equals the record; only ever falls, and is raised only by the DECISION rule 5 of the
#: structure rule requires.
MAX_FILE_LINES = 79458

_FUNCTION_ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \| `([^`]+)` \|$")
_FILE_ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \|$")

FunctionRow = tuple[int, str, str]
FileRow = tuple[int, str]


@functools.cache
def _measure() -> StructureMeasure:
    return measure_repository(REPO, paths=SCOPE)


@functools.cache
def _ledger_rows() -> tuple[tuple[FunctionRow, ...], tuple[FileRow, ...]]:
    """The ledger page's two tables, read once per process: (function rows, file rows)."""
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    function_rows: list[FunctionRow] = []
    file_rows: list[FileRow] = []

    start = lines.index("## Functions above 100 lines")
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        match = _FUNCTION_ROW.match(line)
        if match:
            function_rows.append((int(match.group(1)), match.group(2), match.group(3)))

    start = lines.index("## Files above 1,000 lines")
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        match = _FILE_ROW.match(line)
        if match:
            file_rows.append((int(match.group(1)), match.group(2)))

    return tuple(function_rows), tuple(file_rows)


def test_the_limits_are_100_and_1000() -> None:
    assert DEFAULT_FUNCTION_LIMIT == 100
    assert DEFAULT_FILE_LIMIT == 1000


def test_every_function_equals_its_row() -> None:
    measure = _measure()
    function_rows, _ = _ledger_rows()
    row_by_key = {(file, name): lines for lines, file, name in function_rows}
    measured_by_key = {(f.path, f.name): f.lines for f in measure.large_functions}

    problems = []
    for (file, name), lines in measured_by_key.items():
        row = row_by_key.get((file, name))
        if row is None:
            problems.append(
                f"`{name}` (`{file}`) has {lines} lines, above the limit, and no row: cut it "
                f"below the limit")
        elif lines > row:
            problems.append(f"`{name}` (`{file}`) grew from {row} to {lines} lines: cut it back")
        elif lines < row:
            problems.append(f"`{name}` (`{file}`) fell from {row} to {lines} lines: lower its row")
    for file, name in row_by_key:
        if (file, name) not in measured_by_key:
            problems.append(f"`{name}` (`{file}`) is no longer above the limit: delete its row")

    assert not problems, "\n".join(problems)


def test_every_file_equals_its_row() -> None:
    measure = _measure()
    _, file_rows = _ledger_rows()
    row_by_key = {file: lines for lines, file in file_rows}
    measured_by_key = {f.path: f.lines for f in measure.large_files}

    problems = []
    for file, lines in measured_by_key.items():
        row = row_by_key.get(file)
        if row is None:
            problems.append(
                f"`{file}` has {lines} lines, above the limit, and no row: cut it below the limit")
        elif lines > row:
            problems.append(f"`{file}` grew from {row} to {lines} lines: cut it back")
        elif lines < row:
            problems.append(f"`{file}` fell from {row} to {lines} lines: lower its row")
    for file in row_by_key:
        if file not in measured_by_key:
            problems.append(f"`{file}` is no longer above the limit: delete its row")

    assert not problems, "\n".join(problems)


def test_the_rows_and_their_lines_never_rise() -> None:
    function_rows, file_rows = _ledger_rows()
    problems = []

    if len(function_rows) != MAX_FUNCTION_ROWS:
        problems.append(
            f"{len(function_rows)} function rows, pin MAX_FUNCTION_ROWS is {MAX_FUNCTION_ROWS}: "
            f"match the pin to the table")
    function_lines = sum(lines for lines, _, _ in function_rows)
    if function_lines != MAX_FUNCTION_LINES:
        problems.append(
            f"{function_lines} function lines, pin MAX_FUNCTION_LINES is {MAX_FUNCTION_LINES}: "
            f"match the pin to the table")
    if len(file_rows) != MAX_FILE_ROWS:
        problems.append(
            f"{len(file_rows)} file rows, pin MAX_FILE_ROWS is {MAX_FILE_ROWS}: match the pin to "
            f"the table")
    file_lines = sum(lines for lines, _ in file_rows)
    if file_lines != MAX_FILE_LINES:
        problems.append(
            f"{file_lines} file lines, pin MAX_FILE_LINES is {MAX_FILE_LINES}: match the pin to "
            f"the table")

    assert not problems, "\n".join(problems)


def test_every_large_debt_has_its_boundary() -> None:
    function_rows, file_rows = _ledger_rows()
    text = LEDGER.read_text(encoding="utf-8")

    problems = []
    for lines, file, name in function_rows:
        if lines > 300 and f"`{name}` (`{file}`)" not in text:
            problems.append(
                f"`{name}` (`{file}`) has {lines} lines, above 300, and no boundary in the page: "
                f"write its boundary and steps")
    for lines, file in file_rows:
        if lines > 2000 and f"`{file}`:" not in text:
            problems.append(
                f"`{file}` has {lines} lines, above 2,000, and no boundary in the page: write its "
                f"boundary and steps")

    assert not problems, "\n".join(problems)

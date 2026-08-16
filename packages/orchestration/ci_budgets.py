"""Repository ceilings the `budgets` CI stage checks — DATA plus two pure functions.

The stage TABLE lives in :mod:`packages.orchestration.ci_stages` and the stage
RUNNER in :mod:`packages.orchestration.ci_run`; this module holds the numbers a
`budgets` check compares against and the parsing that turns a tool's own output
into one. Like the stage table it RUNS NOTHING at import: importing a ceiling
must never be able to start a linter or a test run.

Remedy deliberately does NOT fix the lint debt this module freezes (DECISION
F083 D5, finding R-0468). The twenty-six errors are a mass edit across files
this feature does not otherwise touch, which AGENTS.md Scope Control forbids as
its own activity. The ceiling makes the debt VISIBLE and stops it growing, which
is the honest half of the job; lowering it is a branch of its own.

Remedy deliberately does NOT run `ruff` from inside this module. The observed
count is passed IN, so the ceiling logic is testable without a subprocess and
the one test that really does invoke the linter is marked and isolated.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

#: Ruff's own final summary line, singular and plural, e.g. `Found 26 errors.`.
_RUFF_FOUND_LINE = re.compile(r"^Found (\d+) errors?\.$", re.M)

#: Ruff's own wording when it found nothing at all; it prints no `Found` line.
_RUFF_CLEAN_LINE = "All checks passed!"

#: RATCHET (DECISION F083 D5, finding R-0468): the 26 errors `ruff check .`
#: reports at this repository's root under its own pyproject.toml, frozen so the
#: debt cannot grow silently. This number may only be LOWERED, never raised —
#: raising it to make a round green turns the one honest lint signal in this
#: repository into decoration.
LINT_ERROR_CEILING = 26


@dataclass(frozen=True)
class BudgetCheck:
    """One ceiling compared against one observation: what, whether, and by how much."""

    name: str
    ok: bool
    observed: int
    ceiling: int
    detail: str


def parse_ruff_error_count(output: str) -> int:
    """The error count ruff itself reported, read from its own summary line.

    Returns the integer from the final `Found N errors.` line, or 0 when the
    output carries ruff's `All checks passed!` instead. Raises `ValueError`
    naming what it could not parse when neither shape is present — an
    unparseable reading must never be mistaken for a clean one.
    """
    matches = _RUFF_FOUND_LINE.findall(output)
    if matches:
        return int(matches[-1])
    if _RUFF_CLEAN_LINE in output:
        return 0
    tail = output.strip().splitlines()[-1] if output.strip() else "<empty output>"
    raise ValueError(
        f"cannot read a ruff error count: no 'Found N errors.' line and no "
        f"{_RUFF_CLEAN_LINE!r} in the output; its last line was {tail!r}"
    )


def check_lint_ceiling(observed: int) -> BudgetCheck:
    """Compare an observed ruff error count against the ratcheted ceiling."""
    ok = observed <= LINT_ERROR_CEILING
    if ok:
        detail = f"{observed} ruff errors, at or below the ceiling of {LINT_ERROR_CEILING}"
    else:
        detail = (
            f"{observed} ruff errors, ABOVE the ceiling of {LINT_ERROR_CEILING}: "
            f"{observed - LINT_ERROR_CEILING} more than this repository froze. "
            f"Fix the new errors; do not raise the ceiling (DECISION F083 D5)."
        )
    return BudgetCheck(
        name="lint_errors",
        ok=ok,
        observed=observed,
        ceiling=LINT_ERROR_CEILING,
        detail=detail,
    )

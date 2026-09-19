"""Repository checks the `budgets` CI stage runs — pure functions over a tool's output.

The stage TABLE lives in :mod:`packages.orchestration.ci_stages` and the stage
RUNNER in :mod:`packages.orchestration.ci_run`; this module holds the parsing
that turns a tool's own output into a number and the rule that number is judged
by. Like the stage table it RUNS NOTHING at import: importing a check must never
be able to start a linter or a test run.

Remedy deliberately keeps NO lint baseline and NO lint ceiling (DECISION
amend0911-feedback D7, findings R-0468 and R-0469): `ruff check .` must report
zero findings. The ratchet this replaces (DECISION F083 D5, ceiling 26) let the
count drift unnoticed, because a rise that lands inside a round becomes the next
round's base; a check at zero has no base to drift from.

Remedy deliberately does NOT run `ruff` from inside this module. The observed
count is passed IN, so the rule is testable without a subprocess and the one
test that really does invoke the linter is marked and isolated.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

#: Ruff's own final summary line, singular and plural, e.g. `Found 26 errors.`.
_RUFF_FOUND_LINE = re.compile(r"^Found (\d+) errors?\.$", re.M)

#: Ruff's own wording when it found nothing at all; it prints no `Found` line.
_RUFF_CLEAN_LINE = "All checks passed!"


@dataclass(frozen=True)
class BudgetCheck:
    """One rule judged against one observation: what, whether, and what was seen."""

    name: str
    ok: bool
    observed: int
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


def check_lint_clean(observed: int) -> BudgetCheck:
    """Judge an observed ruff error count: any finding at all fails."""
    ok = observed == 0
    if ok:
        detail = "0 ruff errors"
    else:
        detail = (
            f"{observed} ruff error(s): this repository allows none. Fix them; "
            f"do not add a baseline, a ceiling, a noqa or an ignore "
            f"(DECISION amend0911-feedback D7)."
        )
    return BudgetCheck(name="lint_errors", ok=ok, observed=observed, detail=detail)

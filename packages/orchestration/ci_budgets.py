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

import math
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


#: A built asset's own content-hash segment, vite's naming convention
#: (`index-BKD2HAVk.js`): stripped so a rebuild whose bytes did not change in a way
#: that matters — same file, new hash — is never read as a chunk added or removed.
_CHUNK_HASH_RE = re.compile(r"-(?=[0-9A-Za-z_]*[0-9])[0-9A-Za-z_]{6,10}(?=\.[^.]+$)")


def normalize_chunk_name(path: str) -> str:
    """The stable name a built asset is judged under: its vite content hash stripped."""
    return _CHUNK_HASH_RE.sub("", path)


@dataclass(frozen=True)
class BundleReport:
    """One build's own chunk sizes, keyed by `normalize_chunk_name`."""

    chunks: dict[str, int]

    @property
    def total_bytes(self) -> int:
        return sum(self.chunks.values())


def bundle_report(files: dict[str, int]) -> BundleReport:
    """Group a raw `{relative path: bytes}` reading (a `dist/` walk) by its
    normalized chunk name, summing any raw paths that collide after normalization."""
    chunks: dict[str, int] = {}
    for path, size in files.items():
        name = normalize_chunk_name(path)
        chunks[name] = chunks.get(name, 0) + size
    return BundleReport(chunks=chunks)


#: `apps/ui`'s own baseline, a fresh `vite build` measured at DECISION F044 D8
#: (2026-09-30), keyed by `normalize_chunk_name`. The cap below is this total plus
#: 10% (docs/ui/design_reference/acceptance_criteria.md §5); raising it is a decision,
#: never a silent drift.
BUNDLE_BASELINE_CHUNKS: dict[str, int] = {
    "index.html": 414,
    "assets/index.css": 83758,
    "assets/diffHighlightGrammars.js": 1695,
    "assets/index.js": 783940,
    "story/story-player.css": 11940,
    "story/story-player.js": 266239,
}

#: DECISION F044 D8: the cap over the baseline's own total (acceptance_criteria.md §5).
BUNDLE_SIZE_CAP_FACTOR = 1.10


def check_bundle_size(report: BundleReport) -> BudgetCheck:
    """Judge one build's own `BundleReport` against the baseline plus 10%. A breach
    names the chunks that grew, largest delta first."""
    baseline_total = sum(BUNDLE_BASELINE_CHUNKS.values())
    cap = math.ceil(baseline_total * BUNDLE_SIZE_CAP_FACTOR)
    ok = report.total_bytes <= cap
    if ok:
        detail = f"{report.total_bytes} bytes <= cap {cap} (baseline {baseline_total} + 10%)"
    else:
        names = set(report.chunks) | set(BUNDLE_BASELINE_CHUNKS)
        deltas = sorted(
            ((name, report.chunks.get(name, 0) - BUNDLE_BASELINE_CHUNKS.get(name, 0)) for name in names),
            key=lambda pair: pair[1],
            reverse=True,
        )
        grown = ", ".join(f"{name} +{delta}B" for name, delta in deltas if delta > 0)
        detail = (
            f"{report.total_bytes} bytes > cap {cap} (baseline {baseline_total} + 10%); "
            f"grown: {grown or 'no single chunk grew; every chunk shrank or held'}"
        )
    return BudgetCheck(name="bundle_size", ok=ok, observed=report.total_bytes, detail=detail)


#: DECISION F044 D9: the budget `docs/ui/design_reference/acceptance_criteria.md` §5 fixes —
#: "First paint < 1.5s (built bundle, cold)" — in milliseconds, the unit Chrome's own paint
#: timing entries report in.
FIRST_PAINT_BUDGET_MS = 1500


def check_first_paint(observed_ms: int) -> BudgetCheck:
    """Judge one build's own first-contentful-paint reading, in milliseconds, against the
    budget. A breach names both the reading and the overage."""
    ok = observed_ms <= FIRST_PAINT_BUDGET_MS
    if ok:
        detail = f"{observed_ms}ms <= budget {FIRST_PAINT_BUDGET_MS}ms"
    else:
        over = observed_ms - FIRST_PAINT_BUDGET_MS
        detail = f"{observed_ms}ms > budget {FIRST_PAINT_BUDGET_MS}ms (over by {over}ms)"
    return BudgetCheck(name="first_paint", ok=ok, observed=observed_ms, detail=detail)

"""F082 Q7 — "the bench never runs implicitly", pinned as an ENUMERATED ALLOWLIST.

The acceptance criterion is that the capability bench runs on demand and never as
a side effect of doing something else. Until R16 it was the feature's last
UNPINNED criterion: it held only because nothing under ``apps/``, ``packages/``
or ``scripts/`` happened to call the bench's two write entry points.

DECISION F082 D9 chose the allowlist form over a total absence. A total-absence
pin would be falsified by the very round that completes the feature — R17's
fake-provider run is a driver whose whole job is to CALL both entry points — and
a gate that the feature's own completion breaks teaches the next worker to edit
tests to green. So the pin asserts instead that the set of modules calling either
entry point EQUALS :data:`EXPLICIT_BENCH_CALLERS`, which R17 spent on exactly one
name — the bench run's own entry point. "Never implicitly" was never a claim that
nothing calls the bench; it is a claim that nothing calls it as a SIDE EFFECT,
and an enumerated caller is the opposite of an implicit one.

Why an absence test is dangerous when it is the only guard: it reports green for
whatever reason it finds nothing. A scanner pointed at the wrong tree, a walker
that swallowed a parse error, or a rename of the very symbol it guards all empty
its search space, and an emptied search space passes forever while the property
it claimed to protect quietly dies. Properties 1 and 2 below exist ONLY to make
that failure impossible: property 1 fails loudly if either guarded symbol is
renamed away, and property 2 fails loudly if the scan visits nothing. The pin is
shown to be capable of going RED by being MADE to go red — a disposable worktree
adds one call to a scratch module and property 3 fails there.

Callers are found by PARSING each file with :mod:`ast`, never by substring
search. A ``def`` line, a docstring mention, an import and a comment are not
calls, and only a parser can tell them apart; property 4 pins that distinction
against the two real modules that DEFINE the guarded symbols.
"""
from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

from packages.orchestration import bench_dry_run, bench_history

#: Resolved from ``__file__`` and never from the CWD: a scan whose root depends
#: on where pytest was invoked is a scan that can silently address nothing.
REPO_ROOT = Path(__file__).resolve().parents[2]

#: Where each guarded write entry point is DEFINED, repo-relative. Property 4
#: pins that these two files are scanned and are NOT reported as callers of the
#: symbols they define.
GUARDED_ENTRY_POINTS = {
    "packages/orchestration/bench_history.py": "append_bench_run",
    "packages/orchestration/bench_dry_run.py": "dry_run_from_order_set",
}

#: The two names the criterion is about: the only ways the bench writes.
GUARDED_SYMBOLS = frozenset(GUARDED_ENTRY_POINTS.values())

#: The three trees a production caller could live in. ``tests/`` is deliberately
#: NOT scanned: a test calling the bench IS the bench running on demand.
SCANNED_TREES = ("apps", "packages", "scripts")

#: THE ALLOWLIST — repo-relative module paths permitted to call a guarded entry
#: point. ONE name today, R17's, which is a measured fact and not an assumption.
#:
#: R17 ADDED that one name, the bench run's entry point. Adding to this set is a
#: DELIBERATE ACT that says the bench gained an explicit caller, never a repair
#: to make a red test green. A name appearing here without a round that meant to
#: put it here is the failure this pin exists to surface.
EXPLICIT_BENCH_CALLERS: frozenset[str] = frozenset({
    # R17: the fake-provider bench run's entry point. It calls BOTH guarded
    # symbols on purpose — that is what an explicit caller is — and DECISION
    # F082 D9 predicted this exact one name before it existed.
    "packages/orchestration/bench_run.py",
})

#: File counts measured at R16 against this repository: apps 73, packages 256,
#: scripts 29. The assertion below uses FLOORS well beneath those numbers rather
#: than equalities, so an unrelated module added or deleted never breaks this
#: pin, while a scanner that addressed the wrong root or swallowed its walk still
#: fails loudly. The real observed counts are named in the failure message.
MIN_SCANNED_FILES = {"apps": 40, "packages": 150, "scripts": 15}


def _python_files(tree: str) -> list[Path]:
    """Every ``.py`` file under one scanned tree, sorted, cache dirs excluded."""
    root = REPO_ROOT / tree
    if not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*.py") if "__pycache__" not in p.parts)


def _called_names(source: str) -> set[str]:
    """Every name this source CALLS, taken from the parse tree.

    ``ast.Name.id`` covers ``append_bench_run(...)`` and ``ast.Attribute.attr``
    covers ``bench_history.append_bench_run(...)``. A ``def`` statement, an
    import, a docstring and a comment produce no :class:`ast.Call` node at all,
    which is the entire reason this is a parser and not a substring search.
    """
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            names.add(func.id)
        elif isinstance(func, ast.Attribute):
            names.add(func.attr)
    return names


def _scan() -> tuple[dict[str, int], list[tuple[str, str]], list[str]]:
    """Walk the three trees once and report what was seen.

    Returns the per-tree file count, every ``(module, symbol)`` caller pair
    found, and every file that could not be read or parsed. Unreadable files are
    RETURNED rather than skipped: a scanner that goes quiet on a parse error is
    exactly the vacuous pass this file refuses.
    """
    counts: dict[str, int] = {}
    callers: list[tuple[str, str]] = []
    unparseable: list[str] = []
    for tree in SCANNED_TREES:
        files = _python_files(tree)
        counts[tree] = len(files)
        for path in files:
            rel = path.relative_to(REPO_ROOT).as_posix()
            try:
                called = _called_names(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, SyntaxError, ValueError) as exc:
                unparseable.append(f"{rel} ({type(exc).__name__})")
                continue
            for symbol in sorted(called & GUARDED_SYMBOLS):
                callers.append((rel, symbol))
    return counts, callers, unparseable


# ---------------------------------------------------------------------------
# 1. ANTI-VACUOUS, SYMBOLS — the guarded names still exist and are callable
# ---------------------------------------------------------------------------

def test_both_guarded_entry_points_are_importable_and_callable() -> None:
    """A rename must break this file LOUDLY instead of emptying its search space.

    Without this, renaming ``append_bench_run`` would leave the scan below
    searching for a name nothing uses, and a search for a name nothing uses
    passes forever.
    """
    assert callable(bench_history.append_bench_run)
    assert callable(bench_dry_run.dry_run_from_order_set)
    assert GUARDED_SYMBOLS == {"append_bench_run", "dry_run_from_order_set"}


def test_every_guarded_entry_point_file_exists_where_it_is_claimed() -> None:
    """The allowlist's own coordinates are checked, not assumed."""
    missing = [rel for rel in GUARDED_ENTRY_POINTS if not (REPO_ROOT / rel).is_file()]
    assert not missing, f"Guarded entry point files not found: {missing}"


# ---------------------------------------------------------------------------
# 2. ANTI-VACUOUS, SCAN — the walk really visits files, in every tree
# ---------------------------------------------------------------------------

def test_the_scan_visits_python_files_in_every_tree() -> None:
    counts, _, unparseable = _scan()
    assert not unparseable, (
        "Files the caller scan could not parse — a caller could be hiding in "
        f"one of them: {unparseable}"
    )
    too_few = {tree: counts[tree] for tree in SCANNED_TREES
               if counts[tree] < MIN_SCANNED_FILES[tree]}
    assert not too_few, (
        f"The caller scan visited too few files: observed {counts}, "
        f"floors {MIN_SCANNED_FILES}. A scan this small is not evidence of "
        "absence — check REPO_ROOT and SCANNED_TREES before touching the floors."
    )


# ---------------------------------------------------------------------------
# 3. THE CRITERION — callers equal the allowlist, exactly
# ---------------------------------------------------------------------------

def test_only_allowlisted_modules_call_the_bench_write_entry_points() -> None:
    """F082's acceptance criterion, in the D9 form that survives R17's run."""
    _, callers, unparseable = _scan()
    assert not unparseable, f"Unparseable files hide callers: {unparseable}"
    offenders = sorted({module for module, _ in callers} - EXPLICIT_BENCH_CALLERS)
    detail = "; ".join(f"{module} calls {symbol}"
                       for module, symbol in sorted(callers)
                       if module not in EXPLICIT_BENCH_CALLERS)
    assert not offenders, (
        "The bench gained an implicit caller: " + detail + ". "
        "The bench runs ON DEMAND only (F082 acceptance criterion, DECISION "
        "F082 D9). Remove the call, or — if this module is a DELIBERATE, "
        "explicit entry point — add its path to EXPLICIT_BENCH_CALLERS in this "
        "file and say so in the round's handback."
    )
    stale = sorted(EXPLICIT_BENCH_CALLERS - {module for module, _ in callers})
    assert not stale, (
        f"Allowlisted modules that call nothing: {stale}. An allowlist entry "
        "that guards no call is a permission nobody asked for; delete it."
    )


# ---------------------------------------------------------------------------
# 4. THE PARSER TELLS A DEF FROM A CALL — pinned against the two real modules
# ---------------------------------------------------------------------------

def test_a_definition_is_not_reported_as_a_call() -> None:
    """``bench_history.py`` DEFINES ``append_bench_run`` and ``bench_dry_run.py``
    DEFINES ``dry_run_from_order_set``. Both files are scanned, both mention
    their symbol in a ``def`` line, and neither is a caller. A substring grep
    reports both; the parser reports neither, and that gap is why this file
    parses."""
    counts, callers, _ = _scan()
    assert sum(counts.values()) > 0
    scanned = {path.relative_to(REPO_ROOT).as_posix()
               for tree in SCANNED_TREES for path in _python_files(tree)}
    reported = {module for module, _ in callers}
    for rel, symbol in GUARDED_ENTRY_POINTS.items():
        source = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert rel in scanned, f"{rel} was never scanned, so property 3 is blind"
        assert f"def {symbol}(" in source, (
            f"{rel} no longer defines {symbol} — this pin's premise moved")
        assert symbol not in _called_names(source), (
            f"{rel} was read as CALLING {symbol}, but it only defines it")
        assert rel not in reported, f"{rel} was wrongly reported as a caller"


# ---------------------------------------------------------------------------
# 5. NO IMPORT-TIME SIDE EFFECT — the one implicit run the scan cannot see
# ---------------------------------------------------------------------------

def test_importing_the_bench_modules_writes_nothing_to_the_cwd(tmp_path: Path) -> None:
    """Running at IMPORT is the purest form of running implicitly.

    A fresh subprocess, so no module this session already imported can hide the
    effect, with its CWD inside ``tmp_path`` so any relative write lands
    somewhere this test can see.
    """
    before = sorted(p.name for p in tmp_path.iterdir())
    assert before == []
    result = subprocess.run(
        [sys.executable, "-c",
         "import packages.orchestration.bench_history\n"
         "import packages.orchestration.bench_dry_run\n"],
        cwd=str(tmp_path), capture_output=True, text=True, timeout=120,
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
    )
    assert result.returncode == 0, (
        f"Importing the bench modules failed: {result.stderr}")
    after = sorted(p.name for p in tmp_path.iterdir())
    assert after == [], (
        f"Importing the bench modules created {after} in the CWD — the bench "
        "did work at import time, which is running implicitly.")

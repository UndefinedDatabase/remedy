#!/usr/bin/env python3
"""F075 — the self-run gauntlet: run ten curated missions, judge them, report.

This script is deliberately THIN. The pass definition lives in
``packages/orchestration/gauntlet_evaluator.py`` and the report in
``packages/orchestration/gauntlet_matrix.py``; keeping the judgement importable
is what makes ``--dry-run`` a proof rather than a rehearsal — the tests judge
the same code the real campaign will.

Usage::

    python3 scripts/self_run_gauntlet.py --dry-run <evidence-dir> [--only N]
                                         [--format md|json|both] [--out DIR]

``--dry-run`` evaluates ALREADY RECORDED evidence and executes nothing: no
provider call, no mission, no write into the evidence it reads. ``--only N``
selects the Nth run in the canonical (sorted directory name) order — rerunning
one order is cheap and expected, but a real pass must still be ten consecutive
greens from one invocation.

Live execution is T003 and is deliberately absent here: invoking without
``--dry-run`` says so and exits non-zero rather than pretending to run.

Exit codes: 0 = every recorded run flawless · 1 = at least one run not flawless
(or nothing recorded) · 2 = usage error. The non-zero exit on a failed campaign
is the point: a gate that always exits 0 is not a gate.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from packages.orchestration.gauntlet_evaluator import (  # noqa: E402
    GauntletVerdict,
    evaluate_evidence_dir,
)
from packages.orchestration.gauntlet_matrix import (  # noqa: E402
    matrix_json_bytes,
    render_matrix_markdown,
    write_matrix,
)

EXIT_PASS = 0
EXIT_NOT_A_PASS = 1
EXIT_USAGE = 2

#: What a run without ``--dry-run`` gets. Named rather than hinted: the campaign
#: driver is T003, and a harness that quietly did nothing would be worse than one
#: that says what it does not yet do.
LIVE_RUN_UNAVAILABLE = (
    "live execution is not implemented in this round (F075 T003). "
    "Use --dry-run <evidence-dir> to evaluate recorded evidence."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="self_run_gauntlet.py",
        description="Judge a gauntlet campaign against the frozen pass definition.")
    parser.add_argument(
        "--dry-run", metavar="EVIDENCE_DIR", dest="dry_run",
        help="evaluate recorded evidence in this directory; execute nothing")
    parser.add_argument(
        "--only", type=int, metavar="N",
        help="evaluate only the Nth run (1-based, canonical order)")
    parser.add_argument(
        "--format", choices=("md", "json", "both"), default="md",
        help="what to print to stdout (default: md)")
    parser.add_argument(
        "--out", metavar="DIR",
        help="also write matrix.md and matrix.json into DIR")
    parser.add_argument(
        "--label", metavar="NAME",
        help="evidence label used in the report (default: the directory name)")
    return parser


def _emit(verdict: GauntletVerdict, args: argparse.Namespace) -> None:
    label = args.label
    if args.format in ("md", "both"):
        sys.stdout.write(render_matrix_markdown(verdict, label=label))
    if args.format in ("json", "both"):
        sys.stdout.write(matrix_json_bytes(verdict, label=label))
    if args.out:
        write_matrix(verdict, Path(args.out), label=label)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.dry_run:
        parser.error(LIVE_RUN_UNAVAILABLE)  # exits 2

    evidence_dir = Path(args.dry_run)
    if not evidence_dir.is_dir():
        sys.stderr.write(f"no such evidence directory: {evidence_dir}\n")
        return EXIT_USAGE

    try:
        verdict = evaluate_evidence_dir(evidence_dir, only=args.only)
    except IndexError as exc:
        sys.stderr.write(f"{exc}\n")
        return EXIT_USAGE

    _emit(verdict, args)
    return EXIT_PASS if verdict.passed else EXIT_NOT_A_PASS


if __name__ == "__main__":
    raise SystemExit(main())

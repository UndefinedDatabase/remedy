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
    python3 scripts/self_run_gauntlet.py --live <campaign-root> [--only N] ...

``--dry-run`` evaluates ALREADY RECORDED evidence and executes nothing: no
provider call, no mission, no write into the evidence it reads. ``--only N``
selects the Nth run in the canonical (sorted directory name) order — rerunning
one order is cheap and expected, but a real pass must still be ten consecutive
greens from one invocation.

``--live`` runs the frozen ten for real, each in its own isolated data root,
and judges the result with the same evaluator. Give it a campaign root OUTSIDE
the repository: run artifacts are never committed (R-0176). One invocation
means one campaign — there is no resume, because ten consecutive greens from
one invocation is the whole claim.

**A live campaign refuses to start while any order declares an injection class
the product cannot yet degrade.** Three of the four wait on an exception
boundary ``orchestrator_loop.run_mission`` does not have; running their orders
un-injected would spend real tokens producing evidence that omits the very
fault it was supposed to prove. See
:mod:`packages.orchestration.gauntlet_injection`.

Invoking with neither flag says so and exits 2 rather than pretending to run.

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
    "choose a mode: --dry-run <evidence-dir> to evaluate recorded evidence, "
    "or --live <campaign-root> to run the frozen ten for real."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="self_run_gauntlet.py",
        description="Judge a gauntlet campaign against the frozen pass definition.")
    parser.add_argument(
        "--dry-run", metavar="EVIDENCE_DIR", dest="dry_run",
        help="evaluate recorded evidence in this directory; execute nothing")
    parser.add_argument(
        "--live", metavar="CAMPAIGN_ROOT", dest="live",
        help="run the frozen ten for real into this directory (keep it OUTSIDE "
             "the repository) and judge the result")
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


def preflight_injections(orders) -> list[str]:
    """The orders whose declared injections cannot be driven honestly today.

    Checked BEFORE the first provider call: a campaign that discovers this on
    order six has already spent five orders' worth of real tokens on a run it
    could never have judged.
    """
    from packages.orchestration.gauntlet_injection import (
        MissingSeamError,
        check_injections_supported,
    )

    blocked: list[str] = []
    for order in orders:
        try:
            check_injections_supported(order.injections)
        except MissingSeamError as exc:
            blocked.append(f"{order.id}: {exc}")
    return blocked


def run_live(args: argparse.Namespace) -> int:
    """Execute the frozen set once, then judge it with the same evaluator."""
    from packages.orchestration.gauntlet_orders import OrderSetError, load_order_set
    from packages.orchestration.gauntlet_runner import run_campaign

    try:
        orders = load_order_set()
    except OrderSetError as exc:
        sys.stderr.write(f"the frozen order set is not intact: {exc}\n")
        return EXIT_USAGE

    blocked = preflight_injections(orders)
    if blocked:
        sys.stderr.write(
            "refusing to start a live campaign: "
            f"{len(blocked)} order(s) declare an injection class the product "
            "cannot yet degrade, and running them un-injected would produce "
            "evidence that omits the fault it was meant to prove.\n")
        for line in blocked:
            sys.stderr.write(f"  - {line}\n")
        return EXIT_USAGE

    campaign_root = Path(args.live)
    if args.only is not None:
        if args.only < 1 or args.only > len(orders):
            sys.stderr.write(f"--only {args.only} is outside 1..{len(orders)}\n")
            return EXIT_USAGE
        orders = (orders[args.only - 1],)

    def announce(index: int, order, outcome) -> None:
        state = outcome.crashed or outcome.terminal_status
        sys.stderr.write(f"[{index}/{len(orders)}] {order.id}: {state}\n")

    run_campaign(orders, campaign_root, on_order=announce)
    verdict = evaluate_evidence_dir(campaign_root)
    _emit(verdict, args)
    return EXIT_PASS if verdict.passed else EXIT_NOT_A_PASS


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.dry_run and args.live:
        parser.error("choose one mode: --dry-run or --live, not both")  # exits 2
    if args.live:
        return run_live(args)
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

"""Data group command handlers (F276): the data root's footprint, and its reclaim."""

from __future__ import annotations

import os as _os
import sys as _sys
from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok

if TYPE_CHECKING:
    import argparse


def format_data_bytes(n: int) -> str:
    """A byte count for a person: 1023 B, 1.0 KB, 652.0 GB (powers of 1024)."""
    value = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{int(value)} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    raise AssertionError("unreachable")


def _cmd_data_usage(*, json_output: bool = False) -> None:
    from packages.orchestration.data_footprint import (
        FOOTPRINT_CLASSES,
        export_footprint_json,
        footprint,
    )
    from packages.orchestration.data_paths import resolve_data_root

    fp = footprint(resolve_data_root())
    if json_output:
        emit_ok(**export_footprint_json(fp))
        return
    print(f"Data root: {fp.root}")
    if not fp.exists:
        print("  (does not exist — nothing stored yet)")
        return
    totals = fp.class_totals()
    for data_class in FOOTPRINT_CLASSES:
        size, files = totals[data_class]
        print(f"  {data_class:<13} {format_data_bytes(size):>10}  {files} files")
        for child in fp.children:
            if child.data_class == data_class:
                print(f"    {child.name:<22} {format_data_bytes(child.bytes):>10}  {child.files} files")
    print(f"  {'total':<13} {format_data_bytes(fp.total_bytes):>10}  {fp.total_files} files")


def _cmd_data_reclaim(*, apply_it: bool = False, json_output: bool = False,
                      orphans: bool = False) -> None:
    """Preview, or with ``apply_it`` remove, the data root's reclaimable scratch.

    The preview is the DEFAULT and it deletes nothing. ``--apply`` removes exactly
    the paths the plan it just computed holds; `data_reclaim.apply_reclaim` re-checks
    every rule against the live filesystem, so nothing this function prints can widen
    what is deleted.

    ``orphans`` widens the PLAN by one case — a staging copy whose job record is gone,
    which the default refuses — and widens nothing else. It is orthogonal to
    ``apply_it``: the preview is still the default, so ``--orphans`` on its own prints
    a wider preview and deletes nothing at all.

    EXIT CODE (DECISION F276 D3 (e)): 0, including when paths were refused — a refusal
    is the guarded answer the operator asked for. 1 only when a deletion was ATTEMPTED
    and failed, which is a loud failure and not a report.
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.data_reclaim import apply_reclaim, plan_reclaim

    root = resolve_data_root()
    plan = plan_reclaim(root, orphans=orphans)
    outcome = apply_reclaim(plan) if apply_it else None
    _print_reclaim(plan, outcome, json_output=json_output, orphans=orphans)
    if outcome is not None and outcome.had_failure:
        _sys.exit(1)


def _print_reclaim(plan, outcome, *, json_output: bool, orphans: bool = False) -> None:
    """Render one reclaim plan and its outcome. Prints; never decides an exit code."""
    from packages.orchestration.data_reclaim import ORPHAN_JOB_STATE, export_reclaim_json

    if json_output:
        emit_ok(**export_reclaim_json(plan, outcome))
        return

    print(f"Data root: {plan.root}")
    if not plan.exists:
        print("  (does not exist — nothing to reclaim)")
        return

    # Root-relative, because a prefix class's entry IS the top-level child and a
    # "<class>/<name>" join would print `review_staging/review_staging.Ab12Cd`.
    def _rel(path: str) -> str:
        return _os.path.relpath(path, plan.root)

    # After an apply, list what was REALLY removed: a candidate the deletion-time
    # re-check refused is in `plan.candidates` and must not be reported as gone.
    listed = ([c for c in plan.candidates if c.path in set(outcome.removed)]
              if outcome else list(plan.candidates))
    if listed:
        print(f"  {'Removed' if outcome else 'Reclaimable'}:")
        for c in listed:
            print(f"    {_rel(c.path)}  job {c.job_id} ({c.job_state})  "
                  f"{c.age_days:.1f}d  {format_data_bytes(c.bytes)}")
    else:
        print(f"  {'Removed' if outcome else 'Reclaimable'}: nothing")

    # The two numbers an operator decides on, named SEPARATELY: an orphan is reclaimed
    # because no record for it exists, a terminal job's copy because its record says the
    # job is over, and those are different kinds of confidence. Printed ONLY when the
    # operator opted in, so the default preview is byte for byte what it was before,
    # and only when there is something to split: the heading above already says
    # "nothing", and two zero lines under it would be noise, not an answer.
    if orphans and listed:
        orphaned = [c for c in listed if c.job_state == ORPHAN_JOB_STATE]
        ordinary = [c for c in listed if c.job_state != ORPHAN_JOB_STATE]
        for label, group in (("orphans (no job record):", orphaned),
                             ("terminal jobs:", ordinary)):
            print(f"    of those, {label:<26}{len(group)} paths  "
                  f"{format_data_bytes(sum(c.bytes for c in group))}")

    refusals = list(plan.refusals) + list(outcome.refusals if outcome else ())
    if refusals:
        print("  Refused (kept, with the reason):")
        for r in refusals:
            print(f"    {_rel(r.path)}  {r.reason}: {r.detail}  "
                  f"{format_data_bytes(r.bytes)}")
    # DISCOVERABILITY, and the DEFAULT path only. An operator reading hundreds of
    # gigabytes of `job_unresolved` must not have to read the source to learn that
    # `--orphans` exists. Printed when the flag was NOT typed and there is something for
    # it to consider, so it is an answer rather than noise; the `--json` document is
    # untouched by it, which is what keeps the machine shape byte-identical by default.
    if not orphans:
        unresolved = [r for r in refusals if r.reason == "job_unresolved"]
        if unresolved:
            print(f"    {len(unresolved)} of those are job_unresolved "
                  f"({format_data_bytes(sum(r.bytes for r in unresolved))}) — re-run "
                  f"with --orphans to reclaim the ones no record owns any more")

    if plan.unreclaimed:
        print("  Not reclaimed — reclaim addresses ephemeral classes only:")
        for u in plan.unreclaimed:
            print(f"    {u.name} ({u.data_class})  {format_data_bytes(u.bytes)}")

    if outcome:
        print(f"  Freed {format_data_bytes(outcome.freed_bytes)} "
              f"in {len(outcome.removed)} paths")
    else:
        print(f"  Would free {format_data_bytes(plan.total_bytes)} "
              f"in {len(plan.candidates)} paths — nothing deleted; re-run with --apply")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "data.usage": lambda args: _cmd_data_usage(json_output=getattr(args, "json", False)),
    "data.reclaim": lambda args: _cmd_data_reclaim(
        apply_it=getattr(args, "apply", False),
        json_output=getattr(args, "json", False),
        orphans=getattr(args, "orphans", False),
    ),
}

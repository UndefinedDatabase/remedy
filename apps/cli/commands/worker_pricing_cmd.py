"""`remedy worker pricing-update` (F158 T003, DECISION F158 D6).

Imports a maintained price catalog for one worker adapter. The difference to the current catalog is
always shown first, and the file is written only when the command is run again with `--yes`, so no
price changes without a person having seen what changes. The imported file must pass every rule of
`packages/orchestration/price_catalog.py`, and a catalog that changes anything must raise its
`pricing_version`, so each valuation keeps naming the prices it used.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from apps.cli.json_envelope import emit_ok, fail

EXIT_USAGE = 2
EXIT_ERROR = 1


def _cmd_worker_pricing_update(*, file: str, yes: bool, catalog_dir: str | None,
                               json_output: bool) -> None:
    from packages.orchestration.price_catalog import (
        PriceCatalogError,
        plan_price_catalog_update,
        write_price_catalog_update,
    )

    try:
        text = Path(file).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail("unreadable_price_catalog", f"cannot read {file}: {exc}", json_output=json_output,
             exit_code=EXIT_USAGE)
    try:
        update = plan_price_catalog_update(text, directory=Path(catalog_dir) if catalog_dir else None)
    except PriceCatalogError as exc:
        fail("invalid_price_catalog", str(exc), json_output=json_output, exit_code=EXIT_ERROR)
    written = write_price_catalog_update(update) if yes else False

    if json_output:
        emit_ok(adapter=update.adapter, target=str(update.target),
                current_version=update.current_version, new_version=update.new_version,
                changed=update.changed, written=written, diff=list(update.diff),
                warnings=list(update.warnings))
        return
    current = "none" if update.current_version is None else update.current_version
    print(f"Price catalog of {update.adapter}: pricing version {current} to {update.new_version}")
    if not update.changed:
        print("No change: the imported catalog equals the current one, so nothing is written.")
        return
    for line in update.diff:
        print(line)
    for warning in update.warnings:
        print(f"warning: {warning}")
    if written:
        print(f"Wrote {update.target}.")
    else:
        print("Nothing was written. Run the same command again with --yes to write this catalog.")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "worker.pricing-update": lambda args: _cmd_worker_pricing_update(
        file=args.file,
        yes=bool(getattr(args, "yes", False)),
        catalog_dir=getattr(args, "catalog_dir", None),
        json_output=args.json,
    ),
}

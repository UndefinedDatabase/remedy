"""`project catalog-check` / `project catalog-show` handlers (F206 T004, DECISION F206 D4)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse


def _catalog_file_path(catalog_arg: str | None):
    from pathlib import Path

    from packages.orchestration.repo_catalog import repo_catalog_path

    return Path(catalog_arg) if catalog_arg else repo_catalog_path()


def _load_or_fail(path, *, json_output: bool):
    """The catalog at `path`, or `fail("repo_catalog_invalid", ...)` with its cycle, if any."""
    from packages.orchestration.repo_catalog import (
        RepoCatalogCycleError,
        RepoCatalogError,
        load_repo_catalog,
    )

    try:
        return load_repo_catalog(path)
    except RepoCatalogError as exc:
        cycle = list(exc.cycle) if isinstance(exc, RepoCatalogCycleError) else None
        fail("repo_catalog_invalid", str(exc), json_output=json_output,
             exit_code=1, catalog=str(path), cycle=cycle)
    except OSError as exc:
        fail("repo_catalog_invalid", f"{path}: the repository catalog cannot be read: {exc}",
             json_output=json_output, exit_code=1, catalog=str(path), cycle=None)


def _cmd_catalog_check(*, catalog_arg: str | None = None, json_output: bool = False) -> None:
    from packages.orchestration.repo_catalog_plausibility import check_repo_catalog_plausibility

    path = _catalog_file_path(catalog_arg)
    if not path.exists():
        if json_output:
            emit_ok(catalog=str(path), present=False)
        else:
            print(f"No repository catalog at {path}.")
        return

    catalog = _load_or_fail(path, json_output=json_output)
    result = check_repo_catalog_plausibility(catalog)

    if json_output:
        emit_ok(
            catalog=str(path), present=True, valid=True,
            repositories=len(catalog.entries),
            warnings=[dict(w._asdict()) for w in result.warnings],
            skipped=[dict(s._asdict()) for s in result.skipped],
        )
        return
    print(f"Catalog: {path}")
    print(f"Valid: {len(catalog.entries)} repositories.")
    for warning in result.warnings:
        print(f"Warning: {warning.sentence}")
    for skip in result.skipped:
        print(f"Skipped: {skip.pid}: {skip.reason}")


def _cmd_catalog_show(*, catalog_arg: str | None = None, json_output: bool = False) -> None:
    from packages.orchestration.repo_catalog import describe_repo_catalog_edge, repo_catalog_order

    path = _catalog_file_path(catalog_arg)
    if not path.exists():
        if json_output:
            emit_ok(catalog=str(path), present=False)
        else:
            print(f"No repository catalog at {path}.")
        return

    catalog = _load_or_fail(path, json_output=json_output)
    order = repo_catalog_order(catalog, catalog.pids)

    if json_output:
        emit_ok(
            catalog=str(path), present=True,
            repos=[
                {
                    "pid": entry.pid, "name": entry.name, "root": entry.root,
                    "owner": entry.owner, "depends_on": list(entry.depends_on),
                    "publishes": list(entry.publishes), "consumes": list(entry.consumes),
                }
                for entry in catalog.entries
            ],
            order=list(order.pids),
            edges=[
                {
                    "consumer": edge.consumer, "library": edge.library,
                    "path": list(edge.path), "sentence": describe_repo_catalog_edge(edge),
                }
                for edge in order.edges
            ],
        )
        return

    print(f"Catalog: {path}")
    for entry in catalog.entries:
        print(f"{entry.pid}:")
        if entry.name:
            print(f"  name: {entry.name}")
        if entry.root:
            print(f"  root: {entry.root}")
        if entry.owner:
            print(f"  owner: {entry.owner}")
        if entry.depends_on:
            print(f"  depends_on: {', '.join(entry.depends_on)}")
        if entry.publishes:
            print(f"  publishes: {', '.join(entry.publishes)}")
        if entry.consumes:
            print(f"  consumes: {', '.join(entry.consumes)}")
    print("Order: " + " -> ".join(order.pids))
    for edge in order.edges:
        print(f"  {describe_repo_catalog_edge(edge)}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "project.catalog-check": lambda args: _cmd_catalog_check(
        catalog_arg=getattr(args, "catalog", None), json_output=getattr(args, "json", False)),
    "project.catalog-show": lambda args: _cmd_catalog_show(
        catalog_arg=getattr(args, "catalog", None), json_output=getattr(args, "json", False)),
}

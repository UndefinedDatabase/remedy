"""F082 T001 — the frozen bench order set, and the freeze that binds each order's
version to its bytes.

The gauntlet's freeze (``gauntlet_orders.load_order_set``) compares an order
file's digest against the single digest the manifest records for it, so editing
an order DOES fail — but recomputing that one digest passes with no version bump
anywhere. F082's acceptance is stronger: "changing an order file without bumping
its version fails validation". DECISION F082 D2 settles how. Each order file
carries its own ``bench_order_version``, and the manifest records, per order, a
``digests`` map from version string to the sha256 of the bytes published under
that version. Validation demands that the file's CURRENT digest equal
``digests[str(version)]`` for the version the file still claims, so an unbumped
edit cannot pass; bumping means adding a new entry, which is a deliberate act
and leaves the previous pair in place as the series' own history.

The freeze's honest limit, stated here because a reader will look for it:
editing an order file alone fails, but editing it AND rewriting the digest
already recorded for the version it claims passes. Nothing inside an exported
evidence bundle can refuse that — the manifest is the ONLY record of what
version 1's bytes were, so a rewritten manifest leaves nothing to compare
against, and D2 rejected deriving the version from git history precisely
because validation must hold where no history exists. What the freeze buys is
that the edit can no longer be silent: it takes two coordinated changes in two
files, and the discarded pair is missing from the series.

ADDITIVE by construction (F082 inventory Q11): every symbol this module needs
from the gauntlet is IMPORTED, none is moved. ``load_order`` does the whole
order-file schema check — kinds, budgets, milestones — so bench order files
carry ``gauntlet_order_version`` too and reuse it verbatim.

Not reused, and why: ``gauntlet_orders.load_manifest`` and ``::load_order_set``
cannot serve a second set. They hard-require ``gauntlet_order_set_version`` to
equal the gauntlet's constant, exactly ``GAUNTLET_ORDER_COUNT`` (ten) entries,
a ``template_digest`` and a ``set_hash`` — none of which describes the bench
set. The alternative was to parameterise them, which edits a module seven test
files import by name. So the manifest reading is written here and the per-file
reading is imported.

Nothing here executes an order. This module reads, verifies, and refuses.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.gauntlet_orders import (
    MANIFEST_FILENAME,
    GauntletOrder,
    OrderSetError,
    file_sha256,
    load_order,
)

#: Bench-set version, bumped by a human when the set itself deliberately changes
#: (an order added or removed). Per-ORDER versions are independent of it: an
#: order's series is its own, which is the comparability honesty F082 asks for.
BENCH_ORDER_SET_VERSION = 1


def default_bench_orders_dir(repo_root: Path | None = None) -> Path:
    """Where the frozen bench set lives. One spelling, so nothing loads a copy."""
    root = repo_root or Path(__file__).resolve().parents[2]
    return root / "scripts" / "bench_orders"


class BenchOrderSetError(RuntimeError):
    """The frozen bench set does not match its manifest, or an order is malformed.

    Raised rather than reported softly: a bench run against a set that is not
    the set the manifest describes measures neither, and its numbers would join
    a history that claims to be comparable.
    """


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise BenchOrderSetError(message)


@dataclass(frozen=True)
class BenchOrder:
    """One bench order: the gauntlet's order shape plus the version it claims.

    ``order`` is a real :class:`GauntletOrder` rather than a copy of its fields
    — the runner seam takes that type, so the bench hands over what it already
    validated instead of a parallel structure that could drift from it.
    """

    order: GauntletOrder
    version: int

    @property
    def id(self) -> str:
        return self.order.id

    @property
    def file_name(self) -> str:
        return self.order.file_name

    @property
    def sha256(self) -> str:
        return self.order.sha256


def load_bench_order(path: Path) -> BenchOrder:
    """Read and validate one bench order file, schema first, then its version tag."""
    try:
        order = load_order(path)
    except OrderSetError as exc:
        # Re-raised under the bench's own error so a caller catches ONE type.
        # The message already names the file, so it is carried through as is.
        raise BenchOrderSetError(str(exc)) from exc

    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise BenchOrderSetError(f"{path.name}: unreadable ({exc})") from exc

    version = body.get("bench_order_version")
    _require(isinstance(version, int) and not isinstance(version, bool) and version >= 1,
             f"{path.name}: bench_order_version must be a positive integer, "
             f"found {version!r}")
    return BenchOrder(order=order, version=int(version))


def load_bench_manifest(orders_dir: Path | None = None) -> dict[str, Any]:
    """The bench manifest, validated as a manifest — not yet against the files."""
    directory = orders_dir or default_bench_orders_dir()
    path = directory / MANIFEST_FILENAME
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise BenchOrderSetError(f"{MANIFEST_FILENAME}: unreadable ({exc})") from exc
    _require(isinstance(body, dict), f"{MANIFEST_FILENAME}: not a JSON object")
    _require(body.get("bench_order_set_version") == BENCH_ORDER_SET_VERSION,
             f"{MANIFEST_FILENAME}: unsupported bench_order_set_version "
             f"{body.get('bench_order_set_version')!r}")
    entries = body.get("orders")
    _require(isinstance(entries, list) and entries,
             f"{MANIFEST_FILENAME}: orders must be a non-empty list")
    return body


def load_bench_order_set(orders_dir: Path | None = None) -> tuple[BenchOrder, ...]:
    """The bench set in manifest order, with every freeze check applied.

    Raises :class:`BenchOrderSetError` on the FIRST thing that does not hold: a
    manifest entry whose file is missing, a file on disk the manifest omits, an
    id that repeats, a version the manifest and the file disagree about, a
    version absent from its own ``digests`` map, or a digest that moved without
    the version moving with it.
    """
    directory = orders_dir or default_bench_orders_dir()
    manifest = load_bench_manifest(directory)
    entries: list[dict[str, Any]] = manifest["orders"]

    listed = [str(entry.get("file", "")) for entry in entries]
    for name in listed:
        _require((directory / name).is_file(),
                 f"{MANIFEST_FILENAME}: lists {name!r}, which is not on disk")
    on_disk = sorted(p.name for p in directory.glob("*.json")
                     if p.name != MANIFEST_FILENAME)
    unlisted = sorted(set(on_disk) - set(listed))
    _require(not unlisted,
             f"{MANIFEST_FILENAME}: order files on disk the manifest does not "
             f"list: {unlisted}")

    orders: list[BenchOrder] = []
    for entry in entries:
        name = str(entry.get("file", ""))
        bench_order = load_bench_order(directory / name)
        _require(bench_order.id == str(entry.get("id", "")),
                 f"{name}: id {bench_order.id!r} does not match the manifest "
                 f"({entry.get('id')!r})")

        declared_version = entry.get("version")
        _require(declared_version == bench_order.version,
                 f"{name}: the file claims bench_order_version "
                 f"{bench_order.version}, the manifest records "
                 f"{declared_version!r} — bump both or neither")

        digests = entry.get("digests")
        _require(isinstance(digests, dict) and digests,
                 f"{name}: the manifest records no digests map")
        key = str(bench_order.version)
        _require(key in digests,
                 f"{name}: version {key} has no digest recorded — a new version "
                 f"publishes new bytes, so it needs its own entry")

        actual = file_sha256(directory / name)
        _require(actual == str(digests[key]),
                 f"{name}: sha256 {actual} does not match the digest recorded "
                 f"for version {key} ({digests[key]}) — the file was edited "
                 f"without bumping its bench_order_version")
        orders.append(bench_order)

    ids = [o.id for o in orders]
    _require(len(set(ids)) == len(ids),
             f"duplicate bench order ids in the set: {ids}")
    return tuple(orders)

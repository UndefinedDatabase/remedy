"""F075 T002 — the curated ten-order set: frozen, versioned, and checkable.

Ten missions decide whether Remedy's multi-cycle defaults flip, so the ten
cannot drift while the campaign runs. Order-set edits mid-campaign are
forbidden and any change resets the gauntlet count (T1_F075.md, A9) — which is
only enforceable if "changed" is a computable fact. It is: every order file
carries a sha256 in the set manifest, and the manifest carries a set hash over
those digests. A single retouched word moves both.

The orders live in ``scripts/gauntlet_orders/`` beside the CLI that runs them,
not under the test fixture area: they are campaign INPUT, and filing real input
as test data is how it quietly becomes editable.

Each order names the risk it probes, in prose, in the file. Ten orders that all
probe the same risk are one order run ten times, and the whole value of the set
is that a reader can see at a glance why each one is there.

Nothing here executes an order. This module reads, verifies, and refuses.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: Order-file schema version, and the frozen set version. The set version is
#: bumped by a human when the ten deliberately change — which resets the count.
GAUNTLET_ORDER_VERSION = 1
#: v2 (R-0187) added a ``max_cycles`` budget to every order. v3 (R-0189) adds
#: the sample-project TEMPLATE to the freeze: the world a mission runs in
#: shapes its outcome exactly as much as the order does, so a changed template
#: is a changed set. A re-issue RESETS the campaign count (T1_F075.md A9) —
#: which costs nothing, because no attempt has ever passed.
GAUNTLET_ORDER_SET_VERSION = 3

#: How many orders a gauntlet is. Not a default: the gate is "ten flawless".
GAUNTLET_ORDER_COUNT = 10

MANIFEST_FILENAME = "manifest.json"

#: The mission kinds the set must mix (T1_F075.md, Design). A set that is ten
#: pure-code changes proves that Remedy can do one thing ten times.
KIND_PURE_CODE_CHANGE = "pure_code_change"
KIND_TEST_ADD = "test_add"
KIND_SMALL_APP_FEATURE = "small_app_feature_with_smoke"
KIND_DOC_GENERATION = "doc_generation"
KIND_TWO_MILESTONE_MISSION = "two_milestone_mission"
ORDER_KINDS: tuple[str, ...] = (
    KIND_PURE_CODE_CHANGE,
    KIND_TEST_ADD,
    KIND_SMALL_APP_FEATURE,
    KIND_DOC_GENERATION,
    KIND_TWO_MILESTONE_MISSION,
)

#: Budget keys every order must carry. A missing budget is an unbounded run,
#: and an unbounded run cannot fail a budget — so it is refused at load time.
#: ``max_cycles`` joined in set v2 (R-0187): a mission whose jobs are wedged at
#: one cycle can never finish, so how many cycles an order may spend is part of
#: what the order says, not a global default.
BUDGET_KEYS: tuple[str, ...] = ("max_iterations", "max_tokens",
                                "max_wall_seconds", "max_cycles")


def default_orders_dir(repo_root: Path | None = None) -> Path:
    """Where the frozen set lives. One spelling, so nothing loads a copy."""
    root = repo_root or Path(__file__).resolve().parents[2]
    return root / "scripts" / "gauntlet_orders"


def default_template_dir(repo_root: Path | None = None) -> Path:
    """The sample project a gauntlet mission is given to work on."""
    root = repo_root or Path(__file__).resolve().parents[2]
    return root / "scripts" / "gauntlet_sample_project"


#: Directories never copied into a run's workspace and never digested: build
#: droppings, not the project.
TEMPLATE_IGNORED_DIRS = frozenset({"__pycache__", ".pytest_cache", ".git"})


def template_tree_digest(template_dir: Path | None = None) -> str:
    """One digest over the template: sorted relative paths and their contents.

    Paths are part of it, so a file that MOVES changes the digest as surely as
    a file that changes — the same rule the runner's data-root hash uses.
    """
    directory = template_dir or default_template_dir()
    running = hashlib.sha256()
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        if TEMPLATE_IGNORED_DIRS & set(path.relative_to(directory).parts):
            continue
        running.update(str(path.relative_to(directory)).encode("utf-8"))
        running.update(b"\0")
        running.update(hashlib.sha256(path.read_bytes()).digest())
        running.update(b"\0")
    return running.hexdigest()


@dataclass(frozen=True)
class GauntletOrder:
    """One curated mission order, as written in its file."""

    id: str
    kind: str
    title: str
    rationale: str
    risk_probed: str
    goal: str
    milestones: tuple[dict[str, Any], ...]
    budget: dict[str, int]
    injections: tuple[str, ...]
    file_name: str
    sha256: str

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id, "kind": self.kind, "title": self.title,
            "risk_probed": self.risk_probed, "file": self.file_name,
            "sha256": self.sha256, "budget": dict(self.budget),
            "injections": list(self.injections),
        }


class OrderSetError(RuntimeError):
    """The frozen set does not match its manifest, or an order is malformed.

    Raised rather than reported as a soft finding: running a campaign against a
    set that is not the set the manifest describes proves nothing about either.
    """


def file_sha256(path: Path) -> str:
    """The digest of an order file, over its exact bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compute_set_hash(entries: list[dict[str, Any]], *,
                     template_digest: str = "") -> str:
    """The set hash: one digest over ``<sha256>  <file>`` lines plus the template.

    Order-sensitive on purpose — reordering the ten changes which order is
    ``--only 3``, so it is a change to the set. The template digest is folded
    in (v3) because the world the missions run in decides their outcomes too.
    """
    payload = "".join(f"{e.get('sha256', '')}  {e.get('file', '')}\n" for e in entries)
    if template_digest:
        payload += f"{template_digest}  <template>\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise OrderSetError(message)


def load_order(path: Path) -> GauntletOrder:
    """Read and validate one order file. A malformed order is never half-loaded."""
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise OrderSetError(f"{path.name}: unreadable ({exc})") from exc
    _require(isinstance(body, dict), f"{path.name}: not a JSON object")

    version = body.get("gauntlet_order_version")
    _require(version == GAUNTLET_ORDER_VERSION,
             f"{path.name}: unsupported gauntlet_order_version {version!r}")

    for field in ("id", "kind", "title", "rationale", "risk_probed", "goal"):
        value = body.get(field)
        _require(isinstance(value, str) and value.strip(),
                 f"{path.name}: missing or blank {field}")
    _require(body["kind"] in ORDER_KINDS,
             f"{path.name}: unknown kind {body['kind']!r}")

    milestones = body.get("milestones")
    _require(isinstance(milestones, list) and milestones,
             f"{path.name}: at least one milestone is required")

    budget = body.get("budget")
    _require(isinstance(budget, dict), f"{path.name}: missing budget")
    for key in BUDGET_KEYS:
        value = budget.get(key)
        _require(isinstance(value, int) and not isinstance(value, bool) and value > 0,
                 f"{path.name}: budget.{key} must be a positive integer")

    injections = body.get("injections", [])
    _require(isinstance(injections, list),
             f"{path.name}: injections must be a list")

    return GauntletOrder(
        id=body["id"],
        kind=body["kind"],
        title=body["title"],
        rationale=body["rationale"],
        risk_probed=body["risk_probed"],
        goal=body["goal"],
        milestones=tuple(m for m in milestones if isinstance(m, dict)),
        budget={key: int(budget[key]) for key in BUDGET_KEYS},
        injections=tuple(str(i) for i in injections),
        file_name=path.name,
        sha256=file_sha256(path),
    )


def load_manifest(orders_dir: Path | None = None) -> dict[str, Any]:
    """The set manifest, validated as a manifest — not yet against the files."""
    directory = orders_dir or default_orders_dir()
    path = directory / MANIFEST_FILENAME
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise OrderSetError(f"{MANIFEST_FILENAME}: unreadable ({exc})") from exc
    _require(isinstance(body, dict), f"{MANIFEST_FILENAME}: not a JSON object")
    _require(body.get("gauntlet_order_set_version") == GAUNTLET_ORDER_SET_VERSION,
             f"{MANIFEST_FILENAME}: unsupported set version "
             f"{body.get('gauntlet_order_set_version')!r}")
    entries = body.get("orders")
    _require(isinstance(entries, list), f"{MANIFEST_FILENAME}: orders must be a list")
    _require(len(entries) == GAUNTLET_ORDER_COUNT,
             f"{MANIFEST_FILENAME}: a gauntlet is {GAUNTLET_ORDER_COUNT} orders, "
             f"found {len(entries)}")
    return body


def load_order_set(orders_dir: Path | None = None,
                   template_dir: Path | None = None) -> tuple[GauntletOrder, ...]:
    """The ten orders in manifest order, with every freeze check applied.

    Raises :class:`OrderSetError` on the first thing that does not hold: a
    digest that moved, an id that repeats, a file the manifest does not list.
    """
    directory = orders_dir or default_orders_dir()
    manifest = load_manifest(directory)
    entries: list[dict[str, Any]] = manifest["orders"]

    listed = [str(e.get("file", "")) for e in entries]
    on_disk = sorted(p.name for p in directory.glob("*.json")
                     if p.name != MANIFEST_FILENAME)
    _require(sorted(listed) == on_disk,
             f"{MANIFEST_FILENAME}: listed orders {sorted(listed)} do not match "
             f"the files on disk {on_disk}")

    orders: list[GauntletOrder] = []
    for entry in entries:
        order = load_order(directory / str(entry.get("file", "")))
        _require(order.sha256 == str(entry.get("sha256", "")),
                 f"{order.file_name}: sha256 {order.sha256} does not match the "
                 f"manifest ({entry.get('sha256')}) — the frozen set was edited")
        _require(order.id == str(entry.get("id", "")),
                 f"{order.file_name}: id {order.id!r} does not match the manifest")
        orders.append(order)

    ids = [o.id for o in orders]
    _require(len(set(ids)) == len(ids), f"duplicate order ids in the set: {ids}")

    # v3: the template is frozen with the orders. A retouched sample file is a
    # changed campaign, and the loader says so before a single token is spent.
    declared = str(manifest.get("template_digest", ""))
    _require(bool(declared), f"{MANIFEST_FILENAME}: no template_digest recorded")
    actual = template_tree_digest(template_dir)
    _require(declared == actual,
             f"the sample-project template was edited: digest {actual} does not "
             f"match the manifest ({declared})")

    expected = compute_set_hash(entries, template_digest=declared)
    _require(str(manifest.get("set_hash", "")) == expected,
             f"{MANIFEST_FILENAME}: set_hash {manifest.get('set_hash')} does not "
             f"match the listed digests ({expected}) — the manifest was edited")
    return tuple(orders)

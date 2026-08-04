"""F075 T002 — the frozen ten, pinned.

Order-set edits mid-campaign are forbidden and any change resets the gauntlet
count (T1_F075.md, A9). That rule is only enforceable if "changed" is a
computable fact, so these tests are the enforcement: the real set on disk must
be exactly ten orders, with unique ids, a budget on every one, digests that
match the manifest, a set hash that matches the digests, and the kind mix the
feature file asks for.

The tampering tests work on a COPY: they prove the loader refuses an edited
set, which is the only way to know the freeze is real rather than decorative.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from packages.orchestration.gauntlet_evaluator import INJECTION_CLASSES
from packages.orchestration.gauntlet_orders import (
    BUDGET_KEYS,
    GAUNTLET_ORDER_COUNT,
    GAUNTLET_ORDER_SET_VERSION,
    GAUNTLET_ORDER_VERSION,
    MANIFEST_FILENAME,
    ORDER_KINDS,
    OrderSetError,
    compute_set_hash,
    default_orders_dir,
    file_sha256,
    load_manifest,
    load_order,
    load_order_set,
)

ORDERS_DIR = default_orders_dir()


# ---------------------------------------------------------------------------
# The real set on disk
# ---------------------------------------------------------------------------

def test_the_set_is_exactly_ten_orders() -> None:
    assert len(load_order_set()) == GAUNTLET_ORDER_COUNT


def test_every_order_id_is_unique() -> None:
    ids = [o.id for o in load_order_set()]
    assert len(set(ids)) == GAUNTLET_ORDER_COUNT
    assert ids == sorted(ids), "manifest order matches id order, so --only N is stable"


def test_every_order_carries_a_positive_budget() -> None:
    for order in load_order_set():
        assert set(order.budget) == set(BUDGET_KEYS), order.id
        assert all(order.budget[key] > 0 for key in BUDGET_KEYS), order.id


def test_the_kind_mix_the_feature_file_asks_for_is_present() -> None:
    kinds = {o.kind for o in load_order_set()}
    assert kinds == set(ORDER_KINDS)


def test_every_order_states_a_distinct_risk_in_prose() -> None:
    """Ten orders probing the same risk are one order run ten times."""
    orders = load_order_set()
    assert len({o.risk_probed for o in orders}) == GAUNTLET_ORDER_COUNT
    assert len({o.rationale for o in orders}) == GAUNTLET_ORDER_COUNT
    for order in orders:
        assert len(order.rationale) > 120, f"{order.id}: rationale is not an argument"


def test_every_harness_failure_injection_class_is_exercised_by_the_set() -> None:
    injected = {name for o in load_order_set() for name in o.injections}
    assert injected == set(INJECTION_CLASSES)


def test_every_order_has_at_least_one_milestone_with_a_dod() -> None:
    for order in load_order_set():
        assert order.milestones, order.id
        for milestone in order.milestones:
            assert milestone.get("dod"), f"{order.id}: {milestone.get('id')} has no DoD"


def test_the_two_milestone_orders_really_have_two() -> None:
    for order in load_order_set():
        if order.kind == "two_milestone_mission":
            assert len(order.milestones) == 2, order.id


def test_the_manifest_digests_match_the_files_on_disk() -> None:
    manifest = load_manifest()
    for entry in manifest["orders"]:
        path = ORDERS_DIR / entry["file"]
        assert file_sha256(path) == entry["sha256"], entry["file"]


def test_the_set_hash_matches_the_listed_digests() -> None:
    manifest = load_manifest()
    assert manifest["set_hash"] == compute_set_hash(manifest["orders"])


def test_the_set_is_frozen_at_version_one() -> None:
    assert load_manifest()["gauntlet_order_set_version"] == GAUNTLET_ORDER_SET_VERSION
    for order in load_order_set():
        body = json.loads((ORDERS_DIR / order.file_name).read_text(encoding="utf-8"))
        assert body["gauntlet_order_version"] == GAUNTLET_ORDER_VERSION


def test_no_stray_json_file_hides_beside_the_set() -> None:
    listed = {e["file"] for e in load_manifest()["orders"]} | {MANIFEST_FILENAME}
    assert {p.name for p in ORDERS_DIR.glob("*.json")} == listed


# ---------------------------------------------------------------------------
# The freeze, proven by tampering with a copy
# ---------------------------------------------------------------------------

@pytest.fixture()
def set_copy(tmp_path: Path) -> Path:
    target = tmp_path / "gauntlet_orders"
    shutil.copytree(ORDERS_DIR, target)
    assert len(load_order_set(target)) == GAUNTLET_ORDER_COUNT
    return target


def rewrite(path: Path, mutate) -> None:
    body = json.loads(path.read_text(encoding="utf-8"))
    mutate(body)
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_editing_one_order_breaks_the_manifest(set_copy: Path) -> None:
    first = load_manifest(set_copy)["orders"][0]["file"]
    rewrite(set_copy / first, lambda b: b.update(title=b["title"] + "."))
    with pytest.raises(OrderSetError, match="the frozen set was edited"):
        load_order_set(set_copy)


def test_editing_the_manifest_to_match_breaks_the_set_hash(set_copy: Path) -> None:
    """The obvious way around the digest check, closed by the set hash."""
    entry_file = load_manifest(set_copy)["orders"][0]["file"]
    rewrite(set_copy / entry_file, lambda b: b.update(title=b["title"] + "."))
    manifest_path = set_copy / MANIFEST_FILENAME

    def fix_digest(body: dict) -> None:
        body["orders"][0]["sha256"] = file_sha256(set_copy / entry_file)

    rewrite(manifest_path, fix_digest)
    with pytest.raises(OrderSetError, match="the manifest was edited"):
        load_order_set(set_copy)


def test_reordering_the_set_changes_the_set_hash(set_copy: Path) -> None:
    """--only 3 must mean the same order tomorrow."""
    manifest = load_manifest(set_copy)
    reordered = list(reversed(manifest["orders"]))
    assert compute_set_hash(reordered) != manifest["set_hash"]


def test_removing_an_order_is_refused(set_copy: Path) -> None:
    victim = load_manifest(set_copy)["orders"][0]["file"]
    (set_copy / victim).unlink()
    with pytest.raises(OrderSetError, match="do not match the files on disk"):
        load_order_set(set_copy)


def test_adding_an_unlisted_order_is_refused(set_copy: Path) -> None:
    shutil.copy(set_copy / load_manifest(set_copy)["orders"][0]["file"],
                set_copy / "g11-sneaked-in.json")
    with pytest.raises(OrderSetError, match="do not match the files on disk"):
        load_order_set(set_copy)


def test_a_duplicate_id_is_refused(set_copy: Path) -> None:
    manifest = load_manifest(set_copy)
    first, second = manifest["orders"][0]["file"], manifest["orders"][1]["file"]
    rewrite(set_copy / second, lambda b: b.update(
        id=json.loads((set_copy / first).read_text(encoding="utf-8"))["id"]))

    def resync(body: dict) -> None:
        body["orders"][1]["sha256"] = file_sha256(set_copy / second)
        body["orders"][1]["id"] = body["orders"][0]["id"]
        body["set_hash"] = compute_set_hash(body["orders"])

    rewrite(set_copy / MANIFEST_FILENAME, resync)
    with pytest.raises(OrderSetError, match="duplicate order ids"):
        load_order_set(set_copy)


def test_a_nine_order_manifest_is_not_a_gauntlet(set_copy: Path) -> None:
    def drop(body: dict) -> None:
        body["orders"] = body["orders"][:-1]
        body["set_hash"] = compute_set_hash(body["orders"])

    rewrite(set_copy / MANIFEST_FILENAME, drop)
    with pytest.raises(OrderSetError, match="a gauntlet is 10 orders"):
        load_order_set(set_copy)


def test_an_unknown_set_version_is_refused(set_copy: Path) -> None:
    rewrite(set_copy / MANIFEST_FILENAME,
            lambda b: b.update(gauntlet_order_set_version=2))
    with pytest.raises(OrderSetError, match="unsupported set version"):
        load_manifest(set_copy)


@pytest.mark.parametrize("field", ["id", "kind", "title", "rationale",
                                   "risk_probed", "goal"])
def test_a_blank_required_field_is_refused(set_copy: Path, field: str) -> None:
    path = set_copy / load_manifest(set_copy)["orders"][0]["file"]
    rewrite(path, lambda b: b.update({field: "  "}))
    with pytest.raises(OrderSetError, match=f"missing or blank {field}"):
        load_order(path)


def test_an_unknown_kind_is_refused(set_copy: Path) -> None:
    path = set_copy / load_manifest(set_copy)["orders"][0]["file"]
    rewrite(path, lambda b: b.update(kind="vibes"))
    with pytest.raises(OrderSetError, match="unknown kind"):
        load_order(path)


@pytest.mark.parametrize("bad", [0, -1, "many", True, None])
def test_a_missing_or_non_positive_budget_is_refused(set_copy: Path, bad) -> None:
    path = set_copy / load_manifest(set_copy)["orders"][0]["file"]
    rewrite(path, lambda b: b["budget"].update(max_tokens=bad))
    with pytest.raises(OrderSetError, match="budget.max_tokens"):
        load_order(path)


def test_an_order_without_milestones_is_refused(set_copy: Path) -> None:
    path = set_copy / load_manifest(set_copy)["orders"][0]["file"]
    rewrite(path, lambda b: b.update(milestones=[]))
    with pytest.raises(OrderSetError, match="at least one milestone"):
        load_order(path)


def test_an_unreadable_order_is_refused(set_copy: Path) -> None:
    path = set_copy / load_manifest(set_copy)["orders"][0]["file"]
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(OrderSetError, match="unreadable"):
        load_order(path)

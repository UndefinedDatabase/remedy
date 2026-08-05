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
    GauntletOrder,
    OrderSetError,
    compute_set_hash,
    default_orders_dir,
    default_template_dir,
    file_sha256,
    load_manifest,
    load_order,
    load_order_set,
    template_tree_digest,
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


def test_the_set_hash_matches_the_listed_digests_and_the_template() -> None:
    manifest = load_manifest()
    assert manifest["set_hash"] == compute_set_hash(
        manifest["orders"], template_digest=manifest["template_digest"])


def test_the_set_is_frozen_at_the_declared_set_version() -> None:
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
    """The literal used to be 2, which set v2 (R-0187) turned into the REAL
    version. The assertion is unchanged; the example had to become a version
    that is genuinely unknown."""
    rewrite(set_copy / MANIFEST_FILENAME,
            lambda b: b.update(
                gauntlet_order_set_version=GAUNTLET_ORDER_SET_VERSION + 1))
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


# ---------------------------------------------------------------------------
# Set v2 (R-0187): every order says how many cycles it may spend
# ---------------------------------------------------------------------------

def test_the_set_is_at_version_four() -> None:
    assert GAUNTLET_ORDER_SET_VERSION == 4
    assert load_manifest()["gauntlet_order_set_version"] == 4


def test_every_order_carries_a_positive_cycle_budget() -> None:
    assert "max_cycles" in BUDGET_KEYS
    for order in load_order_set():
        assert order.budget["max_cycles"] > 0, order.id


def test_the_cycle_budgets_are_chosen_per_order_not_copied() -> None:
    """A doc order and a two-milestone mission needing the same number of
    cycles would mean nobody thought about either."""
    by_kind: dict[str, list[int]] = {}
    for order in load_order_set():
        by_kind.setdefault(order.kind, []).append(order.budget["max_cycles"])
    assert min(by_kind["two_milestone_mission"]) > max(by_kind["doc_generation"]), \
        "two milestones of real work need more cycles than prose"
    assert len({c for cs in by_kind.values() for c in cs}) > 1


# ---------------------------------------------------------------------------
# Set v3 (R-0189): the sample-project template is frozen with the orders
# ---------------------------------------------------------------------------

def test_the_manifest_records_the_template_digest() -> None:
    assert load_manifest()["template_digest"] == template_tree_digest()


def test_the_template_suite_is_green_and_self_sufficient() -> None:
    """The world a mission is given must start from a passing suite — a
    template whose tests already fail would make every DoD meaningless."""
    import subprocess
    import sys

    proc = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q"],
                          cwd=str(default_template_dir()),
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout[-2000:]


def test_the_template_holds_what_the_orders_name() -> None:
    """The goal-vs-template audit, pinned: an order about a hard-coded backoff
    cap is meaningless unless the cap is really there."""
    root = default_template_dir()
    source = (root / "sampleproj" / "retry.py").read_text(encoding="utf-8")
    assert "BACKOFF_CAP_SECONDS" in source
    config = (root / "sampleproj" / "config.py").read_text(encoding="utf-8")
    assert "ENV_VARS" in config and "explicit" in config
    parsing = (root / "sampleproj" / "parsing.py").read_text(encoding="utf-8")
    assert "return None" in parsing
    # g05: the duplication really is duplicated.
    marker = "path normalisation (duplicated in"
    assert marker in (root / "sampleproj" / "importer.py").read_text(encoding="utf-8")
    assert marker in (root / "sampleproj" / "report.py").read_text(encoding="utf-8")
    assert (root / "CHANGELOG.md").is_file() and (root / "README.md").is_file()


def test_editing_a_template_file_is_refused(tmp_path: Path, set_copy: Path) -> None:
    """Tampering with the world is tampering with the campaign."""
    template = tmp_path / "template"
    shutil.copytree(default_template_dir(), template)
    (template / "README.md").write_text("edited\n", encoding="utf-8")
    with pytest.raises(OrderSetError, match="template was edited"):
        load_order_set(set_copy, template)


def test_a_manifest_without_a_template_digest_is_refused(set_copy: Path) -> None:
    rewrite(set_copy / MANIFEST_FILENAME, lambda b: b.pop("template_digest"))
    with pytest.raises(OrderSetError, match="no template_digest recorded"):
        load_order_set(set_copy)


# ---------------------------------------------------------------------------
# Set v4 (R-0194): budgets sized from measured economics, not from a guess
# ---------------------------------------------------------------------------

#: What R9's live run measured. The compiler expanded a ONE-milestone goal into
#: THREE plan milestones; a milestone cost three iterations (dispatch, the
#: R-0191 refusal, the declare) and the mission needed one more to be declared
#: achieved. R-0193 makes the direct path two, so this floor is the pessimistic
#: figure: a run that ignores the directive still fits.
MEASURED_EXPANSION = 3
MEASURED_ITERATIONS_PER_MILESTONE = 3


def measured_floor(order: GauntletOrder) -> int:
    return (MEASURED_EXPANSION * MEASURED_ITERATIONS_PER_MILESTONE
            * len(order.milestones)) + 1


def test_every_order_says_why_its_budget_is_that_size() -> None:
    """A budget without a stated reason is the guess v4 exists to replace."""
    for order in load_order_set():
        body = json.loads(
            (ORDERS_DIR / order.file_name).read_text(encoding="utf-8"))
        assert body.get("budget_rationale", "").strip(), order.id


def test_every_iteration_budget_fits_the_measured_plan_shape() -> None:
    for order in load_order_set():
        assert order.budget["max_iterations"] >= measured_floor(order), order.id


def test_the_budgets_carry_margin_but_not_slack() -> None:
    """The gate still measures economy: a budget nothing can fail is not one."""
    for order in load_order_set():
        assert order.budget["max_iterations"] <= measured_floor(order) + 5, \
            order.id


def test_the_two_milestone_orders_are_budgeted_above_the_rest() -> None:
    two = [o.budget["max_iterations"] for o in load_order_set()
           if o.kind == "two_milestone_mission"]
    rest = [o.budget["max_iterations"] for o in load_order_set()
            if o.kind != "two_milestone_mission"]
    assert two and rest and min(two) > max(rest)


def test_the_cycle_budgets_did_not_move_with_the_iteration_budgets() -> None:
    """v4 re-sizes what R9 measured wrong. Cycles were measured RIGHT (jobs
    reached all_green at cycles=4), so touching them would be an edit without
    evidence."""
    cycles = {o.id: o.budget["max_cycles"] for o in load_order_set()}
    assert cycles == {
        "g01-pure-code-change": 4, "g02-test-add": 4,
        "g03-small-app-feature-smoke": 5, "g04-doc-generation": 3,
        "g05-two-milestone-mission": 8,
        "g06-provider-api-error-mid-move": 4,
        "g07-truncated-model-response": 4,
        "g08-harness-death-mid-dispatch": 5,
        "g09-harness-death-mid-write": 8, "g10-escalate-then-finish": 3,
    }

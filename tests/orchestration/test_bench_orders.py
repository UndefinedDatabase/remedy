"""F082 T001 — the frozen bench order set and the version freeze over it.

Every negative case is built in a tmp COPY of ``scripts/bench_orders``. A test
that mutated the real directory would leave the frozen set edited on disk, which
is precisely the failure this module exists to detect.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from packages.orchestration.bench_orders import (
    BENCH_ORDER_SET_VERSION,
    BenchOrderSetError,
    default_bench_orders_dir,
    load_bench_order_set,
)
from packages.orchestration.gauntlet_orders import BUDGET_KEYS, ORDER_KINDS

#: The ids the bench set is frozen at. Three, not five: F082's inventory S3
#: found the API-endpoint and frontend-widget capabilities inexpressible against
#: the sample project, and an order that cannot run would be frozen forever.
EXPECTED_BENCH_ORDER_IDS = (
    "b01-cli-report-width",
    "b02-config-lookup-bugfix",
    "b03-cli-render-refactor",
)


@pytest.fixture()
def bench_copy(tmp_path: Path) -> Path:
    """A writable copy of the frozen set, so no test can touch the real one."""
    target = tmp_path / "bench_orders"
    shutil.copytree(default_bench_orders_dir(), target)
    return target


def _read_manifest(directory: Path) -> dict:
    return json.loads((directory / "manifest.json").read_text(encoding="utf-8"))


def _write_manifest(directory: Path, body: dict) -> None:
    (directory / "manifest.json").write_text(
        json.dumps(body, indent=2) + "\n", encoding="utf-8")


def _entry(body: dict, order_id: str) -> dict:
    return next(e for e in body["orders"] if e["id"] == order_id)


def test_the_frozen_set_loads_and_every_order_validates():
    orders = load_bench_order_set()
    assert tuple(o.id for o in orders) == EXPECTED_BENCH_ORDER_IDS
    for order in orders:
        assert order.version >= 1
        assert order.order.kind in ORDER_KINDS
        assert set(order.order.budget) == set(BUDGET_KEYS)
        assert order.order.milestones
        assert order.order.goal.strip()
        assert order.order.rationale.strip()
        assert order.order.risk_probed.strip()


def test_the_copy_loads_exactly_as_the_real_set_does(bench_copy: Path):
    assert [o.id for o in load_bench_order_set(bench_copy)] == \
        [o.id for o in load_bench_order_set()]


def test_editing_an_order_without_bumping_its_version_fails_validation(bench_copy: Path):
    """F082's acceptance criterion: an unbumped edit must not pass."""
    path = bench_copy / "b01-cli-report-width.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body["goal"] = body["goal"] + " Also rename the module."
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(BenchOrderSetError, match="without bumping its bench_order_version"):
        load_bench_order_set(bench_copy)


def test_bumping_the_version_and_recording_the_new_digest_passes(bench_copy: Path):
    path = bench_copy / "b01-cli-report-width.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body["goal"] = body["goal"] + " Also rename the module."
    body["bench_order_version"] = 2
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    manifest = _read_manifest(bench_copy)
    entry = _entry(manifest, "b01-cli-report-width")
    entry["version"] = 2
    entry["digests"]["2"] = hashlib.sha256(path.read_bytes()).hexdigest()
    _write_manifest(bench_copy, manifest)

    orders = load_bench_order_set(bench_copy)
    assert next(o for o in orders if o.id == "b01-cli-report-width").version == 2
    # The previous pair survives: the series' own history is not overwritten.
    assert "1" in _entry(_read_manifest(bench_copy), "b01-cli-report-width")["digests"]


def test_bumping_the_version_without_recording_a_digest_fails(bench_copy: Path):
    path = bench_copy / "b02-config-lookup-bugfix.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body["bench_order_version"] = 2
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = _read_manifest(bench_copy)
    _entry(manifest, "b02-config-lookup-bugfix")["version"] = 2
    _write_manifest(bench_copy, manifest)

    with pytest.raises(BenchOrderSetError, match="has no digest recorded"):
        load_bench_order_set(bench_copy)


def test_the_file_and_the_manifest_must_claim_the_same_version(bench_copy: Path):
    """A file-side bump alone is not a bump: the manifest has to say so too."""
    path = bench_copy / "b03-cli-render-refactor.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body["bench_order_version"] = 2
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = _read_manifest(bench_copy)
    entry = _entry(manifest, "b03-cli-render-refactor")
    entry["digests"]["2"] = hashlib.sha256(path.read_bytes()).hexdigest()
    _write_manifest(bench_copy, manifest)

    with pytest.raises(BenchOrderSetError, match="bump both or neither"):
        load_bench_order_set(bench_copy)


def test_a_manifest_side_digest_rewrite_is_outside_what_the_freeze_can_see(bench_copy: Path):
    """The freeze's honest limit, pinned so nobody reads more into it (D2).

    Editing the ORDER FILE alone fails, which is F082's acceptance criterion.
    Editing the file AND rewriting the digest already recorded for version 1
    passes, and no check inside an evidence bundle could refuse it: the manifest
    is the only record of what version 1's bytes were, so rewriting it leaves
    nothing to compare against. DECISION F082 D2 rejected deriving the version
    from git history precisely because validation must hold where no history
    exists. This test states the residual rather than letting a reader assume it
    away.
    """
    path = bench_copy / "b03-cli-render-refactor.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body["goal"] = "Do something else entirely."
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = _read_manifest(bench_copy)
    _entry(manifest, "b03-cli-render-refactor")["digests"]["1"] = \
        hashlib.sha256(path.read_bytes()).hexdigest()
    _write_manifest(bench_copy, manifest)

    orders = load_bench_order_set(bench_copy)
    assert next(o for o in orders if o.id == "b03-cli-render-refactor").version == 1


def test_a_duplicate_id_fails(bench_copy: Path):
    path = bench_copy / "b02-config-lookup-bugfix.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body["id"] = "b01-cli-report-width"
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = _read_manifest(bench_copy)
    entry = _entry(manifest, "b02-config-lookup-bugfix")
    entry["id"] = "b01-cli-report-width"
    entry["digests"]["1"] = hashlib.sha256(path.read_bytes()).hexdigest()
    _write_manifest(bench_copy, manifest)

    with pytest.raises(BenchOrderSetError, match="duplicate bench order ids"):
        load_bench_order_set(bench_copy)


def test_a_manifest_entry_whose_file_is_missing_fails(bench_copy: Path):
    (bench_copy / "b03-cli-render-refactor.json").unlink()

    with pytest.raises(BenchOrderSetError, match="which is not on disk"):
        load_bench_order_set(bench_copy)


def test_an_on_disk_file_the_manifest_omits_fails(bench_copy: Path):
    manifest = _read_manifest(bench_copy)
    manifest["orders"] = [e for e in manifest["orders"]
                          if e["id"] != "b03-cli-render-refactor"]
    _write_manifest(bench_copy, manifest)

    with pytest.raises(BenchOrderSetError, match="the manifest does not list"):
        load_bench_order_set(bench_copy)


def test_an_unsupported_set_version_fails(bench_copy: Path):
    manifest = _read_manifest(bench_copy)
    manifest["bench_order_set_version"] = BENCH_ORDER_SET_VERSION + 1
    _write_manifest(bench_copy, manifest)

    with pytest.raises(BenchOrderSetError, match="unsupported bench_order_set_version"):
        load_bench_order_set(bench_copy)


def test_a_malformed_order_file_fails_on_the_reused_schema_check(bench_copy: Path):
    """The schema check is ``gauntlet_orders.load_order``, imported not copied."""
    path = bench_copy / "b01-cli-report-width.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body["budget"].pop("max_cycles")
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = _read_manifest(bench_copy)
    _entry(manifest, "b01-cli-report-width")["digests"]["1"] = \
        hashlib.sha256(path.read_bytes()).hexdigest()
    _write_manifest(bench_copy, manifest)

    with pytest.raises(BenchOrderSetError, match="budget.max_cycles"):
        load_bench_order_set(bench_copy)


def test_a_non_integer_version_tag_fails(bench_copy: Path):
    path = bench_copy / "b02-config-lookup-bugfix.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body["bench_order_version"] = "1"
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = _read_manifest(bench_copy)
    _entry(manifest, "b02-config-lookup-bugfix")["digests"]["1"] = \
        hashlib.sha256(path.read_bytes()).hexdigest()
    _write_manifest(bench_copy, manifest)

    with pytest.raises(BenchOrderSetError, match="bench_order_version must be a positive integer"):
        load_bench_order_set(bench_copy)


def test_the_real_frozen_set_is_untouched_after_the_negative_cases():
    """The tmp-copy discipline, asserted rather than assumed."""
    orders = load_bench_order_set()
    assert tuple(o.id for o in orders) == EXPECTED_BENCH_ORDER_IDS
    assert all(o.version == 1 for o in orders)

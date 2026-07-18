"""F4 (round 26) — one shared bounded acquisition budget for _view_from_dir and _StagedArtifacts.
Exceeding a per-member/aggregate/count limit BLOCKS; a cached re-read does not recharge; separate
members charge separately; a refused member is never interpreted as merely absent."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_budget", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_z = importlib.util.spec_from_file_location(
    "_brz_budget", REPO_ROOT / "scripts" / "build_review_zip.py")
_brz = importlib.util.module_from_spec(_z); _z.loader.exec_module(_brz)

from packages.common.acquisition_budget import AcquisitionBudget, AcquisitionBudgetError


class TestBudgetObject:
    def test_aggregate_boundary_passes_plus_one_blocks(self):
        b = AcquisitionBudget(max_total_bytes=10, max_members=100, max_member_bytes=100)
        b.charge("a", 6)
        b.charge("b", 4)                       # total exactly 10 — at the boundary, passes
        with pytest.raises(AcquisitionBudgetError):
            b.charge("c", 1)                   # 11 > 10 — blocks

    def test_member_count_boundary_passes_plus_one_blocks(self):
        b = AcquisitionBudget(max_members=2, max_total_bytes=1000, max_member_bytes=1000)
        b.charge("a", 1)
        b.charge("b", 1)
        with pytest.raises(AcquisitionBudgetError):
            b.charge("c", 1)

    def test_per_member_limit_blocks(self):
        b = AcquisitionBudget(max_member_bytes=5, max_total_bytes=1000, max_members=100)
        with pytest.raises(AcquisitionBudgetError):
            b.charge("big", 6)

    def test_duplicate_logical_member_blocks(self):
        b = AcquisitionBudget()
        b.charge("a", 1)
        with pytest.raises(AcquisitionBudgetError):
            b.charge("a", 1)

    def test_separate_members_charge_separately(self):
        b = AcquisitionBudget(max_members=5, max_total_bytes=100, max_member_bytes=100)
        b.charge("a", 3)
        b.charge("b", 3)
        assert b.members == 2 and b.total == 6


class TestViewFromDirBudget:
    def test_over_member_count_blocks(self, tmp_path, monkeypatch):
        for i in range(4):
            (tmp_path / f"f{i}.json").write_text("{}")
        import packages.common.acquisition_budget as ab
        monkeypatch.setattr(ab, "MAX_MEMBERS", 2)
        with pytest.raises(AcquisitionBudgetError):
            _brm._view_from_dir(str(tmp_path))

    def test_within_budget_ok(self, tmp_path, monkeypatch):
        for i in range(2):
            (tmp_path / f"f{i}.json").write_text("{}")
        import packages.common.acquisition_budget as ab
        monkeypatch.setattr(ab, "MAX_MEMBERS", 2)
        v = _brm._view_from_dir(str(tmp_path))
        assert v.isfile("f0.json") and v.isfile("f1.json")


class TestStagedArtifactsBudget:
    def _stage(self, tmp_path, n):
        cur = tmp_path / "staging" / "evidence" / "current"
        cur.mkdir(parents=True)
        for i in range(n):
            (cur / f"m{i}.json").write_text('{"x": 1}')
        return str(tmp_path / "staging")

    def test_over_aggregate_blocks(self, tmp_path):
        root = self._stage(tmp_path, 3)
        budget = AcquisitionBudget(max_total_bytes=10, max_members=100, max_member_bytes=100)
        sa = _brz._StagedArtifacts(root, "evidence/current", budget=budget)
        # each member is 8 bytes; the third exceeds the 10-byte aggregate.
        sa.load("m0.json")
        with pytest.raises(_brz.ArchivePlanError):
            sa.load("m1.json")

    def test_cached_reread_does_not_recharge(self, tmp_path):
        root = self._stage(tmp_path, 1)
        budget = AcquisitionBudget(max_members=1, max_total_bytes=1000, max_member_bytes=1000)
        sa = _brz._StagedArtifacts(root, "evidence/current", budget=budget)
        raw1, _ = sa.load("m0.json")
        raw2, _ = sa.load("m0.json")           # cached — must not trip the count/duplicate limit
        assert raw1 == raw2 and budget.members == 1

    def test_over_member_count_blocks(self, tmp_path):
        root = self._stage(tmp_path, 3)
        budget = AcquisitionBudget(max_members=1, max_total_bytes=1000, max_member_bytes=1000)
        sa = _brz._StagedArtifacts(root, "evidence/current", budget=budget)
        sa.load("m0.json")
        with pytest.raises(_brz.ArchivePlanError):
            sa.load("m1.json")

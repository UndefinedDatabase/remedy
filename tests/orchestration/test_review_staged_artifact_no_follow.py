"""F6 (round 25) — staged bytes are acquired through anchored, O_NOFOLLOW secure_fs reads. A staged
member that is a symlink (or a regular file swapped to one) is refused and reported ABSENT: no
outside bytes are ever read, in either the standalone _view_from_dir walk or the coordinator's
_StagedArtifacts.load — even before the ArchivePlan blocks the member.
"""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_nf", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_z = importlib.util.spec_from_file_location(
    "_brz_nf", REPO_ROOT / "scripts" / "build_review_zip.py")
_brz = importlib.util.module_from_spec(_z); _z.loader.exec_module(_brz)

SECRET = b'{"SECRET":"outside-bytes-must-not-be-read"}'


class TestViewFromDirNoFollow:
    def test_symlinked_member_is_not_read(self, tmp_path):
        outside = tmp_path / "outside.json"
        outside.write_bytes(SECRET)
        ev = tmp_path / "ev"
        ev.mkdir()
        (ev / "real.json").write_text('{"ok": true}')
        os.symlink(outside, ev / "final_verifier_report.json")
        v = _brm._view_from_dir(str(ev))
        assert v.isfile("real.json")
        assert not v.isfile("final_verifier_report.json")
        assert all(SECRET not in data for data in v._files.values())

    def test_symlinked_subdir_is_not_traversed(self, tmp_path):
        outside_dir = tmp_path / "outside"
        outside_dir.mkdir()
        (outside_dir / "leak.json").write_bytes(SECRET)
        ev = tmp_path / "ev"
        ev.mkdir()
        (ev / "keep.json").write_text("{}")
        os.symlink(outside_dir, ev / "task_runs")
        v = _brm._view_from_dir(str(ev))
        assert v.isfile("keep.json")
        assert not v.isfile("task_runs/leak.json")
        assert all(SECRET not in data for data in v._files.values())


class TestStagedArtifactsNoFollow:
    def test_symlinked_staged_member_reads_absent(self, tmp_path):
        outside = tmp_path / "outside.json"
        outside.write_bytes(SECRET)
        staged = tmp_path / "staging"
        cur = staged / "evidence" / "current"
        cur.mkdir(parents=True)
        (cur / "real.json").write_text('{"ok": true}')
        os.symlink(outside, cur / "final_verifier_report.json")
        sa = _brz._StagedArtifacts(str(staged), "evidence/current")
        raw, sha = sa.load("final_verifier_report.json")
        assert raw is None                              # refused, reported absent
        real, _ = sa.load("real.json")
        assert real is not None
        assert SECRET not in (real or b"")

    def test_regular_swapped_to_symlink_reads_absent(self, tmp_path):
        # A member that is a symlink at read time (a regular→symlink swap) is refused.
        outside = tmp_path / "outside.json"
        outside.write_bytes(SECRET)
        staged = tmp_path / "staging"
        cur = staged / "evidence" / "current"
        cur.mkdir(parents=True)
        os.symlink(outside, cur / "change_provenance_gate.json")
        sa = _brz._StagedArtifacts(str(staged), "evidence/current")
        raw, _ = sa.load("change_provenance_gate.json")
        assert raw is None

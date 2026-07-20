"""F6 (round 24) — once the Source snapshot exists, the Root Manifest is immune to staging-filesystem
races. The manifest is built from the frozen snapshot bytes, so a gate/proof/task artifact that is
mutated, deleted, or added on disk AFTER the snapshot cannot change what the manifest reports.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_race", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)


def _seed(dirpath: Path):
    (dirpath / "fresh_evidence_gate.json").write_text('{"verdict": "PASS"}')
    (dirpath / "manifest.json").write_text('{"job_id": "j1"}')
    (dirpath / "task_runs" / "T001").mkdir(parents=True)
    (dirpath / "task_runs" / "T001" / "review.json").write_text('{"v": 1}')


class TestFrozenAgainstMutation:
    def test_mutated_gate_on_disk_does_not_change_the_view(self, tmp_path):
        _seed(tmp_path)
        ev = _brm._view_from_dir(str(tmp_path))                 # snapshot taken here
        # An attacker flips the packaged gate on disk after the snapshot.
        (tmp_path / "fresh_evidence_gate.json").write_text('{"verdict": "BLOCKED"}')
        assert ev.read_json("fresh_evidence_gate.json")["verdict"] == "PASS"

    def test_deleted_artifact_on_disk_still_present_in_view(self, tmp_path):
        _seed(tmp_path)
        ev = _brm._view_from_dir(str(tmp_path))
        (tmp_path / "manifest.json").unlink()
        assert ev.isfile("manifest.json")
        assert ev.read_json("manifest.json")["job_id"] == "j1"

    def test_added_artifact_after_snapshot_is_invisible(self, tmp_path):
        _seed(tmp_path)
        ev = _brm._view_from_dir(str(tmp_path))
        (tmp_path / "task_runs" / "T002").mkdir()
        (tmp_path / "task_runs" / "T002" / "review.json").write_text("{}")
        assert ev.listdir("task_runs") == ["T001"]
        assert not ev.isfile("task_runs/T002/review.json")


class TestManifestUsesFrozenBytes:
    def test_manifest_job_id_is_the_snapshot_value_not_the_disk_value(self, tmp_path, monkeypatch):
        _seed(tmp_path)
        ev = _brm._view_from_dir(str(tmp_path))
        # Mutate the on-disk manifest AFTER the view (snapshot) is built.
        (tmp_path / "manifest.json").write_text(json.dumps({"job_id": "TAMPERED"}))
        monkeypatch.chdir(tmp_path)
        m = _brm.build_manifest_from_snapshot(ev, evidence_path=None)
        assert m["packaged_evidence_job_id"] == "j1"

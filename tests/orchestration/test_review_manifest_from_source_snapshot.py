"""F6 (round 24) — the Root Manifest is built from the IMMUTABLE Source snapshot bytes.

`build_manifest_from_snapshot` consumes an `_EvidenceView` over exactly the bytes the ZIP packages,
so no Evidence fact is interpreted from one read of the staging filesystem and packaged from another.
This suite pins the view semantics (a snapshot byte map answers every Evidence read), the
standalone/dir wrapper, and that the manifest-assembly core never opens the staging filesystem for
an Evidence fact.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_snap", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)


class _Member:
    """Minimal stand-in for a SnapshotMember: the view only reads ``.data`` bytes."""
    def __init__(self, data: bytes):
        self.data = data


def _snapshot(prefix, files):
    return {f"{prefix}/{rel}": _Member(data) for rel, data in files.items()}


class TestViewFromSnapshot:
    def test_reads_come_from_snapshot_bytes(self):
        snap = _snapshot("evidence/current", {
            "fresh_evidence_gate.json": b'{"verdict": "PASS"}',
            "task_runs/T001/review.json": b'{"final_verdict": "operator_attested"}',
        })
        ev = _brm._view_from_snapshot(snap, "evidence/current")
        assert ev.read_json("fresh_evidence_gate.json")["verdict"] == "PASS"
        assert ev.isdir("task_runs") and ev.listdir("task_runs") == ["T001"]
        assert ev.isfile("task_runs/T001/review.json")
        assert ev.read_bytes("task_runs/T001/review.json") == b'{"final_verdict": "operator_attested"}'

    def test_only_current_prefix_members_are_evidence(self):
        snap = _snapshot("evidence/current", {"manifest.json": b"{}"})
        snap["scripts/build_review_zip.py"] = _Member(b"# not evidence")
        ev = _brm._view_from_snapshot(snap, "evidence/current")
        assert ev.isfile("manifest.json")
        assert not ev.isfile("scripts/build_review_zip.py")

    def test_absent_read_is_empty(self):
        ev = _brm._view_from_snapshot(_snapshot("evidence/current", {}), "evidence/current")
        assert ev.read_json("nope.json") == {}
        assert ev.read_bytes("nope.json") is None
        assert ev.status("nope.json") == "absent"


class TestDirViewRoundTrips:
    def test_view_from_dir_reads_the_tree_once(self, tmp_path):
        (tmp_path / "manifest.json").write_text('{"job_id": "j1"}')
        (tmp_path / "task_runs" / "T001").mkdir(parents=True)
        (tmp_path / "task_runs" / "T001" / "review.json").write_text("{}")
        ev = _brm._view_from_dir(str(tmp_path))
        assert ev.read_json("manifest.json")["job_id"] == "j1"
        assert ev.listdir("task_runs") == ["T001"]

    def test_as_view_is_idempotent(self, tmp_path):
        (tmp_path / "manifest.json").write_text("{}")
        ev = _brm._view_from_dir(str(tmp_path))
        assert _brm._as_view(ev) is ev
        assert isinstance(_brm._as_view(str(tmp_path)), _brm._EvidenceView)
        assert _brm._as_view(None) is None


class TestManifestFactsMatchSnapshotBytes:
    def test_packaged_job_id_comes_from_snapshot(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        snap = _snapshot("evidence/current", {
            "manifest.json": json.dumps({"job_id": "SNAPJOB", "task_count": 1,
                                         "task_ids": ["T001"]}).encode(),
        })
        ev = _brm._view_from_snapshot(snap, "evidence/current")
        m = _brm.build_manifest_from_snapshot(ev, evidence_path=None)
        assert m["packaged_evidence_job_id"] == "SNAPJOB"
        assert m["packaged_evidence_manifest_task_ids"] == ["T001"]


class TestCoreNeverOpensStagingForEvidence:
    def test_no_direct_open_or_isfile_in_the_core(self):
        src = inspect.getsource(_brm.build_manifest_from_snapshot)
        # The manifest-assembly core reads Evidence only through the view; it must not open, stat or
        # list the staging filesystem itself.
        assert "open(" not in src
        assert "os.path.isfile" not in src
        assert "os.path.getmtime" not in src
        assert "os.listdir" not in src

    def test_helpers_route_evidence_reads_through_the_view(self):
        for fn in (_brm._scan_task_runs, _brm.validate_evidence_candidate,
                   _brm.validate_manual_completion, _brm._verify_commit_chain,
                   _brm._check_bundle_integrity, _brm._build_alignment):
            src = inspect.getsource(fn)
            # No helper reads an evidence artifact by joining the evidence dir and opening it.
            assert "os.path.join(evidence_dir" not in src, fn.__name__

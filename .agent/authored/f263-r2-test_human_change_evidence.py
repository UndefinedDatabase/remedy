"""F263 T001 — the human change record travels into the evidence bundle and BLOCKS when broken.

Temporary git repositories only. No provider call is ever made.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import human_change as HC
from packages.orchestration import pingpong_job as PJ
from packages.orchestration.data_paths import job_evidence_dir
from packages.orchestration.final_verifier import build_final_verifier_report
from packages.orchestration.job_evidence import export_job_evidence

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_human_change", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b)
_b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_human_change", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e)
_e.loader.exec_module(_E2E)


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    (r / "edit.txt").write_text("before\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


def _certify(repo: Path, job_id: str) -> Path:
    state = HC.capture_target_state(repo)
    (repo / "edit.txt").write_text("after, by hand\n")
    change = HC.detect_human_change(repo, state)
    return HC.write_human_change_record(job_id, repo, change, detected_by="test")


class TestTheExport:
    def test_a_job_without_records_exports_an_intact_empty_set(self, tmp_path):
        integrity, written = HC.export_human_change_records("job-1", tmp_path / "out")
        assert integrity == {"schema_version": "1.0.0", "ok": True, "records": [],
                             "failures": []}
        assert written == []

    def test_every_record_and_its_diff_travel_byte_for_byte(self, repo, tmp_path):
        record = _certify(repo, "job-1")
        out = tmp_path / "out"
        integrity, written = HC.export_human_change_records("job-1", out)
        assert integrity["ok"] is True and integrity["records"] == [record.stem]
        assert written == [f"human_changes/{record.name}", f"human_changes/{record.stem}.diff"]
        for rel in written:
            assert (out / rel).read_bytes() == (record.parent / Path(rel).name).read_bytes()

    def test_a_record_that_does_not_verify_is_a_failure_of_the_export(self, repo, tmp_path):
        record = _certify(repo, "job-1")
        diff = record.parent / f"{record.stem}.diff"
        diff.write_bytes(diff.read_bytes().replace(b"by hand", b"by hanD"))
        integrity, _ = HC.export_human_change_records("job-1", tmp_path / "out")
        assert integrity["ok"] is False
        assert integrity["failures"] == [f"{record.stem}: diff sha256 does not match the record"]


class TestTheJobExport:
    def test_the_bundle_carries_the_record_and_its_integrity(self, repo, tmp_path):
        job = PJ.parse_job_file("# One\n\n## Task 1 — write\n\nWrite one.txt.\n", str(repo))
        record = _certify(repo, job.job_id)
        out = tmp_path / "bundle"
        export_job_evidence(job.job_id, str(out))
        integrity = json.loads((out / HC.INTEGRITY_FILE).read_text())
        assert integrity["ok"] is True and integrity["records"] == [record.stem]
        assert (out / "human_changes" / record.name).read_bytes() == record.read_bytes()

    def test_a_broken_record_blocks_the_final_verifier(self, repo, tmp_path):
        job = PJ.parse_job_file("# One\n\n## Task 1 — write\n\nWrite one.txt.\n", str(repo))
        record = _certify(repo, job.job_id)
        body = json.loads(record.read_text())
        body["files"] = []
        record.write_text(json.dumps(body))
        out = tmp_path / "bundle"
        export_job_evidence(job.job_id, str(out))
        report = build_final_verifier_report(str(out))
        assert report["human_change_integrity_blocked"] is True
        assert report["verdict"] == "BLOCKED"


class TestTheFinalVerifier:
    def test_an_intact_set_does_not_block(self, tmp_path):
        (tmp_path / HC.INTEGRITY_FILE).write_text(json.dumps(
            {"schema_version": "1.0.0", "ok": True, "records": ["hcr-a-b"], "failures": []}))
        assert build_final_verifier_report(str(tmp_path))["human_change_integrity_blocked"] is False

    def test_a_failure_blocks(self, tmp_path):
        (tmp_path / HC.INTEGRITY_FILE).write_text(json.dumps(
            {"schema_version": "1.0.0", "ok": False, "records": ["hcr-a-b"],
             "failures": ["hcr-a-b: record_sha256 does not match the record"]}))
        report = build_final_verifier_report(str(tmp_path))
        assert report["human_change_integrity_blocked"] is True
        assert report["verdict"] == "BLOCKED"


def _ready(patch_name: str | None = None, **patch) -> bool:
    gates = {k: dict(v) for k, v in _E2E._complete_gates().items()}
    if patch_name is not None:
        gates[patch_name] = {**gates[patch_name], **patch}
    return _brm.evaluate_ready_gate_matrix(lambda name: gates.get(name))["ok"]


class TestTheReadyGate:
    def test_the_complete_matrix_with_the_new_gate_is_ready(self):
        assert _ready() is True

    def test_a_missing_integrity_file_is_not_ready(self):
        gates = {k: dict(v) for k, v in _E2E._complete_gates().items()}
        del gates[HC.INTEGRITY_FILE]
        assert _brm.evaluate_ready_gate_matrix(lambda name: gates.get(name))["ok"] is False

    def test_a_failure_in_the_integrity_file_is_not_ready(self):
        assert _ready(HC.INTEGRITY_FILE, ok=False, failures=["hcr-a-b: bad"]) is False

    def test_a_blocked_final_verifier_is_not_ready(self):
        assert _ready("final_verifier_report.json", human_change_integrity_blocked=True) is False

    def test_the_manual_completion_bundle_writes_an_intact_empty_set(self, tmp_path):
        from packages.orchestration.manual_attestation import build_manual_completion_gates

        build_manual_completion_gates(
            str(tmp_path), job_id="job-1", authority=["a.py"], file_hashes={"a.py": "sha256:x"},
            step="1-2", total_passed=1, verification_runs=[])
        gate = json.loads((tmp_path / HC.INTEGRITY_FILE).read_text())
        assert gate["ok"] is True and gate["records"] == []
        assert _brm._gate_closed_schema_problems(HC.INTEGRITY_FILE, gate) == []

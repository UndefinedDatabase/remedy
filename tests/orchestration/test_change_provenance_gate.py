"""Tests for change_provenance_gate.py — dirty source files vs evidence backing."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.change_provenance_gate import (
    build_change_provenance_gate,
    write_change_provenance_gate,
)


def _write_workspace_diff(evidence: Path, files: list[str]) -> None:
    lines = ["# Job workspace diff"]
    for f in files:
        lines.append(f"--- a/{f}")
        lines.append(f"+++ b/{f}")
        lines.append("+change")
    (evidence / "workspace.diff").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_apply_json(evidence: Path, files: list[str]) -> None:
    data = [{
        "task_id": "T001",
        "status": "completed",
        "apply_manifest": {"applied_files": files},
    }]
    (evidence / "workspace_apply.json").write_text(json.dumps(data) + "\n", encoding="utf-8")


def _write_task_safe_diff(evidence: Path, task_id: str, files: list[str]) -> None:
    task_dir = evidence / "task_runs" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    lines = []
    for f in files:
        lines.append(f"--- a/{f}")
        lines.append(f"+++ b/{f}")
        lines.append("+change")
    (task_dir / "safe.diff").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_all_covered_passes(tmp_path):
    _write_workspace_diff(tmp_path, ["packages/orchestration/foo.py"])
    gate = build_change_provenance_gate(
        str(tmp_path),
        ["packages/orchestration/foo.py"],
        "job-1",
    )

    assert gate["verdict"] == "PASS"
    assert gate["uncovered_files"] == []
    assert gate["covered_files"] == ["packages/orchestration/foo.py"]
    assert gate["issues"] == []
    assert gate["schema_version"] == "1.0.0"


def test_uncovered_source_blocks(tmp_path):
    _write_workspace_diff(tmp_path, ["packages/orchestration/foo.py"])
    gate = build_change_provenance_gate(
        str(tmp_path),
        ["packages/orchestration/foo.py", "packages/orchestration/bar.py"],
        "job-1",
    )

    assert gate["verdict"] == "BLOCKED"
    assert "packages/orchestration/bar.py" in gate["uncovered_files"]
    assert any("bar.py" in issue for issue in gate["issues"])


def test_apply_json_provides_coverage(tmp_path):
    _write_apply_json(tmp_path, ["src/mod.py"])
    gate = build_change_provenance_gate(str(tmp_path), ["src/mod.py"], "job-1")

    assert gate["verdict"] == "PASS"
    assert "workspace_apply.json" in gate["evidence_sources"]


def test_task_safe_diff_provides_coverage(tmp_path):
    _write_task_safe_diff(tmp_path, "T001", ["src/mod.py"])
    gate = build_change_provenance_gate(str(tmp_path), ["src/mod.py"], "job-1")

    assert gate["verdict"] == "PASS"
    assert "task_runs/T001/safe.diff" in gate["evidence_sources"]


def test_non_source_files_excluded(tmp_path):
    # No evidence at all, but every dirty file is a non-source artifact.
    dirty = [
        "packages/orchestration/__pycache__/foo.cpython-311.pyc",
        "remedy-job-evidence/manifest.json",
        "build/output.whl",
        "run.log",
        "remedy-review-123.zip",
        ".coverage",
        "htmlcov/index.html",
        "src/pkg.egg-info/PKG-INFO",
    ]
    gate = build_change_provenance_gate(str(tmp_path), dirty, "job-1")

    assert gate["verdict"] == "PASS"
    assert gate["source_files"] == []
    assert set(dirty) == set(gate["excluded_files"])


def test_empty_dirty_files_passes(tmp_path):
    gate = build_change_provenance_gate(str(tmp_path), [], "job-1")

    assert gate["verdict"] == "PASS"
    assert gate["source_files"] == []
    assert gate["uncovered_files"] == []


def test_current_job_id_recorded(tmp_path):
    gate = build_change_provenance_gate(str(tmp_path), [], "job-xyz")
    assert gate["current_job_id"] == "job-xyz"


def test_write_registers_output(tmp_path):
    _write_workspace_diff(tmp_path, ["src/mod.py"])
    written: dict[str, str] = {}
    write_change_provenance_gate(str(tmp_path), ["src/mod.py"], "job-1", written)

    assert "change_provenance_gate.json" in written
    on_disk = json.loads((tmp_path / "change_provenance_gate.json").read_text())
    assert on_disk["verdict"] == "PASS"
    assert on_disk["schema_version"] == "1.0.0"


def test_write_noop_when_no_evidence_dir():
    written: dict[str, str] = {}
    write_change_provenance_gate("", ["src/mod.py"], "job-1", written)
    assert written == {}


def test_content_hash_match_passes(tmp_path):
    """Path-covered file with matching content hash passes."""
    repo = tmp_path / "repo"
    repo.mkdir()
    src = repo / "src" / "mod.py"
    src.parent.mkdir(parents=True)
    src.write_text("print('hello')\n")

    import hashlib
    expected_hash = hashlib.sha256(src.read_bytes()).hexdigest()

    evidence = tmp_path / "evidence"
    evidence.mkdir()
    _write_workspace_diff(evidence, ["src/mod.py"])
    (evidence / "workspace_apply.json").write_text(json.dumps([{
        "task_id": "T001",
        "status": "completed",
        "apply_manifest": {
            "applied_files": ["src/mod.py"],
            "applied_file_proofs": {
                "src/mod.py": {"final_workspace_sha256": expected_hash},
            },
        },
    }]))

    gate = build_change_provenance_gate(
        str(evidence), ["src/mod.py"], "job-1", repo_root=str(repo),
    )
    assert gate["verdict"] == "PASS"
    assert gate["content_hash_verified"] is True
    assert gate["hash_mismatches"] == []


def test_content_hash_mismatch_blocks(tmp_path):
    """Path-covered file with different content hash blocks."""
    repo = tmp_path / "repo"
    repo.mkdir()
    src = repo / "src" / "mod.py"
    src.parent.mkdir(parents=True)
    src.write_text("print('modified')\n")

    evidence = tmp_path / "evidence"
    evidence.mkdir()
    _write_workspace_diff(evidence, ["src/mod.py"])
    (evidence / "workspace_apply.json").write_text(json.dumps([{
        "task_id": "T001",
        "status": "completed",
        "apply_manifest": {
            "applied_files": ["src/mod.py"],
            "applied_file_proofs": {
                "src/mod.py": {"final_workspace_sha256": "0000dead"},
            },
        },
    }]))

    gate = build_change_provenance_gate(
        str(evidence), ["src/mod.py"], "job-1", repo_root=str(repo),
    )
    assert gate["verdict"] == "BLOCKED"
    assert len(gate["hash_mismatches"]) == 1
    assert gate["hash_mismatches"][0]["file"] == "src/mod.py"
    assert any("content hash mismatch" in i for i in gate["issues"])


def test_no_hash_proof_still_passes_path_only(tmp_path):
    """When no evidence hash exists, path coverage alone passes (no repo_root)."""
    _write_workspace_diff(tmp_path, ["src/mod.py"])
    gate = build_change_provenance_gate(str(tmp_path), ["src/mod.py"], "job-1")
    assert gate["verdict"] == "PASS"
    assert gate["content_hash_verified"] is False


def test_content_proof_json_provides_hashes(tmp_path):
    """current_change_content_proof.json is read as a hash source."""
    repo = tmp_path / "repo"
    repo.mkdir()
    src = repo / "src" / "mod.py"
    src.parent.mkdir(parents=True)
    src.write_text("content\n")

    import hashlib
    h = hashlib.sha256(src.read_bytes()).hexdigest()

    evidence = tmp_path / "evidence"
    evidence.mkdir()
    _write_workspace_diff(evidence, ["src/mod.py"])
    (evidence / "current_change_content_proof.json").write_text(json.dumps({
        "file_hashes": {"src/mod.py": h},
    }))

    gate = build_change_provenance_gate(
        str(evidence), ["src/mod.py"], "job-1", repo_root=str(repo),
    )
    assert gate["verdict"] == "PASS"
    assert "current_change_content_proof.json" in gate["evidence_sources"]


def test_excluded_operational_dirs_not_source(tmp_path):
    """Operational evidence dirs are excluded, not counted as source."""
    dirty = [
        "remedy-job-evidence-selfrun/manifest.json",
        ".agent/live_review.md",
        "run_transcript.txt",
        ".data/cache.json",
    ]
    gate = build_change_provenance_gate(str(tmp_path), dirty, "job-1")
    assert gate["verdict"] == "PASS"
    assert gate["source_files"] == []
    assert len(gate["excluded_files"]) == 4


def test_stale_apply_proofs_tracked(tmp_path):
    """Stale workspace_apply hashes superseded by content proof are tracked."""
    _write_workspace_diff(tmp_path, ["src/mod.py"])
    apply_data = [{
        "task_id": "T001",
        "status": "completed",
        "apply_manifest": {
            "applied_files": ["src/mod.py"],
            "applied_file_proofs": {
                "src/mod.py": {"sha256": "old_hash_aaa"},
            },
        },
    }]
    (tmp_path / "workspace_apply.json").write_text(
        json.dumps(apply_data) + "\n", encoding="utf-8",
    )
    proof = {"schema_version": "1.0.0", "file_hashes": {"src/mod.py": "new_hash_bbb"}}
    (tmp_path / "current_change_content_proof.json").write_text(
        json.dumps(proof) + "\n", encoding="utf-8",
    )
    src = tmp_path / "repo" / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / "mod.py").write_text("content")
    gate = build_change_provenance_gate(
        str(tmp_path), ["src/mod.py"], "job-1", repo_root=str(tmp_path / "repo"),
    )
    assert len(gate["stale_apply_proofs"]) == 1
    stale = gate["stale_apply_proofs"][0]
    assert stale["file"] == "src/mod.py"
    assert stale["apply_sha256"] == "old_hash_aaa"
    assert stale["current_proof_sha256"] == "new_hash_bbb"


def test_list_shaped_apply_proofs_parsed(tmp_path):
    """List-shaped applied_file_proofs are parsed for hashes."""
    _write_workspace_diff(tmp_path, ["src/mod.py"])
    apply_data = [{
        "task_id": "T001",
        "status": "completed",
        "apply_manifest": {
            "applied_files": ["src/mod.py"],
            "applied_file_proofs": [
                {"path": "src/mod.py", "final_workspace_sha256": "abc123"},
            ],
        },
    }]
    (tmp_path / "workspace_apply.json").write_text(
        json.dumps(apply_data) + "\n", encoding="utf-8",
    )
    src = tmp_path / "repo" / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / "mod.py").write_text("content")
    gate = build_change_provenance_gate(
        str(tmp_path), ["src/mod.py"], "job-1", repo_root=str(tmp_path / "repo"),
    )
    assert "abc123" in gate["evidence_hashes"].values()


def test_stale_list_apply_proof_tracked(tmp_path):
    """List-shaped apply proof superseded by content proof is tracked."""
    _write_workspace_diff(tmp_path, ["src/mod.py"])
    apply_data = [{
        "task_id": "T001",
        "status": "completed",
        "apply_manifest": {
            "applied_files": ["src/mod.py"],
            "applied_file_proofs": [
                {"path": "src/mod.py", "final_workspace_sha256": "old_list_hash"},
            ],
        },
    }]
    (tmp_path / "workspace_apply.json").write_text(
        json.dumps(apply_data) + "\n", encoding="utf-8",
    )
    proof = {"schema_version": "1.0.0", "file_hashes": {"src/mod.py": "new_proof_hash"}}
    (tmp_path / "current_change_content_proof.json").write_text(
        json.dumps(proof) + "\n", encoding="utf-8",
    )
    src = tmp_path / "repo" / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / "mod.py").write_text("content")
    gate = build_change_provenance_gate(
        str(tmp_path), ["src/mod.py"], "job-1", repo_root=str(tmp_path / "repo"),
    )
    assert len(gate["stale_apply_proofs"]) == 1
    stale = gate["stale_apply_proofs"][0]
    assert stale["apply_sha256"] == "old_list_hash"
    assert stale["current_proof_sha256"] == "new_proof_hash"


def test_dict_shaped_apply_proofs_still_work(tmp_path):
    """Dict-shaped applied_file_proofs (original format) still parse."""
    _write_workspace_diff(tmp_path, ["src/mod.py"])
    apply_data = [{
        "task_id": "T001",
        "status": "completed",
        "apply_manifest": {
            "applied_files": ["src/mod.py"],
            "applied_file_proofs": {
                "src/mod.py": {"final_workspace_sha256": "dict_hash_xyz"},
            },
        },
    }]
    (tmp_path / "workspace_apply.json").write_text(
        json.dumps(apply_data) + "\n", encoding="utf-8",
    )
    src = tmp_path / "repo" / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / "mod.py").write_text("content")
    gate = build_change_provenance_gate(
        str(tmp_path), ["src/mod.py"], "job-1", repo_root=str(tmp_path / "repo"),
    )
    assert gate["evidence_hashes"]["src/mod.py"] == "dict_hash_xyz"


def test_stale_apply_no_content_proof_blocks(tmp_path):
    """Stale apply hash with no current content proof → hash mismatch → BLOCKED."""
    _write_workspace_diff(tmp_path, ["src/mod.py"])
    apply_data = [{
        "task_id": "T001",
        "status": "completed",
        "apply_manifest": {
            "applied_files": ["src/mod.py"],
            "applied_file_proofs": [
                {"path": "src/mod.py", "final_workspace_sha256": "stale_hash"},
            ],
        },
    }]
    (tmp_path / "workspace_apply.json").write_text(
        json.dumps(apply_data) + "\n", encoding="utf-8",
    )
    # No current_change_content_proof.json — apply hash is authoritative
    src = tmp_path / "repo" / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / "mod.py").write_text("definitely different content")
    gate = build_change_provenance_gate(
        str(tmp_path), ["src/mod.py"], "job-1", repo_root=str(tmp_path / "repo"),
    )
    # stale_hash won't match SHA256 of "definitely different content"
    assert gate["verdict"] == "BLOCKED"
    assert len(gate["hash_mismatches"]) == 1


def test_real_workspace_apply_list_proofs(tmp_path):
    """Real workspace_apply fixture with list proofs → expected stale_apply_proofs."""
    _write_workspace_diff(tmp_path, ["packages/orchestration/gate.py", "tests/test_gate.py"])
    apply_data = [{
        "task_id": "T001",
        "status": "applied_to_job_workspace",
        "apply_manifest": {
            "applied_files": ["packages/orchestration/gate.py", "tests/test_gate.py"],
            "applied_file_proofs": [
                {"path": "packages/orchestration/gate.py", "final_workspace_sha256": "aaa111"},
                {"path": "tests/test_gate.py", "final_workspace_sha256": "bbb222"},
            ],
        },
    }]
    (tmp_path / "workspace_apply.json").write_text(
        json.dumps(apply_data) + "\n", encoding="utf-8",
    )
    proof = {
        "schema_version": "1.0.0",
        "file_hashes": {
            "packages/orchestration/gate.py": "ccc333",
            "tests/test_gate.py": "ddd444",
        },
    }
    (tmp_path / "current_change_content_proof.json").write_text(
        json.dumps(proof) + "\n", encoding="utf-8",
    )
    pkg = tmp_path / "repo" / "packages" / "orchestration"
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "gate.py").write_text("gate content")
    tests = tmp_path / "repo" / "tests"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / "test_gate.py").write_text("test content")
    gate = build_change_provenance_gate(
        str(tmp_path),
        ["packages/orchestration/gate.py", "tests/test_gate.py"],
        "job-1",
        repo_root=str(tmp_path / "repo"),
    )
    assert len(gate["stale_apply_proofs"]) == 2
    stale_files = {s["file"] for s in gate["stale_apply_proofs"]}
    assert "packages/orchestration/gate.py" in stale_files
    assert "tests/test_gate.py" in stale_files


def test_unrelated_source_file_blocks(tmp_path):
    """A dirty source file with no evidence backing blocks."""
    _write_workspace_diff(tmp_path, ["src/mod.py"])
    gate = build_change_provenance_gate(
        str(tmp_path),
        ["src/mod.py", "packages/orchestration/design_worker.py"],
        "job-1",
    )
    assert gate["verdict"] == "BLOCKED"
    assert "packages/orchestration/design_worker.py" in gate["uncovered_files"]

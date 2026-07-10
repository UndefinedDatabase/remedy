"""Tests for artifact_contract_gate.py — required artifact contract checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from packages.orchestration.artifact_contract_gate import (
    CORE_ARTIFACTS,
    CRITICAL_FV_REFERENCES,
    build_artifact_contract_gate,
    check_stream_artifacts,
    write_artifact_contract_gate,
)


def _write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data) + "\n", encoding="utf-8")


def _seed_core(tmp_path: Path, job_id: str = "job-abc", completeness: dict | None = None) -> str:
    for name in CORE_ARTIFACTS:
        if name == "manifest.json":
            _write(tmp_path / name, {"job_id": job_id})
        elif name == "final_verifier_report.json":
            _write(tmp_path / name, {"evidence_completeness": completeness or {}})
        else:
            _write(tmp_path / name, {"ok": True})
    return str(tmp_path)


def test_all_present_passes(tmp_path):
    evidence = _seed_core(tmp_path)
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "PASS"
    assert gate["missing_required"] == []
    assert gate["issues"] == []
    assert all(gate["required_artifacts"].values())
    assert gate["schema_version"] == "1.0.0"


def test_missing_core_blocks(tmp_path):
    evidence = _seed_core(tmp_path)
    (tmp_path / "token_truth.json").unlink()

    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "token_truth.json" in gate["missing_required"]
    assert any("token_truth.json" in issue for issue in gate["issues"])


def test_critical_fv_referenced_missing_blocks(tmp_path):
    evidence = _seed_core(
        tmp_path,
        completeness={"token_truth": False, "safe_diff": True},
    )
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "token_truth" in gate["fv_referenced_missing"]
    assert "token_truth" in gate["critical_fv_missing"]


def test_noncritical_fv_referenced_missing_not_blocked(tmp_path):
    evidence = _seed_core(
        tmp_path,
        completeness={"review_scope_packet": False, "spec_compliance_check": False},
    )
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "PASS"
    assert "review_scope_packet" in gate["fv_referenced_missing"]
    assert gate["critical_fv_missing"] == []


def test_change_provenance_gate_missing_blocks(tmp_path):
    evidence = _seed_core(tmp_path)
    (tmp_path / "change_provenance_gate.json").unlink(missing_ok=True)

    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "change_provenance_gate.json" in gate["missing_required"]


def test_stale_job_id_blocks(tmp_path):
    evidence = _seed_core(tmp_path, job_id="job-old")
    gate = build_artifact_contract_gate(evidence, current_job_id="job-new")

    assert gate["verdict"] == "BLOCKED"
    assert gate["job_id_fresh"] is False
    assert gate["evidence_job_id"] == "job-old"
    assert any("job_id" in issue for issue in gate["issues"])


def test_commit_execution_gate_missing_blocks(tmp_path):
    evidence = _seed_core(tmp_path)
    (tmp_path / "commit_execution_gate.json").unlink(missing_ok=True)

    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "commit_execution_gate.json" in gate["missing_required"]


def test_fv_referenced_missing_tests_txt_blocks(tmp_path):
    evidence = _seed_core(
        tmp_path,
        completeness={"tests_txt": False},
    )
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "tests_txt" in gate["critical_fv_missing"]


def test_fv_referenced_missing_safe_diff_blocks(tmp_path):
    evidence = _seed_core(
        tmp_path,
        completeness={"safe_diff": False},
    )
    gate = build_artifact_contract_gate(evidence)

    assert gate["verdict"] == "BLOCKED"
    assert "safe_diff" in gate["critical_fv_missing"]


def test_critical_references_include_all_gates(tmp_path):
    expected = {"token_truth", "fresh_evidence_gate", "artifact_contract_gate",
                "runtime_integration_gate", "commit_execution_gate",
                "change_provenance_gate", "safe_diff", "review_json", "tests_txt"}
    assert CRITICAL_FV_REFERENCES == expected


def test_write_registers_output(tmp_path):
    evidence = _seed_core(tmp_path)
    written: dict[str, str] = {}
    write_artifact_contract_gate(evidence, written)

    assert "artifact_contract_gate.json" in written
    on_disk = json.loads((tmp_path / "artifact_contract_gate.json").read_text())
    assert on_disk["verdict"] == "PASS"
    assert on_disk["schema_version"] == "1.0.0"


# ---------------------------------------------------------------------------
# Finding 7 — referenced F004 stream artifacts must exist in the bundle
# ---------------------------------------------------------------------------

_REFS = [
    "streams/builder/round-01/attempt-01/raw_stream.jsonl",
    "streams/builder/round-01/attempt-01/run_events.jsonl",
]


_CONTENT = {
    "streams/builder/round-01/attempt-01/raw_stream.jsonl": '{"type":"result"}\n',
    "streams/builder/round-01/attempt-01/run_events.jsonl": '{"seq":1}\n',
}


def _bundle_with_streams(
    base, *, refs=_REFS, present=True, stream_evidence=True, listing=True,
):
    """Minimal evidence bundle with one task run and its stream artifact listing.

    The listing mirrors what ``job_evidence._copy_task_stream_artifacts`` writes:
    bundle-relative path -> {sha256, size_bytes}.
    """
    run = base / "task_runs" / "T001"
    run.mkdir(parents=True, exist_ok=True)
    pe = {"builder_provider": "claude", "reviewer_provider": "claude"}
    if stream_evidence:
        pe["stream_evidence_present"] = True
        pe["stream_artifact_refs"] = list(refs)
    (run / "provider_evidence.json").write_text(json.dumps(pe), encoding="utf-8")

    artifacts = {}
    if present:
        for ref in refs:
            p = run / ref
            p.parent.mkdir(parents=True, exist_ok=True)
            data = _CONTENT.get(ref, '{"type":"result"}\n').encode()
            p.write_bytes(data)
            artifacts[f"task_runs/T001/{ref}"] = {
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
            }
    if listing and stream_evidence:
        (run / "stream_artifacts.json").write_text(
            json.dumps({"schema_version": "1.0.0", "task_id": "T001",
                        "artifacts": artifacts}),
            encoding="utf-8",
        )
    return base


def _artifact(base, ref):
    return base / "task_runs" / "T001" / ref


def _listing_path(base):
    return base / "task_runs" / "T001" / "stream_artifacts.json"


def _patch_listing(base, fn):
    p = _listing_path(base)
    doc = json.loads(p.read_text())
    fn(doc["artifacts"])
    p.write_text(json.dumps(doc), encoding="utf-8")


def _both_blocked(base):
    res = check_stream_artifacts(str(base))
    gate = build_artifact_contract_gate(str(base))
    assert res["verdict"] == "BLOCKED", res
    assert gate["verdict"] == "BLOCKED", gate["issues"]
    return res


class TestStreamArtifactContract:
    def test_not_applicable_without_stream_evidence(self, tmp_path):
        _bundle_with_streams(tmp_path, present=False, stream_evidence=False)
        res = check_stream_artifacts(str(tmp_path))
        assert res["applicable"] is False
        assert res["verdict"] == "NOT_APPLICABLE"
        assert build_artifact_contract_gate(str(tmp_path))["stream_artifacts"]["verdict"] == "NOT_APPLICABLE"

    def test_passes_when_all_referenced_artifacts_exist(self, tmp_path):
        _bundle_with_streams(tmp_path)
        res = check_stream_artifacts(str(tmp_path))
        assert res["verdict"] == "PASS"
        assert res["artifacts_verified"] == 2
        assert res["artifacts_present"] == 2
        assert res["tasks_with_stream_evidence"] == ["T001"]
        assert res["stream_artifact_hash_mismatches"] == []
        assert res["stream_artifact_size_mismatches"] == []

    def test_blocks_when_a_referenced_artifact_is_missing(self, tmp_path):
        _bundle_with_streams(tmp_path, present=False)
        res = check_stream_artifacts(str(tmp_path))
        assert res["verdict"] == "BLOCKED"
        assert len(res["missing_stream_artifacts"]) == 2

        gate = build_artifact_contract_gate(str(tmp_path))
        assert gate["verdict"] == "BLOCKED"
        assert any("raw_stream.jsonl" in i for i in gate["issues"])

    def test_blocks_unsafe_refs(self, tmp_path):
        _bundle_with_streams(
            tmp_path, refs=["../../etc/passwd", "/abs/raw_stream.jsonl"], present=False,
        )
        res = check_stream_artifacts(str(tmp_path))
        assert res["verdict"] == "BLOCKED"
        assert len(res["unsafe_stream_artifact_refs"]) == 2
        assert res["missing_stream_artifacts"] == []

    def test_history_bundle_does_not_influence_current_verdict(self, tmp_path):
        current = tmp_path / "current"
        _bundle_with_streams(current)
        # A sibling history bundle with broken refs must not be scanned.
        _bundle_with_streams(tmp_path / "history" / "oldjob", present=False)
        assert build_artifact_contract_gate(str(current))["stream_artifacts"]["verdict"] == "PASS"


# ---------------------------------------------------------------------------
# Finding 1 — existence is not integrity: hashes and sizes are recomputed
# ---------------------------------------------------------------------------

_RAW = _REFS[0]
_EVENTS = _REFS[1]


class TestStreamArtifactTampering:
    def test_one_byte_raw_stream_modification_blocks(self, tmp_path):
        _bundle_with_streams(tmp_path)
        p = _artifact(tmp_path, _RAW)
        p.write_bytes(p.read_bytes().replace(b'"result"', b'"resulX"'))
        res = _both_blocked(tmp_path)
        assert [m["path"] for m in res["stream_artifact_hash_mismatches"]] == [
            f"task_runs/T001/{_RAW}"
        ]

    def test_one_byte_run_events_modification_blocks(self, tmp_path):
        _bundle_with_streams(tmp_path)
        p = _artifact(tmp_path, _EVENTS)
        p.write_bytes(p.read_bytes().replace(b"1", b"2"))
        res = _both_blocked(tmp_path)
        assert [m["path"] for m in res["stream_artifact_hash_mismatches"]] == [
            f"task_runs/T001/{_EVENTS}"
        ]

    def test_same_size_different_content_blocks(self, tmp_path):
        """A swap that preserves byte length must still be caught by the hash."""
        _bundle_with_streams(tmp_path)
        p = _artifact(tmp_path, _RAW)
        original = p.read_bytes()
        tampered = original.replace(b"result", b"rZsult")
        assert len(tampered) == len(original)
        p.write_bytes(tampered)

        res = _both_blocked(tmp_path)
        assert res["stream_artifact_hash_mismatches"], "hash check did not fire"
        assert res["stream_artifact_size_mismatches"] == [], "size happened to differ"

    def test_wrong_recorded_size_blocks(self, tmp_path):
        _bundle_with_streams(tmp_path)
        _patch_listing(tmp_path, lambda a: a[f"task_runs/T001/{_RAW}"].update(size_bytes=99999))
        res = _both_blocked(tmp_path)
        assert [m["path"] for m in res["stream_artifact_size_mismatches"]] == [
            f"task_runs/T001/{_RAW}"
        ]
        assert res["stream_artifact_hash_mismatches"] == []

    def test_missing_metadata_entry_blocks(self, tmp_path):
        _bundle_with_streams(tmp_path)
        _patch_listing(tmp_path, lambda a: a.pop(f"task_runs/T001/{_EVENTS}"))
        res = _both_blocked(tmp_path)
        assert res["missing_stream_artifact_metadata"] == [f"task_runs/T001/{_EVENTS}"]

    def test_extra_metadata_entry_blocks(self, tmp_path):
        _bundle_with_streams(tmp_path)
        _patch_listing(
            tmp_path,
            lambda a: a.update({
                "task_runs/T001/streams/builder/round-01/attempt-01/ghost.jsonl": {
                    "sha256": "0" * 64, "size_bytes": 1,
                }
            }),
        )
        res = _both_blocked(tmp_path)
        assert res["unexpected_stream_artifacts"] == [
            "task_runs/T001/streams/builder/round-01/attempt-01/ghost.jsonl"
        ]

    def test_missing_provider_reference_blocks(self, tmp_path):
        """A file listed and present, but no longer referenced, is unexpected."""
        _bundle_with_streams(tmp_path)
        run = tmp_path / "task_runs" / "T001"
        pe = json.loads((run / "provider_evidence.json").read_text())
        pe["stream_artifact_refs"] = [_RAW]  # drop the run_events reference
        (run / "provider_evidence.json").write_text(json.dumps(pe), encoding="utf-8")
        res = _both_blocked(tmp_path)
        assert res["unexpected_stream_artifacts"] == [f"task_runs/T001/{_EVENTS}"]

    def test_unsafe_listing_path_blocks(self, tmp_path):
        _bundle_with_streams(tmp_path)
        _patch_listing(
            tmp_path,
            lambda a: a.update({"/etc/passwd": {"sha256": "0" * 64, "size_bytes": 1}}),
        )
        res = _both_blocked(tmp_path)
        assert "/etc/passwd" in res["unexpected_stream_artifacts"]

    def test_missing_listing_file_blocks(self, tmp_path):
        _bundle_with_streams(tmp_path, listing=False)
        res = _both_blocked(tmp_path)
        assert res["missing_stream_artifact_listing"] == [
            "task_runs/T001/stream_artifacts.json"
        ]

    def test_duplicate_reference_blocks(self, tmp_path):
        _bundle_with_streams(tmp_path, refs=[_RAW, _EVENTS, _RAW])
        res = _both_blocked(tmp_path)
        assert res["duplicate_stream_artifact_refs"] == [f"task_runs/T001/{_RAW}"]

    def test_untampered_bundle_still_passes(self, tmp_path):
        _bundle_with_streams(tmp_path)
        assert check_stream_artifacts(str(tmp_path))["verdict"] == "PASS"
        assert build_artifact_contract_gate(str(tmp_path))["stream_artifacts"]["verdict"] == "PASS"

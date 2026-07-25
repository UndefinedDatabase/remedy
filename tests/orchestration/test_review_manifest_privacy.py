"""F004 Findings 3 and 4 — the shareable manifest must be honest and private.

The review manifest travels to external reviewers. It must never disclose a
machine-specific absolute path, and it must report the real Job ID and final
audit status for an operator-attested manual completion (which deliberately has
no ``job_flow.json``).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.build_review_manifest import (  # noqa: E402
    _read_final_audit,
    _read_job_id,
    _shareable_path,
)

FORBIDDEN_PREFIXES = ("/home/", "/Users/", "/private/", "/tmp/", "/mnt/", "/var/folders/")


def _manual_bundle(base: Path, job_id: str = "manualjob123") -> Path:
    base.mkdir(parents=True, exist_ok=True)
    (base / "manifest.json").write_text(json.dumps({"job_id": job_id}))
    (base / "final_verifier_report.json").write_text(json.dumps({"verdict": "PASS_WITH_RISKS"}))
    (base / "final_job_review.json").write_text(json.dumps({"job_id": job_id, "verdict": "operator_attested"}))
    return base


def _provider_bundle(base: Path, job_id: str = "providerjob9") -> Path:
    base.mkdir(parents=True, exist_ok=True)
    (base / "manifest.json").write_text(json.dumps({"job_id": "stale-should-not-win"}))
    (base / "job_flow.json").write_text(json.dumps({
        "job_id": job_id,
        "final_audit": {"status": "PASS", "missing_observability_artifacts": []},
    }))
    return base


class TestManualCompletionIdentity:
    def test_job_id_falls_back_to_manifest(self, tmp_path):
        ev = _manual_bundle(tmp_path / "manual")
        assert _read_job_id(str(ev)) == "manualjob123"

    def test_job_id_never_empty_when_manifest_has_one(self, tmp_path):
        ev = _manual_bundle(tmp_path / "m2")
        (ev / "final_job_review.json").unlink()
        assert _read_job_id(str(ev)) == "manualjob123"

    def test_final_audit_uses_final_verifier_verdict(self, tmp_path):
        ev = _manual_bundle(tmp_path / "m3")
        assert _read_final_audit(str(ev))["status"] == "PASS_WITH_RISKS"

    def test_final_audit_falls_back_to_final_job_review(self, tmp_path):
        ev = _manual_bundle(tmp_path / "m4")
        (ev / "final_verifier_report.json").unlink()
        assert _read_final_audit(str(ev))["status"] == "operator_attested"

    def test_no_provider_observability_is_fabricated(self, tmp_path):
        ev = _manual_bundle(tmp_path / "m5")
        assert not (ev / "job_flow.json").exists()
        assert _read_final_audit(str(ev))["missing_observability_artifacts"] == []


class TestProviderBundleUnchanged:
    def test_job_flow_job_id_wins(self, tmp_path):
        ev = _provider_bundle(tmp_path / "prov")
        assert _read_job_id(str(ev)) == "providerjob9"

    def test_job_flow_final_audit_wins(self, tmp_path):
        ev = _provider_bundle(tmp_path / "prov2")
        assert _read_final_audit(str(ev))["status"] == "PASS"


class TestShareablePath:
    def test_repo_paths_become_source_root_token(self, tmp_path):
        root = tmp_path / "repo"
        (root / "a" / "b").mkdir(parents=True)
        assert _shareable_path(str(root), str(root)) == "[source_root]"
        assert _shareable_path(str(root / "a" / "b"), str(root)) == "[source_root]/a/b"

    def test_outside_paths_collapse_to_placeholder(self, tmp_path):
        root = tmp_path / "repo"
        root.mkdir()
        outside = tmp_path / "elsewhere" / "evidence_bundle"
        outside.mkdir(parents=True)
        assert _shareable_path(str(outside), str(root)) == "[external_evidence]/evidence_bundle"

    def test_never_emits_a_private_prefix(self, tmp_path):
        root = tmp_path / "repo"
        root.mkdir()
        for candidate in (str(root), str(root / "x"), str(tmp_path / "outside")):
            rendered = _shareable_path(candidate, str(root))
            for bad in FORBIDDEN_PREFIXES:
                assert bad not in rendered, f"{rendered!r} leaks {bad}"

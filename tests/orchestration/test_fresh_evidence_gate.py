"""Tests for fresh_evidence_gate.py — run freshness + validity + authority."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.fresh_evidence_gate import (
    build_fresh_evidence_gate,
    write_fresh_evidence_gate,
)


def _seed_manifest(tmp_path: Path, job_id: str) -> str:
    (tmp_path / "manifest.json").write_text(
        json.dumps({"job_id": job_id, "bundle_type": "job_evidence"}) + "\n"
    )
    return str(tmp_path)


def _seed_agent(monkeypatch, tmp_path: Path, plan_range: str, lr_range: str) -> None:
    """Point .agent lookups at a controlled agent dir under tmp_path."""
    agent = tmp_path / ".agent"
    agent.mkdir(exist_ok=True)
    (agent / "plan.md").write_text(f"# Steps {plan_range}: something\n")
    (agent / "live_review.md").write_text(f"# Live Review — Steps {lr_range}\n")
    monkeypatch.chdir(tmp_path)


def test_matching_job_id_with_step_range_passes(tmp_path, monkeypatch):
    evidence = _seed_manifest(tmp_path, "job-abc")
    _seed_agent(monkeypatch, tmp_path, plan_range="5681-5740", lr_range="5681-5740")
    gate = build_fresh_evidence_gate(evidence, "job-abc", current_step_range="5681-5740")

    assert gate["verdict"] == "PASS"
    assert gate["job_id_match"] is True
    assert gate["evidence_job_id"] == "job-abc"
    assert gate["schema_version"] == "1.0.0"
    assert gate["issues"] == []


def test_empty_step_range_blocks(tmp_path):
    evidence = _seed_manifest(tmp_path, "job-abc")
    gate = build_fresh_evidence_gate(evidence, "job-abc")

    assert gate["verdict"] == "BLOCKED"
    assert gate["current_step_range"] == ""
    assert any("current_step_range is empty" in issue for issue in gate["issues"])
    assert gate["evidence_authoritative"] is False


def test_none_step_range_blocks(tmp_path):
    evidence = _seed_manifest(tmp_path, "job-abc")
    gate = build_fresh_evidence_gate(evidence, "job-abc", current_step_range=None)

    assert gate["verdict"] == "BLOCKED"
    assert gate["current_step_range"] == ""


def test_mismatched_job_id_blocks(tmp_path):
    evidence = _seed_manifest(tmp_path, "job-old")
    gate = build_fresh_evidence_gate(evidence, "job-new")

    assert gate["verdict"] == "BLOCKED"
    assert gate["job_id_match"] is False
    assert gate["evidence_authoritative"] is False
    assert any("job_id" in issue for issue in gate["issues"])


def test_validity_and_authoritative_fields(tmp_path, monkeypatch):
    evidence = _seed_manifest(tmp_path, "job-abc")
    _seed_agent(monkeypatch, tmp_path, plan_range="5681-5740", lr_range="5681-5740")
    gate = build_fresh_evidence_gate(evidence, "job-abc", current_step_range="5681-5740")

    assert gate["evidence_freshness"] == {
        "is_fresh": True,
        "job_id_match": True,
        "step_range_match": True,
    }
    assert gate["evidence_validity"]["is_valid_current_run"] is True
    assert gate["evidence_validity"]["has_job_id"] is True
    assert gate["evidence_validity"]["has_manifest"] is True
    assert gate["evidence_authoritative"] is True


def test_stale_evidence_not_authoritative(tmp_path):
    gate = build_fresh_evidence_gate(str(tmp_path), "job-abc")

    assert gate["evidence_job_id"] == ""
    assert gate["evidence_validity"]["is_valid_current_run"] is False
    assert gate["evidence_validity"]["has_manifest"] is False
    assert gate["evidence_authoritative"] is False
    assert gate["verdict"] == "BLOCKED"


def test_step_range_mismatch_warns(tmp_path, monkeypatch):
    evidence = _seed_manifest(tmp_path, "job-abc")
    _seed_agent(monkeypatch, tmp_path, plan_range="1000-1050", lr_range="1000-1050")

    gate = build_fresh_evidence_gate(evidence, "job-abc", current_step_range="5621-5680")

    assert gate["verdict"] == "PASS_WITH_RISKS"
    assert gate["job_id_match"] is True
    assert gate["plan_match"] is False
    assert gate["live_review_match"] is False
    assert gate["evidence_authoritative"] is False
    assert gate["current_step_range"] == "5621-5680"


def test_step_range_match_passes(tmp_path, monkeypatch):
    evidence = _seed_manifest(tmp_path, "job-abc")
    _seed_agent(monkeypatch, tmp_path, plan_range="5621-5680", lr_range="5621-5680")

    gate = build_fresh_evidence_gate(evidence, "job-abc", current_step_range="Steps 5621-5680")

    assert gate["verdict"] == "PASS"
    assert gate["plan_match"] is True
    assert gate["live_review_match"] is True
    assert gate["current_step_range"] == "5621-5680"
    assert gate["evidence_authoritative"] is True


def test_write_registers_output(tmp_path, monkeypatch):
    evidence = _seed_manifest(tmp_path, "job-abc")
    _seed_agent(monkeypatch, tmp_path, plan_range="5681-5740", lr_range="5681-5740")
    written: dict[str, str] = {}
    write_fresh_evidence_gate(evidence, "job-abc", current_step_range="5681-5740", written=written)

    assert "fresh_evidence_gate.json" in written
    on_disk = json.loads((tmp_path / "fresh_evidence_gate.json").read_text())
    assert on_disk["verdict"] == "PASS"
    assert on_disk["schema_version"] == "1.0.0"

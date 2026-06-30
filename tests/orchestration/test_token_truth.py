"""Tests for token_truth.py — honest actual-vs-estimated aggregation + writer."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.token_truth import (
    build_token_truth,
    write_token_truth,
)


def _run_dir(base: Path, task_id: str) -> Path:
    d = base / "task_runs" / task_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _seed_task(
    base: Path,
    task_id: str = "T001",
    *,
    builder: int = 8573,
    reviewer: int = 4923,
    repair: int = 0,
    provider_evidence: dict | None = None,
) -> None:
    d = _run_dir(base, task_id)
    (d / "token_accounting.json").write_text(json.dumps({
        "kind": "estimated",
        "actual_tokens_available": False,
        "builder_prompt_tokens_estimated": builder,
        "reviewer_prompt_tokens_estimated": reviewer,
        "repair_prompt_tokens_estimated": repair,
    }))
    if provider_evidence is None:
        provider_evidence = {
            "builder_provider": "claude-cli",
            "reviewer_provider": "claude-cli",
        }
    (d / "provider_evidence.json").write_text(json.dumps(provider_evidence))


def test_estimated_only_no_actual(tmp_path: Path) -> None:
    _seed_task(tmp_path)
    (tmp_path / "prompt_trace_summary.json").write_text(json.dumps({
        "total_prompts": 2,
    }))

    report = build_token_truth(str(tmp_path))

    assert report["schema_version"] == "1.0.0"
    assert report["source"] == "evidence_aggregation"
    assert report["provider"] == "claude-cli"
    assert report["actual_available"] is False
    assert report["actual_prompt_tokens"] is None
    assert report["actual_completion_tokens"] is None
    assert report["actual_total_tokens"] is None
    assert report["actual_cache_creation_tokens"] is None
    assert report["actual_cache_read_tokens"] is None
    assert report["estimated_prompt_tokens"] == 13496
    assert report["estimated_completion_tokens"] == 0
    assert report["estimated_total_tokens"] == 13496
    assert report["measurement_source"] == "character_heuristic"
    assert report["measurement_confidence"] == "low"
    assert report["missing_reason"]
    assert report["builder_estimated_total"] == 8573
    assert report["reviewer_estimated_total"] == 4923
    assert report["repair_estimated_total"] == 0
    assert report["provider_call_count"] == 2
    assert report["per_task"]["T001"] == {
        "builder_estimated": 8573,
        "reviewer_estimated": 4923,
        "repair_estimated": 0,
        "actual_available": False,
    }


def test_multiple_tasks_aggregate(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", builder=1000, reviewer=500, repair=0)
    _seed_task(tmp_path, "T002", builder=2000, reviewer=1500, repair=300)

    report = build_token_truth(str(tmp_path))

    assert report["builder_estimated_total"] == 3000
    assert report["reviewer_estimated_total"] == 2000
    assert report["repair_estimated_total"] == 300
    assert report["estimated_prompt_tokens"] == 5300
    assert report["estimated_total_tokens"] == 5300
    assert set(report["per_task"]) == {"T001", "T002"}


def test_actual_usage_populated(tmp_path: Path) -> None:
    _seed_task(tmp_path, "T001", provider_evidence={
        "builder_provider": "anthropic-api",
        "model": "claude-opus-4-8",
        "usage": {
            "input_tokens": 1200,
            "output_tokens": 340,
            "total_tokens": 1540,
            "cache_creation_input_tokens": 800,
            "cache_read_input_tokens": 200,
        },
    })

    report = build_token_truth(str(tmp_path))

    assert report["provider"] == "anthropic-api"
    assert report["model"] == "claude-opus-4-8"
    assert report["actual_available"] is True
    assert report["actual_prompt_tokens"] == 1200
    assert report["actual_completion_tokens"] == 340
    assert report["actual_total_tokens"] == 1540
    assert report["actual_cache_creation_tokens"] == 800
    assert report["actual_cache_read_tokens"] == 200
    assert report["missing_reason"] is None
    assert report["per_task"]["T001"]["actual_available"] is True


def test_empty_evidence_dir(tmp_path: Path) -> None:
    report = build_token_truth(str(tmp_path))

    assert report["actual_available"] is False
    assert report["estimated_prompt_tokens"] == 0
    assert report["per_task"] == {}
    assert report["provider"] == "claude-cli"
    assert report["provider_call_count"] == 0


def test_write_token_truth(tmp_path: Path) -> None:
    _seed_task(tmp_path)
    written: dict[str, str] = {}

    write_token_truth(str(tmp_path), written)

    out = tmp_path / "token_truth.json"
    assert out.exists()
    assert written["token_truth.json"] == str(out)
    data = json.loads(out.read_text())
    assert data["estimated_total_tokens"] == 13496


def test_write_token_truth_no_dir() -> None:
    written: dict[str, str] = {}
    write_token_truth("", written)
    assert written == {}


def test_no_cross_contamination(tmp_path: Path) -> None:
    """Estimated values must never appear in actual_* fields."""
    _seed_task(tmp_path, builder=9999, reviewer=7777, repair=3333)

    report = build_token_truth(str(tmp_path))

    assert report["actual_available"] is False
    assert report["actual_prompt_tokens"] is None
    assert report["actual_completion_tokens"] is None
    assert report["actual_total_tokens"] is None
    assert report["actual_cache_creation_tokens"] is None
    assert report["actual_cache_read_tokens"] is None

    assert report["estimated_prompt_tokens"] == 9999 + 7777 + 3333
    assert report["builder_estimated_total"] == 9999
    assert report["reviewer_estimated_total"] == 7777
    assert report["repair_estimated_total"] == 3333

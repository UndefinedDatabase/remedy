"""F1 (round 21) — the Root Manifest references only members that exist; no stale
review_zip_verification.json path remains."""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location("_brm", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_brm)


def test_no_stale_verification_reference_in_source():
    src = (REPO_ROOT / "scripts" / "build_review_manifest.py").read_text()
    # the only permitted occurrence is inside a comment noting the round-20 rename
    for line in src.splitlines():
        if "review_zip_verification.json" in line:
            assert line.lstrip().startswith("#"), line


def test_review_archive_names_the_expectation_member(tmp_path):
    ev = tmp_path / "ev"
    (ev / "task_runs" / "t1").mkdir(parents=True)
    (ev / "job_flow.json").write_text('{"job_id":"j","final_audit":{"status":"pass"}}')
    for f in ("manifest.json", "agent_run_trace.jsonl", "agent_run_trace_summary.json",
              "prompt_trace_summary.json", "command_transcript.json"):
        (ev / f).write_text("{}")
    for f in ("prompt_trace.jsonl", "prompt_trace_summary.json", "review.json", "repair_loop.json",
              "token_accounting.json", "provider_evidence.json"):
        (ev / "task_runs" / "t1" / f).write_text("{}")
    m = _brm.build_manifest(evidence_dir=str(ev), selection_mode="explicit",
                            selection_reason="test", candidate_count=0,
                            rejected_candidate_count=0, selected_mtime="")
    ra = m["current_evidence"]["review_archive"]
    assert ra["expectation"] == "evidence/current/review_zip_expectation.json"
    assert "verification" not in ra

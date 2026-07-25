"""
Focused tests for T005 — self-run observability index and the T003/T004 fixes.

Coverage:
  - Observability index over a complete evidence dir → valid JSON, all sections
  - Observability index over an incomplete/missing evidence dir → "absent"
    markers, still valid JSON
  - No absolute local paths leak into the index output
  - No raw full prompts in the index (only summaries with sha256 + token count)
  - Missing data is marked "absent" rather than hidden as empty/zero
  - The index is generated under the evidence dir bundled at
    evidence/current/self_run_observability_index.json in the review zip
  - T003: reviewer "pass" + findings is normalized to needs_repair
  - T004: command transcript mutation reporting agrees with the target guard's
    noise-exclusion policy for cache-only changes
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_observability_index import (
    ABSENT,
    build_observability_index,
)

# ---------------------------------------------------------------------------
# Synthetic evidence directory builder
# ---------------------------------------------------------------------------


def _write_complete_evidence(root: Path, *, raw_prompt: str = "RAW_SECRET_PROMPT_BODY") -> Path:
    """Create a complete, self-consistent evidence directory under ``root``."""
    ev = root / "remedy-job-evidence-deadbeef"
    ev.mkdir(parents=True)

    (ev / "job_flow.json").write_text(json.dumps({
        "command": "do.job-flow",
        "job_id": "JOB-1",
        "report": {
            "job_id": "JOB-1",
            "job_title": "Demo job",
            "tasks": [{
                "task_id": "T001",
                "title": "Do a thing",
                "status": "completed",
                "final_status": "staged_review_passed",
                "reviewer_verdict": "pass",
                "run_id": "RUN-1",
                "test_passed": True,
                "safe_diff_files": ["src/ok.py"],
            }],
        },
        "final_audit": {
            "status": "READY_FOR_APPROVAL",
            "promote_ready": True,
            "human_decision_required": True,
            "changed_files": ["src/ok.py"],
            "test_summary": ["pytest: passed"],
            "recommended_next_action": "remedy do job-promote JOB-1 --approve",
            "missing_observability_artifacts": [],
        },
    }))

    (ev / "agent_run_trace_summary.json").write_text(json.dumps({
        "total_events": 6,
        "event_counts": {"builder_prompt_created": 1},
        "tasks_traced": ["T001"],
        "providers": ["fake"],
        "max_round": 2,
        "has_builder_events": True,
        "has_reviewer_events": True,
        "has_repair_events": False,
        "has_final_audit": True,
        "changed_files": ["src/ok.py"],
    }))
    # Root artifacts referenced by data_availability.
    for name in ("manifest.json", "command_transcript.json",
                 "prompt_trace_summary.json", "tasks.json"):
        (ev / name).write_text("{}")
    (ev / "agent_run_trace.jsonl").write_text("")

    task_dir = ev / "task_runs" / "T001"
    task_dir.mkdir(parents=True)

    # prompt_trace.jsonl carries raw prompt text that must NEVER reach the index.
    (task_dir / "prompt_trace.jsonl").write_text("\n".join(json.dumps(r) for r in [
        {
            "round": 1, "role": "builder", "prompt_kind": "build",
            "provider": "fake", "prompt": raw_prompt,
            "prompt_sha256": "a" * 64, "prompt_chars": 1234,
            "prompt_tokens_estimated": 321,
            "context_categories": ["task"], "changed_files": ["src/ok.py"],
        },
        {
            "round": 1, "role": "reviewer", "prompt_kind": "review",
            "provider": "fake", "prompt": raw_prompt,
            "prompt_sha256": "b" * 64, "prompt_chars": 999,
            "prompt_tokens_estimated": 222,
        },
    ]) + "\n")

    (task_dir / "review.json").write_text(json.dumps({
        "final_verdict": "pass",
        "reviews": [{
            "round": 1, "kind": "initial",
            "findings": [{
                "id": "F1", "severity": "medium",
                "file": "src/ok.py", "summary": "tidy up",
            }],
        }],
    }))
    (task_dir / "repair_loop.json").write_text(json.dumps({
        "status": "resolved", "enabled": True,
        "repair_rounds_used": 1, "repair_rounds_allowed": 2,
        "open_findings": [], "resolved_findings": ["F1"],
        "final_reviewer_verdict": "pass",
        "decisions": [], "finding_status_map": [],
    }))
    (task_dir / "token_accounting.json").write_text(json.dumps({
        "kind": "estimated", "actual_tokens_available": False,
        "builder_prompt_tokens_estimated": 321,
        "reviewer_prompt_tokens_estimated": 222,
        "repair_prompt_tokens_estimated": 0,
        "task_tokens_estimated": 543,
        "token_note": "estimated only",
    }))
    (task_dir / "tests.txt").write_text("pytest: passed\n")
    (task_dir / "provider_evidence.json").write_text("{}")
    (task_dir / "summary.md").write_text("done\n")
    return ev


# Top-level keys every index must always carry (present or absent).
_REQUIRED_SECTIONS = (
    "index_kind", "index_version", "generated_at", "evidence_dir",
    "evidence_dir_present", "job_id", "tasks_generated", "tasks",
    "timeline_summary", "tokens", "changed_artifacts", "tests", "audit",
    "next_action", "data_availability",
)


# ---------------------------------------------------------------------------
# Complete evidence dir
# ---------------------------------------------------------------------------


class TestCompleteEvidence:
    def test_valid_json_all_sections_present(self, tmp_path):
        ev = _write_complete_evidence(tmp_path)
        index = build_observability_index(str(ev))

        # Round-trips through JSON without error → valid JSON.
        reparsed = json.loads(json.dumps(index))
        for key in _REQUIRED_SECTIONS:
            assert key in reparsed, f"missing top-level section {key!r}"

        assert reparsed["index_kind"] == "self_run_observability_index"
        assert reparsed["evidence_dir_present"] is True
        assert reparsed["job_id"] == "JOB-1"
        assert reparsed["tasks_generated"] == ["T001"]
        assert len(reparsed["tasks"]) == 1
        task = reparsed["tasks"][0]
        assert task["task_id"] == "T001"
        assert task["tests"]["result"] == "passed"
        assert reparsed["timeline_summary"]["status"] == "present"
        assert reparsed["audit"]["status"] == "READY_FOR_APPROVAL"

    def test_no_absolute_local_paths_in_output(self, tmp_path):
        ev = _write_complete_evidence(tmp_path)
        index = build_observability_index(str(ev))
        serialized = json.dumps(index)

        # The absolute evidence path must never appear; only its basename.
        assert str(ev) not in serialized
        assert str(tmp_path) not in serialized
        assert index["evidence_dir"] == "remedy-job-evidence-deadbeef"
        # data_availability references are bare relative names.
        for ref in index["data_availability"].values():
            assert ref == ABSENT or not ref.startswith("/")

    def test_absolute_paths_in_changed_files_dropped(self, tmp_path):
        ev = _write_complete_evidence(tmp_path)
        # Inject an absolute path into the task's changed-file list.
        jf = ev / "job_flow.json"
        data = json.loads(jf.read_text())
        data["report"]["tasks"][0]["safe_diff_files"] = ["/etc/passwd", "src/ok.py"]
        jf.write_text(json.dumps(data))

        index = build_observability_index(str(ev))
        serialized = json.dumps(index)
        assert "/etc/passwd" not in serialized
        assert index["tasks"][0]["changed_files"] == ["src/ok.py"]

    def test_no_raw_prompts_only_summaries(self, tmp_path):
        ev = _write_complete_evidence(tmp_path, raw_prompt="RAW_SECRET_PROMPT_BODY")
        index = build_observability_index(str(ev))
        serialized = json.dumps(index)

        # Raw prompt text must never be copied into the index.
        assert "RAW_SECRET_PROMPT_BODY" not in serialized

        prompts = index["tasks"][0]["prompts"]
        worker = prompts["worker_prompts"][0]
        # Only safe metadata: sha256 + token estimate, never the body.
        assert worker["prompt_sha256"] == "a" * 64
        assert worker["prompt_tokens_estimated"] == 321
        assert "prompt" not in worker


# ---------------------------------------------------------------------------
# Incomplete / missing evidence dir
# ---------------------------------------------------------------------------


class TestIncompleteEvidence:
    def test_missing_dir_still_valid_json_with_absent_markers(self, tmp_path):
        missing = tmp_path / "does-not-exist"
        index = build_observability_index(str(missing))

        reparsed = json.loads(json.dumps(index))  # valid JSON
        for key in _REQUIRED_SECTIONS:
            assert key in reparsed

        assert reparsed["evidence_dir_present"] is False
        assert reparsed["job_id"] == ABSENT
        assert reparsed["tasks_generated"] == ABSENT
        assert reparsed["tasks"] == []
        assert reparsed["next_action"] == ABSENT
        # Every root artifact is explicitly marked absent, not silently omitted.
        for ref in reparsed["data_availability"].values():
            assert ref == ABSENT

    def test_missing_artifacts_marked_absent_not_zero(self, tmp_path):
        # Evidence dir exists, but only job_flow lists a task — no task_runs/.
        ev = tmp_path / "remedy-job-evidence-partial"
        ev.mkdir()
        (ev / "job_flow.json").write_text(json.dumps({
            "report": {"job_id": "JOB-2", "tasks": [{"task_id": "T001"}]},
        }))

        index = build_observability_index(str(ev))
        json.loads(json.dumps(index))  # still valid JSON

        task = index["tasks"][0]
        # Missing token accounting → status marker, NOT a fabricated zero block.
        assert task["tokens"] == {"status": ABSENT}
        # Missing review/repair data → absent markers, not empty success.
        assert task["findings_opened"] == ABSENT
        assert task["repair_loop"] == {"status": ABSENT}
        assert task["prompts"]["status"] == ABSENT
        # Timeline summary absent rather than fabricated counts.
        assert index["timeline_summary"]["status"] == ABSENT
        assert index["audit"]["status"] == ABSENT


# ---------------------------------------------------------------------------
# T006 / packaging: index lands under evidence/current in the review zip
# ---------------------------------------------------------------------------


class TestIndexInReviewZip:
    @pytest.fixture
    def isolate_data(self, tmp_path, monkeypatch):
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        return data_dir

    def test_index_generated_under_evidence_current_prefix(
        self, capsys, isolate_data, tmp_path
    ):
        from apps.cli.grouped import main as grouped_main

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Demo\n")
        job_file = tmp_path / "job.md"
        job_file.write_text(
            "# Job: Index Zip\n\n## Task 1\nAdd a file.\n\nAcceptance:\n- file exists\n"
        )
        ev = tmp_path / "evidence"

        grouped_main([
            "do", "job-flow",
            "--job-file", str(job_file), "--repo", str(repo),
            "--builder", "fake", "--reviewer", "fake",
            "--out", str(ev), "--json",
        ])
        capsys.readouterr()

        idx = ev / "self_run_observability_index.json"
        assert idx.exists(), "index must be generated in the evidence dir"
        # Valid JSON with the expected kind.
        data = json.loads(idx.read_text())
        assert data["index_kind"] == "self_run_observability_index"

        # T003: index status must be persisted in an evidence artifact, not only
        # printed to stdout. job_flow.json is re-persisted after index build.
        flow = json.loads((ev / "job_flow.json").read_text())
        assert flow["observability_index_status"] == "generated"
        assert flow["observability_index_ref"] == "self_run_observability_index.json"
        assert "observability_index_error" not in flow

        # The review zip bundles the evidence dir under evidence/current/, so
        # the index ships at this canonical path.
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=str(ev))
        zip_prefix = manifest["current_evidence"]["zip_prefix"]
        assert zip_prefix == "evidence/current"
        assert f"{zip_prefix}/self_run_observability_index.json" == \
            "evidence/current/self_run_observability_index.json"


# ---------------------------------------------------------------------------
# T003: reviewer verdict normalization
# ---------------------------------------------------------------------------


class TestReviewerVerdictNormalization:
    def test_pass_with_findings_normalized_to_needs_repair(self):
        from packages.orchestration.pingpong_provider import (
            ReviewerOutput,
            ReviewFinding,
            normalize_reviewer_verdict,
        )
        out = ReviewerOutput(
            verdict="pass",
            findings=[ReviewFinding(id="F1", severity="high", summary="bug")],
            summary="looks fine",
        )
        result = normalize_reviewer_verdict(out)
        assert result.verdict == "needs_repair"
        assert result.verdict_normalized is True
        assert result.original_verdict == "pass"
        # The audit note explains the normalization.
        assert "normalized pass->needs_repair" in result.summary

    def test_pass_without_findings_not_normalized(self):
        from packages.orchestration.pingpong_provider import (
            ReviewerOutput,
            normalize_reviewer_verdict,
        )
        out = ReviewerOutput(verdict="pass", findings=[], summary="clean")
        result = normalize_reviewer_verdict(out)
        assert result.verdict == "pass"
        assert result.verdict_normalized is False
        assert result.original_verdict == ""


# ---------------------------------------------------------------------------
# T004: command transcript agrees with target guard on cache-only changes
# ---------------------------------------------------------------------------


class TestTranscriptTargetGuardConsistency:
    def test_cache_only_change_is_not_a_content_mutation(self, tmp_path):
        # The guard classifier and the transcript must agree: cache-only churn
        # is noise, never a target mutation.
        from packages.orchestration.pingpong_loop import (
            _check_target_mutation,
            _is_target_noise,
            _snapshot_target,
        )

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "real.py").write_text("x = 1\n")
        before = _snapshot_target(repo)

        # Add only volatile tool-cache files.
        cache = repo / ".pytest_cache" / "v"
        cache.mkdir(parents=True)
        (cache / "lastfailed").write_text("{}")
        (repo / "real.cpython-311.pyc").write_text("bytecode")

        meaningful, noise = _check_target_mutation(repo, before)
        assert meaningful == [], f"cache files must not be meaningful: {meaningful}"
        assert noise, "cache files must be reported as noise"
        assert all(_is_target_noise(n) for n in noise)

    def test_transcript_reports_noise_without_claiming_mutation(self, tmp_path):
        from apps.cli.commands.do_cmd import _persist_command_transcript

        ev = tmp_path / "evidence"
        _persist_command_transcript(
            job_id="JOB-1",
            evidence_out=str(ev),
            flow_result={"command": "do.job-flow", "final_audit": {"status": "READY"}},
            repo="/repo",
            started_at="2026-06-29T00:00:00+00:00",
            target_hash_before="0123456789abcdef",
            target_hash_after="0123456789abcdef",
            changed_content_files=[],
            ignored_noise_files=[".pytest_cache/v/lastfailed", "real.pyc"],
        )
        ct = json.loads((ev / "command_transcript.json").read_text())

        # Cache-only change → no content mutation, headline flag agrees.
        assert ct["target_content_mutated"] is False
        assert ct["target_repo_mutated"] is False
        assert ct["target_repo_mutated"] is ct["target_content_mutated"]
        # But the noise IS reported, not hidden.
        assert ct["target_noise_changed"] is True
        assert ct["ignored_noise_files"] == sorted(
            [".pytest_cache/v/lastfailed", "real.pyc"]
        )

    def test_operational_artifact_change_is_not_a_content_mutation(self, tmp_path):
        # Task 2: a Remedy operational artifact (e.g. remedy-review-*.zip) landing
        # in the target repo must be classified as operational, never as a content
        # mutation. The guard and the three-way classifier must agree.
        from packages.orchestration.pingpong_loop import (
            _check_target_mutation,
            _classify_target_changes,
            _is_operational_artifact,
            _snapshot_target,
        )

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "real.py").write_text("x = 1\n")
        before = _snapshot_target(repo)

        # Drop only an operational review zip at the repo root.
        zip_name = "remedy-review-20260101-000000.zip"
        (repo / zip_name).write_text("PK\x03\x04 fake zip bytes")

        content, operational, noise = _classify_target_changes(repo, before)
        assert content == [], f"operational artifact must not be content: {content}"
        assert zip_name in operational
        assert noise == []
        assert _is_operational_artifact(zip_name)

        # Two-way guard view: not meaningful, but reported as ignored.
        meaningful, ignored = _check_target_mutation(repo, before)
        assert meaningful == []
        assert zip_name in ignored

    def test_transcript_reports_operational_artifact_without_claiming_mutation(
        self, tmp_path
    ):
        from apps.cli.commands.do_cmd import _persist_command_transcript

        ev = tmp_path / "evidence"
        zip_name = "remedy-review-20260101-000000.zip"
        _persist_command_transcript(
            job_id="JOB-1",
            evidence_out=str(ev),
            flow_result={"command": "do.job-flow", "final_audit": {"status": "READY"}},
            repo="/repo",
            started_at="2026-06-29T00:00:00+00:00",
            target_hash_before="0123456789abcdef",
            target_hash_after="0123456789abcdef",
            changed_content_files=[],
            ignored_noise_files=[],
            ignored_operational_artifacts=[zip_name],
        )
        ct = json.loads((ev / "command_transcript.json").read_text())

        # Operational-only change → no content mutation; headline flag agrees.
        assert ct["target_content_mutated"] is False
        assert ct["target_repo_mutated"] is False
        assert ct["target_repo_mutated"] is ct["target_content_mutated"]
        # But the operational artifact IS reported, not hidden.
        assert ct["target_operational_artifacts_changed"] is True
        assert ct["ignored_operational_artifacts"] == [zip_name]

    def test_real_source_mutation_still_blocks(self, tmp_path):
        # A genuine source file change must be classified as content (meaningful),
        # never swallowed as operational or noise — the guard must still block.
        from packages.orchestration.pingpong_loop import (
            _check_target_mutation,
            _classify_target_changes,
            _snapshot_target,
        )

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "real.py").write_text("x = 1\n")
        before = _snapshot_target(repo)

        # Mutate an existing source file AND add a new one.
        (repo / "real.py").write_text("x = 2\n")
        (repo / "new_module.py").write_text("y = 3\n")

        content, operational, noise = _classify_target_changes(repo, before)
        assert "real.py" in content
        assert "new_module.py" in content
        assert operational == []
        assert noise == []

        meaningful, _ignored = _check_target_mutation(repo, before)
        assert "real.py" in meaningful
        assert "new_module.py" in meaningful

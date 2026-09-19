"""Tests for the cockpit bridge adapter and the review manifest's review state and subject."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestCockpitBridgeAdapter:
    def test_load_job_accepts_uuid(self):
        from packages.orchestration.ui_server import _load_job
        _, err = _load_job("not-a-valid-id-at-all!!!!")
        assert err is not None

    def test_load_job_returns_not_found_for_missing_plan(self):
        from packages.orchestration.ui_server import _load_job
        _, err = _load_job("deadbeef12345678")
        assert err is not None
        assert err[0] == 404

    def test_evidence_index_resolution(self, tmp_path):
        from packages.orchestration.ui_server import _resolve_evidence_dir
        result = _resolve_evidence_dir("nonexistent_job_id_12345678")
        assert result is None


class TestReviewStateExtraction:
    """The manifest reads the live ledger in the format the ledger is written in.

    `Gate: F<n> R<n> — ... VERDICT <X>.` records carry the verdicts and
    `- R-<n> — <Severity>...` lines register findings, closed by `Done: R-<n> — `
    lines; the state is read through `scripts/rotate_live_review.py`, the canonical
    reader, never through a private regex (T016 (b)).
    """

    def test_pass_verdict_review_ready(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review — F900 Synthetic\n\n"
            "## Findings\n\n"
            "- R-0001 — Low, A FINDING THAT WAS RESOLVED.\n\n"
            "Done: R-0001 — resolved at R2 by commit abc1234.\n\n"
            "Gate: F900 R2 — the F900 round 2 entry. VERDICT PASS. Re-derived.\n\n"
            "## Builder Handoff — PR #100 merged\n",
            encoding="utf-8",
        )
        (agent_dir / "plan.md").write_text(
            "# Plan — Steps 100-120\n\n## Goal\nDo stuff.\n"
        )
        from scripts.build_review_manifest import _extract_review_state
        rs = _extract_review_state()
        assert rs["latest_live_review_verdict"] == "PASS"
        assert rs["open_findings"] == []
        assert rs["builder_handoff_present"] is True
        assert rs["review_ready"] is True
        assert rs["plan_step_range"] == "100-120"
        assert rs["plan_goal_present"] is True

    def test_a_ledger_with_no_gate_record_has_an_absent_verdict(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review — F900 Synthetic\n\n## Findings\n", encoding="utf-8",
        )
        from scripts.build_review_manifest import _extract_review_state
        rs = _extract_review_state()
        assert rs["latest_live_review_verdict"] == "absent"
        assert rs["review_ready"] is False

    def test_open_findings_not_ready(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review — F900 Synthetic\n\n"
            "## Findings\n\n"
            "- R-9001 — High, SOMETHING STILL OPEN.\n\n"
            "Gate: F900 R1 — the F900 round 1 entry. VERDICT PASS.\n\n"
            "## Builder Handoff — PR merged\n",
            encoding="utf-8",
        )
        from scripts.build_review_manifest import _extract_review_state
        rs = _extract_review_state()
        assert rs["review_ready"] is False
        assert rs["open_findings"] == ["R-9001"]

    def test_the_last_gate_record_carries_the_verdict(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review — F900 Synthetic\n\n"
            "Gate: F900 R1 — the F900 round 1 entry. VERDICT FAIL. One red.\n\n"
            "Gate: F900 R2 — THE ROUND 1 VERDICT BOOKED INTO THE RECORD. "
            "VERDICT PASS_WITH_RISKS — the closure verdict.\n\n"
            "## Builder Handoff\n",
            encoding="utf-8",
        )
        from scripts.build_review_manifest import _extract_review_state
        rs = _extract_review_state()

        assert rs["latest_live_review_verdict"] == "PASS_WITH_RISKS"
        assert rs["open_findings"] == []
        assert rs["builder_handoff_present"] is True
        # ...and PASS_WITH_RISKS is honestly NOT review-ready: a human still has to sign
        # this off. The fix for that is a human, not a softer verdict.
        assert rs["review_ready"] is False

    def test_missing_handoff_not_ready(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review — F900 Synthetic\n\n"
            "Gate: F900 R1 — the F900 round 1 entry. VERDICT PASS.\n",
            encoding="utf-8",
        )
        from scripts.build_review_manifest import _extract_review_state
        rs = _extract_review_state()
        assert rs["review_ready"] is False
        assert rs["builder_handoff_present"] is False

    def test_the_manifest_reads_the_real_ledger_as_the_canonical_reader_does(self, monkeypatch):
        """T016 (b): fed the REAL `.agent/live_review.md`, the manifest's open set is
        the canonical reader's by distinct id, and its verdict is the last booked
        `Gate:` record's. The reader it replaced found no `## Verdict (reviewer-owned)`
        heading and no `### R-<n>` block there, and reported `absent` and `[]`."""
        from scripts.build_review_manifest import _extract_review_state
        from scripts.rotate_live_review import count_open_findings, open_finding_ids

        ledger = REPO_ROOT / ".agent" / "live_review.md"
        text = ledger.read_bytes().decode("utf-8")
        monkeypatch.chdir(REPO_ROOT)
        rs = _extract_review_state()

        assert rs["review_state_source"] == ".agent/live_review.md"
        assert len(rs["open_findings"]) == count_open_findings(text)
        assert rs["open_findings"] == open_finding_ids(text)
        # the last booked verdict, read off the last `Gate:` line independently
        last_gate = [line for line in text.split("\n") if line.startswith("Gate: ")][-1]
        booked = re.search(r"\bVERDICT (PASS_WITH_RISKS|PASS|FAIL|NEEDS_REPAIR|BLOCKED)\b", last_gate)
        assert booked is not None, last_gate[:120]
        assert rs["latest_live_review_verdict"] == booked.group(1)


class TestReviewSubjectClassification:
    def test_clean_main(self):
        from scripts.build_review_manifest import _classify_review_subject
        rs = _classify_review_subject("main", "abc123def", [], False, True)
        assert rs["kind"] == "clean_commit"
        assert "Clean main" in rs["human_summary"]

    def test_dirty_main(self):
        from scripts.build_review_manifest import _classify_review_subject
        rs = _classify_review_subject("main", "abc123def", ["M foo.py"], False, True)
        assert rs["kind"] == "dirty_working_tree"
        assert "Dirty" in rs["human_summary"]

    def test_feature_branch(self):
        from scripts.build_review_manifest import _classify_review_subject
        rs = _classify_review_subject("feature/foo", "abc123def", [], False, True)
        assert rs["kind"] == "feature_branch"

    def test_dirty_feature_branch(self):
        from scripts.build_review_manifest import _classify_review_subject
        rs = _classify_review_subject("feature/bar", "abc", ["M x.py"], True, True)
        assert rs["kind"] == "dirty_working_tree"
        assert rs["has_untracked_files"] is True

    def test_no_commits(self):
        from scripts.build_review_manifest import _classify_review_subject
        rs = _classify_review_subject("main", "unknown", [], False, False)
        assert rs["kind"] == "unknown"
        assert rs["degraded_metadata"] is True

    def test_master_treated_as_main(self):
        from scripts.build_review_manifest import _classify_review_subject
        rs = _classify_review_subject("master", "abc123def", [], False, True)
        assert rs["kind"] == "clean_commit"

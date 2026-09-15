"""Tests for the cockpit bridge adapter and the review manifest's review state and subject."""
from __future__ import annotations


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
    def test_pass_verdict_review_ready(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review\n\n"
            "## Verdict (reviewer-owned)\n"
            "**PASS** @ abc123\n\n"
            "---\n\n"
            "## Builder Handoff — PR #100 merged\n\n"
            "### Changed Files\n- foo.py\n"
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

    def test_pending_verdict_not_ready(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review\n\n"
            "## Verdict (reviewer-owned)\n"
            "*(pending reviewer)*\n"
        )
        from scripts.build_review_manifest import _extract_review_state
        rs = _extract_review_state()
        assert rs["review_ready"] is False

    def test_open_findings_not_ready(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review\n\n"
            "## Verdict (reviewer-owned)\n"
            "**PASS** @ abc123\n\n"
            "## Builder Handoff — PR merged\n\n"
            "### R-9001 Blocker — something\n"
            "Still open.\n"
        )
        from scripts.build_review_manifest import _extract_review_state
        rs = _extract_review_state()
        assert rs["review_ready"] is False
        assert "R-9001" in rs["open_findings"]

    def test_an_accepted_with_risks_closure_is_machine_readable(
        self, tmp_path, monkeypatch,
    ):
        """The exact shape of an accepted closure live review.

        The F007 closure package shipped a live review headed `## Verdict` with the
        verdict on the next line. `remedy integrity check` accepted that (it reads the
        line after any `## Verdict` heading), so the operator believed the verdict was
        machine-readable — but the review MANIFEST requires the reviewer-owned heading and
        a bold token, found neither, and packaged `latest_live_review_verdict: "absent"`.
        This pins the contract the manifest actually parses.
        """
        monkeypatch.chdir(tmp_path)
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review — Steps 6621-6660 — F007 closure\n\n"
            "## Verdict (reviewer-owned)\n"
            "**PASS_WITH_RISKS** — ACCEPTED (F007, external review, 2026-07-13; "
            "0 open findings)\n\n"
            "## Builder Handoff\n\n"
            "Operator closure by hand: no Builder, no provider call.\n"
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
            "# Live Review\n\n"
            "## Verdict (reviewer-owned)\n"
            "**PASS** @ abc123\n"
        )
        from scripts.build_review_manifest import _extract_review_state
        rs = _extract_review_state()
        assert rs["review_ready"] is False
        assert rs["builder_handoff_present"] is False


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

"""The agent state files, the job summary section and the autonomy readiness assessment.

These checks moved here from `tests/serve_http_handler/test_dashboard_contract.py` when the old cockpit's
dashboard was deleted (amend1015f D27): their subjects (the `.agent/` state files, `remedy job`'s
summary section, the shell-free subprocess rule and `autonomy_readiness`) all stay.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ORCH = REPO_ROOT / "packages" / "orchestration"
CLI_COMMANDS = REPO_ROOT / "apps" / "cli" / "commands"


class TestAgentStateFilesCurrentBranch:
    def test_context_md_references_current_branch(self):
        ctx = (REPO_ROOT / ".agent" / "context.md").read_text()
        assert "## Active Branch" in ctx
        assert "feature/" in ctx
        assert "steps-74_1-79" not in ctx
        assert "steps-91-100" not in ctx

    def test_plan_md_references_current_steps(self):
        plan = (REPO_ROOT / ".agent" / "plan.md").read_text()
        # Plan always references current or later steps
        assert "Steps" in plan
        assert "## Goal" in plan

    def test_no_stale_branch_references_in_context(self):
        ctx = (REPO_ROOT / ".agent" / "context.md").read_text()
        assert "feature/steps-74" not in ctx
        assert "PR #33" not in ctx


class TestJobSummaryCommandContract:
    def test_job_summary_command_exists(self):
        src = (CLI_COMMANDS / "job.py").read_text()
        assert "def _summary_section(job: JobPlan)" in src
        assert '("summary", _summary_section)' in src

    def test_job_summary_outputs_demo_mode(self):
        src = (CLI_COMMANDS / "job.py").read_text()
        assert "demo_mode" in src
        assert "data_honest" in src

    def test_no_shell_true_in_subprocess_calls(self):
        """Verify no subprocess calls use shell=True (comments mentioning it are OK)."""
        exempt = {"test_runner.py"}
        for f in ORCH.glob("*.py"):
            if f.name in exempt:
                continue
            src = f.read_text()
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.keyword) and node.arg == "shell":
                    if isinstance(node.value, ast.Constant) and node.value.value is True:
                        pytest.fail(f"{f.name} has shell=True in code")


class TestLiveReviewAndAgentStateRefs:
    def test_live_review_has_steps_section(self):
        review = (REPO_ROOT / ".agent" / "live_review.md").read_text()
        assert "Steps" in review

    def test_context_md_no_stale_steps(self):
        ctx = (REPO_ROOT / ".agent" / "context.md").read_text()
        # Context may reference 253-260 or later steps (261+)
        assert "Steps" in ctx
        assert "steps-74_1-79" not in ctx
        assert "Steps 91-100" not in ctx

    def test_plan_md_references_current_steps(self):
        plan = (REPO_ROOT / ".agent" / "plan.md").read_text()
        # Plan may reference 253-260 or later steps
        assert "Steps" in plan and "## Goal" in plan

    def test_live_review_canonical_path(self):
        """Review history must live in .agent/, not .data/."""
        agent_path = REPO_ROOT / ".agent" / "live_review.md"
        assert agent_path.exists(), "live_review.md must exist at .agent/live_review.md"


class TestAutonomyReadiness:
    def test_readiness_runtime_with_empty_job(self):
        """Runtime test: assess_job_readiness returns real report for minimal job."""
        from packages.orchestration.autonomy_readiness import (
            assess_job_readiness,
            export_readiness_json,
        )
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan(job_title="test-readiness", user_prompt="test")
        report = assess_job_readiness(job, [])
        data = export_readiness_json(report)

        assert data["version"] == 2
        assert data["scope"] == "job"
        assert "highest_eligible_level" in data
        assert isinstance(data["levels"], list)
        assert len(data["levels"]) == 8
        assert data["levels"][0]["eligible"] is True  # Level 0 always eligible
        assert "signals" in data

    def test_readiness_runtime_with_events(self):
        """Level 1 requires attached_repo + tasks."""
        from packages.orchestration.autonomy_readiness import assess_job_readiness
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry

        job = JobPlan(
            job_title="test-readiness",
            user_prompt="test",
            tasks=[TaskEntry(title="do thing")],
            metadata={"target_repo": "/tmp/fake"},
        )
        report = assess_job_readiness(job, [])
        # Level 1 (propose) should be eligible: has repo + tasks
        assert report.highest_eligible_level >= 1

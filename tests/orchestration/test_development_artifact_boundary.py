"""Guard tests: development artifact boundary enforcement.

Ensures product-facing modules do not depend on .agent/live_review.md.
Legacy development modules are explicitly whitelisted by relative path.
"""

from __future__ import annotations

import inspect
import re
from pathlib import Path

# Modules that must NEVER reference live_review.md or REMEDY_REVIEW_FILE.
_PRODUCT_MODULES = (
    "execution_approval_policy",
    "managed_builder_execution",
    "main_builder_adapter",
    "worker_facade_cmd",
)

# Legacy/development modules allowed to reference live_review.md.
# Uses relative paths from repo root — not bare filenames.
_ALLOWED_LEGACY = {
    "packages/orchestration/self_dogfood.py",
    "packages/orchestration/self_dogfood_execution.py",
    "packages/orchestration/overnight_executor.py",
    "packages/orchestration/overnight_mission.py",
    "packages/orchestration/builder_routing.py",
    "packages/orchestration/repair_loop_v2.py",
    "packages/orchestration/orchestrator_brain.py",
    "packages/orchestration/integrity_gate.py",
    "packages/orchestration/review_bundle.py",
    "apps/cli/commands/progress_cmd.py",
    "apps/cli/commands/feature_cmd.py",
}

_LIVE_REVIEW_PATTERN = re.compile(
    r"live_review\.md|REMEDY_REVIEW_FILE|read_agent_file\(['\"]live_review"
)

_ROOT = Path(__file__).resolve().parents[2]


class TestProductModulesNoLiveReview:
    """Product modules must not depend on .agent/live_review.md."""

    def test_execution_approval_policy(self):
        from packages.orchestration import execution_approval_policy as mod
        source = inspect.getsource(mod)
        assert not _LIVE_REVIEW_PATTERN.search(source), \
            "execution_approval_policy.py must not reference live_review.md"

    def test_managed_builder_execution(self):
        from packages.orchestration import managed_builder_execution as mod
        source = inspect.getsource(mod)
        assert not _LIVE_REVIEW_PATTERN.search(source), \
            "managed_builder_execution.py must not reference live_review.md"

    def test_main_builder_adapter(self):
        from packages.orchestration import main_builder_adapter as mod
        source = inspect.getsource(mod)
        assert not _LIVE_REVIEW_PATTERN.search(source), \
            "main_builder_adapter.py must not reference live_review.md"

    def test_worker_facade_cmd(self):
        from apps.cli.commands import worker_facade_cmd as mod
        source = inspect.getsource(mod)
        assert not _LIVE_REVIEW_PATTERN.search(source), \
            "worker_facade_cmd.py must not reference live_review.md"


class TestAllowlistCompleteness:
    """Every allowlisted path must exist in the repo."""

    def test_all_allowlisted_paths_exist(self):
        missing = [p for p in _ALLOWED_LEGACY if not (_ROOT / p).exists()]
        assert not missing, f"Stale allowlist entries (files not found): {missing}"


class TestWhitelistBoundary:
    """Source files referencing live_review.md must be in the allowed set."""

    def test_no_new_product_dependency(self):
        """Scan packages/ and apps/ for live_review references outside whitelist."""
        violations = []
        for search_dir in ("packages", "apps"):
            dir_path = _ROOT / search_dir
            if not dir_path.is_dir():
                continue
            for py_file in dir_path.rglob("*.py"):
                if py_file.name.startswith("__"):
                    continue
                try:
                    content = py_file.read_text(errors="replace")
                except OSError:
                    continue
                match = _LIVE_REVIEW_PATTERN.search(content)
                if match:
                    rel = str(py_file.relative_to(_ROOT))
                    if rel not in _ALLOWED_LEGACY:
                        violations.append(
                            f"{rel} (matched: {match.group()!r}) — "
                            "remove the dependency or add to _ALLOWED_LEGACY "
                            "if development-only"
                        )
        assert not violations, (
            "New live_review.md dependency in product code:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


class TestMissionReportNoDevTruth:
    """Mission report generation must not require .agent/live_review.md."""

    def test_dogfood_run_policy_section_no_live_review(self):
        from packages.orchestration import execution_approval_policy as pol_mod
        pol_source = inspect.getsource(pol_mod)
        assert not _LIVE_REVIEW_PATTERN.search(pol_source)


class TestDoctorCoreNoDevTruth:
    """Doctor core (in worker_facade_cmd) must not reference live_review.md."""

    def test_doctor_core_no_live_review(self):
        from apps.cli.commands import worker_facade_cmd as mod
        source = inspect.getsource(mod)
        assert not _LIVE_REVIEW_PATTERN.search(source), \
            "worker_facade_cmd.py must not reference live_review.md"


class TestApprovalCLINoDevTruth:
    """Approval CLI must rely on structured data, not .agent/live_review.md."""

    def test_approval_commands_no_live_review(self):
        from apps.cli.commands import worker_facade_cmd as mod
        source = inspect.getsource(mod)
        assert not _LIVE_REVIEW_PATTERN.search(source)


# ---------------------------------------------------------------------------
# Functional proofs: product paths work without .agent/ directory
# ---------------------------------------------------------------------------


class TestFunctionalNoAgent:
    """Product-facing paths must work without .agent/ directory."""

    def test_mission_morning_report_no_agent(self, tmp_path):
        """Morning report policy section works with structured data only."""
        from packages.orchestration.execution_approval_policy import (
            execution_approval_policy_summary,
        )
        summary = execution_approval_policy_summary(tmp_path)
        assert isinstance(summary, dict)
        assert "enabled_policy_count" in summary

    def test_worker_doctor_core_no_agent(self, tmp_path):
        """Doctor core import checks work without .agent/."""
        import importlib
        for mod_name in (
            "packages.orchestration.execution_approval_policy",
            "packages.orchestration.managed_builder_execution",
            "packages.orchestration.main_builder_adapter",
        ):
            mod = importlib.import_module(mod_name)
            assert mod is not None

    def test_approval_policy_evaluate_no_agent(self, tmp_path):
        """Policy evaluation works with structured tmp data, no .agent/."""
        from packages.orchestration.execution_approval_policy import (
            evaluate_execution_approval_policy,
        )
        decision = evaluate_execution_approval_policy(
            "nonexistent-session", "nonexistent-template", data_dir=tmp_path,
        )
        assert not decision.allowed
        assert decision.decision_code in ("missing_template", "missing_session")

    def test_review_bundle_structured_sections_no_agent(self, tmp_path):
        """Structured review bundle sections do not require .agent/live_review.md."""
        from packages.orchestration.execution_approval_policy import (
            execution_approval_policy_summary,
        )
        summary = execution_approval_policy_summary(tmp_path)
        assert isinstance(summary, dict)

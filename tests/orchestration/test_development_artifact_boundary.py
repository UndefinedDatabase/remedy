"""Guard tests: development artifact boundary enforcement.

Ensures product-facing modules do not depend on .agent/live_review.md.
Legacy development modules are explicitly whitelisted.
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
_ALLOWED_LEGACY = {
    "self_dogfood.py",
    "self_dogfood_execution.py",
    "overnight_executor.py",
    "overnight_mission.py",
    "builder_routing.py",
    "repair_loop_v2.py",
    "orchestrator_brain.py",
    "integrity_gate.py",
    "review_bundle.py",
    "progress_cmd.py",
    "feature_cmd.py",
}

_LIVE_REVIEW_PATTERN = re.compile(r"live_review\.md|REMEDY_REVIEW_FILE|read_agent_file\(['\"]live_review")


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


class TestWhitelistBoundary:
    """Source files referencing live_review.md must be in the allowed set."""

    def test_no_new_product_dependency(self):
        """Scan packages/ and apps/ for live_review references outside whitelist."""
        violations = []
        root = Path(__file__).resolve().parents[2]
        for search_dir in ("packages", "apps"):
            dir_path = root / search_dir
            if not dir_path.is_dir():
                continue
            for py_file in dir_path.rglob("*.py"):
                if py_file.name.startswith("__"):
                    continue
                try:
                    content = py_file.read_text(errors="replace")
                except OSError:
                    continue
                if _LIVE_REVIEW_PATTERN.search(content):
                    if py_file.name not in _ALLOWED_LEGACY:
                        violations.append(str(py_file.relative_to(root)))
        assert not violations, (
            f"New live_review.md dependency in product code: {violations}. "
            f"Add to _ALLOWED_LEGACY if development-only, or remove the reference."
        )


class TestMissionReportNoDevTruth:
    """Mission report generation must not require .agent/live_review.md."""

    def test_dogfood_run_policy_section_no_live_review(self):
        from packages.orchestration import dogfood_run as mod
        source = inspect.getsource(mod)
        # dogfood_run.py may have legacy self-dogfood references, but
        # the execution_approval_policy_summary import must not involve live_review
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

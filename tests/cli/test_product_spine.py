"""Product spine consistency tests — verify operator-facing commands,
stale doc strings, and fast test lane existence."""

from __future__ import annotations

import os
import stat
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Step 2671: operator-facing command entries exist + safe classification
# ---------------------------------------------------------------------------


class TestOperatorCommandsExist:
    def test_worker_facade_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {c.command_id for c in CATALOG}
        for cmd_id in ("worker.doctor", "worker.add", "worker.disable"):
            assert cmd_id in ids, f"{cmd_id} missing from catalog"

    def test_mission_facade_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {c.command_id for c in CATALOG}
        for cmd_id in ("mission.run", "mission.report"):
            assert cmd_id in ids, f"{cmd_id} missing from catalog"

    def test_doctor_core_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("doctor.core")
        assert cmd is not None
        assert cmd.action_class == "read_only"

    def test_worker_doctor_is_read_only(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("worker.doctor")
        assert cmd.action_class == "read_only"

    def test_mission_report_is_read_only(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("mission.report")
        assert cmd.action_class == "read_only"

    def test_mission_run_is_write_metadata(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("mission.run")
        assert cmd.action_class == "write_metadata"

    def test_all_operator_commands_have_handlers(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        for cmd_id in ("worker.doctor", "worker.add", "worker.disable",
                       "mission.run", "mission.report", "doctor.core",
                       "approval.policy-list", "approval.policy-show",
                       "approval.policy-enable", "approval.policy-disable",
                       "approval.policy-evaluate", "approval.policy-grant"):
            assert cmd_id in handlers, f"{cmd_id} missing from handlers"

    def test_approval_group_in_catalog(self):
        from apps.cli.command_catalog import GROUPS
        assert "approval" in GROUPS

    def test_approval_commands_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {c.command_id for c in CATALOG}
        for cmd_id in ("approval.policy-list", "approval.policy-show",
                       "approval.policy-enable", "approval.policy-disable",
                       "approval.policy-evaluate", "approval.policy-grant"):
            assert cmd_id in ids, f"{cmd_id} missing from catalog"


# ---------------------------------------------------------------------------
# Step 2670: stale command scanner
# ---------------------------------------------------------------------------


class TestStaleCommandScanner:
    def _read_doc(self, name: str) -> str:
        p = _ROOT / "docs" / name
        if not p.exists():
            return ""
        return p.read_text(encoding="utf-8", errors="replace")

    def test_no_stale_adapter_flag_in_quickstart(self):
        text = self._read_doc("simple-operator-quickstart-v0.md")
        assert "--adapter " not in text, \
            "Stale --adapter flag (should be --adapter-id)"

    def test_no_stale_adapter_flag_in_operator_path(self):
        text = self._read_doc("controlled-claude-code-operator-path-v0.md")
        assert "--adapter " not in text or "--adapter-id" in text, \
            "Stale --adapter flag without --adapter-id"

    def test_no_stale_self_proposal_list(self):
        text = self._read_doc("simple-operator-quickstart-v0.md")
        assert "remedy self proposal-list" not in text, \
            "Stale command: 'remedy self proposal-list' (should be 'self-repair')"

    def test_no_product_facing_dogfood_in_quickstart_main(self):
        text = self._read_doc("simple-operator-quickstart-v0.md")
        main = text.split("## Advanced commands")[0] if "## Advanced commands" in text else text
        assert "dogfood" not in main.lower(), \
            "Product-facing quickstart main section should not use 'dogfood'"

    def test_no_stale_self_proposal_list_in_mission_docs(self):
        text = self._read_doc("mission-run-loop-morning-report-v0.md")
        assert "remedy self proposal-list" not in text, \
            "Stale command in mission docs"

    def test_core_spine_doc_exists(self):
        p = _ROOT / "docs" / "core-product-spine-v0.md"
        assert p.exists(), "core-product-spine-v0.md must exist"


# ---------------------------------------------------------------------------
# Step 2672: fast lane self-test
# ---------------------------------------------------------------------------


class TestFastLaneSelfTest:
    def test_fast_lane_script_exists(self):
        p = _ROOT / "scripts" / "remedy_test_fast.sh"
        assert p.exists(), "scripts/remedy_test_fast.sh must exist"

    def test_fast_lane_is_executable(self):
        p = _ROOT / "scripts" / "remedy_test_fast.sh"
        st = os.stat(p)
        assert st.st_mode & stat.S_IXUSR, "remedy_test_fast.sh must be executable"

    def test_fast_lane_invokes_pytest_wrapper(self):
        p = _ROOT / "scripts" / "remedy_test_fast.sh"
        text = p.read_text(encoding="utf-8")
        assert "remedy_pytest.sh" in text, \
            "Fast lane must use remedy_pytest.sh wrapper"

    def test_fast_lane_no_provider_commands(self):
        p = _ROOT / "scripts" / "remedy_test_fast.sh"
        lines = p.read_text(encoding="utf-8").splitlines()
        code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
        code = "\n".join(code_lines).lower()
        for forbidden in ("claude ", "ollama ", "openai "):
            assert forbidden not in code, \
                f"Fast lane code must not reference provider: {forbidden}"

    def test_fast_lane_no_ui_build(self):
        p = _ROOT / "scripts" / "remedy_test_fast.sh"
        text = p.read_text(encoding="utf-8")
        for forbidden in ("npm ", "yarn ", "vite ", "webpack "):
            assert forbidden not in text.lower(), \
                f"Fast lane must not invoke UI build: {forbidden}"

    def test_fast_lane_no_heavy_runtime_smoke(self):
        p = _ROOT / "scripts" / "remedy_test_fast.sh"
        text = p.read_text(encoding="utf-8")
        heavy = [
            "test_worker_cli_runtime.py",
            "test_self_dogfood_execution_cli.py",
            "test_smoke_scripts.py",
            "test_overnight_executor_cli.py",
            "test_review_bundle_runtime.py",
        ]
        for name in heavy:
            assert name not in text, \
                f"Fast lane must not include heavy runtime file: {name}"

    def test_fast_lane_no_subprocess_files(self):
        p = _ROOT / "scripts" / "remedy_test_fast.sh"
        text = p.read_text(encoding="utf-8")
        subprocess_files = [
            "test_command_catalog.py",
            "test_contract_runtime.py",
            "test_config_cmd.py",
        ]
        for name in subprocess_files:
            assert name not in text, \
                f"Fast lane must not include subprocess file: {name}"

    def test_runtime_lane_script_exists(self):
        p = _ROOT / "scripts" / "remedy_test_runtime.sh"
        assert p.exists(), "scripts/remedy_test_runtime.sh must exist"

    def test_runtime_lane_is_executable(self):
        p = _ROOT / "scripts" / "remedy_test_runtime.sh"
        st = os.stat(p)
        assert st.st_mode & stat.S_IXUSR, "remedy_test_runtime.sh must be executable"

    def test_runtime_lane_uses_remedy_pytest(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "remedy_pytest.sh" in text, "Runtime lane must use remedy_pytest.sh"

    def test_runtime_lane_runs_suites_separately(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "for f in" in text or "for file in" in text, \
            "Runtime lane must run suites in separate invocations"

    def test_runtime_lane_node_isolation_for_subprocess_heavy(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "NODE_ISOLATED_FILES" in text, \
            "Runtime lane must define NODE_ISOLATED_FILES for per-node isolation"
        assert "node-isolated suite" in text, \
            "Runtime lane must label node-isolated suites"

    def test_runtime_lane_collect_only_for_nodes(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "--collect-only" in text, \
            "Runtime lane must use --collect-only to discover test nodes"

    def test_runtime_lane_review_bundle_is_node_isolated(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        node_section_start = text.index("NODE_ISOLATED_FILES")
        node_section_end = text.index(")", node_section_start)
        node_section = text[node_section_start:node_section_end]
        assert "test_review_bundle_runtime.py" in node_section, \
            "test_review_bundle_runtime.py must be in NODE_ISOLATED_FILES"

    def test_runtime_lane_node_start_end_markers(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "START node:" in text, \
            "Runtime lane must print START node marker"
        assert "END node:" in text, \
            "Runtime lane must print END node marker"

    def test_runtime_lane_no_tail_pipe_on_nodes(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "| tail -1" not in text, \
            "Runtime lane must not pipe node output to tail -1"

    def test_runtime_lane_node_failure_summary(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "Failed nodes:" in text, \
            "Runtime lane must print failed node summary"

    def test_runtime_lane_stale_process_check(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "stale" in text.lower(), \
            "Runtime lane must include stale process diagnostic"

    def test_runtime_lane_includes_review_bundle_runtime(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "test_review_bundle_runtime.py" in text

    def test_runtime_lane_includes_config_cmd(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "test_config_cmd.py" in text

    def test_runtime_lane_no_provider_invocation(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "provider" not in text.lower() or "does not" in text.lower()
        assert "claude" not in text.lower()
        assert "ollama" not in text.lower()

    def test_runtime_lane_no_ui_build(self):
        text = (_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "npm run build" not in text
        assert "vite build" not in text

    def test_fast_lane_includes_product_spine(self):
        p = _ROOT / "scripts" / "remedy_test_fast.sh"
        text = p.read_text(encoding="utf-8")
        assert "test_product_spine.py" in text, \
            "Fast lane must include product spine tests"

    def test_full_lane_script_exists(self):
        p = _ROOT / "scripts" / "remedy_test_full.sh"
        assert p.exists(), "scripts/remedy_test_full.sh must exist"

    def test_full_lane_is_executable(self):
        p = _ROOT / "scripts" / "remedy_test_full.sh"
        st = os.stat(p)
        assert st.st_mode & stat.S_IXUSR, "remedy_test_full.sh must be executable"

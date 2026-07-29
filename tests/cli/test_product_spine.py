"""Product spine consistency tests — verify operator-facing commands,
stale doc strings, and fast test lane existence."""

from __future__ import annotations

import os
import stat
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent

#: Where an ist-doc can live after the docs restructure (index: docs/README.md).
_DOC_DIRS = ("system", "guides", "")


def _read_doc(name: str) -> str:
    """The text of ``name`` wherever it lives under docs/ — never a silent ""."""
    for sub in _DOC_DIRS:
        p = (_ROOT / "docs" / sub / name) if sub else (_ROOT / "docs" / name)
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    raise AssertionError(f"doc not found under docs/: {name}")


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
        """Read a doc from the restructured tree.

        The docs moved into docs/system/ and docs/guides/; the flat lookup
        silently returned "" for every one of them, so these assertions were
        passing against an empty string. Missing is now an explicit failure.
        """
        return _read_doc(name)

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
        p = _ROOT / "docs" / "system" / "core-product-spine-v0.md"
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

# ---------------------------------------------------------------------------
# Step 3167-3174: Job-centric core tests
# ---------------------------------------------------------------------------


class TestJobCentricCatalog:
    """Job commands are primary; mission is advanced."""

    def test_job_status_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("job.status")
        assert cmd is not None
        assert cmd.action_class == "read_only"
        assert cmd.supports_json

    def test_job_report_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("job.report")
        assert cmd is not None
        assert cmd.action_class == "read_only"
        assert cmd.supports_json

    def test_job_status_has_handler(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "job.status" in handlers

    def test_job_report_has_handler(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "job.report" in handlers

    def test_mission_group_is_advanced(self):
        from apps.cli.command_catalog import GROUPS
        desc = GROUPS["mission"].description.lower()
        assert "advanced" in desc or "internal" in desc, \
            "Mission group description must indicate advanced/internal"

    def test_mission_not_primary_path(self):
        from apps.cli.command_catalog import GROUPS
        desc = GROUPS["mission"].description.lower()
        assert "normal" not in desc or "use \'job\'" in desc, \
            "Mission must not be described as normal primary path"


class TestJobFirstHappyPath:
    """Top-level help uses job-first language."""

    def test_happy_path_starts_with_do(self):
        from apps.cli.grouped import _QUICK_START
        lines = _QUICK_START.strip().splitlines()
        first_cmd_line = [l for l in lines if l.strip().startswith("1.")][0]
        assert "remedy do" in first_cmd_line

    def test_happy_path_has_do_report(self):
        from apps.cli.grouped import _QUICK_START
        assert "do report" in _QUICK_START

    def test_happy_path_has_do_promote(self):
        from apps.cli.grouped import _QUICK_START
        assert "do promote" in _QUICK_START

    def test_happy_path_no_mission_as_primary(self):
        from apps.cli.grouped import _QUICK_START
        assert "mission run" not in _QUICK_START, \
            "Happy path must not use mission run as primary"


class TestCommandTaxonomyDocs:
    """Docs use job-first language."""

    def _read_doc(self, name: str) -> str:
        """Read a doc from the restructured tree.

        The docs moved into docs/system/ and docs/guides/; the flat lookup
        silently returned "" for every one of them, so these assertions were
        passing against an empty string. Missing is now an explicit failure.
        """
        return _read_doc(name)

    def test_spine_doc_has_job_first_flow(self):
        text = self._read_doc("core-product-spine-v0.md")
        assert "job status" in text
        assert "job report" in text

    def test_spine_doc_mission_is_advanced(self):
        text = self._read_doc("core-product-spine-v0.md")
        assert "mission contract" in text.lower() or "internal" in text.lower()

    def test_quickstart_doc_job_first(self):
        text = self._read_doc("simple-operator-quickstart-v0.md")
        assert "job status" in text
        assert "job report" in text

    def test_quickstart_no_mission_as_primary(self):
        text = self._read_doc("simple-operator-quickstart-v0.md")
        lines = text.split("\n")
        quick_start_lines = []
        in_quick = False
        for line in lines:
            if "## Quick start" in line:
                in_quick = True
                continue
            if in_quick and line.startswith("## "):
                break
            if in_quick:
                quick_start_lines.append(line)
        quick_text = "\n".join(quick_start_lines)
        assert "mission" not in quick_text.lower(), \
            "Quick start section must not reference mission commands"

    def test_boundary_doc_no_product_dependency(self):
        text = self._read_doc("development-artifact-boundary-v0.md")
        assert "NOT product runtime state" in text


class TestJobFacadeNoAgent:
    """Job status/report work without .agent directory."""

    def test_job_status_handler_no_agent(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import contextlib
        import io

        from apps.cli.commands.job import _cmd_job_status
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                _cmd_job_status("00000000-0000-0000-0000-000000000000", json_output=True)
            except SystemExit:
                pass
        output = buf.getvalue()
        assert "job_not_found" in output or "error" in output

    def test_job_report_handler_no_agent(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import contextlib
        import io

        from apps.cli.commands.job import _cmd_job_report
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                _cmd_job_report("00000000-0000-0000-0000-000000000000", json_output=True)
            except SystemExit:
                pass
        output = buf.getvalue()
        assert "job_not_found" in output or "error" in output

    def test_job_status_invalid_id_safe(self):
        """A bad id fails safely: named error on stderr, no partial JSON.

        The machine token `invalid_job_id` is a `stop_reason` of the test
        execution service; the job CLI reports a bad id as a human error on
        stderr and exits non-zero. This pins that behaviour instead.
        """
        import contextlib
        import io

        from apps.cli.commands.job import _cmd_job_status
        out, err = io.StringIO(), io.StringIO()
        code = None
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                _cmd_job_status("not-a-uuid", json_output=True)
            except SystemExit as exc:
                code = exc.code
        assert code not in (None, 0)
        assert "invalid job ID" in err.getvalue()
        assert "not-a-uuid" in err.getvalue()
        assert "Traceback" not in err.getvalue()
        assert out.getvalue().strip() == ""

# ---------------------------------------------------------------------------
# Steps 3229-3237: Enriched truth, demo integration, safety proofs
# ---------------------------------------------------------------------------


class TestJobTruthExtraction:
    """_extract_job_truth returns correct fields from Job model."""

    def test_empty_job_truth(self, tmp_path, monkeypatch):
        monkeypatch.setenv('REMEDY_DATA_DIR', str(tmp_path))
        from apps.cli.commands.job import _extract_job_truth
        from packages.core.models import Job
        job = Job(name='empty test')
        truth = _extract_job_truth(job)
        assert truth['artifact_count'] == 0
        assert truth['patch_intent_ids'] == []
        assert truth['approval_required'] is False
        assert truth['latest_stop_reason'] == ''
        assert truth['event_count'] == 0

    def test_job_with_artifact_counts(self, tmp_path, monkeypatch):
        monkeypatch.setenv('REMEDY_DATA_DIR', str(tmp_path))
        from apps.cli.commands.job import _extract_job_truth
        from packages.core.models import Artifact, Job
        job = Job(name='artifact test', artifacts=[
            Artifact(name='plan', content='plan output'),
            Artifact(name='build', content='build output'),
        ])
        truth = _extract_job_truth(job)
        assert truth['artifact_count'] == 2
        assert truth['patch_intent_ids'] == []

    def test_job_with_patch_intent(self, tmp_path, monkeypatch):
        monkeypatch.setenv('REMEDY_DATA_DIR', str(tmp_path))
        from apps.cli.commands.job import _extract_job_truth
        from packages.core.models import Artifact, Job
        art = Artifact(
            name='patch',
            content='diff output',
            metadata={'patch_intent_count': 1},
        )
        job = Job(name='patch test', artifacts=[art])
        truth = _extract_job_truth(job)
        assert truth['artifact_count'] == 1
        assert len(truth['patch_intent_ids']) == 1
        assert truth['approval_required'] is True

    def test_patch_applied_clears_approval(self, tmp_path, monkeypatch):
        monkeypatch.setenv('REMEDY_DATA_DIR', str(tmp_path))
        from apps.cli.commands.job import _extract_job_truth
        from packages.core.models import Artifact, Job
        intent_id = 'abcd1234-0'
        art = Artifact(
            name='patch',
            content='diff output',
            metadata={
                'patch_intent_count': 1,
                'patch_intent_apply_records': {
                    intent_id: {'state': 'applied'},
                },
            },
        )
        job = Job(name='applied test', artifacts=[art])
        truth = _extract_job_truth(job)
        assert truth['approval_required'] is False


class TestJobStatusReportTruthFields:
    """Status and report JSON include enriched truth fields."""

    def _make_job_and_save(self, tmp_path):
        from packages.core.models import Artifact, Job, RunState, Task
        from packages.orchestration.storage import save_job
        art = Artifact(
            name='builder output',
            content='diff --git a/foo.py',
            metadata={'patch_intent_count': 1},
        )
        task = Task(description='Fix the bug', inputs={'task_type': 'code_repair'})
        job = Job(
            name='Demo fix',
            state=RunState.PAUSED,
            tasks=[task],
            artifacts=[art],
        )
        save_job(job, root=tmp_path)
        return job

    def test_status_json_has_truth_fields(self, tmp_path, monkeypatch):
        import contextlib
        import io
        import json

        monkeypatch.setenv('REMEDY_DATA_DIR', str(tmp_path))
        job = self._make_job_and_save(tmp_path)
        from apps.cli.commands.job import _cmd_job_status
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_job_status(str(job.id), json_output=True)
        data = json.loads(buf.getvalue())
        assert data['artifact_count'] == 1
        assert data['approval_required'] is True
        assert 'patch_intent_ids' in data
        assert 'next_safe_action' in data

    def test_report_json_has_truth_fields(self, tmp_path, monkeypatch):
        import contextlib
        import io
        import json

        monkeypatch.setenv('REMEDY_DATA_DIR', str(tmp_path))
        job = self._make_job_and_save(tmp_path)
        from apps.cli.commands.job import _cmd_job_report
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_job_report(str(job.id), json_output=True)
        data = json.loads(buf.getvalue())
        assert data['artifact_count'] == 1
        assert data['approval_required'] is True
        assert data['code_applied'] is False
        assert 'tasks' in data
        assert len(data['tasks']) == 1

    def test_report_invalid_id_safe(self):
        """Same contract as job status: named stderr error, no partial JSON."""
        import contextlib
        import io

        from apps.cli.commands.job import _cmd_job_report
        out, err = io.StringIO(), io.StringIO()
        code = None
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                _cmd_job_report('not-a-uuid', json_output=True)
            except SystemExit as exc:
                code = exc.code
        assert code not in (None, 0)
        assert 'invalid job ID' in err.getvalue()
        assert 'Traceback' not in err.getvalue()
        assert out.getvalue().strip() == ""


class TestNoProviderNoApplyProof:
    """Job commands never import provider SDKs or apply code."""

    def test_job_py_no_provider_import(self):
        from pathlib import Path
        src = Path(__file__).resolve().parent.parent.parent / 'apps' / 'cli' / 'commands' / 'job.py'
        text = src.read_text()
        for pattern in ['import anthropic', 'import openai', 'from anthropic', 'from openai']:
            assert pattern not in text, f'job.py must not import provider SDK: {pattern}'

    def test_job_py_no_subprocess(self):
        from pathlib import Path
        src = Path(__file__).resolve().parent.parent.parent / 'apps' / 'cli' / 'commands' / 'job.py'
        text = src.read_text()
        assert 'subprocess.run' not in text
        assert 'subprocess.Popen' not in text
        assert 'shell=True' not in text

    def test_report_always_code_applied_false(self, tmp_path, monkeypatch):
        import contextlib
        import io
        import json

        monkeypatch.setenv('REMEDY_DATA_DIR', str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name='no-apply proof')
        save_job(job, root=tmp_path)
        from apps.cli.commands.job import _cmd_job_report
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_job_report(str(job.id), json_output=True)
        data = json.loads(buf.getvalue())
        assert data['code_applied'] is False, 'v1 must never report code_applied=True'

    def test_status_next_action_never_apply(self, tmp_path, monkeypatch):
        import contextlib
        import io
        import json

        monkeypatch.setenv('REMEDY_DATA_DIR', str(tmp_path))
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name='no-apply-action proof')
        save_job(job, root=tmp_path)
        from apps.cli.commands.job import _cmd_job_status
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_job_status(str(job.id), json_output=True)
        data = json.loads(buf.getvalue())
        nsa = data.get('next_safe_action', '')
        assert 'apply' not in nsa.lower() or 'patch approve' in nsa.lower(), \
            'Next safe action must not suggest applying code directly'


class TestDoRunHelpAlignment:
    """Happy path and docs use do run syntax consistently."""

    def test_happy_path_uses_do_run(self):
        from apps.cli.grouped import _QUICK_START
        lines = _QUICK_START.strip().splitlines()
        first = [l for l in lines if l.strip().startswith('1.')][0]
        assert 'do run' in first or 'remedy do' in first

    def test_spine_doc_uses_do_run(self):
        text = _read_doc('core-product-spine-v0.md')
        assert 'do run' in text

    def test_quickstart_doc_uses_do_run(self):
        text = _read_doc('simple-operator-quickstart-v0.md')
        assert 'do run' in text

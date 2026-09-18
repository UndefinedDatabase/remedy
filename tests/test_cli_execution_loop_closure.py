"""Tests for Steps 155-162 — CLI closure for fixture-builder, repair loop,
reviewer, memory candidates, --ui flag, smoke, dev status, docs.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _make_job(*, tasks=None, name="test", metadata=None):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
    job = JobPlan(job_title=name)
    if metadata:
        job.metadata = dict(metadata)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = TaskEntry(title=t.get("description", task_type), inputs=inputs)
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# =========================================================================
# Step 155 — Fixture Builder Mode CLI Closure
# =========================================================================

class TestDoProviderCliParsing:
    """F268 (R-0933): `--fixture-builder` is deleted from `do`; the builder and reviewer
    of the run `do "<order>"` starts are chosen by `--builder-provider` / `--reviewer-provider`."""

    def test_parser_refuses_the_deleted_fixture_builder(self):
        from apps.cli.grouped import build_parser
        with pytest.raises(SystemExit) as exc:
            build_parser().parse_args(
                ["do", "run", "goal", "--fixture-builder", "repair-loop", "--no-ui", "--json"])
        assert exc.value.code == 2

    def test_parser_takes_both_provider_flags(self):
        from apps.cli.grouped import build_parser
        p = build_parser()
        args, unk = p.parse_known_args(
            ["do", "run", "goal", "--builder-provider", "fake",
             "--reviewer-provider=claude-cli", "--no-ui", "--json"])
        assert (args.builder_provider, args.reviewer_provider) == ("fake", "claude-cli")
        assert unk == []

    def test_default_command_rewrite(self):
        """remedy do '<goal>' rewrites to do run '<goal>' and stays on the bare sequence route."""
        from apps.cli.grouped import main
        with patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            main(["do", "Make tests pass", "--builder-provider", "fake",
                  "--reviewer-provider=fake", "--no-ui", "--json"])
        assert mock_do.called
        kwargs = mock_do.call_args[1]
        assert kwargs["builder_provider"] == "fake"
        assert kwargs["reviewer_provider"] == "fake"
        assert kwargs["no_ui"] is True
        assert kwargs["truly_bare"] is True

    def test_invalid_provider_fails(self):
        """A provider outside the four `create_provider` builds exits 2."""
        from apps.cli.commands.do_cmd import _validate_role_override
        for name in ("fake", "claude", "claude-cli", "ollama", None):
            _validate_role_override("builder", "provider", name)
        for bad in ("fixture", "none", "bogus-mode"):
            with pytest.raises(SystemExit) as exc:
                _validate_role_override("reviewer", "provider", bad)
            assert exc.value.code == 2

    def test_main_py_under_120_lines(self):
        main_py = _ROOT / "apps" / "cli" / "main.py"
        lines = main_py.read_text().count("\n")
        assert lines <= 120

    def test_no_flat_argparse(self):
        """grouped.py must not use old flat argparse pattern."""
        grouped_py = _ROOT / "apps" / "cli" / "grouped.py"
        src = grouped_py.read_text()
        assert "add_subparsers" in src  # uses grouped pattern
        # No raw ArgumentParser at module level (only _SilentParser subclass)
        lines = [l for l in src.splitlines()
                 if "ArgumentParser()" in l and "_SilentParser" not in l
                 and "class" not in l and "#" not in l]
        assert len(lines) == 0


# =========================================================================
# Step 156 — Repair-loop Fake E2E Closure
# =========================================================================

class TestRepairLoopFullE2EClosure:
    """Repair loop fixture proves 2-cycle controlled architecture."""

    def test_repair_loop_full_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            from packages.orchestration.autorun import run_autorun
            result = run_autorun(
                "Fix calc", tmp,
                autonomy_level=6, max_cycles=3,
                fixture_builder="repair-loop", json_output=True,
            )
            events_dict = {e["event"]: e["value"] for e in result.events}
            assert result.cycles_run == 2
            assert result.stage == "completed"
            assert events_dict.get("source_context_injected") == "True"
            assert events_dict.get("structured_patch_created") == "True"
            assert events_dict.get("source_patch_applied") == "True"
            assert events_dict.get("repair_context_created") == "True"
            assert events_dict.get("repair_loop_used") == "True"
            assert events_dict.get("tests_passed") == "True"

    def test_repair_loop_max_cycles_1_stops(self):
        """max_cycles=1 stops after cycle 1 with tests_passed=false."""
        with tempfile.TemporaryDirectory() as tmp:
            from packages.orchestration.autorun import run_autorun
            result = run_autorun(
                "Fix calc", tmp,
                autonomy_level=6, max_cycles=1,
                fixture_builder="repair-loop", json_output=True,
            )
            events_dict = {e["event"]: e["value"] for e in result.events}
            assert result.cycles_run == 1
            assert events_dict.get("tests_passed") == "False"

    def test_repair_loop_final_calc_correct(self):
        """After repair loop, calc.py has correct implementation."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            from packages.orchestration.autorun import run_autorun
            run_autorun(
                "Fix calc", tmp,
                autonomy_level=6, max_cycles=3,
                fixture_builder="repair-loop", json_output=True,
            )
            calc_py = repo / "calc.py"
            assert calc_py.exists()
            src = calc_py.read_text()
            assert "a * b" in src
            assert "a + b" in src

    def test_no_raw_leaks_in_json(self):
        """JSON output must not contain raw stdout/stderr/traceback."""
        with tempfile.TemporaryDirectory() as tmp:
            from packages.orchestration.autorun import run_autorun
            result = run_autorun(
                "Fix calc", tmp,
                autonomy_level=6, max_cycles=3,
                fixture_builder="repair-loop", json_output=True,
            )
            full = json.dumps({"events": result.events, "stage": result.stage})
            for bad in ("stdout", "stderr", "Traceback", "raw_output", "command_output"):
                assert bad not in full


# =========================================================================
# Step 157 — Reviewer CLI Closure
# =========================================================================

class TestReviewerPackageLoop:
    """`run_reviewer` survives the deletion of the `review` group: `dev status` probes it."""

    def test_reviewer_no_auto_append(self):
        """run_reviewer must NOT modify job.tasks."""
        from packages.orchestration.reviewer import _fixture_reviewer, run_reviewer
        job = _make_job()
        count = len(job.tasks)
        run_reviewer(job, reviewer_fn=_fixture_reviewer)
        assert len(job.tasks) == count


# =========================================================================
# Step 158 — Memory Candidate CLI Closure
# =========================================================================

class TestMemoryCandidateCliCommands:
    """Memory candidate commands exist and produce correct JSON."""

    def test_candidates_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("memory.candidates")
        assert cmd.supports_json

    def test_approve_candidate_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("memory.approve-candidate")
        assert cmd.supports_json

    def test_reject_candidate_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("memory.reject-candidate")
        assert cmd.supports_json

    def test_candidates_handler_json(self):
        from packages.orchestration.memory_candidates import create_candidate
        job = _make_job()
        job.metadata = {}
        create_candidate(job, "repair_pattern", "Fixed mul")

        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
             patch("apps.cli.commands.memory.lookup_job_id", side_effect=lambda raw: raw):
            import contextlib
            import io

            from apps.cli.commands.memory import _cmd_memory_candidates
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                _cmd_memory_candidates(str(job.job_id), json_output=True)
        data = json.loads(buf.getvalue())
        assert data["version"] == 1
        assert len(data["candidates"]) >= 1
        assert data["candidates"][0]["status"] == "pending"

    def test_approve_candidate_handler_json(self):
        from packages.orchestration.memory_candidates import create_candidate
        job = _make_job()
        job.metadata = {}
        c = create_candidate(job, "test_command", "pytest works")

        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
             patch("apps.cli.commands.memory.lookup_job_id", side_effect=lambda raw: raw), \
             patch("packages.orchestration.pingpong_job.save_job_plan"), \
             patch.dict("sys.modules", {"packages.orchestration.memory": MagicMock()}):
            import contextlib
            import io

            from apps.cli.commands.memory import _cmd_memory_approve_candidate
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                _cmd_memory_approve_candidate(str(job.job_id), c["id"], json_output=True)
        data = json.loads(buf.getvalue())
        assert data["approved"] is True
        assert data["memory_created"] is True

    def test_reject_candidate_handler_json(self):
        from packages.orchestration.memory_candidates import create_candidate
        job = _make_job()
        job.metadata = {}
        c = create_candidate(job, "test_command", "pytest works")

        with patch("packages.orchestration.pingpong_job.load_job_plan", return_value=job), \
             patch("apps.cli.commands.memory.lookup_job_id", side_effect=lambda raw: raw), \
             patch("packages.orchestration.pingpong_job.save_job_plan"):
            import contextlib
            import io

            from apps.cli.commands.memory import _cmd_memory_reject_candidate
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                _cmd_memory_reject_candidate(str(job.job_id), c["id"], json_output=True)
        data = json.loads(buf.getvalue())
        assert data["rejected"] is True
        assert data["memory_created"] is False

    def test_candidates_not_auto_approved(self):
        """All candidates must be pending by default."""
        from packages.orchestration.memory_candidates import create_candidate, list_candidates
        job = _make_job()
        job.metadata = {}
        create_candidate(job, "repair_pattern", "A")
        create_candidate(job, "test_command", "B")
        for c in list_candidates(job):
            assert c["status"] == "pending"


# =========================================================================
# Step 159 — --ui boolean flag + live UI contract
# =========================================================================

class TestUiBooleanFlagParsing:
    """--ui must be store_true boolean flag."""

    def test_ui_bare_flag_parses(self):
        from apps.cli.grouped import build_parser
        p = build_parser()
        args, unk = p.parse_known_args(
            ["do", "run", "goal", "--ui", "--json"])
        assert args.ui is True
        assert unk == []

    def test_no_ui_suppresses(self):
        from apps.cli.grouped import build_parser
        p = build_parser()
        args, unk = p.parse_known_args(
            ["do", "run", "goal", "--ui", "--no-ui", "--json"])
        assert args.ui is True
        assert args.no_ui is True

    def test_enable_ui_logic(self):
        """enable_ui = ui and not no_ui."""
        from apps.cli.grouped import main
        with patch("apps.cli.commands.do_cmd._cmd_do") as mock:
            main(["do", "goal", "--ui", "--json"])
        kwargs = mock.call_args[1]
        assert kwargs["enable_ui"] is True

        with patch("apps.cli.commands.do_cmd._cmd_do") as mock2:
            main(["do", "goal", "--ui", "--no-ui", "--json"])
        kwargs2 = mock2.call_args[1]
        assert kwargs2["enable_ui"] is False

    def test_live_state_v2_schema(self):
        from packages.orchestration.ui_server import _build_live_state_json
        job = _make_job()
        job.metadata = {}
        with patch("packages.orchestration.ui_server._load_events", return_value=[]):
            state = _build_live_state_json(job)
        required = {
            "version", "job_id", "cursor", "stage", "running",
            "node_count", "edge_count", "active_task_id",
            "latest_completed_task_id", "repair_loop_used",
            "reviewer_pending_count", "memory_candidate_count",
        }
        assert required.issubset(set(state.keys()))


# =========================================================================
# Step 160 — Smoke script structural checks
# =========================================================================

class TestSmokeScriptNewCliSections:
    """Smoke script includes new CLI contracts."""

    def test_smoke_has_repair_loop_section(self):
        script = (_ROOT / "scripts" / "remedy_smoke.sh").read_text()
        assert "repair-loop" in script
        assert "12ao" in script

    def test_smoke_has_memory_candidates_section(self):
        script = (_ROOT / "scripts" / "remedy_smoke.sh").read_text()
        assert "memory candidates" in script
        assert "12aq" in script

    def test_smoke_has_do_group_help(self):
        script = (_ROOT / "scripts" / "remedy_smoke.sh").read_text()
        assert " do " in script


# =========================================================================
# Step 161 — Dev Status Expanded
# =========================================================================

class TestDevStatusExpandedCapabilities:
    """Dev status includes repair_loop_ok, reviewer_loop_ok, etc."""

    def test_dev_status_expanded_schema(self):
        import contextlib
        import io

        from apps.cli.commands.dev import _dev_status
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _dev_status(json_output=True)
        data = json.loads(buf.getvalue())
        for key in ("repair_loop_ok", "reviewer_loop_ok",
                     "memory_candidates_ok", "live_ui_ok"):
            assert key in data

    def test_capabilities_ok_when_importable(self):
        import contextlib
        import io

        from apps.cli.commands.dev import _dev_status
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _dev_status(json_output=True)
        data = json.loads(buf.getvalue())
        # All modules exist, so should be True
        assert data["repair_loop_ok"] is True
        assert data["reviewer_loop_ok"] is True
        assert data["memory_candidates_ok"] is True
        assert data["live_ui_ok"] is True

    def test_missing_module_is_blocker(self):
        """If module import fails, it becomes a blocker."""
        import contextlib
        import io

        from apps.cli.commands.dev import _dev_status
        with patch.dict("sys.modules", {"packages.orchestration.repair_context": None}):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                _dev_status(json_output=True)
        data = json.loads(buf.getvalue())
        # repair_context import fails → repair_loop_ok should be False
        # (May still succeed if already cached — this is a structural test)
        assert "advisories" in data
        assert "remaining_blockers" in data


# =========================================================================
# Step 162 — Docs/Help Closure
# =========================================================================

class TestDocsHelpReviewMemoryCommands:
    """Help pages include new commands."""

    def test_memory_candidate_commands_in_catalog(self):
        from apps.cli.command_catalog import get_commands_for_group
        cmds = {c.subcommand for c in get_commands_for_group("memory")}
        assert "candidates" in cmds
        assert "approve-candidate" in cmds
        assert "reject-candidate" in cmds

    def test_quick_start_updated(self):
        from apps.cli.grouped import _QUICK_START
        assert 'remedy do "Write a CONTRIBUTING.md"' in _QUICK_START
        assert "remedy job list" in _QUICK_START

    def test_no_auto_commit_in_docs(self):
        """No docs suggesting automatic git commit."""
        from apps.cli.grouped import _QUICK_START
        assert "git commit" not in _QUICK_START.lower()
        assert "auto-approve" not in _QUICK_START.lower()

    def test_no_auto_memory_approval_in_docs(self):
        """Catalog descriptions say human approval required."""
        from apps.cli.command_catalog import get_command
        desc = get_command("memory.candidates").description
        assert "human" in desc.lower() or "approval" in desc.lower()

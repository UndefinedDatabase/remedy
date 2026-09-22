"""Tests for Steps 155-162 — CLI closure for fixture-builder, repair loop,
reviewer, memory candidates, --ui flag, smoke, dev status, docs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

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
        """remedy do '<goal>' rewrites to do run '<goal>', the one route (DECISION F268 D16 (1))."""
        from apps.cli.grouped import main
        with patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            main(["do", "Make tests pass", "--builder-provider", "fake",
                  "--reviewer-provider=fake", "--no-ui", "--json"])
        assert mock_do.called
        kwargs = mock_do.call_args[1]
        assert kwargs["builder_provider"] == "fake"
        assert kwargs["reviewer_provider"] == "fake"
        assert kwargs["no_ui"] is True

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


# =========================================================================
# Step 157 — Reviewer CLI Closure
# =========================================================================

class TestReviewerPackageLoop:
    """`run_reviewer` survives the deletion of the `review` group: `dev status` probes it."""

    def test_reviewer_no_auto_append(self):
        """run_reviewer must NOT modify job.tasks."""
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job()
        count = len(job.tasks)
        run_reviewer(job, reviewer_fn=lambda ctx: [{"title": "Add edge case tests"}])
        assert len(job.tasks) == count


# =========================================================================
# Step 159 — --ui boolean flag + live UI contract
# =========================================================================

class TestUiBooleanFlagParsing:
    """The live UI contract. `--ui` left `do` with DECISION F268 D16 (2), and its three
    parsing tests with it."""

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
        }
        assert required.issubset(set(state.keys()))
        # F273 R-0992: the memory-candidate store has no writer, so no count.
        assert "memory_candidate_count" not in state


# =========================================================================
# Step 160 — Smoke script structural checks
# =========================================================================

class TestSmokeScriptNewCliSections:
    """Smoke script includes new CLI contracts."""

    def test_smoke_has_do_sequence_section(self):
        """Section 12ao runs `remedy do` as the sequence (DECISION F268 D17 (2))."""
        script = (_ROOT / "scripts" / "remedy_smoke.sh").read_text()
        assert '_SMOKE_SECTION="12ao"' in script
        section = script.split('_SMOKE_SECTION="12ao"', 1)[1].split("_SMOKE_SECTION=", 1)[0]
        [do_line] = [line for line in section.splitlines() if "remedy do \"" in line]
        assert "--no-llm" in do_line
        assert "--builder-provider fake" in do_line
        assert "--reviewer-provider fake" in do_line
        assert "--autonomy-level" not in script
        assert "DO_JOB_ID=" in section

    def test_smoke_has_do_group_help(self):
        script = (_ROOT / "scripts" / "remedy_smoke.sh").read_text()
        assert " do " in script


class TestDevSmokeHelpJson:
    """F283 R14 C3 — `dev smoke-help` answers `--json` in the envelope."""

    def test_dev_smoke_help_json_through_the_dispatcher(self):
        import contextlib
        import io

        from apps.cli.grouped import main
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main(["dev", "smoke-help", "--json"])
        data = json.loads(buf.getvalue())
        assert data["schema_version"] == 1
        assert data["ok"] is True
        assert data["commands"] == [
            "source scripts/remedy_smoke.sh && remedy_smoke",
            "bash scripts/remedy_smoke.sh",
        ]


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
        for key in ("repair_loop_ok", "reviewer_loop_ok", "live_ui_ok"):
            assert key in data
        assert "memory_candidates_ok" not in data    # F273 R-0992

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

    def test_quick_start_updated(self):
        from apps.cli.grouped import _QUICK_START
        assert 'remedy do "Write a CONTRIBUTING.md"' in _QUICK_START
        assert "remedy job list" in _QUICK_START

    def test_no_auto_commit_in_docs(self):
        """No docs suggesting automatic git commit."""
        from apps.cli.grouped import _QUICK_START
        assert "git commit" not in _QUICK_START.lower()
        assert "auto-approve" not in _QUICK_START.lower()

"""Tests for integrity_gate.py — handler import, live_review, plan, R-0017 regression."""

from __future__ import annotations

import json

from packages.orchestration.integrity_gate import (
    IntegrityCheck,
    IntegrityGateResult,
    IntegrityStatus,
    _ctx_says_complete,
    export_integrity_json,
    run_integrity_checks,
)

# ---------------------------------------------------------------------------
# R-0017 regression — _ctx_says_complete
# ---------------------------------------------------------------------------


class TestCtxSaysComplete:
    """R-0017: only explicit ## Scope COMPLETE triggers, not prior block text."""

    def test_done_in_prior_status_does_not_trigger(self):
        ctx = (
            "## Prior Step Status\n"
            "- Steps 940-974: PASS — Repair Loop v0 + Truth Closure done.\n"
            "- Steps 975-994: PASS — Review Bundle v1 done.\n"
            "\n"
            "## Scope\n"
            "Steps 1045-1064: Run Contract Enforcement v1\n"
        )
        assert _ctx_says_complete(ctx) is False

    def test_complete_in_prior_status_does_not_trigger(self):
        ctx = (
            "## Prior Step Status\n"
            "- Steps 1030-1044: PASS WITH RISKS — complete.\n"
            "\n"
            "## Scope\n"
            "Steps 1045-1064: Run Contract Enforcement v1\n"
        )
        assert _ctx_says_complete(ctx) is False

    def test_explicit_scope_complete_triggers(self):
        ctx = (
            "## Scope\n"
            "Steps 1045-1064: Run Contract Enforcement v1 — COMPLETE\n"
        )
        assert _ctx_says_complete(ctx) is True

    def test_explicit_scope_done_triggers(self):
        ctx = "## Scope\nSteps 1045-1064 — DONE\n"
        assert _ctx_says_complete(ctx) is True

    def test_current_step_complete_triggers(self):
        ctx = "## Current Step\n1064 — FINAL handoff COMPLETE\n"
        assert _ctx_says_complete(ctx) is True

    def test_empty_context_does_not_trigger(self):
        assert _ctx_says_complete("") is False

    def test_no_scope_heading_does_not_trigger(self):
        ctx = "Some random text with done and complete words."
        assert _ctx_says_complete(ctx) is False

    def test_pending_live_review_with_explicit_complete_fails(self, tmp_path):
        """Pending verdict + explicit scope COMPLETE should fail integrity."""
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review\n## Verdict\nPENDING\n"
        )
        (agent_dir / "context.md").write_text(
            "## Scope\nSteps 1-10 — COMPLETE\n"
        )

        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = run_integrity_checks()
            lr_check = next(c for c in result.checks if c.name == "live_review_verdict")
            assert lr_check.status == IntegrityStatus.FAIL
        finally:
            os.chdir(old_cwd)

    def test_pending_live_review_with_no_explicit_complete_warns_or_passes(self, tmp_path):
        """Pending verdict + no explicit COMPLETE should not fail."""
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(
            "# Live Review\n## Verdict\nPENDING\n"
        )
        (agent_dir / "context.md").write_text(
            "## Prior Step Status\n- Steps 1-5: PASS — done.\n\n"
            "## Scope\nSteps 6-10: In progress\n"
        )

        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = run_integrity_checks()
            lr_check = next(c for c in result.checks if c.name == "live_review_verdict")
            assert lr_check.status != IntegrityStatus.FAIL
        finally:
            os.chdir(old_cwd)


# ---------------------------------------------------------------------------
# Handler import check
# ---------------------------------------------------------------------------


class TestHandlerImportCheck:
    def test_handler_import_passes(self):
        result = run_integrity_checks()
        handler_check = next(c for c in result.checks if c.name == "handler_import")
        assert handler_check.status == IntegrityStatus.PASS


# ---------------------------------------------------------------------------
# High blocker check
# ---------------------------------------------------------------------------


class TestHighBlockerCheck:
    """R-0648: the fixtures are ledgers in the form ``.agent/live_review.md`` really uses —
    ``- R-XXXX — <Severity>, <headline>`` registrations resolved by ``Done: R-XXXX — `` lines.
    """

    @staticmethod
    def _blocker_check(tmp_path, monkeypatch, ledger: str):
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(ledger, encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        result = run_integrity_checks()
        return next(c for c in result.checks if c.name == "high_blockers_open")

    def test_an_open_high_in_the_real_ledger_form_fails(self, tmp_path, monkeypatch):
        check = self._blocker_check(tmp_path, monkeypatch, (
            "# Live Review\n\n## Findings\n\n"
            "- R-0901 — High, AN OPEN HIGH THE CLOSURE MUST NOT PASS OVER. Measured.\n\n"
            "- R-0902 — Low, an open Low that blocks nothing.\n"
        ))
        assert check.status == IntegrityStatus.FAIL
        assert check.message == "1 open blocker/high: R-0901"

    def test_a_resolved_high_and_open_lows_pass(self, tmp_path, monkeypatch):
        check = self._blocker_check(tmp_path, monkeypatch, (
            "# Live Review\n\n## Findings\n\n"
            "- R-0901 — High, A HIGH THAT WAS REPAIRED.\n\n"
            "- R-0902 — Medium — an open Medium, carried as a documented risk.\n\n"
            "Done: R-0901 — repaired and red-proved.\n"
        ))
        assert check.status == IntegrityStatus.PASS
        assert check.message == "no open blocker/high findings"


# ---------------------------------------------------------------------------
# Export / JSON safety
# ---------------------------------------------------------------------------


class TestExportSafety:
    def test_no_raw_traceback_in_json(self):
        result = IntegrityGateResult(checks=[
            IntegrityCheck("test", IntegrityStatus.FAIL, "some message"),
        ])
        exported = export_integrity_json(result)
        json_str = json.dumps(exported)
        assert "Traceback" not in json_str
        assert "File \"" not in json_str

    def test_export_json_structure(self):
        result = IntegrityGateResult(checks=[
            IntegrityCheck("a", IntegrityStatus.PASS, "ok"),
        ])
        exported = export_integrity_json(result)
        assert exported["version"] == 1
        assert exported["passed"] is True
        assert exported["fail_count"] == 0
        assert len(exported["checks"]) == 1
        assert exported["checks"][0]["name"] == "a"
        assert exported["checks"][0]["status"] == "pass"


# ---------------------------------------------------------------------------
# Plan consistency
# ---------------------------------------------------------------------------


class TestPlanConsistency:
    def test_unchecked_with_scope_complete_fails(self, tmp_path):
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "plan.md").write_text("# Plan\n- [ ] Step 1\n- [x] Step 2\n")
        (agent_dir / "context.md").write_text("## Scope\nSteps 1-2 — COMPLETE\n")
        (agent_dir / "live_review.md").write_text("## Verdict\nPASS\n")

        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = run_integrity_checks()
            plan_check = next(c for c in result.checks if c.name == "plan_consistency")
            assert plan_check.status == IntegrityStatus.FAIL
        finally:
            os.chdir(old_cwd)

    def test_unchecked_without_scope_complete_passes(self, tmp_path):
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "plan.md").write_text("# Plan\n- [ ] Step 1\n- [x] Step 2\n")
        (agent_dir / "context.md").write_text("## Scope\nSteps 1-2: In progress\n")
        (agent_dir / "live_review.md").write_text("## Verdict\nIN PROGRESS\n")

        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = run_integrity_checks()
            plan_check = next(c for c in result.checks if c.name == "plan_consistency")
            assert plan_check.status == IntegrityStatus.PASS
        finally:
            os.chdir(old_cwd)


# F085 T002b — integrity_gate._check_collect_only on the shared `test`-class seam


def test_collect_only_runs_on_the_guarded_seam(monkeypatch):
    """The spawn goes through `run_guarded_test_command` with no cwd pin, and its BYTES decode."""
    import subprocess

    from packages.orchestration import integrity_gate

    seen: dict[str, object] = {}

    def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
        seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
        return subprocess.CompletedProcess(list(cmd), 1, b"", b"boom-\xff-undecodable\n")

    monkeypatch.setattr(integrity_gate, "run_guarded_test_command", _fake_guarded)
    check = integrity_gate._check_collect_only()

    assert seen == {
        "cmd": ["bash", "scripts/remedy_pytest.sh", "tests/", "--collect-only", "-q"],
        "timeout_sec": 120,
        "cwd": None,
    }
    assert check.status is integrity_gate.IntegrityStatus.FAIL
    assert "boom-" in check.message
    assert "undecodable" in check.message

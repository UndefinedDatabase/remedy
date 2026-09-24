"""Tests for integrity_gate.py — handler import, live_review, plan, R-0017 regression."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from packages.orchestration import integrity_gate
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


class TestLiveReviewVerdictReadsTheLastGateRecord:
    """R-0998: the verdict is the last ``Gate:`` record's, read by the ledger's own reader."""

    _COMPLETE = "## Scope\nF999 — COMPLETE\n"
    _OPEN = "## Scope\nF999 — in progress\n"

    @staticmethod
    def _verdict_check(tmp_path, monkeypatch, ledger: str, context: str):
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "live_review.md").write_text(ledger, encoding="utf-8")
        (agent_dir / "context.md").write_text(context, encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        result = run_integrity_checks()
        return next(c for c in result.checks if c.name == "live_review_verdict")

    def test_a_last_gate_reading_fail_under_a_complete_context_fails(self, tmp_path, monkeypatch):
        check = self._verdict_check(tmp_path, monkeypatch, (
            "# Live Review\n\n## Findings\n\n"
            "Gate: F999 R1 — the F999 round 1 entry. VERDICT PASS, re-derived.\n\n"
            "Gate: F999 R2 — the F999 round 2 entry. VERDICT FAIL, two findings.\n"
        ), self._COMPLETE)
        assert check.status == IntegrityStatus.FAIL
        assert check.message == "Context says complete but the last Gate verdict is FAIL"

    def test_a_quoted_verdict_heading_inside_a_finding_changes_nothing(self, tmp_path, monkeypatch):
        check = self._verdict_check(tmp_path, monkeypatch, (
            "# Live Review\n\n## Findings\n\n"
            "- R-0901 — Low, a finding that quotes the retired heading:\n"
            "## Verdict\nFAIL\n\n"
            "Gate: F999 R1 — the F999 round 1 entry. VERDICT PASS_WITH_RISKS, one risk.\n"
        ), self._COMPLETE)
        assert check.status == IntegrityStatus.PASS
        assert check.message == "last Gate verdict PASS_WITH_RISKS"

    def test_a_fail_before_the_last_gate_record_does_not_count(self, tmp_path, monkeypatch):
        check = self._verdict_check(tmp_path, monkeypatch, (
            "# Live Review\n\n## Findings\n\n"
            "Gate: F999 R1 — the F999 round 1 entry. VERDICT FAIL, repaired next.\n\n"
            "Gate: F999 R2 — the F999 round 2 entry. VERDICT PASS, the repair held.\n"
        ), self._COMPLETE)
        assert check.status == IntegrityStatus.PASS
        assert check.message == "last Gate verdict PASS"

    def test_a_fail_mid_feature_is_reported_but_does_not_fail(self, tmp_path, monkeypatch):
        check = self._verdict_check(tmp_path, monkeypatch, (
            "# Live Review\n\n## Findings\n\n"
            "Gate: F999 R1 — the F999 round 1 entry. VERDICT FAIL, a repair round follows.\n"
        ), self._OPEN)
        assert check.status == IntegrityStatus.PASS
        assert check.message == "last Gate verdict FAIL"

    def test_no_gate_record_warns_and_fails_under_a_complete_context(self, tmp_path, monkeypatch):
        ledger = "# Live Review\n\n## Findings\n\n- R-0901 — Low, an open Low.\n"
        check = self._verdict_check(tmp_path, monkeypatch, ledger, self._OPEN)
        assert check.status == IntegrityStatus.WARN
        assert check.message == "no verdict found: last Gate record absent"
        (tmp_path / ".agent" / "context.md").write_text(self._COMPLETE, encoding="utf-8")
        result = run_integrity_checks()
        check = next(c for c in result.checks if c.name == "live_review_verdict")
        assert check.status == IntegrityStatus.FAIL
        assert check.message == "Context says complete but the last Gate verdict is absent"

    def test_an_unloadable_ledger_reader_fails_the_check(self, tmp_path, monkeypatch):
        from packages.orchestration import integrity_gate

        def _broken():
            raise ImportError("no ledger reader")

        monkeypatch.setattr(integrity_gate, "_load_ledger_reader", _broken)
        check = self._verdict_check(tmp_path, monkeypatch, (
            "Gate: F999 R1 — the F999 round 1 entry. VERDICT PASS.\n"
        ), self._OPEN)
        assert check.status == IntegrityStatus.FAIL
        assert check.message == "ledger reader failed: ImportError: no ledger reader"


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


# F283 R17 C6 — `integrity check --json` answers in the envelope (D10)


class TestIntegrityCheckJSONEnvelope:
    """`apps.cli.commands.integrity_cmd._cmd_integrity_check` under `--json`:
    a passing gate answers `emit_ok`, and a failing one answers ONE
    `integrity_failed` failure envelope (D10 (3)) rather than a raw document
    followed by a bare `sys.exit(1)`."""

    @staticmethod
    def _args(*, collect_only: bool = False) -> argparse.Namespace:
        return argparse.Namespace(json=True, collect_only=collect_only)

    def test_a_passing_gate_answers_emit_ok(self, monkeypatch, capsys):
        from apps.cli.commands import integrity_cmd

        result = IntegrityGateResult(checks=[IntegrityCheck("a", IntegrityStatus.PASS, "ok")])
        monkeypatch.setattr(integrity_gate, "run_integrity_checks", lambda **kw: result)
        integrity_cmd._cmd_integrity_check(self._args())
        body = json.loads(capsys.readouterr().out)
        assert body["schema_version"] == 1 and body["ok"] is True
        assert body["passed"] is True
        assert body["fail_count"] == 0

    def test_a_failing_gate_answers_one_failure_envelope_and_exits_1(self, monkeypatch, capsys):
        from apps.cli.commands import integrity_cmd

        result = IntegrityGateResult(checks=[IntegrityCheck("a", IntegrityStatus.FAIL, "boom")])
        monkeypatch.setattr(integrity_gate, "run_integrity_checks", lambda **kw: result)
        with pytest.raises(SystemExit) as caught:
            integrity_cmd._cmd_integrity_check(self._args())
        assert caught.value.code == 1
        body = json.loads(capsys.readouterr().out)
        assert body["schema_version"] == 1 and body["ok"] is False
        assert body["error"] == "integrity_failed"
        assert body["passed"] is False
        assert body["fail_count"] == 1


# ---------------------------------------------------------------------------
# amendment amend0923-selfuse-write — the repository root holds tracked files only
# ---------------------------------------------------------------------------


class TestRepoRootHygiene:
    """R-0829 and DECISION amend0923-selfuse-write D5, 2026-09-23.

    The packer refuses these shapes at build time, but a build happens once per
    closure. This check runs every round, so reviewer scratch cannot sit in the
    root for the weeks it took R-0829 to be noticed.
    """

    @staticmethod
    def _check(tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        return integrity_gate._check_repo_root_hygiene()

    def test_a_clean_root_passes(self, tmp_path, monkeypatch):
        (tmp_path / "packages").mkdir()
        check = self._check(tmp_path, monkeypatch)
        assert check.name == "repo_root_hygiene"
        assert check.status is IntegrityStatus.PASS

    def test_reviewer_scratch_fails_and_is_named(self, tmp_path, monkeypatch):
        (tmp_path / "remedy-review-old-scratch").mkdir()
        check = self._check(tmp_path, monkeypatch)
        assert check.status is IntegrityStatus.FAIL
        assert "remedy-review-old-scratch" in check.message

    def test_each_refused_shape_fails(self, tmp_path, monkeypatch):
        (tmp_path / "remedy-job-evidence-f112-closure").mkdir()
        (tmp_path / "stray.zip").write_bytes(b"x")
        (tmp_path / "BUILDER_WAS_HERE.txt").write_text("x")
        check = self._check(tmp_path, monkeypatch)
        assert check.status is IntegrityStatus.FAIL
        for name in ("remedy-job-evidence-f112-closure", "stray.zip",
                     "BUILDER_WAS_HERE.txt"):
            assert name in check.message

    def test_the_message_names_at_most_five(self, tmp_path, monkeypatch):
        for i in range(9):
            (tmp_path / f"remedy-review-{i}-scratch").mkdir()
        check = self._check(tmp_path, monkeypatch)
        assert check.status is IntegrityStatus.FAIL
        named = [n for n in range(9) if f"remedy-review-{n}-scratch" in check.message]
        assert len(named) == 5, f"named {named}"
        assert "9" in check.message, "the message must state the true total"

    def test_an_unreadable_root_skips_rather_than_fails(self, tmp_path, monkeypatch):
        """The handler is narrowed to OSError, so the SKIP path is proved here.

        A blind `except Exception` would have been the 291st excused handler
        against the ratchet frozen at 290 in tests/test_ble001_ratchet.py.
        Reading the root directory is the only thing this check does that can
        fail, so OSError is the whole set — and this test is what says so.
        """
        monkeypatch.chdir(tmp_path)

        def _boom(self):
            raise PermissionError("root is unreadable")

        monkeypatch.setattr(Path, "iterdir", _boom)
        check = integrity_gate._check_repo_root_hygiene()
        assert check.status is IntegrityStatus.SKIP
        assert "root is unreadable" in check.message

    def test_the_check_is_registered_in_the_gate(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = run_integrity_checks()
        names = [c.name for c in result.checks]
        assert "repo_root_hygiene" in names
        assert names.index("repo_root_hygiene") == names.index("relevant_untracked") + 1

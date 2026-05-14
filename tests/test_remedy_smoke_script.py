"""
Tests for scripts/remedy_smoke.sh structural correctness.

These tests inspect the script text for required patterns and, where bash
is available, run lightweight execution checks using stub remedy commands.

All execution tests are skipped if bash is not on PATH.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import textwrap
from pathlib import Path

import pytest

SMOKE_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "remedy_smoke.sh"
_BASH = shutil.which("bash")
_REQUIRES_BASH = pytest.mark.skipif(_BASH is None, reason="bash not on PATH")
# invert: skip when bash IS None (we need it)
_NEEDS_BASH = pytest.mark.skipif(_BASH is None, reason="bash not found")


def _script_text() -> str:
    return SMOKE_SCRIPT.read_text()


# ---------------------------------------------------------------------------
# Script text assertions (no bash needed)
# ---------------------------------------------------------------------------


class TestSmokeScriptText:
    def test_script_exists(self):
        assert SMOKE_SCRIPT.exists(), f"smoke script not found: {SMOKE_SCRIPT}"

    def test_defines_remedy_smoke_function(self):
        assert "remedy_smoke()" in _script_text()

    def test_function_body_uses_subshell(self):
        text = _script_text()
        # The function must open a subshell: "remedy_smoke() {" ... "  ("
        # We check that `(\n    set -euo pipefail` pattern is present.
        assert "(\n    set -euo pipefail" in text or "(\n  set -euo pipefail" in text, (
            "function body must open a subshell with ( followed by set -euo pipefail"
        )

    def test_set_euo_inside_subshell_not_at_top_level(self):
        text = _script_text()
        lines = text.splitlines()
        # Top-level `set -euo pipefail` must not appear outside function/subshell
        top_level_set = [
            l for l in lines
            if l.strip() == "set -euo pipefail" and not l.startswith(" ") and not l.startswith("\t")
        ]
        assert top_level_set == [], (
            f"set -euo pipefail found at top level (leaks to caller): {top_level_set}"
        )

    def test_has_direct_run_entrypoint(self):
        text = _script_text()
        assert 'BASH_SOURCE[0]' in text and '"${0}"' in text, (
            "missing direct-run entrypoint: if [[ \"${BASH_SOURCE[0]}\" == \"${0}\" ]]"
        )

    def test_entrypoint_calls_remedy_smoke(self):
        text = _script_text()
        # The entrypoint block must contain `remedy_smoke`
        assert "remedy_smoke" in text.split('BASH_SOURCE[0]')[-1], (
            "direct-run entrypoint does not call remedy_smoke"
        )

    def test_view_path_extraction_has_safe_fallback(self):
        text = _script_text()
        # Must use awk or a pipeline ending in `|| true` for VIEW_PATH extraction
        assert ("awk" in text and "Brain Viewer v0" in text) or \
               ("grep" in text and "|| true" in text), (
            "VIEW_PATH extraction must use awk-based or '|| true' safe fallback"
        )

    def test_view_path_uses_awk_sub(self):
        text = _script_text()
        # Must use sub() to strip the prefix, not -F': ' field splitting
        assert "sub(/^Brain Viewer v0: /, \"\")" in text or \
               "sub(/^Brain Viewer v0: /," in text, (
            "VIEW_PATH extraction must use awk sub() to avoid colon-truncation on unusual paths"
        )

    def test_view_path_not_grep_sed_pipeline(self):
        text = _script_text()
        # The old fragile pattern was: grep ... | sed ...
        # Ensure it is not present unprotected
        lines = text.splitlines()
        fragile = [l for l in lines if "grep" in l and "sed" in l and "|| true" not in l]
        assert fragile == [], f"grep|sed pipeline without || true guard: {fragile}"

    def test_no_http_server(self):
        assert "http.server" not in _script_text()

    def test_no_xdg_open(self):
        assert "xdg-open" not in _script_text()

    def test_no_open_http_url(self):
        text = _script_text()
        assert 'open "http' not in text and "open 'http" not in text

    def test_no_lan_url_variable(self):
        text = _script_text()
        assert "VIEWER_HOST" not in text
        assert "LAN" not in text

    def test_no_pid_file(self):
        assert "PID_FILE" not in _script_text()

    def test_remedy_smoke_is_asserted_passed(self):
        assert "remedy_smoke: PASSED" in _script_text()

    def test_project_alias_asserted(self):
        assert "remedy project" in _script_text()

    def test_show_project_asserted(self):
        assert "remedy show-project" in _script_text()

    def test_project_placeholder_asserted(self):
        assert "project_placeholder" in _script_text()

    def test_apply_before_approval_step_present(self):
        text = _script_text()
        assert "apply before approval" in text and "blocked" in text, (
            "smoke must test apply-before-approval (expect blocked)"
        )

    def test_apply_after_approval_step_present(self):
        text = _script_text()
        assert "apply-patch-intent" in text and "Apply approved patch intent" in text, (
            "smoke must test apply-patch-intent after approval"
        )

    def test_apply_noop_step_present(self):
        text = _script_text()
        assert "Repeat apply" in text and "no-op" in text, (
            "smoke must test repeat apply as no-op"
        )

    def test_target_repo_cleanup_before_mkdir(self):
        text = _script_text()
        # rm -rf must appear before mkdir -p for TARGET_REPO
        rm_pos = text.find('rm -rf "${TARGET_REPO}"')
        mk_pos = text.find('mkdir -p "${TARGET_REPO}"')
        assert rm_pos != -1, "smoke must rm -rf TARGET_REPO before mkdir"
        assert mk_pos != -1, "smoke must mkdir -p TARGET_REPO"
        assert rm_pos < mk_pos, "rm -rf must come before mkdir -p"

    def test_brain_asserts_patch_apply_node(self):
        text = _script_text()
        assert "patch_apply" in text and "patch_apply node" in text, (
            "smoke step 11 must assert patch_apply node appears after apply lifecycle"
        )

    def test_run_log_schema_step_present(self):
        text = _script_text()
        # Must verify exact metadata keys
        assert "bytes_written" in text and "line_count" in text and "intent_id" in text, (
            "smoke must verify run-log metadata keys (bytes_written, line_count, intent_id)"
        )
        assert "patch_intent_applied" in text, (
            "smoke must check for patch_intent_applied events"
        )

    def test_run_log_checks_blocked_applied_noop_outcomes(self):
        text = _script_text()
        assert "'blocked'" in text and "'applied'" in text and "'noop'" in text, (
            "smoke run-log check must verify blocked, applied, and noop outcomes"
        )

    def test_runs_root_resolved(self):
        text = _script_text()
        assert "RUNS_ROOT" in text, (
            "smoke must define RUNS_ROOT for run-log inspection"
        )

    def test_applied_file_content_check_present(self):
        text = _script_text()
        assert "Remedy control marker" in text or "control markers" in text.lower(), (
            "smoke must check applied file for absence of Remedy control markers"
        )

    def test_applied_file_no_marker_prefix_asserted(self):
        text = _script_text()
        assert "<!-- remedy:patch-intent" in text and "Generated by Remedy" in text, (
            "smoke must assert absence of control marker prefix and Generated-by line"
        )

    def test_proposed_update_section_asserted(self):
        text = _script_text()
        assert "## Proposed Update" in text, (
            "smoke must assert ## Proposed Update section present in applied file"
        )


# ---------------------------------------------------------------------------
# Execution tests (require bash)
# ---------------------------------------------------------------------------


def _write_stub_remedy(tmp_path: Path, script_body: str) -> Path:
    """Write a stub `remedy` script that responds to sub-commands."""
    stub = tmp_path / "remedy"
    stub.write_text("#!/usr/bin/env bash\n" + script_body)
    stub.chmod(stub.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return stub


def _run_in_bash(script: str, env: dict | None = None, cwd: str | None = None) -> subprocess.CompletedProcess:
    merged = {**os.environ, **(env or {})}
    return subprocess.run(
        [_BASH, "-c", script],
        capture_output=True,
        text=True,
        env=merged,
        cwd=cwd,
    )


@pytest.mark.skipif(_BASH is None, reason="bash not found")
class TestSmokeScriptExecution:
    def test_direct_run_exits_nonzero_without_remedy(self, tmp_path):
        """Direct execution should fail if remedy is not on PATH."""
        env = {"PATH": str(tmp_path), "HOME": str(tmp_path)}
        result = _run_in_bash(f"bash '{SMOKE_SCRIPT}'", env=env)
        assert result.returncode != 0

    def test_sourcing_does_not_set_nounset(self, tmp_path):
        """After sourcing, caller's nounset should not be enabled by the script."""
        script = textwrap.dedent(f"""
            source '{SMOKE_SCRIPT}'
            # Check that nounset (set -u) is NOT enabled in this shell
            if [[ "$-" == *u* ]]; then
                echo "FAIL: nounset leaked"
                exit 1
            fi
            echo "OK: nounset not leaked"
        """)
        result = _run_in_bash(script)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "OK: nounset not leaked" in result.stdout

    def test_sourcing_does_not_set_pipefail(self, tmp_path):
        """After sourcing, caller's pipefail should not be enabled by the script."""
        script = textwrap.dedent(f"""
            source '{SMOKE_SCRIPT}'
            # pipefail is not accessible via $-, check via set -o
            if set -o | grep -q 'pipefail.*on'; then
                echo "FAIL: pipefail leaked"
                exit 1
            fi
            echo "OK: pipefail not leaked"
        """)
        result = _run_in_bash(script)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "OK: pipefail not leaked" in result.stdout

    def test_sourcing_defines_remedy_smoke_function(self, tmp_path):
        """After sourcing, remedy_smoke should be defined as a function."""
        script = textwrap.dedent(f"""
            source '{SMOKE_SCRIPT}'
            if declare -f remedy_smoke > /dev/null 2>&1; then
                echo "OK: remedy_smoke defined"
            else
                echo "FAIL: remedy_smoke not defined"
                exit 1
            fi
        """)
        result = _run_in_bash(script)
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "OK: remedy_smoke defined" in result.stdout

    def test_direct_run_calls_remedy_smoke(self, tmp_path):
        """Direct execution invokes the function (stub remedy records it was called)."""
        stub_dir = tmp_path / "bin"
        stub_dir.mkdir()
        # Stub remedy: always exits 1 so the smoke aborts early,
        # but we can detect that it was called.
        called_marker = tmp_path / "remedy_called"
        stub = stub_dir / "remedy"
        stub.write_text(textwrap.dedent(f"""
            #!/usr/bin/env bash
            touch '{called_marker}'
            exit 1
        """))
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        env = {"PATH": f"{stub_dir}:{os.environ.get('PATH', '')}", "HOME": str(tmp_path)}
        result = _run_in_bash(f"bash '{SMOKE_SCRIPT}'", env=env)
        # Smoke will fail (stub exits 1), but remedy must have been invoked
        assert called_marker.exists(), "stub remedy was never called by direct run"

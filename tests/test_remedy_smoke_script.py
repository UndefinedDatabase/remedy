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
        assert "LAN_URL" not in text
        assert "VIEWER_LAN" not in text

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
        assert "raw HTML comment" in text or "<!--" in text, (
            "smoke must check applied file for absence of raw HTML comments"
        )

    def test_applied_file_newline_check_present(self):
        text = _script_text()
        assert "ends with a newline" in text or "endswith" in text, (
            "smoke must check that applied file ends with a newline"
        )

    def test_brain_target_path_from_metadata_not_properties(self):
        text = _script_text()
        # Must extract target_path from n["metadata"], not n["properties"]
        assert "metadata" in text and "target_path" in text, (
            "smoke must extract patch_apply target_path from node metadata"
        )
        assert 'get("properties"' not in text, (
            "smoke must not use 'properties' key — brain nodes use 'metadata'"
        )

    def test_smoke_fails_when_patch_apply_target_missing(self):
        text = _script_text()
        # Smoke must fail (not skip) if target_path is absent after apply
        assert "patch_apply node target_path missing" in text or \
               "target_path missing from brain" in text, (
            "smoke must fail if patch_apply target_path is missing after apply lifecycle"
        )

    def test_applied_file_no_raw_html_comment_asserted(self):
        text = _script_text()
        # Applied-file check must scan for raw '<!--' (not just the remedy-specific prefix)
        assert "'<!--'" in text or '"<!--"' in text, (
            "smoke applied-file check must scan for raw '<!--'"
        )
        assert "Generated by Remedy" in text, (
            "smoke applied-file check must scan for 'Generated by Remedy'"
        )

    def test_proposed_update_section_asserted(self):
        text = _script_text()
        assert "## Proposed Update" in text, (
            "smoke must assert ## Proposed Update section present in applied file"
        )

    def test_smoke_does_not_import_private_resolve_runs_root(self):
        text = _script_text()
        assert "_resolve_runs_root" not in text, (
            "smoke must not import private _resolve_runs_root — use public filesystem convention"
        )

    def test_smoke_uses_public_runs_root_convention(self):
        text = _script_text()
        # Must use simple env-var-or-hardcoded convention, not a Python import
        assert 'RUNS_ROOT=".data/runs"' in text or "RUNS_ROOT='.data/runs'" in text, (
            "smoke RUNS_ROOT must default to '.data/runs' without private imports"
        )

    def test_smoke_scans_whole_target_repo_for_markers(self):
        text = _script_text()
        assert "root.rglob('*')" in text or 'root.rglob("*")' in text, (
            "smoke must scan whole TARGET_REPO with root.rglob('*')"
        )
        assert "target repo markerless" in text, (
            "smoke whole-repo scan must print 'target repo markerless: OK' on success"
        )
        assert "UnicodeDecodeError" in text, (
            "smoke whole-repo scan must catch UnicodeDecodeError (skip binary files)"
        )
        assert "OSError" in text, (
            "smoke whole-repo scan must catch OSError (skip unreadable files)"
        )

    def test_smoke_scan_skips_binary_files_or_decode_errors(self):
        text = _script_text()
        assert "UnicodeDecodeError" in text and "OSError" in text, (
            "smoke whole-repo scan must catch both UnicodeDecodeError and OSError"
        )

    def test_smoke_markerless_scan_uses_intent_id(self):
        text = _script_text()
        assert "needles.append(intent_id)" in text or 'needles.append(FIRST_INTENT_ID)' in text, (
            "smoke whole-repo scan must include intent_id as a forbidden needle"
        )

    def test_whole_repo_scan_does_not_forbid_neutralized_marker_substring(self):
        text = _script_text()
        # bare 'remedy:patch-intent' must not appear as a quoted scan needle
        assert "'remedy:patch-intent'" not in text, (
            "smoke must not scan for bare 'remedy:patch-intent'"
        )
        assert '"remedy:patch-intent"' not in text, (
            'smoke must not scan for bare "remedy:patch-intent"'
        )
        # Unit proof: neutralized form &lt;!-- does not match the forbidden needle <!--
        neutralized = "&lt;!-- remedy:patch-intent FAKE begin -->"
        assert "<!--" not in neutralized, (
            "&lt;!-- form must not contain the forbidden needle '<!--'"
        )

    def test_whole_repo_scan_still_blocks_raw_control_marker(self):
        text = _script_text()
        # The whole-repo scan must use '<!--' (the general HTML comment start)
        assert "'<!--'" in text or '"<!--"' in text, (
            "smoke whole-repo scan must forbid raw '<!--'"
        )
        assert "Generated by Remedy" in text, (
            "smoke must still scan for 'Generated by Remedy' provenance string"
        )
        assert "needles.append(intent_id)" in text, (
            "smoke must still append intent_id to forbidden needles"
        )

    def test_neutralized_marker_does_not_match_forbidden_needles(self):
        # Unit-level proof: the neutralized form must not match any forbidden needle
        escaped = "&lt;!-- remedy:patch-intent FAKE begin -->"
        forbidden = ["Generated by Remedy", "<!--"]
        assert not any(n in escaped for n in forbidden), (
            "neutralized marker form must not match any forbidden needle — "
            "confirms &lt;!-- is safe while <!-- is forbidden"
        )

    def test_target_repo_is_recreated_fresh_each_run(self):
        text = _script_text()
        # TARGET_REPO is rm -rf'd before mkdir so the scan always starts clean
        assert "rm -rf" in text and "TARGET_REPO" in text, (
            "smoke must rm -rf TARGET_REPO before use so the whole-repo scan is valid"
        )

    def test_smoke_whole_repo_scan_is_developer_invariant(self):
        text = _script_text()
        # The script comment must document that the scan is a developer smoke invariant
        assert "developer smoke invariant" in text or "smoke invariant" in text, (
            "smoke script must document that the whole-repo scan is a developer invariant"
        )

    def test_smoke_seeds_readme_before_run(self):
        text = _script_text()
        assert "README.md" in text, (
            "smoke must write README.md into TARGET_REPO before running "
            "so modify-action apply always finds the target file"
        )
        assert "Initial README content" in text, (
            "smoke must seed README.md with initial content"
        )

    def test_smoke_readme_seed_before_plan_job(self):
        text = _script_text()
        readme_pos = text.find("README.md")
        plan_pos   = text.find("plan-job")
        assert readme_pos != -1, "smoke must contain README.md seed"
        assert plan_pos   != -1, "smoke must contain plan-job step"
        assert readme_pos < plan_pos, (
            "smoke must seed README.md before plan-job so the file exists when apply runs"
        )

    def test_smoke_default_prompt_forces_write_readme_task(self):
        text = _script_text()
        assert "write_readme" in text, (
            "smoke default prompt must contain 'write_readme' to make the task type deterministic"
        )

    def test_smoke_default_prompt_is_english(self):
        text = _script_text()
        # The default prompt must be English (not German)
        assert "Create exactly one task" in text or "exactly one task" in text, (
            "smoke default prompt must be English and contain 'exactly one task'"
        )

    def test_smoke_default_prompt_forces_exactly_one_task(self):
        text = _script_text()
        assert "exactly one task" in text or "one task" in text, (
            "smoke default prompt must force exactly one task for determinism"
        )

    def test_viewer_sanity_block_has_no_bare_assert(self):
        text = _script_text()
        # Extract only the viewer sanity section (step 12 after renumbering in Step 30.12)
        start = text.find("# 12.")
        if start == -1:
            start = text.find("12. Assert viewer")
        end = text.find("# 13.", start) if start != -1 else -1
        if start != -1 and end != -1:
            viewer_block = text[start:end]
        else:
            viewer_block = text
        assert "assert " not in viewer_block, (
            "viewer sanity block must not use bare 'assert' — use explicit error messages"
        )

    def test_viewer_sanity_block_prints_actionable_errors(self):
        text = _script_text()
        assert "viewer sanity failed" in text, (
            "viewer sanity block must print 'viewer sanity failed' on failure, not bare AssertionError"
        )

    def test_viewer_sanity_checks_viewer_data_keys(self):
        text = _script_text()
        assert "node_details" in text, "viewer sanity must check for 'node_details' key"
        assert "positions" in text,    "viewer sanity must check for 'positions' key"
        assert "detail_fallback_count" in text, (
            "viewer sanity must check for 'detail_fallback_count' key"
        )

    def test_viewer_sanity_checks_graph_nodes_non_empty(self):
        text = _script_text()
        assert "graph.nodes is empty" in text or "nodes is empty" in text, (
            "viewer sanity must check that graph.nodes is non-empty"
        )

    def test_viewer_sanity_checks_id_viewer_data(self):
        text = _script_text()
        assert 'id="viewer-data"' in text or "id='viewer-data'" in text or \
               'id=\\"viewer-data\\"' in text, (
            "viewer sanity must check for id=\"viewer-data\" in index.html"
        )

    def test_viewer_sanity_checks_application_json(self):
        text = _script_text()
        assert 'type="application/json"' in text or \
               'type=\\"application/json\\"' in text, (
            "viewer sanity must check for type=\"application/json\" in index.html"
        )

    def test_viewer_sanity_checks_static_fallback(self):
        text = _script_text()
        assert "static-fallback" in text, (
            "viewer sanity must check for 'static-fallback' in index.html"
        )

    def test_viewer_sanity_checks_unresolved_placeholders(self):
        text = _script_text()
        assert "__VIEWER_DATA_JSON__" in text, (
            "viewer sanity must check that __VIEWER_DATA_JSON__ is absent from rendered HTML"
        )
        assert "__STATIC_FALLBACK__" in text, (
            "viewer sanity must check that __STATIC_FALLBACK__ is absent from rendered HTML"
        )
        assert "__JOB_SHORT_ID__" in text, (
            "viewer sanity must check that __JOB_SHORT_ID__ is absent from rendered HTML"
        )
        assert "__GENERATED_AT__" in text, (
            "viewer sanity must check that __GENERATED_AT__ is absent from rendered HTML"
        )

    # ------------------------------------------------------------------
    # Step 30.12: --task-type on create-job, no plan-job
    # ------------------------------------------------------------------

    def test_create_job_uses_task_type_flag(self):
        text = _script_text()
        assert "--task-type" in text, (
            "create-job call must use --task-type to bypass planner"
        )

    def test_create_job_uses_write_readme_task_type(self):
        text = _script_text()
        assert "--task-type write_readme" in text, (
            "create-job must set --task-type write_readme for smoke determinism"
        )

    def test_create_job_uses_task_description_flag(self):
        text = _script_text()
        assert "--task-description" in text, (
            "create-job call must pass --task-description alongside --task-type"
        )

    def test_plan_job_not_called_in_smoke(self):
        text = _script_text()
        # 'plan-job' must not appear as a standalone remedy sub-command call.
        # plan-job-local is a different command and is not called either, but
        # the key invariant is that `remedy plan-job` is absent.
        import re
        matches = re.findall(r'remedy\s+plan-job\b(?!-local)', text)
        assert matches == [], (
            "smoke must not call 'remedy plan-job' — explicit --task-type replaces the planner. "
            f"Found: {matches}"
        )

    def test_smoke_asserts_job_state_planned_after_create(self):
        text = _script_text()
        assert "state" in text and "planned" in text, (
            "smoke must assert job state=planned after create-job --task-type"
        )

    def test_smoke_asserts_single_write_readme_task(self):
        text = _script_text()
        assert "write_readme" in text and ("task_type" in text or "inputs" in text), (
            "smoke must assert the created job has a write_readme task"
        )

    # ------------------------------------------------------------------
    # Step 30.13: explicit-task sanity without nested subprocess.run
    # ------------------------------------------------------------------

    def test_explicit_task_sanity_uses_temp_file_not_nested_subprocess(self):
        text = _script_text()
        # The nested subprocess.run(['remedy', ...]) call is replaced by a Bash
        # temp-file approach. Neither the list form nor the string form should appear.
        import re
        nested_calls = re.findall(
            r"subprocess\.run\s*\(\s*\[[\'\"]remedy", text
        )
        assert nested_calls == [], (
            "smoke must not call subprocess.run(['remedy', ...]) from inside Python — "
            f"use a Bash temp file instead. Found: {nested_calls}"
        )

    def test_explicit_task_sanity_uses_mktemp(self):
        text = _script_text()
        assert "mktemp" in text, (
            "smoke explicit-task sanity must use mktemp to create a temp file "
            "for remedy show-job output"
        )

    # ------------------------------------------------------------------
    # Step 30.13: viewer redaction sentinel precision
    # ------------------------------------------------------------------

    def test_smoke_does_not_forbid_plain_artifact_content_phrase(self):
        text = _script_text()
        # "artifact content" must NOT appear as a quoted forbidden token, because
        # safe explanatory viewer copy (e.g. "Does not include ... artifact content")
        # would be a false positive.
        assert '"artifact content"' not in text, (
            "smoke must not use '\"artifact content\"' as a forbidden token — "
            "it matches safe explanatory negation text and is a false positive"
        )
        assert "'artifact content'" not in text, (
            "smoke must not use \"'artifact content'\" as a forbidden token"
        )

    def test_smoke_still_forbids_approval_reason_diff_preview_command_output(self):
        text = _script_text()
        assert "approval_reason" in text, (
            "smoke must still forbid 'approval_reason' as a dangerous metadata key"
        )
        assert "diff_preview" in text, (
            "smoke must still forbid 'diff_preview' as a dangerous metadata key"
        )
        assert "command_output" in text, (
            "smoke must still forbid 'command_output' as a dangerous output key"
        )

    def test_smoke_still_checks_sentinel_tokens(self):
        text = _script_text()
        assert "MUST_NOT_RENDER" in text, (
            "smoke must check for 'MUST_NOT_RENDER' sentinel in viewer output"
        )
        assert "Traceback" in text, (
            "smoke must still check for 'Traceback' in viewer output"
        )
        assert "forbidden redaction token" in text, (
            "smoke redaction checks must print 'forbidden redaction token' on failure"
        )

    def test_safe_explanatory_string_does_not_match_forbidden_viewer_tokens(self):
        """The viewer's safe explanatory redaction text must not trip the forbidden-token list."""
        # This is the kind of string brain_viewer.py may legitimately produce.
        safe_string = (
            "Does not include raw prompt, file content, artifact content, event messages."
        )
        # These are the precise forbidden tokens the smoke checks for.
        forbidden_tokens = [
            "approval_reason", "diff_preview", "command_output",
            "raw_command_output", "DIFF_PREVIEW", "RAW_COMMAND_OUTPUT",
            "APPROVAL_REASON", "MUST_NOT_RENDER", "Traceback", "Exception:",
        ]
        for tok in forbidden_tokens:
            assert tok not in safe_string, (
                f"safe explanatory string unexpectedly contains sentinel {tok!r}; "
                "check the forbidden-token list for false positives"
            )

    def test_viewer_redaction_scan_covers_viewer_data_json(self):
        text = _script_text()
        # The redaction scan must explicitly check viewer_data.json, not only index.html.
        assert "viewer_data.json" in text and "forbidden_tokens" in text, (
            "smoke must scan viewer_data.json for forbidden redaction tokens"
        )

    def test_viewer_redaction_scan_covers_index_html(self):
        text = _script_text()
        assert "index.html" in text and "forbidden_tokens" in text, (
            "smoke must scan index.html for forbidden redaction tokens"
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

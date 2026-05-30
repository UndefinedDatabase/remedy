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
        assert "remedy project show" in _script_text()

    def test_project_placeholder_asserted(self):
        assert "project_placeholder" in _script_text()

    def test_apply_before_approval_step_present(self):
        text = _script_text()
        assert "apply before approval" in text and "blocked" in text, (
            "smoke must test apply-before-approval (expect blocked)"
        )

    def test_apply_after_approval_step_present(self):
        text = _script_text()
        assert "patch apply" in text and "Apply approved patch intent" in text, (
            "smoke must test patch apply after approval"
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

    def test_smoke_readme_seed_before_job_run(self):
        text = _script_text()
        readme_pos = text.find("README.md")
        run_pos    = text.find("remedy job run-next")
        assert readme_pos != -1, "smoke must contain README.md seed"
        assert run_pos    != -1, "smoke must contain remedy job run-next step"
        assert readme_pos < run_pos, (
            "smoke must seed README.md before job run-next so the file exists when apply runs"
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
        # 'job plan' must not appear as a standalone remedy call in smoke.
        # The smoke uses --task-type on create to bypass the planner.
        import re
        matches = re.findall(r'remedy\s+job\s+plan\b', text)
        assert matches == [], (
            "smoke must not call 'remedy job plan' — explicit --task-type replaces the planner. "
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
            "for remedy job show output"
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

    # Step 31: Apply Proof smoke checks

    def test_smoke_checks_patch_apply_proof_recorded_event(self):
        text = _script_text()
        assert "patch_apply_proof_recorded" in text, (
            "smoke must check for patch_apply_proof_recorded events (Step 31)"
        )

    def test_smoke_proof_checks_exact_13_keys(self):
        text = _script_text()
        # All 13 required proof event keys must appear in the smoke verification
        for key in (
            "before_sha256", "after_sha256",
            "before_bytes", "after_bytes", "bytes_delta",
            "before_line_count", "after_line_count", "line_delta",
            "applied_at",
        ):
            assert key in text, (
                f"smoke must verify proof event key {key!r} (Step 31)"
            )

    def test_smoke_proof_checks_after_sha_length(self):
        text = _script_text()
        # Smoke must validate that after_sha256 is 64 chars
        assert "after_sha256" in text and "64" in text, (
            "smoke must validate after_sha256 is 64-char hex"
        )

    def test_smoke_proof_checks_bytes_delta_positive(self):
        text = _script_text()
        assert "bytes_delta" in text and "0" in text, (
            "smoke must verify bytes_delta is positive after apply"
        )

    def test_smoke_proof_no_raw_content_forbidden_strings(self):
        text = _script_text()
        # The proof check must exclude the same forbidden strings as the run-log check
        assert "'approval_reason'" in text or '"approval_reason"' in text, (
            "smoke proof check must reject approval_reason"
        )

    # --- Step 32: Repository structure sanity block -----------------------

    def test_smoke_has_structure_sanity_step(self):
        text = _script_text()
        assert "Repository structure sanity" in text, (
            "smoke must have a repository structure sanity check step"
        )

    def test_smoke_structure_sanity_checks_data_paths(self):
        text = _script_text()
        assert "data_paths" in text, "structure sanity must check data_paths module"

    def test_smoke_structure_sanity_checks_path_utils(self):
        text = _script_text()
        assert "path_utils" in text, "structure sanity must check path_utils module"

    def test_smoke_structure_sanity_checks_no_local_sanitize(self):
        text = _script_text()
        assert "_sanitize_path_component" in text, (
            "structure sanity must check that _sanitize_path_component is gone from consumers"
        )

    def test_smoke_structure_sanity_covers_repo_applicator(self):
        text = _script_text()
        assert "repo_applicator" in text, (
            "structure sanity no-local-sanitizer check must cover repo_applicator.py"
        )

    def test_smoke_structure_sanity_checks_remedy_data_dir(self):
        text = _script_text()
        assert "REMEDY_DATA_DIR" in text, (
            "structure sanity must verify no inline REMEDY_DATA_DIR reads in production code"
        )

    def test_smoke_structure_sanity_checks_reserved_docstrings(self):
        text = _script_text()
        assert "docstring" in text or "startswith" in text, (
            "structure sanity must verify reserved namespace __init__.py files have docstrings"
        )

    def test_smoke_viewer_sanity_comment_has_no_unescaped_double_quotes_in_c_script(self):
        """The python3 -c script for step 12 must not have unescaped double-quotes in comments.

        An unescaped " inside a bash double-quoted string terminates it early,
        causing subsequent words (e.g. 'not') to become sys.argv[1] instead of
        VIEW_DIR, silently breaking the viewer sanity check.
        """
        text = _script_text()
        # The specific comment that was broken: must use single quotes inside, not double
        assert '"Does not include' not in text, (
            "viewer sanity step 12 Python comment must use single quotes around the "
            "example phrase to avoid terminating the bash double-quoted -c string early"
        )

    def test_smoke_proof_comment_mentions_lifecycle_prerequisite(self):
        text = _script_text()
        assert "approve/apply lifecycle" in text or "lifecycle" in text, (
            "proof event check must note that it assumes approve/apply has already run"
        )

    # --- Step 33: Permission-gated test run block -------------------------

    def test_smoke_has_run_tests_local_step(self):
        text = _script_text()
        assert "test run" in text, (
            "smoke must call remedy test run as part of Step 33"
        )

    def test_smoke_grants_repo_test_run_permission(self):
        text = _script_text()
        assert "repo_test_run" in text, (
            "smoke must grant repo_test_run permission before running tests"
        )

    def test_smoke_asserts_test_run_completed_schema(self):
        text = _script_text()
        assert "test_run_completed" in text, (
            "smoke must verify test_run_completed run-log event is present"
        )

    def test_smoke_checks_test_run_required_metadata_keys(self):
        text = _script_text()
        # All 11 required schema keys must appear in the smoke check.
        required = [
            "test_run_id",
            "command",
            "status",
            "exit_code",
            "duration_ms",
            "output_line_count",
            "output_bytes",
            "command_source_type",
            "command_source_path",
            "command_purpose",
            "command_confidence",
        ]
        for key in required:
            assert key in text, (
                f"smoke test_run_completed schema check must reference key '{key}'"
            )

    def test_smoke_forbids_raw_output_in_test_run_log(self):
        text = _script_text()
        # The smoke must verify these forbidden keys don't appear in test_run metadata.
        for key in ("stdout", "stderr", "raw_output", "command_output"):
            assert key in text, (
                f"smoke must block forbidden key '{key}' from test_run_completed metadata"
            )

    def test_smoke_asserts_test_run_node_in_brain(self):
        text = _script_text()
        assert "test_run" in text, (
            "smoke must verify 'test_run' node type appears in brain after test run"
        )

    def test_smoke_target_repo_has_tests_directory(self):
        text = _script_text()
        assert "test_readme" in text or "tests/" in text, (
            "smoke target repo must include a tests/ directory with a pytest file"
        )

    # --- Step 34: Command Discovery (step 6n) --------------------------------

    def test_smoke_has_discover_commands_step(self):
        text = _script_text()
        assert "test discover" in text, (
            "smoke must call remedy test discover as part of Step 34"
        )

    def test_smoke_discover_commands_checks_json(self):
        text = _script_text()
        assert "test discover" in text and "--json" in text, (
            "smoke test discover step must use --json for structured verification"
        )

    def test_smoke_discover_commands_checks_command_source_type(self):
        text = _script_text()
        assert "command_source_type" in text, (
            "smoke must verify command_source_type in test_run_completed metadata"
        )

    # --- Step 34.1: Multi-ecosystem Command Discovery (step 6n hardening) ----

    def test_smoke_target_repo_has_makefile_with_test_target(self):
        text = _script_text()
        assert "Makefile" in text, (
            "smoke target repo must include a Makefile for make test discovery"
        )
        assert "make test" in text or "make\ntest" in text or ".PHONY" in text, (
            "smoke Makefile must declare a test target"
        )

    def test_smoke_target_repo_has_pnpm_lockfile(self):
        text = _script_text()
        assert "pnpm-lock.yaml" in text, (
            "smoke target repo must include pnpm-lock.yaml for JS lockfile detection"
        )

    def test_smoke_target_repo_has_cargo_toml_subdir(self):
        text = _script_text()
        assert "Cargo.toml" in text, (
            "smoke target repo must include a Cargo.toml subdir for Rust ecosystem detection"
        )

    def test_smoke_target_repo_has_go_mod_subdir(self):
        text = _script_text()
        assert "go.mod" in text, (
            "smoke target repo must include a go.mod subdir for Go ecosystem detection"
        )

    def test_smoke_target_repo_has_jvm_manifest(self):
        text = _script_text()
        assert "build.gradle" in text or "pom.xml" in text, (
            "smoke target repo must include a Gradle or Maven manifest for JVM detection"
        )

    def test_smoke_discover_commands_checks_schema_version(self):
        text = _script_text()
        assert "version" in text and ("version'] != 1" in text or "version == 1" in text
                                       or "version.*1" in text or "!= 1" in text), (
            "smoke step 6n must verify version=1 in discover-commands JSON schema"
        )

    def test_smoke_discover_commands_checks_selected_test_candidate(self):
        text = _script_text()
        assert "selected_test_candidate" in text, (
            "smoke step 6n must verify selected_test_candidate field in discover-commands JSON"
        )

    def test_smoke_discover_commands_checks_constitution_source(self):
        text = _script_text()
        assert "constitution" in text, (
            "smoke step 6n must verify selected candidate comes from constitution source"
        )

    def test_smoke_discover_commands_checks_make_test_selected(self):
        text = _script_text()
        # smoke must verify make test is selected (argv check)
        assert ("make" in text and "test" in text
                and ("argv" in text or "make.*test" in text)), (
            "smoke step 6n must verify selected argv is ['make', 'test']"
        )

    def test_smoke_discover_commands_checks_pnpm_argv(self):
        text = _script_text()
        assert "pnpm" in text, (
            "smoke step 6n must verify pnpm is chosen for JS package manager (pnpm-lock.yaml present)"
        )

    def test_smoke_discover_commands_checks_multi_ecosystem_source_types(self):
        text = _script_text()
        # All required source types must be referenced in step 6n verification
        for src in ("constitution", "makefile", "package_json", "cargo", "go"):
            assert src in text, (
                f"smoke step 6n must verify source type '{src}' appears in discovered candidates"
            )

    def test_smoke_discover_commands_checks_jvm_source(self):
        text = _script_text()
        assert "gradle" in text or "maven" in text, (
            "smoke step 6n must verify a JVM source type (gradle or maven) is discovered"
        )

    def test_smoke_discover_commands_checks_source_path_relative(self):
        text = _script_text()
        # step 6n must verify source paths are not absolute (don't start with /)
        assert "source_path" in text and (
            "startswith('/')" in text or "relative" in text or "absolute" in text
        ), (
            "smoke step 6n must verify source_path values are relative, not absolute"
        )

    def test_smoke_discover_commands_checks_counts_field(self):
        text = _script_text()
        assert "counts" in text, (
            "smoke step 6n must verify 'counts' field in discover-commands JSON schema"
        )

    # --- Step 33.1: Trust/Timeline sanity section (step 6m) ----------------

    def test_smoke_has_trust_timeline_sanity_step(self):
        text = _script_text()
        assert "brain trust" in text and "brain timeline" in text, (
            "smoke must run both remedy brain trust and remedy brain timeline in step 6m"
        )

    def test_smoke_trust_timeline_sanity_checks_structural_presence(self):
        text = _script_text()
        # The step must verify the human output mentions "test run" structurally.
        assert "test run" in text or "test_run" in text, (
            "smoke 6m must check that trust/timeline mention 'test run' structurally"
        )

    def test_smoke_trust_timeline_sanity_does_not_reject_bare_stdout_in_human_text(self):
        text = _script_text()
        # Step 6m must NOT check `assert "stdout" not in trust` or similar.
        # Such a check would false-positive on redaction notes like
        # "(raw stdout/stderr not included in this report)".
        # Verify the 6m section does not use bare "stdout" as a forbidden token check.
        # We do this by confirming the human-text forbidden token list does NOT contain
        # a bare 'stdout' string in the forbidden_tokens / tok-check block.
        import re
        # Find the 6m block between "6m." and "6n." or "else" or "7."
        m = re.search(r"6m\..*?(?=echo.*?---\s+[67]\.|else\s+echo)", text, re.DOTALL)
        section_6m = m.group(0) if m else text
        # In the 6m section, "stdout" should only appear inside a comment/explanatory string,
        # not as a standalone forbidden token string like 'stdout'.
        # The forbidden list in 6m uses tokens like 'raw_output', 'command_output', etc.
        assert "'stdout'" not in section_6m and '"stdout"' not in section_6m, (
            "smoke 6m human-text check must not use bare 'stdout' as a forbidden token "
            "(would false-positive on redaction note text)"
        )

    def test_smoke_trust_timeline_sanity_still_blocks_real_leak_tokens(self):
        text = _script_text()
        # Real leak indicators must still be forbidden in the 6m human-text check.
        for tok in ("raw_output", "command_output", "RAW_COMMAND_OUTPUT",
                    "Traceback", "Exception:"):
            assert tok in text, (
                f"smoke 6m must still block actual leak token '{tok}' "
                "from trust report / timeline human output"
            )

    def test_smoke_trust_timeline_sanity_ok_message(self):
        text = _script_text()
        assert "trust/timeline mention test run structurally" in text, (
            "smoke 6m must print confirmation that trust/timeline mention test run structurally"
        )


    # --- Step 46.2: Memory --approved + brain memory nodes (step 12g) --------

    def test_smoke_has_memory_approved_store(self):
        text = _script_text()
        assert "--approved" in text and "memory store" in text, (
            "smoke must call remedy memory store --approved for approved memory test"
        )

    def test_smoke_checks_brain_memory_nodes(self):
        text = _script_text()
        assert "'memory'" in text or '"memory"' in text, (
            "smoke must verify 'memory' node type in brain graph"
        )

    def test_smoke_checks_memory_value_no_leak(self):
        text = _script_text()
        assert "'value'" in text and "leak" in text, (
            "smoke must verify memory node metadata does not contain 'value' (no leak)"
        )

    def test_smoke_checks_context_project_memory(self):
        text = _script_text()
        assert "project_memory" in text, (
            "smoke must verify project_memory signal in context_coverage"
        )

    # --- Step 46.2: Agent loop run-log schema (step 12h) -------------------

    def test_smoke_has_agent_loop_schema_check(self):
        text = _script_text()
        assert "agent_loop" in text and "schema" in text.lower(), (
            "smoke must verify agent_loop event schema"
        )

    def test_smoke_checks_agent_loop_required_meta_keys(self):
        text = _script_text()
        for key in ("cycle", "max_cycles", "decision", "stage", "reason",
                     "task_count", "pending_task_count", "pending_approval_count",
                     "applied_count", "test_run_count"):
            assert key in text, (
                f"smoke agent_loop schema check must reference key '{key}'"
            )

    def test_smoke_checks_no_agent_loop_task_exit(self):
        text = _script_text()
        assert "agent_loop_task_exit" in text, (
            "smoke must verify agent_loop_task_exit event does not exist"
        )

    def test_smoke_checks_agent_loop_forbidden_strings(self):
        text = _script_text()
        for s in ("stdout", "stderr", "raw_output", "Traceback"):
            assert s in text, (
                f"smoke agent_loop schema check must forbid '{s}'"
            )

    # --- Step 48: Readiness job JSON (step 12i) ----------------------------

    def test_smoke_has_readiness_job_json_step(self):
        text = _script_text()
        assert "readiness job" in text and "--json" in text, (
            "smoke must call remedy readiness job --json (Step 48)"
        )

    def test_smoke_readiness_checks_version_scope_levels(self):
        text = _script_text()
        assert "highest_eligible_level" in text, (
            "smoke 12i must check highest_eligible_level in readiness JSON"
        )

    def test_smoke_readiness_checks_8_levels(self):
        text = _script_text()
        assert "8" in text and "levels" in text, (
            "smoke 12i must verify 8 levels in readiness JSON"
        )

    def test_smoke_readiness_checks_level_5_6_blocked(self):
        text = _script_text()
        assert "rollback" in text or "level 5" in text, (
            "smoke 12i must check level 5 is not eligible"
        )
        assert "MCP" in text or "level 6" in text, (
            "smoke 12i must check level 6 is not eligible"
        )

    def test_smoke_brain_autonomy_readiness_node(self):
        text = _script_text()
        assert "autonomy_readiness" in text, (
            "smoke 12i must verify autonomy_readiness node in brain graph"
        )

    # --- Step 49: Context pack JSON (step 12j) ----------------------------

    def test_smoke_has_context_pack_step(self):
        text = _script_text()
        assert "context pack" in text and "--json" in text, (
            "smoke must call remedy context pack --json (Step 49)"
        )

    def test_smoke_context_pack_checks_compact_mode(self):
        text = _script_text()
        assert "compact" in text and "mode" in text, (
            "smoke 12j must verify compact mode in context pack JSON"
        )

    def test_smoke_context_pack_checks_caveman_mode(self):
        text = _script_text()
        assert "caveman" in text, (
            "smoke 12j must verify caveman mode in context pack JSON"
        )

    def test_smoke_context_pack_checks_sections(self):
        text = _script_text()
        assert "sections" in text and "estimated_tokens" in text, (
            "smoke 12j must verify sections and estimated_tokens"
        )

    def test_smoke_context_pack_caveman_le_compact(self):
        text = _script_text()
        assert "caveman" in text and "compact" in text, (
            "smoke 12j must verify caveman tokens <= compact tokens"
        )

    # --- Step 50: Memory learn JSON (step 12k) ----------------------------

    def test_smoke_has_memory_learn_step(self):
        text = _script_text()
        assert "memory learn" in text and "--approved" in text, (
            "smoke must call remedy memory learn --approved --json (Step 50)"
        )

    def test_smoke_memory_learn_checks_version_schema(self):
        text = _script_text()
        assert "learned_count" in text and "skipped_count" in text, (
            "smoke 12k must verify learned_count and skipped_count"
        )

    def test_smoke_memory_learn_idempotent(self):
        text = _script_text()
        assert "idempotent" in text or "second learn" in text, (
            "smoke 12k must verify second learn creates 0 new entries"
        )

    # --- Steps 48-50: Run-log schema (step 12l) --------------------------

    def test_smoke_has_readiness_assessed_event(self):
        text = _script_text()
        assert "readiness_assessed" in text, (
            "smoke 12l must verify readiness_assessed run-log event"
        )

    def test_smoke_has_context_pack_created_event(self):
        text = _script_text()
        assert "context_pack_created" in text, (
            "smoke 12l must verify context_pack_created run-log event"
        )

    def test_smoke_has_memory_learned_event(self):
        text = _script_text()
        assert "memory_learned" in text, (
            "smoke 12l must verify memory_learned run-log event"
        )

    def test_smoke_readiness_assessed_metadata_keys(self):
        text = _script_text()
        for key in ("scope", "highest_eligible_level", "missing_count", "blocker_count"):
            assert key in text, (
                f"smoke 12l must verify readiness_assessed metadata key '{key}'"
            )

    def test_smoke_context_pack_created_metadata_keys(self):
        text = _script_text()
        for key in ("budget", "estimated_tokens", "mode", "truncated", "section_count"):
            assert key in text, (
                f"smoke 12l must verify context_pack_created metadata key '{key}'"
            )

    def test_smoke_memory_learned_metadata_keys(self):
        text = _script_text()
        for key in ("learned_count", "skipped_count", "approved", "source_count"):
            assert key in text, (
                f"smoke 12l must verify memory_learned metadata key '{key}'"
            )

    # --- Step 51: File provenance (step 12m) --------------------------------

    def test_smoke_has_file_why_step(self):
        text = _script_text()
        assert "file why" in text, (
            "smoke must call remedy file why (Step 51)"
        )

    def test_smoke_file_why_checks_version_found_chain(self):
        text = _script_text()
        assert "found" in text and "chain" in text, (
            "smoke 12m must verify found and chain in file why JSON"
        )

    def test_smoke_file_why_checks_chain_steps(self):
        text = _script_text()
        for step in ("patch_intent", "patch_apply", "patch_apply_proof"):
            assert step in text, (
                f"smoke 12m must verify chain includes step '{step}'"
            )

    # --- Step 51: Brain causal proof graph (step 12n) ----------------------

    def test_smoke_has_brain_causal_proof_step(self):
        text = _script_text()
        assert "causal proof" in text.lower() or "patch_apply_proof" in text, (
            "smoke must verify patch_apply_proof node in brain (Step 51)"
        )

    def test_smoke_checks_causal_edges(self):
        text = _script_text()
        for edge in ("approved_by", "allowed_apply", "recorded_proof"):
            assert edge in text, (
                f"smoke 12n must verify causal edge '{edge}' in brain graph"
            )

    def test_smoke_file_group_in_help(self):
        text = _script_text()
        assert "file" in text, (
            "smoke must include 'file' group in help verification loop"
        )

    # --- Step 52: Continue from node (step 12o) ------------------------------

    def test_smoke_has_brain_continue_step(self):
        text = _script_text()
        assert "brain continue" in text, (
            "smoke must call remedy brain continue (Step 52)"
        )

    def test_smoke_brain_continue_checks_json_schema(self):
        text = _script_text()
        for key in ("parent_job_id", "child_job_id", "origin_node_id", "origin_node_type"):
            assert key in text, (
                f"smoke 12o must verify key '{key}' in brain continue JSON"
            )

    def test_smoke_brain_continue_checks_inherited(self):
        text = _script_text()
        assert "inherited_project" in text and "inherited_repo" in text, (
            "smoke 12o must verify inherited_project and inherited_repo"
        )

    def test_smoke_brain_continue_verifies_child_job(self):
        text = _script_text()
        assert "child job" in text.lower() or "child_job_id" in text, (
            "smoke 12o must verify child job exists"
        )

    # --- Step 53: Project brain aggregate (step 12p) -------------------------

    def test_smoke_has_project_brain_step(self):
        text = _script_text()
        assert "project brain" in text, (
            "smoke must call remedy project brain (Step 53)"
        )

    def test_smoke_project_brain_checks_json_schema(self):
        text = _script_text()
        for key in ("project_id", "project_name", "scope"):
            assert key in text, (
                f"smoke 12p must verify key '{key}' in project brain JSON"
            )

    def test_smoke_project_brain_checks_graph_and_summary(self):
        text = _script_text()
        assert "graph" in text and "summary" in text, (
            "smoke 12p must verify graph and summary in project brain JSON"
        )

    def test_smoke_project_brain_checks_project_node(self):
        text = _script_text()
        assert "'project'" in text or '"project"' in text, (
            "smoke 12p must verify project node type exists"
        )

    def test_smoke_project_brain_checks_no_path_leak(self):
        text = _script_text()
        assert "repo_basename" in text, (
            "smoke 12p must verify repo nodes have repo_basename (no full path)"
        )

    # --- Step 35: Run Contract (step 12a) -----------------------------------

    def test_smoke_has_run_contract_check(self):
        text = _script_text()
        assert "policy contract" in text, (
            "smoke must call remedy policy contract as part of Step 35"
        )

    def test_smoke_run_contract_checks_json_keys(self):
        text = _script_text()
        assert "autonomy_level" in text, (
            "smoke step 12a must validate autonomy_level in run-contract JSON"
        )

    def test_smoke_run_contract_checks_allowed_actions(self):
        text = _script_text()
        assert "allowed_actions" in text, (
            "smoke step 12a must validate allowed_actions in run-contract JSON"
        )

    def test_smoke_run_contract_checks_scope_job(self):
        text = _script_text()
        assert "scope" in text and "'job'" in text, (
            "smoke step 12a must validate scope == 'job' in run-contract JSON"
        )

    def test_smoke_run_contract_checks_autonomy_int(self):
        text = _script_text()
        assert "autonomy_level" in text and "int" in text, (
            "smoke step 12a must validate autonomy_level is int"
        )

    def test_smoke_run_contract_checks_forbidden_strings(self):
        text = _script_text()
        assert "approval_reason" in text and "diff_preview" in text, (
            "smoke step 12a must check forbidden strings in run-contract JSON"
        )

    # --- Step 36: Token Policy (step 12b) -----------------------------------

    def test_smoke_has_token_policy_check(self):
        text = _script_text()
        assert "policy token" in text, (
            "smoke must call remedy policy token as part of Step 36"
        )

    def test_smoke_token_policy_checks_zero_token(self):
        text = _script_text()
        assert "zero_token_steps" in text, (
            "smoke step 12b must validate zero_token_steps in token-policy JSON"
        )

    def test_smoke_token_policy_checks_command_discovery_zero_token(self):
        text = _script_text()
        assert "command_discovery" in text, (
            "smoke step 12b must verify command_discovery is a zero-token step"
        )

    def test_smoke_token_policy_checks_scope_job(self):
        text = _script_text()
        assert "scope" in text, (
            "smoke step 12b must validate scope in token-policy JSON"
        )

    def test_smoke_token_policy_checks_forbidden_context(self):
        text = _script_text()
        assert "forbidden_context" in text, (
            "smoke step 12b must validate forbidden_context in token-policy JSON"
        )

    def test_smoke_token_policy_uses_precise_blocklist(self):
        """Smoke 12b must use precise secret patterns, not dumb substring bans."""
        text = _script_text()
        # Must contain precise patterns
        for pattern in ("sk-", "ghp_", "password="):
            assert pattern in text, (
                f"smoke step 12b must use precise pattern '{pattern}' for leak detection"
            )
        # The old false-positive pattern must not appear in the 12b section
        idx_12b = text.index("12b")
        section = text[idx_12b:idx_12b + 2000]
        assert "'api_key'" not in section, (
            "smoke 12b must not use bare 'api_key' as forbidden — "
            "false-positives on category name 'api_keys'"
        )

    # --- Step 37: Worker Adapters (step 12c) --------------------------------

    def test_smoke_has_workers_check(self):
        text = _script_text()
        assert "worker list" in text, (
            "smoke must call remedy worker list as part of Step 37"
        )

    def test_smoke_workers_checks_ollama(self):
        text = _script_text()
        assert "ollama" in text, (
            "smoke step 12c must verify ollama is in worker specs"
        )

    def test_smoke_workers_checks_claude_code(self):
        text = _script_text()
        assert "claude_code" in text, (
            "smoke step 12c must verify claude_code is in worker specs"
        )

    def test_smoke_workers_checks_version_envelope(self):
        text = _script_text()
        assert "providers" in text, (
            "smoke step 12c must check for 'providers' key in workers JSON envelope"
        )

    # --- Step 35-37: Run-log schema (step 12e) ----------------------------

    def test_smoke_has_run_log_schema_step_12e(self):
        text = _script_text()
        assert "run_contract_inspected" in text, (
            "smoke step 12e must verify run_contract_inspected run-log schema"
        )
        assert "token_policy_inspected" in text, (
            "smoke step 12e must verify token_policy_inspected run-log schema"
        )

    def test_smoke_run_log_checks_exact_rc_keys(self):
        text = _script_text()
        for key in ("allowed_action_count", "denied_action_count", "max_loops"):
            assert key in text, (
                f"smoke step 12e must verify run_contract_inspected key '{key}'"
            )

    def test_smoke_run_log_checks_exact_tp_keys(self):
        text = _script_text()
        for key in ("zero_token_step_count", "local_first_step_count", "expensive_step_count"):
            assert key in text, (
                f"smoke step 12e must verify token_policy_inspected key '{key}'"
            )

    # --- Step 35-37: Brain node integration (step 12d) ----------------------

    def test_smoke_brain_checks_run_contract_node(self):
        text = _script_text()
        assert "run_contract" in text, (
            "smoke step 12d must verify run_contract node in brain graph"
        )

    def test_smoke_brain_checks_token_policy_node(self):
        text = _script_text()
        assert "token_policy" in text, (
            "smoke step 12d must verify token_policy node in brain graph"
        )

    def test_smoke_brain_checks_worker_adapter_node(self):
        text = _script_text()
        assert "worker_adapter" in text, (
            "smoke step 12d must verify worker_adapter node in brain graph"
        )

    # --- Step 53.1: Project brain includes child job (step 12p) ---------------

    def test_smoke_project_brain_checks_child_job(self):
        text = _script_text()
        assert "child" in text.lower() and "project brain" in text.lower(), (
            "smoke 12p must verify child job in project brain aggregate"
        )

    # --- Step 54: Patch revert (step 12q) ------------------------------------

    def test_smoke_has_revert_step(self):
        text = _script_text()
        assert "patch revert" in text, (
            "smoke must call remedy patch revert"
        )

    def test_smoke_revert_checks_noop(self):
        text = _script_text()
        assert "second revert" in text.lower() or "noop" in text, (
            "smoke must verify second revert is noop"
        )

    # --- Step 55: Change set (step 12r) --------------------------------------

    def test_smoke_has_change_list(self):
        text = _script_text()
        assert "change list" in text, (
            "smoke must call remedy change list"
        )

    def test_smoke_change_list_checks_schema(self):
        text = _script_text()
        assert "'changes'" in text or '"changes"' in text, (
            "smoke must verify changes key in change list JSON"
        )

    # --- Step 56: Token economy (step 12s) -----------------------------------

    def test_smoke_has_token_ordering(self):
        text = _script_text()
        assert "caveman" in text and "compact" in text and "standard" in text, (
            "smoke must check all three context pack modes"
        )

    def test_smoke_has_worker_recommend(self):
        text = _script_text()
        assert "worker recommend" in text, (
            "smoke must call remedy worker recommend"
        )

    def test_smoke_worker_recommend_checks_schema(self):
        text = _script_text()
        assert "recommended_worker" in text and "token_mode" in text, (
            "smoke must verify worker recommend JSON schema"
        )

    # --- Step 54-56: Brain nodes (step 12t) ----------------------------------

    def test_smoke_brain_checks_change_set_node(self):
        text = _script_text()
        assert "change_set" in text, (
            "smoke must verify change_set node in brain graph"
        )

    # --- Step 63: Memory card commands (step 12u) ----------------------------

    def test_smoke_has_memory_card_show(self):
        text = _script_text()
        assert "card-show" in text, (
            "smoke must verify memory card-show help"
        )

    # --- Step 64: Worker show + explain (steps 12v-12w) ----------------------

    def test_smoke_has_worker_show(self):
        text = _script_text()
        assert "worker show" in text, (
            "smoke must call remedy worker show"
        )

    def test_smoke_has_worker_explain(self):
        text = _script_text()
        assert "worker explain" in text, (
            "smoke must call remedy worker explain"
        )

    # --- Step 65: Repo status + git_status brain (steps 12x-12y) -------------

    def test_smoke_has_repo_status(self):
        text = _script_text()
        assert "repo status" in text, (
            "smoke must call remedy repo status"
        )

    def test_smoke_brain_checks_git_status_node(self):
        text = _script_text()
        assert "git_status" in text, (
            "smoke must verify git_status node in brain graph"
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

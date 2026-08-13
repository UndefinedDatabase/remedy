"""Tests for diff_repair_response.py (F111 T002, response half).

Covers the five public entry points: the wrapper decode with its named
rejection reasons, the validation with its declared-files/touched-paths
cross-check and its delegated path-safety messages, the non-raising fence
pre-check that answers with data rather than an exception, the blank-context
normalisation that survives a transport stripping a lone trailing space, and
the conversion into the ``StructuredPatch`` the existing applicator takes.

The path-safety assertions deliberately name the exact message strings
`structured_patch.unsafe_path_issues` produces, so a future reword of those
strings fails here instead of drifting silently.

repo_root is a bare tmp_path: no git init, no fixtures beyond tmp_path,
matching tests/orchestration/test_diff_repair.py.
"""

from __future__ import annotations

import json

from packages.orchestration.diff_repair_response import (
    DIFF_REPAIR_RESPONSE_FORMAT,
    DIFF_REPAIR_RESPONSE_VERSION,
    DiffRepairResponse,
    diff_repair_response_to_patch,
    normalize_diff_blank_context,
    parse_diff_repair_response,
    precheck_diff_repair_fences,
    validate_diff_repair_response,
)
from packages.orchestration.structured_patch import validate_structured_patch

# One file, one hunk — the smallest well-formed repair diff.
DIFF_ONE_FILE = (
    "--- a/src/app.py\n"
    "+++ b/src/app.py\n"
    "@@ -1,3 +1,3 @@\n"
    " import os\n"
    "-value = 1\n"
    "+value = 2\n"
)

# The same diff plus a second file, used for the undeclared-path cross-check.
DIFF_TWO_FILES = DIFF_ONE_FILE + (
    "--- a/src/util.py\n"
    "+++ b/src/util.py\n"
    "@@ -10,2 +10,2 @@\n"
    "-helper = 1\n"
    "+helper = 2\n"
)


def _record(**overrides) -> dict:
    """Build a well-formed response dict, with named fields overridden."""
    data = {
        "format": DIFF_REPAIR_RESPONSE_FORMAT,
        "version": DIFF_REPAIR_RESPONSE_VERSION,
        "diff": DIFF_ONE_FILE,
        "files": ["src/app.py"],
    }
    data.update(overrides)
    return data


def _fenced(data: dict) -> str:
    """Wrap a record in a ```json fenced block, as a model would emit it."""
    return "Here is the fix:\n\n```json\n" + json.dumps(data) + "\n```\n"


# ═══════════════════════════════════════════════════════════════════════════
# parse_diff_repair_response — locating and decoding the wrapper
# ═══════════════════════════════════════════════════════════════════════════


class TestParseDiffRepairResponse:
    """The decode returns a record or a named reason, never a bare None."""

    def test_fenced_json_block(self):
        response, reason = parse_diff_repair_response(_fenced(_record()))
        assert reason == ""
        assert response == DiffRepairResponse(
            diff=DIFF_ONE_FILE,
            files=("src/app.py",),
            format=DIFF_REPAIR_RESPONSE_FORMAT,
            version=DIFF_REPAIR_RESPONSE_VERSION,
        )

    def test_bare_object(self):
        response, reason = parse_diff_repair_response(json.dumps(_record()))
        assert reason == ""
        assert response is not None
        assert response.files == ("src/app.py",)
        assert response.diff == DIFF_ONE_FILE

    def test_bare_object_with_trailing_prose(self):
        raw = json.dumps(_record()) + "\n\nThat should do it."
        response, reason = parse_diff_repair_response(raw)
        assert reason == ""
        assert response is not None
        assert response.files == ("src/app.py",)

    def test_prose_only_reports_no_json_object(self):
        response, reason = parse_diff_repair_response(
            "I could not produce a diff for this failure."
        )
        assert response is None
        assert reason == "no_json_object"

    def test_broken_json_in_fence_reports_invalid_json(self):
        raw = '```json\n{"format": "unified_diff", "version": 1, "diff": }\n```\n'
        response, reason = parse_diff_repair_response(raw)
        assert response is None
        assert reason == "invalid_json"

    def test_missing_format_field(self):
        data = _record()
        del data["format"]
        response, reason = parse_diff_repair_response(json.dumps(data))
        assert response is None
        assert reason == "missing_field:format"

    def test_missing_version_field(self):
        data = _record()
        del data["version"]
        response, reason = parse_diff_repair_response(json.dumps(data))
        assert response is None
        assert reason == "missing_field:version"

    def test_missing_diff_field(self):
        data = _record()
        del data["diff"]
        response, reason = parse_diff_repair_response(json.dumps(data))
        assert response is None
        assert reason == "missing_field:diff"

    def test_missing_files_field(self):
        data = _record()
        del data["files"]
        response, reason = parse_diff_repair_response(json.dumps(data))
        assert response is None
        assert reason == "missing_field:files"

    def test_wrong_format_reports_the_value(self):
        response, reason = parse_diff_repair_response(
            json.dumps(_record(format="file_ops"))
        )
        assert response is None
        assert reason == "wrong_format:file_ops"

    def test_unsupported_version_reports_the_value(self):
        response, reason = parse_diff_repair_response(
            json.dumps(_record(version=2))
        )
        assert response is None
        assert reason == "unsupported_version:2"

    def test_files_as_a_string_is_rejected(self):
        response, reason = parse_diff_repair_response(
            json.dumps(_record(files="src/app.py"))
        )
        assert response is None
        assert reason == "files_not_a_list"


# ═══════════════════════════════════════════════════════════════════════════
# validate_diff_repair_response — the declared-files cross-check
# ═══════════════════════════════════════════════════════════════════════════


class TestValidateDiffRepairResponse:
    """What the model declares must be exactly what the diff touches."""

    def test_declared_list_equal_to_touched_paths_is_valid(self):
        response = DiffRepairResponse(
            diff=DIFF_TWO_FILES, files=("src/app.py", "src/util.py")
        )
        assert validate_diff_repair_response(response) == []

    def test_diff_touching_an_undeclared_path(self):
        response = DiffRepairResponse(diff=DIFF_TWO_FILES, files=("src/app.py",))
        assert validate_diff_repair_response(response) == [
            "diff touches undeclared path: src/util.py"
        ]

    def test_declared_path_the_diff_never_touches(self):
        response = DiffRepairResponse(
            diff=DIFF_ONE_FILE, files=("src/app.py", "src/util.py")
        )
        assert validate_diff_repair_response(response) == [
            "declared path not touched by the diff: src/util.py"
        ]

    def test_empty_diff(self):
        response = DiffRepairResponse(diff="   \n  ", files=("src/app.py",))
        assert "empty diff" in validate_diff_repair_response(response)

    def test_empty_files_list(self):
        response = DiffRepairResponse(diff=DIFF_ONE_FILE, files=())
        assert "empty files list" in validate_diff_repair_response(response)

    def test_absolute_declared_path_carries_the_shared_message(self):
        response = DiffRepairResponse(diff=DIFF_ONE_FILE, files=("/etc/passwd",))
        assert (
            "absolute path not allowed: /etc/passwd"
            in validate_diff_repair_response(response)
        )

    def test_dot_dot_declared_path_carries_the_shared_message(self):
        response = DiffRepairResponse(diff=DIFF_ONE_FILE, files=("../outside.py",))
        assert (
            "path traversal not allowed: ../outside.py"
            in validate_diff_repair_response(response)
        )

    def test_dotenv_declared_path_carries_the_shared_message(self):
        response = DiffRepairResponse(diff=DIFF_ONE_FILE, files=("config/.env",))
        assert (
            "sensitive file not allowed: config/.env"
            in validate_diff_repair_response(response)
        )


# ═══════════════════════════════════════════════════════════════════════════
# precheck_diff_repair_fences — the fence decision as data
# ═══════════════════════════════════════════════════════════════════════════


class TestPrecheckDiffRepairFences:
    """An out-of-fence path is a rejection value, never a raised exception."""

    def test_ordinary_path_is_allowed_under_default_fences(self, tmp_path):
        response = DiffRepairResponse(diff=DIFF_ONE_FILE, files=("src/app.py",))
        precheck = precheck_diff_repair_fences(tmp_path, response)
        assert precheck.allowed is True
        assert precheck.denied_paths == ()
        assert precheck.reasons == ()

    def test_builtin_denied_path_is_rejected_with_a_reason(self, tmp_path):
        response = DiffRepairResponse(diff=DIFF_ONE_FILE, files=("remedy.toml",))
        precheck = precheck_diff_repair_fences(tmp_path, response)
        assert precheck.allowed is False
        assert precheck.denied_paths == ("remedy.toml",)
        assert len(precheck.reasons) == 1
        path, reason = precheck.reasons[0]
        assert path == "remedy.toml"
        assert reason

    def test_path_outside_the_job_allow_glob_is_rejected(self, tmp_path):
        response = DiffRepairResponse(diff=DIFF_ONE_FILE, files=("docs/guide.md",))
        precheck = precheck_diff_repair_fences(
            tmp_path, response, job_fences={"allow": ["src/**"], "deny": []}
        )
        assert precheck.allowed is False
        assert precheck.denied_paths == ("docs/guide.md",)


# ═══════════════════════════════════════════════════════════════════════════
# normalize_diff_blank_context — the stripped blank context line (R-0313)
# ═══════════════════════════════════════════════════════════════════════════


class TestNormalizeDiffBlankContext:
    """A blank context line stripped to "" is body only while the budget says so."""

    def test_blank_context_line_inside_a_hunk_regains_its_space(self):
        # The R-0313 input: `_apply_hunks` returns None on the left-hand text
        # and applies cleanly on the right-hand one.
        assert normalize_diff_blank_context(
            "@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n"
        ) == "@@ -1,3 +1,3 @@\n a\n \n-b\n+B\n"

    def test_diff_needing_no_repair_is_byte_identical(self):
        # Byte-identity, not merely equality of content: the trailing newline
        # must survive, because `diff_repair_response_to_patch` splits the
        # NORMALISED text and the section assertions below compare exact bytes.
        assert normalize_diff_blank_context(DIFF_ONE_FILE) == DIFF_ONE_FILE

    def test_blank_line_between_two_file_sections_is_untouched(self):
        """A separator between file sections is not hunk body, so it keeps no space.

        R-0317: the shared DIFF_ONE_FILE constant declares `@@ -1,3 +1,3 @@`
        over a body that spends only two old and two new lines, so it is exactly
        the over-declared shape whose leftover budget used to convert the
        separator into a context line, and asserting identity on it is the
        regression pin.
        """
        second = (
            "--- a/src/util.py\n"
            "+++ b/src/util.py\n"
            "@@ -10,2 +10,2 @@\n"
            "-helper = 1\n"
            "+helper = 2\n"
        )
        between = DIFF_ONE_FILE + "\n" + second
        assert normalize_diff_blank_context(between) == between

    def test_blank_with_unspent_budget_at_end_of_input_stays_blank(self):
        # The header still has one old and one new line left at the final "",
        # but nothing follows it, so nothing identifies it as body: the safe
        # reading leaves it alone rather than guessing a context line (R-0317).
        trailing = "@@ -1,3 +1,3 @@\n a\n-b\n+B\n\n"
        assert normalize_diff_blank_context(trailing) == trailing

    def test_blank_after_the_hunk_budget_is_spent_stays_blank(self):
        # The counters reach zero at "+B", so the "" that follows is the text
        # AFTER the hunk and is left exactly as the model sent it.
        spent = "@@ -1,2 +1,2 @@\n a\n-b\n+B\n\n"
        result = normalize_diff_blank_context(spent)
        assert result == spent
        assert result.splitlines()[-1] == ""


# ═══════════════════════════════════════════════════════════════════════════
# diff_repair_response_to_patch — one UnifiedDiff per declared path
# ═══════════════════════════════════════════════════════════════════════════


class TestDiffRepairResponseToPatch:
    """The conversion the applicator consumes: per-path sections, never the whole diff."""

    def test_single_file_response_converts_to_one_unified_diff(self):
        response = DiffRepairResponse(diff=DIFF_ONE_FILE, files=("src/app.py",))
        patch = diff_repair_response_to_patch(response)

        assert patch.intent_kind == "unified_diff"
        assert patch.target_paths == ("src/app.py",)
        assert patch.applicability == "applicable"
        assert patch.requires_approval is True

        assert len(patch.unified_diffs) == 1
        only = patch.unified_diffs[0]
        assert only.path == "src/app.py"
        assert only.diff == DIFF_ONE_FILE.rstrip("\n")

    def test_two_file_response_gives_each_path_only_its_own_section(self):
        response = DiffRepairResponse(
            diff=DIFF_TWO_FILES, files=("src/app.py", "src/util.py")
        )
        patch = diff_repair_response_to_patch(response)

        assert [d.path for d in patch.unified_diffs] == ["src/app.py", "src/util.py"]
        app_diff, util_diff = (d.diff for d in patch.unified_diffs)

        assert "src/util.py" not in app_diff
        assert "helper" not in app_diff
        assert "src/app.py" not in util_diff
        assert "value = 2" not in util_diff
        assert app_diff.startswith("--- a/src/app.py\n")
        assert util_diff.startswith("--- a/src/util.py\n")

    def test_declared_path_the_diff_never_touches_is_an_empty_diff(self):
        # Fail-closed by construction: the empty section is what
        # validate_structured_patch names, instead of a silent no-op apply.
        response = DiffRepairResponse(
            diff=DIFF_ONE_FILE, files=("src/app.py", "src/ghost.py")
        )
        patch = diff_repair_response_to_patch(response)

        ghost = [d for d in patch.unified_diffs if d.path == "src/ghost.py"]
        assert len(ghost) == 1
        assert ghost[0].diff == ""
        assert validate_structured_patch(patch) == [
            "unified_diff src/ghost.py: empty diff"
        ]

    def test_valid_response_converts_to_a_patch_the_validator_accepts(self):
        response = DiffRepairResponse(
            diff=DIFF_TWO_FILES, files=("src/app.py", "src/util.py")
        )
        assert validate_diff_repair_response(response) == []
        assert validate_structured_patch(diff_repair_response_to_patch(response)) == []

"""
Tests for packages/orchestration/path_utils.py — Step 32: Repository Structure Foundation.

Verifies:
- sanitize_path_component behavior matches the previous local implementations exactly
- the regex and max-length constant appear only once in production code
"""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.path_utils import sanitize_path_component


class TestSanitizePathComponent:
    def test_preserves_lowercase_letters(self):
        assert sanitize_path_component("abc") == "abc"

    def test_preserves_uppercase_letters(self):
        assert sanitize_path_component("ABC") == "ABC"

    def test_preserves_digits(self):
        assert sanitize_path_component("123") == "123"

    def test_preserves_underscore(self):
        assert sanitize_path_component("a_b") == "a_b"

    def test_preserves_hyphen(self):
        assert sanitize_path_component("a-b") == "a-b"

    def test_preserves_mixed_safe(self):
        assert sanitize_path_component("write_readme") == "write_readme"
        assert sanitize_path_component("my-task-type") == "my-task-type"
        assert sanitize_path_component("Task42_v2") == "Task42_v2"

    def test_replaces_slash(self):
        assert sanitize_path_component("a/b") == "a_b"

    def test_replaces_dot(self):
        assert sanitize_path_component("a.b") == "a_b"

    def test_replaces_space(self):
        assert sanitize_path_component("a b") == "a_b"

    def test_replaces_colon(self):
        assert sanitize_path_component("a:b") == "a_b"

    def test_replaces_unicode_punctuation(self):
        result = sanitize_path_component("héllo")
        # 'é' is not in [a-zA-Z0-9_-], so it should be replaced
        assert "é" not in result

    def test_strips_leading_underscore(self):
        assert sanitize_path_component("_abc") == "abc"

    def test_strips_trailing_underscore(self):
        assert sanitize_path_component("abc_") == "abc"

    def test_strips_leading_and_trailing_underscore_from_traversal(self):
        # "../escape" → "_..escape" but ".." becomes "__", strip → "escape"
        result = sanitize_path_component("../escape")
        assert result == "escape"

    def test_truncates_to_48_characters(self):
        long = "a" * 60
        result = sanitize_path_component(long)
        assert len(result) == 48
        assert result == "a" * 48

    def test_truncation_before_strip(self):
        # value that would produce underscores at boundary after truncation
        value = "abc_" + "a" * 44 + "_def"
        result = sanitize_path_component(value)
        assert len(result) <= 48

    def test_returns_unknown_for_empty(self):
        assert sanitize_path_component("") == "unknown"

    def test_returns_unknown_for_only_dots(self):
        assert sanitize_path_component("...") == "unknown"

    def test_returns_unknown_for_only_slashes(self):
        assert sanitize_path_component("///") == "unknown"

    def test_returns_unknown_when_all_chars_replaced(self):
        # All non-safe chars → all underscores → stripped → empty → "unknown"
        assert sanitize_path_component("...") == "unknown"

    def test_result_max_48_chars(self):
        # Should never exceed 48 chars for any input
        for val in ["x" * 100, "a" * 48, "hello world", "../../evil", ""]:
            result = sanitize_path_component(val)
            assert len(result) <= 48, f"Result too long for {val!r}: {result!r}"

    def test_result_contains_only_safe_chars(self):
        import re
        safe_re = re.compile(r"^[a-zA-Z0-9_-]+$")
        for val in ["write_readme", "a/b/c", "../../evil", "hello world", "täsk"]:
            result = sanitize_path_component(val)
            if result != "unknown":
                assert safe_re.match(result), f"Unsafe chars in result for {val!r}: {result!r}"


class TestSingleImplementationInvariant:
    """Verify the regex and max-length constant appear only once in production code."""

    def _find_repo_root(self) -> Path:
        from packages.orchestration import path_utils
        return Path(path_utils.__file__).resolve().parents[2]

    def test_regex_appears_once_in_production(self):
        import re
        repo = self._find_repo_root()
        needle = re.compile(r'\[\^a-zA-Z0-9_-\]')
        matches = []
        for p in (repo / "packages").rglob("*.py"):
            if "test_" in p.name or "__pycache__" in str(p):
                continue
            text = p.read_text()
            if needle.search(text):
                matches.append(str(p.relative_to(repo)))
        assert matches == ["packages/orchestration/path_utils.py"], (
            f"Regex [^a-zA-Z0-9_-] found in unexpected files: {matches}"
        )

    def test_max_length_48_appears_once_in_production(self):
        repo = self._find_repo_root()
        # Look for "_MAX_PATH_COMPONENT_LENGTH = 48" or "48" as a bare constant
        # We check for the specific constant name, not just the digit "48".
        matches = []
        for p in (repo / "packages").rglob("*.py"):
            if "test_" in p.name or "__pycache__" in str(p):
                continue
            text = p.read_text()
            if "_MAX_PATH_COMPONENT_LENGTH" in text:
                matches.append(str(p.relative_to(repo)))
        assert matches == ["packages/orchestration/path_utils.py"], (
            f"_MAX_PATH_COMPONENT_LENGTH found in unexpected files: {matches}"
        )

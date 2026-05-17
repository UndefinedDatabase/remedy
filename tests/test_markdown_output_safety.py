"""Tests for the shared Markdown output-boundary safety helper."""

import pytest

from packages.orchestration.markdown_output_safety import (
    HTML_COMMENT_START,
    HTML_COMMENT_START_SAFE,
    neutralize_markdown_html_comment_start,
)


class TestConstants:
    def test_html_comment_start_value(self):
        assert HTML_COMMENT_START == "<!--"

    def test_html_comment_start_safe_value(self):
        assert HTML_COMMENT_START_SAFE == "&lt;!--"

    def test_safe_form_does_not_contain_raw_start(self):
        assert HTML_COMMENT_START not in HTML_COMMENT_START_SAFE


class TestNeutralizeMarkdownHtmlCommentStart:
    def test_neutralizes_generic_comment(self):
        result = neutralize_markdown_html_comment_start("<!-- generic comment -->")
        assert result == "&lt;!-- generic comment -->"

    def test_neutralizes_remedy_specific_marker(self):
        result = neutralize_markdown_html_comment_start("<!-- remedy:patch-intent FAKE begin -->")
        assert result == "&lt;!-- remedy:patch-intent FAKE begin -->"

    def test_neutralizes_multiple_occurrences(self):
        result = neutralize_markdown_html_comment_start("<!-- a --> text <!-- b -->")
        assert result == "&lt;!-- a --> text &lt;!-- b -->"
        assert "<!--" not in result

    def test_leaves_already_safe_form_unchanged(self):
        already_safe = "&lt;!-- already neutralized -->"
        result = neutralize_markdown_html_comment_start(already_safe)
        assert result == already_safe

    def test_does_not_double_encode(self):
        # "&lt;!--" contains no "<!--" so a second pass must leave it intact
        safe = "&lt;!-- once -->"
        result = neutralize_markdown_html_comment_start(safe)
        assert result == safe

    def test_leaves_plain_text_unchanged(self):
        result = neutralize_markdown_html_comment_start("just plain text")
        assert result == "just plain text"

    def test_empty_string(self):
        assert neutralize_markdown_html_comment_start("") == ""

    def test_coerces_non_string_input(self):
        # The function accepts object and coerces to str
        result = neutralize_markdown_html_comment_start(42)
        assert result == "42"

    def test_coerces_none_to_string(self):
        result = neutralize_markdown_html_comment_start(None)
        assert result == "None"

    def test_raw_html_comment_absent_from_result(self):
        inputs = [
            "<!-- a -->",
            "prefix <!-- comment --> suffix",
            "<!--no-space-->",
            "<!-- remedy:patch-intent x begin -->",
        ]
        for inp in inputs:
            assert "<!--" not in neutralize_markdown_html_comment_start(inp)

    def test_result_is_always_str(self):
        assert isinstance(neutralize_markdown_html_comment_start("text"), str)
        assert isinstance(neutralize_markdown_html_comment_start(0), str)

"""
Unit tests for apps/cli/help_renderer.py — Bootcamp-style Unicode box renderer.

Tests: box alignment, render functions, edge cases.
"""

from __future__ import annotations

from apps.cli.help_renderer import (
    BOX_WIDTH,
    _box,
    render_command_help,
    render_error,
    render_group_help,
    render_root_help,
)


class TestBoxAlignment:
    """All box lines must have exactly BOX_WIDTH + 2 visible characters."""

    def _line_lengths(self, box_text: str) -> list[int]:
        return [len(line) for line in box_text.splitlines()]

    def test_options_box_aligned(self) -> None:
        text = _box("Options", [("--help", "Show this message and exit.")])
        lengths = self._line_lengths(text)
        assert all(l == BOX_WIDTH + 2 for l in lengths), lengths

    def test_commands_box_aligned(self) -> None:
        rows = [("job", "Create jobs."), ("project", "Manage projects.")]
        text = _box("Commands", rows)
        lengths = self._line_lengths(text)
        assert all(l == BOX_WIDTH + 2 for l in lengths), lengths

    def test_single_row_box_aligned(self) -> None:
        text = _box("X", [("a", "b")])
        lengths = self._line_lengths(text)
        assert all(l == BOX_WIDTH + 2 for l in lengths), lengths

    def test_empty_box_aligned(self) -> None:
        text = _box("Empty", [])
        lengths = self._line_lengths(text)
        assert all(l == BOX_WIDTH + 2 for l in lengths), lengths

    def test_long_title_box_aligned(self) -> None:
        text = _box("A" * 40, [("x", "y")])
        lengths = self._line_lengths(text)
        assert all(l == BOX_WIDTH + 2 for l in lengths), lengths

    def test_long_content_truncated(self) -> None:
        text = _box("Test", [("x" * 40, "y" * 50)])
        for line in text.splitlines():
            assert len(line) == BOX_WIDTH + 2, f"Line too long: {len(line)}"


class TestBoxStructure:
    """Box must have correct Unicode corner characters."""

    def test_corners(self) -> None:
        text = _box("Test", [("a", "b")])
        lines = text.splitlines()
        assert lines[0][0] == "\u256d"  # top-left
        assert lines[0][-1] == "\u256e"  # top-right
        assert lines[-1][0] == "\u2570"  # bottom-left
        assert lines[-1][-1] == "\u256f"  # bottom-right

    def test_content_bars(self) -> None:
        text = _box("Test", [("a", "b")])
        lines = text.splitlines()
        for line in lines[1:-1]:
            assert line[0] == "\u2502"  # left bar
            assert line[-1] == "\u2502"  # right bar


class TestRenderRootHelp:
    def test_contains_usage(self) -> None:
        result = render_root_help("remedy", "Test description", [("job", "Jobs")])
        assert "Usage: remedy" in result

    def test_contains_commands(self) -> None:
        result = render_root_help("remedy", "Desc", [("job", "Jobs"), ("brain", "Brain")])
        assert "Commands" in result
        assert "job" in result
        assert "brain" in result

    def test_contains_options(self) -> None:
        result = render_root_help("remedy", "Desc", [])
        assert "Options" in result
        assert "--help" in result


class TestRenderGroupHelp:
    def test_contains_usage(self) -> None:
        result = render_group_help("remedy", "job", "Manage jobs.", [("create", "Create")])
        assert "Usage: remedy job" in result

    def test_contains_commands(self) -> None:
        result = render_group_help("remedy", "brain", "Brain.", [("graph", "Graph"), ("node", "Node")])
        assert "graph" in result
        assert "node" in result

    def test_contains_hint(self) -> None:
        result = render_group_help("remedy", "job", "Jobs.", [("create", "Create")])
        assert "remedy job <command> --help" in result


class TestRenderCommandHelp:
    def test_contains_usage(self) -> None:
        result = render_command_help("remedy", "job", "create", "Create a job.", [("prompt", "What")], [("--project", "UUID")])
        assert "Usage: remedy job create" in result
        assert "PROMPT" in result

    def test_contains_arguments(self) -> None:
        result = render_command_help("remedy", "patch", "apply", "Apply.", [("job_id", "UUID"), ("intent_id", "ID")], [])
        assert "Arguments" in result
        assert "job_id" in result
        assert "intent_id" in result

    def test_no_arguments_box_if_none(self) -> None:
        result = render_command_help("remedy", "job", "list", "List.", [], [])
        assert "Arguments" not in result

    def test_contains_options(self) -> None:
        result = render_command_help("remedy", "brain", "graph", "Graph.", [("job_id", "UUID")], [("--json", "JSON")])
        assert "--json" in result
        assert "--help" in result


class TestRenderError:
    def test_contains_error(self) -> None:
        result = render_error("remedy", "Unknown command 'foo'.")
        assert "Error:" in result
        assert "foo" in result

    def test_contains_usage(self) -> None:
        result = render_error("remedy job", "Bad command.")
        assert "Usage: remedy job" in result

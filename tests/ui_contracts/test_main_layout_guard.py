"""Guard: main column has exactly four primary areas.

Prevents regressions like PipelinePanel becoming a fifth main-column row.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SHELL_TSX = ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.tsx"
SHELL_CSS = ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.module.css"


class TestMainColumnStructure:
    def test_shell_main_has_four_children(self):
        content = SHELL_TSX.read_text()
        main_match = re.search(
            r"<main[^>]*className=\{styles\.main\}[^>]*>(.*?)</main>",
            content, re.DOTALL,
        )
        assert main_match, "Could not find <main className={styles.main}> in RemedyShell.tsx"
        main_body = main_match.group(1)
        components = re.findall(r"<([A-Z]\w+)", main_body)
        assert len(components) == 4, (
            f"Main column should have exactly 4 children, found {len(components)}: {components}. "
            "If adding a component, place it in the right panel or a detail popover."
        )

    def test_shell_main_expected_components(self):
        content = SHELL_TSX.read_text()
        main_match = re.search(
            r"<main[^>]*className=\{styles\.main\}[^>]*>(.*?)</main>",
            content, re.DOTALL,
        )
        assert main_match
        main_body = main_match.group(1)
        expected = ["TopMetricsBar", "CommandBar", "BrainGraphStage", "PhaseTimeline"]
        for name in expected:
            assert name in main_body, f"Expected {name} in main column"

    def test_shell_main_no_pipeline_panel(self):
        content = SHELL_TSX.read_text()
        main_match = re.search(
            r"<main[^>]*className=\{styles\.main\}[^>]*>(.*?)</main>",
            content, re.DOTALL,
        )
        assert main_match
        main_body = main_match.group(1)
        assert "PipelinePanel" not in main_body, "PipelinePanel must not be in main column"

    def test_css_main_grid_four_rows(self):
        content = SHELL_CSS.read_text()
        main_match = re.search(r"\.main\s*\{([^}]+)\}", content)
        assert main_match, "Could not find .main CSS rule"
        main_css = main_match.group(1)
        rows_match = re.search(r"grid-template-rows:\s*([\s\S]*?);", main_css)
        assert rows_match, "Could not find grid-template-rows in .main"
        rows_str = rows_match.group(1)
        rows = re.findall(r"(?:clamp|minmax)\([^)]+\)", rows_str)
        assert len(rows) == 4, (
            f"Main grid should define exactly 4 row sizes, found {len(rows)}: {rows}"
        )

    def test_pipeline_in_right_panel(self):
        right_panel = ROOT / "apps" / "ui" / "src" / "components" / "panels" / "RightLivePanel.tsx"
        content = right_panel.read_text()
        assert "PipelinePanel" in content, "PipelinePanel should be in RightLivePanel"

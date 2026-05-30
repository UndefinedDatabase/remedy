"""
Tests for reserved namespace __init__.py docstrings — Step 32.

Verifies that all empty reserved namespace packages have non-empty
module docstrings that describe their planned purpose and current status.
"""

from __future__ import annotations

from pathlib import Path

import pytest


def _repo_root() -> Path:
    from packages.orchestration import data_paths
    return Path(data_paths.__file__).resolve().parents[2]


RESERVED_INIT_FILES = [
    "packages/artifacts/__init__.py",
    "packages/runtimes/__init__.py",
    "packages/verification/__init__.py",
    "apps/api/__init__.py",
    "apps/worker/__init__.py",
    "packages/providers/claude_agent/__init__.py",
    "packages/providers/docker_runtime/__init__.py",
    "packages/providers/mempalace/__init__.py",
]


class TestReservedNamespaceDocstrings:
    @pytest.mark.parametrize("rel_path", RESERVED_INIT_FILES)
    def test_file_exists(self, rel_path):
        path = _repo_root() / rel_path
        assert path.exists(), f"{rel_path} does not exist"

    @pytest.mark.parametrize("rel_path", RESERVED_INIT_FILES)
    def test_has_module_docstring(self, rel_path):
        path = _repo_root() / rel_path
        text = path.read_text().strip()
        assert text.startswith('"""') or text.startswith("'''"), (
            f"{rel_path} does not start with a triple-quoted docstring; "
            f"got: {text[:80]!r}"
        )

    @pytest.mark.parametrize("rel_path", RESERVED_INIT_FILES)
    def test_docstring_is_non_trivially_long(self, rel_path):
        path = _repo_root() / rel_path
        text = path.read_text().strip()
        assert len(text) >= 100, (
            f"{rel_path} docstring is too short ({len(text)} chars); "
            "expected meaningful description of planned purpose and current status"
        )

    @pytest.mark.parametrize("rel_path", RESERVED_INIT_FILES)
    def test_docstring_mentions_reserved_or_status(self, rel_path):
        path = _repo_root() / rel_path
        text = path.read_text().lower()
        assert "reserved" in text or "not implemented" in text or "planned" in text, (
            f"{rel_path} docstring does not mention 'reserved', 'not implemented', or 'planned'"
        )

    @pytest.mark.parametrize("rel_path", RESERVED_INIT_FILES)
    def test_docstring_has_no_runtime_code(self, rel_path):
        """Reserved namespace __init__.py must not define runtime code."""
        path = _repo_root() / rel_path
        text = path.read_text()
        # Strip the docstring first (between first """ and closing """)
        # and check nothing significant remains
        stripped = text.strip()
        # Find end of docstring
        if stripped.startswith('"""'):
            end = stripped.find('"""', 3)
            after = stripped[end + 3:].strip() if end != -1 else ""
        elif stripped.startswith("'''"):
            end = stripped.find("'''", 3)
            after = stripped[end + 3:].strip() if end != -1 else ""
        else:
            after = stripped
        # After the docstring there should be no code (empty or just comments)
        code_lines = [
            line for line in after.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        assert not code_lines, (
            f"{rel_path} has runtime code after docstring: {code_lines[:3]}"
        )

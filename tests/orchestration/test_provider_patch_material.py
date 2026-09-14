"""Trusted Provider Patch Materialization v0 tests (Steps 1353/1355/1361).

Conversion (unified diff / JSON ops) and architecture guards (no provider SDK /
network / subprocess / apply imports).

Remedy deliberately no longer tests materialization, private storage, verification,
apply compatibility or redaction here: every one of those reached its subject through
the `provider intake-repair` command, which F275 T001 deleted with the Trust Gate.
There is no longer any way to create material, so there is nothing to materialize,
store, verify, apply or redact in a test. R-0867 records what the surviving module is
left with.
"""
from __future__ import annotations

from pathlib import Path

from packages.orchestration import provider_patch_material as PM

# ---------------------------------------------------------------------------
# Conversion (Steps 1339-1340)
# ---------------------------------------------------------------------------


class TestConversion:
    def test_md_modify_supported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- a/docs/x.md\n+++ b/docs/x.md\n@@ -1 +1,2 @@\n a\n+b\n")
        assert ext.ok and ext.action == "modify" and ext.target_path == "docs/x.md"
        assert ext.added_lines == ["b"]

    def test_md_create_supported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- /dev/null\n+++ b/docs/new.md\n@@ -0,0 +1,2 @@\n+line a\n+line b\n")
        assert ext.ok and ext.action == "create"
        assert ext.added_lines == ["line a", "line b"]

    def test_source_file_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-a\n+b\n")
        assert not ext.ok and ext.reason == "non_markdown_target"

    def test_delete_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- a/docs/x.md\n+++ /dev/null\n@@ -1 +0,0 @@\n-a\n")
        assert not ext.ok and ext.reason == "delete_unsupported"

    def test_rename_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "rename from docs/a.md\nrename to docs/b.md\n")
        assert not ext.ok and ext.reason == "rename_unsupported"

    def test_binary_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch("GIT binary patch\n...\n")
        assert not ext.ok and ext.reason == "binary_patch"

    def test_multi_file_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- a/docs/a.md\n+++ b/docs/a.md\n@@ -1 +1 @@\n+x\n"
            "--- a/docs/b.md\n+++ b/docs/b.md\n@@ -1 +1 @@\n+y\n")
        assert not ext.ok and ext.reason == "not_single_target"

    def test_json_ops_supported(self):
        ext = PM.materialize_structured_operations(
            [{"path": "docs/notes.md", "op": "modify", "content": ["a", "b"]}])
        assert ext.ok and ext.action == "modify" and ext.added_lines == ["a", "b"]

    def test_json_ops_source_unsupported(self):
        ext = PM.materialize_structured_operations(
            [{"path": "src/x.py", "op": "modify", "content": ["a"]}])
        assert not ext.ok


# ---------------------------------------------------------------------------
# Architecture guards (Step 1355)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/provider_patch_material.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_network_or_subprocess(self):
        for ln in self._imports():
            for bad in ("subprocess", "socket", "requests", "httpx", "urllib", "http.client"):
                assert bad not in ln
        assert "import subprocess" not in self.SRC
        assert "shell=True" not in self.SRC

    def test_no_provider_sdk(self):
        for ln in self._imports():
            low = ln.lower()
            for bad in ("ollama", "anthropic", "openai", "claude", "litellm"):
                assert bad not in low

    def test_no_apply_or_test_exec_imports(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "source_apply" not in ln
            assert "test_execution_service" not in ln
            assert "do_continue" not in ln

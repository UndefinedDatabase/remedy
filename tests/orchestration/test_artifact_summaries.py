"""F108 T001 — ArtifactSummary schema, mechanical sectioners, hash-invalidated cache."""
from __future__ import annotations

from pathlib import Path

from packages.orchestration.artifact_summary import (
    ArtifactSummary,
    compute_artifact_hash,
    load_cached_summary,
    save_summary,
    section_diff,
    section_log,
)

_TWO_FILE_DIFF = """diff --git a/foo.py b/foo.py
index 1111111..2222222 100644
--- a/foo.py
+++ b/foo.py
@@ -1,1 +1,1 @@
-old foo
+new foo
diff --git a/bar.py b/bar.py
index 3333333..4444444 100644
--- a/bar.py
+++ b/bar.py
@@ -1,1 +1,1 @@
-old bar
+new bar
"""

_BARE_DIFF = """--- a/foo.py
+++ b/foo.py
@@ -1,1 +1,1 @@
-old foo
+new foo
"""


def _make_summary(artifact_hash: str) -> ArtifactSummary:
    return ArtifactSummary(
        l1="a short summary",
        l2=[],
        full_ref="workspace.diff",
        generator="test-fixture",
        generated_at="2026-09-02T00:00:00Z",
        artifact_hash=artifact_hash,
    )


# ---------------------------------------------------------------------------
# compute_artifact_hash
# ---------------------------------------------------------------------------


def test_compute_artifact_hash_deterministic_and_content_sensitive():
    digest_a1 = compute_artifact_hash(b"content A")
    digest_a2 = compute_artifact_hash(b"content A")
    digest_b = compute_artifact_hash(b"content B")
    assert digest_a1 == digest_a2
    assert digest_a1 != digest_b


# ---------------------------------------------------------------------------
# load_cached_summary / save_summary
# ---------------------------------------------------------------------------


def test_load_cached_summary_returns_none_when_no_cache_file(tmp_path: Path):
    artifact_path = tmp_path / "workspace.diff"
    artifact_path.write_bytes(b"some diff content")

    assert load_cached_summary(artifact_path) is None


def test_save_then_load_round_trip_on_unmodified_artifact(tmp_path: Path):
    artifact_path = tmp_path / "workspace.diff"
    artifact_path.write_bytes(b"some diff content")
    artifact_hash = compute_artifact_hash(artifact_path.read_bytes())
    summary = _make_summary(artifact_hash)

    save_summary(artifact_path, summary)
    loaded = load_cached_summary(artifact_path)

    assert loaded is not None
    assert loaded == summary


def test_load_cached_summary_invalidates_on_hash_mismatch(tmp_path: Path):
    artifact_path = tmp_path / "workspace.diff"
    artifact_path.write_bytes(b"content A")
    artifact_hash_a = compute_artifact_hash(artifact_path.read_bytes())
    save_summary(artifact_path, _make_summary(artifact_hash_a))

    # Artifact changes on disk after the summary was generated.
    artifact_path.write_bytes(b"content B, totally different")

    assert load_cached_summary(artifact_path) is None


# ---------------------------------------------------------------------------
# section_diff
# ---------------------------------------------------------------------------


def test_section_diff_splits_two_files_with_correct_span_refs():
    entries = section_diff(_TWO_FILE_DIFF)

    assert len(entries) == 2
    assert entries[0]["section"] == "foo.py"
    assert entries[0]["span_ref"] == "file:foo.py"
    assert entries[1]["section"] == "bar.py"
    assert entries[1]["span_ref"] == "file:bar.py"

    assert "diff --git a/foo.py b/foo.py" in entries[0]["text"]
    assert "bar.py" not in entries[0]["text"]
    assert "diff --git a/bar.py b/bar.py" in entries[1]["text"]
    assert "foo.py" not in entries[1]["text"]


def test_section_diff_with_no_git_header_is_unsectioned():
    entries = section_diff(_BARE_DIFF)

    assert len(entries) == 1
    assert entries[0]["section"] == "(unsectioned)"
    assert entries[0]["span_ref"] == "file:(unsectioned)"


def test_section_diff_empty_string_returns_one_empty_entry():
    entries = section_diff("")

    assert len(entries) == 1
    assert entries[0]["text"] == ""
    assert entries[0]["section"] == "(unsectioned)"


# ---------------------------------------------------------------------------
# section_log
# ---------------------------------------------------------------------------


def test_section_log_splits_three_blank_line_separated_blocks():
    log_text = "first block\nline two\n\nsecond block\n\nthird block\nline two"
    entries = section_log(log_text)

    assert len(entries) == 3
    assert entries[0]["section"] == "block-0"
    assert entries[1]["section"] == "block-1"
    assert entries[2]["section"] == "block-2"
    assert entries[0]["text"] == "first block\nline two"
    assert entries[1]["text"] == "second block"
    assert entries[2]["text"] == "third block\nline two"


def test_section_log_fixed_chunk_fallback_with_no_blank_lines():
    lines = [f"log line {i}" for i in range(450)]
    log_text = "\n".join(lines)

    entries = section_log(log_text, chunk_lines=200)

    assert len(entries) > 1
    for entry in entries:
        assert entry["text"].count("\n") + 1 <= 200

    reconstructed = "\n".join(entry["text"] for entry in entries)
    assert reconstructed == log_text


def test_section_log_empty_string_returns_empty_list():
    assert section_log("") == []

"""F041 T001 — the artifact roots and the traversal fixtures (DECISION F041 D1).

`resolve_artifact_path` is the one gate between a requested name and a file the cockpit reads,
so every way out of a root is a fixture here: an absolute path, a `..` part even when it lands
inside, a backslash, a NUL, a symlink to a file outside, and a symlinked directory. The view
tests pin the whole wire shape, literal on purpose.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.artifact_preview import (
    MAX_LISTED_IMAGES,
    artifact_root,
    artifacts_view,
    resolve_artifact_path,
)

JOB_ID = "0123456789abcdef0123456789abcdef"


@pytest.fixture
def data_root(tmp_path: Path) -> Path:
    return tmp_path / "data"


def _evidence(data_root: Path) -> Path:
    directory = data_root / "jobs" / JOB_ID / "evidence"
    directory.mkdir(parents=True)
    return directory


def _workspace(data_root: Path) -> Path:
    directory = data_root / "job_workspaces" / f"staging_{JOB_ID[:16]}"
    directory.mkdir(parents=True)
    return directory


class TestResolveArtifactPath:
    def test_a_file_inside_the_root_resolves(self, tmp_path):
        (tmp_path / "captures").mkdir()
        (tmp_path / "captures" / "a.png").write_bytes(b"png")
        assert resolve_artifact_path(tmp_path, "captures/a.png") == (
            tmp_path / "captures" / "a.png").resolve()

    @pytest.mark.parametrize("relative", [
        "", "/etc/passwd", "../outside.md", "captures/../README.md", "captures\\a.png",
        "README.md\x00.png", "captures", "missing.md",
    ])
    def test_a_refused_or_absent_name_resolves_to_none(self, tmp_path, relative):
        (tmp_path / "captures").mkdir()
        (tmp_path / "README.md").write_text("inside")
        (tmp_path.parent / "outside.md").write_text("outside")
        assert resolve_artifact_path(tmp_path, relative) is None

    def test_a_symlink_to_a_file_outside_is_refused(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        (tmp_path / "secret.md").write_text("secret")
        (root / "README.md").symlink_to(tmp_path / "secret.md")
        assert resolve_artifact_path(root, "README.md") is None

    def test_a_symlinked_directory_leading_outside_is_refused(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        (tmp_path / "elsewhere").mkdir()
        (tmp_path / "elsewhere" / "a.png").write_bytes(b"png")
        (root / "captures").symlink_to(tmp_path / "elsewhere", target_is_directory=True)
        assert resolve_artifact_path(root, "captures/a.png") is None

    def test_a_symlink_that_stays_inside_resolves(self, tmp_path):
        (tmp_path / "real.md").write_text("real")
        (tmp_path / "README.md").symlink_to(tmp_path / "real.md")
        assert resolve_artifact_path(tmp_path, "README.md") == (tmp_path / "real.md").resolve()


class TestArtifactRoot:
    def test_the_roots_are_derived_from_the_data_root(self, data_root):
        evidence, workspace = _evidence(data_root), _workspace(data_root)
        assert artifact_root(JOB_ID, "evidence", data_root) == evidence
        assert artifact_root(JOB_ID, "workspace", data_root) == workspace

    def test_an_absent_or_unknown_root_is_none(self, data_root):
        assert artifact_root(JOB_ID, "evidence", data_root) is None
        assert artifact_root(JOB_ID, "workspace", data_root) is None
        _evidence(data_root)
        assert artifact_root(JOB_ID, "repo", data_root) is None


class TestArtifactsView:
    def test_a_job_with_nothing_answers_the_empty_view(self, data_root):
        assert artifacts_view(JOB_ID, data_root) == {"readme": None, "images": [], "error": ""}

    def test_the_workspace_readme_wins_over_the_evidence_one(self, data_root):
        _evidence(data_root).joinpath("README.md").write_text("# From evidence\n")
        _workspace(data_root).joinpath("README.md").write_text("# From workspace\n")
        view = artifacts_view(JOB_ID, data_root)
        assert view["readme"] == {
            "root": "workspace", "path": "README.md", "html": "<h1>From workspace</h1>",
            "truncated": False, "source_bytes": 17,
        }

    def test_the_evidence_readme_is_used_when_the_workspace_is_gone(self, data_root):
        _evidence(data_root).joinpath("README.md").write_text("<script>x</script>\n")
        view = artifacts_view(JOB_ID, data_root)
        assert view == {
            "readme": {
                "root": "evidence", "path": "README.md",
                "html": "<p>&lt;script&gt;x&lt;/script&gt;</p>", "truncated": False,
                "source_bytes": 19,
            },
            "images": [],
            "error": "",
        }

    def test_a_readme_that_is_not_utf8_is_rendered_with_replacements(self, data_root):
        _evidence(data_root).joinpath("README.md").write_bytes(b"caf\xe9\n")
        assert artifacts_view(JOB_ID, data_root)["readme"]["html"] == "<p>caf�</p>"

    def test_the_captures_list_holds_only_images_inside_the_root(self, data_root, tmp_path):
        captures = _evidence(data_root) / "captures"
        captures.mkdir()
        (captures / "b.PNG").write_bytes(b"12345")
        (captures / "a.jpg").write_bytes(b"123")
        (captures / "c.svg").write_text("<svg/>")
        (captures / "notes.md").write_text("x")
        (captures / "dir.png").mkdir()
        (tmp_path / "outside.png").write_bytes(b"1")
        (captures / "link.png").symlink_to(tmp_path / "outside.png")
        assert artifacts_view(JOB_ID, data_root)["images"] == [
            {"root": "evidence", "path": "captures/a.jpg", "bytes": 3,
             "content_type": "image/jpeg"},
            {"root": "evidence", "path": "captures/b.PNG", "bytes": 5,
             "content_type": "image/png"},
        ]

    def test_the_captures_list_is_capped(self, data_root):
        captures = _evidence(data_root) / "captures"
        captures.mkdir()
        for index in range(MAX_LISTED_IMAGES + 5):
            (captures / f"{index:04d}.png").write_bytes(b"p")
        images = artifacts_view(JOB_ID, data_root)["images"]
        assert len(images) == MAX_LISTED_IMAGES == 200
        assert images[-1]["path"] == f"captures/{MAX_LISTED_IMAGES - 1:04d}.png"

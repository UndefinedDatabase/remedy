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
    FILE_MAX_BYTES,
    MAX_LISTED_IMAGES,
    ArtifactFile,
    artifact_root,
    artifacts_view,
    read_artifact_file,
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


class TestReadArtifactFile:
    """The file route's reader (DECISION F041 D2): two servable names, and nothing else."""

    def test_a_screenshot_is_served_with_its_image_type(self, data_root):
        captures = _evidence(data_root) / "captures"
        captures.mkdir()
        (captures / "home.PNG").write_bytes(b"\x89PNG-bytes")
        assert read_artifact_file(JOB_ID, "evidence", "captures/home.PNG", data_root) == (
            ArtifactFile(status=200, content_type="image/png", body=b"\x89PNG-bytes", error=""))

    @pytest.mark.parametrize("root", ["workspace", "evidence"])
    def test_the_readme_is_served_as_plain_text_from_either_root(self, data_root, root):
        base = _workspace(data_root) if root == "workspace" else _evidence(data_root)
        (base / "README.md").write_text("<script>x</script>\n")
        assert read_artifact_file(JOB_ID, root, "README.md", data_root) == ArtifactFile(
            status=200, content_type="text/plain; charset=utf-8",
            body=b"<script>x</script>\n", error="")

    @pytest.mark.parametrize(("root", "relative"), [
        ("repo", "README.md"),
        ("", "README.md"),
        ("evidence", ""),
        ("evidence", "notes.md"),
        ("evidence", "captures/c.svg"),
        ("evidence", "captures/sub/a.png"),
        ("evidence", "captures/../README.md"),
        ("evidence", "captures/./a.png"),
        ("evidence", "captures//a.png"),
        ("evidence", "/captures/a.png"),
        ("evidence", "../jobs/x/evidence/captures/a.png"),
        ("workspace", "captures/a.png"),
        ("evidence", "docs/README.md"),
    ])
    def test_any_other_request_is_refused_before_the_disk_is_read(self, data_root, root,
                                                                  relative):
        captures = _evidence(data_root) / "captures"
        captures.mkdir()
        (captures / "a.png").write_bytes(b"png")
        (captures / "c.svg").write_text("<svg/>")
        assert read_artifact_file(JOB_ID, root, relative, data_root) == ArtifactFile(
            status=400, content_type="", body=b"", error="invalid artifact request")

    def test_a_missing_file_or_root_is_not_found(self, data_root):
        missing = ArtifactFile(status=404, content_type="", body=b"", error="artifact not found")
        assert read_artifact_file(JOB_ID, "evidence", "README.md", data_root) == missing
        (_evidence(data_root) / "captures").mkdir()
        assert read_artifact_file(JOB_ID, "evidence", "captures/a.png", data_root) == missing

    def test_a_symlink_leaving_the_root_is_not_found(self, data_root, tmp_path):
        captures = _evidence(data_root) / "captures"
        captures.mkdir()
        (tmp_path / "secret.png").write_bytes(b"secret")
        (captures / "a.png").symlink_to(tmp_path / "secret.png")
        assert read_artifact_file(JOB_ID, "evidence", "captures/a.png", data_root).status == 404

    def test_a_file_over_the_cap_is_too_large(self, data_root):
        captures = _evidence(data_root) / "captures"
        captures.mkdir()
        (captures / "big.png").write_bytes(b"\0" * (FILE_MAX_BYTES + 1))
        (captures / "edge.png").write_bytes(b"\0" * FILE_MAX_BYTES)
        assert read_artifact_file(JOB_ID, "evidence", "captures/big.png", data_root) == (
            ArtifactFile(status=413, content_type="", body=b"", error="artifact too large"))
        assert read_artifact_file(JOB_ID, "evidence", "captures/edge.png",
                                  data_root).status == 200
        assert FILE_MAX_BYTES == 10_485_760

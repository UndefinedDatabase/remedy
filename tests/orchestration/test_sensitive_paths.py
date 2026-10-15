"""The one sensitive-path classifier and the snapshot that obeys it (operator amendment amend1014c, R1)."""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.job_apply import _is_blocked_path
from packages.orchestration.sensitive_paths import (
    is_secret_file_name,
    sensitive_exclude_pathspecs,
    sensitive_path_category,
)
from packages.orchestration.worktrees import write_tree_at


@pytest.mark.parametrize("path,fragment", [
    (".env", "environment"), (".env.local", "environment"), ("app/.env-prod", "environment"),
    ("credentials.json", "credentials"), ("a/secrets.json", "credentials"), (".secrets", "credentials"),
    ("api_key.txt", "credentials"), ("id_ed25519", "credentials"),
    ("k/server.PEM", "private key"), ("x.key", "private key"), ("x.p12", "private key"),
    ("x.pfx", "private key"), ("x.jks", "private key"),
    (".git/config", "git"), ("../outside.txt", "outside"), ("/etc/passwd", "outside"),
])
def test_a_sensitive_name_has_a_category_and_an_ordinary_name_has_none(path, fragment):
    assert fragment in sensitive_path_category(path)


@pytest.mark.parametrize("path", ["README.md", "src/env.py", "environment.md", "keyboard.txt", "notes.txt"])
def test_ordinary_paths_have_no_category(path):
    assert sensitive_path_category(path) == ""


def test_apply_and_the_context_pack_ask_the_same_classifier():
    from packages.orchestration.pingpong_loop import _is_secret_file

    for name in (".env", ".env.test", "credentials.json", "secrets.json", ".secrets", "api_key.txt"):
        assert _is_secret_file(name) and is_secret_file_name(name)
        assert _is_blocked_path(name)
    assert _is_blocked_path("deploy.pem") == "private_key_file"
    assert not _is_secret_file("README.md") and _is_blocked_path("README.md") == ""


def test_the_target_state_snapshot_never_hashes_a_sensitive_file(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    run = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True)  # noqa: E731
    run("init", "-q")
    run("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "i")
    (repo / "README.md").write_text("ordinary\n")
    marker = b"DUMMY-SNAPSHOT-MARKER-77"
    (repo / ".env").write_bytes(marker)
    (repo / "sub").mkdir()
    (repo / "sub" / "x.pem").write_bytes(marker)

    tree = write_tree_at(repo)

    names = subprocess.run(["git", "ls-tree", "-r", "--name-only", tree], cwd=repo, check=True,
                           capture_output=True, text=True).stdout.split()
    assert names == ["README.md"]
    objects = subprocess.run(["git", "cat-file", "--batch-all-objects", "--batch"], cwd=repo,
                             check=True, capture_output=True).stdout
    assert marker not in objects
    assert all(spec.startswith(":(exclude,glob)**/") for spec in sensitive_exclude_pathspecs())

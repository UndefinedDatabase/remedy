"""The `remedy serve` supervisor's paths (F200, DECISION F200 D1).

A client finds the supervisor only by computing the same paths from the same data
root, so these tests pin where each file lives, that the class is registered, and
where the socket length limit falls.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration import serve_paths as SP
from packages.orchestration.data_paths import classify_data_child


def test_every_file_lives_in_the_serve_class_of_the_given_root(tmp_path):
    paths = SP.serve_paths(tmp_path)
    assert paths == SP.ServePaths(
        root=tmp_path / "serve",
        socket=tmp_path / "serve" / "serve.sock",
        pid_file=tmp_path / "serve" / "serve.pid",
        token_file=tmp_path / "serve" / "serve.token",
        runs_dir=tmp_path / "serve" / "runs",
    )


def test_without_a_root_the_paths_follow_the_resolved_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "elsewhere"))
    assert SP.serve_paths().socket == tmp_path / "elsewhere" / "serve" / "serve.sock"


def test_the_serve_class_is_durable():
    assert classify_data_child("serve") == "durable"


def test_computing_the_paths_creates_nothing(tmp_path):
    SP.serve_paths(tmp_path)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("size", [1, 50, SP.SOCKET_PATH_MAX_BYTES])
def test_a_socket_path_up_to_the_limit_is_accepted(size):
    assert SP.socket_path_problem(Path("/" + "a" * (size - 1))) == ""


def test_one_byte_past_the_limit_is_refused_with_the_setting_to_change():
    path = Path("/" + "a" * SP.SOCKET_PATH_MAX_BYTES)
    problem = SP.socket_path_problem(path)
    assert f"is {SP.SOCKET_PATH_MAX_BYTES + 1} bytes long" in problem
    assert f"at most {SP.SOCKET_PATH_MAX_BYTES}" in problem
    assert "REMEDY_DATA_DIR" in problem


def test_the_limit_counts_bytes_not_characters():
    # Each "é" is two bytes in UTF-8, so 52 of them after "/" is 105 bytes.
    assert SP.socket_path_problem(Path("/" + "é" * 52)) != ""
    assert SP.socket_path_problem(Path("/" + "é" * 51)) == ""


def test_the_limit_fits_the_smaller_platform_limit():
    # macOS `sun_path` is 104 bytes with the terminating NUL; Linux's is 108.
    assert SP.SOCKET_PATH_MAX_BYTES == 104 - 1

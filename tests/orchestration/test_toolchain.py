"""`remedy doctor toolchain` and the report under it (T2_F279 T004, DECISION F279 D6).

No test here reaches the network: the package index is replaced by a function the test hands
in, and the one test of the real fetcher replaces `urlopen` itself.
"""
from __future__ import annotations

import argparse
import io
import json

import pytest

from packages.orchestration import toolchain
from packages.orchestration.toolchain import (
    NOT_INSTALLED,
    UNKNOWN,
    installed_version,
    offline,
    pinned_tools,
    pinned_versions,
    pypi_newest,
    toolchain_rows,
)

# R-1045: `uv`, the generator `constraints.txt` names, is part of the `dev` extra and so of the report.
DECLARED = ["pydantic", "psutil", "pytest", "pytest-xdist", "ruff", "mypy", "pytest-cov", "coverage", "uv"]


def test_the_report_covers_the_runtime_dependencies_and_the_dev_extra():
    text = (toolchain.REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert pinned_tools(text) == DECLARED


def test_every_reported_tool_is_pinned_by_the_constraints_file():
    pins = pinned_versions((toolchain.REPO_ROOT / "constraints.txt").read_text(encoding="utf-8"))
    assert [name for name in DECLARED if name not in pins] == []


def test_the_three_columns_come_from_their_three_sources():
    rows = toolchain_rows(fetch_newest=lambda name: f"{name}-newest",
                          installed=lambda name: f"{name}-installed")
    by_name = {row.name: row for row in rows}
    assert [row.name for row in rows] == DECLARED
    ruff = by_name["ruff"]
    assert ruff.installed == "ruff-installed" and ruff.newest == "ruff-newest"
    assert ruff.pinned == pinned_versions(
        (toolchain.REPO_ROOT / "constraints.txt").read_text(encoding="utf-8"))["ruff"]


def test_offline_and_an_empty_answer_both_read_unknown_never_a_number():
    assert {row.newest for row in toolchain_rows(fetch_newest=offline)} == {UNKNOWN}
    assert {row.newest for row in toolchain_rows(fetch_newest=lambda name: "")} == {UNKNOWN}


def test_a_package_that_is_not_installed_says_so():
    assert installed_version("remedy-no-such-package-f279") == NOT_INSTALLED


class TestTheIndexFetch:
    def test_a_reachable_index_answers_its_version(self, monkeypatch):
        body = json.dumps({"info": {"version": "9.9.9"}}).encode()
        monkeypatch.setattr("urllib.request.urlopen", lambda url, timeout: io.BytesIO(body))
        assert pypi_newest("ruff") == "9.9.9"

    @pytest.mark.parametrize("failure", [OSError("offline"), ValueError("bad json")])
    def test_any_fetch_failure_reads_unknown(self, monkeypatch, failure):
        def refuse(url, timeout):
            raise failure

        monkeypatch.setattr("urllib.request.urlopen", refuse)
        assert pypi_newest("ruff") == UNKNOWN


class TestTheCommand:
    def _run(self, capsys, **flags):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_toolchain

        _cmd_doctor_toolchain(argparse.Namespace(**flags))
        return capsys.readouterr().out

    def test_offline_json_names_every_tool_with_three_columns(self, monkeypatch, capsys):
        def never(name):
            raise AssertionError(f"--offline asked the package index for {name}")

        monkeypatch.setattr(toolchain, "pypi_newest", never)
        document = json.loads(self._run(capsys, json=True, offline=True))
        assert document["ok"] is True and document["offline"] is True
        assert [tool["name"] for tool in document["tools"]] == DECLARED
        assert {tool["newest"] for tool in document["tools"]} == {UNKNOWN}
        assert all(set(tool) == {"name", "installed", "pinned", "newest"} for tool in document["tools"])

    def test_online_asks_the_index(self, monkeypatch, capsys):
        monkeypatch.setattr(toolchain, "pypi_newest", lambda name: "1.0")
        document = json.loads(self._run(capsys, json=True, offline=False))
        assert document["offline"] is False
        assert {tool["newest"] for tool in document["tools"]} == {"1.0"}

    def test_text_mode_prints_a_header_and_one_line_per_tool(self, capsys):
        out = self._run(capsys, json=False, offline=True)
        lines = out.splitlines()
        header = next(i for i, line in enumerate(lines) if line.split() == ["tool", "installed", "pinned", "newest"])
        assert [line.split()[0] for line in lines[header + 1:]] == DECLARED
        assert "every newest version reads unknown" in out

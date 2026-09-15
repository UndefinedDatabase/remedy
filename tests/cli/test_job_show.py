"""F261 T002 — `remedy job show <id>`, the one read command of a job.

Round 8 (finding R-0896): next-step hints told the operator to run
``remedy job show <id> --json`` and the command exited 2 on the flag. `job show`
now declares ``--json``; its output was always JSON, so the flag changes nothing.
"""
from __future__ import annotations

import json

import pytest

from apps.cli.grouped import build_parser, main
from packages.core.models import RunState
from packages.orchestration.pingpong_job import JobPlan, save_job_plan


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


def _show(capsys, *argv: str):
    main(["job", "show", *argv])
    return capsys.readouterr()


class TestJsonFlag:
    def test_job_show_json_parses_with_no_unknown_argument(self) -> None:
        args, unknown = build_parser().parse_known_args(["job", "show", "abc", "--json"])

        assert args._command_id == "job.show"
        assert unknown == []

    def test_the_json_flag_changes_nothing_in_the_output(self, data_root, capsys) -> None:
        job = JobPlan(job_title="show me", state=RunState.PENDING)
        save_job_plan(job)

        bare = _show(capsys, str(job.job_id))
        flagged = _show(capsys, str(job.job_id), "--json")

        assert json.loads(bare.out)["job_id"] == job.job_id
        assert flagged.out == bare.out
        assert flagged.err == bare.err

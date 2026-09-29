"""`remedy job story` — F039 T003, DECISIONS F039 D7 and D8.

Modelled on `test_job_ownership.py`: the CLI handler is proved through the real argv
dispatcher, over a real `JobPlan` saved to a temp data root. `story_export.STORY_PLAYER_DIR`
is patched to a temporary built player for every test that needs one to succeed, so no test
depends on `apps/ui`'s own build; `reset_config()` runs around each test so a budget env var
set by one test never leaks into the next.
"""
from __future__ import annotations

import json
import stat
from uuid import uuid4

import pytest

from packages.orchestration import pingpong_job as pj
from packages.orchestration import story_export
from packages.orchestration.config import reset_config
from packages.orchestration.pingpong_job import JobPlan, TaskEntry
from packages.orchestration.story_export import export_story_html


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


@pytest.fixture(autouse=True)
def _no_leaked_config_cache():
    """Leave the process-global config cache exactly as empty as found."""
    yield
    reset_config()


@pytest.fixture
def player_dir(tmp_path, monkeypatch):
    directory = tmp_path / "player"
    directory.mkdir()
    (directory / "story-player.js").write_text("console.log('story player');", encoding="utf-8")
    (directory / "story-player.css").write_text("body { margin: 0; }", encoding="utf-8")
    monkeypatch.setattr(story_export, "STORY_PLAYER_DIR", directory)
    return directory


@pytest.fixture
def job() -> pj.JobPlan:
    job = JobPlan(job_title="CLI story test", tasks=[TaskEntry(title="write a readme")])
    pj.save_job_plan(job)
    return job


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return (code or 0), capsys.readouterr().out


class TestJobStoryTextAndJSON:
    def test_the_json_form_exits_0_with_the_envelope_and_the_files_own_size(
        self, job, player_dir, tmp_path, capsys,
    ):
        target = tmp_path / "out.html"
        code, out = _run(["job", "story", str(job.job_id), "--export", str(target), "--json"], capsys)
        assert code == 0
        body = json.loads(out)
        assert body["ok"] is True
        assert body["job_id"] == str(job.job_id)
        assert body["path"] == str(target)
        assert body["bytes"] == target.stat().st_size
        assert body["budget_bytes"] == 5_000_000
        assert target.read_bytes() == export_story_html(job, max_bytes=5_000_000)

    def test_the_file_mode_is_0644(self, job, player_dir, tmp_path, capsys):
        target = tmp_path / "out.html"
        _run(["job", "story", str(job.job_id), "--export", str(target), "--json"], capsys)
        assert stat.S_IMODE(target.stat().st_mode) == 0o644

    def test_the_text_form_prints_exactly_the_one_line(self, job, player_dir, tmp_path, capsys):
        target = tmp_path / "out.html"
        code, out = _run(["job", "story", str(job.job_id), "--export", str(target)], capsys)
        assert code == 0
        n = target.stat().st_size
        assert out == (
            f"Wrote the story of job {job.job_id} to {target} ({n} bytes). Open it in any "
            f"browser; it needs no network and no Remedy.\n"
        )


class TestJobStoryExitCodes:
    def test_an_unknown_job_exits_3_job_not_found_and_writes_nothing(self, player_dir, tmp_path, capsys):
        target = tmp_path / "out.html"
        code, out = _run(["job", "story", str(uuid4()), "--export", str(target), "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "job_not_found"
        assert not target.exists()

    def test_a_missing_player_exits_3_story_player_missing_and_writes_nothing(
        self, job, tmp_path, monkeypatch, capsys,
    ):
        monkeypatch.setattr(story_export, "STORY_PLAYER_DIR", tmp_path / "absent")
        target = tmp_path / "out.html"
        code, out = _run(["job", "story", str(job.job_id), "--export", str(target), "--json"], capsys)
        assert code == 3
        assert json.loads(out)["error"] == "story_player_missing"
        assert not target.exists()

    def test_a_too_small_budget_exits_1_story_too_large_and_writes_nothing(
        self, job, player_dir, tmp_path, monkeypatch, capsys,
    ):
        monkeypatch.setenv("REMEDY_STORY_EXPORT_MAX_BYTES", "10")
        target = tmp_path / "out.html"
        code, out = _run(["job", "story", str(job.job_id), "--export", str(target), "--json"], capsys)
        assert code == 1
        assert json.loads(out)["error"] == "story_too_large"
        assert not target.exists()

    def test_a_missing_directory_exits_1_story_write_failed_and_writes_nothing(
        self, job, player_dir, tmp_path, capsys,
    ):
        target = tmp_path / "nowhere" / "out.html"
        code, out = _run(["job", "story", str(job.job_id), "--export", str(target), "--json"], capsys)
        assert code == 1
        assert json.loads(out)["error"] == "story_write_failed"
        assert not target.exists()

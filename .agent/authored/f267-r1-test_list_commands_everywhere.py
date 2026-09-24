"""Every list command's HANDLER honours the shared list flags (F267 T002 and T003).

`TestListCommandOptions` in `tests/test_command_catalog.py` proves that every
list-shaped catalog entry DECLARES `--sort`, `--desc`, `--since`, `--until` and
`--limit`; argparse accepts a flag nobody reads, so that test cannot tell a wired
handler from one that ignores the flag. The tests below run each command through
the grouped CLI instead, over the set `_is_list_command` derives from the catalog
itself, never a hand-written list (DECISION F267 D1).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, _is_list_command

REPO_ROOT = Path(__file__).resolve().parents[2]

LIST_COMMANDS = sorted((c for c in CATALOG if _is_list_command(c)), key=lambda c: c.command_id)

#: DECISION F262 D4 kept these four out of scope, each for a reason of its own;
#: F275 deleted all four commands (finding R-0858), so none may come back unnoticed.
D4_EXCLUSIONS = {
    "builder.adapter-list": "no date on its row shape",
    "execution.template-list": "no date on its row shape",
    "worker.registry-list": "no date on its row shape",
    "approval.policy-list": "browsed by name and state, not by recency",
}

#: The one required positional a list command may take; the fixture supplies it.
KNOWN_POSITIONALS = {"job_id"}

_BOGUS = re.compile(r"^unknown --sort field 'bogus'; valid fields: [a-z_]+(, [a-z_]+)*$")


def _argv(entry, job_id: str) -> list[str]:
    group, sub = entry.command_id.split(".", 1)
    argv = [group, sub]
    for arg in entry.args:
        if arg.required and not arg.is_option:
            argv.append(job_id)
    return argv


@pytest.fixture
def seeded_job(tmp_path, monkeypatch) -> str:
    """An isolated data root holding one registered project, selected through
    `REMEDY_PROJECT` so a project-scoped list runs its default path, and one saved
    job with nothing in it."""
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan
    from packages.orchestration.project_registry import RemyProject, save_project

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    save_project(RemyProject(name="F267 list probe", slug="f267-list-probe"))
    monkeypatch.setenv("REMEDY_PROJECT", "f267-list-probe")
    job = JobPlan(job_title="F267 list probe", state=RunState.PENDING)
    save_job_plan(job)
    return str(job.job_id)


def _run(argv: list[str], capsys) -> tuple[int, str, str]:
    from apps.cli.grouped import main

    with pytest.raises(SystemExit) as exc:
        main(argv)
    captured = capsys.readouterr()
    return exc.value.code, captured.out, captured.err


class TestTheInScopeSet:
    def test_the_catalog_holds_list_commands(self):
        assert LIST_COMMANDS, "no list-shaped command found in CATALOG"

    def test_no_d4_exclusion_is_back_in_the_catalog(self):
        ids = {c.command_id for c in CATALOG}
        back = sorted(set(D4_EXCLUSIONS) & ids)
        assert not back, f"a DECISION F262 D4 exclusion is in the catalog again: {back}"

    @pytest.mark.parametrize("entry", LIST_COMMANDS, ids=lambda c: c.command_id)
    def test_every_required_positional_is_one_the_probe_can_supply(self, entry):
        required = {a.name for a in entry.args if a.required and not a.is_option}
        assert required <= KNOWN_POSITIONALS, (
            f"{entry.command_id} requires {sorted(required - KNOWN_POSITIONALS)}, "
            "which the handler test below cannot supply"
        )


class TestEveryHandlerRefusesAnUnknownSortField:
    """T002: the handler, not the parser, refuses `--sort bogus` and names the valid set."""

    @pytest.mark.parametrize("entry", LIST_COMMANDS, ids=lambda c: c.command_id)
    def test_text_output(self, entry, seeded_job, capsys):
        code, out, err = _run([*_argv(entry, seeded_job), "--sort", "bogus"], capsys)
        assert code not in (0, None), f"{entry.command_id} accepted --sort bogus"
        last = err.strip().splitlines()[-1] if err.strip() else ""
        assert _BOGUS.match(last.removeprefix("Error: ")), (
            f"{entry.command_id} did not name its valid fields: {err!r}"
        )

    @pytest.mark.parametrize("entry", LIST_COMMANDS, ids=lambda c: c.command_id)
    def test_json_output(self, entry, seeded_job, capsys):
        code, out, err = _run([*_argv(entry, seeded_job), "--sort", "bogus", "--json"], capsys)
        assert code not in (0, None), f"{entry.command_id} accepted --sort bogus"
        body = json.loads(out)
        assert body["ok"] is False
        assert body["error"] == "invalid_list_option"
        assert _BOGUS.match(body["message"]), (
            f"{entry.command_id} did not name its valid fields: {body['message']!r}"
        )


class TestTheTenSecondDemo:
    """T003: a run from two days ago is found with one command, `--since 3d --until 1d`."""

    @pytest.fixture
    def three_runs(self, tmp_path) -> Path:
        data_root = tmp_path / "data"
        now = datetime.now(timezone.utc)
        for run_id, days in (("run-five-days", 5), ("run-two-days", 2), ("run-an-hour", 1 / 24)):
            run_dir = data_root / "runs" / run_id
            run_dir.mkdir(parents=True)
            (run_dir / "result.json").write_text(json.dumps({
                "run_id": run_id,
                "goal": f"goal of {run_id}",
                "final_status": "completed",
                "finished_at": (now - timedelta(days=days)).isoformat(),
            }))
        return data_root

    def _remedy(self, data_root: Path, *args: str) -> subprocess.CompletedProcess:
        env = {**os.environ, "REMEDY_DATA_DIR": str(data_root)}
        env.pop("REMEDY_PROJECT", None)
        return subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", *args],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120, env=env,
        )

    def test_the_store_is_where_run_list_reads(self, three_runs, monkeypatch):
        from packages.orchestration import data_paths

        monkeypatch.setenv("REMEDY_DATA_DIR", str(three_runs))
        assert data_paths.runs_dir() == three_runs / "runs"

    def test_the_window_finds_exactly_the_run_from_two_days_ago(self, three_runs):
        proc = self._remedy(three_runs, "run", "list", "--since", "3d", "--until", "1d", "--json")
        assert proc.returncode == 0, proc.stderr
        runs = json.loads(proc.stdout)["runs"]
        assert [r["run_id"] for r in runs] == ["run-two-days"]
        assert runs[0]["goal"] == "goal of run-two-days"

    def test_the_text_output_names_only_that_run(self, three_runs):
        proc = self._remedy(three_runs, "run", "list", "--since", "3d", "--until", "1d")
        assert proc.returncode == 0, proc.stderr
        assert "run-two-days" in proc.stdout
        assert "run-five-days" not in proc.stdout
        assert "run-an-hour" not in proc.stdout

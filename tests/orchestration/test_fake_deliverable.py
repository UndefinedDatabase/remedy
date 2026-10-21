"""amend1015c D6 — the fake builder `--builder-provider fake` selects writes its task's deliverable.

Operator order amend1015-final-closure, E5 (R-1325): an order about the README of a repository
whose one tracked file is `README.md` must change `README.md`, not a `docs/README.md` the order
never named. The cause was the fixture's fixed file, so the real `remedy do run` with the fake
providers is the test.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.fake_deliverable import DeliverableFakeProvider, prompt_deliverable_file
from packages.orchestration.pingpong_provider import create_provider
from packages.orchestration.pingpong_provider_fake import FakeProvider

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(("prompt", "expected"), [
    ("Order\n\nThis task's deliverable: README.md\n", "README.md"),
    ("This task's deliverable: src/a.md\nThis task's deliverable: docs/b.markdown",
     "docs/b.markdown"),
    ("This task's deliverable: src/main.py", ""),     # the fake's note is Markdown
    ("This task's deliverable: readme", ""),          # a plain word names no file
    ("This task's deliverable: check: README.md meets the order", ""),
    ("This task's deliverable: .env", ""),            # never a sensitive path
    ("This task's deliverable: ../outside.md", ""),
    ("No deliverable line at all", ""),
])
def test_the_prompts_deliverable_file(prompt, expected):
    assert prompt_deliverable_file(prompt) == expected


def test_the_command_lines_fake_follows_the_deliverable_and_a_tests_own_fake_does_not():
    prompt = "Order\n\nThis task's deliverable: notes/todo.md\n"
    assert isinstance(create_provider("fake"), DeliverableFakeProvider)
    assert create_provider("fake").build(prompt).files_changed == ["notes/todo.md"]
    assert create_provider("fake").build("no deliverable").files_changed == ["docs/README.md"]
    assert FakeProvider().build(prompt).files_changed == ["docs/README.md"]


def test_an_order_about_the_readme_changes_the_readme(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# tiny' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=repo, check=True)
    data_root = tmp_path / "data"
    env = {**os.environ, "PYTHONPATH": str(REPO_ROOT), "REMEDY_DATA_DIR": str(data_root),
           "GIT_CEILING_DIRECTORIES": str(tmp_path)}
    done = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "do", "run", "pass die readme an", "--repo",
         str(repo), "--builder-provider", "fake", "--reviewer-provider", "fake", "--no-ui",
         "--json"], cwd=str(tmp_path), capture_output=True, text=True, env=env, timeout=300)
    assert done.returncode == 0, done.stdout[-2000:] + done.stderr[-2000:]
    [job_id] = json.loads(done.stdout)["job_ids"]
    job = json.loads((data_root / "jobs" / job_id / "job.json").read_text())
    assert [task["title"] for task in job["tasks"]] == ["Deliver README.md"]
    changed = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", job["worktree"]["base_commit"],
         job["worktree"]["head"]], capture_output=True, text=True, check=True).stdout
    assert changed == "README.md\n"

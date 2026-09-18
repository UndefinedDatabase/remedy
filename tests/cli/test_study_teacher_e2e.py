"""F266 T003 — the three-step (`init` -> `study run` -> `teacher ask`) proved
end to end against a foreign repository fixture.

`init` runs as the real CLI subprocess it is everywhere else in this suite
(tests/cli/test_golden_path.py's `_git_repo`/`_init_project` pattern). `study
run` and `teacher ask` run IN-PROCESS, through the same handler functions
tests/cli/test_study_cmd.py and tests/cli/test_teacher_cmd.py already call
directly, so this test controls both transport seams deterministically:
`study run`'s call_fn returns nothing, forcing the documented heuristic
fallback (packages/orchestration/study.py's own "falls back to the heuristic
value ... on exhaustion or on any call_fn exception" behavior), and `teacher
ask`'s call captures the exact prompt the model was shown — the same "assert
what the model was shown" method tests/cli/test_teacher_cmd.py uses for every
other grounding-source proof.

The fixture repository carries ONE distinctive top-level directory name that
no general-knowledge answer could produce by chance, so an answer containing
it is derivable only from the `study:structure` card `study run` wrote.
"""
from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
from io import StringIO
from pathlib import Path

_CLI = [sys.executable, "-m", "apps.cli.grouped"]

#: A top-level directory name no general-knowledge answer could produce by
#: chance — the fact every assertion below hinges on.
_MARKER_DIR = "zzyzx_ledger_workers"


def _env(tmp_path: Path) -> dict:
    return {
        **os.environ,
        "PYTHONPATH": os.getcwd(),
        "REMEDY_DATA_DIR": str(tmp_path / "data"),
    }


def _foreign_repo(tmp_path: Path) -> Path:
    """A minimal git repository, distinct from remedy, carrying the marker directory."""
    repo = tmp_path / "foreign_repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Foreign Project\n")
    (repo / "pyproject.toml").write_text("[project]\nname = 'foreign'\n")
    marker = repo / _MARKER_DIR
    marker.mkdir()
    (marker / "worker.py").write_text("# worker\n")
    tests_dir = repo / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_worker.py").write_text("def test_pass(): pass\n")

    subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return repo


def _no_narration(prompt: str, attempt: int) -> str:
    """`study run`'s call_fn seam, forced empty so every category keeps its
    heuristic value — deterministic, no live model dependency."""
    return ""


class TestThreeStepEndToEnd:
    """T003 Acceptance: init -> study run -> teacher ask, proved end to end."""

    def test_teacher_ask_answers_from_a_study_card_after_the_three_step(self, tmp_path, monkeypatch):
        repo = _foreign_repo(tmp_path)
        env = _env(tmp_path)

        init = subprocess.run(
            [*_CLI, "init"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert init.returncode == 0, init.stderr

        before = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.chdir(str(repo))

        from apps.cli.commands.study_cmd import _cmd_study_run

        study_out = StringIO()
        with contextlib.redirect_stdout(study_out):
            _cmd_study_run(None, project=None, json_output=True, call_fn=_no_narration)
        study_result = json.loads(study_out.getvalue())

        assert study_result["cards_written"] == [
            "study:structure", "study:core_modules", "study:conventions", "study:entry_points",
        ]
        assert study_result["partial"] is False

        # study is read-only against the repository it studies (Acceptance).
        after = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout
        assert after == before

        # Every card is written approved, with no per-card prompt (DECISION F266 D2).
        from packages.memory.local_gateway import list_memory

        cards = list_memory(project_id=study_result["project_id"])
        study_cards = [c for c in cards if c.provenance == "machine-study"]
        assert len(study_cards) == 4
        assert all(c.approved for c in study_cards)
        structure_card = next(c for c in study_cards if c.key == "study:structure")
        assert _MARKER_DIR in structure_card.value

        # teacher ask, in-process so the model transport can be captured — the
        # same "assert what the model was shown" method
        # tests/cli/test_teacher_cmd.py uses for every grounding-source proof.
        captured_prompts: list[str] = []

        def _capturing_call(prompt: str, *, model: str):
            from packages.orchestration.teacher_model import TeacherReply
            from packages.orchestration.teacher_spend import TeacherUsage

            captured_prompts.append(prompt)
            return TeacherReply(text="answered from study cards", usage=TeacherUsage())

        from apps.cli.commands.teacher_cmd import _cmd_teacher_ask

        ask_out = StringIO()
        with contextlib.redirect_stdout(ask_out):
            _cmd_teacher_ask(
                "What are this repository's top-level directories?",
                json_output=True,
                call=_capturing_call,
            )
        ask_result = json.loads(ask_out.getvalue())

        assert len(captured_prompts) == 1
        assert _MARKER_DIR in captured_prompts[0], (
            "the model must be shown the study card carrying the marker "
            "directory - the fact this fixture's answer is only derivable from"
        )
        assert "study" in ask_result["grounding_sources"]
        assert ask_result["refused"] is False

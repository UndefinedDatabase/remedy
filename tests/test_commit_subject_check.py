"""amend1010-cadence-guards — the commit-msg hook's script refuses an unsafe subject."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_commit_subject.py"


def _run(tmp_path: Path, text: str) -> subprocess.CompletedProcess:
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text(text, encoding="utf-8")
    return subprocess.run([sys.executable, str(SCRIPT), str(message)], capture_output=True, text=True, timeout=30)


def test_an_absolute_path_is_refused(tmp_path):
    result = _run(tmp_path, "add /home/alice/x\n")
    assert result.returncode == 1
    assert "metadata scanner" in result.stderr


@pytest.mark.parametrize("subject", [
    "F303 R1: the cockpit reads /api/v1/digest",
    "add review-remedy slash command",
])
def test_a_safe_subject_passes(tmp_path, subject):
    assert _run(tmp_path, subject + "\n").returncode == 0


def test_a_comment_only_message_passes(tmp_path):
    assert _run(tmp_path, "# a comment\n# another\n").returncode == 0

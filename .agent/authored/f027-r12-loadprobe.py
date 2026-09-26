"""F027 R12 C4 — the round's load probe (G4).

Proves the R-1072 repair holds under parallel load: one test, parametrized
over 48 values, each calling
TestWithdrawLiveDoor.test_a_withdrawn_pause_never_parks_the_relaunch with
pytest's own tmp_path/monkeypatch fixtures, run once alone and then all 48
under `pytest -n 16` from a detached worktree of the repaired tree — and
that none of it writes a branch or a worktree into the shared repository.

Usage: python3 f027-r12-loadprobe.py <path-to-detached-worktree>
Run from the primary checkout so its git counts read the shared repository.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRATCH_TEST = '''\
import pytest

# Imported as a module, not "from ... import TestWithdrawLiveDoor": a
# top-level name matching pytest's Test* convention would be collected a
# second time here, over-counting the load proof by one node.
import tests.ui_server.test_pause_door_live as _pause_door_live


@pytest.mark.parametrize("i", range(48))
def test_zz_r1072_load(i, tmp_path, monkeypatch):
    _pause_door_live.TestWithdrawLiveDoor().test_a_withdrawn_pause_never_parks_the_relaunch(
        tmp_path, monkeypatch)
'''


def _counts() -> tuple[int, int]:
    branches = subprocess.run(
        ["git", "for-each-ref", "refs/heads/remedy/"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    worktrees = subprocess.run(
        ["git", "worktree", "list"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    return len(branches), len(worktrees)


def _last_line(text: str) -> str:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else ""


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()

    before_branches, before_worktrees = _counts()
    print(f"BEFORE: remedy branches={before_branches} worktrees={before_worktrees}")

    scratch = worktree / "tests" / "ui_server" / "test_zz_r1072_load.py"
    scratch.write_text(SCRATCH_TEST)

    alone = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/ui_server/test_zz_r1072_load.py::test_zz_r1072_load[0]"],
        cwd=str(worktree), capture_output=True, text=True,
    )
    alone_summary = _last_line(alone.stdout)
    print(f"ALONE exit={alone.returncode}: {alone_summary}")

    loaded = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-n", "16",
         "tests/ui_server/test_zz_r1072_load.py"],
        cwd=str(worktree), capture_output=True, text=True,
    )
    loaded_summary = _last_line(loaded.stdout)
    print(f"LOADED exit={loaded.returncode}: {loaded_summary}")

    after_branches, after_worktrees = _counts()
    print(f"AFTER: remedy branches={after_branches} worktrees={after_worktrees}")

    nothing_leaked = (
        after_branches == before_branches and after_worktrees == before_worktrees
    )
    passed_48 = loaded.returncode == 0 and "48 passed" in loaded_summary
    print(f"LOAD PROOF: 48 passed and nothing leaked: {passed_48 and nothing_leaked}")
    return 0 if (passed_48 and nothing_leaked) else 1


if __name__ == "__main__":
    raise SystemExit(main())

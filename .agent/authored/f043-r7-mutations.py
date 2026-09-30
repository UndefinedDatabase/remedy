#!/usr/bin/env python3
"""F043 R7's red-proof tool (G3, evidence, not product).

One entry, `mutations.py <worktree>`. For each mutation below it edits the landed handler in
`apps/cli/commands/brain.py` inside the given worktree (asserting the FROM text — the landed
handler's own four lines, from `        except OSError:` through `    graph =
build_project_brain` — occurs exactly once there, even though the bare `        except OSError:`
line occurs twice in the file), runs `tests/test_brain_viewer.py` with the worktree as the working
directory and first on `PYTHONPATH`, restores the file's original bytes, and reports whether the
restore was byte-identical. It runs an unmutated control of the same test first and last, so a
test that was already red before any mutation is never mistaken for one a mutation caught.

Both mutations are real behaviour changes DECISION F043 D6's narrowed handler must catch: m1 the
landed handler goes back to catching `Exception` (no mark is needed inside the worktree, since the
ratchet only binds the tree that ships); m2 the landed handler catches `ValueError` in place of
`OSError`.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

TEST_FILE = "tests/test_brain_viewer.py"
TARGET_FILE = "apps/cli/commands/brain.py"

FROM_TEXT = (
    "        except OSError:\n"
    "            pass\n"
    "\n"
    "    graph = build_project_brain"
)

#: label, the FROM text (occurs exactly once, asserted below), the TO text.
MUTATIONS = [
    (
        "m1",
        FROM_TEXT,
        (
            "        except Exception:\n"
            "            pass\n"
            "\n"
            "    graph = build_project_brain"
        ),
    ),
    (
        "m2",
        FROM_TEXT,
        (
            "        except ValueError:\n"
            "            pass\n"
            "\n"
            "    graph = build_project_brain"
        ),
    ),
]


def mutate(path: Path, from_text: str, to_text: str) -> bytes:
    original = path.read_bytes()
    text = original.decode("utf-8")
    count = text.count(from_text)
    if count != 1:
        raise SystemExit(f"FROM text occurs {count} times in {path}, expected exactly 1")
    path.write_text(text.replace(from_text, to_text, 1), encoding="utf-8")
    return original


def restore(path: Path, original: bytes) -> None:
    path.write_bytes(original)
    identical = path.read_bytes() == original
    print(f"restored byte-identical: {identical}")
    if not identical:
        raise SystemExit(f"restore was not byte-identical for {path}")


def run_pytest(worktree: Path) -> tuple[int, str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) if not existing else f"{worktree}:{existing}"
    cmd = ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_FILE]
    proc = subprocess.run(
        cmd, cwd=str(worktree), capture_output=True, text=True, timeout=300, env=env,
    )
    return proc.returncode, proc.stdout + proc.stderr


def pytest_failed_count(output: str) -> str:
    match = re.search(r"(\d+) failed", output)
    return match.group(1) if match else "0"


def report_check(label: str, exit_code: int, output: str) -> bool:
    """Prints the one line the block orders and answers whether the check was caught (non-zero
    exit). A mutation that stayed green is printed exactly as measured — never papered over."""
    reading = f"failed={pytest_failed_count(output)}"
    caught = exit_code != 0
    print(f"{label}: exit={exit_code} {reading}{'' if caught else ' STAYED GREEN'}")
    return caught


def run_control(worktree: Path, when: str) -> bool:
    print(f"=== CONTROL ({when}) ===")
    exit_code, output = run_pytest(worktree)
    ok = exit_code == 0
    print(f"control ({when}): pytest exit={exit_code} failed={pytest_failed_count(output)} all_pass={ok}")
    return ok


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")

    control_before_ok = run_control(worktree, "before")

    all_caught = True
    for label, from_text, to_text in MUTATIONS:
        path = worktree / TARGET_FILE
        original = mutate(path, from_text, to_text)
        try:
            exit_code, output = run_pytest(worktree)
            caught = report_check(label, exit_code, output)
            all_caught = all_caught and caught
        finally:
            restore(path, original)

    control_after_ok = run_control(worktree, "after")

    overall = all_caught and control_before_ok and control_after_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())

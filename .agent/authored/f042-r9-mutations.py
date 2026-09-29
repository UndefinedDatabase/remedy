"""F042 R9 G3 — red-proofs for R-1113's repair (mutation tool).

Given a worktree path, for each mutation below edits
``packages/orchestration/project_cockpit.py`` INSIDE that worktree (asserting
its FROM text occurs exactly once there), runs
``tests/orchestration/test_project_cockpit.py`` with the worktree as the
working directory and first on ``PYTHONPATH``, restores the original bytes,
and prints the run's label, exit code, failed count and FAILED node ids. An
unmutated control runs first and last. Ends with
``ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>``.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

TARGET = "packages/orchestration/project_cockpit.py"
TEST = "tests/orchestration/test_project_cockpit.py"

FROM = (
    "        except (OSError, ValueError):  "
    "# R-1113: an unreadable job's inbox is skipped, never the card\n"
)

_NODE_PREFIX = f"{TEST}::TestProjectSummary::"

MUTATIONS = [
    (
        "m1 the handler catches Exception again",
        "        except Exception:  # R-1113: an unreadable job's inbox is skipped, never the card\n",
        {f"{_NODE_PREFIX}test_an_unexpected_error_in_the_inbox_is_not_swallowed"},
    ),
    (
        "m2 the handler catches OSError alone",
        "        except OSError:  # R-1113: an unreadable job's inbox is skipped, never the card\n",
        {f"{_NODE_PREFIX}test_an_unreadable_jobs_run_log_is_skipped_never_the_card[undecodable]"},
    ),
    (
        "m3 the handler catches ValueError alone",
        "        except ValueError:  # R-1113: an unreadable job's inbox is skipped, never the card\n",
        {f"{_NODE_PREFIX}test_an_unreadable_jobs_run_log_is_skipped_never_the_card[directory]"},
    ),
]


def _run_tests(worktree: Path) -> tuple[int, str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) + (os.pathsep + existing if existing else "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST],
        cwd=str(worktree), env=env, capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _failed_node_ids(output: str) -> list[str]:
    return [line[len("FAILED "):].split(" ")[0] for line in output.splitlines() if line.startswith("FAILED ")]


def _failed_count(output: str) -> int:
    match = re.search(r"(\d+) failed", output)
    return int(match.group(1)) if match else 0


def main() -> None:
    worktree = Path(sys.argv[1]).resolve()
    target_path = worktree / TARGET
    original = target_path.read_bytes()
    from_bytes = FROM.encode("utf-8")
    assert original.count(from_bytes) == 1, "FROM text not found exactly once before any mutation"

    all_clean = True

    def run_labeled(label: str, expected_ids: set[str] | None) -> None:
        nonlocal all_clean
        code, output = _run_tests(worktree)
        failed = _failed_count(output)
        node_ids = _failed_node_ids(output)
        print(f"{label}: exit={code} failed={failed} node_ids={node_ids}")
        if expected_ids is None:
            caught = code == 0 and failed == 0 and not node_ids
        else:
            caught = set(node_ids) == expected_ids and code != 0
        print(f"  caught as expected: {caught}")
        if not caught:
            all_clean = False

    print("--- control (unmutated, first) ---")
    run_labeled("control-first", None)

    for label, to_text, expected_ids in MUTATIONS:
        current = target_path.read_bytes()
        assert current.count(from_bytes) == 1, f"{label}: FROM text not exactly once before mutation"
        target_path.write_bytes(current.replace(from_bytes, to_text.encode("utf-8"), 1))
        print(f"--- {label} ---")
        run_labeled(label, expected_ids)
        target_path.write_bytes(original)
        restored = target_path.read_bytes()
        identical = restored == original
        print(f"restored byte-identical: {identical}")
        if not identical:
            all_clean = False

    print("--- control (unmutated, last) ---")
    run_labeled("control-last", None)

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_clean}")


if __name__ == "__main__":
    main()

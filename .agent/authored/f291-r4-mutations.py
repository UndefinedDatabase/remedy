"""F291 R4 C5 — the round 4 mutation tool (G3 red proofs).

Takes a worktree path as its one argument. For each mutation below it edits the
named file INSIDE that worktree (asserting its FROM text occurs exactly once
there), runs ``python3 -B -m pytest -q -p no:cacheprovider
tests/test_parametrize_ids_stable.py tests/orchestration/test_self_use_generator.py``
with the worktree as the working directory and first on ``PYTHONPATH``, restores
the bytes, and prints one line per mutation: its label, the exit code and the
failed count. It runs an unmutated control first and last, reports
``restored byte-identical: True`` after each restore, and ends with
``ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>``.

After the mutations it plants a dangling link at
``tests/regression/test_runtime_chain_zz_gone.py`` INSIDE the worktree, runs the
same two test files filtered to ``-k "fresh_value_at_collection or
real_tree_offers_a_module"``, prints that exit code and failed count (must be
exit 0), and removes the link.

Never run against the primary checkout — always a disposable worktree.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

TEST_TARGETS = [
    "tests/test_parametrize_ids_stable.py",
    "tests/orchestration/test_self_use_generator.py",
]
GENERATOR_PATH = "packages/orchestration/self_use_generator.py"
GUARD_PATH = "tests/test_parametrize_ids_stable.py"
DANGLING_LINK_RELPATH = "tests/regression/test_runtime_chain_zz_gone.py"
PLANTED_KEXPR = "fresh_value_at_collection or real_tree_offers_a_module"

X2_FROM = (
    "        except FileNotFoundError:\n"
    "            # R-1114, DECISION F291 D4: a test can write and remove a temporary module\n"
    "            # under `tests/` beside this read — gone, not unreadable.\n"
    "            continue\n"
    "        except (OSError, UnicodeDecodeError) as exc:\n"
    "            raise SelfUseGenerationError(f\"{path}: unreadable ({exc})\") from exc\n"
)
X2_TO = (
    "        except FileNotFoundError:\n"
    "            # R-1114, DECISION F291 D4: a test can write and remove a temporary module\n"
    "            # under `tests/` beside this read — gone, not unreadable.\n"
    "            continue\n"
    "        except (OSError, UnicodeDecodeError) as exc:\n"
    "            continue\n"
)

MUTATIONS = [
    {
        "label": "x1 (Tier 5's new clause catches ValueError in place of FileNotFoundError)",
        "path": GENERATOR_PATH,
        "from_text": "        except FileNotFoundError:\n",
        "to_text": "        except ValueError:\n",
    },
    {
        "label": "x2 (Tier 5's reader skips every read error: the (OSError, UnicodeDecodeError) clause also continues)",
        "path": GENERATOR_PATH,
        "from_text": X2_FROM,
        "to_text": X2_TO,
    },
    {
        "label": "x3 (the guard's new clause catches ValueError in place of FileNotFoundError)",
        "path": GUARD_PATH,
        "from_text": "        except FileNotFoundError:\n",
        "to_text": "        except ValueError:\n",
    },
]


def _env_with_pythonpath(worktree: Path) -> dict[str, str]:
    env = {**os.environ}
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) + (f":{existing}" if existing else "")
    return env


def _run_pytest(worktree: Path, extra_args: list[str] | None = None) -> tuple[int, str]:
    args = ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_TARGETS]
    if extra_args:
        args.extend(extra_args)
    result = subprocess.run(
        args,
        cwd=str(worktree),
        env=_env_with_pythonpath(worktree),
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout + result.stderr


def _failed_count(output: str) -> int:
    match = re.search(r"(\d+) failed", output)
    return int(match.group(1)) if match else 0


def _passed_count(output: str) -> int:
    match = re.search(r"(\d+) passed", output)
    return int(match.group(1)) if match else 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f291-r4-mutations.py <worktree-path>")
        return 2
    worktree = Path(sys.argv[1]).resolve()

    all_ok = True

    # Control run FIRST — unmutated, must pass.
    exit_code, output = _run_pytest(worktree)
    failed = _failed_count(output)
    print(f"control (before) exit={exit_code} failed={failed}")
    if exit_code != 0 or failed != 0:
        all_ok = False

    for mutation in MUTATIONS:
        target = worktree / mutation["path"]
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(mutation["from_text"])
        if occurrences != 1:
            print(
                f"{mutation['label']}: FROM text occurs {occurrences} times in "
                f"{mutation['path']}, expected exactly 1 — STOP"
            )
            return 1
        mutated_text = original_text.replace(mutation["from_text"], mutation["to_text"], 1)
        target.write_bytes(mutated_text.encode("utf-8"))
        try:
            exit_code, output = _run_pytest(worktree)
            failed = _failed_count(output)
            print(f"{mutation['label']}: exit={exit_code} failed={failed}")
            if exit_code == 0:
                all_ok = False
        finally:
            target.write_bytes(original)
            restored = target.read_bytes()
            identical = restored == original
            print(f"restored byte-identical: {identical}")
            if not identical:
                all_ok = False

    # Control run LAST — unmutated again, must pass.
    exit_code, output = _run_pytest(worktree)
    failed = _failed_count(output)
    print(f"control (after) exit={exit_code} failed={failed}")
    if exit_code != 0 or failed != 0:
        all_ok = False

    # The planted-vanished-file run: a dangling link under tests/regression/ must be
    # skipped cleanly by both readers, not raised over (R-1114).
    link_path = worktree / DANGLING_LINK_RELPATH
    link_path.symlink_to(worktree / "tests" / "regression" / "_zz_gone_target_missing.py")
    try:
        exit_code, output = _run_pytest(worktree, extra_args=["-k", PLANTED_KEXPR])
        passed = _passed_count(output)
        failed = _failed_count(output)
        print(f"planted dangling link run: exit={exit_code} passed={passed} failed={failed}")
        if exit_code != 0 or failed != 0:
            all_ok = False
    finally:
        link_path.unlink()

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

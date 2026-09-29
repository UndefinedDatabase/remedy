"""F041 R4 C5 — the round 4 mutation tool (G4's red proofs, DECISION F041 D4).

Takes ONE argument: the path of a worktree checked out at C5. For each mutation
below it edits the named production file INSIDE that worktree — asserting its
FROM text occurs EXACTLY ONCE there — runs the named test file with the
worktree as the working directory and its own root first on PYTHONPATH,
restores the file's original bytes, and reports whether the mutation was
CAUGHT: real exit code 1 with at least one failed test. A collection error
(any other non-zero exit, or a zero exit) is a broken edit, not a reading.

Every test file a mutation names is also run UNMUTATED, once before the first
mutation and once after the last, as the control.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

FAILED_RE = re.compile(r"(\d+) failed")


@dataclass(frozen=True)
class Mutation:
    label: str
    prod_path: str
    test_path: str
    from_text: str
    to_text: str


MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        "q1 preview_view answers the stored link in every state",
        "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        '        "url": record["url"] if live else "",\n'
        '        "port": record["port"] if live else 0,\n',
        '        "url": record["url"],\n'
        '        "port": record["port"],\n',
    ),
    Mutation(
        "q2 mark_viewed writes a record that is not live",
        "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        '    record = load_preview(job_id, data_root)\n'
        '    if record["state"] != STATE_LIVE:\n'
        '        return record\n'
        '    record = dict(record)\n'
        '    record["viewed_at"] = now.isoformat()\n'
        '    _persist(record, job_id, data_root)\n'
        '    return record\n',
        '    record = load_preview(job_id, data_root)\n'
        '    record = dict(record)\n'
        '    record["viewed_at"] = now.isoformat()\n'
        '    _persist(record, job_id, data_root)\n'
        '    return record\n',
    ),
    Mutation(
        "q3 idle_stop_due expires a preview whose ttl is zero or less",
        "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        '    if record["state"] != STATE_LIVE or ttl_seconds <= 0:\n'
        '        return False\n',
        '    if record["state"] != STATE_LIVE:\n'
        '        return False\n',
    ),
    Mutation(
        "q4 revalidate_live no longer stops a preview that stopped answering",
        "packages/orchestration/preview_control.py",
        "tests/orchestration/test_preview_control.py",
        '    message = _verb_message(probed)\n'
        '    runner("stop", root)\n'
        '    settled = _settle(\n'
        '        record, state=STATE_FAILED, reason=f"the app stopped answering: {message}",\n',
        '    message = _verb_message(probed)\n'
        '    settled = _settle(\n'
        '        record, state=STATE_FAILED, reason=f"the app stopped answering: {message}",\n',
    ),
    Mutation(
        "q5 step no longer revalidates a live preview",
        "packages/orchestration/preview_worker.py",
        "tests/orchestration/test_preview_worker.py",
        '            record = preview_control.revalidate_live(\n'
        '                job, runner, now=now, data_root=self._data_root)\n'
        '            if record["state"] != preview_control.STATE_LIVE:\n'
        '                with self._lock:\n'
        '                    self._live.discard(job_id)\n',
        '            pass\n',
    ),
    Mutation(
        "q6 close no longer stops the previews the worker keeps live",
        "packages/orchestration/preview_worker.py",
        "tests/orchestration/test_preview_worker.py",
        '            self._thread = None\n'
        '        self.stop_all()\n',
        '            self._thread = None\n',
    ),
    Mutation(
        "q7 the door no longer hands the job to the worker",
        "packages/orchestration/ui_server.py",
        "tests/ui_server/test_preview_commands.py",
        '        if self.preview_worker is not None:\n'
        '            self.preview_worker.submit(job_id)\n',
        '',
    ),
    Mutation(
        "q8 adopt_live takes on a record whatever its state",
        "packages/orchestration/preview_worker.py",
        "tests/orchestration/test_preview_worker.py",
        '            record = preview_control.load_preview(job_id, self._data_root)\n'
        '            if record["state"] == preview_control.STATE_LIVE:\n'
        '                with self._lock:\n'
        '                    self._live.add(job_id)\n',
        '            record = preview_control.load_preview(job_id, self._data_root)\n'
        '            with self._lock:\n'
        '                self._live.add(job_id)\n',
    ),
)


def _ordered_test_files() -> list[str]:
    seen: list[str] = []
    for mutation in MUTATIONS:
        if mutation.test_path not in seen:
            seen.append(mutation.test_path)
    return seen


def run_pytest(worktree: Path, test_path: str) -> tuple[int, int, str]:
    """Run one test file inside ``worktree``, the worktree's own root first on
    PYTHONPATH. Returns (real exit code, failed-test count, combined output)."""
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) + (os.pathsep + existing if existing else "")
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", test_path],
        cwd=str(worktree), capture_output=True, text=True, env=env, check=False,
    )
    output = result.stdout + result.stderr
    match = FAILED_RE.search(output)
    failed = int(match.group(1)) if match else 0
    return result.returncode, failed, output


def run_control(worktree: Path, label: str) -> bool:
    clean = True
    for test_path in _ordered_test_files():
        code, failed, output = run_pytest(worktree, test_path)
        print(f"control ({label}) {test_path}: exit={code} failed={failed}")
        if code != 0 or failed != 0:
            clean = False
            print(output)
    return clean


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: f041-r4-mutations.py <worktree-path>", file=sys.stderr)
        sys.exit(2)
    worktree = Path(sys.argv[1]).resolve()

    all_clean = True
    all_clean &= run_control(worktree, "first")

    for mutation in MUTATIONS:
        prod_file = worktree / mutation.prod_path
        original = prod_file.read_bytes()
        text = original.decode("utf-8")
        occurrences = text.count(mutation.from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{mutation.label}: FROM text occurs {occurrences} times in "
                f"{mutation.prod_path}, expected exactly 1")
        mutated_text = text.replace(mutation.from_text, mutation.to_text, 1)
        prod_file.write_text(mutated_text, encoding="utf-8")

        try:
            code, failed, output = run_pytest(worktree, mutation.test_path)
        finally:
            prod_file.write_bytes(original)

        caught = code == 1 and failed >= 1
        print(f"{mutation.label}: exit={code} failed={failed} caught={caught}")
        if not caught:
            print(output)
            all_clean = False

        restored = prod_file.read_bytes()
        identical = restored == original
        print(f"restored byte-identical: {identical}")
        if not identical:
            all_clean = False

    all_clean &= run_control(worktree, "last")

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_clean}")
    sys.exit(0 if all_clean else 1)


if __name__ == "__main__":
    main()

"""F036 R3 G5 — red-proof tool: mutate the round 3 storage/hook/CLI code, prove
each mutation turns tests/orchestration/test_result_tour.py or
tests/cli/test_job_show.py red, restore.

Usage:
    python3 -B .agent/authored/f036-r3-mutations.py <worktree-path>

For each mutation below: edit the named file INSIDE the given worktree
(asserting the FROM text occurs exactly once), run BOTH test files from the
worktree's own root with that root FIRST on sys.path (via PYTHONPATH) after
purging `__pycache__`, restore the original bytes, and print one line: the
label, the exit code, the failed count and the failing node ids. An
unmutated control runs first and last. Ends with "restored byte-identical:
<bool>" and "ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>".
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TEST_RELS = ("tests/orchestration/test_result_tour.py", "tests/cli/test_job_show.py")

RESULT_TOUR = "packages/orchestration/result_tour.py"
LONG_RUN_EXECUTOR = "packages/orchestration/long_run_executor.py"
JOB_CMD = "apps/cli/commands/job.py"

#: (label, target file, FROM text, TO text) — each FROM text must occur
#: exactly once in the unmutated file; each mutation is a real behaviour
#: change the F036 R3 block names under G5.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    ("m1 every write goes to version 1, overwriting tour.json",
     RESULT_TOUR,
     """        versions = stored_tour_versions(job_id)
        next_version = (versions[-1] if versions else 0) + 1
        path = tour_path(job_id, next_version)""",
     """        versions = stored_tour_versions(job_id)
        next_version = 1  # MUTATED: always version 1
        path = tour_path(job_id, next_version)"""),
    ("m2 load_result_tour answers the LOWEST stored version",
     RESULT_TOUR,
     """    version = versions[-1]
    path = tour_path(job_id, version)""",
     """    version = versions[0]  # MUTATED: lowest version
    path = tour_path(job_id, version)"""),
    ("m3 write_result_tour catches no OSError",
     RESULT_TOUR,
     "    except (OSError, ValueError, ResultTourError) as exc:",
     "    except (ValueError, ResultTourError) as exc:  # MUTATED: no OSError"),
    ("m4 a good write leaves tour_error in place",
     RESULT_TOUR,
     """    metadata = getattr(job, "metadata", None)
    if isinstance(metadata, dict):
        metadata.pop(TOUR_ERROR_METADATA_KEY, None)
    return path""",
     """    metadata = getattr(job, "metadata", None)
    if isinstance(metadata, dict):
        pass  # MUTATED: leaves tour_error in place
    return path"""),
    ("m5 load_result_tour skips the tour_problems check",
     RESULT_TOUR,
     "    problems = tour_problems(tour)",
     "    problems = []  # MUTATED: skip tour_problems check"),
    ("m6 render_tour_lines omits each stop's anchor line",
     RESULT_TOUR,
     """        anchor = stop["anchor"]
        lines.append(f"     -> {anchor['kind']}: {anchor['ref']}")""",
     """        anchor = stop["anchor"]  # MUTATED: anchor line omitted"""),
    ("m7 stored_tour_versions counts directories too",
     RESULT_TOUR,
     """            if not child.is_file():
                continue""",
     """            if False:  # MUTATED: count directories too
                continue"""),
    ("m8 the hook runs outside the report's condition, for every terminal",
     LONG_RUN_EXECUTOR,
     """        write_final_report(job)

        from packages.orchestration.result_tour import write_result_tour

        # Never raises either (DECISION F036 D4 (3)): the tour's first stop
        # can anchor to the report just written above.
        write_result_tour(job)
    return job_status""",
     """        write_final_report(job)

    from packages.orchestration.result_tour import write_result_tour  # MUTATED: outside condition

    # Never raises either (DECISION F036 D4 (3)): the tour's first stop
    # can anchor to the report just written above.
    write_result_tour(job)
    return job_status"""),
    ("m9 --tour builds every section, not only tour",
     JOB_CMD,
     """    elif tour:
        # `--tour` alone: the `tour` section, built and printed the way `--full` does.
        shown["sections"], section_text = _build_show_sections(job, names=("tour",))""",
     """    elif tour:
        # `--tour` alone: the `tour` section, built and printed the way `--full` does.
        shown["sections"], section_text = _build_show_sections(job)  # MUTATED: every section"""),
    ("m10 with nothing stored the section raises tour_unreadable",
     JOB_CMD,
     """    if loaded is None:
        stored, version, tour = False, 0, build_fallback_tour(job)
    else:
        stored, (version, tour) = True, loaded""",
     """    if loaded is None:
        raise ShowSectionError("tour_unreadable", "MUTATED: nothing stored raises")
    else:
        stored, (version, tour) = True, loaded"""),
)

_FAILED_COUNT_RE = re.compile(r"(\d+) failed")
_FAILED_NODE_RE = re.compile(r"^FAILED (\S+)", re.MULTILINE)


def _purge_pycache(root: Path) -> None:
    for directory in root.rglob("__pycache__"):
        if directory.is_dir():
            shutil.rmtree(directory, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    """Run both round 3 test files inside *root*; (exit_code, failed_count, failing_ids)."""
    _purge_pycache(root)
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(root) + (os.pathsep + existing if existing else "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_RELS],
        cwd=str(root), env=env, capture_output=True, text=True,
    )
    output = proc.stdout + proc.stderr
    failed_match = _FAILED_COUNT_RE.search(output)
    failed_count = int(failed_match.group(1)) if failed_match else 0
    failing_ids = _FAILED_NODE_RE.findall(output)
    return proc.returncode, failed_count, failing_ids


def _report(label: str, exit_code: int, failed_count: int, failing_ids: list[str]) -> None:
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={failing_ids}")


def main() -> None:
    worktree = Path(sys.argv[1]).resolve()
    targets = {RESULT_TOUR, LONG_RUN_EXECUTOR, JOB_CMD}
    originals = {rel: (worktree / rel).read_bytes() for rel in targets}

    exit_code, failed_count, failing_ids = _run_tests(worktree)
    _report("control (before)", exit_code, failed_count, failing_ids)
    control_before_ok = exit_code == 0 and failed_count == 0

    all_caught = True
    for label, target_rel, from_text, to_text in MUTATIONS:
        target = worktree / target_rel
        original_bytes = originals[target_rel]
        original_text = original_bytes.decode("utf-8")
        occurrences = original_text.count(from_text)
        assert occurrences == 1, f"{label}: FROM text occurs {occurrences} times, not 1"
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed_count, failing_ids = _run_tests(worktree)
        finally:
            target.write_bytes(original_bytes)
        _report(label, exit_code, failed_count, failing_ids)
        if failed_count < 1:
            all_caught = False

    exit_code, failed_count, failing_ids = _run_tests(worktree)
    _report("control (after)", exit_code, failed_count, failing_ids)
    control_after_ok = exit_code == 0 and failed_count == 0

    restored = all((worktree / rel).read_bytes() == originals[rel] for rel in targets)
    print(f"restored byte-identical: {restored}")

    overall = all_caught and control_before_ok and control_after_ok and restored
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")


if __name__ == "__main__":
    main()

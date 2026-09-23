"""F278 R2 G5 — revert probes, run inside a DISPOSABLE worktree at the round's last code commit.

Usage: python3 revert_probes.py <worktree-path> <round-base-sha>. For each probe the named
production files are restored from the round base while every test stays at the round's
version; the probe then runs the named test files and must go red. An unmutated control runs
first and last, and the tree is restored with `git checkout HEAD -- <files>` after each probe.
"""
import subprocess
import sys

WT, BASE = sys.argv[1], sys.argv[2]
TESTS = [
    "tests/orchestration/test_durable_write_guard.py",
    "tests/orchestration/test_checkpoints.py",
    "tests/orchestration/test_task_execution.py",
]
PROBES = {
    "p1_pingpong_helper_only": ["packages/orchestration/pingpong_job.py"],
    "p2_pingpong_group": [
        "packages/orchestration/pingpong_job.py",
        "packages/orchestration/checkpoints.py",
        "packages/orchestration/mission_compiler.py",
        "packages/orchestration/mission_state.py",
    ],
    "p3_proposed_tasks": ["packages/orchestration/proposed_tasks.py"],
}


def git(*args: str) -> None:
    subprocess.run(["git", "-C", WT, *args], check=True)


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or ln.startswith("ERROR")
            or " passed" in ln or " failed" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


run("control_before")
for name, files in PROBES.items():
    git("checkout", BASE, "--", *files)
    run(name)
    git("checkout", "HEAD", "--", *files)
    status = subprocess.run(["git", "-C", WT, "status", "--porcelain"],
                            capture_output=True, text=True).stdout
    print(f"{name} restored clean: {status == ''}")
run("control_after")

"""F278 R3 G5 — revert probes, run inside a DISPOSABLE worktree at the round's last code commit.

Usage: python3 revert_probes.py <worktree-path> <round-base-sha>. For each probe the named
production file is restored from the round base while every test stays at the round's
version; the probe then runs the named test files and must go red. An unmutated control runs
first and last, and the tree is restored with `git checkout HEAD -- <files>` after each probe.
"""
import subprocess
import sys

WT, BASE = sys.argv[1], sys.argv[2]
TESTS = [
    "tests/orchestration/test_durable_write_guard.py",
    "tests/orchestration/test_real_test_execution.py",
    "tests/orchestration/test_self_dogfood_execution.py",
    "tests/orchestration/test_token_economy.py",
]
PROBES = {
    "p1_real_test_execution": ["packages/orchestration/real_test_execution.py"],
    "p2_self_dogfood_execution": ["packages/orchestration/self_dogfood_execution.py"],
    "p3_token_economy": ["packages/orchestration/token_economy.py"],
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

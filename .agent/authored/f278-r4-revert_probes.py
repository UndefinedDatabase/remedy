"""F278 R4 G5 — revert probes, run inside a DISPOSABLE worktree at the round's last code commit.

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
    "tests/orchestration/test_repository_snapshot.py",
    "tests/test_project_registry.py",
]
PROBES = {
    "p1_dev_server_only": ["packages/runtimes/dev_server.py"],
    "p2_dev_server_group": [
        "packages/runtimes/dev_server.py",
        "packages/runtimes/runtime_supervisor.py",
        "apps/cli/commands/runtime_cmd.py",
    ],
    "p3_repository_snapshot": ["packages/orchestration/repository_snapshot.py"],
    "p4_project_registry": ["packages/orchestration/project_registry.py"],
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

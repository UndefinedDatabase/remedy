"""F015 R6 G5 — red proofs of the two closure-suite repairs, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
m1 removes the repair itself. m2 is a MECHANISM probe: a zero hang guard must reproduce the
closure suite's own failure message, which shows the guard is what fired there.
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/runtimes/test_supervisor_portability.py::TestPostHandshakeTerminalState",
         "tests/cli/test_real_test_execution_cli.py::test_json_purity"]
MUTATIONS = {
    "m1_stop_never_waits_for_the_exiting_supervisor": (
        "packages/runtimes/dev_server.py",
        "            while time.monotonic() < deadline and _pid_alive(state.supervisor_pid):\n",
        "            while False:\n",
    ),
    "m2_a_zero_hang_guard_reproduces_the_suite_failure": (
        "tests/cli/runtime_helpers.py",
        "    timeout: int = 30,\n",
        "    timeout: int = 0,\n",
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or " passed" in ln or " failed" in ln
            or "timed out after" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


run("control_before")
for name, (rel, frm, to) in MUTATIONS.items():
    path = WT / rel
    good = path.read_bytes()
    text = good.decode("utf-8")
    print(f"{name} FROM count in {rel}: {text.count(frm)}")
    if text.count(frm) != 1:
        sys.exit(f"{name}: FROM must occur exactly once; stopping")
    path.write_text(text.replace(frm, to, 1), encoding="utf-8")
    run(name)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
run("control_after")

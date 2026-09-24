"""F284 R2 red proofs: python3 -B mutations.py <worktree> <base sha> <probe plugin path>.

Runs the five teardown nodes of tests/orchestration/test_product_smoke.py under the R-0950 probe
plugin's modes, with this round's test file ("new") and with the file at <base> ("old"), and
restores the file byte-identical after each "old" run. Unmutated controls run first and last.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
PROBE = Path(sys.argv[3]).resolve()
REL = "tests/orchestration/test_product_smoke.py"
F = "tests/orchestration/test_product_smoke.py::"
NODES = [F + "TestAppStartsGreen::test_the_app_is_always_stopped",
         F + "test_no_zombie_processes_after_the_suite",
         F + "TestCorePathsRun::test_the_app_is_stopped_after_a_path_failure",
         F + "TestCleanConsoleRun::test_the_app_is_stopped_even_when_the_console_is_dirty",
         F + "test_no_zombie_processes_after_every_outcome"]
# label, mode, file version, expected exit
RUNS = [
    ("control first", "", "new", 0),
    ("p1 FOREIGN, this round's file", "FOREIGN", "new", 0),
    ("p2 FOREIGN, the base file", "FOREIGN", "old", 1),
    ("p3 LEAK, this round's file", "LEAK", "new", 1),
    ("p4 REPORTED, this round's file", "REPORTED", "new", 1),
    ("p5 REPORTED, the base file", "REPORTED", "old", 1),
    ("m1 LEAK, the owner check removed", "LEAK", "mut", 1),
    ("control last", "", "new", 0),
]
OWNER_FROM = '            assert listeners_inside(port, root) == [], f"port {port} still held by this app"\n'
OWNER_TO = "            pass\n"


def app_processes():
    """Live processes started from a pytest temporary project, as a count."""
    import psutil

    count = 0
    for proc in psutil.process_iter(["cmdline", "cwd"]):
        cwd = proc.info.get("cwd") or ""
        cmd = " ".join(proc.info.get("cmdline") or [])
        if "pytest-of-" in cwd and "_app.py" in cmd:
            count += 1
    return count


target = WT / REL
new_bytes = target.read_bytes()
old_bytes = subprocess.run(["git", "-C", str(WT), "show", f"{BASE}:{REL}"],
                           capture_output=True, check=True).stdout
new_text = new_bytes.decode("utf-8")
print(f"m1 FROM occurs {new_text.count(OWNER_FROM)}x in {REL}")
mut_bytes = new_text.replace(OWNER_FROM, OWNER_TO).encode("utf-8")
before = app_processes()
shutil.copyfile(PROBE, WT / "r0950_probe.py")
ok = new_text.count(OWNER_FROM) == 1
try:
    for label, mode, version, expected in RUNS:
        if version == "old":
            target.write_bytes(old_bytes)
        elif version == "mut":
            target.write_bytes(mut_bytes)
        env = dict(os.environ, R0950_MODE=mode)
        try:
            r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                "-p", "r0950_probe", *NODES], cwd=WT, env=env,
                               capture_output=True, text=True)
        finally:
            target.write_bytes(new_bytes)
        lines = [ln for ln in r.stdout.splitlines() if re.search(r"\d+ (passed|failed)", ln)]
        summary = lines[-1] if lines else r.stdout[-300:]
        failed = sorted(ln.split("::")[-1].split(" ")[0] for ln in r.stdout.splitlines()
                        if ln.startswith("FAILED"))
        print(f"{label}: exit {r.returncode}: {summary}; failed: {failed}")
        ok = ok and r.returncode == expected
    restored = target.read_bytes() == new_bytes
    print(f"test file restored byte-identical: {restored}")
    ok = ok and restored
finally:
    (WT / "r0950_probe.py").unlink()
after = app_processes()
print(f"fixture app processes alive before: {before}, after: {after}")
ok = ok and after == before
print(f"ALL PROBES READ AS EXPECTED AND RESTORED CLEANLY: {ok}")

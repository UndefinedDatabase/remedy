"""F015 R10 G4 probe: run from the root of a disposable worktree at the round's C2.

Usage: python3 -B <payload dir>/probe.py <payload dir>/
Prints three readings and restores the test file byte-identical to its C2 state.
"""
import subprocess
import sys

PATH = "tests/runtimes/test_supervisor_portability.py"
PAY = sys.argv[1]
FROM = open(PAY + "test_from.txt", encoding="utf-8").read()
TO = open(PAY + "test_to.txt", encoding="utf-8").read()
NODES = [
    PATH + "::TestPersistentLogPumpHealth::test_a_broken_helper_thread_fails_the_regression",
    PATH + "::TestPersistentLogPumpHealth::test_a_pump_failure_racing_the_application_exit_is_recorded_honestly",
]
SLOW_FROM = FROM.replace('"w") as fh:\n',
                         '"w") as fh:\n        if name == "error": time.sleep(1.0)\n')
SLOW_TO = TO.replace("    os.replace(scratch, path)\n",
                     '    if name == "error": time.sleep(1.0)\n    os.replace(scratch, path)\n')
assert SLOW_FROM != FROM and SLOW_TO != TO

with open(PATH, "rb") as fh:
    c2 = fh.read()
text = c2.decode("utf-8")
assert text.count(TO) == 1 and text.count(FROM) == 0, "not the C2 state"


def run(label, body):
    with open(PATH, "w", encoding="utf-8") as fh:
        fh.write(body)
    subprocess.run("find . -name __pycache__ -type d -prune -exec rm -rf {} +",
                   shell=True, check=True)
    proc = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p",
                           "no:cacheprovider", *NODES], capture_output=True, text=True)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    failed = [ln for ln in lines if ln.startswith("FAILED")]
    print(label, "| exit", proc.returncode, "|", lines[-1] if lines else "", "|", failed)


try:
    run("CONTROL the C2 file", text)
    run("RED the old _mark, error marker paused 1s before its write",
        text.replace(TO, SLOW_FROM))
    run("GREEN the new _mark, error marker paused 1s before its rename",
        text.replace(TO, SLOW_TO))
finally:
    with open(PATH, "wb") as fh:
        fh.write(c2)
with open(PATH, "rb") as fh:
    print("restored byte-identical:", fh.read() == c2)

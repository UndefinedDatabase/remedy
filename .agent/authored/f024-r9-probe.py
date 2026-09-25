"""F024 R9 G4 probe: run from the root of a disposable worktree at the round's C2.

Usage: python3 -B <payload dir>/probe.py <payload dir>/
Links the primary checkout's apps/ui/node_modules into the worktree (gitignored, absent from
any fresh worktree, and the node skips without it), prints three readings of the live scrub
node, restores the test file byte-identical to its C2 state and removes the link.
"""
import os
import subprocess
import sys

PATH = "tests/ui_server/test_timeline_scrub_live.py"
PAY = sys.argv[1]
FROM = open(PAY + "test_from.txt", encoding="utf-8").read()
TO = open(PAY + "test_to.txt", encoding="utf-8").read()
LINK = "apps/ui/node_modules"
PRIMARY = "/home/decodeux/Repos/remedy/apps/ui/node_modules"

with open(PATH, "rb") as fh:
    c2 = fh.read()
text = c2.decode("utf-8")
assert text.count(TO) == 1 and text.count(FROM) == 0, "not the C2 state"
assert not os.path.lexists(LINK), "the worktree already holds apps/ui/node_modules"
os.symlink(PRIMARY, LINK)


def run(label, body, ci):
    with open(PATH, "w", encoding="utf-8") as fh:
        fh.write(body)
    subprocess.run("find . -name __pycache__ -type d -prune -exec rm -rf {} +",
                   shell=True, check=True)
    env = {k: v for k, v in os.environ.items() if k not in ("CI", "FORCE_COLOR", "NO_COLOR")}
    if ci:
        env["CI"] = "true"
    proc = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-rfs", "-p",
                           "no:cacheprovider", PATH], capture_output=True, text=True, env=env)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    failed = [ln[:90] for ln in lines if ln.startswith(("FAILED", "SKIPPED"))]
    print(label, "| exit", proc.returncode, "|", lines[-1] if lines else "", "|", failed)


try:
    run("CONTROL the C2 file, CI unset", text, False)
    run("RED the old line, CI=true", text.replace(TO, FROM), True)
    run("GREEN the C2 file, CI=true", text, True)
finally:
    with open(PATH, "wb") as fh:
        fh.write(c2)
    os.remove(LINK)
with open(PATH, "rb") as fh:
    print("restored byte-identical:", fh.read() == c2)
print("link removed:", not os.path.lexists(LINK))

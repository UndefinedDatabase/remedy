"""F278 T003 — prove a marking commit changes COMMENTS only, never code.

Usage: python3 marking_check.py <repo> <commit> [<commit> ...]. For each commit, every
changed line pair from `git diff -U0 <commit>~1 <commit>` must keep the same code: the text
before the first `#` that starts a comment, stripped of trailing spaces, is identical, the
new line carries `# noqa: BLE001 — ` followed by a non-empty reason, and the commit adds and
removes the same number of lines. Prints one verdict line per commit and exits 1 on any
violation.
"""
import re
import subprocess
import sys

REPO = sys.argv[1]
NOQA = re.compile(r"# noqa: BLE001 — \S")


def code_part(line: str) -> str:
    # The handler lines this checks contain no string literal holding a `#`.
    return line.split("#", 1)[0].rstrip()


bad = 0
for commit in sys.argv[2:]:
    diff = subprocess.run(["git", "-C", REPO, "diff", "-U0", f"{commit}~1", commit],
                          capture_output=True, text=True, check=True).stdout
    removed, added, problems = [], [], []
    for ln in diff.splitlines():
        if ln.startswith("---") or ln.startswith("+++"):
            continue
        if ln.startswith("-"):
            removed.append(ln[1:])
        elif ln.startswith("+"):
            added.append(ln[1:])
    if len(removed) != len(added):
        problems.append(f"{len(removed)} lines removed but {len(added)} added")
    for old, new in zip(removed, added):
        if code_part(old) != code_part(new):
            problems.append(f"code changed: {old.strip()!r} -> {new.strip()!r}")
        if not NOQA.search(new):
            problems.append(f"no reasoned noqa: {new.strip()!r}")
    verdict = "OK" if not problems else "VIOLATION"
    print(f"{commit} {verdict} pairs={len(added)}")
    for p in problems[:10]:
        print("   ", p)
    bad += bool(problems)
sys.exit(1 if bad else 0)

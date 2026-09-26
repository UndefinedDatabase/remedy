"""Build F027 R14's closure payloads in a simulated tree at 409f285e: book R13, rotate, closure edits.
Adapted from `.agent/authored/f026-r8-build.py`. F027 consumed no self-use item (the track read
`self-use NONE (queue exhausted)`), so `scripts/self_use_queue.json` is not edited."""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/decodeux/Repos/remedy")
SRC = REPO / ".remedy-wt/f027-r14"
SIM = REPO / ".remedy-wt/f027-r14-sim"
BASE = "409f285ea"
STATUS_LINE = ("- [x] F027 — Task veto (T001–T003 complete; "
               "accepted 2026-09-26 · live review PASS — ACCEPTED · Evidence job f027r13e1001 · "
               "package remedy-review-20260926-111715-READY_FOR_REVIEW.zip · SHA-256 "
               "abb65b1df0346c8670423a7da903e3e3c6facfc4cac4602bb5a983b47b4bd993 · package path "
               "/home/decodeux/Repos/remedy-history/zips · accepted HEAD f3afc333a70eae5f339fce8c18004db68a7cea1f)")


def sh(*a, cwd=SIM, check=True):
    return subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, check=check).stdout


def sha(p):
    b = Path(p).read_bytes()
    return len(b), hashlib.sha256(b).hexdigest()


def replace_once(path, old, new):
    t = path.read_text(encoding="utf-8")
    assert t.count(old) == 1, (path, old)
    path.write_text(t.replace(old, new), encoding="utf-8")


if SIM.exists():
    sh("git", "worktree", "remove", "--force", str(SIM), cwd=REPO)
sh("git", "worktree", "add", "--detach", str(SIM), BASE, cwd=REPO)
(SRC / "status_line.txt").write_text(STATUS_LINE + "\n", encoding="utf-8")

# C2 — the booking
lr = SIM / ".agent/live_review.md"
lr.write_bytes(lr.read_bytes() + (SRC / "ledger.md").read_bytes())
shutil.copyfile(SRC / "plan.md", SIM / ".agent/plan.md")
sh("git", "add", "-A")
sh("git", "commit", "-q", "-m", "sim C2")
print("C2 numstat", sh("git", "show", "--numstat", "--format=", "HEAD").split())
for p in (".agent/live_review.md", ".agent/plan.md"):
    print("C2", p, *sha(SIM / p))
sys.path.insert(0, str(SIM / "scripts"))
from rotate_live_review import open_finding_ids  # noqa: E402

print("open at C2", sorted(open_finding_ids(lr.read_text(encoding="utf-8"))))

# C3 — the rotation
rot = subprocess.run([sys.executable, "scripts/rotate_live_review.py"], cwd=SIM, capture_output=True, text=True)
print("ROTATION exit", rot.returncode)
print(rot.stdout.strip())
sh("git", "add", "-A")
sh("git", "commit", "-q", "-m", "sim C3")
print("C3 numstat", sh("git", "show", "--numstat", "--format=", "HEAD").split())
for p in (".agent/live_review.md", ".agent/live_review_archive.md"):
    print("C3", p, *sha(SIM / p))

# C4 — the closure edits
replace_once(SIM / "docs/roadmap/STATUS.md", "- [~] F027 — Task veto\n", STATUS_LINE + "\n")
replace_once(SIM / "README.md", "105 of 286 registered items accepted.", "106 of 286 registered items accepted.")
replace_once(SIM / "README.md", "| 5 | Operator Cockpit | 22 | 34 |", "| 5 | Operator Cockpit | 23 | 34 |")
para = (SRC / "readme_para.txt").read_text(encoding="utf-8")
replace_once(SIM / "README.md", "\nFull per-feature state: [`docs/roadmap/STATUS.md`]",
             "\n" + para + "\nFull per-feature state: [`docs/roadmap/STATUS.md`]")
diff = sh("git", "diff", "HEAD")
(SRC / "closure.diff").write_text(diff, encoding="utf-8")
print("closure.diff numstat", sh("git", "diff", "--numstat", "HEAD").split())
for p in ("docs/roadmap/STATUS.md", "README.md"):
    print("C4", p, *sha(SIM / p))
print("status line count", (SIM / "docs/roadmap/STATUS.md").read_text().splitlines().count(STATUS_LINE))
sel = ["tests/docs/", "tests/cli/test_advertised_commands.py", "tests/orchestration/test_live_review_rotation.py",
       "tests/orchestration/test_integrity_gate.py", "tests/orchestration/test_self_use_generator.py"]
run = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *sel], cwd=SIM,
                     capture_output=True, text=True)
print("selection exit", run.returncode, run.stdout.strip().splitlines()[-1])
integ = subprocess.run([sys.executable, "-m", "apps.cli.main", "integrity", "check", "--json"], cwd=SIM,
                       capture_output=True, text=True)
print("integrity", integ.returncode, integ.stdout.strip()[-120:])
# red control: the accepted count left at 105
replace_once(SIM / "README.md", "106 of 286 registered items accepted.", "105 of 286 registered items accepted.")
red = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/docs/"], cwd=SIM,
                     capture_output=True, text=True)
print("red control (count 105) exit", red.returncode, red.stdout.strip().splitlines()[-1])
replace_once(SIM / "README.md", "105 of 286 registered items accepted.", "106 of 286 registered items accepted.")
replace_once(SIM / "README.md", "| 5 | Operator Cockpit | 23 | 34 |", "| 5 | Operator Cockpit | 22 | 34 |")
red2 = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/docs/"], cwd=SIM,
                      capture_output=True, text=True)
print("red control (tier 5 done 22) exit", red2.returncode, red2.stdout.strip().splitlines()[-1])
sh("git", "worktree", "remove", "--force", str(SIM), cwd=REPO)

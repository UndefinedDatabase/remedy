"""Build F025 R11's closure payloads in a simulated tree at 21aa3097: book R10, rotate, closure edits."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/decodeux/Repos/remedy")
SRC = REPO / ".remedy-wt/f025-r11"
SIM = REPO / ".remedy-wt/f025-r11-sim"
BASE = "21aa3097e"
STATUS_LINE = ("- [x] F025 — Pause/resume (global & per node) (T001–T003 complete, R-1055 carried to F285; "
               "accepted 2026-09-25 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f025r10e1001 · "
               "package remedy-review-20260925-174026-READY_FOR_REVIEW.zip · SHA-256 "
               "5202e21aed884f7ae6a8b79a852d2c4683436f2220d1a910d072cec01ac38e6f · package path "
               "/home/decodeux/Repos/remedy-history/zips · accepted HEAD f7b127bde0e2d705f0a8da49b1d9404d983048d4)")


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
replace_once(SIM / "docs/roadmap/STATUS.md", "- [~] F025 — Pause/resume (global & per node)\n", STATUS_LINE + "\n")
replace_once(SIM / "README.md", "102 of 285 registered items accepted.", "103 of 285 registered items accepted.")
replace_once(SIM / "README.md", "| 5 | Operator Cockpit | 20 | 34 |", "| 5 | Operator Cockpit | 21 | 34 |")
para = (SRC / "readme_para.txt").read_text(encoding="utf-8")
replace_once(SIM / "README.md", "\nFull per-feature state: [`docs/roadmap/STATUS.md`]",
             "\n" + para + "\nFull per-feature state: [`docs/roadmap/STATUS.md`]")
q = SIM / "scripts/self_use_queue.json"
qt = q.read_text(encoding="utf-8")
i = qt.index('"id": "SU-030"')
j = qt.index('"consumed_by": ""', i)
assert qt.count('"consumed_by": ""') == 1, qt.count('"consumed_by": ""')
q.write_text(qt[:j] + '"consumed_by": "F025"' + qt[j + len('"consumed_by": ""'):], encoding="utf-8")
assert json.loads(q.read_text())["items"][-1]["consumed_by"] == "F025"
diff = sh("git", "diff", "HEAD")
(SRC / "closure.diff").write_text(diff, encoding="utf-8")
print("closure.diff numstat", sh("git", "diff", "--numstat", "HEAD").split())
for p in ("docs/roadmap/STATUS.md", "README.md", "scripts/self_use_queue.json"):
    print("C4", p, *sha(SIM / p))
print("status line count", (SIM / "docs/roadmap/STATUS.md").read_text().splitlines().count(STATUS_LINE))
sel = ["tests/docs/", "tests/cli/test_advertised_commands.py", "tests/orchestration/test_live_review_rotation.py",
       "tests/orchestration/test_integrity_gate.py", "tests/orchestration/test_self_use_generator.py"]
run = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *sel], cwd=SIM,
                     capture_output=True, text=True)
print("selection exit", run.returncode, run.stdout.strip().splitlines()[-1])
# red control: the accepted count left at 102
replace_once(SIM / "README.md", "103 of 285 registered items accepted.", "102 of 285 registered items accepted.")
red = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/docs/"], cwd=SIM,
                     capture_output=True, text=True)
print("red control (count 102) exit", red.returncode, red.stdout.strip().splitlines()[-1])
sh("git", "worktree", "remove", "--force", str(SIM), cwd=REPO)

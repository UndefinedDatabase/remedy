"""Build F289 R7's closure payloads in a simulated tree at 439162d5: book R6, rotate, closure edits.
Adapted from `.agent/authored/f027-r14-build.py`. F289 consumed the self-use item SU-033, so the
closure edits also set its `consumed_by` in `scripts/self_use_queue.json`."""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/decodeux/Repos/remedy")
SRC = REPO / ".remedy-wt/f289-r7"
SIM = REPO / ".remedy-wt/f289-r7-sim"
BASE = "439162d5e"
STATUS_LINE = ("- [x] F289 — Self-use sources completion (doc staleness and doctor warnings) (T001–T003 complete; "
               "accepted 2026-09-26 · live review PASS — ACCEPTED · Evidence job f289r6e1001 · "
               "package remedy-review-20260926-225640-READY_FOR_REVIEW.zip · SHA-256 "
               "7044a4959459a9144a0b3030453ed74944ab4edad8125fd67c2eb2e6cc488a62 · package path "
               "/home/decodeux/Repos/remedy-history/zips · accepted HEAD 32013a054ea65dce679cc65fe2cd01fe8d73a76d)")


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
replace_once(SIM / "docs/roadmap/STATUS.md",
             "- [~] F289 — Self-use sources completion (doc staleness and doctor warnings)\n", STATUS_LINE + "\n")
replace_once(SIM / "README.md", "106 of 289 registered items accepted.", "107 of 289 registered items accepted.")
replace_once(SIM / "README.md", "| 5 | Operator Cockpit | 23 | 36 |", "| 5 | Operator Cockpit | 24 | 36 |")
para = (SRC / "readme_para.txt").read_text(encoding="utf-8")
replace_once(SIM / "README.md", "\nFull per-feature state: [`docs/roadmap/STATUS.md`]",
             "\n" + para + "\nFull per-feature state: [`docs/roadmap/STATUS.md`]")
replace_once(SIM / "scripts/self_use_queue.json", '"consumed_by": "",', '"consumed_by": "F289",')
diff = sh("git", "diff", "HEAD")
(SRC / "closure.diff").write_text(diff, encoding="utf-8")
print("closure.diff numstat", sh("git", "diff", "--numstat", "HEAD").split())
for p in ("docs/roadmap/STATUS.md", "README.md", "scripts/self_use_queue.json"):
    print("C4", p, *sha(SIM / p))
print("status line count", (SIM / "docs/roadmap/STATUS.md").read_text().splitlines().count(STATUS_LINE))
q = subprocess.run([sys.executable, "-c",
                    "from packages.orchestration.self_use_queue import load_self_use_queue, pending_self_use_items;"
                    "q = load_self_use_queue(); print([e.consumed_by for e in q if e.id == 'SU-033'],"
                    " len(pending_self_use_items()))"], cwd=SIM, capture_output=True, text=True)
print("queue", q.stdout.strip(), q.stderr.strip()[-200:])
sel = ["tests/docs/", "tests/cli/test_advertised_commands.py", "tests/orchestration/test_live_review_rotation.py",
       "tests/orchestration/test_integrity_gate.py", "tests/orchestration/test_self_use_generator.py",
       "tests/orchestration/test_self_use_queue.py"]
run = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *sel], cwd=SIM,
                     capture_output=True, text=True)
print("selection exit", run.returncode, run.stdout.strip().splitlines()[-1])
integ = subprocess.run([sys.executable, "-m", "apps.cli.main", "integrity", "check", "--json"], cwd=SIM,
                       capture_output=True, text=True)
print("integrity", integ.returncode, integ.stdout.strip()[-120:])
# red control: the accepted count left at 106
replace_once(SIM / "README.md", "107 of 289 registered items accepted.", "106 of 289 registered items accepted.")
red = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/docs/"], cwd=SIM,
                     capture_output=True, text=True)
print("red control (count 106) exit", red.returncode, red.stdout.strip().splitlines()[-1])
replace_once(SIM / "README.md", "106 of 289 registered items accepted.", "107 of 289 registered items accepted.")
replace_once(SIM / "README.md", "| 5 | Operator Cockpit | 24 | 36 |", "| 5 | Operator Cockpit | 23 | 36 |")
red2 = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/docs/"], cwd=SIM,
                      capture_output=True, text=True)
print("red control (tier 5 done 23) exit", red2.returncode, red2.stdout.strip().splitlines()[-1])
sh("git", "worktree", "remove", "--force", str(SIM), cwd=REPO)

"""Build F028 R12's closure payloads in a simulated tree at 41e4b9fd: book R11, rotate, closure edits.
Adapted from `.agent/authored/f288-r10-build.py`. F028 consumed no self-use item (the queue was
exhausted, `self-use NONE (queue exhausted)`), so the closure edits touch no queue entry."""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/decodeux/Repos/remedy")
SRC = REPO / ".remedy-wt/f028-r12"
SIM = REPO / ".remedy-wt/f028-r10-sim"
BASE = "41e4b9fdc"
STATUS_LINE = ("- [x] F028 — Task injection (T001–T003 complete; accepted 2026-09-27 · live review PASS — "
               "ACCEPTED · Evidence job f028r11e1001 · package remedy-review-20260927-132129-READY_FOR_REVIEW.zip · "
               "SHA-256 904723bf332d1f076cdfde262f84609fada02ca86635f3ef09a88c3d025692fe · package path "
               "/home/decodeux/Repos/remedy-history/zips · accepted HEAD 9cfd84d1217c24057173f4b9a8db03734c174c09)")


def sh(*a, cwd=SIM, check=True):
    return subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, check=check).stdout


def sha(p):
    b = Path(p).read_bytes()
    return len(b), hashlib.sha256(b).hexdigest()


def replace_once(path, old, new):
    t = path.read_text(encoding="utf-8")
    assert t.count(old) == 1, (path, old)
    path.write_text(t.replace(old, new), encoding="utf-8")


def commit(msg):
    sh("git", "add", "-A")
    sh("git", "-c", "user.name=sim", "-c", "user.email=sim@example.com", "commit", "-q", "-m", msg)


sh("git", "checkout", "-q", "--detach", BASE)
sh("git", "reset", "--hard", BASE)
sh("git", "clean", "-fdq")
(SRC / "status_line.txt").write_text(STATUS_LINE + "\n", encoding="utf-8")

# C2 — the booking
lr = SIM / ".agent/live_review.md"
assert lr.read_bytes().endswith(b"\n") and not lr.read_bytes().endswith(b"\n\n")
lr.write_bytes(lr.read_bytes() + (SRC / "ledger.md").read_bytes())
shutil.copyfile(SRC / "plan.md", SIM / ".agent/plan.md")
commit("sim C2")
print("C2 numstat", sh("git", "show", "--numstat", "--format=", "HEAD").split())
for p in (".agent/live_review.md", ".agent/plan.md"):
    print("C2", p, *sha(SIM / p))
sys.path.insert(0, str(SIM / "scripts"))
from rotate_live_review import open_finding_ids  # noqa: E402

print("open at C2", sorted(open_finding_ids(lr.read_text(encoding="utf-8"))))

# C3 — the rotation
rot = subprocess.run([sys.executable, "scripts/rotate_live_review.py"], cwd=SIM, capture_output=True, text=True)
print("ROTATION exit", rot.returncode)
print(rot.stdout.strip(), rot.stderr.strip()[-300:])
commit("sim C3")
print("C3 numstat", sh("git", "show", "--numstat", "--format=", "HEAD").split())
for p in (".agent/live_review.md", ".agent/live_review_archive.md"):
    print("C3", p, *sha(SIM / p))

# C4 — the closure edits
replace_once(SIM / "docs/roadmap/STATUS.md", "- [~] F028 — Task injection\n", STATUS_LINE + "\n")
replace_once(SIM / "README.md", "108 of 289 registered items accepted.", "109 of 289 registered items accepted.")
replace_once(SIM / "README.md", "| 5 | Operator Cockpit | 25 | 36 |", "| 5 | Operator Cockpit | 26 | 36 |")
para = (SRC / "readme_para.txt").read_text(encoding="utf-8")
replace_once(SIM / "README.md", "\nFull per-feature state: [`docs/roadmap/STATUS.md`]",
             "\n" + para + "\nFull per-feature state: [`docs/roadmap/STATUS.md`]")
(SRC / "closure.diff").write_text(sh("git", "diff", "HEAD"), encoding="utf-8")
print("closure.diff numstat", sh("git", "diff", "--numstat", "HEAD").split())
for p in ("docs/roadmap/STATUS.md", "README.md"):
    print("C4", p, *sha(SIM / p))
print("status line count", (SIM / "docs/roadmap/STATUS.md").read_text(encoding="utf-8").splitlines().count(STATUS_LINE))
q = subprocess.run([sys.executable, "-c",
                    "from packages.orchestration.self_use_queue import pending_self_use_items;"
                    "print(len(pending_self_use_items()))"], cwd=SIM, capture_output=True, text=True)
print("pending self-use items", q.stdout.strip(), q.stderr.strip()[-200:])
sel = ["tests/docs/", "tests/cli/test_advertised_commands.py", "tests/orchestration/test_live_review_rotation.py",
       "tests/orchestration/test_integrity_gate.py", "tests/orchestration/test_self_use_generator.py",
       "tests/orchestration/test_self_use_queue.py", "tests/cli/test_golden_path.py"]
run = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *sel], cwd=SIM,
                     capture_output=True, text=True)
print("selection exit", run.returncode, run.stdout.strip().splitlines()[-1])
integ = subprocess.run([sys.executable, "-m", "apps.cli.main", "integrity", "check", "--json"], cwd=SIM,
                       capture_output=True, text=True)
print("integrity", integ.returncode, integ.stdout.strip()[-160:])
# red control: the accepted count left at 108
replace_once(SIM / "README.md", "109 of 289 registered items accepted.", "108 of 289 registered items accepted.")
red = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/docs/"], cwd=SIM,
                     capture_output=True, text=True)
print("red control (count 108) exit", red.returncode, red.stdout.strip().splitlines()[-1])
replace_once(SIM / "README.md", "108 of 289 registered items accepted.", "109 of 289 registered items accepted.")
replace_once(SIM / "README.md", "| 5 | Operator Cockpit | 26 | 36 |", "| 5 | Operator Cockpit | 25 | 36 |")
red2 = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/docs/"], cwd=SIM,
                      capture_output=True, text=True)
print("red control (tier 5 done 25) exit", red2.returncode, red2.stdout.strip().splitlines()[-1])
replace_once(SIM / "README.md", "| 5 | Operator Cockpit | 25 | 36 |", "| 5 | Operator Cockpit | 26 | 36 |")
print("restored README", *sha(SIM / "README.md"))

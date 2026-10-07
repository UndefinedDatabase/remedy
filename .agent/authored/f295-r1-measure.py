"""F295 round 1 reviewer measurement: what the machine-client path answers today.

Usage: python3 measure.py <primary checkout>
Runs every probe against a scratch repository and a scratch data root under this
script's own folder; never touches the operator's data root.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PRIMARY = Path(sys.argv[1]).resolve()
HERE = Path(__file__).resolve().parent
PROBE = HERE / "probe"
DATA = HERE / "data"
for p in (PROBE, DATA):
    if p.exists():
        shutil.rmtree(p)
PROBE.mkdir()
DATA.mkdir()

env = dict(os.environ)
env["REMEDY_DATA_DIR"] = str(DATA)
env["PYTHONPATH"] = str(PRIMARY)
env.pop("REMEDY_SERVE_SOCKET", None)


def git(*args):
    subprocess.run(["git", "-C", str(PROBE), *args], check=True, capture_output=True)


(PROBE / "README.md").write_text("# probe\n")
(PROBE / "hello.py").write_text("def hello():\n    return 'hi'\n")
git("init", "-q", "-b", "main")
git("-c", "user.name=p", "-c", "user.email=p@p", "add", "-A")
git("-c", "user.name=p", "-c", "user.email=p@p", "commit", "-q", "-m", "init")
(PROBE / "order.md").write_text("Add a docstring to hello in hello.py.\n")


def remedy(*args, stdin=subprocess.DEVNULL, timeout=180):
    cmd = [sys.executable, "-m", "apps.cli.main", *args]
    try:
        r = subprocess.run(cmd, cwd=str(PROBE), env=env, stdin=stdin,
                           capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired as exc:
        return "TIMEOUT", exc.stdout or "", exc.stderr or ""


def show(title, res, keys_only=False):
    code, out, err = res
    print(f"=== {title}: exit {code}")
    try:
        doc = json.loads(out)
        if keys_only:
            print("keys:", sorted(doc.keys()))
        else:
            print(json.dumps(doc, indent=1)[:3000])
        return doc
    except Exception:
        print("stdout:", out[-1500:])
        print("stderr:", err[-1500:])
        return None


d1 = show("do order.md --plan-only --no-llm --json --no-ui --yes",
          remedy("do", "order.md", "--plan-only", "--no-llm", "--json", "--no-ui", "--yes"))
if d1:
    jobs = d1.get("jobs") or []
    for j in jobs:
        print("job", j.get("job_id"), "tasks:", [t.get("title") for t in j.get("tasks", [])])
show("do missing.md --plan-only --no-llm --json --no-ui --yes",
     remedy("do", "missing.md", "--plan-only", "--no-llm", "--json", "--no-ui", "--yes"))
st = show("status --json", remedy("status", "--json"))
if d1 and d1.get("job_ids"):
    jid = d1["job_ids"][0]
    show("decision list --json", remedy("decision", "list", jid, "--json"))
# a full run with fake providers, stdin a pipe nobody writes to
r, w = os.pipe()
res = remedy("do", "Add a docstring to hello in hello.py.", "--json", "--no-ui", "--yes",
             "--no-llm", "--builder-provider", "fake", "--reviewer-provider", "fake",
             "--max-cost-usd", "1", stdin=r, timeout=300)
os.close(w)
os.close(r)
d2 = show("do <text> --json --no-ui --yes --no-llm fake/fake, stdin open pipe", res, keys_only=True)
if d2:
    print("stopped_before_apply:", d2.get("stopped_before_apply"), "steps:",
          [(s.get("name"), s.get("status")) for s in d2.get("steps", [])])
    print("cost:", json.dumps(d2.get("cost"))[:600])
show("status --json after run", remedy("status", "--json"))

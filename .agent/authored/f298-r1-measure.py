"""F298 round 1 — the claim's measurement: repeat each "Measured" sentence of T12_F298.md.

Usage: python3 -B measure.py <primary checkout> <scratch folder>
Every probe runs with the fake providers against scratch repositories and a scratch data root
inside <scratch folder>, which is deleted and re-made first. The one reading of a real data root
is `remedy status --json` against the default root, which only reads.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PRIMARY = Path(sys.argv[1]).resolve()
S = Path(sys.argv[2]).resolve()
if S.exists():
    shutil.rmtree(S)
S.mkdir(parents=True)
DATA = S / "data"
IDENT = {"GIT_AUTHOR_NAME": "p", "GIT_AUTHOR_EMAIL": "p@p", "GIT_COMMITTER_NAME": "p",
         "GIT_COMMITTER_EMAIL": "p@p"}
ENV = {**os.environ, **IDENT, "REMEDY_DATA_DIR": str(DATA), "PYTHONPATH": str(PRIMARY)}
ENV.pop("REMEDY_SERVE_SOCKET", None)
FAKE = ["--no-ui", "--yes", "--no-llm", "--builder-provider", "fake", "--reviewer-provider", "fake"]


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def git(cwd, *a):
    return subprocess.run(["git", "-C", str(cwd), *a], env=ENV, capture_output=True, text=True)


def repo(name, upstream=False):
    r = S / name
    r.mkdir()
    git(r, "init", "-q", "-b", "main")
    (r / "README.md").write_text(f"# {name}\n", encoding="utf-8")
    git(r, "add", "README.md")
    git(r, "commit", "-q", "-m", "init")
    if upstream:
        bare = S / f"{name}-upstream.git"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(bare)], env=ENV, check=True)
        git(r, "remote", "add", "origin", str(bare))
        git(r, "push", "-q", "-u", "origin", "main")
    return r


def remedy(cwd, *args, env=None, timeout=600):
    r = subprocess.run([sys.executable, "-B", "-m", "apps.cli.main", *args], cwd=str(cwd),
                       env=env or ENV, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                       timeout=timeout)
    try:
        body = json.loads(r.stdout)
    except ValueError:
        body = {"_stdout": r.stdout[-600:], "_stderr": r.stderr[-600:]}
    return r.returncode, body


def steps(body):
    return [(s.get("name"), s.get("status"), (s.get("detail") or "")[:150]) for s in body.get("steps", [])]


def job_record(job_id):
    return json.loads((DATA / "jobs" / job_id / "job.json").read_text(encoding="utf-8"))


def digest():
    code, body = remedy(S, "status", "--json")
    return body.get("client") or {}


order = S / "order.md"
order.write_text("---\nmax-cost-usd: 1\n---\nAdd a line saying hello to README.md\n", encoding="utf-8")
order_b = S / "order-b.md"
order_b.write_text("---\nproject: b\nmax-cost-usd: 1\n---\nAdd a line saying hello to README.md\n",
                   encoding="utf-8")
plain = S / "plain"
plain.mkdir()
A = repo("a", upstream=True)
B = repo("b")

say("## M1 an order runs where the client stands")
# The scratch folder sits inside the primary checkout, so without a ceiling git would find the
# checkout above `plain` and the probe would run a job against it (first attempt, 2026-10-07).
NO_CLIMB = {**ENV, "GIT_CEILING_DIRECTORIES": str(S)}
code, body = remedy(plain, "do", str(order), *FAKE, "--json", env=NO_CLIMB)
say("M1a in a folder that is no repository: exit", code, "error", body.get("error"), "steps", steps(body))
code, body = remedy(B, "do", str(order), "--plan-only", "--no-llm", "--no-ui", "--yes", "--json")
say("M1b register b by a plan-only order in b: exit", code, "steps", steps(body)[:1])
code, body = remedy(A, "do", str(order_b), *FAKE, "--json")
say("M1c in repository a, header project: b: exit", code, "error", body.get("error"))
say("    init:", steps(body)[:1])
jid = (body.get("job_ids") or [""])[0]
rec = job_record(jid) if jid else {}
say("    job", jid, "repo_path", rec.get("repo_path"), "project_id", rec.get("project_id"))
say("    next:", body.get("next"))
say("    git status of a:", git(A, "status", "--porcelain").stdout.split("\n"))
say("    git status of b:", git(B, "status", "--porcelain").stdout.split("\n"))

say("## M2 a blocked apply under --approve --json")
code, body = remedy(A, "do", str(order), *FAKE, "--json")
say("M2a full fake run in a: exit", code, "error", body.get("error"), "steps", [s[:2] for s in steps(body)])
say("    unmet_blocking_criteria", json.dumps(body.get("unmet_blocking_criteria"))[:400])
job2 = (body.get("job_ids") or [""])[0]
mission2 = body.get("mission_id")
head_before = git(A, "rev-parse", "HEAD").stdout.strip()
up_before = git(S / "a-upstream.git", "rev-parse", "main").stdout.strip()
code, body = remedy(A, "job", "apply", job2, "--approve", "--commit-with-history", "--push", "--json")
say("M2b job apply --approve --commit-with-history --push --json: exit", code, "ok", body.get("ok"),
    "status", body.get("status"), "error", body.get("error"))
say("    blocked_reason", str(body.get("blocked_reason"))[:300])
say("    keys", sorted(body))
say("    a HEAD moved:", git(A, "rev-parse", "HEAD").stdout.strip() != head_before,
    "| upstream moved:", git(S / "a-upstream.git", "rev-parse", "main").stdout.strip() != up_before,
    "| a status:", git(A, "status", "--porcelain").stdout.split("\n"))

say("## M8 what the records say about the completed job")
rec2 = job_record(job2)
review = sorted((DATA / "jobs" / job2).rglob("final_job_review.json"))
for p in review[:1]:
    fr = json.loads(p.read_text(encoding="utf-8"))
    crit = fr.get("acceptance_criteria") or fr.get("criteria") or []
    say("M8a final_job_review.json verdict", fr.get("verdict") or fr.get("overall_verdict"),
        "| criteria", len(crit), "| keys", sorted(fr)[:30])
say("M8b job record test_passed", rec2.get("test_passed"), "| test_command", repr(rec2.get("test_command")),
    "| total_tokens", rec2.get("total_tokens"))
say("M8c job record keys naming tokens or calls:",
    sorted(k for k in rec2 if "token" in k or "call" in k or "cache" in k))
d = digest()
j = [x for x in d.get("jobs", []) if x["job_id"] == job2]
say("M8d digest job keys", sorted(j[0]) if j else None, "| cost", j[0].get("cost") if j else None)
say("M8e digest project keys", sorted(d["projects"][0]) if d.get("projects") else None)
say("M8f digest decision keys", sorted(d["decisions"][0]) if d.get("decisions") else "(no open decision)")
say("M8g digest top-level keys", sorted(d))

say("## M4 no command declines; an abandoned mission's job still waits")
say("M4a commands named decline or reject on job:",
    [ln.strip() for ln in (PRIMARY / "apps/cli/command_catalog.py").read_text().splitlines()
     if 'subcommand="decline"' in ln or 'subcommand="reject"' in ln])
code, body = remedy(A, "mission", "abandon", mission2, "--json")
say("M4b mission abandon: exit", code, "ok", body.get("ok"))
d = digest()
j = [x for x in d.get("jobs", []) if x["job_id"] == job2]
say("M4c after abandon: waits_for_apply", j[0]["waits_for_apply"] if j else None,
    "| in awaiting_apply", job2 in d.get("awaiting_apply", []))

say("## M5 an order of two jobs")
code, body = remedy(A, "do", str(order), *FAKE, "--force-mission", "--json")
say("M5 --force-mission: exit", code, "error", body.get("error"), "job_ids", body.get("job_ids"),
    "waiting_job_ids", body.get("waiting_job_ids"))
say("    next:", body.get("next"))

say("## M6 the same order file twice")
c1, b1 = remedy(A, "do", str(order), "--plan-only", "--no-llm", "--no-ui", "--yes", "--json")
c2, b2 = remedy(A, "do", str(order), "--plan-only", "--no-llm", "--no-ui", "--yes", "--json")
say("M6 two plan-only starts of one file: exits", c1, c2, "missions", b1.get("mission_id"), b2.get("mission_id"),
    "| distinct:", b1.get("mission_id") != b2.get("mission_id"))

say("## M9 templates and what registering leaves in the repository")
t = subprocess.run([sys.executable, "-B", "-c", "from packages.orchestration.contract_templates import "
                    "list_contract_templates as l; print(l())"], cwd=PRIMARY, env=ENV,
                   capture_output=True, text=True)
say("M9a contract templates", t.stdout.strip())
o2 =S / "order-tpl.md"
o2.write_text("---\ncontract: small-change\nmax-cost-usd: 1\n---\nAdd a line to README.md\n", encoding="utf-8")
code, body = remedy(A, "do", str(o2), *FAKE, "--json")
say("M9b an order naming another template: exit", code, "error", body.get("error"))
C = repo("c")
code, body = remedy(C, "init", "--json")
say("M9c remedy init in a clean repository: exit", code, "| git status:",
    git(C, "status", "--porcelain", "--untracked-files=all").stdout.split("\n"))

say("## M10 caps and tokens")
say("M10a order header keys",
    subprocess.run([sys.executable, "-B", "-c", "from packages.orchestration.order_file import "
                    "ORDER_FILE_HEADER_KEYS as k; print(k)"], cwd=PRIMARY, env=ENV,
                   capture_output=True, text=True).stdout.strip())

say("## M7 the digest's size")
d = digest()
say("M7a scratch root: jobs", len(d.get("jobs", [])), "| awaiting_apply", len(d.get("awaiting_apply", [])),
    "| client bytes", len(json.dumps(d)))
src = DATA / "jobs" / job2 / "job.json"
text = src.read_text(encoding="utf-8")
for n in range(1000):
    new_id = f"{n:016x}"
    (DATA / "jobs" / new_id).mkdir()
    (DATA / "jobs" / new_id / "job.json").write_text(text.replace(job2, new_id), encoding="utf-8")
d = digest()
say("M7b with 1,000 copies of the completed job added: jobs", len(d.get("jobs", [])),
    "| awaiting_apply", len(d.get("awaiting_apply", [])), "| client bytes", len(json.dumps(d)),
    "| degraded", d.get("degraded"))
real = {k: v for k, v in os.environ.items() if k != "REMEDY_SERVE_SOCKET"}
real["PYTHONPATH"] = str(PRIMARY)
code, body = remedy(PRIMARY, "status", "--json", env=real)
c = body.get("client") or {}
states = {}
for x in c.get("jobs", []):
    states[x["state"]] = states.get(x["state"], 0) + 1
say("M7c the operator's own data root: exit", code, "| jobs", len(c.get("jobs", [])),
    "| awaiting_apply", len(c.get("awaiting_apply", [])), "| open decisions", len(c.get("decisions", [])),
    "| client bytes", len(json.dumps(c)), "| states", dict(sorted(states.items())))

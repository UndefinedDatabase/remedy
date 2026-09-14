# F275 R63 — the residue diagnosis instrument, saved verbatim as an authored blob

Its extension is `.md` and that is load-bearing: a `.py` file anywhere `ruff check .` scans
is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this round gates on.

```python
"""F275 R63 — the residue diagnosis instrument. Re-derives every figure the artefact states.

Four readings, printed under four banners. (1) THE CLASSES: the three largest residue
classes of the round 61 flipped run, attributed to the source frame `--tb=line` prints for
each and to the `Error:` text the handler captured. (2) THE MECHANISM: the same three
failures reproduced by CALLING the shipped functions, each beside a control that succeeds.
(3) THE SEAM: an `ast` count of the sites that bind a `UUID` and pass it on. (4) THE
CANDIDATE RULE: the three scoped `tests/cli/` runs, read out of their own logs.

Reads only; creates nothing and writes nothing. The four log files it reads are the
reviewer's own dry-run output under the gitignored `.remedy-wt/`.
"""
import ast
import collections
import pathlib
import re
import subprocess
import sys
import uuid

REPO = pathlib.Path("/home/decodeux/Repos/remedy")
SCR = REPO / ".remedy-wt"
WT61 = str(SCR / "wt_r61") + "/"
ELINE = re.compile(r"^E\s+([A-Za-z_.]*(?:Error|Exception|Warning|Exit)[A-Za-z_.]*):\s*(.*)$")
FRAME = re.compile(r"^(/[^:]+):(\d+): ([A-Za-z_.]*(?:Error|Exception|Warning|Exit)[A-Za-z_.]*):")
STDERR = re.compile(r"^Error: (.*)$")
CLASSES = {
    "SystemExit": lambda e, m: e == "SystemExit",
    "hexadecimal UUID": lambda e, m: "badly formed hexadecimal UUID" in m,
    "unsupported operand /": lambda e, m: e == "TypeError"
    and "unsupported operand type(s) for /" in m,
}

print("=== 1. THE CLASSES, attributed ===")
lines = (SCR / "r61_flipped.log").read_text(encoding="utf-8", errors="replace").split("\n")
recs = []
for i, raw in enumerate(lines):
    m = ELINE.match(raw)
    if not m:
        continue
    frame = err = None
    for j in range(i + 1, min(i + 40, len(lines))):
        s = STDERR.match(lines[j])
        if s and err is None:
            err = s.group(1)
        f = FRAME.match(lines[j])
        if f:
            if f.group(3) == m.group(1):
                frame = (f.group(1), int(f.group(2)))
            break
    recs.append((m.group(1), m.group(2), frame, err))
print(f"E-lines paired: {len(recs)}")
for label, pred in CLASSES.items():
    sel = [r for r in recs if pred(r[0], r[1])]
    fr = collections.Counter(r[2] or ("<no frame>", 0) for r in sel)
    print(f"  {label:<24} E-lines {len(sel):>4}")
    for top, topn in fr.most_common(2):
        path = top[0][len(WT61):] if top[0].startswith(WT61) else top[0]
        print(f"      frame  {topn:>4}  {path}:{top[1]}")
    sh = collections.Counter()
    print(f"      with a captured `Error:` line: {sum(1 for r in sel if r[3])}")
    for r in sel:
        if not r[3]:
            continue
        head = re.sub(r"'[^']*'", "'X'", r[3])
        for tok in re.findall(r"'([^']*)'", r[3]):
            head += "  [arg=16hex]" if re.fullmatch(r"[0-9a-f]{16}", tok) else (
                "  [arg=8hex]" if re.fullmatch(r"[0-9a-f]{8}", tok) else "  [arg=other]")
        sh[head] += 1
    for head, n in sh.most_common(4):
        print(f"      stderr {n:>4}  {head}")

print("\n=== 2. THE MECHANISM, reproduced by calling the shipped functions ===")
sys.path.insert(0, str(REPO))
from packages.orchestration.data_paths import job_dir, mint_job_id  # noqa: E402
from packages.orchestration.pingpong_job import JobPlan, load_job_plan  # noqa: E402

ROOT = pathlib.Path("/nonexistent-probe-root")
minted = mint_job_id()
print(f"mint_job_id() len {len(minted)} hyphens {minted.count('-')} | "
      f"str(uuid4()) len {len(str(uuid.uuid4()))} hyphens 4")
try:
    uuid.UUID(minted)
    print("  UUID(mint_job_id()) SUCCEEDED — class does not reproduce")
except ValueError as exc:
    print(f"  UUID(mint_job_id()) -> ValueError: {exc}")
for label, call in (("job_dir", lambda: job_dir(uuid.uuid4(), ROOT)),
                    ("load_job_plan", lambda: load_job_plan(uuid.uuid4(), ROOT))):
    try:
        call()
        print(f"  {label}(UUID) SUCCEEDED — class does not reproduce")
    except TypeError as exc:
        print(f"  {label}(UUID, root) -> TypeError: {exc}")
print(f"  JobPlan(job_id=uuid4()).job_id is a {type(JobPlan(job_id=uuid.uuid4()).job_id).__name__}"
      " — the dataclass does not coerce")
print(f"  CONTROL job_dir(minted, root) -> {job_dir(minted, ROOT)}")
print(f"  CONTROL load_job_plan(minted, root) -> {load_job_plan(minted, ROOT)!r}")

print("\n=== 2b. THE RESOLVER, run against a store holding BOTH shapes ===")
import os  # noqa: E402
import shutil  # noqa: E402

STORE = SCR / "r63_store"
if STORE.exists():
    shutil.rmtree(STORE)
(STORE / "jobs").mkdir(parents=True)
os.environ["REMEDY_DATA_DIR"] = str(STORE)
from packages.orchestration.data_paths import (  # noqa: E402
    _classic_job_id_matches, _task_job_id_matches, resolve_job_id,
)

_classic, _unified = str(uuid.uuid4()), mint_job_id()
(STORE / "jobs" / f"{_classic}.json").write_text("{}")
(STORE / "jobs" / _unified).mkdir()
(STORE / "jobs" / _unified / "job.json").write_text("{}")
for _label, _jid, _pre in (("classic 8-hex prefix", _classic, _classic[:8]),
                           ("unified 8-hex prefix", _unified, _unified[:8]),
                           ("unified WHOLE id", _unified, _unified)):
    _c = "finds it" if _classic_job_id_matches(_pre) else "[]"
    _t = "finds it" if _task_job_id_matches(_pre) else "[]"
    try:
        _r = "returns the canonical id" if resolve_job_id(_pre) else "?"
    except SystemExit as _exc:
        _r = f"SystemExit: {_exc.code}"
    print(f"  {_label:<22} classic {_c:<9} task {_t:<9} resolve_job_id -> {_r}")
shutil.rmtree(STORE)
os.environ.pop("REMEDY_DATA_DIR", None)
print("  the synthetic store was removed")

print("\n=== 3. THE SEAM, counted by ast ===")
files = [REPO / p for p in subprocess.run(
    ["git", "-C", str(REPO), "ls-files", "apps", "packages"],
    capture_output=True, text=True, check=True).stdout.split("\n") if p.endswith(".py")]


def is_uuid(node):
    f = node.func
    return (isinstance(f, ast.Name) and f.id == "UUID") or (
        isinstance(f, ast.Attribute) and f.attr == "UUID")


calls, passed = 0, []
for path in files:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        continue
    rel = str(path.relative_to(REPO))
    calls += sum(1 for n in ast.walk(tree) if isinstance(n, ast.Call) and is_uuid(n))
    for scope in ast.walk(tree):
        if not isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        bound = {n.targets[0].id for n in ast.walk(scope)
                 if isinstance(n, ast.Assign) and len(n.targets) == 1
                 and isinstance(n.targets[0], ast.Name)
                 and isinstance(n.value, ast.Call) and is_uuid(n.value)}
        if not bound:
            continue
        for n in ast.walk(scope):
            if not isinstance(n, ast.Call):
                continue
            callee = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
            if callee in ("UUID", None):
                continue
            for a in list(n.args) + [k.value for k in n.keywords]:
                if isinstance(a, ast.Name) and a.id in bound:
                    passed.append((rel, scope.name, callee))
print(f"tracked .py under apps/ and packages/: {len(files)}")
print(f"every `UUID(...)` call: {calls}")
print(f"sites that BIND a UUID and pass it on: {len(passed)} "
      f"over {len({(r[0], r[1]) for r in passed})} scopes in {len({r[0] for r in passed})} files")
print(f"  under apps/cli/: {sum(1 for r in passed if r[0].startswith('apps/cli/'))}"
      f"   outside it: {sum(1 for r in passed if not r[0].startswith('apps/cli/'))}")
for callee, n in collections.Counter(r[2] for r in passed).most_common(4):
    print(f"  callee {n:>4}  {callee}")
rest = [r for r in passed if not r[0].startswith("apps/cli/")]
print("  the sites OUTSIDE apps/cli/, which a handler-scoped rule never reaches:")
for rel, n in collections.Counter(r[0] for r in rest).most_common(6):
    print(f"    {n:>4}  {rel}")
for callee, n in collections.Counter(r[2] for r in rest).most_common(6):
    print(f"    callee {n:>4}  {callee}")

print("\n=== 4. THE CANDIDATE RULE, read out of the three scoped run logs ===")
for label, log in (("control  ", "r63_cli_control.log"), ("flipped  ", "r63_cli_flipped.log"),
                   ("candidate", "r63_cli_unwrapped.log")):
    text = (SCR / log).read_text(encoding="utf-8", errors="replace")
    tail = [ln.strip() for ln in text.split("\n") if re.search(r"\d+ (passed|failed)", ln)]
    cnt = collections.Counter()
    for ln in text.split("\n"):
        m = ELINE.match(ln)
        if m:
            for lb, pred in CLASSES.items():
                if pred(m.group(1), m.group(2)):
                    cnt[lb] += 1
    ids = {ln[7:].split(" ")[0].strip() for ln in text.split("\n") if ln.startswith("FAILED ")}
    print(f"{label}  {tail[-1] if tail else '?':<42} ids {len(ids):>4}  "
          f"SystemExit {cnt['SystemExit']:>3}  hexUUID {cnt['hexadecimal UUID']:>3}  "
          f"operand {cnt['unsupported operand /']:>3}")


def ids_of(log):
    return {ln[7:].split(" ")[0].strip()
            for ln in (SCR / log).read_text(encoding="utf-8", errors="replace").split("\n")
            if ln.startswith("FAILED ")}


f, u = ids_of("r63_cli_flipped.log"), ids_of("r63_cli_unwrapped.log")
print(f"the candidate rule FIXED {len(f - u)} and BROKE {len(u - f)}; {len(u & f)} survive")
for n in sorted(u - f):
    print(f"  BROKE  {n}")
```

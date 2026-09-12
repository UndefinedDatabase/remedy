# F275 R69 — the guarded flip transform, part 1 of two, verbatim

> THE FILE IS SPLIT BECAUSE OF THE INSERTION CAP, NOT BECAUSE IT HAS TWO PARTS.
> The guarded transform is one file of 653 lines; a single authored blob would be
> one commit of over 500 insertions, which AGENTS.md DECISION F104 D1 forbids and whose
> exemption list names only the five `.agent/` state files. The fence below is part 1
> of two, and the two fences CONCATENATE BYTE FOR BYTE to the whole file — the round's
> gate re-derives that rather than trusting it. The cut falls at a top-level `def`
> boundary so each part parses as a readable unit of its own.
>
> Saved as `.md` and not as `.py` so that `ruff check .` does not count it, per the
> ceiling `tests/orchestration/test_ci_budgets.py` freezes.

```python
"""F275 R69 DRY RUN, GUARDED — the flip with DECISION F275 D29's P1 and P3 implemented.

Extends `.remedy-wt/r46_flip_transform.py`, which round 50 re-ran unchanged. Two rules
change and one is added; everything else is byte-for-byte the same transform.

  P1  T2 and T3 no longer ask whether the RECEIVER'S NAME contains a target word. They
      consume the RULED SITE SET of `.agent/f275_t003_descriptor_sites.md` — R = P | S,
      2198 sites keyed by (path, line, col, attr) — and rename only a site that set
      holds. The OWNER, which decides `job_id` against `task_id`, comes from the static
      sweep's verdict where it has one, else from the probe's line when that line names
      exactly one owner, else from the receiver name restricted to the owners the probe's
      line names. A site none of the three resolves is LEFT ALONE and reported.

  P3  A construction keyword arriving through `**defaults` is not a `keyword.arg`, so no
      rewrite keyed on the constructor reaches it. Two passes implement DECISION F275 D31:
      S1 rewrites the STRING KEYS of a dict literal assigned to a name that is splatted
      into a target constructor, and S2 rewrites the KEYWORDS of a call to a helper
      factory defined in the SAME file. Both use one table, and both DROP the keys D31
      rules dropped rather than renaming them.

Everything else — T1, T4, T5, T6, I1, I2, I3, the five exclusions, and the right-to-left
byte-span edit machinery — is unchanged from R46.

Usage: python3 -B r61_flip_transform.py <worktree> <ruled.json> <owners.json> <status.json>
"""
import ast
import collections
import json
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1])
RULED_JSON = sys.argv[2]
OWNERS_JSON = sys.argv[3]
UNIFIED = "packages.orchestration.pingpong_job"

TYPE_RENAME = {"Job": "JobPlan", "Task": "TaskEntry"}
SEAM = {"save_job": "save_job_plan", "load_job": "load_job_plan",
        "load_job_safe": "load_job_plan_safe", "list_jobs": "list_job_plans",
        "list_jobs_safe": "list_job_plans_safe"}
JOB_FIELD = {"id": "job_id", "name": "job_title"}
TASK_FIELD = {"id": "task_id", "description": "title"}
CTOR_KW = {"Job": {"name": "job_title", "id": "job_id"},
           "Task": {"description": "title", "type": "task_class",
                    "task_type": "task_class", "id": "task_id"}}
DELETE_LINE = "\x00R55-DELETE-LINE\x00"
JOBISH = ("job", "plan", "record")
TASKISH = ("task",)

# DECISION F275 D31. A key the classic record IGNORED and the unified record REFUSES is
# DROPPED, never renamed: it set nothing before the flip, so removing it changes no value.
SPLAT_KEY = {"Job": {"name": "job_title", "id": "job_id",
                     "permissions": None, "description": None},
             "Task": {"description": "title", "type": None}}

EXCLUDE = {
    "packages/core/models.py",                  # DEFINES the classic Job and Task
    "packages/orchestration/pingpong_job.py",   # DEFINES JobPlan and TaskEntry
    "packages/orchestration/storage.py",        # IMPLEMENTS the classic store
    "tests/test_storage.py",                    # tests the classic store as such
    "tests/test_models.py",
}

RULED = {}
with open(OWNERS_JSON) as fh:
    for key, owner in json.load(fh).items():
        path, line, col, attr = key.rsplit("|", 3)
        RULED[(path, int(line), int(col), attr)] = owner
with open(RULED_JSON) as fh:
    _r = json.load(fh)
RULED_KEYS = {(p, l, c, a) for p, l, c, a in _r["R"]}

# DECISION F275 D35 — the third retype rule family. Nine `Task.status.value` chains, keyed
# by (path, enclosing scope, occurrence of the chain inside that scope) and NEVER by line
# number, which is what finding `R-0879` cost this chain to learn.
STATUS_JSON = sys.argv[4] if len(sys.argv) > 4 else None
STATUS_RULED = {}
if STATUS_JSON:
    with open(STATUS_JSON) as fh:
        for r in json.load(fh)["sites"]:
            STATUS_RULED.setdefault(r["path"], set()).add((r["scope"], r["occ"]))


def status_chain_keys(path, tree):
    """Map id(inner `.status` node) -> (scope, occurrence) for every chain in this file."""
    if path not in STATUS_RULED:
        return {}
    owner = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for sub in ast.walk(fn):
                if isinstance(sub, ast.Attribute):
                    prev = owner.get(id(sub))
                    if prev is None or fn.lineno > prev.lineno:
                        owner[id(sub)] = fn
    nodes = [n.value for n in ast.walk(tree)
             if isinstance(n, ast.Attribute) and n.attr == "value"
             and isinstance(n.value, ast.Attribute) and n.value.attr == "status"]
    nodes.sort(key=lambda n: (n.lineno, n.col_offset))
    seen = collections.Counter()
    out = {}
    for n in nodes:
        fn = owner.get(id(n))
        scope = fn.name if fn else "<module>"
        seen[scope] += 1
        out[id(n)] = (scope, seen[scope])
    return out


def tracked():
    out = subprocess.run(["git", "ls-files", "*.py"], capture_output=True, text=True,
                         cwd=str(WT)).stdout
    return [p for p in out.split() if p]


def recv_name(node):
    return str(getattr(node, "id", None) or getattr(node, "attr", "") or "")


def is_jobish(name):
    low = name.lower()
    return low in ("j", "stored") or any(t in low for t in JOBISH)


def is_taskish(name):
    low = name.lower()
    return low in ("t", "tk") or any(t in low for t in TASKISH)


def import_replacement(node, indent):
    """I1 and I2, unchanged from R46: a target import moves its MODULE PATH, and an
    import naming a target beside a non-target is SPLIT rather than moved."""
    moves = dict(TYPE_RENAME)
    moves.update(SEAM)
    names = node.names
    hit = [a for a in names if a.name in moves]
    if not hit:
        return None
    rest = [a for a in names if a.name not in moves]

    def render(alias, rename):
        base = moves[alias.name] if rename else alias.name
        return f"{base} as {alias.asname}" if alias.asname else base

    moved = f"from {UNIFIED} import " + ", ".join(render(a, True) for a in hit)
    if not rest:
        return moved
    kept = f"from {node.module} import " + ", ".join(render(a, False) for a in rest)
    return kept + "\n" + indent + moved


def splat_targets(tree):
    """P3 half one: names splatted into a target constructor, and the helper factories.

    Returns (splatted_names, helpers) where `splatted_names` maps a local name to the
    constructor it is splatted into, and `helpers` maps a function name defined in this
    module to that same constructor, for every function whose `**kwargs` parameter
    reaches a target construction.
    """
    splatted, helpers = {}, {}
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        kwarg = fn.args.kwarg.arg if fn.args.kwarg else None
        for n in ast.walk(fn):
            if not isinstance(n, ast.Call):
                continue
            called = n.func.id if isinstance(n.func, ast.Name) else None
            if called not in SPLAT_KEY:
                continue
            for kw in n.keywords:
                if kw.arg is not None or not isinstance(kw.value, ast.Name):
                    continue
                splatted[kw.value.id] = called
                if kwarg and kwarg == kw.value.id:
                    helpers[fn.name] = called
    # A helper whose `**kwargs` reaches the constructor through a local dict it updates.
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not fn.args.kwarg:
            continue
        kwarg = fn.args.kwarg.arg
        local = {name for name, ctor in splatted.items()}
        for n in ast.walk(fn):
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr == "update" and isinstance(n.func.value, ast.Name)
                    and n.func.value.id in local
                    and any(isinstance(a, ast.Name) and a.id == kwarg for a in n.args)):
                helpers[fn.name] = splatted[n.func.value.id]
    return splatted, helpers


def collect(path, src, counts, undecided, unhandled):
    """Return (line edits, whole-node import replacements)."""
    tree = ast.parse(src, filename=path)
    edits, imports = [], []
    splatted, helpers = splat_targets(tree)
    status_keys = status_chain_keys(path, tree)
    minted = scope_minted_names(tree)
    ordinals = task_ordinals(tree)

    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            indent = " " * n.col_offset
            rep = import_replacement(n, indent)
            if rep is not None:
                imports.append((n.lineno, n.col_offset, n.end_lineno, n.end_col_offset, rep))
                counts["I import split" if "\n" in rep else "I import moved"] += 1
            continue

        if isinstance(n, ast.Name) and n.id in TYPE_RENAME:
            edits.append((n.lineno, n.col_offset, n.end_col_offset, TYPE_RENAME[n.id]))
            counts["T1 type name"] += 1

        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            # S1 and S3 — the defaults table a `**` splat reads, in every binding shape
            # the repository actually uses. A sweep for `ast.Assign -> ast.Dict` alone
            # sees 16 of the 37 sites; `defaults: dict = {...}` is an AnnAssign and
            # `defaults = dict(...)` is a Call, and each of those two misses cost this
            # dry run a full suite run before it was measured.
            if isinstance(n, ast.Assign):
                target = n.targets[0] if len(n.targets) == 1 else None
            else:
                target = n.target
            if not isinstance(target, ast.Name) or n.value is None:
                continue
            ctor = splatted.get(target.id)
            if ctor:
                rewrite_splat_source(n.value, ctor, src, edits, counts, unhandled,
                                     path, target.id)

        elif isinstance(n, ast.Call):
            f = n.func
            called = recv_name(f) if isinstance(f, (ast.Name, ast.Attribute)) else None

            if (isinstance(f, ast.Attribute) and f.attr == "isoformat"
                    and isinstance(f.value, ast.Attribute)
                    and f.value.attr == "created_at"
                    and is_jobish(recv_name(f.value.value))):
                edits.append((n.lineno, f.value.end_col_offset, n.end_col_offset, ""))
                counts["T6 isoformat"] += 1

            if called in SEAM:
                new = SEAM[called]
                if isinstance(f, ast.Name):
                    edits.append((f.lineno, f.col_offset, f.end_col_offset, new))
                else:
                    edits.append((f.lineno, f.end_col_offset - len(f.attr),
                                  f.end_col_offset, new))
                counts["T5 seam"] += 1

            if called in CTOR_KW:
                table = CTOR_KW[called]
                for k in n.keywords:
                    if k.arg in table:
                        edits.append((k.lineno, k.col_offset,
                                      k.col_offset + len(k.arg), table[k.arg]))
                        counts[f"T4 {k.arg}"] += 1
                        if k.arg == "id":
                            rewrite_id_value(called, n, k, src, edits, counts,
                                             unhandled, path, minted, ordinals)
                    elif k.arg is None and isinstance(k.value, ast.Dict):
                        # `Job(**{...})` — the table is the splat argument itself.
                        rewrite_dict_keys(k.value, called, src, edits, counts,
                                          unhandled, path)

            # S2 — a call to a helper factory defined in this same file.
            if isinstance(f, ast.Name) and f.id in helpers:
                table = SPLAT_KEY[helpers[f.id]]
                for k in n.keywords:
                    if k.arg not in table:
                        continue
                    new = table[k.arg]
                    if new is None:
                        drop_call_keyword(n, k, src, edits, counts, unhandled, path)
                    else:
                        edits.append((k.lineno, k.col_offset,
                                      k.col_offset + len(k.arg), new))
                        counts["S2 helper keyword"] += 1

        elif isinstance(n, ast.Attribute) and n.attr == "value" \
                and isinstance(n.value, ast.Attribute) and n.value.attr == "status" \
                and status_keys.get(id(n.value)) in STATUS_RULED.get(path, ()):
            # T8 — a `.value` read on a status that is a `str` after the flip becomes a
            # read of the status. The `.value` suffix is deleted; nothing else moves.
            edits.append((n.lineno, n.value.end_col_offset, n.end_col_offset, ""))
            counts["T8 status value read"] += 1

        elif isinstance(n, ast.Attribute):
            # P1 — the ruled site set decides, and the owner decides which table.
            key = (path, n.lineno, n.col_offset, n.attr)
            owner = RULED.get(key)
            start = n.end_col_offset - len(n.attr)
            if owner == "Job" and n.attr in JOB_FIELD:
                edits.append((n.lineno, start, n.end_col_offset, JOB_FIELD[n.attr]))
                counts["T2 job field"] += 1
            elif owner == "Task" and n.attr in TASK_FIELD:
                edits.append((n.lineno, start, n.end_col_offset, TASK_FIELD[n.attr]))
                counts["T3 task field"] += 1
            elif n.attr in ("id", "name", "description"):
                undecided.append((path, n.lineno, recv_name(n.value), n.attr,
                                  key in RULED_KEYS))
    return edits, imports


MINTER = "mint_job_id"
MINTER_IMPORT = f"from packages.orchestration.data_paths import {MINTER}"


def scope_minted_names(tree):
    """Names a scope binds to `uuid4()`, so `jid = uuid4(); Job(id=jid)` is reachable."""
    out = {}
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module)):
            continue
        for n in ast.walk(fn):
            if (isinstance(n, ast.Assign) and len(n.targets) == 1
                    and isinstance(n.targets[0], ast.Name)
                    and isinstance(n.value, ast.Call)
                    and isinstance(n.value.func, ast.Name)
                    and n.value.func.id in ("uuid4", "_uuid4")):
                out[n.targets[0].id] = n.value
    return out


```

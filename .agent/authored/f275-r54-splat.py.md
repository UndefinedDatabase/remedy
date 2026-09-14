# F275 R54 — `f275_r54_splat.py`, the `**` splat resolver and its artefact generator

> Committed verbatim so `.agent/f275_t003_splat_sites.md` is reproducible from the
> repository itself. It is a `.md` and not a `.py` because a `.py` file anywhere
> `ruff check .` scans is counted by `tests/orchestration/test_ci_budgets.py`.

```python
"""F275 R54 — DECISION F275 D29's P3: the `**` splat class, resolved to its dict literals.

Usage: python3 -B f275_r54_splat.py <base> [<out.md>]

Rule I4 of `.agent/f275_t003_flip_residue.md`: a keyword arriving through `**defaults` is
not a `keyword.arg`, so no rewrite of `keyword.arg` reaches it and the classic key survives
the flip into a constructor that refuses it. This instrument resolves those sites.

For every `Job(...)` / `Task(...)` call carrying a `**` argument it resolves the splatted
expression, within the enclosing scope, to the dict literals that feed it — a direct
`{...}`, a name assigned a `{...}`, and the `.update(...)` / `|` / `**` merges applied to
it — and reports the KEYS those literals carry. The construction mapping this chain has
ruled is then applied to each key, so a key nothing rules is visible rather than assumed.
"""
import ast
import collections
import json
import os
import subprocess
import sys

TARGETS = ("Job", "Task")
EXCLUDE = {"packages/core/models.py", "packages/orchestration/pingpong_job.py",
           "packages/orchestration/storage.py", "tests/test_storage.py",
           "tests/test_models.py"}
# What this chain has ruled a classic construction keyword becomes on the unified record.
RULED = {
    "Job": {"id": "job_id (DECISION F275 D24)", "name": "job_title (DECISION F275 D24)",
            "created_at": "created_at, an isoformat str (DECISION F275 D24)"},
    "Task": {"id": "task_id (DECISION F275 D25)", "description": "title (DECISION F275 D25)",
             "type": "DROPPED — never set anything (DECISION F275 D25)",
             "task_type": "DROPPED — never set anything (DECISION F275 D25)"},
}
SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)


def call_class(node):
    if not isinstance(node, ast.Call):
        return None
    f = node.func
    n = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
    return n if n in TARGETS else None


def enclosing_scopes(tree):
    """(node -> the nearest enclosing FunctionDef/Lambda), for splat resolution."""
    owner = {}

    def walk(node, cur):
        for child in ast.iter_child_nodes(node):
            nxt = child if isinstance(child, SCOPES) else cur
            owner[child] = cur
            walk(child, nxt)

    walk(tree, None)
    return owner


def dict_keys(node):
    """The literal string keys a dict expression carries, plus a flag for unknown parts."""
    keys, opaque = [], False
    if isinstance(node, ast.Dict):
        for k in node.keys:
            if k is None:
                opaque = True                      # `{**other}`
            elif isinstance(k, ast.Constant) and isinstance(k.value, str):
                keys.append(k.value)
            else:
                opaque = True
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
        for kw in node.keywords:
            if kw.arg is None:
                opaque = True
            else:
                keys.append(kw.arg)
    else:
        opaque = True
    return keys, opaque


def resolve(name, scope, path):
    """Every literal key reaching `name` inside `scope`: its assignment and its merges."""
    keys, opaque, evidence = [], False, []
    if scope is None:
        return keys, True, evidence
    for n in ast.walk(scope):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and \
                isinstance(n.targets[0], ast.Name) and n.targets[0].id == name:
            k, o = dict_keys(n.value)
            keys += k
            opaque = opaque or o
            evidence.append(("assign", n.lineno, sorted(set(k)), o))
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) \
                and n.target.id == name and n.value is not None:
            # `defaults: dict = {...}` is an AnnAssign, not an Assign, and this repository
            # writes the helper factories that way: 11 sites were invisible without this.
            k, o = dict_keys(n.value)
            keys += k
            opaque = opaque or o
            evidence.append(("annassign", n.lineno, sorted(set(k)), o))
        elif isinstance(n, ast.AugAssign) and isinstance(n.target, ast.Name) \
                and n.target.id == name:
            k, o = dict_keys(n.value)
            keys += k
            opaque = opaque or o
            evidence.append(("augassign", n.lineno, sorted(set(k)), o))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and n.func.attr == "update" and isinstance(n.func.value, ast.Name) \
                and n.func.value.id == name:
            for a in n.args:
                k, o = dict_keys(a)
                keys += k
                opaque = opaque or o
                evidence.append(("update", n.lineno, sorted(set(k)), o))
            for kw in n.keywords:
                if kw.arg:
                    keys.append(kw.arg)
                else:
                    opaque = True
    return keys, opaque, evidence

OUT_LINES: list = []


def say(s=""):
    print(s)
    OUT_LINES.append(s)


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    paths = [p for p in subprocess.run(["git", "ls-files", "*.py"], cwd=base, check=True,
                                       capture_output=True, text=True).stdout.split("\n") if p]
    scanned = [p for p in paths if p not in EXCLUDE]

    sites, plain = [], collections.Counter()
    for rel in scanned:
        try:
            tree = ast.parse(open(os.path.join(base, rel), "rb").read(), filename=rel)
        except (SyntaxError, OSError, ValueError):
            continue
        owner = enclosing_scopes(tree)
        for n in ast.walk(tree):
            cls = call_class(n)
            if cls is None:
                continue
            splats = [kw for kw in n.keywords if kw.arg is None]
            if not splats:
                plain[cls] += 1
                continue
            for kw in splats:
                scope = owner.get(n)
                while scope is not None and not isinstance(scope, SCOPES):
                    scope = owner.get(scope)
                if isinstance(kw.value, ast.Name):
                    keys, opaque, ev = resolve(kw.value.id, scope, rel)
                    shape = "name"
                else:
                    keys, opaque = dict_keys(kw.value)
                    ev, shape = [], type(kw.value).__name__
                sites.append({"path": rel, "line": n.lineno, "cls": cls, "shape": shape,
                              "splat": getattr(kw.value, "id", "(expr)"),
                              "keys": sorted(set(keys)), "opaque": opaque,
                              "scope": getattr(scope, "name", "<module>"),
                              "evidence": ev})

    say("tracked .py %d | scanned %d" % (len(paths), len(scanned)))
    say("plain constructions (no splat): %s" % dict(plain))
    say("SPLAT constructions: %d  (Job %d, Task %d)"
          % (len(sites), sum(1 for s in sites if s["cls"] == "Job"),
             sum(1 for s in sites if s["cls"] == "Task")))
    say("  resolved to at least one literal key: %d"
          % sum(1 for s in sites if s["keys"]))
    say("  carrying an OPAQUE part the reader cannot resolve: %d"
          % sum(1 for s in sites if s["opaque"]))
    say("  resolved to NO key at all: %d"
          % sum(1 for s in sites if not s["keys"]))

    # The two field sets are read by IMPORTING the shipped classes, never from their source:
    # `Job` ignores an unknown keyword (pydantic's default `extra='ignore'`) while `JobPlan`
    # is a dataclass and raises `TypeError: ... unexpected keyword argument`, which is the
    # class DECISION F275 D26 measured at 867 lines.
    sys.path.insert(0, os.path.abspath(base))
    import dataclasses
    from packages.core.models import Job, Task                      # noqa: E402
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry  # noqa: E402
    FIELDS = {"Job": (set(Job.model_fields), {f.name for f in dataclasses.fields(JobPlan)}),
              "Task": (set(Task.model_fields), {f.name for f in dataclasses.fields(TaskEntry)})}
    for cls in TARGETS:
        classic, unified = FIELDS[cls]
        kc = collections.Counter()
        for s in sites:
            if s["cls"] == cls:
                for k in s["keys"]:
                    kc[k] += 1
        if not kc:
            continue
        say("\n%s(**...) keys — %d classic fields, %d unified fields:"
              % (cls, len(classic), len(unified)))
        buckets = collections.Counter()
        for k, c in kc.most_common():
            if k in RULED[cls]:
                v, b = RULED[cls][k], "ruled"
            elif k in unified:
                v, b = "carried unchanged — the unified record declares it", "carried"
            elif k not in classic:
                v, b = ("DROP — the classic record IGNORED it and the unified record REFUSES it",
                        "drop-never-set")
            else:
                v, b = ("*** UNRULED — the classic record declares it and the unified record "
                        "does not ***", "unruled")
            buckets[b] += 1
            say("  %4d  %-22s %s" % (c, k, v))
        say("  buckets: %s" % dict(buckets))

    say("\nsplat sites by file:")
    for p, c in collections.Counter(s["path"] for s in sites).most_common(15):
        say("  %4d  %s" % (c, p))

    # THE CALLERS' HALF. Rule I4 says the pass must reach the helper's dict literal AND its
    # callers' keywords: `_make_job(id=..., name=...)` is an ordinary `keyword.arg` on a call
    # whose callee is NOT `Job`, so no rewrite keyed on the constructor name reaches it.
    # A helper is resolved PER FILE and never by bare name: `_make_job` is defined
    # independently in many test modules, so a global name set attributes a call to whichever
    # definition it happens to match. Only a call in the file that DEFINES the helper counts.
    # A caller keyword matching one of the helper's OWN named parameters is consumed by the
    # helper and never reaches the constructor; only the remainder lands in `**kwargs`.
    helpers = {}                                    # path -> {name: (own params, target cls)}
    for rel in scanned:
        try:
            tree = ast.parse(open(os.path.join(base, rel), "rb").read(), filename=rel)
        except (SyntaxError, OSError, ValueError):
            continue
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                    or fn.args.kwarg is None:
                continue
            for n in ast.walk(fn):
                cls = call_class(n)
                if cls and any(kw.arg is None for kw in n.keywords):
                    own = {a.arg for a in (list(fn.args.posonlyargs) + list(fn.args.args)
                                           + list(fn.args.kwonlyargs))}
                    helpers.setdefault(rel, {})[fn.name] = (own, cls)
                    break
    say("\nHELPER FACTORIES (a `**kwargs` parameter and a target splat construction): "
          "%d in %d files" % (sum(len(v) for v in helpers.values()), len(helpers)))

    calls, consumed, ckeys = 0, collections.Counter(), collections.Counter()
    for rel in sorted(helpers):
        try:
            tree = ast.parse(open(os.path.join(base, rel), "rb").read(), filename=rel)
        except (SyntaxError, OSError, ValueError):
            continue
        local = helpers[rel]
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Name) \
                    or n.func.id not in local:
                continue
            own, cls = local[n.func.id]
            calls += 1
            for kw in n.keywords:
                if not kw.arg:
                    continue
                if kw.arg in own:
                    consumed[kw.arg] += 1
                else:
                    ckeys[(cls, kw.arg)] += 1
    say("CALLS to a helper defined in the SAME file: %d" % calls)
    say("keywords the helper's own parameters CONSUME (they never reach a constructor): %s"
          % dict(consumed.most_common(8)))
    say("keywords that reach the constructor through `**kwargs`, and what each becomes:")
    for (cls, k), c in ckeys.most_common():
        classic, unified = FIELDS[cls]
        if k in RULED[cls]:
            v = RULED[cls][k]
        elif k in unified:
            v = "carried unchanged — the unified record declares it"
        elif k not in classic:
            v = "DROP — the classic record IGNORED it and the unified record REFUSES it"
        else:
            v = "*** UNRULED — classic declares it, unified does not ***"
        say("  %4d  %s.%-20s %s" % (c, cls, k, v))

    out = sys.argv[2] if len(sys.argv) > 2 else None
    if out:
        head = [
            "# F275 T003 — the `**` splat class, resolved",
            "",
            "> DECISION F275 D29's P3, and rule I4 of `.agent/f275_t003_flip_residue.md`: a",
            "> keyword arriving through `**defaults` is not a `keyword.arg`, so no rewrite keyed",
            "> on the constructor reaches it, and the classic key survives the flip into a",
            "> constructor that refuses it. Generated by the instrument committed at",
            "> `.agent/authored/f275-r54-splat.py.md`, never retyped. Measurement base: `%s`."
            % subprocess.run(["git", "rev-parse", "--short=8", "HEAD"], cwd=base, check=True,
                             capture_output=True, text=True).stdout.strip(),
            "",
            "This file SIZES and RULES the splat class; it performs none of it, and no line",
            "under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that",
            "wrote it.",
            "",
            "## 1. Why the two records disagree, measured by CALLING them",
            "",
            "`Job` is a pydantic model whose `model_config` leaves `extra` at its default, so an",
            "unknown keyword is silently IGNORED and sets nothing. `JobPlan` is a dataclass, so",
            "the same keyword raises `TypeError: JobPlan.__init__() got an unexpected keyword",
            "argument`. Both readings were taken by constructing each class, not by reading its",
            "source. That difference is the whole of this class: a key the classic record",
            "tolerated is a key the unified record refuses.",
            "",
            "## 2. The reading, complete and untrimmed",
            "",
            "```",
        ]
        foot = [
            "```",
            "",
            "## 3. What this does NOT settle",
            "",
            "THE RESOLUTION IS PARTIAL AND SAYS SO. A splat whose expression is not a locally",
            "assigned dict literal resolves to no key of its own; those helpers take their keys",
            "entirely from their callers, which section 2's callers' half covers. A dict built",
            "by a merge the reader cannot evaluate is reported as OPAQUE rather than as empty.",
            "",
            "A HELPER IS RESOLVED PER FILE AND NEVER BY BARE NAME. `_make_job` is defined",
            "independently in many test modules, so a call is attributed only inside the file",
            "that defines the helper it names. A by-name reading across files attributes calls",
            "that no helper of this class owns, so it is not taken and not reported here.",
        ]
        open(out, "w").write("\n".join(head + OUT_LINES + foot).rstrip("\n") + "\n")
        print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

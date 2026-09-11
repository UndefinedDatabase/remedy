# F275 R61 — `f275_r61_status_sites.py`, the nine-site set of DECISION F275 D35, keyed by SCOPE

> Committed verbatim because the third retype rule family consumes this set and because
> finding `R-0879` is the record of what a set keyed by LINE NUMBER costs. Nine sites are
> not too few for that lesson: the key is `(path, enclosing scope, occurrence of the chain
> inside that scope)`, it is RESOLVED against the tree the transform is about to run on,
> and a site that fails to resolve stops the generator with a non-zero exit.
> Its first version keyed on the `.status` ATTRIBUTE and REFUSED, correctly, at
> `brain_detail.py:380` — `status=node.status or task.status.value` holds two `.status`
> nodes and only one continues into `.value`. The unit is therefore the CHAIN.
> It is a `.md` and not a `.py` because a `.py` file anywhere `ruff check .` scans is
> counted by `tests/orchestration/test_ci_budgets.py`.

```python
"""F275 R61 — the nine `Task.status.value` sites DECISION F275 D35 names, keyed by SCOPE.

`R-0879` is the finding that a site set keyed by LINE NUMBER goes stale the moment the
branch commits anything above it. That lesson binds a set of nine exactly as it binds a set
of 2198, so this set is keyed by (path, enclosing scope, occurrence index of the `status`
attribute inside that scope) from the outset, and it is RESOLVED against the tree the
transform is about to run on. If any site fails to resolve the generator exits non-zero.

Usage: python3 -B r61_status_sites.py <worktree> <out.json>
"""
import ast
import collections
import json
import sys

WT, OUT = sys.argv[1], sys.argv[2]

# The nine sites, as (path, line) at `abc9b8a9`, copied from DECISION F275 D35. The line
# numbers are used ONCE, here, to pick the node; what is STORED is the scope key.
NINE = [("apps/cli/commands/job.py", 655),
        ("packages/orchestration/brain_detail.py", 353),
        ("packages/orchestration/brain_detail.py", 366),
        ("packages/orchestration/brain_detail.py", 372),
        ("packages/orchestration/brain_detail.py", 380),
        ("packages/orchestration/project_brain.py", 317),
        ("packages/orchestration/trust_report.py", 118),
        ("tests/orchestration/test_final_audit_evidence.py", 261),
        ("tests/orchestration/test_resume_kill.py", 261)]


def index(path):
    """Every `<expr>.status.value` CHAIN of `path`, keyed by scope and occurrence."""
    src = open(f"{WT}/{path}", "rb").read()
    tree = ast.parse(src, filename=path)
    owner = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for sub in ast.walk(fn):
                if isinstance(sub, ast.Attribute):
                    prev = owner.get(id(sub))
                    if prev is None or fn.lineno > prev.lineno:
                        owner[id(sub)] = fn
    # The unit is the CHAIN `<expr>.status.value`, not the `.status` node: a single line
    # may hold two `.status` nodes — `status=node.status or task.status.value` does — and
    # only one of them continues into `.value`. Keying on the chain is unambiguous where
    # keying on the attribute is not, which this generator REFUSED to guess at.
    nodes = [n.value for n in ast.walk(tree)
             if isinstance(n, ast.Attribute) and n.attr == "value"
             and isinstance(n.value, ast.Attribute) and n.value.attr == "status"]
    nodes.sort(key=lambda n: (n.lineno, n.col_offset))
    seen = collections.Counter()
    by_scope, by_line = {}, collections.defaultdict(list)
    for n in nodes:
        fn = owner.get(id(n))
        scope = fn.name if fn else "<module>"
        seen[scope] += 1
        by_scope[(scope, seen[scope])] = n
        by_line[n.lineno].append((scope, seen[scope], n))
    return by_scope, by_line


out, lost = [], []
for path, line in NINE:
    by_scope, by_line = index(path)
    hits = by_line.get(line, [])
    if len(hits) != 1:
        lost.append((path, line, "%d `.status.value` chains on that line, expected 1" % len(hits)))
        continue
    scope, occ, node = hits[0]
    out.append({"path": path, "scope": scope, "occ": occ,
                "line_at_generation": line, "col": node.col_offset})

print("nine sites, keyed by (path, scope, occurrence):")
for r in out:
    print("   %-52s %-34s #%d   (line %d here)"
          % (r["path"], r["scope"], r["occ"], r["line_at_generation"]))
print("resolved %d of %d" % (len(out), len(NINE)))
if lost:
    print("\nTHE GENERATOR REFUSES. Unresolved:")
    for row in lost:
        print("   %s" % (row,))
    sys.exit(3)

json.dump({"sites": out}, open(OUT, "w"), indent=1)
print("wrote %s" % OUT)
```

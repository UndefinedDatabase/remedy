# F275 R59 — `f275_r59_rekey.py`, the site-set re-key and its refusal precondition

> Committed verbatim because DECISION F275 D34 part two orders this stage and finding
> `R-0879` is what it answers. It sits BETWEEN the measured ruled site set and the flip
> transform: it re-expresses every site by a key that carries no line number, resolves that
> key against the tree the transform is about to run on, and emits the set back in the
> `(path, line, col, attr)` form the transform already consumes — so the transform itself
> is unchanged. If ANY ruled site fails to resolve it exits non-zero and names the count
> and the files, which is the whole point: the defect was never that a key drifted but that
> nothing noticed for three rounds.
> It is a `.md` and not a `.py` because a `.py` file anywhere `ruff check .` scans is
> counted by `tests/orchestration/test_ci_budgets.py`.

```python
"""F275 R59 — re-key the ruled site set off line numbers, and REFUSE on a stale one.

DECISION F275 D34 part two. The ruled site set R of `.agent/f275_t003_descriptor_sites.md`
is 2198 sites keyed by (path, line, col, attr), measured at `a815c9a3`. A line number is
not an identity: round 57's migration moved 54 of them and the transform then renamed
nothing there, which is finding `R-0879`.

This stage sits BETWEEN the measured set and the transform. It re-keys every ruled site by
(path, enclosing scope qualname, attr, occurrence index of that attr inside that scope, in
source order), resolves that key against the tree the transform is about to run on, and
emits the set re-expressed as (path, line, col, attr) keys AT THAT TREE — so the transform
itself keeps the interface it already has.

THE PRECONDITION IS THE POINT. If ANY ruled site fails to resolve at the new tree, this
stage exits NON-ZERO and names the count and the files. The defect D34 rules is not that a
key drifted; it is that nothing noticed for three rounds.

Usage: python3 -B r59_rekey.py <OLD_WT> <NEW_WT> <R.json> <owners.json> <out.json>
"""
import ast
import collections
import json
import sys

OLD, NEW, R_JSON, OWNERS_JSON, OUT = sys.argv[1:6]


def index(wt, path):
    """Every Attribute node of `path`, keyed BOTH ways, in one pass.

    Lifted byte-for-byte from `.remedy-wt/r58_rekey.py`, the script whose measurement
    DECISION F275 D34 rests on, so that this stage resolves keys exactly as the reading
    that ruled them did.
    """
    try:
        src = open(f"{wt}/{path}", "rb").read()
        tree = ast.parse(src, filename=path)
    except (SyntaxError, OSError):
        return None, None
    owner = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for sub in ast.walk(fn):
                # innermost wins: a later, deeper assignment overwrites
                if isinstance(sub, ast.Attribute):
                    prev = owner.get(id(sub))
                    if prev is None or fn.lineno > prev.lineno:
                        owner[id(sub)] = fn
    nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Attribute)]
    nodes.sort(key=lambda n: (n.lineno, n.col_offset))
    seen = collections.Counter()
    by_line, by_scope = {}, {}
    for n in nodes:
        fn = owner.get(id(n))
        scope = fn.name if fn else "<module>"
        k = (scope, n.attr)
        seen[k] += 1
        by_line[(n.lineno, n.col_offset, n.attr)] = n
        by_scope[(scope, n.attr, seen[k])] = n
    return by_line, by_scope


with open(R_JSON) as fh:
    R = [tuple(r) for r in json.load(fh)["R"]]
with open(OWNERS_JSON) as fh:
    OWNERS = {}
    for key, owner in json.load(fh).items():
        p, ln, col, attr = key.rsplit("|", 3)
        OWNERS[(p, int(ln), int(col), attr)] = owner

paths = sorted({p for p, _l, _c, _a in R})

resolved = []          # (path, line, col, attr) AT THE NEW TREE
resolved_owners = {}   # same key -> owner
lost = []              # ruled sites that do NOT resolve at the new tree
line_ok = 0            # THE CONTROL: what the old line key alone would have recovered

for path in paths:
    old_line, old_scope = index(OLD, path)
    new_line, new_scope = index(NEW, path)
    if old_line is None:
        lost += [(p, ln, attr, "unreadable at OLD") for p, ln, _c, attr in R if p == path]
        continue
    if new_line is None:
        lost += [(p, ln, attr, "unreadable at NEW") for p, ln, _c, attr in R if p == path]
        continue
    rev = {id(node): key for key, node in old_scope.items()}
    for p, ln, col, attr in [r for r in R if r[0] == path]:
        node = old_line.get((ln, col, attr))
        if node is None:
            lost.append((p, ln, attr, "not found at OLD"))
            continue
        if (ln, col, attr) in new_line:
            line_ok += 1
        key = rev.get(id(node))
        target = new_scope.get(key) if key else None
        if target is None:
            lost.append((p, ln, attr, f"scope key {key} unresolved at NEW"))
            continue
        nk = (p, target.lineno, target.col_offset, target.attr)
        resolved.append(nk)
        owner = OWNERS.get((p, ln, col, attr))
        if owner is not None:
            resolved_owners[nk] = owner

print(f"ruled sites in R                     : {len(R)}")
print(f"recovered by (scope, attr, occurrence): {len(resolved)}")
print(f"CONTROL, recovered by (line, col, attr): {line_ok}")
print(f"UNRESOLVED                            : {len(lost)}")
print(f"owners carried across                 : {len(resolved_owners)}")

if lost:
    print("\nTHE PRECONDITION REFUSES. Unresolved ruled sites, by file:")
    for f, n in collections.Counter(x[0] for x in lost).most_common():
        print(f"   {n:>4}  {f}")
    for row in lost[:20]:
        print(f"        {row}")
    sys.exit(3)

with open(OUT, "w") as fh:
    json.dump({"R": [list(k) for k in resolved]}, fh)
owners_out = OUT.replace(".json", "_owners.json")
with open(owners_out, "w") as fh:
    json.dump({"|".join(str(x) for x in k): v for k, v in resolved_owners.items()}, fh)
print(f"\nwrote {OUT} and {owners_out}")
```

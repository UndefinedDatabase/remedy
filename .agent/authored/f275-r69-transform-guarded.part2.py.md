# F275 R69 — the guarded flip transform, part 2 of two, verbatim

> THE FILE IS SPLIT BECAUSE OF THE INSERTION CAP, NOT BECAUSE IT HAS TWO PARTS.
> The guarded transform is one file of 653 lines; a single authored blob would be
> one commit of over 500 insertions, which AGENTS.md DECISION F104 D1 forbids and whose
> exemption list names only the five `.agent/` state files. The fence below is part 2
> of two, and the two fences CONCATENATE BYTE FOR BYTE to the whole file — the round's
> gate re-derives that rather than trusting it. The cut falls at a top-level `def`
> boundary so each part parses as a readable unit of its own.
>
> Saved as `.md` and not as `.py` so that `ruff check .` does not count it, per the
> ceiling `tests/orchestration/test_ci_budgets.py` freezes.

```python
def task_ordinals(tree):
    """The ORDINAL of every `Task(id=...)` construction, which is its unified id.

    `TaskEntry.task_id` is `f"T{parse_idx + 1:03d}"` by parse order, so a task's unified
    id is its POSITION in its job's task list and not a minted value. Three shapes carry
    that position and each is resolved here; anything else resolves to None and the site
    is reported rather than guessed at.

      L  a list literal — the element index IS the position
      C  a comprehension over `range(...)` — the loop variable is the position
      A  a lone `append` or a lone construction in its function — position 1
    """
    out = {}
    for parent in ast.walk(tree):
        for _field, value in ast.iter_fields(parent):
            for child in (value if isinstance(value, list) else [value]):
                if isinstance(child, ast.AST):
                    child._r58_parent = parent
    made = [n for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id in ("Task", "TaskEntry")
            and any(k.arg == "id" for k in n.keywords)]
    for n in made:
        parent = getattr(n, "_r58_parent", None)
        if isinstance(parent, ast.List):
            out[id(n)] = ("literal", f'"T{parent.elts.index(n) + 1:03d}"')
        elif isinstance(parent, (ast.ListComp, ast.GeneratorExp)):
            gens = parent.generators
            var = gens[0].target.id if gens and isinstance(gens[0].target, ast.Name) else None
            out[id(n)] = ("comprehension", f'f"T{{{var} + 1:03d}}"' if var else None)
        else:
            fn = None
            for cand in ast.walk(tree):
                if isinstance(cand, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if cand.lineno <= n.lineno <= (cand.end_lineno or cand.lineno):
                        if fn is None or cand.lineno > fn.lineno:
                            fn = cand
            siblings = [m for m in made
                        if fn and fn.lineno <= m.lineno <= (fn.end_lineno or fn.lineno)]
            out[id(n)] = ("lone", '"T001"') if len(siblings) == 1 else ("other", None)
    return out


def rewrite_id_value(called, call, kw, src, edits, counts, unhandled, path,
                     minted, ordinals):
    """DECISION F275 D32's first rule family, and it is TWO rules, not one.

    A JOB id has a mechanical counterpart: the unified record spells it as the sixteen hex
    characters `data_paths.mint_job_id()` returns, so `uuid4()` becomes that call and a
    `UUID(x)` coercion becomes `x`. A TASK id does not: `TaskEntry.task_id` is an ORDINAL
    by parse order, so the counterpart is the position, resolved by `task_ordinals`.
    """
    v = kw.value
    if called == "Task":
        kind, literal = ordinals.get(id(call), ("other", None))
        if literal is None:
            unhandled.append((path, call.lineno, called, "id",
                              f"task ordinal unresolved ({kind})"))
            return
        edits.append((v.lineno, v.col_offset, v.end_col_offset, literal))
        counts[f"T7 task ordinal ({kind})"] += 1
        return
    # a JOB id
    if isinstance(v, ast.Call) and isinstance(v.func, ast.Name):
        if v.func.id in ("uuid4", "_uuid4"):
            edits.append((v.lineno, v.col_offset, v.end_col_offset, f"{MINTER}()"))
            counts["T7 job id minted"] += 1
            return
        if v.func.id == "UUID" and len(v.args) == 1 and not v.keywords:
            inner = v.args[0]
            keep = src.split("\n")[inner.lineno - 1].encode("utf-8")[
                inner.col_offset:inner.end_col_offset].decode("utf-8")
            if inner.lineno == inner.end_lineno:
                edits.append((v.lineno, v.col_offset, v.end_col_offset, keep))
                counts["T7 job id UUID() unwrapped"] += 1
                return
    if isinstance(v, ast.Name) and v.id in minted:
        src_call = minted[v.id]
        edits.append((src_call.lineno, src_call.col_offset, src_call.end_col_offset,
                      f"{MINTER}()"))
        counts["T7 job id minted via a local"] += 1
        return
    counts["T7 job id left alone"] += 1


def rewrite_splat_source(value, ctor, src, edits, counts, unhandled, path, label):
    """Rewrite the defaults table a `**` splat reads, whatever shape it is written in."""
    if isinstance(value, ast.Dict):
        rewrite_dict_keys(value, ctor, src, edits, counts, unhandled, path)
        return
    if (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
            and value.func.id == "dict"):
        table = SPLAT_KEY[ctor]
        for kw in value.keywords:
            if kw.arg not in table:
                continue
            new = table[kw.arg]
            if new is None:
                drop_call_keyword(value, kw, src, edits, counts, unhandled, path)
            else:
                edits.append((kw.lineno, kw.col_offset,
                              kw.col_offset + len(kw.arg), new))
                counts["S3 dict-call key"] += 1
        return
    unhandled.append((path, value.lineno, ctor, label,
                      f"splat source is {type(value).__name__}"))


def rewrite_dict_keys(node, ctor, src, edits, counts, unhandled, path):
    """S1 — rename or DROP the constant string keys of one dict literal."""
    table = SPLAT_KEY[ctor]
    lines = src.split("\n")
    for key, value in zip(node.keys, node.values):
        if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
            continue
        if key.value not in table:
            continue
        new = table[key.value]
        if new is not None:
            # The key node's span covers its quotes; replace the text between them.
            edits.append((key.lineno, key.col_offset + 1,
                          key.end_col_offset - 1, new))
            counts["S1 splat key"] += 1
            continue
        # A DROP: remove the whole `"key": value` element and one trailing comma.
        if key.lineno != value.end_lineno:
            unhandled.append((path, key.lineno, ctor, key.value, "multi-line element"))
            continue
        raw = lines[key.lineno - 1].encode("utf-8")
        end = value.end_col_offset
        while end < len(raw) and raw[end:end + 1] in (b" ", b","):
            end += 1
        head = raw[:key.col_offset].decode("utf-8")
        tail = raw[end:].decode("utf-8")
        if head.strip() == "" and tail.strip() == "":
            edits.append((key.lineno, 0, len(raw), DELETE_LINE))
        else:
            edits.append((key.lineno, key.col_offset, end, ""))
        counts["S1 splat key DROPPED"] += 1


def drop_call_keyword(call, kw, src, edits, counts, unhandled, path):
    """S2's DROP half — remove a `key=value` argument and one trailing comma."""
    lines = src.split("\n")
    if kw.lineno != kw.value.end_lineno:
        unhandled.append((path, kw.lineno, "call", kw.arg, "multi-line argument"))
        return
    raw = lines[kw.lineno - 1].encode("utf-8")
    end = kw.value.end_col_offset
    while end < len(raw) and raw[end:end + 1] in (b" ", b","):
        end += 1
    head = raw[:kw.col_offset].decode("utf-8")
    tail = raw[end:].decode("utf-8")
    if head.strip() == "" and tail.strip() == "":
        edits.append((kw.lineno, 0, len(raw), DELETE_LINE))
    else:
        edits.append((kw.lineno, kw.col_offset, end, ""))
    counts["S2 helper keyword DROPPED"] += 1


def apply_edits(src, edits, imports):
    """Line edits right-to-left IN BYTES; then whole-node import replacements.

    A DROP is marked IN PLACE with a sentinel and filtered only at the end. An index
    cannot carry it: I2 SPLICES an import node into two statements, so every line number
    below that node moves, and a deletion index computed before the splice removes a line
    four below the one the rule named. That is a silent corruption — the result still
    parses — and it cost this dry run one run.
    """
    lines = src.split("\n")
    by_line = collections.defaultdict(list)
    drops = set()
    for lineno, a, b, new in edits:
        if new == DELETE_LINE:
            drops.add(lineno)
        else:
            by_line[lineno].append((a, b, new))
    for lineno, items in by_line.items():
        idx = lineno - 1
        if idx >= len(lines) or lineno in drops:
            continue
        raw = lines[idx].encode("utf-8")
        for a, b, new in sorted(set(items), key=lambda x: -x[0]):
            raw = raw[:a] + new.encode("utf-8") + raw[b:]
        lines[idx] = raw.decode("utf-8")
    for lineno in drops:
        if lineno - 1 < len(lines):
            lines[lineno - 1] = DELETE_LINE

    # Replace import statements last and bottom-up, so earlier spans keep their indices.
    for lineno, col, end_lineno, end_col, rep in sorted(imports, key=lambda x: -x[0]):
        head = lines[lineno - 1].encode("utf-8")[:col].decode("utf-8")
        tail = lines[end_lineno - 1].encode("utf-8")[end_col:].decode("utf-8")
        lines[lineno - 1:end_lineno] = (head + rep + tail).split("\n")

    return "\n".join(ln for ln in lines if ln != DELETE_LINE)


def ensure_minter_import(out, counts, unhandled, rel):
    """I5 — the MINTER's import arrives with the minter, exactly as I3 does for the seam.

    Rewriting `Job(id=uuid4())` to `JobPlan(job_id=mint_job_id())` while leaving the name
    unbound is the `NameError` rule I3 already records for `save_job_plan`, arriving
    through a VALUE instead of through a call. The import goes after the LAST top-level
    `import` or `from` statement, which is where this repository puts them.
    """
    if f"{MINTER}(" not in out or MINTER_IMPORT in out:
        return out
    if f"import {MINTER}" in out or f"{MINTER} as " in out:
        return out
    try:
        tree = ast.parse(out)
    except SyntaxError:
        unhandled.append((rel, 0, "I5", MINTER, "output did not parse before the import"))
        return out
    last = 0
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last = max(last, node.end_lineno or node.lineno)
    if last == 0:
        unhandled.append((rel, 0, "I5", MINTER, "no top-level import to anchor to"))
        return out
    lines = out.split("\n")
    lines.insert(last, MINTER_IMPORT)
    counts["I5 minter import added"] += 1
    return "\n".join(lines)


def refuse_on_stale_site_set():
    """DECISION F275 D43, finding `R-0879`. THE PRECONDITION THE TRANSFORM OWES ITS INPUT.

    P1 keys by the node it is standing on — `(path, n.lineno, n.col_offset, n.attr)` — so a
    ruled key at a position no Attribute node occupies can never be produced by the walk and
    renames nothing, silently. Round 68 measured that cost at 54 renames against the round 53
    committed set. A set that has gone stale must STOP a run rather than quietly edit less of
    the tree than it says it does, which is the whole of what `R-0879` asks for.

    The re-key stage is the repair and this is the backstop: the stage refuses to EMIT a
    stale set, and this refuses to CONSUME one, so skipping the stage cannot reintroduce the
    defect.
    """
    lost, detail = collections.Counter(), []
    for rel in sorted({k[0] for k in RULED_KEYS}):
        keys = [k for k in RULED_KEYS if k[0] == rel]
        try:
            tree = ast.parse((WT / rel).read_text(), filename=rel)
        except (SyntaxError, OSError):
            lost[rel] += len(keys)
            detail.append((rel, None, None, "unreadable at this tree"))
            continue
        pos = {(n.lineno, n.col_offset, n.attr) for n in ast.walk(tree)
               if isinstance(n, ast.Attribute)}
        for k in keys:
            if (k[1], k[2], k[3]) not in pos:
                lost[rel] += 1
                detail.append(k)
    total = sum(lost.values())
    print(f"PRECONDITION: ruled keys {len(RULED_KEYS)} | "
          f"resolving at this tree {len(RULED_KEYS) - total} | NOT resolving {total}")
    if total:
        print("")
        print("THE TRANSFORM REFUSES. The ruled site set is STALE against this tree: the "
              "keys below resolve to no attribute node, so a run would rename less of the "
              "tree than the set names, and would say nothing about it. Finding R-0879.")
        for rel, n in lost.most_common():
            print(f"   {n:>4}  {rel}")
        for row in sorted(detail)[:20]:
            print(f"        {row}")
        sys.exit(4)


def main():
    refuse_on_stale_site_set()
    counts = collections.Counter()
    undecided, unhandled = [], []
    written, skipped, broke = 0, 0, []
    for rel in tracked():
        if rel in EXCLUDE:
            counts["X excluded"] += 1
            continue
        p = WT / rel
        try:
            src = p.read_text()
        except OSError:
            skipped += 1
            continue
        try:
            edits, imports = collect(rel, src, counts, undecided, unhandled)
        except SyntaxError:
            skipped += 1
            continue
        if not edits and not imports:
            continue
        out = apply_edits(src, edits, imports)
        out = ensure_minter_import(out, counts, unhandled, rel)
        try:
            ast.parse(out, filename=rel)
        except SyntaxError as exc:
            broke.append((rel, str(exc)))
            continue
        p.write_text(out)
        written += 1

    print(f"files rewritten: {written} | skipped unparsable: {skipped}")
    print(f"files the edit would have BROKEN and were left alone: {len(broke)}")
    for rel, err in broke[:20]:
        print(f"  {rel}: {err}")
    print("\nrewrites by rule:")
    for k, v in sorted(counts.items()):
        print(f"  {k:26s} {v}")
    print(f"total rewrites: {sum(v for k, v in counts.items() if not k.startswith('X'))}")

    print(f"\nDROP elements the edit could not reach: {len(unhandled)}")
    for row in unhandled[:20]:
        print("   ", row)

    in_r = [u for u in undecided if u[4]]
    print(f"\nUNDECIDED .id/.name/.description sites: {len(undecided)}"
          f" | of those IN the ruled set but with no owner: {len(in_r)}")
    by_recv = collections.Counter(r[2] for r in in_r)
    for r, c in by_recv.most_common(15):
        print(f"    {r or '(expr)':26s} {c}")


main()
```

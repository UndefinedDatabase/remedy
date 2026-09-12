# F275 R82 — the generator that builds the flip's input set

This is the producer of `.agent/f275_t003_flip_input_r82.md`. It performs the
subtraction DECISION F275 D55 orders, re-keys the surviving set onto the tree the
flip will run on with the committed round 59 stage, re-checks it with the committed
round 73 owner check, and runs two controls beside the re-key. Its stdout IS the
artefact's body.

It is carried in a `.md` rather than a `.py` on purpose: `tests/orchestration/test_ci_budgets.py`
counts every `.py` file `ruff check .` scans, and a scratch instrument committed under
`.agent/` is not production code. The carrier holds exactly one `python` fence and the
fence is extracted, never retyped.

NO COMMIT ID AND NO REPOSITORY PATH IS EMBEDDED. Every tree, every data input and every
instrument arrives as an argument, so the flip round re-derives its input at ITS OWN base
instead of inheriting a set measured in round 82. Nothing printed carries a wall-clock
value of any kind, because the artefact is compared byte for byte against a later re-run.

Usage:

    python3 -B <extracted fence> BASE TIP SHIFT DELETE \
        CORRECTED_JSON OWNERS_JSON REKEY_PY OWNER_PY SCRATCH

BASE is the tree the corrected set is keyed at; TIP is the tree the flip will run on;
SHIFT and DELETE are the two controls — TIP with three blank lines inserted inside one
module's docstring, and TIP with one ruled statement removed. Each of the four needs a
git index, because the owner check enumerates with `git ls-files`.

```python
"""F275 R82 — the flip's input set: subtract, re-key, re-check, and control.

Stdout is the artefact's body. Every listing over a set is sorted before it is
emitted and no wall-clock value is printed, so three runs agree byte for byte.
"""
import hashlib
import json
import os
import subprocess
import sys

(BASE, TIP, SHIFT, DELETE, CORRECTED, OWNERS, REKEY, OWNER,
 SCRATCH) = sys.argv[1:10]

# The two sites DECISION F275 D55 takes out of the flip's input, BY NAME. They are
# data, not a measurement: the decision names them and this stage removes exactly them.
DROP = [
    ("tests/cli/test_repair_runtime.py", 68, 32, "id"),
    ("packages/orchestration/brain_detail.py", 345, 54, "id"),
]
# The module the DELETE control mutates. Named here only so the partition of S2 knows
# which file to partition; the mutation itself is made outside this generator.
MUTATED = "packages/orchestration/brain_detail.py"

DROPSET = set(DROP)


def emit(s=""):
    """One artefact line. Every non-blank line carries exactly one leading space."""
    sys.stdout.write((" " + s if s else "") + "\n")


def emit_stream(text, tag):
    """A sub-instrument's WHOLE stdout, one line per line, indented four further.

    A line the instrument left empty is emitted empty rather than as four spaces:
    an artefact line of nothing but whitespace is trailing whitespace, and the
    artefact is a committed document.
    """
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines:
        emit("    (%s was empty)" % tag)
        return
    for ln in lines:
        emit(("    " + ln) if ln.strip() else "")


def digest(path):
    b = open(path, "rb").read()
    return len(b), hashlib.sha256(b).hexdigest()


def load_sites(path):
    return [tuple(x) for x in json.load(open(path))["R"]]


def load_owners(path):
    out = {}
    for k, v in json.load(open(path)).items():
        p, ln, col, attr = k.rsplit("|", 3)
        out[(p, int(ln), int(col), attr)] = v
    return out


def key_str(k):
    return "%s|%d|%d|%s" % k


def write_set(sites, owners, stem):
    """The pair of files the two instruments read: a ruled set and an owners map."""
    a = os.path.join(SCRATCH, stem + ".json")
    b = os.path.join(SCRATCH, stem + "_owners.json")
    json.dump({"R": [list(k) for k in sites]}, open(a, "w"))
    json.dump({key_str(k): v for k, v in sorted(owners.items())}, open(b, "w"))
    return a, b


def argv_line(argv):
    """The argument vector by basename: literal, and free of any scratch prefix."""
    return "$ python3 -B " + " ".join(os.path.basename(x) for x in argv[2:])


def run(argv, tag):
    p = subprocess.run(argv, capture_output=True, text=True)
    emit("    " + argv_line(argv))
    emit_stream(p.stdout, tag + " stdout")
    if p.stderr.strip():
        emit_stream(p.stderr, tag + " stderr")
    emit("    REAL EXIT CODE = %d" % p.returncode)
    return p.returncode


# ---------------------------------------------------------------- S0
emit("S0  THE PINNED INPUTS, BY BYTE COUNT AND DIGEST")
emit()
for label, path in (("corrected set", CORRECTED), ("corrected owners", OWNERS),
                    ("re-key stage", REKEY), ("owner check", OWNER)):
    n, s = digest(path)
    emit("    %-18s %-34s %7d bytes  sha256 %s"
         % (label, os.path.basename(path), n, s))
emit()

# ---------------------------------------------------------------- S1
R = load_sites(CORRECTED)
OWN = load_owners(OWNERS)

emit("S1  THE SUBTRACTION")
emit()
emit("    corrected set, ruled sites               : %d" % len(R))
emit("    corrected set, distinct tuples           : %d" % len(set(R)))
emit("    owners map, keys                         : %d" % len(OWN))
unnamed = sorted(set(R) - set(OWN))
emit("    ruled sites the owners map does NOT name : %d" % len(unnamed))
for k in unnamed:
    emit("        %s" % key_str(k))
emit()
for k in DROP:
    emit("    DROP %s" % key_str(k))
    emit("        occurrences in the corrected set : %d" % R.count(k))
    emit("        owner in the owners map          : %s" % OWN.get(k, "(none)"))
emit()
kept = [k for k in R if k not in DROPSET]
kept_owners = {k: v for k, v in OWN.items() if k not in DROPSET}
emit("    after the subtraction, ruled sites        : %d" % len(kept))
emit("    after the subtraction, owner keys         : %d" % len(kept_owners))
emit("    CROSS-CHECK sites removed                 : %d  exactly two: %s"
     % (len(R) - len(kept), len(R) - len(kept) == 2))
emit("    CROSS-CHECK owner keys removed            : %d  exactly two: %s"
     % (len(OWN) - len(kept_owners), len(OWN) - len(kept_owners) == 2))
survivors = [k for k in DROP if k in set(kept)]
emit("    CROSS-CHECK dropped sites that survive    : %d  none survives: %s"
     % (len(survivors), not survivors))
emit()
emit("    the canonical form is sorted(surviving set) rendered by json.dumps with")
emit("    separators=(\",\", \":\"), encoded UTF-8")
payload = json.dumps(sorted(kept), separators=(",", ":")).encode("utf-8")
emit("    canonical payload, bytes                  : %d" % len(payload))
emit("    canonical payload, sha256                 : %s"
     % hashlib.sha256(payload).hexdigest())
emit()

# ---------------------------------------------------------------- S2
kept_json, kept_owners_json = write_set(kept, kept_owners, "r82_subtracted")

emit("S2  THE RE-KEY AND ITS TWO CONTROLS")
emit()
# A reading the SPEC does not order, printed because the identity below is otherwise
# unexplained: the two trees carry the same bytes everywhere the ruled set looks.
diff_paths = []
for top in ("packages", "apps", "tests"):
    for root, _dirs, files in os.walk(os.path.join(TIP, top)):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), TIP)
            a = os.path.join(BASE, rel)
            b = os.path.join(TIP, rel)
            if not os.path.exists(a):
                diff_paths.append(rel)
            elif open(a, "rb").read() != open(b, "rb").read():
                diff_paths.append(rel)
emit("    paths under packages/, apps/ or tests/ that DIFFER between BASE and TIP : %d"
     % len(diff_paths))
for rel in sorted(diff_paths):
    emit("        %s" % rel)
emit()

rekey_out = {}
for tag, tree in (("tip", TIP), ("shift", SHIFT), ("delete", DELETE)):
    out = os.path.join(SCRATCH, "r82_rekey_" + tag + ".json")
    emit("    the re-key stage, BASE to %s" % tag.upper())
    run([sys.executable, "-B", REKEY, BASE, tree, kept_json, kept_owners_json, out],
        "re-key " + tag)
    rekey_out[tag] = out
    emit()

tip_sites = load_sites(rekey_out["tip"])
emit("    CROSS-CHECK re-key BASE to TIP equals the subtracted set as a SET : %s"
     % (set(tip_sites) == set(kept)))
emit("    CROSS-CHECK re-key BASE to TIP equals the subtracted set IN ORDER : %s"
     % (tip_sites == kept))
emit()

del_sites = load_sites(rekey_out["delete"])
del_owners = load_owners(rekey_out["delete"].replace(".json", "_owners.json"))
emit("    the DELETE set against the TIP set, as sets")
emit("        sites in both                        : %d"
     % len(set(tip_sites) & set(del_sites)))
emit("        in TIP and not in DELETE             : %d"
     % len(set(tip_sites) - set(del_sites)))
for k in sorted(set(tip_sites) - set(del_sites)):
    emit("            %s" % key_str(k))
emit("        in DELETE and not in TIP             : %d"
     % len(set(del_sites) - set(tip_sites)))
for k in sorted(set(del_sites) - set(tip_sites)):
    emit("            %s" % key_str(k))
emit()

tip_src = open(os.path.join(TIP, MUTATED), encoding="utf-8").read().split("\n")
del_src = open(os.path.join(DELETE, MUTATED), encoding="utf-8").read().split("\n")
pairs = [(a, b) for a, b in zip(tip_sites, del_sites) if a[0] == MUTATED]
relocated = [(a, b) for a, b in pairs if tip_src[a[1] - 1] == del_src[b[1] - 1]]
rebound = [(a, b) for a, b in pairs if tip_src[a[1] - 1] != del_src[b[1] - 1]]
emit("    the ruled sites of the mutated file, partitioned")
emit("        the mutated file                     : %s" % MUTATED)
emit("        its ruled sites in the set           : %d" % len(pairs))
emit("        merely RE-LOCATED, statement text unchanged : %d" % len(relocated))
emit("        RE-BOUND to a different statement           : %d" % len(rebound))
emit("        CROSS-CHECK %d + %d = %d against %d : %s"
     % (len(relocated), len(rebound), len(relocated) + len(rebound), len(pairs),
        len(relocated) + len(rebound) == len(pairs)))
for a, b in sorted(rebound):
    emit("        RE-BOUND")
    emit("            old coordinates at TIP           : %d:%d .%s" % (a[1], a[2], a[3]))
    emit("            new coordinates at DELETE        : %d:%d .%s" % (b[1], b[2], b[3]))
    emit("            old source line                  : %s" % tip_src[a[1] - 1])
    emit("            new source line                  : %s" % del_src[b[1] - 1])
    emit("            owner carried across by the map  : %s"
         % del_owners.get(b, "(none)"))
emit()

# ---------------------------------------------------------------- S3
emit("S3  THE SHIPPED OWNER CHECK")
emit()
# The first run is over the CORRECTED set at BASE and is not ordered by the SPEC. It is
# here so the sentence "the subtraction took only refused sites" is a reading of two
# runs rather than a claim: without a before, the after decides nothing.
emit("    the owner check over the CORRECTED set at BASE, the BEFORE reading")
run([sys.executable, "-B", OWNER, BASE, CORRECTED, OWNERS], "owner corrected")
emit()
for tag, tree in (("TIP", TIP), ("DELETE", DELETE)):
    out = rekey_out[tag.lower()]
    emit("    the owner check over the re-keyed subtracted set at %s" % tag)
    run([sys.executable, "-B", OWNER, tree, out, out.replace(".json", "_owners.json")],
        "owner " + tag)
    emit()

# ---------------------------------------------------------------- S4
emit("S4  THE SET BY FILE")
emit()
by_file = {}
by_attr = {}
for p, _ln, _col, attr in tip_sites:
    by_file[p] = by_file.get(p, 0) + 1
    by_attr[attr] = by_attr.get(attr, 0) + 1
emit("    distinct files                            : %d" % len(by_file))
emit("    ruled sites                               : %d" % len(tip_sites))
for attr in sorted(by_attr):
    emit("    sites with attribute .%-18s : %d" % (attr, by_attr[attr]))
emit("    CROSS-CHECK the attribute counts sum to   : %d  against %d : %s"
     % (sum(by_attr.values()), len(tip_sites),
        sum(by_attr.values()) == len(tip_sites)))
emit()
emit("    one line per file, SORTED BY PATH")
for p in sorted(by_file):
    emit("        %5d  %s" % (by_file[p], p))
```

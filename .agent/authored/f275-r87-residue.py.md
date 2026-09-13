# F275 R87 — the residue instrument over pinned full-suite transcripts

This is the instrument SPEC I of the round 87 block orders. It reads three full-suite
transcripts the reviewer took — an unflipped CONTROL, a FLIPPED run with one-line
tracebacks, and a FLIPPED run with short tracebacks — and prints which failures the flip
alone causes and where they raise. Its stdout is the body of the round's artefact.

It is carried in a `.md` rather than a `.py` on purpose: `tests/orchestration/test_ci_budgets.py`
counts every `.py` file `ruff check .` scans, and a scratch instrument committed under
`.agent/` is not production code. The carrier holds exactly one `python` fence and the
fence is extracted, never retyped.

NO COMMIT ID AND NO REPOSITORY PATH IS EMBEDDED. The three transcripts and the path prefix
of the flipped tree inside them arrive as arguments. Nothing printed carries a wall-clock
value, and every listing over a set is sorted, so two runs agree byte for byte.

Usage:

    python3 -B <extracted fence> CONTROL FLIPPED FLIPPED_SHORT PREFIX

What it prints:

- I1 for each transcript, pytest's final tally line with its ` in <seconds>s (<clock>)`
  suffix removed, and the count of distinct node ids on lines matching
  `^(FAILED|ERROR) (\S+)`.
- I2 the flip-only set (FLIPPED minus CONTROL) and the control-only set by count, and the
  symmetric difference of the two flipped transcripts' sets listed by node id.
- I3 over FLIPPED_SHORT, the sections between the first `= ERRORS =` or `= FAILURES =`
  heading and the `short test summary info` line, split at lines matching
  `^_+ (.+?) _+$`, and their count.
- I4 the count per exception class, the count per (deepest in-tree frame `::` function,
  class) pair for every pair of count 3 or more, the count per production frame path, and
  the totals of production, test and unattributable deepest frames, with a cross-check
  that the three totals sum to the section count.

Definitions, stated beside the readings they produce:

- A section's EXCEPTION CLASS is group 1 of its LAST line matching `^E   (\S+?): (.*)$`,
  else `<none>`.
- Its DEEPEST IN-TREE FRAME is the last line matching `^(\S+\.py):(\d+): in (\S+)$` whose
  path, with PREFIX stripped and then one `/` stripped when PREFIX is present, does not
  start with `/` and does not contain `site-packages`. A section with none is
  UNATTRIBUTABLE. A frame is PRODUCTION when its relative path does not start with `tests/`.
- A tally line is the LAST line that is a comma-separated run of `<n> <word>` counts
  followed by ` in <seconds>s (<clock>)`; only the counts are printed.
- Every count listing is sorted by count descending and then by key ascending, a total
  order, so equal counts cannot change places between runs.

```python
"""F275 R87 — classify pinned full-suite transcripts into the failures the flip alone causes.

Arguments: CONTROL FLIPPED FLIPPED_SHORT PREFIX. Every tree path is an argument; nothing
here names a commit or a checkout. Stdout carries no wall-clock value, and every listing
over a set is sorted, so two runs over the same bytes agree byte for byte.
"""
import re
import sys
from collections import Counter

CONTROL, FLIPPED, FLIPPED_SHORT, PREFIX = sys.argv[1:5]

NODE = re.compile(r"^(FAILED|ERROR) (\S+)")
# pytest's tally, with its " in <seconds>s (<clock>)" suffix; the suffix is the only
# wall-clock value in a transcript and it is cut before anything is printed.
TALLY = re.compile(r"^(\d+ (?:failed|passed|skipped|errors?|warnings?|deselected|xfailed|xpassed)"
                   r"(?:, \d+ [a-z]+)*) in [0-9.]+s \([0-9:.]+\)$")
HEADER = re.compile(r"^_+ (.+?) _+$")
EXC = re.compile(r"^E   (\S+?): (.*)$")
FRAME = re.compile(r"^(\S+\.py):(\d+): in (\S+)$")


def read_lines(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def tally(lines):
    found = [m.group(1) for m in (TALLY.match(ln) for ln in lines) if m]
    return found[-1] if found else "<no tally line>"


def node_set(lines):
    return {m.group(2) for m in (NODE.match(ln) for ln in lines) if m}


def ranked(counter):
    """A count listing, sorted by count descending and then by key ascending."""
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))


def relative(path):
    """The frame path with the tree prefix and one slash stripped, when the prefix is present."""
    if path.startswith(PREFIX):
        path = path[len(PREFIX):]
        if path.startswith("/"):
            path = path[1:]
    return path


def sections(lines):
    """Every section between the first ERRORS or FAILURES heading and the summary line."""
    start = None
    for i, ln in enumerate(lines):
        if re.search(r"= ERRORS =|= FAILURES =", ln):
            start = i
            break
    if start is None:
        return []
    end = len(lines)
    for i in range(start, len(lines)):
        if "short test summary info" in lines[i]:
            end = i
            break
    out = []
    for ln in lines[start + 1:end]:
        m = HEADER.match(ln)
        if m:
            out.append((m.group(1), []))
        elif out:
            out[-1][1].append(ln)
    return out


def classify(body):
    exc = "<none>"
    frame = None
    for ln in body:
        m = EXC.match(ln)
        if m:
            exc = m.group(1)
        m = FRAME.match(ln)
        if m:
            rel = relative(m.group(1))
            if not rel.startswith("/") and "site-packages" not in rel:
                frame = (rel, m.group(3))
    return exc, frame


def main():
    names = (("control", CONTROL), ("flipped", FLIPPED), ("flipped short", FLIPPED_SHORT))
    texts = {label: read_lines(path) for label, path in names}
    sets = {label: node_set(texts[label]) for label, _ in names}

    print("I1  THE TALLIES AND THE BAD NODES")
    for label, _ in names:
        print("    %-14s tally: %s" % (label, tally(texts[label])))
        print("    %-14s distinct FAILED/ERROR node ids: %d" % (label, len(sets[label])))
    print("")

    print("I2  THE SETS")
    flip_only = sets["flipped"] - sets["control"]
    control_only = sets["control"] - sets["flipped"]
    print("    flip-only (flipped minus control): %d" % len(flip_only))
    print("    control-only (control minus flipped): %d" % len(control_only))
    sym = sorted(sets["flipped"] ^ sets["flipped short"])
    print("    symmetric difference of the two flipped transcripts: %d" % len(sym))
    for node in sym:
        side = "flipped" if node in sets["flipped"] else "flipped short"
        print("        %s  (only in %s)" % (node, side))
    print("")

    print("I3  THE SECTIONS OF THE SHORT-TRACEBACK FLIPPED TRANSCRIPT")
    secs = sections(texts["flipped short"])
    by_class = Counter()
    by_pair = Counter()
    by_prod = Counter()
    totals = Counter()
    for _title, body in secs:
        exc, frame = classify(body)
        by_class[exc] += 1
        if frame is None:
            totals["unattributable"] += 1
            continue
        rel, func = frame
        by_pair[(rel + "::" + func, exc)] += 1
        if rel.startswith("tests/"):
            totals["test"] += 1
        else:
            totals["production"] += 1
            by_prod[rel] += 1
    print("    sections: %d" % len(secs))
    print("")

    print("I4  THE CLASSIFICATION")
    print("    by exception class, count descending then name:")
    for exc, n in ranked(by_class):
        print("        %4d  %s" % (n, exc))
    print("    by (deepest in-tree frame, exception class), pairs of count 3 or more:")
    for (where, exc), n in sorted(by_pair.items(), key=lambda kv: (-kv[1], kv[0])):
        if n >= 3:
            print("        %4d  %s  %s" % (n, where, exc))
    print("    by production frame path, count descending then path:")
    for rel, n in ranked(by_prod):
        print("        %4d  %s" % (n, rel))
    print("    deepest frames: production %d, test %d, unattributable %d"
          % (totals["production"], totals["test"], totals["unattributable"]))
    print("    CROSS-CHECK %d + %d + %d = %d sections: %s"
          % (totals["production"], totals["test"], totals["unattributable"],
             sum(totals.values()), sum(totals.values()) == len(secs)))


main()
```

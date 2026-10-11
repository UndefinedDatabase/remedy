"""DECISION F205 D8: resolve the two conflicts of merging origin/main 4a24150a0 into the branch.

Run from the repository root while `git merge --no-ff --no-commit origin/main` stands with exactly
one conflict region in each of the two files below. Both sides appended text at the same place:

- `.agent/decisions.md`: main's four DECISIONs amend1010-cadence-guards D1 to D4 come first, then
  the branch's DECISIONs F205 D1 to D8, so the operator's answer D8 stays the file's last entry; one
  empty line separates the two blocks, as it separates every DECISION.
- `.agent/live_review.md`: the branch's Gate entries F205 R4 to R9 come first, then one empty line,
  then main's eight registrations R-1236 to R-1243, byte for byte. Main's side also still holds the
  line `Gate: F302 R7 ...`, which the branch's own ledger rotation moved into
  `.agent/live_review_archive.md` (round 10, commit C2); it is dropped here and nowhere else, and the
  script refuses unless the archive holds that exact line.

The script refuses, and writes nothing, on any other shape.
"""
from __future__ import annotations

from pathlib import Path

OURS, SEP, THEIRS = "<<<<<<< HEAD", "=======", ">>>>>>> origin/main"


def _split(path: Path) -> tuple[list[str], list[str], list[str], list[str]]:
    rows = path.read_text(encoding="utf-8").split("\n")
    starts = [i for i, r in enumerate(rows) if r == OURS]
    seps = [i for i, r in enumerate(rows) if r == SEP]
    ends = [i for i, r in enumerate(rows) if r == THEIRS]
    if not (len(starts) == len(seps) == len(ends) == 1 and starts[0] < seps[0] < ends[0]):
        raise SystemExit(f"REFUSED {path}: not exactly one conflict region")
    a, b, c = starts[0], seps[0], ends[0]
    return rows[:a], rows[a + 1:b], rows[b + 1:c], rows[c + 1:]


def main() -> int:
    archive = Path(".agent/live_review_archive.md").read_text(encoding="utf-8").split("\n")
    out: dict[Path, str] = {}

    path = Path(".agent/decisions.md")
    head, ours, theirs, tail = _split(path)
    if not (ours[0].startswith("## DECISION F205 D1 ") and theirs[0].startswith("## DECISION amend1010-cadence-guards D1 ")):
        raise SystemExit(f"REFUSED {path}: unexpected block heads")
    if ours[-1] == "" or theirs[-1] == "" or head[-1] != "" or tail != [""]:
        raise SystemExit(f"REFUSED {path}: unexpected block edges")
    out[path] = "\n".join(head + theirs + [""] + ours + tail)

    path = Path(".agent/live_review.md")
    head, ours, theirs, tail = _split(path)
    if not (ours[0].startswith("Gate: F205 R4 ") and ours[-1].startswith("Gate: F205 R9 ")):
        raise SystemExit(f"REFUSED {path}: unexpected ours block")
    if not (theirs[0].startswith("Gate: F302 R7 ") and theirs[0] in archive):
        raise SystemExit(f"REFUSED {path}: main's first line is not the archived F302 R7 gate")
    regs = theirs[1:]
    want = [f"- R-{n} — " for n in range(1236, 1244)]
    if [r[: len(w)] for r, w in zip(regs, want)] != want or len(regs) != 8:
        raise SystemExit(f"REFUSED {path}: main's registrations are not R-1236 to R-1243 in order")
    if head[-1] != "" or tail != [""]:
        raise SystemExit(f"REFUSED {path}: unexpected block edges")
    out[path] = "\n".join(head + ours + [""] + regs + tail)

    for p, text in out.items():
        p.write_text(text, encoding="utf-8")
        print(f"resolved {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

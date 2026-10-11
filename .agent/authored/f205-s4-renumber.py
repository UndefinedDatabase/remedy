"""DECISION F205 D8: renumber the branch's two repaired findings, R-1236 to R-1244 and R-1237 to R-1245.

Run from the repository root at the base commit 710614217. Every (path, line) below is the one place
the branch names one of the two findings, with the number of each id the line must hold before the
edit. The script refuses, and writes nothing, when any line holds a different count; it never touches
the operator's DECISION F205 D8, the handoff or any copy under .agent/authored, which keep the old
numbers as history.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NEW = {"R-1236": "R-1244", "R-1237": "R-1245"}
ID = re.compile(r"\bR-123[67]\b")

# path -> {1-based line number: (count of R-1236, count of R-1237)}
SITES: dict[str, dict[int, tuple[int, int]]] = {
    ".agent/live_review_archive.md": {7758: (1, 0), 7760: (1, 0), 7762: (0, 1), 7764: (0, 1)},
    ".agent/live_review.md": {198: (1, 0), 200: (0, 1)},
    ".agent/decisions.md": {28912: (1, 0), 28914: (1, 0), 28916: (1, 0)},
    "docs/agents/planner_reviewer_prompt.md": {575: (1, 0), 578: (0, 1)},
    "docs/roadmap/STATUS.md": {245: (1, 1)},
    "docs/roadmap/features/T13_F205.md": {67: (1, 0)},
    "packages/orchestration/public_api_writes.py": {112: (1, 0)},
    "tests/orchestration/test_mission_contract.py": {654: (0, 1)},
    "tests/ui_server/test_public_api.py": {1638: (1, 0)},
}


def main() -> int:
    edited: dict[Path, bytes] = {}
    for rel, lines in SITES.items():
        path = Path(rel)
        rows = path.read_bytes().decode("utf-8").split("\n")
        for number, (want36, want37) in lines.items():
            row = rows[number - 1]
            got = (row.count("R-1236"), row.count("R-1237"))
            if got != (want36, want37) or len(ID.findall(row)) != want36 + want37:
                print(f"REFUSED {rel}:{number}: holds {got}, expected {(want36, want37)}")
                return 1
            rows[number - 1] = ID.sub(lambda m: NEW[m.group(0)], row)
        edited[path] = "\n".join(rows).encode("utf-8")
    for path, data in edited.items():
        path.write_bytes(data)
        print(f"edited {path}")
    print(f"renumbered {sum(sum(a + b for a, b in v.values()) for v in SITES.values())} ids in {len(edited)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

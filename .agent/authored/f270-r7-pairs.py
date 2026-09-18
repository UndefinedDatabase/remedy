"""F270 round 7 closure edits as FROM/TO pairs, applied to a tree given as argv[1].

The STATUS line, the README counters and paragraph, and SU-021's `consumed_by`. Each FROM must
occur exactly once before, each TO exactly once after. Also the reviewer's dry run.
"""
import sys
from pathlib import Path

S = Path("/home/decodeux/Repos/remedy/.remedy-wt/f270-r7")
TREE = Path(sys.argv[1])

STATUS_FROM = "- [~] F270 — History apply: one commit per task, merge on demand\n"
STATUS_TO = (S / "status_line.txt").read_text()

README_PAIRS = [
    ("83 of 281 registered items accepted.", "84 of 281 registered items accepted."),
    ("| 2 | Minimal Self-Build Runtime | 25 | 34 |", "| 2 | Minimal Self-Build Runtime | 26 | 34 |"),
    ("starts a follow-up mission carrying the unmet criteria).\n\n"
     "Accepted in Tier 3 so far:",
     "starts a follow-up mission carrying the unmet criteria),\n"
     + (S / "readme_paragraph.txt").read_text()
     + "\nAccepted in Tier 3 so far:"),
]

QUEUE_FROM = ('"consumed_by": "",\n'
              '      "provenance": "generated (self-use-generator tier 1, ledger scan, R-0445)"\n'
              '    }\n'
              '  ]')
QUEUE_TO = QUEUE_FROM.replace('"consumed_by": "",', '"consumed_by": "F270",')


def apply(path: Path, pairs) -> None:
    text = path.read_text()
    for old, new in pairs:
        assert text.count(old) == 1, (path, old[:60], text.count(old))
        text = text.replace(old, new)
    for _old, new in pairs:
        assert text.count(new) == 1, (path, new[:60], text.count(new))
    path.write_text(text)
    print("applied", path, len(pairs), "pair(s)")


apply(TREE / "docs/roadmap/STATUS.md", [(STATUS_FROM, STATUS_TO)])
apply(TREE / "README.md", README_PAIRS)
apply(TREE / "scripts/self_use_queue.json", [(QUEUE_FROM, QUEUE_TO)])

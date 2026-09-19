"""F273 round 25 closure edits as FROM/TO pairs, applied to a tree: `pairs.py reg|close <tree>`.

`reg` registers F282 (amend0911-feedback rule B): its feature file, its STATUS line after F263,
the TOTAL_FEATURES pin with its comment, and the README's registered count and Tier 2 total.
`close` is F273's closure edit: its STATUS line, the README's accepted count, Tier 2 done count
and paragraph, and SU-023's `consumed_by`. Each FROM must occur exactly once before, each TO
exactly once after. Also the reviewer's dry run.
"""
import sys
from pathlib import Path

S = Path("/home/decodeux/Repos/remedy/.remedy-wt/f273-r25")
MODE, TREE = sys.argv[1], Path(sys.argv[2])

F263 = "- [ ] F263 — Human-change absorption (absorb)\n"
REG = {
    "docs/roadmap/STATUS.md": [(F263, F263 + "- [ ] F282 — Findings paydown v2\n")],
    "tests/docs/test_docs_consistency.py": [(
        "#: placed it directly after F280; see T2_F281.md.\nTOTAL_FEATURES = 281\n",
        "#: placed it directly after F280; see T2_F281.md. One more, F282 (findings\n"
        "#: paydown v2), was registered on 2026-09-19 by F273's closure under operator\n"
        "#: amendment amend0911-feedback rule B and placed after F263, the fifth\n"
        "#: unaccepted line below F273; see T2_F282.md.\nTOTAL_FEATURES = 282\n",
    )],
    "README.md": [
        ("85 of 281 registered items accepted.", "85 of 282 registered items accepted."),
        ("| 2 | Minimal Self-Build Runtime | 27 | 34 |", "| 2 | Minimal Self-Build Runtime | 27 | 35 |"),
    ],
}
F271_TAIL = "replacing is deleting; and five unreached modules are deleted),\n"
CLOSE = {
    "docs/roadmap/STATUS.md": [("- [~] F273 — Findings paydown v1\n", (S / "status_line.txt").read_text())],
    "README.md": [
        ("85 of 282 registered items accepted.", "86 of 282 registered items accepted."),
        ("| 2 | Minimal Self-Build Runtime | 27 | 35 |", "| 2 | Minimal Self-Build Runtime | 28 | 35 |"),
        (F271_TAIL + "F045 loop definitions,",
         F271_TAIL + (S / "readme_paragraph.txt").read_text() + "F045 loop definitions,"),
    ],
    "scripts/self_use_queue.json": [(
        '"consumed_by": "",\n'
        '      "provenance": "generated (self-use-generator tier 1, ledger scan, R-0499)"\n',
        '"consumed_by": "F273",\n'
        '      "provenance": "generated (self-use-generator tier 1, ledger scan, R-0499)"\n',
    )],
}


def apply(path: Path, pairs) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        assert text.count(old) == 1, (path, old[:60], text.count(old))
        text = text.replace(old, new)
    for _old, new in pairs:
        assert text.count(new) == 1, (path, new[:60], text.count(new))
    path.write_text(text, encoding="utf-8")
    print("applied", path, len(pairs), "pair(s)")


if MODE == "reg":
    target = TREE / "docs/roadmap/features/T2_F282.md"
    assert not target.exists(), target
    target.write_bytes((S / "T2_F282.md").read_bytes())
    print("wrote", target)
    for rel, pairs in REG.items():
        apply(TREE / rel, pairs)
elif MODE == "close":
    for rel, pairs in CLOSE.items():
        apply(TREE / rel, pairs)
else:
    raise SystemExit(f"unknown mode {MODE!r}")

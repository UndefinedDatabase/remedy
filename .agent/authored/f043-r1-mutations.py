#!/usr/bin/env python3
"""F043 R1's mutation tool (G5, the red proofs).

Each mutation below edits ONE production file inside a disposable worktree, asserting its FROM
text occurs there exactly once, runs the named check (the round's three vitest files, or the
render harness), restores the file's original bytes, and reports whether the check actually went
red. An unmutated control of both checks runs first and last, so a control failure — not the
mutation — never masquerades as a caught mutation. Never run against the primary checkout: the
caller passes a disposable worktree path, and this tool only ever edits files under it.

Usage: python3 -B f043-r1-mutations.py <worktree path>
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
VITEST_CONFIG = PRIMARY / "apps" / "ui" / "vitest.config.ts"
VITEST_FILES = [
    "src/api/terminology.test.ts",
    "src/api/terminologyAudit.test.ts",
    "src/components/term/termAudit.test.ts",
]

TERMINOLOGY = "apps/ui/src/api/terminology.ts"
TERMINOLOGY_AUDIT = "apps/ui/src/api/terminologyAudit.ts"
TERM_TSX = "apps/ui/src/components/term/Term.tsx"
LIVE_STATUS_PILL = "apps/ui/src/components/panels/LiveStatusPill.tsx"

MUTATIONS = [
    {
        "id": "t1",
        "label": "t1 termEntry answers TERM_CATALOG[key] ?? null",
        "file": TERMINOLOGY,
        "check": "vitest",
        "from": 'Object.prototype.hasOwnProperty.call(TERM_CATALOG, key) ? TERM_CATALOG[key] : null',
        "to": "TERM_CATALOG[key] ?? null",
    },
    {
        "id": "t2",
        "label": "t2 status.delayed anchor reads quietly in place of visibly",
        "file": TERMINOLOGY,
        "check": "vitest",
        "from": "visibly",
        "to": "quietly",
    },
    {
        "id": "a1",
        "label": "a1 collectDataTerms returns its values unsorted",
        "file": TERMINOLOGY_AUDIT,
        "check": "vitest",
        "from": "return [...found].sort();",
        "to": "return [...found];",
    },
    {
        "id": "a2",
        "label": "a2 collectDataTerms drops the white space required before data-term=",
        "file": TERMINOLOGY_AUDIT,
        "check": "vitest",
        "from": 'const DATA_TERM_ATTR = /\\sdata-term="([^"]*)"/g;',
        "to": 'const DATA_TERM_ATTR = /data-term="([^"]*)"/g;',
    },
    {
        "id": "a3",
        "label": "a3 auditTermUse returns dead unsorted",
        "file": TERMINOLOGY_AUDIT,
        "check": "vitest",
        "from": "const dead = [...keySet].filter((key) => !usedSet.has(key)).sort();",
        "to": "const dead = [...keySet].filter((key) => !usedSet.has(key));",
    },
    {
        "id": "c1",
        "label": "c1 Term omits data-term for a key the catalog lacks",
        "file": TERM_TSX,
        "check": "vitest",
        "from": "<span className={styles.term} data-term={term}>{children}</span>;",
        "to": "<span className={styles.term}>{children}</span>;",
    },
    {
        "id": "c2",
        "label": "c2 the pill renders REPLAY without its term",
        "file": LIVE_STATUS_PILL,
        "check": "vitest",
        "from": '<Term term="status.replay">REPLAY</Term>',
        "to": "REPLAY",
    },
    {
        "id": "h1",
        "label": "h1 the tooltip is portalled into the term's own span instead of document.body",
        "file": TERM_TSX,
        "check": "harness",
        "from": "        document.body,",
        "to": "        spanRef.current as Element,",
    },
    {
        "id": "h2",
        "label": "h2 Escape no longer closes the tooltip",
        "file": TERM_TSX,
        "check": "harness",
        "from": 'if (event.key === "Escape" && open) {',
        "to": 'if (false && event.key === "Escape" && open) {',
    },
    {
        "id": "h3",
        "label": "h3 focus starts the hover timer instead of opening at once",
        "file": TERM_TSX,
        "check": "harness",
        "from": "onFocus={() => setOpen(true)}",
        "to": "onFocus={() => setHovering(true)}",
    },
    {
        "id": "h4",
        "label": "h4 TERM_HOVER_DELAY_MS is 0",
        "file": TERM_TSX,
        "check": "harness",
        "from": "export const TERM_HOVER_DELAY_MS = 120;",
        "to": "export const TERM_HOVER_DELAY_MS = 0;",
    },
    {
        "id": "h5",
        "label": "h5 the placement never moves the tooltip above the term",
        "file": TERM_TSX,
        "check": "harness",
        "from": "if (top + tipHeight > height - VIEWPORT_MARGIN) {",
        "to": "if (false) {",
    },
]


def run_vitest(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--root", str(worktree / "apps" / "ui"),
         "--config", str(VITEST_CONFIG), *VITEST_FILES],
        cwd=str(worktree / "apps" / "ui"),
        capture_output=True, text=True, timeout=120,
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_harness(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-B", str(worktree / ".agent" / "authored" / "f043-r1-render_measure.py"), str(worktree)],
        capture_output=True, text=True, timeout=180,
    )
    return proc.returncode, proc.stdout + proc.stderr


def vitest_reading(output: str) -> str:
    match = re.search(r"(\d+) failed", output)
    if match:
        return f"{match.group(1)} failed"
    if re.search(r"\d+ passed", output):
        return "0 failed"
    return "unknown (no pass/fail summary found)"


def harness_reading(output: str) -> str:
    match = re.search(r"RENDER: \d+ of \d+ checks pass", output)
    return match.group(0) if match else "unknown (no RENDER line found)"


def run_control(worktree: Path, label: str) -> bool:
    v_code, v_out = run_vitest(worktree)
    print(f"{label} vitest: exit={v_code} {vitest_reading(v_out)}")
    h_code, h_out = run_harness(worktree)
    print(f"{label} harness: exit={h_code} {harness_reading(h_out)}")
    return v_code == 0 and h_code == 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    all_caught = True
    all_restored = True

    control_before_ok = run_control(worktree, "CONTROL (before)")

    for mutation in MUTATIONS:
        target = worktree / mutation["file"]
        original = target.read_bytes()
        text = original.decode("utf-8")
        occurrences = text.count(mutation["from"])
        if occurrences != 1:
            print(f"{mutation['label']}: FROM text occurs {occurrences} times, expected 1 -- ABORT")
            return 1
        mutated = text.replace(mutation["from"], mutation["to"], 1)
        target.write_bytes(mutated.encode("utf-8"))

        if mutation["check"] == "vitest":
            code, out = run_vitest(worktree)
            reading = vitest_reading(out)
        else:
            code, out = run_harness(worktree)
            reading = harness_reading(out)

        caught = code != 0
        all_caught = all_caught and caught

        target.write_bytes(original)
        restored = target.read_bytes() == original
        all_restored = all_restored and restored

        print(f"{mutation['label']}: exit={code} {reading}")
        print(f"restored byte-identical: {restored}")

    control_after_ok = run_control(worktree, "CONTROL (after)")

    verdict = all_caught and all_restored and control_before_ok and control_after_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {verdict}")
    return 0 if verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())

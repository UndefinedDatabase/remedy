#!/usr/bin/env python3
"""F044 R2's mutation tool (evidence, not product): the round's red proofs.

One entry, `mutations.py <worktree path>`. For each of the thirteen mutations below, it edits the
named production file INSIDE the given worktree (asserting the FROM text occurs there exactly
once), runs the ONE check the mutation names, restores the file's original bytes, and reports the
restore as byte-identical. Every mutation must turn its check red; a mutation that stays green is
reported as green, never papered over. An unmutated control of all three checks runs first and
last, so a red control at either end means the harness itself, not a mutation, is broken.

The three checks:
  vitest  — the primary's vitest binary over the worktree's own apps/ui, the palette's two test
            files (DECISION F044 D2).
  wiring  — the wiring guard, `tests/ui_contracts/test_palette_sheet_wiring.py`, from the
            worktree's own root.
  harness — the round's render harness, copied into the worktree at C1c/C1d, run over the
            worktree itself.

Usage: python3 mutations.py <worktree path>
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
VITEST_CONFIG = PRIMARY / "apps" / "ui" / "vitest.config.ts"


class Mutation:
    def __init__(self, label: str, rel_path: str, from_text: str, to_text: str, check: str):
        self.label = label
        self.rel_path = rel_path
        self.from_text = from_text
        self.to_text = to_text
        self.check = check


MUTATIONS = [
    Mutation(
        "s1 recent rows are listed for a query too",
        "apps/ui/src/api/paletteSheet.ts",
        "if (isBlank) {\n    for (const ref of input.recents) {",
        "if (true) {\n    for (const ref of input.recents) {",
        "vitest",
    ),
    Mutation(
        "s2 rememberPaletteRef keeps a second copy of the chosen ref",
        "apps/ui/src/api/paletteSheet.ts",
        "recents.filter((r) => r !== ref)",
        "recents.filter((r) => true)",
        "vitest",
    ),
    Mutation(
        "s3 readPaletteRecents no longer cuts at the limit",
        "apps/ui/src/api/paletteSheet.ts",
        'return parsed.filter((item): item is string => typeof item === "string").slice(0, PALETTE_RECENT_LIMIT);',
        'return parsed.filter((item): item is string => typeof item === "string");',
        "vitest",
    ),
    Mutation(
        "s4 movePaletteCursor stops at the ends instead of wrapping",
        "apps/ui/src/api/paletteSheet.ts",
        "return (index + delta + count) % count;",
        "return Math.max(0, Math.min(index + delta, count - 1));",
        "vitest",
    ),
    Mutation(
        "s5 the open project is switchable too",
        "apps/ui/src/api/paletteSheet.ts",
        "return projects.filter((project) => project.slug !== activeSlug);",
        "return projects.slice();",
        "vitest",
    ),
    Mutation(
        "s6 highlightPieces no longer clips a range's end to the label",
        "apps/ui/src/api/paletteSheet.ts",
        "const clippedEnd = Math.max(clippedStart, Math.min(end, label.length));",
        "const clippedEnd = Math.max(clippedStart, end);",
        "vitest",
    ),
    Mutation(
        "t1 the tour's sixth step points at terms-button again",
        "apps/ui/src/api/firstRunTour.ts",
        '    target: "command-bar",',
        '    target: "terms-button",',
        "vitest",
    ),
    Mutation(
        "w1 the bar binds window.localStorage without its useMemo",
        "apps/ui/src/components/command/CommandBar.tsx",
        "const storage = useMemo(() => window.localStorage, []);",
        "const storage = window.localStorage;",
        "wiring",
    ),
    Mutation(
        "h1 the sheet is portalled into the bar instead of the page body",
        "apps/ui/src/components/command/PaletteSheet.tsx",
        "document.body,",
        "anchor ?? document.body,",
        "harness",
    ),
    Mutation(
        "h2 a row's mousedown is no longer cancelled",
        "apps/ui/src/components/command/PaletteSheet.tsx",
        "onMouseDown={(event) => event.preventDefault()}",
        "onMouseDown={() => {}}",
        "harness",
    ),
    Mutation(
        "h3 Enter always chooses the first row",
        "apps/ui/src/components/command/CommandBar.tsx",
        "const row = activeIndex >= 0 && activeIndex < rows.length ? rows[activeIndex] : rows[0];",
        "const row = rows[0];",
        "harness",
    ),
    Mutation(
        "h4 the mark's transparent background is dropped",
        "apps/ui/src/components/command/PaletteSheet.module.css",
        "  background: transparent;\n",
        "",
        "harness",
    ),
    Mutation(
        "h5 the sheet's z-index declaration is dropped",
        "apps/ui/src/components/command/PaletteSheet.module.css",
        "  z-index: var(--remedy-z-popover);\n",
        "",
        "harness",
    ),
    Mutation(
        "h6 choosing a row no longer stores the recent refs",
        "apps/ui/src/components/command/CommandBar.tsx",
        "writePaletteRecents(storage, nextRecents);",
        "// writePaletteRecents(storage, nextRecents);",
        "harness",
    ),
]


def run_vitest(worktree: Path) -> tuple[int, str]:
    ui = worktree / "apps" / "ui"
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--root", str(ui), "--config", str(VITEST_CONFIG),
         "src/api/paletteSheet.test.ts", "src/api/firstRunTour.test.ts"],
        cwd=str(ui), capture_output=True, text=True, timeout=120,
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_wiring(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/ui_contracts/test_palette_sheet_wiring.py"],
        cwd=str(worktree), capture_output=True, text=True, timeout=60,
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_harness(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-B", str(worktree / ".agent" / "authored" / "f044-r2-render_measure.py"), str(worktree)],
        capture_output=True, text=True, timeout=180,
    )
    return proc.returncode, proc.stdout + proc.stderr


CHECKS = {"vitest": run_vitest, "wiring": run_wiring, "harness": run_harness}


def vitest_failed_count(output: str) -> int:
    m = re.search(r"Tests\s+(\d+) failed", output)
    return int(m.group(1)) if m else 0


def pytest_failed_count(output: str) -> int:
    m = re.search(r"(\d+) failed", output)
    return int(m.group(1)) if m else 0


def harness_summary(output: str) -> str:
    lines = output.splitlines()
    render_line = next((l for l in lines if l.startswith("RENDER:")), "RENDER: (no line printed)")
    fails = [l for l in lines if l.startswith("FAIL ")]
    return f"{render_line} | failing=[{'; '.join(fails)}]"


def summarize(check: str, exit_code: int, output: str) -> str:
    if check == "vitest":
        return f"vitest failed={vitest_failed_count(output)}"
    if check == "wiring":
        return f"wiring failed={pytest_failed_count(output)}"
    return harness_summary(output)


def run_control(worktree: Path, label: str) -> bool:
    ok = True
    for check_name, runner in CHECKS.items():
        code, output = runner(worktree)
        passed = code == 0
        ok = ok and passed
        print(f"CONTROL ({label}) {check_name}: exit={code} pass={passed} {summarize(check_name, code, output)}")
    return ok


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    control_before = run_control(worktree, "before")

    all_caught = True
    for mutation in MUTATIONS:
        target = worktree / mutation.rel_path
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(mutation.from_text)
        if occurrences != 1:
            print(f"{mutation.label}: FROM text occurs {occurrences} times (expected 1) — ABORTING")
            return 1
        mutated_text = original_text.replace(mutation.from_text, mutation.to_text, 1)
        target.write_bytes(mutated_text.encode("utf-8"))

        runner = CHECKS[mutation.check]
        code, output = runner(worktree)
        caught = code != 0
        all_caught = all_caught and caught

        target.write_bytes(original)
        restored = target.read_bytes()
        identical = restored == original

        print(
            f"{mutation.label} [{mutation.check}]: exit={code} caught={caught} "
            f"{summarize(mutation.check, code, output)} restored byte-identical: {identical}"
        )
        if not identical:
            print(f"{mutation.label}: RESTORE FAILED — ABORTING")
            return 1

    control_after = run_control(worktree, "after")

    result = all_caught and control_before and control_after
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""F044 R4's mutation tool (evidence, not product): the round's red proofs.

One entry, `mutations.py <worktree path>`. For each of the ten mutations below, it edits the
named production file INSIDE the given worktree (asserting the FROM text occurs there exactly
once), runs the ONE check the mutation names, restores the file's original bytes, and reports the
restore as byte-identical. Every mutation must turn its check red; a mutation that stays green is
reported as green, never papered over. An unmutated control of all three checks runs first and
last, so a red control at either end means the harness itself, not a mutation, is broken.

The three checks:
  vitest  — the primary's vitest binary over the worktree's own apps/ui, the round's two pure-rule
            test files (DECISION F044 D4): paletteSheet.test.ts and firstRunTour.test.ts.
  wiring  — the wiring guard, `tests/ui_contracts/test_palette_sheet_wiring.py`, from the
            worktree's own root.
  harness — the round's render harness, copied into the worktree at C1d, run over the worktree
            itself.

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

VITEST_TEST_FILES = [
    "src/api/paletteSheet.test.ts",
    "src/api/firstRunTour.test.ts",
]


class Mutation:
    def __init__(self, label: str, rel_path: str, from_text: str, to_text: str, check: str):
        self.label = label
        self.rel_path = rel_path
        self.from_text = from_text
        self.to_text = to_text
        self.check = check


MUTATIONS = [
    Mutation(
        "a1 the Ask row comes only when no other row was built, even for a question",
        "apps/ui/src/api/paletteSheet.ts",
        'route.kind === "chat" || builtRows.length === 0',
        "builtRows.length === 0",
        "vitest",
    ),
    Mutation(
        "a2 the Ask row comes for every line that is not blank",
        "apps/ui/src/api/paletteSheet.ts",
        'route.kind === "chat" || builtRows.length === 0',
        "true",
        "vitest",
    ),
    Mutation(
        "a3 the Ask row's text keeps the query as typed",
        "apps/ui/src/api/paletteSheet.ts",
        'const text = query.replace(/\\s+/g, " ").trim();',
        "const text = query;",
        "vitest",
    ),
    Mutation(
        "t1 the sixth tour step keeps its old title",
        "apps/ui/src/api/firstRunTour.ts",
        'title: "Ask or jump to anything",',
        'title: "Jump to anything",',
        "vitest",
    ),
    Mutation(
        "w1 the chat sheet mounts the tab without the question",
        "apps/ui/src/components/command/ChatSheet.tsx",
        " initialQuestion={question} />",
        " />",
        "wiring",
    ),
    Mutation(
        "h1 the tab marks the initial question asked without asking it",
        "apps/ui/src/components/graph/EvidenceChatTab.tsx",
        "      askedInitial.current = true;\n      void ask(initialQuestion);",
        "      askedInitial.current = true;",
        "harness",
    ),
    Mutation(
        "h2 the scope checkbox is shown with no task",
        "apps/ui/src/components/graph/EvidenceChatTab.tsx",
        "{!projectOnly && (",
        "{true && (",
        "harness",
    ),
    Mutation(
        "h3 the chat sheet's z-index declaration is dropped",
        "apps/ui/src/components/command/ChatSheet.module.css",
        "  z-index: var(--remedy-z-overlay);\n",
        "",
        "harness",
    ),
    Mutation(
        "h4 Escape no longer closes the chat sheet",
        "apps/ui/src/components/command/ChatSheet.tsx",
        'if (event.key === "Escape") onClose();',
        "if (false) onClose();",
        "harness",
    ),
    Mutation(
        "h5 BAR_PLACEHOLDER goes back to round 3's words",
        "apps/ui/src/components/command/CommandBar.tsx",
        """export const BAR_PLACEHOLDER = 'Ask your agent or jump to anything (e.g., "improve error handling")';""",
        """export const BAR_PLACEHOLDER = 'Jump to anything (e.g., "error handling")';""",
        "harness",
    ),
]


def run_vitest(worktree: Path) -> tuple[int, str]:
    ui = worktree / "apps" / "ui"
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--root", str(ui), "--config", str(VITEST_CONFIG), *VITEST_TEST_FILES],
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
        [sys.executable, "-B", str(worktree / ".agent" / "authored" / "f044-r4-render_measure.py"), str(worktree)],
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

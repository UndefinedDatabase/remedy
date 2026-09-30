#!/usr/bin/env python3
"""F044 R3's mutation tool (evidence, not product): the round's red proofs.

One entry, `mutations.py <worktree path>`. For each of the sixteen mutations below, it edits the
named production file INSIDE the given worktree (asserting the FROM text occurs there exactly
once), runs the ONE check the mutation names, restores the file's original bytes, and reports the
restore as byte-identical. Every mutation must turn its check red; a mutation that stays green is
reported as green, never papered over. An unmutated control of all four checks runs first and
last, so a red control at either end means the harness itself, not a mutation, is broken.

The four checks:
  vitest      — the primary's vitest binary over the worktree's own apps/ui, the round's four
                pure-rule test files (DECISION F044 D3).
  wiring      — the wiring guard, `tests/ui_contracts/test_palette_sheet_wiring.py`, from the
                worktree's own root.
  placeholder — the placeholder guard, `tests/ui_server/test_dashboard_contract.py -k cli_language`,
                from the worktree's own root.
  harness     — the round's render harness, copied into the worktree at C1d, run over the
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

VITEST_TEST_FILES = [
    "src/api/paletteSheet.test.ts",
    "src/api/paletteCommandState.test.ts",
    "src/api/paletteArgs.test.ts",
    "src/api/paletteSend.test.ts",
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
        "m1 the routed command is no longer put first",
        "apps/ui/src/api/paletteSheet.ts",
        "if (routedCommand !== null) {",
        "if (false) {",
        "vitest",
    ),
    Mutation(
        "m2 a reason is read from an inherited key too",
        "apps/ui/src/api/paletteSheet.ts",
        'return Object.prototype.hasOwnProperty.call(commandReasons, command) ? commandReasons[command] : "";',
        'return commandReasons[command] ?? "";',
        "vitest",
    ),
    Mutation(
        "m3 the command rows are not cut at the limit",
        "apps/ui/src/api/paletteSheet.ts",
        "return ordered.slice(0, COMMAND_RESULT_LIMIT).map(({ entry, ranges }) => {",
        "return ordered.map(({ entry, ranges }) => {",
        "vitest",
    ),
    Mutation(
        '"task" mode lists every section',
        "apps/ui/src/api/paletteSheet.ts",
        'if (input.mode === "task") {',
        'if (input.mode === "never") {',
        "vitest",
    ),
    Mutation(
        "m5 an ended job's reason wins over a form entry's",
        "apps/ui/src/api/paletteCommandState.ts",
        'if (entry.flow === "form") return PALETTE_FORM_REASON;\n'
        "  if (facts.ended) return PALETTE_ENDED_REASON;",
        'if (facts.ended) return PALETTE_ENDED_REASON;\n'
        '  if (entry.flow === "form") return PALETTE_FORM_REASON;',
        "vitest",
    ),
    Mutation(
        "m6 a resume is refused while a pause is on its way",
        "apps/ui/src/api/paletteCommandState.ts",
        'return facts.pauseAction === "resume" || facts.pauseAction === "take_back" '
        '? "" : PALETTE_NOT_PAUSED_REASON;',
        'return facts.pauseAction === "resume" ? "" : PALETTE_NOT_PAUSED_REASON;',
        "vitest",
    ),
    Mutation(
        "m7 an optional argument left blank is recorded as \"\"",
        "apps/ui/src/api/paletteArgs.ts",
        'const values = trimmed === "" ? { ...flow.values } : { ...flow.values, [arg.name]: trimmed };',
        "const values = { ...flow.values, [arg.name]: trimmed };",
        "vitest",
    ),
    Mutation(
        "m8 a rerun goes through the card sender",
        "apps/ui/src/api/paletteSend.ts",
        "if (flow.entry.command === RERUN_COMMAND) {",
        "if (false && flow.entry.command === RERUN_COMMAND) {",
        "vitest",
    ),
    Mutation(
        "m9 a rerun that needs confirming omits PALETTE_RERUN_CONFIRM_ELSEWHERE",
        "apps/ui/src/api/paletteSend.ts",
        'return { tone: "warn", sentence: `${view.sentence} ${PALETTE_RERUN_CONFIRM_ELSEWHERE}` };',
        'return { tone: "warn", sentence: view.sentence };',
        "vitest",
    ),
    Mutation(
        "h1 choosing a refused row runs it",
        "apps/ui/src/components/command/CommandBar.tsx",
        'if (row.disabledReason !== "") return;',
        "if (false) return;",
        "harness",
    ),
    Mutation(
        "h2 Escape during a flow no longer cancels it",
        "apps/ui/src/components/command/CommandBar.tsx",
        "      if (flow !== null) {\n        cancelFlow();\n      } else {\n        setOpen(false);",
        "      if (false) {\n        cancelFlow();\n      } else {\n        setOpen(false);",
        "harness",
    ),
    Mutation(
        "h3 the shell's add-task surface does not open the sheet",
        "apps/ui/src/components/shell/RemedyShell.tsx",
        "setAddTaskOpen(true);",
        "setAddTaskOpen(false);",
        "harness",
    ),
    Mutation(
        "h4 the status line is no longer fixed",
        "apps/ui/src/components/command/PaletteSheet.module.css",
        ".status {\n  position: fixed;",
        ".status {\n  position: static;",
        "harness",
    ),
    Mutation(
        "h5 a refused row's opacity is dropped",
        "apps/ui/src/components/command/PaletteSheet.module.css",
        "  opacity: 0.45;\n  cursor: not-allowed;\n}",
        "  cursor: not-allowed;\n}",
        "harness",
    ),
    Mutation(
        "w1 the shell's own <AddTaskSheet mount is renamed away",
        "apps/ui/src/components/shell/RemedyShell.tsx",
        "<AddTaskSheet target=",
        "<AddTaskSheetX target=",
        "wiring",
    ),
    Mutation(
        'w2 BAR_PLACEHOLDER begins "remedy "',
        "apps/ui/src/components/command/CommandBar.tsx",
        """export const BAR_PLACEHOLDER = 'Jump to anything (e.g., "error handling")';""",
        """export const BAR_PLACEHOLDER = 'remedy jump (e.g., "error handling")';""",
        "placeholder",
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


def run_placeholder(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/ui_server/test_dashboard_contract.py", "-k", "cli_language"],
        cwd=str(worktree), capture_output=True, text=True, timeout=60,
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_harness(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-B", str(worktree / ".agent" / "authored" / "f044-r3-render_measure.py"), str(worktree)],
        capture_output=True, text=True, timeout=180,
    )
    return proc.returncode, proc.stdout + proc.stderr


CHECKS = {"vitest": run_vitest, "wiring": run_wiring, "placeholder": run_placeholder, "harness": run_harness}


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
    if check in ("wiring", "placeholder"):
        return f"{check} failed={pytest_failed_count(output)}"
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

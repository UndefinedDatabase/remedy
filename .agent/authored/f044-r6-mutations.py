#!/usr/bin/env python3
"""F044 R6's red-proof tool (evidence, not product).

One entry, `mutations.py <worktree path>`. For each mutation below it edits the named
production file INSIDE that worktree (asserting its FROM text occurs exactly once there), runs
the named check, restores the bytes, and prints one line per mutation: its label, the check's
real exit code, and the failed count (vitest/pytest) or the harness's own `RENDER: <n> of 9`
reading with its failing labels. Runs an unmutated control of every check first and last. Every
mutation is a real behaviour change that must turn its check red; a mutation that stays green is
reported as green, never papered over.

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
    def __init__(self, label: str, path: str, frm: str, to: str, check: str):
        self.label = label
        self.path = path
        self.frm = frm
        self.to = to
        self.check = check  # "vitest" | "wiring" | "harness"


MUTATIONS = [
    Mutation(
        "z1", "apps/ui/src/components/graph/zoomKeys.ts",
        "  const next = forward ? (at + 1) % ids.length : (at - 1 + ids.length) % ids.length;",
        "  const next = forward ? Math.min(at + 1, ids.length - 1) : Math.max(at - 1, 0);",
        "vitest",
    ),
    Mutation(
        "z2", "apps/ui/src/components/graph/zoomKeys.ts",
        "      if (isZoomRunKind(node.kind) && node.parentId === focus.parentId) ids.push(id);",
        "      if (isZoomRunKind(node.kind)) ids.push(id);",
        "vitest",
    ),
    Mutation(
        "z3", "apps/ui/src/components/graph/zoomKeys.ts",
        "    if (found === null && isZoomRunKind(node.kind) && node.parentId === state.focusId) found = id;",
        "    if (isZoomRunKind(node.kind) && node.parentId === state.focusId) found = id;",
        "vitest",
    ),
    Mutation(
        "z4", "apps/ui/src/components/graph/zoomKeys.ts",
        "  if (at === -1) return forward ? ids[0] : ids[ids.length - 1];",
        "  if (at === -1) return ids[0];",
        "vitest",
    ),
    Mutation(
        "h1", "apps/ui/src/components/graph/useZoomKeys.ts",
        '        dispatch({ type: "click", nodeId: step.nodeId });\n        latest.current.onPick(step.nodeId);',
        '        dispatch({ type: "click", nodeId: step.nodeId });',
        "harness",
    ),
    Mutation(
        "h2", "apps/ui/src/components/shell/useHeldHelpKey.ts",
        "        pending.current = null;\n        onTapRef.current();\n      } else if (openRef.current) {",
        "        pending.current = null;\n      } else if (openRef.current) {",
        "harness",
    ),
    Mutation(
        "h3", "apps/ui/src/components/shell/useHeldHelpKey.ts",
        "      openRef.current = true;\n      setShortcutsOpen(true);\n    }, KEYMAP_HOLD_MS);",
        "    }, KEYMAP_HOLD_MS);",
        "harness",
    ),
    Mutation(
        "h4", "apps/ui/src/components/command/KeymapOverlay.module.css",
        "  z-index: var(--remedy-z-overlay);\n",
        "",
        "harness",
    ),
    Mutation(
        "h5", "apps/ui/src/components/graph/useZoomKeys.ts",
        '      const dialogOpen = document.querySelector(\'[role="dialog"]\') !== null;',
        "      const dialogOpen = false;",
        "harness",
    ),
    Mutation(
        "w1", "apps/ui/src/components/command/KeymapOverlay.tsx",
        "{KEYMAP_BINDINGS.map((binding) => (",
        "{KEYMAP_BINDINGS.slice(0, 3).map((binding) => (",
        "wiring",
    ),
]


def run_vitest(worktree: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(VITEST_BIN), "run", "--root", str(worktree / "apps" / "ui"), "--config", str(VITEST_CONFIG),
         "src/components/graph/zoomKeys.test.ts", "src/api/keymap.test.ts"],
        cwd=str(worktree / "apps" / "ui"), capture_output=True, text=True, timeout=120,
    )


def run_wiring(worktree: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/ui_contracts/test_palette_sheet_wiring.py", "tests/ui_contracts/test_semantic_zoom_wiring.py"],
        cwd=str(worktree), capture_output=True, text=True, timeout=120,
    )


def run_harness(worktree: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", str(worktree / ".agent" / "authored" / "f044-r6-render_measure.py"), str(worktree)],
        cwd=str(worktree), capture_output=True, text=True, timeout=180,
    )


def failed_count(output: str) -> int:
    m = re.search(r"(\d+) failed", output)
    return int(m.group(1)) if m else 0


def harness_reading(output: str) -> str:
    fail_lines = [line for line in output.splitlines() if line.startswith("FAIL ")]
    m = re.search(r"RENDER: (\d+) of (\d+) checks pass", output)
    reading = m.group(0) if m else "RENDER: reading not found"
    labels = [line.split(" ", 2)[1] for line in fail_lines]
    return f"{reading} FAILED: {labels}"


def run_check(check: str, worktree: Path) -> tuple[int, str]:
    if check == "vitest":
        proc = run_vitest(worktree)
        out = proc.stdout + proc.stderr
        return proc.returncode, f"failed={failed_count(out)}"
    if check == "wiring":
        proc = run_wiring(worktree)
        out = proc.stdout + proc.stderr
        return proc.returncode, f"failed={failed_count(out)}"
    proc = run_harness(worktree)
    out = proc.stdout + proc.stderr
    return proc.returncode, harness_reading(out)


def print_result(label: str, exit_code: int, detail: str) -> None:
    print(f"{label} exit={exit_code} {detail}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    all_caught = True

    print("-- CONTROL (before), unmutated --")
    for check in ("vitest", "wiring", "harness"):
        exit_code, detail = run_check(check, worktree)
        print_result(f"control-before-{check}", exit_code, detail)
        if exit_code != 0:
            all_caught = False

    print("-- MUTATIONS --")
    for mutation in MUTATIONS:
        target = worktree / mutation.path
        original = target.read_bytes()
        text = original.decode("utf-8")
        occurrences = text.count(mutation.frm)
        assert occurrences == 1, f"{mutation.label}: FROM text occurs {occurrences} times in {mutation.path}, expected 1"
        mutated_text = text.replace(mutation.frm, mutation.to, 1)
        target.write_bytes(mutated_text.encode("utf-8"))
        try:
            exit_code, detail = run_check(mutation.check, worktree)
            print_result(mutation.label, exit_code, detail)
            if exit_code == 0:
                all_caught = False
        finally:
            target.write_bytes(original)
            restored = target.read_bytes() == original
            print(f"restored byte-identical: {restored}")
            if not restored:
                all_caught = False

    print("-- CONTROL (after), unmutated --")
    for check in ("vitest", "wiring", "harness"):
        exit_code, detail = run_check(check, worktree)
        print_result(f"control-after-{check}", exit_code, detail)
        if exit_code != 0:
            all_caught = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_caught}")
    return 0 if all_caught else 1


if __name__ == "__main__":
    raise SystemExit(main())

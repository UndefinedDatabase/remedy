#!/usr/bin/env python3
"""F044 R5's mutation tool (G5's red proofs).

Takes ONE argument, a worktree path. For each of the eleven mutations below it edits the named
production file INSIDE that worktree (asserting its FROM text occurs exactly once there),
runs the named check (vitest, the wiring pytest, or the render harness), restores the file's
original bytes, and reports whether the check caught the mutation (non-zero exit). The primary
is /home/decodeux/Repos/remedy: the vitest binary and its config, and the wiring test's own
`python3 -m pytest` invocation, are read from there, never from the worktree, exactly as G5
specifies. The worktree is expected to already carry a symlink at `apps/ui/node_modules`
pointing at the primary's own, set up by the caller before this tool runs.

Usage: python3 -B f044-r5-mutations.py <worktree path>
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
VITEST_CONFIG = PRIMARY / "apps" / "ui" / "vitest.config.ts"


def run_vitest(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [
            str(VITEST_BIN), "run",
            "--root", str(worktree / "apps" / "ui"),
            "--config", str(VITEST_CONFIG),
            "src/api/keymap.test.ts", "src/api/termSearch.test.ts", "src/components/graph/zoomView.test.ts",
        ],
        cwd=str(worktree / "apps" / "ui"), capture_output=True, text=True, timeout=120,
    )
    out = proc.stdout + proc.stderr
    m = re.search(r"Tests\s+(\d+) failed \| (\d+) passed", out)
    if m:
        detail = f"{m.group(1)} failed, {m.group(2)} passed"
    else:
        m2 = re.search(r"Tests\s+(\d+) passed", out)
        detail = f"{m2.group(1)} passed, 0 failed" if m2 else "UNPARSED: " + out[-400:]
    return proc.returncode, detail


def run_wiring(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/ui_contracts/test_palette_sheet_wiring.py"],
        cwd=str(worktree), capture_output=True, text=True, timeout=60,
    )
    out = proc.stdout + proc.stderr
    m = re.search(r"(\d+) failed(?:, (\d+) passed)?", out)
    if m:
        detail = f"{m.group(1)} failed"
    else:
        m2 = re.search(r"(\d+) passed", out)
        detail = f"{m2.group(1)} passed, 0 failed" if m2 else "UNPARSED: " + out[-400:]
    return proc.returncode, detail


def run_harness(worktree: Path) -> tuple[int, str]:
    script = worktree / ".agent" / "authored" / "f044-r5-render_measure.py"
    proc = subprocess.run(
        [sys.executable, "-B", str(script), str(worktree)],
        capture_output=True, text=True, timeout=200,
    )
    out = proc.stdout + proc.stderr
    m = re.search(r"RENDER: (\d+) of (\d+) checks pass", out)
    failing = re.findall(r"FAIL ([^{]+)\{", out)
    labels = "; failing: " + ", ".join(s.strip() for s in failing) if failing else ""
    if m:
        detail = f"RENDER: {m.group(1)} of {m.group(2)}{labels}"
    else:
        detail = "UNPARSED: " + out[-400:]
    return proc.returncode, detail


CHECK = {"vitest": run_vitest, "wiring": run_wiring, "harness": run_harness}

# label, file (relative to worktree), FROM (must occur exactly once), TO, check kind.
KEYMAP = "apps/ui/src/api/keymap.ts"
ZOOMVIEW = "apps/ui/src/components/graph/zoomView.ts"
SHELL = "apps/ui/src/components/shell/RemedyShell.tsx"
BAR = "apps/ui/src/components/command/CommandBar.tsx"

MUTATIONS = [
    ("k1", KEYMAP, "if (isTypingTarget(target)) {", "if (false) {", "vitest"),
    ("k2", KEYMAP,
     'if (key.toLowerCase() === "k" && (ctrlKey || metaKey) && !altKey) {',
     'if (key.toLowerCase() === "k" && (ctrlKey || metaKey)) {', "vitest"),
    ("k3", KEYMAP,
     "    default:\n      return { action: null, pendingG: false };",
     "    default:\n      return { action: null, pendingG };", "vitest"),
    ("k4", KEYMAP,
     'const zoomable = target === null || tag === "BODY";', "const zoomable = true;", "vitest"),
    ("k5", KEYMAP,
     'return { action: dialogOpen ? null : "walk-back", pendingG: false };',
     'return { action: "walk-back", pendingG: false };', "vitest"),
    ("k6", KEYMAP,
     'const tag = (target.tagName ?? "").toUpperCase();', 'const tag = (target.tagName ?? "");', "vitest"),
    ("z1", ZOOMVIEW,
     "return !dialogOpen && !isTypingTarget(target);", "return !dialogOpen;", "vitest"),
    ("h1", SHELL,
     '      } else if (result.action === "open-bar") {\n        event.preventDefault();',
     '      } else if (result.action === "open-bar") {', "harness"),
    ("h2", BAR,
     "  useEffect(() => {\n    if (focusRequest > 0) inputRef.current?.focus();\n  }, [focusRequest]);\n\n",
     "", "harness"),
    ("h3", SHELL,
     "const result = keymapAction(event, target, pendingG.current, dialogOpen);\n      pendingG.current = result.pendingG;",
     "const result = keymapAction(event, target, pendingG.current, dialogOpen);", "harness"),
    ("w1", SHELL,
     "setBarFocusRequest((count) => count + 1);", "setBarFocusRequest(1);", "wiring"),
]


def run_control(worktree: Path, when: str) -> bool:
    ok = True
    for kind in ("vitest", "wiring", "harness"):
        code, detail = CHECK[kind](worktree)
        print(f"control-{when}-{kind}: exit={code} {detail}")
        if code != 0:
            ok = False
    return ok


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    all_ok = True

    if not run_control(worktree, "first"):
        print("CONTROL FAILED UNMUTATED (first) — aborting")
        return 1

    for label, relpath, frm, to, kind in MUTATIONS:
        path = worktree / relpath
        original = path.read_bytes()
        text = original.decode("utf-8")
        count = text.count(frm)
        if count != 1:
            print(f"{label}: FROM text occurs {count} times in {relpath}, expected 1 — ABORTING")
            return 1
        mutated = text.replace(frm, to, 1).encode("utf-8")
        path.write_bytes(mutated)
        code, detail = CHECK[kind](worktree)
        path.write_bytes(original)
        restored = path.read_bytes() == original
        caught = code != 0
        if not caught:
            all_ok = False
        if not restored:
            all_ok = False
        print(f"{label}: exit={code} {detail} caught={caught}")
        print(f"{label} restored byte-identical: {restored}")

    if not run_control(worktree, "last"):
        all_ok = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

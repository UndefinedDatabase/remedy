#!/usr/bin/env python3
"""F043 R4's red-proof tool (G5, evidence, not product).

One entry, `mutations.py <worktree>`. For each mutation below it edits ONE production file
inside the given worktree (asserting the FROM text occurs exactly once there), runs the ONE
check the mutation is supposed to redden, restores the file's original bytes, and reports
whether the restore was byte-identical. It runs an unmutated control of all three checks
(vitest, pytest, the render harness) first and last, so a check that was already red before any
mutation is never mistaken for one a mutation caught.

Every mutation is a real behaviour change over round 4's S1-S8 production code (DECISION F043
D4): q1-q3 are read by vitest, w1-w2 by the shell/overlay wiring tests, h1-h6 by the render
harness — h4 is R-1115's own red proof, `.tipDetail` losing `display: block`.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
VITEST_CONFIG = PRIMARY / "apps" / "ui" / "vitest.config.ts"

#: The two files G3 names for this round's own vitest additions (checklist item 33: every
#: vitest mutation check runs both, never only the one file a mutation touches).
VITEST_TEST_FILES = [
    "src/api/firstRunTour.test.ts",
    "src/components/term/termPanel.test.ts",
]

PYTEST_TEST_FILES = [
    "tests/ui_contracts/test_tour_overlay_contract.py",
    "tests/ui_contracts/test_term_panel_wiring.py",
]
HARNESS_RELATIVE = ".agent/authored/f043-r4-render_measure.py"

#: label, the file the mutation edits (relative to the worktree), the FROM text (occurs exactly
#: once, asserted below), the TO text, and which check reads the change.
MUTATIONS = [
    (
        "q1", "apps/ui/src/api/firstRunTour.ts",
        '    return storage.getItem(FIRST_RUN_TOUR_KEY) === null;\n'
        '  } catch {\n'
        '    return false;\n'
        '  }',
        '    return storage.getItem(FIRST_RUN_TOUR_KEY) === null;\n'
        '  } catch {\n'
        '    return true;\n'
        '  }',
        "vitest",
    ),
    (
        "q2", "apps/ui/src/api/firstRunTour.ts",
        "storage.setItem(FIRST_RUN_TOUR_KEY, FIRST_RUN_TOUR_SEEN);",
        'storage.setItem(FIRST_RUN_TOUR_KEY, "done");',
        "vitest",
    ),
    (
        "q3", "apps/ui/src/components/term/TermPanel.tsx",
        "      {onStartTour && (\n"
        '        <button type="button" className={styles.tour} onClick={onStartTour}>Take the tour</button>\n'
        "      )}",
        "      {(\n"
        '        <button type="button" className={styles.tour} onClick={onStartTour}>Take the tour</button>\n'
        "      )}",
        "vitest",
    ),
    (
        "w1", "apps/ui/src/components/shell/RemedyShell.tsx",
        "      <FirstRunTourMount relaunch={tourRelaunch} />\n",
        "",
        "pytest",
    ),
    (
        "w2", "apps/ui/src/components/tour/TourOverlay.tsx",
        'ui={{ card: "tour-overlay", backdrop: "tour-backdrop" }}',
        'ui={{ card: "tour-overlay", backdrop: "tour-dim" }}',
        "pytest",
    ),
    (
        "h1", "apps/ui/src/components/tour/FirstRunTour.tsx",
        "onClose={() => { markFirstRunTourSeen(storage); setOpen(false); }}",
        "onClose={() => { setOpen(false); }}",
        "harness",
    ),
    (
        "h2", "apps/ui/src/components/tour/TourFrame.tsx",
        "export const TOUR_SPOT_PAD_PX = 6;",
        "export const TOUR_SPOT_PAD_PX = 0;",
        "harness",
    ),
    (
        "h3", "apps/ui/src/components/tour/TourFrame.tsx",
        "  const spotDrawn = !shown && spot !== null;",
        "  const spotDrawn = false;",
        "harness",
    ),
    (
        "h4", "apps/ui/src/components/term/Term.module.css",
        ".tipDetail {\n"
        "  display: block;\n"
        "  margin-top: 6px;",
        ".tipDetail {\n"
        "  margin-top: 6px;",
        "harness",
    ),
    (
        "h5", "apps/ui/src/components/shell/RemedyShell.tsx",
        "onStartTour={() => { setTermsOpen(false); setTourRelaunch((count) => count + 1); }}",
        "onStartTour={() => { setTourRelaunch((count) => count + 1); }}",
        "harness",
    ),
    (
        "h6", "apps/ui/src/components/tour/FirstRunTour.tsx",
        "if (relaunch > 0) setOpen(true);",
        "if (false) setOpen(true);",
        "harness",
    ),
]


def mutate(path: Path, from_text: str, to_text: str) -> bytes:
    original = path.read_bytes()
    text = original.decode("utf-8")
    count = text.count(from_text)
    if count != 1:
        raise SystemExit(f"FROM text occurs {count} times in {path}, expected exactly 1")
    path.write_text(text.replace(from_text, to_text, 1), encoding="utf-8")
    return original


def restore(path: Path, original: bytes) -> None:
    path.write_bytes(original)
    identical = path.read_bytes() == original
    print(f"restored byte-identical: {identical}")
    if not identical:
        raise SystemExit(f"restore was not byte-identical for {path}")


def run_vitest(worktree: Path) -> tuple[int, str]:
    cmd = [
        str(VITEST_BIN), "run",
        "--root", str(worktree / "apps" / "ui"),
        "--config", str(VITEST_CONFIG),
        *VITEST_TEST_FILES,
    ]
    proc = subprocess.run(
        cmd, cwd=str(worktree / "apps" / "ui"),
        capture_output=True, text=True, timeout=120,
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_pytest(worktree: Path) -> tuple[int, str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) if not existing else f"{worktree}:{existing}"
    cmd = ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PYTEST_TEST_FILES]
    proc = subprocess.run(
        cmd, cwd=str(worktree), capture_output=True, text=True, timeout=120, env=env,
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_harness(worktree: Path) -> tuple[int, str]:
    cmd = ["python3", "-B", str(worktree / HARNESS_RELATIVE), str(worktree)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return proc.returncode, proc.stdout + proc.stderr


def vitest_failed_count(output: str) -> str:
    match = re.search(r"Tests\s+(\d+) failed", output)
    return match.group(1) if match else "0"


def pytest_failed_count(output: str) -> str:
    match = re.search(r"(\d+) failed", output)
    return match.group(1) if match else "0"


def render_reading(output: str) -> str:
    match = re.search(r"RENDER: \d+ of \d+ checks pass", output)
    return match.group(0) if match else "RENDER: <no reading found>"


def run_check(kind: str, worktree: Path) -> tuple[int, str]:
    if kind == "vitest":
        return run_vitest(worktree)
    if kind == "pytest":
        return run_pytest(worktree)
    return run_harness(worktree)


def report_check(label: str, kind: str, exit_code: int, output: str) -> bool:
    """Prints the one line the block orders and answers whether the check was caught (non-zero
    exit). A mutation that stayed green is printed exactly as measured — never papered over."""
    if kind == "vitest":
        reading = f"failed={vitest_failed_count(output)}"
    elif kind == "pytest":
        reading = f"failed={pytest_failed_count(output)}"
    else:
        reading = render_reading(output)
    caught = exit_code != 0
    print(f"{label}: exit={exit_code} {reading}{'' if caught else ' STAYED GREEN'}")
    return caught


def run_control(worktree: Path, when: str) -> bool:
    print(f"=== CONTROL ({when}) ===")
    v_exit, v_out = run_vitest(worktree)
    p_exit, p_out = run_pytest(worktree)
    h_exit, h_out = run_harness(worktree)
    ok = v_exit == 0 and p_exit == 0 and h_exit == 0
    print(
        f"control ({when}): vitest exit={v_exit} pytest exit={p_exit} "
        f"harness exit={h_exit} {render_reading(h_out)} all_pass={ok}"
    )
    return ok


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")

    control_before_ok = run_control(worktree, "before")

    all_caught = True
    for label, rel_path, from_text, to_text, kind in MUTATIONS:
        path = worktree / rel_path
        original = mutate(path, from_text, to_text)
        try:
            exit_code, output = run_check(kind, worktree)
            caught = report_check(label, kind, exit_code, output)
            all_caught = all_caught and caught
        finally:
            restore(path, original)

    control_after_ok = run_control(worktree, "after")

    overall = all_caught and control_before_ok and control_after_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())

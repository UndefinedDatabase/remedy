#!/usr/bin/env python3
"""F042 R4's mutation tool (G5): red-proofs S1 to S6 inside a disposable worktree.

Usage: python3 f042-r4-mutations.py <worktree path>

For each mutation below it edits the named production file INSIDE that worktree (asserting its
FROM text occurs exactly once there), runs the named check, restores the original bytes, and
prints one line: the mutation's label, the check's real exit code, and either the failed count
(vitest, pytest) or the harness's own "RENDER: <n> of 17 checks pass" reading with the names of
its failing checks. It runs an unmutated CONTROL of every check used, first and last, reports
"restored byte-identical: <bool>" after each restore, and ends with "ALL MUTATIONS CAUGHT AND
RESTORED CLEANLY: <bool>". It never touches any file outside the worktree it is handed.
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


def _run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None, timeout: int = 300) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    return proc.returncode, proc.stdout + proc.stderr


def run_vitest_home(worktree: Path) -> tuple[int, str]:
    return _run_vitest(worktree, "src/api/homeGrid.test.ts")


def run_vitest_address(worktree: Path) -> tuple[int, str]:
    return _run_vitest(worktree, "src/api/cockpitAddress.test.ts")


def _run_vitest(worktree: Path, test_file: str) -> tuple[int, str]:
    ui = worktree / "apps" / "ui"
    code, out = _run(
        ["node", str(VITEST_BIN), "run", "--root", str(ui), "--config", str(VITEST_CONFIG), test_file],
        cwd=ui,
    )
    m = re.search(r"Tests\s+(\d+)\s+failed", out)
    failed = m.group(1) if m else ("0" if code == 0 else "?")
    return code, f"failed={failed}"


def run_pytest(worktree: Path) -> tuple[int, str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) if not existing else f"{worktree}{os.pathsep}{existing}"
    code, out = _run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/ui_contracts/test_project_switcher_wiring.py"],
        cwd=worktree, env=env,
    )
    m = re.search(r"(\d+)\s+failed", out)
    failed = m.group(1) if m else ("0" if code == 0 else "?")
    return code, f"failed={failed}"


def run_harness(worktree: Path) -> tuple[int, str]:
    code, out = _run(
        ["python3", "-B", str(worktree / ".agent" / "authored" / "f042-r4-render_measure.py"), str(worktree)],
        cwd=worktree, timeout=300,
    )
    m = re.search(r"RENDER: \d+ of \d+ checks pass", out)
    reading = m.group(0) if m else "no RENDER line"
    if m:
        failing = [line.split(" ", 2)[1] for line in out.splitlines() if line.startswith("FAIL ")]
        if failing:
            reading = f"{reading} failing: {', '.join(failing)}"
    return code, reading


# Each mutation: a label, the file it edits (relative to the worktree), the FROM text it asserts
# occurs exactly once, the TO text it replaces that with, and the check it runs.
MUTATIONS = [
    dict(
        label="g1", file="apps/ui/src/api/homeGrid.ts", check=run_vitest_home,
        frm='if (cost.basis === "absent" || cost.value_usd === null) return "Cost today: not measured";',
        to='if (cost.value_usd === null) return "Cost today: not measured";',
    ),
    dict(
        label="g2", file="apps/ui/src/api/homeGrid.ts", check=run_vitest_home,
        frm="export const HOME_PAGE_SIZE = 12;",
        to="export const HOME_PAGE_SIZE = 10;",
    ),
    dict(
        label="g3", file="apps/ui/src/api/homeGrid.ts", check=run_vitest_home,
        frm='if (lowered === "running") return "current";',
        to='if (lowered === "running") return "open";',
    ),
    dict(
        label="a1", file="apps/ui/src/api/cockpitAddress.ts", check=run_vitest_address,
        frm='  params.delete("project");\n',
        to="",
    ),
    dict(
        label="w1", file="apps/ui/src/RemedyApp.tsx", check=run_pytest,
        frm=(
            "const onHome = useCallback(() => {\n"
            "    writeAddress(homeSearch(window.location.search), false);\n"
            "  }, [writeAddress]);"
        ),
        to=(
            "function onHome() {\n"
            "    writeAddress(homeSearch(window.location.search), false);\n"
            "  }"
        ),
    ),
    dict(
        label="x1", file="apps/ui/src/components/shell/ProjectProvider.tsx", check=run_harness,
        frm="if (gate.current.current() !== project) gate.current.begin(project);",
        to="",
    ),
    dict(
        label="x2", file="apps/ui/src/RemedyApp.tsx", check=run_harness,
        frm='alignContent: "center", gap: 16, ',
        to="",
    ),
    dict(
        label="h1", file="apps/ui/src/RemedyApp.tsx", check=run_harness,
        frm=(
            "if (replace) {\n"
            '      window.history.replaceState(window.history.state, "", url);\n'
            "    } else {\n"
            '      window.history.pushState(window.history.state, "", url);\n'
            "    }"
        ),
        to='window.history.pushState(window.history.state, "", url);',
    ),
    dict(
        label="h2", file="apps/ui/src/components/home/HomeGrid.tsx", check=run_harness,
        frm="onClick={() => switchTo(entry.slug)}",
        to="onClick={() => {}}",
    ),
    dict(
        label="h3", file="apps/ui/src/components/home/HomeGrid.tsx", check=run_harness,
        frm=(
            "setSummaries((prev) => {\n"
            "        const next = { ...prev };\n"
            "        for (const [slug, summary] of pairs) next[slug] = summary;\n"
            "        return next;\n"
            "      });"
        ),
        to="",
    ),
]


def control(worktree: Path) -> bool:
    ok = True
    for name, fn in (
        ("vitest homeGrid", run_vitest_home),
        ("vitest cockpitAddress", run_vitest_address),
        ("pytest wiring", run_pytest),
        ("harness", run_harness),
    ):
        code, reading = fn(worktree)
        print(f"CONTROL {name}: exit={code} {reading}")
        if code != 0:
            ok = False
    return ok


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    print("-- control, first --")
    first_ok = control(worktree)

    all_caught = True
    for mutation in MUTATIONS:
        label = mutation["label"]
        path = worktree / mutation["file"]
        original = path.read_bytes()
        text = original.decode("utf-8")
        frm = mutation["frm"]
        occurrences = text.count(frm)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times in {mutation['file']}, expected 1 -- ABORTING")
            return 3
        path.write_bytes(text.replace(frm, mutation["to"], 1).encode("utf-8"))
        try:
            code, reading = mutation["check"](worktree)
        finally:
            path.write_bytes(original)
        restored = path.read_bytes() == original
        caught = code != 0
        print(f"{label}: exit={code} {reading} restored byte-identical: {restored}")
        if not caught or not restored:
            all_caught = False

    print("-- control, last --")
    last_ok = control(worktree)

    result = all_caught and first_ok and last_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())

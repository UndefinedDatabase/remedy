#!/usr/bin/env python3
"""F043 R2's red-proof tool (G5): one real behaviour mutation per production file S1-S9 touched,
each caught by the check the round's spec says catches it — vitest for m1-m7, the round's own
render harness for h1-h3 — then restored byte-identical.

Usage: python3 -B f043-r2-mutations.py <worktree path>

The worktree is a `git worktree add --detach` copy of THIS branch's tip, with
`<worktree>/apps/ui/node_modules` symlinked to the PRIMARY checkout's own (the caller's job,
not this tool's). Every mutation edits a file INSIDE that worktree, asserting its FROM text
occurs exactly once there before writing, runs the named check, restores the original bytes,
and reports whether the restore was byte-identical. An unmutated control of both checks runs
first and last, so a clean run at the end proves the restores left nothing behind.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
VITEST_CONFIG = PRIMARY / "apps" / "ui" / "vitest.config.ts"
VITEST_TESTS = [
    "src/api/terminology.test.ts",
    "src/api/terminologyAudit.test.ts",
    "src/components/term/termAudit.test.ts",
]

TASK_CHECKLIST_CARD = "apps/ui/src/components/panels/TaskChecklistCard.tsx"
TERM_TSX = "apps/ui/src/components/term/Term.tsx"
TOP_METRICS_BAR = "apps/ui/src/components/metrics/TopMetricsBar.tsx"
AGENT_NOW_CARD = "apps/ui/src/components/panels/AgentNowCard.tsx"
DECISION_INBOX_CARD = "apps/ui/src/components/panels/DecisionInboxCard.tsx"
BRAIN_GRAPH_STAGE = "apps/ui/src/components/graph/BrainGraphStage.tsx"
TERMINOLOGY_TS = "apps/ui/src/api/terminology.ts"
RIGHT_LIVE_PANEL_CSS = "apps/ui/src/components/panels/RightLivePanel.module.css"

# (label, file, FROM text, TO text, check kind ["vitest" | "harness"])
MUTATIONS: list[tuple[str, str, str, str, str]] = [
    (
        "m1", TASK_CHECKLIST_CARD,
        '  if (task.state === "blocked") return "blocked.task";\n', "",
        "vitest",
    ),
    (
        "m2", TERM_TSX,
        "tabIndex={insideControl ? undefined : 0}", "tabIndex={0}",
        "vitest",
    ),
    (
        "m3", TOP_METRICS_BAR,
        '  proof: "metric.proof",\n};', '  proof: "metric.proof",\n  tokens: "metric.open",\n};',
        "vitest",
    ),
    (
        "m4", AGENT_NOW_CARD,
        '<Term term="agent.live">Live</Term>', "Live",
        "vitest",
    ),
    (
        "m5", DECISION_INBOX_CARD,
        "<h2><Term term=\"panel.decisions\">Decision inbox</Term></h2>", "<h2>Decision inbox</h2>",
        "vitest",
    ),
    (
        "m6", BRAIN_GRAPH_STAGE,
        '<Term term="graph.scrubbed">SCRUBBED</Term>', "SCRUBBED",
        "vitest",
    ),
    (
        "m7", TERMINOLOGY_TS,
        "the planner chooses how many", "the planner picks how many",
        "vitest",
    ),
    (
        "h1", RIGHT_LIVE_PANEL_CSS,
        ".cardHeader > span { font-size: 12px; color: var(--remedy-muted); }",
        ".cardHeader span { font-size: 12px; color: var(--remedy-muted); }",
        "harness",
    ),
    (
        "h2", RIGHT_LIVE_PANEL_CSS,
        ".liveSmall > span:first-child { width: 7px; height: 7px; border-radius: 50%; background: var(--remedy-green); }",
        ".liveSmall span { width: 7px; height: 7px; border-radius: 50%; background: var(--remedy-green); }",
        "harness",
    ),
    (
        "h3", TOP_METRICS_BAR,
        '  proof: "metric.proof",\n};', '  proof: "metric.proof",\n  tokens: "metric.open",\n};',
        "harness",
    ),
]

FAILED_RE = re.compile(r"Tests\s+(\d+) failed")
RENDER_RE = re.compile(r"RENDER: \d+ of \d+ checks pass")


def run_vitest(worktree: Path) -> tuple[int, str]:
    cwd = worktree / "apps" / "ui"
    cmd = [str(VITEST_BIN), "run", "--root", str(cwd), "--config", str(VITEST_CONFIG), *VITEST_TESTS]
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=300)
    output = proc.stdout + proc.stderr
    match = FAILED_RE.search(output)
    reading = f"{match.group(1)} failed" if match else f"0 failed (exit {proc.returncode})"
    return proc.returncode, reading


def run_harness(worktree: Path) -> tuple[int, str]:
    script = worktree / ".agent" / "authored" / "f043-r2-render_measure.py"
    cmd = ["python3", "-B", str(script), str(worktree)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    output = proc.stdout + proc.stderr
    match = RENDER_RE.search(output)
    reading = match.group(0) if match else f"no RENDER line (exit {proc.returncode})"
    return proc.returncode, reading


def run_check(kind: str, worktree: Path) -> tuple[int, str]:
    return run_vitest(worktree) if kind == "vitest" else run_harness(worktree)


def apply_mutation(worktree: Path, rel_path: str, from_text: str, to_text: str) -> str:
    path = worktree / rel_path
    original = path.read_text(encoding="utf-8")
    count = original.count(from_text)
    assert count == 1, f"{rel_path}: FROM text occurs {count} times, expected exactly 1"
    path.write_text(original.replace(from_text, to_text, 1), encoding="utf-8")
    return original


def restore(worktree: Path, rel_path: str, original: str) -> bool:
    path = worktree / rel_path
    path.write_text(original, encoding="utf-8")
    return path.read_text(encoding="utf-8") == original


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f043-r2-mutations.py <worktree path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    all_ok = True

    print("CONTROL (first) vitest:", end=" ")
    code, reading = run_vitest(worktree)
    print(f"exit={code} reading={reading}")
    if code != 0:
        all_ok = False

    print("CONTROL (first) harness:", end=" ")
    code, reading = run_harness(worktree)
    print(f"exit={code} reading={reading}")
    if code != 0:
        all_ok = False

    for label, rel_path, from_text, to_text, kind in MUTATIONS:
        original = apply_mutation(worktree, rel_path, from_text, to_text)
        code, reading = run_check(kind, worktree)
        print(f"{label}: exit={code} reading={reading}")
        if code == 0:
            all_ok = False
        identical = restore(worktree, rel_path, original)
        print(f"restored byte-identical: {identical}")
        if not identical:
            all_ok = False

    print("CONTROL (last) vitest:", end=" ")
    code, reading = run_vitest(worktree)
    print(f"exit={code} reading={reading}")
    if code != 0:
        all_ok = False

    print("CONTROL (last) harness:", end=" ")
    code, reading = run_harness(worktree)
    print(f"exit={code} reading={reading}")
    if code != 0:
        all_ok = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

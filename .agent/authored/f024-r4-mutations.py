#!/usr/bin/env python3
"""Mutation tool for F024 T003 components: the track geometry, the bar, the stage, the shell, the pill and the hook.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f024-r4-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f024-r4-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

VIEW_REL = "apps/ui/src/components/timeline/timelineView.ts"
HOOK_REL = "apps/ui/src/components/timeline/useTimelineScrub.ts"
BAR_REL = "apps/ui/src/components/timeline/PhaseTimeline.tsx"
STAGE_REL = "apps/ui/src/components/graph/BrainGraphStage.tsx"
STAGE_CSS_REL = "apps/ui/src/components/graph/BrainGraphStage.module.css"
SHELL_REL = "apps/ui/src/components/shell/RemedyShell.tsx"
PILL_REL = "apps/ui/src/components/panels/LiveStatusPill.tsx"
VITEST_FILES = [
    "apps/ui/src/components/timeline/timelineView.test.ts",
]
# The whole contract directory, so the layout, ratchet and timeline guards run beside this
# round's own wiring guard.
GUARD_REL = "tests/ui_contracts"

MUTATIONS = [
    {"id": "m1", "name": "the handle sits at the start of its event's slot", "file": VIEW_REL,
     "from": "  return (p + (at + 1 - from) / (to - from)) / TIMELINE_PHASES.length;\n",
     "to": "  return (p + (at - from) / (to - from)) / TIMELINE_PHASES.length;\n"},
    {"id": "m2", "name": "a segment does not own its right edge", "file": VIEW_REL,
     "from": "  const p = Math.max(0, Math.min(TIMELINE_PHASES.length - 1, Math.ceil(x - EPSILON) - 1));\n",
     "to": "  const p = Math.max(0, Math.min(TIMELINE_PHASES.length - 1, Math.floor(x)));\n"},
    {"id": "m3", "name": "a point in an unreached phase goes before the first event", "file": VIEW_REL,
     "from": "  if (range === null) return whole.lastSeq;\n", "to": "  if (range === null) return -1;\n"},
    {"id": "m4", "name": "the stage draws the live model while scrubbed", "file": STAGE_REL,
     "from": "  const model = scrub.scrubbedModel ?? liveModel;\n", "to": "  const model = liveModel;\n"},
    {"id": "m5", "name": "the banner is not announced", "file": STAGE_REL,
     "from": '        <div className={styles.scrubBanner} role="status" data-ui="scrub-banner">\n',
     "to": '        <div className={styles.scrubBanner} data-ui="scrub-banner">\n'},
    {"id": "m6", "name": "the slider ignores the keyboard", "file": BAR_REL,
     "from": "            if (scrub.onKey(event.key, event.shiftKey)) event.preventDefault();\n",
     "to": "            event.preventDefault();\n"},
    {"id": "m7", "name": "a glyph click lands one event late", "file": BAR_REL,
     "from": "            onClick={() => scrub.scrubTo(g.seq)}\n", "to": "            onClick={() => scrub.scrubTo(g.seq + 1)}\n"},
    {"id": "m8", "name": "the LIVE button hides its state", "file": BAR_REL,
     "from": "          aria-pressed={live}\n", "to": ""},
    {"id": "m9", "name": "the bar keeps a timer", "file": BAR_REL,
     "from": "  const live = state.mode === \"live\";\n",
     "to": "  const live = state.mode === \"live\";\n  window.setTimeout(() => undefined, 0);\n"},
    {"id": "m10", "name": "the bar's phase order drifts", "file": BAR_REL,
     "from": '  "build",\n  "test",\n  "review",\n', "to": '  "build",\n  "review",\n  "test",\n'},
    {"id": "m11", "name": "the stage gets a scrubber without its model", "file": SHELL_REL,
     "from": "rows={ledgerRows} scrub={scrub} serverToken={serverToken} />",
     "to": "rows={ledgerRows} scrub={{ ...scrub, scrubbedModel: null }} serverToken={serverToken} />"},
    {"id": "m12", "name": "the pill says nothing about the replay", "file": SHELL_REL,
     "from": ' replay={scrub.state.mode === "scrubbed"}', "to": ""},
    {"id": "m13", "name": "the transport outranks the replay", "file": PILL_REL,
     "from": "  if (replay) {\n", "to": '  if (replay && streamStatus !== "delayed") {\n'},
    {"id": "m14", "name": "the banner paints a raw colour", "file": STAGE_CSS_REL,
     "from": "  background: var(--remedy-purple);\n", "to": "  background: #a78bfa;\n"},
    {"id": "m15", "name": "an overflowing LIVE replays instead of rebuilding", "file": HOOK_REL,
     "from": "      fed.reset(rows);\n", "to": ""},
    {"id": "m16", "name": "LIVE skips the fast-forward", "file": HOOK_REL,
     "from": "    const frames = catchUpPlan(state.position, state.head, reducedMotion);\n",
     "to": "    const frames = catchUpPlan(state.head, state.head, reducedMotion);\n"},
]


def edits_of(mut):
    return mut.get("edits") or [{"from": mut["from"], "to": mut["to"]}]


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_vitest(worktree, tag):
    cache_dir = HELPER_DIR / f"cache-{tag}-{int(time.time() * 1000)}"
    config = HELPER_DIR / f"vitest.config.{tag}.mjs"
    include = ", ".join(f'"{worktree / f}"' for f in VITEST_FILES)
    config.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        f'  test: {{ environment: "node", include: [{include}] }},\n'
        "};\n"
    )
    proc = subprocess.run([str(VITEST_BIN), "run", "--config", str(config)],
                          cwd=str(PRIMARY_UI), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    m = re.search(r"Tests\s+(\d+)\s+failed\s*\|\s*(\d+)\s+passed", out)
    if m:
        failed, passed = int(m.group(1)), int(m.group(2))
    else:
        m2 = re.search(r"Tests\s+(\d+)\s+passed", out)
        failed, passed = (0, int(m2.group(1))) if m2 else (-1, -1)
    return {"exit": proc.returncode, "failed": failed, "passed": passed}


def run_guard(worktree):
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         str(worktree / GUARD_REL), f"--rootdir={worktree}"],
        cwd=str(worktree), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", out)) else 0
    passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", out)) else 0
    return {"exit": proc.returncode, "failed": failed, "passed": passed}


def run_both(worktree, tag):
    return run_vitest(worktree, tag), run_guard(worktree)


def fmt(v, g):
    return (f"vitest exit={v['exit']} failed={v['failed']} passed={v['passed']} | "
            f"guard exit={g['exit']} failed={g['failed']} passed={g['passed']}")


def main():
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")
    v, g = run_both(worktree, "control-first")
    print(f"CONTROL FIRST: {fmt(v, g)}")
    first_green = v["exit"] == 0 and v["failed"] == 0 and g["exit"] == 0 and g["failed"] == 0
    if not first_green:
        print("control is not green; aborting")
        return 1
    all_ok = True
    for mut in MUTATIONS:
        target = worktree / mut["file"]
        original = target.read_bytes()
        digest = sha256_of(target)
        text = original.decode("utf-8")
        counts = []
        for edit in edits_of(mut):
            counts.append(text.count(edit["from"]))
            text = text.replace(edit["from"], edit["to"], 1)
        if counts != [1] * len(counts):
            print(f"{mut['id']}: SKIPPED, FROM occurrences {counts}")
            all_ok = False
            continue
        target.write_bytes(text.encode("utf-8"))
        try:
            v, g = run_both(worktree, mut["id"])
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = (v["exit"] != 0 and v["failed"] > 0) or (g["exit"] != 0 and g["failed"] > 0)
        all_ok &= caught and restored
        print(f"{mut['id']} ({mut['name']}): {fmt(v, g)} | caught={caught} restored byte-identical={restored}")
    v, g = run_both(worktree, "control-last")
    last_green = v["exit"] == 0 and v["failed"] == 0 and g["exit"] == 0 and g["failed"] == 0
    print(f"CONTROL LAST: {fmt(v, g)}")
    all_ok &= last_green
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Mutation tool for F023 T003 first part: the L3 evidence panel, its tabs, its tokens and their guards.

Given a worktree root, runs an unmutated control first and last, and between them applies
each mutation below (every FROM must occur exactly once in its file), runs the vitest files
of this round and the Python contract guard, restores the file BYTE-IDENTICAL, and reports
each runner's failed count and exit code. A mutation is caught when at least one runner
goes red. vitest runs from the PRIMARY `apps/ui` (a worktree has no node_modules) with a
scratch config under `.remedy-wt/f023-r5-mutscratch/`; pytest runs with `python3 -B` so a
bytecode cache can never serve a previous mutation's module.

Usage: python3 -B mutations.py <worktree_root>
"""
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f023-r5-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

G = "apps/ui/src/components/graph/"
TABS_REL = G + "evidencePanel.ts"
PANEL_REL = G + "EvidencePanel.tsx"
PANEL_CSS_REL = G + "EvidencePanel.module.css"
STAGE_REL = G + "BrainGraphStage.tsx"
POPOVER_REL = G + "RunDetailPopover.tsx"
CRUMBS_CSS_REL = G + "ZoomBreadcrumbs.module.css"
APP_TOKENS_REL = "apps/ui/src/styles/tokens.css"
REF_TOKENS_REL = "docs/ui/design_reference/tokens.css"
VITEST_FILES = [
    G + "evidencePanel.test.ts",
]
GUARD_RELS = [
    "tests/ui_contracts/test_evidence_panel_contract.py",
    "tests/ui_contracts/test_run_detail_wiring.py",
]

MUTATIONS = [
    {"id": "m1", "name": "the tabs lose the feature's order", "file": TABS_REL,
     "from": '  { tab: "diff", label: "Diff" },\n  { tab: "prompt", label: "Prompt trace" },\n',
     "to": '  { tab: "prompt", label: "Prompt trace" },\n  { tab: "diff", label: "Diff" },\n'},
    {"id": "m2", "name": "the trace lists every task's prompts", "file": TABS_REL,
     "from": "    .filter((p) => p.taskId === taskId)\n", "to": "    .filter(() => true)\n"},
    {"id": "m3", "name": "the reviewer's prompt is listed before the builder's", "file": TABS_REL,
     "from": '  const order = (role: string) => (role === "builder" ? 0 : role === "reviewer" ? 1 : 2);\n',
     "to": '  const order = (role: string) => (role === "reviewer" ? 0 : role === "builder" ? 1 : 2);\n'},
    {"id": "m4", "name": "the panel's shadow is a raw colour again", "file": PANEL_CSS_REL,
     "from": "box-shadow: var(--remedy-shadow-panel);", "to": "box-shadow: -18px 0 40px rgba(37, 50, 79, 0.08);"},
    {"id": "m5", "name": "the panel's layer is a number", "file": PANEL_CSS_REL,
     "from": "  z-index: var(--remedy-z-overlay);\n", "to": "  z-index: 80;\n"},
    {"id": "m6", "name": "reduced motion still slides the panel in", "file": PANEL_CSS_REL,
     "from": "  .panel { animation: none; }\n", "to": "  .panel { }\n"},
    {"id": "m7", "name": "the diff loads whichever tab is open", "file": PANEL_REL,
     "from": '        {tab === "diff" && <DiffTab jobId={jobId} token={token} taskId={detail.taskId} />}\n',
     "to": "        <DiffTab jobId={jobId} token={token} taskId={detail.taskId} />\n"},
    {"id": "m8", "name": "a diff read for another task is shown", "file": PANEL_REL,
     "from": "loaded !== null && loaded.taskId === taskId ? loaded.envelope : null",
     "to": "loaded !== null ? loaded.envelope : null"},
    {"id": "m9", "name": "the panel becomes a dialog Escape skips", "file": PANEL_REL,
     "from": '<aside className={styles.panel} aria-label="Evidence" data-ui="evidence-panel">',
     "to": '<aside className={styles.panel} role="dialog" aria-label="Evidence" data-ui="evidence-panel">'},
    {"id": "m10", "name": "the panel opens at L2", "file": STAGE_REL,
     "from": "{focusedRun && zoom.state.level === 3 && zoom.state.tab !== null && (",
     "to": "{focusedRun && zoom.state.level >= 2 && zoom.state.tab !== null && ("},
    {"id": "m11", "name": "the run detail stays open at L3", "file": STAGE_REL,
     "from": "{focusedRun && zoom.state.level === 2 && (", "to": "{focusedRun && ("},
    {"id": "m12", "name": "Open diff opens the prompt tab", "file": POPOVER_REL,
     "from": 'onClick={() => onOpenEvidence("diff")}>Open diff</button>',
     "to": 'onClick={() => onOpenEvidence("prompt")}>Open diff</button>'},
    {"id": "m13", "name": "the app sheet's slide duration drifts from the reference", "file": APP_TOKENS_REL,
     "from": "  --remedy-dur-base: 220ms;\n", "to": "  --remedy-dur-base: 200ms;\n"},
    {"id": "m14", "name": "the reference's panel shadow drifts from the app sheet", "file": REF_TOKENS_REL,
     "from": "  --remedy-shadow-panel: -18px 0 40px rgba(37, 50, 79, 0.08);",
     "to": "  --remedy-shadow-panel: -18px 0 40px rgba(37, 50, 79, 0.1);"},
    {"id": "m15", "name": "the breadcrumbs' layer is a number again", "file": CRUMBS_CSS_REL,
     "from": "  z-index: var(--remedy-z-stage-ui);\n", "to": "  z-index: 5;\n"},
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
         *[str(worktree / g) for g in GUARD_RELS], f"--rootdir={worktree}"],
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

#!/usr/bin/env python3
"""F288 R4 G5 — the round's mutation red-proof tool (DECISION F288 D4).

Given a worktree path, each probe mutates ONE line of ONE file inside that
worktree (asserting the FROM text occurs exactly once in the file), runs
`vitest run` over the worktree's four repaired test files through a
plain-object scratch config rooted at the PRIMARY `apps/ui` (the worktree
carries no installed `node_modules`), restores the file's original bytes
byte-for-byte, and prints the run's label, exit code, failed test count and
failing test names. An unmutated control runs first and last. p1 is the
seq-2 outcome flip (`changed` -> `unchanged`), read as it comes rather than
assumed red: `changed` births a `repair_run` in state "pass" and
`unchanged` births one in state "blocked" (REPAIR_OUTCOME_STATE_TABLE), but
none of brainLedger.test.ts, stateMotion.test.ts, timelineIndex.test.ts or
timelineView.test.ts asserts on a repair_run's own node state or reads
`ignored`, so the flip may have no reader among these four files. p2
(deleting `feedRowOf`'s `planTaskIds` assignment, leaving the key
`undefined` rather than merely `[]` — the recording has no `plan_approved`
frame, so a hard-wired `[]` would be indistinguishable from the untouched
code) and p3 (dropping the recording's last frame) must each turn at least
one of the four files red.
"""
import json
import subprocess
import sys
from pathlib import Path

VITEST = "/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest"
PRIMARY_UI = "/home/decodeux/Repos/remedy/apps/ui"
SCRATCH_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f288-r4-worker")

TEST_FILES = [
    "apps/ui/src/components/graph/brainLedger.test.ts",
    "apps/ui/src/components/graph/renderers/stateMotion.test.ts",
    "apps/ui/src/components/timeline/timelineIndex.test.ts",
    "apps/ui/src/components/timeline/timelineView.test.ts",
]

SEQ2_LINE = (
    '  { seq: 2, event: { seq: 2, event: "task_round_repaired", '
    'timestamp: "2026-09-27T00:54:46.009224+00:00", outcome: "changed", '
    'task_id: "fe1b5b487fda490f", attempt_id: "b1603f4616344102" } },\n'
)
SEQ9_LINE = (
    '  { seq: 9, event: { seq: 9, event: "task_run_completed", '
    'timestamp: "2026-09-27T00:54:46.734042+00:00", outcome: "pass", '
    'task_id: "4b3ddac9dba846af", attempt_id: "935e9371d7ce4fe5" } },\n'
)

PROBES = [
    {
        "label": "p1",
        "file": "apps/ui/src/components/graph/brainDemoRecording.ts",
        "from": SEQ2_LINE,
        "to": SEQ2_LINE.replace('outcome: "changed"', 'outcome: "unchanged"'),
    },
    {
        # A row literal that hard-codes `planTaskIds: []` would be
        # indistinguishable from the untouched code on this recording: it
        # has no `plan_approved` frame, so `planTaskIdsOf` already returns
        # `[]` for every one of its ten rows. "Stops SETTING planTaskIds"
        # means the key is genuinely absent (`undefined`) rather than merely
        # empty — deleting the assignment, not replacing its value.
        "label": "p2",
        "file": "apps/ui/src/api/feedRow.ts",
        "from": "    planTaskIds: planTaskIdsOf(envelope),\n",
        "to": "",
    },
    {
        "label": "p3",
        "file": "apps/ui/src/components/graph/brainDemoRecording.ts",
        "from": SEQ9_LINE,
        "to": "",
    },
]


def write_scratch_config(worktree: Path) -> Path:
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    include_paths = [json.dumps(str(worktree / f)) for f in TEST_FILES]
    include = ",\n      ".join(include_paths)
    config = (
        "export default {\n"
        "  root: " + json.dumps(PRIMARY_UI) + ",\n"
        "  cacheDir: " + json.dumps(str(SCRATCH_DIR / "vite-cache")) + ",\n"
        "  test: {\n"
        '    environment: "node",\n'
        "    include: [\n      " + include + "\n    ],\n"
        "  },\n"
        "};\n"
    )
    path = SCRATCH_DIR / "vitest.scratch.config.mjs"
    path.write_text(config)
    return path


def run_vitest(config_path: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [VITEST, "run", "--config", str(config_path)],
        cwd=PRIMARY_UI,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def summarize(output: str) -> tuple[int, list[str]]:
    """(failed test count, failing test names) read from vitest's own
    tree-reporter output: the summary line 'Tests  N failed | ...' and each
    failing test's own '×'-marked line."""
    failed = 0
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("Tests"):
            parts = stripped.split()
            if "failed" in parts:
                idx = parts.index("failed")
                failed = int(parts[idx - 1])
    names = []
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("× ") or stripped.startswith("x "):
            names.append(stripped[2:].strip())
    return failed, names


def run_probe(label: str, worktree: Path, config_path: Path) -> None:
    code, output = run_vitest(config_path)
    failed, names = summarize(output)
    print(f"--- {label} ---")
    print(f"exit code: {code}")
    print(f"failed count: {failed}")
    for name in names:
        print(f"  failing: {name}")
    if not names and failed:
        print("  (failing names not parsed; see raw output below)")
        print(output)


def mutate(path: Path, from_text: str, to_text: str) -> str:
    original = path.read_text()
    count = original.count(from_text)
    if count != 1:
        raise SystemExit(f"FROM text occurs {count} times (expected 1) in {path}")
    path.write_text(original.replace(from_text, to_text))
    return original


def restore(path: Path, original: str) -> bool:
    path.write_text(original)
    return path.read_text() == original


def main() -> None:
    worktree = Path(sys.argv[1]).resolve()
    config_path = write_scratch_config(worktree)

    run_probe("control (before)", worktree, config_path)

    for probe in PROBES:
        target = worktree / probe["file"]
        original = mutate(target, probe["from"], probe["to"])
        run_probe(probe["label"], worktree, config_path)
        identical = restore(target, original)
        print(f"  restored byte-identical: {identical}")

    run_probe("control (after)", worktree, config_path)


if __name__ == "__main__":
    main()

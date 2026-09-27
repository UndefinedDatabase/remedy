#!/usr/bin/env python3
"""F288 R6 G5 — the round's mutation-and-red-proof tool (DECISION F288 D6, T003).

Usage:
    python3 f288-r6-mutations.py <worktree-path>

For each of the round's seven ordered mutations, this tool edits the named file
INSIDE <worktree-path> (asserting its FROM text occurs EXACTLY ONCE first), runs
the mutation's own check, restores the file's original bytes, and reports the
mutation's label, the run's real exit code, its failed count and failing names.

THREE RUNNERS, an unmutated CONTROL opening and closing each one's own block:

  TypeScript (m1-m3, `promptListEntries` in brainView.ts) — vitest, with a
  PLAIN-OBJECT scratch config: `root` the PRIMARY apps/ui, `cacheDir` under
  `.remedy-wt/`, `test: { environment: "node", include: [<the worktree's own
  brainView.test.ts>] }`, run from the primary checkout's apps/ui. A ROUTE
  PROOF (not itself one of the seven) breaks brainView.ts at its own syntax
  first, proving the scratch config reads the WORKTREE's own sources and not
  the primary checkout's, whatever the test imports.

  Python (m4-m6, PromptNodeList.tsx/.module.css and BrainGraphStage.tsx) —
      python3 -B -m pytest -q -p no:cacheprovider tests/ui_contracts/test_brain_stage_mount.py
  from the worktree's root, after purging its __pycache__ directories.

  Harness (m7) — the worktree's own committed harness,
      python3 <worktree>/.agent/authored/f288-r6-render_measure.py <worktree>
  run so the worktree is both the harness's source and its repo root. A fresh
  worktree carries no apps/ui/node_modules (gitignored), so its own sources
  cannot resolve `react`: a symlink from the primary's apps/ui/node_modules
  into the worktree's apps/ui/ is created before the control run and deleted
  once this runner's block is done.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PRIMARY_ROOT = Path("/home/decodeux/Repos/remedy")
PRIMARY_UI = PRIMARY_ROOT / "apps" / "ui"
PRIMARY_NODE_MODULES = PRIMARY_UI / "node_modules"
VITEST_BIN = PRIMARY_NODE_MODULES / ".bin" / "vitest"
WORKER_DIR = PRIMARY_ROOT / ".remedy-wt" / "f288-r6-worker"
SCRATCH_CONFIG = WORKER_DIR / "vitest.f288-r6-mutations.config.mjs"
SCRATCH_CACHE_DIR = PRIMARY_ROOT / ".remedy-wt" / "f288-r6-vite-cache"

PY_TESTS = ["tests/ui_contracts/test_brain_stage_mount.py"]
TS_TEST_RELPATHS = ["apps/ui/src/components/graph/brainView.test.ts"]
HARNESS_MEASURE_REL = ".agent/authored/f288-r6-render_measure.py"


@dataclass(frozen=True)
class Mutation:
    label: str
    rel_path: str
    from_text: str
    to_text: str
    runner: str  # "ts", "py" or "harness"


ROUTE_PROOF = Mutation(
    "ROUTE PROOF — brainView.ts broken at its own syntax so the worktree's "
    "module graph cannot resolve for any importer, whatever it imports",
    "apps/ui/src/components/graph/brainView.ts",
    "    return { ...n };\n  });\n}\n",
    "    return { ...n };\n  });\n}\n\nexport const __ROUTE_PROOF_SYNTAX_ERROR__ = (((;\n",
    "ts",
)

MUTATIONS = [
    Mutation(
        "m1 promptListEntries keeps a synapse the visible layout lacks",
        "apps/ui/src/components/graph/brainView.ts",
        '    .filter((n) => n.kind === "synapse" && visibleIds.has(n.id))\n',
        '    .filter((n) => n.kind === "synapse")\n',
        "ts",
    ),
    Mutation(
        "m2 promptListEntries answers in_progress rather than current",
        "apps/ui/src/components/graph/brainView.ts",
        '  in_progress: "current",\n',
        "",
        "ts",
    ),
    Mutation(
        "m3 promptListEntries answers an entry for a test_run",
        "apps/ui/src/components/graph/brainView.ts",
        '    .filter((n) => n.kind === "synapse" && visibleIds.has(n.id))\n',
        '    .filter((n) => (n.kind === "synapse" || n.kind === "test_run") && visibleIds.has(n.id))\n',
        "ts",
    ),
    Mutation(
        "m4 the list's button calls onSelect(entry.nodeId)",
        "apps/ui/src/components/graph/PromptNodeList.tsx",
        "              onClick={() => onSelect(entry.promptId)}\n",
        "              onClick={() => onSelect(entry.nodeId)}\n",
        "py",
    ),
    Mutation(
        "m5 the style module hides the nav with display: none",
        "apps/ui/src/components/graph/PromptNodeList.module.css",
        "  clip-path: inset(50%);\n}\n",
        "  clip-path: inset(50%);\n  display: none;\n}\n",
        "py",
    ),
    Mutation(
        "m6 the stage renders <PromptNodeList in the simple branch instead of the live one",
        "apps/ui/src/components/graph/BrainGraphStage.tsx",
        (
            "          <PromptNodeList entries={promptEntries} selectedId={selectedId} onSelect={(promptId) => onSelectNode(promptId)} />\n"
            "          {focusedRun && zoom.state.level === 2 && (\n"
            "            <RunDetailPopover\n"
            "              node={focusedRun}\n"
            "              rows={rows}\n"
            "              promptItems={dashboard.promptTrace?.items ?? []}\n"
            "              jobId={dashboard.jobId}\n"
            "              token={serverToken}\n"
            "              onOpenEvidence={(tab) => zoom.dispatch({ type: \"open_evidence\", tab })}\n"
            "              onClose={() => zoom.dispatch({ type: \"escape\" })}\n"
            "            />\n"
            "          )}\n"
            "          {focusedRun && zoom.state.level === 3 && zoom.state.tab !== null && (\n"
            "            <EvidencePanel\n"
            "              node={focusedRun}\n"
            "              tab={zoom.state.tab}\n"
            "              rows={rows}\n"
            "              promptItems={dashboard.promptTrace?.items ?? []}\n"
            "              jobId={dashboard.jobId}\n"
            "              token={serverToken}\n"
            "              onTab={(tab) => zoom.dispatch({ type: \"open_evidence\", tab })}\n"
            "              onClose={() => zoom.dispatch({ type: \"escape\" })}\n"
            "            />\n"
            "          )}\n"
            "        </>\n"
            "      ) : (\n"
            "        // No tasks, an empty filter, or the operator pressed \"Simple view\":\n"
            "        // BrainGraphCanvas owns its own empty and filter-empty messages.\n"
            "        <BrainGraphCanvas dashboard={dashboard} filter={filter} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />\n"
            "      )}\n"
        ),
        (
            "          {focusedRun && zoom.state.level === 2 && (\n"
            "            <RunDetailPopover\n"
            "              node={focusedRun}\n"
            "              rows={rows}\n"
            "              promptItems={dashboard.promptTrace?.items ?? []}\n"
            "              jobId={dashboard.jobId}\n"
            "              token={serverToken}\n"
            "              onOpenEvidence={(tab) => zoom.dispatch({ type: \"open_evidence\", tab })}\n"
            "              onClose={() => zoom.dispatch({ type: \"escape\" })}\n"
            "            />\n"
            "          )}\n"
            "          {focusedRun && zoom.state.level === 3 && zoom.state.tab !== null && (\n"
            "            <EvidencePanel\n"
            "              node={focusedRun}\n"
            "              tab={zoom.state.tab}\n"
            "              rows={rows}\n"
            "              promptItems={dashboard.promptTrace?.items ?? []}\n"
            "              jobId={dashboard.jobId}\n"
            "              token={serverToken}\n"
            "              onTab={(tab) => zoom.dispatch({ type: \"open_evidence\", tab })}\n"
            "              onClose={() => zoom.dispatch({ type: \"escape\" })}\n"
            "            />\n"
            "          )}\n"
            "        </>\n"
            "      ) : (\n"
            "        // No tasks, an empty filter, or the operator pressed \"Simple view\":\n"
            "        // BrainGraphCanvas owns its own empty and filter-empty messages.\n"
            "        <BrainGraphCanvas dashboard={dashboard} filter={filter} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />\n"
            "        <PromptNodeList entries={promptEntries} selectedId={selectedId} onSelect={(promptId) => onSelectNode(promptId)} />\n"
            "      )}\n"
        ),
        "py",
    ),
    Mutation(
        "m7 the harness, run on a worktree whose PromptNodeList.tsx calls onSelect(entry.nodeId), must exit non-zero with C-e failing",
        "apps/ui/src/components/graph/PromptNodeList.tsx",
        "              onClick={() => onSelect(entry.promptId)}\n",
        "              onClick={() => onSelect(entry.nodeId)}\n",
        "harness",
    ),
]


def purge_pycache(root: Path) -> None:
    for d in root.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def write_scratch_config(worktree: Path) -> None:
    WORKER_DIR.mkdir(parents=True, exist_ok=True)
    includes = ",\n      ".join(f'"{(worktree / rel).as_posix()}"' for rel in TS_TEST_RELPATHS)
    config = (
        "export default {\n"
        f'  root: "{PRIMARY_UI.as_posix()}",\n'
        f'  cacheDir: "{SCRATCH_CACHE_DIR.as_posix()}",\n'
        "  test: {\n"
        '    environment: "node",\n'
        "    include: [\n"
        f"      {includes}\n"
        "    ],\n"
        "  },\n"
        "};\n"
    )
    SCRATCH_CONFIG.write_text(config, encoding="utf-8")


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.returncode, proc.stdout


def pytest_failed_count_and_names(output: str) -> tuple[int, list[str]]:
    names = sorted(set(re.findall(r"^FAILED (\S+)", output, re.MULTILINE)))
    m = re.search(r"(\d+) failed", output)
    count = int(m.group(1)) if m else 0
    if m is None and re.search(r"^ERROR ", output, re.MULTILINE):
        count = len(re.findall(r"^ERROR ", output, re.MULTILINE)) or count
    return count, names


def vitest_failed_count_and_names(output: str) -> tuple[int, list[str]]:
    names = sorted(set(re.findall(r"^\s*FAIL\s+(.+)$", output, re.MULTILINE)))
    m = re.search(r"Tests\s+(\d+) failed", output)
    if m is not None:
        count = int(m.group(1))
    else:
        count = 1 if names or re.search(r"\bError\b", output) else 0
    return count, names


def harness_failed_count_and_names(output: str) -> tuple[int, list[str]]:
    names = sorted(set(re.findall(r"^FAILED ([^:]+):", output, re.MULTILINE)))
    return len(names), names


def run_py_tests(worktree: Path) -> tuple[int, int, list[str]]:
    purge_pycache(worktree)
    code, out = run(["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PY_TESTS], cwd=worktree)
    failed, names = pytest_failed_count_and_names(out)
    return code, failed, names


def run_ts_tests(worktree: Path) -> tuple[int, int, list[str]]:
    write_scratch_config(worktree)
    code, out = run([str(VITEST_BIN), "run", "--config", str(SCRATCH_CONFIG)], cwd=PRIMARY_UI)
    failed, names = vitest_failed_count_and_names(out)
    return code, failed, names


def run_harness(worktree: Path) -> tuple[int, int, list[str]]:
    measure = worktree / HARNESS_MEASURE_REL
    code, out = run(["python3", str(measure), str(worktree)], cwd=worktree)
    failed, names = harness_failed_count_and_names(out)
    return code, failed, names


def symlink_worktree_node_modules(worktree: Path) -> Path:
    link = worktree / "apps" / "ui" / "node_modules"
    if not link.exists():
        link.symlink_to(PRIMARY_NODE_MODULES, target_is_directory=True)
    return link


def remove_symlink(link: Path) -> None:
    if link.is_symlink() or link.exists():
        link.unlink()


def apply_edit(path: Path, from_text: str, to_text: str) -> str:
    original = path.read_text(encoding="utf-8")
    if original.count(from_text) != 1:
        raise SystemExit(f"FROM text does not occur exactly once in {path}: {original.count(from_text)}")
    path.write_text(original.replace(from_text, to_text, 1), encoding="utf-8")
    return original


def restore(path: Path, original: str) -> bool:
    path.write_text(original, encoding="utf-8")
    return path.read_text(encoding="utf-8") == original


def report_run(label: str, runner: str, code: int, failed: int, names: list[str]) -> None:
    print(f"[{runner}] {label}")
    print(f"  exit={code} failed={failed}")
    for n in names:
        print(f"    failing: {n}")


def main() -> None:
    worktree = Path(sys.argv[1]).resolve()
    all_caught = True
    restored_all = True

    print("=== ROUTE PROOF (before any of m1-m3) ===")
    rp_path = worktree / ROUTE_PROOF.rel_path
    rp_original = apply_edit(rp_path, ROUTE_PROOF.from_text, ROUTE_PROOF.to_text)
    code, failed, names = run_ts_tests(worktree)
    report_run(ROUTE_PROOF.label, "ts", code, failed, names)
    route_proof_red = code != 0
    ok = restore(rp_path, rp_original)
    print(f"  restored byte-identical: {ok}")
    all_caught = all_caught and route_proof_red
    restored_all = restored_all and ok
    if not route_proof_red:
        print("  ROUTE PROOF DID NOT REDDEN — the vitest route is not reading the worktree's sources.")

    print("\n=== TypeScript runner (vitest): control, then m1-m3, then control ===")
    code, failed, names = run_ts_tests(worktree)
    report_run("CONTROL (unmutated)", "ts", code, failed, names)
    all_caught = all_caught and code == 0

    for mutation in MUTATIONS:
        if mutation.runner != "ts":
            continue
        path = worktree / mutation.rel_path
        original = apply_edit(path, mutation.from_text, mutation.to_text)
        code, failed, names = run_ts_tests(worktree)
        report_run(mutation.label, "ts", code, failed, names)
        red = code != 0
        if not red:
            print("  GREEN — this mutation was NOT caught.")
        all_caught = all_caught and red
        ok = restore(path, original)
        restored_all = restored_all and ok
        print(f"  restored byte-identical: {ok}")

    code, failed, names = run_ts_tests(worktree)
    report_run("CONTROL (unmutated)", "ts", code, failed, names)
    all_caught = all_caught and code == 0

    print("\n=== Python runner (pytest): control, then m4-m6, then control ===")
    code, failed, names = run_py_tests(worktree)
    report_run("CONTROL (unmutated)", "py", code, failed, names)
    all_caught = all_caught and code == 0

    for mutation in MUTATIONS:
        if mutation.runner != "py":
            continue
        path = worktree / mutation.rel_path
        original = apply_edit(path, mutation.from_text, mutation.to_text)
        code, failed, names = run_py_tests(worktree)
        report_run(mutation.label, "py", code, failed, names)
        red = code != 0
        if not red:
            print("  GREEN — this mutation was NOT caught.")
        all_caught = all_caught and red
        ok = restore(path, original)
        restored_all = restored_all and ok
        print(f"  restored byte-identical: {ok}")

    code, failed, names = run_py_tests(worktree)
    report_run("CONTROL (unmutated)", "py", code, failed, names)
    all_caught = all_caught and code == 0

    print("\n=== Harness runner: control, then m7, then control ===")
    link = symlink_worktree_node_modules(worktree)
    print(f"  symlinked {link} -> {PRIMARY_NODE_MODULES}")

    code, failed, names = run_harness(worktree)
    report_run("CONTROL (unmutated)", "harness", code, failed, names)
    all_caught = all_caught and code == 0

    m7 = next(m for m in MUTATIONS if m.runner == "harness")
    path = worktree / m7.rel_path
    original = apply_edit(path, m7.from_text, m7.to_text)
    code, failed, names = run_harness(worktree)
    report_run(m7.label, "harness", code, failed, names)
    red = code != 0
    c_e_failed = any(n.startswith("C-e") for n in names)
    if not red:
        print("  GREEN — this mutation was NOT caught.")
    elif not c_e_failed:
        print(f"  RED, but not via C-e — failing checks: {names}")
    all_caught = all_caught and red and c_e_failed
    ok = restore(path, original)
    restored_all = restored_all and ok
    print(f"  restored byte-identical: {ok}")

    code, failed, names = run_harness(worktree)
    report_run("CONTROL (unmutated)", "harness", code, failed, names)
    all_caught = all_caught and code == 0

    remove_symlink(link)
    print(f"  removed symlink {link}")

    print(f"\nALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {bool(all_caught and restored_all)}")


if __name__ == "__main__":
    main()

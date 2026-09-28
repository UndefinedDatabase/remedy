#!/usr/bin/env python3
"""F038 R13 G3 — the round's red proofs.

Takes one worktree path and runs two kinds of mutation over the round's own product code:
VITEST, through the primary's own `vitest` binary and a scratch config, over the round's two
touched vitest files (`chatTurn.test.ts`, `evidenceChatAudit.test.ts`); PYTEST, over
`tests/ui_contracts/test_chat_citations.py`, `tests/orchestration/test_chat_answer.py` and
`tests/cli/test_chat_ask.py`, run from the worktree's own root after its `__pycache__`
directories are purged.

Each mutation asserts its FROM text occurs exactly once in the worktree's file, runs its
runner, restores the bytes, and prints its label, the exit code, the failed count and the
failing names. Controls of both runners run first and last, so a change to either wrapper
itself — not just to a mutation's own target — would be caught too. A mutation that stays
GREEN is reported as green, never papered over. Built as round 12's own
`f038-r12-mutations.py` is.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRIMARY_VITEST = REPO_ROOT / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
SCRATCH_DIR = REPO_ROOT / ".remedy-wt" / "f038-r13-worker"

VITEST_TEST_FILES = (
    "apps/ui/src/api/chatTurn.test.ts",
    "apps/ui/src/components/graph/evidenceChatAudit.test.ts",
)

PYTEST_SELECTION = (
    "tests/ui_contracts/test_chat_citations.py",
    "tests/orchestration/test_chat_answer.py",
    "tests/cli/test_chat_ask.py",
)

TOUCHED_PATHS = (
    "packages/orchestration/chat_answer.py",
    "apps/cli/commands/chat_cmd.py",
    "apps/ui/src/api/chatTurn.ts",
    "apps/ui/src/components/graph/EvidenceChatTab.tsx",
)


@dataclass(frozen=True)
class Mutation:
    label: str
    path: str
    from_text: str
    to_text: str
    runner: str  # "vitest" or "pytest"


VITEST_MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        "m3 the summary sentence changed",
        "apps/ui/src/api/chatTurn.ts",
        'export const CHAT_GENERATOR_LINE_SUMMARY_ROLE =\n'
        '  "Written by the summary model; every sentence was checked against the job\'s records.";',
        'export const CHAT_GENERATOR_LINE_SUMMARY_ROLE = "changed";',
        "vitest",
    ),
    Mutation(
        "m4 the tab's generator line not rendered",
        "apps/ui/src/components/graph/EvidenceChatTab.tsx",
        '          <p className={styles.generatorLine} data-ui="chat-generator">'
        '{chatGeneratorLine(view.generator)}</p>\n'
        "          {view.sentences.map((sentence, index) => {",
        "          {view.sentences.map((sentence, index) => {",
        "vitest",
    ),
)

PYTEST_MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        "m1 a mechanical: label answered the unknown sentence",
        "packages/orchestration/chat_answer.py",
        '    if generator.startswith(f"{CHAT_GENERATOR_MECHANICAL}:"):\n'
        "        return CHAT_GENERATOR_LINE_MECHANICAL_FALLBACK",
        '    if generator.startswith(f"{CHAT_GENERATOR_MECHANICAL}:"):\n'
        "        return CHAT_GENERATOR_LINE_UNKNOWN",
        "pytest",
    ),
    Mutation(
        "m2 the generator line not printed",
        "apps/cli/commands/chat_cmd.py",
        "    print(chat_generator_line(answer.generator))\n"
        "    print(render_chat_answer(answer))",
        "    print(render_chat_answer(answer))",
        "pytest",
    ),
    Mutation(
        "m5 the tab's sending: true update deleted",
        "apps/ui/src/components/graph/EvidenceChatTab.tsx",
        "setTurns((sofar) => sofar.map((turn) => (turn.key === key ? { ...turn, sending: true } : turn)));",
        "setTurns((sofar) => sofar.map((turn) => (turn.key === key ? { ...turn } : turn)));",
        "pytest",
    ),
    Mutation(
        "m6 the mechanical constant's sentence changed",
        "packages/orchestration/chat_answer.py",
        'CHAT_GENERATOR_LINE_MECHANICAL = "Built from the job\'s records, without a model."',
        'CHAT_GENERATOR_LINE_MECHANICAL = "changed"',
        "pytest",
    ),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def symlink_node_modules(worktree: Path) -> None:
    """So `react` resolves in a worktree that never ran its own `npm install`."""
    target = worktree / "apps" / "ui" / "node_modules"
    source = REPO_ROOT / "apps" / "ui" / "node_modules"
    if target.is_symlink() or target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(source, target, target_is_directory=True)


def write_vitest_config(worktree: Path) -> Path:
    """A plain scratch config: `root` the worktree's `apps/ui`, a cache directory under
    `.remedy-wt/`, `test.environment` `"node"`, and `test.include` the worktree's two touched
    vitest files by absolute path."""
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = SCRATCH_DIR / "vitest-cache"
    config_path = SCRATCH_DIR / "vitest.scratch.config.ts"
    ui_root = worktree / "apps" / "ui"
    include_files = [str(worktree / relpath) for relpath in VITEST_TEST_FILES]
    include_literal = ", ".join(json.dumps(f) for f in include_files)
    # An ABSOLUTE import: the scratch config lives under `.remedy-wt/f038-r13-worker/`, well
    # outside any `node_modules`, so a bare `"vitest/config"` specifier cannot resolve from
    # there. The primary's own copy is imported by path instead — the same copy the symlink
    # below points the worktree's `apps/ui/node_modules` at.
    defineconfig_path = REPO_ROOT / "apps" / "ui" / "node_modules" / "vitest" / "dist" / "config.js"
    config_path.write_text(
        f'import {{ defineConfig }} from {json.dumps(str(defineconfig_path))};\n'
        "export default defineConfig({\n"
        f"  root: {json.dumps(str(ui_root))},\n"
        f"  cacheDir: {json.dumps(str(cache_dir))},\n"
        "  test: {\n"
        '    environment: "node",\n'
        f"    include: [{include_literal}],\n"
        "  },\n"
        "});\n",
        encoding="utf-8",
    )
    return config_path


def run_vitest(worktree: Path, config_path: Path) -> tuple[int, int, list[str]]:
    report_path = SCRATCH_DIR / "vitest-report.json"
    if report_path.exists():
        report_path.unlink()
    proc = subprocess.run(
        [str(PRIMARY_VITEST), "run", "--config", str(config_path),
         "--reporter=json", f"--outputFile={report_path}"],
        cwd=str(worktree / "apps" / "ui"),
        capture_output=True, text=True,
    )
    exit_code = proc.returncode
    failed_names: list[str] = []
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            report = None
        if report is not None:
            for test_result in report.get("testResults", []):
                for assertion in test_result.get("assertionResults", []):
                    if assertion.get("status") == "failed":
                        failed_names.append(assertion.get("fullName") or assertion.get("title", ""))
    return exit_code, len(failed_names), failed_names


def purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        for item in cache_dir.rglob("*"):
            if item.is_file():
                item.unlink()
        try:
            cache_dir.rmdir()
        except OSError:
            pass


def run_pytest(worktree: Path) -> tuple[int, int, list[str]]:
    purge_pycache(worktree)
    proc = subprocess.run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf", *PYTEST_SELECTION],
        cwd=str(worktree), capture_output=True, text=True,
    )
    exit_code = proc.returncode
    failed_names = [
        line[len("FAILED "):].split(" - ", 1)[0].strip()
        for line in proc.stdout.splitlines()
        if line.startswith("FAILED ")
    ]
    return exit_code, len(failed_names), failed_names


def apply_mutation(worktree: Path, mutation: Mutation) -> bytes:
    target = worktree / mutation.path
    original = target.read_bytes()
    text = original.decode("utf-8")
    count = text.count(mutation.from_text)
    if count != 1:
        raise AssertionError(
            f"{mutation.label}: FROM text occurs {count} times in {mutation.path}, expected 1"
        )
    mutated = text.replace(mutation.from_text, mutation.to_text, 1)
    target.write_bytes(mutated.encode("utf-8"))
    return original


def restore(worktree: Path, mutation: Mutation, original: bytes) -> bool:
    target = worktree / mutation.path
    target.write_bytes(original)
    return target.read_bytes() == original


def run_control(worktree: Path, config_path: Path, label: str, state: dict) -> None:
    print(f"=== CONTROL ({label}) — VITEST ===")
    exit_code, failed_count, failed_names = run_vitest(worktree, config_path)
    print(f"exit={exit_code} failed={failed_count} names={failed_names}")
    if exit_code != 0 or failed_count != 0:
        state["all_caught"] = False
        print(f"CONTROL VITEST ({label}) DID NOT PASS")

    print(f"=== CONTROL ({label}) — PYTEST ===")
    exit_code, failed_count, failed_names = run_pytest(worktree)
    print(f"exit={exit_code} failed={failed_count} names={failed_names}")
    if exit_code != 0 or failed_count != 0:
        state["all_caught"] = False
        print(f"CONTROL PYTEST ({label}) DID NOT PASS")


def run_mutation(worktree: Path, config_path: Path, mutation: Mutation, state: dict) -> None:
    original = apply_mutation(worktree, mutation)
    if mutation.runner == "vitest":
        exit_code, failed_count, failed_names = run_vitest(worktree, config_path)
    else:
        exit_code, failed_count, failed_names = run_pytest(worktree)
    restored_ok = restore(worktree, mutation, original)
    went_red = exit_code != 0 or failed_count > 0
    print(f"{mutation.label}: exit={exit_code} failed={failed_count} names={failed_names} "
          f"restored={restored_ok}")
    if not went_red:
        state["all_caught"] = False
        print(f"  GREEN — NOT CAUGHT: {mutation.label}")
    if not restored_ok:
        state["all_caught"] = False
        print(f"  RESTORE FAILED: {mutation.label}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f038-r13-mutations.py <worktree-path>")
        return 2
    worktree = Path(sys.argv[1]).resolve()

    symlink_node_modules(worktree)
    config_path = write_vitest_config(worktree)

    state = {"all_caught": True}
    baseline_hashes = {path: sha256_bytes((worktree / path).read_bytes()) for path in TOUCHED_PATHS}

    run_control(worktree, config_path, "pre", state)

    for mutation in VITEST_MUTATIONS:
        run_mutation(worktree, config_path, mutation, state)
    for mutation in PYTEST_MUTATIONS:
        run_mutation(worktree, config_path, mutation, state)

    run_control(worktree, config_path, "post", state)

    byte_identical = True
    for path, expected_hash in baseline_hashes.items():
        actual_hash = sha256_bytes((worktree / path).read_bytes())
        if actual_hash != expected_hash:
            byte_identical = False
            print(f"BYTE MISMATCH after restoration: {path}")

    print(f"restored byte-identical: {byte_identical}")
    all_clean = state["all_caught"] and byte_identical
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_clean}")
    return 0 if all_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())

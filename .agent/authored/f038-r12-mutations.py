#!/usr/bin/env python3
"""F038 R12 G5 — the round's red proofs.

Takes one worktree path and runs two kinds of mutation over the round's own product code:
VITEST, through the primary's own `vitest` binary and a scratch config, over the round's two
touched vitest files (`chatTurn.test.ts`, `evidenceChatAudit.test.ts`); PYTEST, over
`tests/ui_contracts/test_chat_citations.py` and `tests/ui_server/test_chat_e2e_live.py`, run
from the worktree's own root after its `__pycache__` directories are purged.

Each mutation asserts its FROM text occurs exactly once in the worktree's file, runs its
runner, restores the bytes, and prints its label, the exit code, the failed count and the
failing names. Controls of both runners run first and last, so a change to either wrapper
itself — not just to a mutation's own target — would be caught too. A mutation that stays
GREEN is reported as green, never papered over.
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
SCRATCH_DIR = REPO_ROOT / ".remedy-wt" / "f038-r12-worker"

VITEST_TEST_FILES = (
    "apps/ui/src/api/chatTurn.test.ts",
    "apps/ui/src/components/graph/evidenceChatAudit.test.ts",
)

PYTEST_SELECTION = (
    "tests/ui_contracts/test_chat_citations.py",
    "tests/ui_server/test_chat_e2e_live.py",
)

TOUCHED_PATHS = (
    "apps/ui/src/api/chatTurn.ts",
    "apps/ui/src/components/graph/EvidenceChatTab.tsx",
    "packages/orchestration/ui_server.py",
    "packages/orchestration/chat_intent.py",
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
        "r1 an answer with no sentence decoded",
        "apps/ui/src/api/chatTurn.ts",
        '|| !Array.isArray(rawEvidence) || typeof omitted !== "number" || !Number.isInteger(omitted)\n'
        '      || !Array.isArray(rawSentences) || rawSentences.length === 0) {',
        '|| !Array.isArray(rawEvidence) || typeof omitted !== "number" || !Number.isInteger(omitted)\n'
        '      || !Array.isArray(rawSentences)) {',
        "vitest",
    ),
    Mutation(
        "r2 a card arg that is not a string decoded",
        "apps/ui/src/api/chatTurn.ts",
        'if (typeof value !== "string") return null;',
        "if (false) return null;",
        "vitest",
    ),
    Mutation(
        "r3 unknown_task's line replaced by the code",
        "apps/ui/src/api/chatTurn.ts",
        'if (reason === "unknown_task") return "This task is not part of the job, so nothing was asked.";',
        'if (reason === "unknown_task") return reason;',
        "vitest",
    ),
    Mutation(
        "r4 the 409 sentence replaced by the decision-inbox one",
        "apps/ui/src/api/chatTurn.ts",
        'const CHAT_CARD_CLOSED_SENTENCE = "The job refused it in its current state, so nothing was done.";',
        'const CHAT_CARD_CLOSED_SENTENCE = '
        '"This decision is no longer open. It may already have been answered.";',
        "vitest",
    ),
    Mutation(
        "r5 both open labels 'Open'",
        "apps/ui/src/api/chatTurn.ts",
        'return tab === "diff" ? "Open the diff" : "Open the prompt trace";',
        'return "Open";',
        "vitest",
    ),
    Mutation(
        "r6 Confirm rendered while sending",
        "apps/ui/src/components/graph/EvidenceChatTab.tsx",
        "{!sending && chatCardCanConfirm(view, outcome) && (",
        "{chatCardCanConfirm(view, outcome) && (",
        "vitest",
    ),
    Mutation(
        "r7 an unavailable turn showing its code",
        "apps/ui/src/components/graph/EvidenceChatTab.tsx",
        "{chatUnavailableLine(view.reason)}",
        "{view.reason}",
        "vitest",
    ),
    Mutation(
        "r8 the open button reading 'Open'",
        "apps/ui/src/components/graph/EvidenceChatTab.tsx",
        "{chatEvidenceTabLabel(tab)}",
        "Open",
        "vitest",
    ),
)

PYTEST_MUTATIONS: tuple[Mutation, ...] = (
    Mutation(
        "r9 the input's aria-label removed",
        "apps/ui/src/components/graph/EvidenceChatTab.tsx",
        'aria-label="Ask the chat"',
        'aria-label="Ask"',
        "pytest",
    ),
    Mutation(
        "r10 the chat route drops the task",
        "packages/orchestration/ui_server.py",
        'task = (qs.get("task") or [""])[0]',
        'task = ""',
        "pytest",
    ),
    Mutation(
        "r11 'stop' removed from _STOP_WORDS",
        "packages/orchestration/chat_intent.py",
        '_STOP_WORDS = frozenset({"stop", "cancel", "abort"})',
        '_STOP_WORDS = frozenset({"cancel", "abort"})',
        "pytest",
    ),
    Mutation(
        "r12 the stop intent built as job.pause with no arguments",
        "packages/orchestration/chat_intent.py",
        'return chat_action_intent("job.stop", {"reason": _reason_after_because(folded)})',
        'return chat_action_intent("job.pause", {})',
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
    # An ABSOLUTE import: the scratch config lives under `.remedy-wt/f038-r12-worker/`, well
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
        print("usage: f038-r12-mutations.py <worktree-path>")
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

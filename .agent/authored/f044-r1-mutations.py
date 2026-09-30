"""F044 R1 C6 — the round's red-proof tool (G4). Takes a worktree path, and for each mutation
edits the named production file INSIDE that worktree (asserting its FROM text occurs exactly once
there), runs the named checks, restores the bytes, and prints one line per mutation: its label,
and per check the exit code and the failed count. Runs an unmutated control of both checks first
and last. Never edited by hand once a round's G4 has run against it — a red proof this script
prints is the tool's own claim about its own behaviour, not a paraphrase.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
VITEST_CONFIG = PRIMARY / "apps" / "ui" / "vitest.config.ts"
VITEST_TEST_FILES = [
    "src/api/fuzzyMatch.test.ts",
    "src/api/paletteCommands.test.ts",
    "src/api/paletteJump.test.ts",
    "src/api/paletteRouting.test.ts",
]
CONTRACT_TEST = "tests/ui_contracts/test_palette_contract.py"


def run_vitest(worktree: Path) -> tuple[int, int]:
    cmd = [
        str(VITEST_BIN), "run",
        "--root", str(worktree / "apps" / "ui"),
        "--config", str(VITEST_CONFIG),
        *VITEST_TEST_FILES,
    ]
    proc = subprocess.run(
        cmd, cwd=str(worktree / "apps" / "ui"),
        capture_output=True, text=True, check=False,
    )
    output = proc.stdout + proc.stderr
    match = re.search(r"Tests\s+(?:(\d+) failed \| )?(\d+) passed", output)
    failed = int(match.group(1)) if match and match.group(1) else 0
    if match is None:
        # No clean summary line (e.g. a collection error) counts as every test failed.
        failed = len(VITEST_TEST_FILES) if proc.returncode != 0 else 0
    return proc.returncode, failed


def run_contract(worktree: Path) -> tuple[int, int]:
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", CONTRACT_TEST]
    proc = subprocess.run(
        cmd, cwd=str(worktree), capture_output=True, text=True, check=False,
    )
    output = proc.stdout + proc.stderr
    match = re.search(r"(\d+) failed", output)
    failed = int(match.group(1)) if match else 0
    error_match = re.search(r"(\d+) error", output)
    if error_match and failed == 0:
        failed = int(error_match.group(1))
    return proc.returncode, failed


CHECKS = {"vitest": run_vitest, "contract": run_contract}

# label, file (relative to worktree), FROM text, TO text, checks that must go red
MUTATIONS = [
    (
        "f1", "apps/ui/src/api/fuzzyMatch.ts",
        'function fold(text: string): string {\n'
        '  let out = "";\n'
        '  for (let i = 0; i < text.length; i += 1) {\n'
        '    out += foldUnit(text[i]);\n'
        '  }\n'
        '  return out;\n'
        '}',
        'function fold(text: string): string {\n'
        '  return text.toLowerCase();\n'
        '}',
        ["vitest"],
    ),
    (
        "f2", "apps/ui/src/api/fuzzyMatch.ts",
        'function firstContiguousHit(\n'
        '  foldedText: string,\n'
        '  foldedQuery: string,\n'
        '): { index: number; wordStart: boolean } | null {\n'
        '  const firstIndex = foldedText.indexOf(foldedQuery);\n'
        '  if (firstIndex === -1) return null;\n'
        '  let searchFrom = 0;\n'
        '  for (;;) {\n'
        '    const found = foldedText.indexOf(foldedQuery, searchFrom);\n'
        '    if (found === -1) break;\n'
        '    if (isWordStart(foldedText, found)) return { index: found, wordStart: true };\n'
        '    searchFrom = found + 1;\n'
        '  }\n'
        '  return { index: firstIndex, wordStart: false };\n'
        '}',
        'function firstContiguousHit(\n'
        '  foldedText: string,\n'
        '  foldedQuery: string,\n'
        '): { index: number; wordStart: boolean } | null {\n'
        '  const firstIndex = foldedText.indexOf(foldedQuery);\n'
        '  if (firstIndex === -1) return null;\n'
        '  return { index: firstIndex, wordStart: false };\n'
        '}',
        ["vitest"],
    ),
    (
        "f3", "apps/ui/src/api/fuzzyMatch.ts",
        "- Math.min(contiguous.index, FUZZY_SUBSEQUENCE_CAP);",
        "- contiguous.index;",
        ["vitest"],
    ),
    (
        "f4", "apps/ui/src/api/fuzzyMatch.ts",
        "if (previousIndex !== -1 && found === previousIndex + 1) hitScore += 2;",
        "if (previousIndex !== -1 && found === previousIndex + 1) hitScore += 0;",
        ["vitest"],
    ),
    (
        "f5", "apps/ui/src/api/fuzzyMatch.ts",
        "    if (a.text.length !== b.text.length) return a.text.length - b.text.length;\n",
        "",
        ["vitest"],
    ),
    (
        "c1", "apps/ui/src/api/paletteCommands.ts",
        '  {\n'
        '    command: "job.preview-stop",\n'
        '    title: "Stop the app preview",\n'
        '    flow: "send",\n'
        '    surface: "",\n'
        '    args: [],\n'
        '  },\n',
        "",
        ["vitest", "contract"],
    ),
    (
        "c2", "apps/ui/src/api/paletteCommands.ts",
        'title: "Veto the task",',
        'title: "Veto a task",',
        ["vitest", "contract"],
    ),
    (
        "r1", "apps/ui/src/api/paletteRouting.ts",
        '  if (stripped.endsWith("?") || opensWithQuestionWord(stripped)) return { kind: "chat" };\n'
        '\n'
        '  const firstWord = stripped.split(" ", 1)[0].toLowerCase();\n'
        '  if (Object.prototype.hasOwnProperty.call(BAR_LEADING_VERBS, firstWord)) {\n'
        '    return { kind: "command", command: BAR_LEADING_VERBS[firstWord] };\n'
        '  }',
        '  const firstWord = stripped.split(" ", 1)[0].toLowerCase();\n'
        '  if (Object.prototype.hasOwnProperty.call(BAR_LEADING_VERBS, firstWord)) {\n'
        '    return { kind: "command", command: BAR_LEADING_VERBS[firstWord] };\n'
        '  }\n'
        '\n'
        '  if (stripped.endsWith("?") || opensWithQuestionWord(stripped)) return { kind: "chat" };',
        ["vitest"],
    ),
    (
        "r2", "apps/ui/src/api/paletteRouting.ts",
        "function startsWithWholePhrase(text: string, phrase: string): boolean {\n"
        "  if (text.slice(0, phrase.length).toLowerCase() !== phrase) return false;\n"
        "  const rest = text[phrase.length];\n"
        "  return rest === undefined || !/[\\p{L}\\p{N}_]/u.test(rest);\n"
        "}",
        "function startsWithWholePhrase(text: string, phrase: string): boolean {\n"
        "  return text.slice(0, phrase.length).toLowerCase() === phrase;\n"
        "}",
        ["vitest"],
    ),
    (
        "r3", "apps/ui/src/api/paletteRouting.ts",
        'function stripLeadingPlease(text: string): string {\n'
        '  return text.slice(0, 7).toLowerCase() === "please " ? text.slice(7) : text;\n'
        '}',
        'function stripLeadingPlease(text: string): string {\n'
        '  return text;\n'
        '}',
        ["vitest"],
    ),
    (
        "r4", "apps/ui/src/api/paletteRouting.ts",
        'return { kind: "command", command: focusedTaskId !== "" ? "job.steer" : "chat.send" };',
        'return { kind: "command", command: "chat.send" };',
        ["vitest"],
    ),
    (
        "r5", "apps/ui/src/api/paletteRouting.ts",
        '  "what", "why", "how", "when", "where", "which", "who", "did", "does", "do",\n'
        '  "is", "are", "was", "were", "can", "could", "has", "have",\n'
        '];',
        '  "what", "why", "how", "when", "where", "which", "who", "did", "does", "do",\n'
        '  "is", "are", "was", "were", "can", "could", "has", "have", "should",\n'
        '];',
        ["vitest", "contract"],
    ),
    (
        "j1", "apps/ui/src/api/paletteJump.ts",
        "if (match !== null && (best === null || match.score > best.match.score)) {",
        "if (match !== null && (best === null || match.score >= best.match.score)) {",
        ["vitest"],
    ),
    (
        "j2", "apps/ui/src/api/paletteJump.ts",
        '  if (query.trim() === "") {\n'
        '    return targets.slice(0, limit).map((target) => ({\n'
        '      target,\n'
        '      field: "label" as JumpField,\n'
        '      match: { score: 0, ranges: [] },\n'
        '    }));\n'
        '  }\n'
        '\n',
        "",
        ["vitest"],
    ),
    (
        "j3", "apps/ui/src/api/paletteJump.ts",
        "  targets.forEach((target, index) => {",
        "  targets.slice(0, limit).forEach((target, index) => {",
        ["vitest"],
    ),
]


def main() -> int:
    worktree = Path(sys.argv[1])
    all_clean = True

    print("CONTROL (before) —")
    v_code, v_failed = run_vitest(worktree)
    c_code, c_failed = run_contract(worktree)
    print(f"  vitest: exit={v_code} failed={v_failed}")
    print(f"  contract: exit={c_code} failed={c_failed}")
    if v_code != 0 or v_failed != 0 or c_code != 0 or c_failed != 0:
        all_clean = False
        print("  CONTROL DID NOT PASS CLEAN")

    for label, rel_path, from_text, to_text, checks in MUTATIONS:
        target = worktree / rel_path
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(from_text)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected 1")
            all_clean = False
            continue
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")

        results = []
        for check in checks:
            code, failed = CHECKS[check](worktree)
            results.append((check, code, failed))
            if code == 0 and failed == 0:
                all_clean = False

        target.write_bytes(original)
        restored = target.read_bytes()
        identical = restored == original
        if not identical:
            all_clean = False

        parts = ", ".join(f"{name} exit={code} failed={failed}" for name, code, failed in results)
        print(f"{label}: {parts}")
        print(f"  restored byte-identical: {identical}")

    print("CONTROL (after) —")
    v_code, v_failed = run_vitest(worktree)
    c_code, c_failed = run_contract(worktree)
    print(f"  vitest: exit={v_code} failed={v_failed}")
    print(f"  contract: exit={c_code} failed={c_failed}")
    if v_code != 0 or v_failed != 0 or c_code != 0 or c_failed != 0:
        all_clean = False
        print("  CONTROL DID NOT PASS CLEAN")

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_clean}")
    return 0 if all_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())

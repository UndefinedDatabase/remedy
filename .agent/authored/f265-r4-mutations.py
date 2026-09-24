"""F265 R4 G5 — mutation red-proofs of the Commands mode, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each run executes BOTH halves against the worktree's sources: pytest over
`tests/orchestration/test_lessons.py` and `tests/ui_contracts/test_lessons_overlay_contract.py`
inside the worktree, and vitest over `apps/ui/src/api/lessons.test.ts`, launched from the
PRIMARY `apps/ui` (a worktree has no node_modules) with a plain-object config whose cacheDir is
under `.remedy-wt/` (DECISION F256 D6). Each FROM is asserted to occur EXACTLY ONCE, the file is
restored byte-for-byte after each, and an unmutated control runs first and last. pytest runs
under `python3 -B` (checklist item 18). Nothing under the primary checkout is written.
"""
import json
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
PRIMARY_UI = pathlib.Path("/home/decodeux/Repos/remedy/apps/ui")
CFG_DIR = pathlib.Path("/home/decodeux/Repos/remedy/.remedy-wt/f265-r4-mutcfg")
PY = "packages/orchestration/lessons.py"
TS = "apps/ui/src/api/lessons.ts"
OV = "apps/ui/src/components/lessons/LessonsOverlay.tsx"
MUTATIONS = {
    "m1_a_changed_handler_module_touches_nothing": (
        PY, '               if str(getattr(handler, "__module__", "")).replace(".", "/") + ".py" in paths}\n',
        "               if False}\n"),
    "m2_a_changed_catalog_line_touches_nothing": (
        PY, "            touched.update(_CATALOG_ID.findall(line))\n", "            pass\n"),
    "m3_any_files_command_id_line_counts": (
        PY, '        elif current == CATALOG_PATH and line[:1] in "+-" and not line.startswith("---"):\n',
        '        elif line[:1] in "+-" and not line.startswith("---"):\n'),
    "m4_the_invocation_drops_the_group": (
        PY, '                         "invocation": f"remedy {entry.group_id} {entry.subcommand}",\n',
        '                         "invocation": f"remedy {entry.subcommand}",\n'),
    "m5_a_row_carries_no_commands": (
        PY, '            "commands": lesson_commands(read_run_diff(run_id, root) or "") if run_id else []}\n',
        '            "commands": []}\n'),
    "m6_the_decoder_drops_the_commands": (
        TS, "    commands: commands as LessonCommand[],\n", "    commands: [],\n"),
    "m7_no_line_for_a_task_without_commands": (
        TS, "  return row.commands.length === 0 ? \"This task's change touched no CLI command.\" : null;\n",
        "  return null;\n"),
    "m8_the_commands_switch_hides_its_state": (
        OV, '            aria-pressed={mode === "commands"} onClick={() => setMode("commands")}>Commands</button>\n',
        '            onClick={() => setMode("commands")}>Commands</button>\n'),
}


def vitest() -> str:
    CFG_DIR.mkdir(exist_ok=True)
    cfg = CFG_DIR / "vitest.config.mjs"
    cfg.write_text("export default " + json.dumps({
        "root": str(PRIMARY_UI), "cacheDir": str(CFG_DIR / "vite-cache"),
        "test": {"environment": "node", "include": [str(WT / "apps/ui/src/api/lessons.test.ts")]},
    }) + ";\n")
    r = subprocess.run([str(PRIMARY_UI / "node_modules/.bin/vitest"), "run", "--config", str(cfg)],
                       cwd=PRIMARY_UI, capture_output=True, text=True)
    tests = [ln.strip() for ln in (r.stdout + r.stderr).splitlines() if ln.strip().startswith("Tests ")]
    return f"vitest REAL_EXIT={r.returncode} {tests[-1] if tests else 'no summary'}"


def pytest() -> str:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        "tests/orchestration/test_lessons.py",
                        "tests/ui_contracts/test_lessons_overlay_contract.py"],
                       cwd=WT, capture_output=True, text=True)
    summary = [ln for ln in r.stdout.splitlines() if " passed" in ln or " failed" in ln]
    return f"pytest REAL_EXIT={r.returncode} {summary[-1] if summary else 'no summary'}"


def run(label: str) -> None:
    print(f"{label}: {pytest()} | {vitest()}")


run("control_before")
for name, (rel, frm, to) in MUTATIONS.items():
    path = WT / rel
    good = path.read_bytes()
    text = good.decode("utf-8")
    print(f"{name} FROM count in {rel}: {text.count(frm)}")
    if text.count(frm) != 1:
        sys.exit(f"{name}: FROM must occur exactly once; stopping")
    path.write_text(text.replace(frm, to, 1), encoding="utf-8")
    run(name)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
run("control_after")

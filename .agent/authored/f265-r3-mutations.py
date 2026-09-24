"""F265 R3 G5 — mutation red-proofs of the learning overlay, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each run executes BOTH halves against the worktree's sources: vitest over
`apps/ui/src/api/lessons.test.ts`, launched from the PRIMARY `apps/ui` (a worktree has no
node_modules) with a plain-object config whose cacheDir is under `.remedy-wt/` (DECISION F256
D6), and pytest over `tests/ui_contracts/test_lessons_overlay_contract.py` inside the worktree.
Each FROM is asserted to occur EXACTLY ONCE, the file is restored byte-for-byte after each, and
an unmutated control runs first and last. Nothing under the primary checkout is written.
"""
import json
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
PRIMARY_UI = pathlib.Path("/home/decodeux/Repos/remedy/apps/ui")
CFG_DIR = pathlib.Path("/home/decodeux/Repos/remedy/.remedy-wt/f265-r3-mutcfg")
LS = "apps/ui/src/api/lessons.ts"
API = "apps/ui/src/api/remedyApi.ts"
OV = "apps/ui/src/components/lessons/LessonsOverlay.tsx"
MUTATIONS = {
    "m1_a_bad_row_is_dropped_not_refused": (
        LS, "  if (rows.some((r) => r === null)) return null;\n", ""),
    "m2_the_overlay_opens_on_the_first_task": (
        LS, "  return first < 0 ? 0 : first;\n", "  return 0;\n"),
    "m3_next_runs_past_the_last_lesson": (
        LS, "    next: current + 1 < count ? current + 1 : null,\n", "    next: current + 1,\n"),
    "m4_any_frame_refreshes_the_index": (
        LS, "(row.kind === LESSON_WRITTEN_EVENT && row.seq > newest ? row.seq : newest), 0);\n",
        "(row.seq > newest ? row.seq : newest), 0);\n"),
    "m5_the_empty_line_ignores_the_switch": (
        LS, "  return index.lessonsEnabled\n", "  return true\n"),
    "m6_the_door_drops_the_token": (
        API, "    return decodeLessonsIndex(await fetchPayload(lessonsIndexPath(request)));\n",
        '    return decodeLessonsIndex(await fetchPayload(lessonsIndexPath({ ...request, token: "" })));\n'),
    "m7_the_decoder_reads_a_key_the_server_never_writes": (
        LS, '  const model = row["model"] === undefined ? "" : textOf(row["model"]);\n',
        '  const model = row["teacher_model"] === undefined ? "" : textOf(row["teacher_model"]);\n'),
    "m8_a_stale_answer_is_painted": (
        OV, "      if (!cancelled) setRead({ index });\n", "      setRead({ index });\n"),
    "m9_escape_does_not_close": (
        OV, '      if (event.key === "Escape") onClose();\n', '      if (event.key === "Enter") onClose();\n'),
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


def contract() -> str:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        "tests/ui_contracts/test_lessons_overlay_contract.py"],
                       cwd=WT, capture_output=True, text=True)
    summary = [ln for ln in r.stdout.splitlines() if " passed" in ln or " failed" in ln]
    return f"contract REAL_EXIT={r.returncode} {summary[-1] if summary else 'no summary'}"


def run(label: str) -> None:
    print(f"{label}: {vitest()} | {contract()}")


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

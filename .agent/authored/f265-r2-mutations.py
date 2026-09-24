"""F265 R2 G5 — mutation red-proofs of the lesson's announcement, stream field and route.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_lessons.py", "tests/ui_server/test_lessons_route.py"]
LS = "packages/orchestration/lessons.py"
PJ = "packages/orchestration/pingpong_job.py"
UI = "packages/orchestration/ui_server.py"
MUTATIONS = {
    "m1_a_stored_lesson_is_never_announced": (
        PJ,
        "        if not stored:\n",
        "        if False:\n",
    ),
    "m2_an_existing_lesson_is_announced_again": (
        PJ,
        "        stored = lessons.load_lesson(task.run_id) is not None\n",
        "        stored = False\n",
    ),
    "m3_the_hook_drops_the_mission": (
        PJ,
        '            task_title=task.title, mission_id=mission.id if mission is not None else "",\n',
        '            task_title=task.title, mission_id="",\n',
    ),
    "m4_the_stream_carries_no_lesson_field": (
        UI,
        '        summary["lesson"] = _lesson_summary_payload(metadata)\n',
        "        pass\n",
    ),
    "m5_the_stream_passes_any_status": (
        UI,
        '            "status": status if status in LESSON_STATUSES else ""}\n',
        '            "status": str(status)}\n',
    ),
    "m6_the_route_is_not_served": (
        UI,
        '                "lessons": _build_lessons_json,\n',
        "",
    ),
    "m7_a_tampered_lesson_breaks_the_index": (
        LS,
        "        except LessonError:\n",
        "        except ZeroDivisionError:\n",
    ),
    "m8_the_off_switch_is_not_named": (
        LS,
        '            reason = ("no lesson was stored for this run" if enabled else\n',
        '            reason = ("no lesson was stored for this run" if True else\n',
    ),
    "m9_a_task_that_never_ran_is_looked_up": (
        LS,
        "        if not run_id:\n",
        "        if False:\n",
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or " passed" in ln or " failed" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


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

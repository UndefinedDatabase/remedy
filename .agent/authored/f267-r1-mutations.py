"""F267 R1 G5 — mutation red-proofs that the catalog-wide handler test and the demo test can fail.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/cli/test_list_commands_everywhere.py"]
LISTING = "            sort=sort, desc=desc, since=since, until=until, limit=limit,\n"
IGNORED = "            sort=None, desc=desc, since=since, until=until, limit=limit,\n"
MUTATIONS = {
    "m1_change_list_ignores_sort": ("apps/cli/commands/change.py", LISTING, IGNORED),
    "m2_decision_list_ignores_sort": ("apps/cli/commands/decision.py", LISTING, IGNORED),
    "m3_mission_list_ignores_sort": ("apps/cli/commands/mission_cmd.py", LISTING, IGNORED),
    "m4_config_list_ignores_sort": (
        "apps/cli/commands/config_cmd.py",
        '            sort=getattr(args, "sort", None),\n',
        "            sort=None,\n",
    ),
    "m5_run_list_has_no_date": (
        "apps/cli/commands/do_cmd.py",
        '            date_getter=lambda r: r.get("finished_at") or None,\n',
        "            date_getter=None,\n",
    ),
    "m6_a_relative_bound_points_forward": (
        "packages/orchestration/list_options.py",
        "        return datetime.now(timezone.utc) - timedelta(**{unit: amount})\n",
        "        return datetime.now(timezone.utc) + timedelta(**{unit: amount})\n",
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

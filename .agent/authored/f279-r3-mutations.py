"""F279 R3 G5 — mutation red-proofs of the doctor environment report, the guide and the shell guard.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C4 commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_env_registry.py", "tests/docs/test_environment_guide.py",
         "tests/cli/test_worker_facade_cmd.py"]
MUTATIONS = {
    "m1_registered_names_called_unknown": (
        "packages/orchestration/config.py",
        "        if not name.startswith(ENV_PREFIX) or name in registered:\n",
        "        if not name.startswith(ENV_PREFIX):\n",
    ),
    "m2_every_boolean_word_accepted": (
        "packages/orchestration/config.py",
        "        return raw.lower() in BOOL_TRUE_WORDS + BOOL_FALSE_WORDS\n",
        "        return True\n",
    ),
    "m3_doctor_drops_the_unparsable_warning": (
        "apps/cli/commands/worker_facade_cmd.py",
        '        _warn("unparsable_env_variable",\n',
        '        (lambda *_: None)("unparsable_env_variable",\n',
    ),
    "m4_doctor_drops_the_closest_match": (
        "apps/cli/commands/worker_facade_cmd.py",
        '        guess = f"closest registered: {closest}" if closest else "no registered name is close"\n',
        '        guess = "no registered name is close"\n',
    ),
    "m5_registry_changed_without_the_guide": (
        "packages/orchestration/config.py",
        '        description="Skip the UI server\'s automatic npm build of apps/ui (env-only flag)",\n',
        '        description="Skip the automatic npm build of apps/ui (env-only flag)",\n',
    ),
    "m6_unregistered_shell_expansion": (
        "scripts/remedy_pytest.sh",
        'LOCK_WAIT="${REMEDY_PYTEST_LOCK_WAIT:-0}"\n',
        'LOCK_WAIT="${REMEDY_PYTEST_LOCK_WAIT:-0}"\nPROBE="${REMEDY_NOT_A_REGISTERED_NAME:-}"\n',
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

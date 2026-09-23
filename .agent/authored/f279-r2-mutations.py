"""F279 R2 G5 — mutation red-proofs of the environment-registry guard, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C3 commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_env_registry.py"]
DEMO_MODE_SPEC = (
    '    ConfigKeySpec(\n'
    '        key="ui.demo_mode",\n'
    '        env_var="REMEDY_UI_DEMO_MODE",\n'
)
MUTATIONS = {
    "m1_unregistered_literal_read": (
        "packages/orchestration/run_log.py",
        'STRICT_EVENT_NAMES_ENV = "REMEDY_STRICT_EVENT_NAMES"\n',
        'STRICT_EVENT_NAMES_ENV = "REMEDY_STRICT_EVENT_NAMES"\n'
        '_PROBE = os.environ.get("REMEDY_NOT_A_REGISTERED_NAME")\n',
    ),
    "m2_unregistered_name_in_a_constant": (
        "packages/runtimes/runtime_config.py",
        'PORT_ENV = "REMEDY_RUNTIME_PORT"\n',
        'PORT_ENV = "REMEDY_RUNTIME_PORTS"\n',
    ),
    "m3_spec_removed": (
        "packages/orchestration/config.py",
        DEMO_MODE_SPEC,
        '    ConfigKeySpec(\n'
        '        key="ui.demo_mode_removed",\n'
        '        env_var="REMEDY_UI_DEMO_MODE_REMOVED",\n',
    ),
    "m4_env_var_registered_twice": (
        "packages/orchestration/config.py",
        '        env_var="REMEDY_UI_NO_AUTO_BUILD",\n',
        '        env_var="REMEDY_UI_DEMO_MODE",\n',
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

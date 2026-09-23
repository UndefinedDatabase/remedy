"""F279 R4 G5 — mutation red-proofs of the registry reader and the typed-read guard, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C3 commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_env_registry.py", "tests/test_ollama_builder.py",
         "tests/test_ollama_provider.py"]
MUTATIONS = {
    "m1_boolean_reads_only_one": (
        "packages/orchestration/config.py",
        "    if spec.value_type is bool:\n        return raw.lower() in BOOL_TRUE_WORDS\n"
        "    if spec.value_type in (int, float):\n",
        "    if spec.value_type is bool:\n        return raw == \"1\"\n"
        "    if spec.value_type in (int, float):\n",
    ),
    "m2_unset_answers_the_default_everywhere": (
        "packages/orchestration/config.py",
        "        return spec.default if spec.env_only else None\n",
        "        return spec.default\n",
    ),
    "m3_parse_error_names_nothing": (
        "packages/orchestration/config.py",
        '                f"Environment variable {name} must be {type_words(spec)} (got {raw!r})") from None\n',
        '                f"bad value (got {raw!r})") from None\n',
    ),
    "m4_a_typed_read_bypasses_the_reader": (
        "packages/orchestration/ui_server.py",
        '    demo_mode = env_value("REMEDY_UI_DEMO_MODE")\n',
        '    demo_mode = os.environ.get("REMEDY_UI_DEMO_MODE") == "1"\n',
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

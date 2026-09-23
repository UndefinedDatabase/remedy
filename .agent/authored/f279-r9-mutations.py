"""F279 R9 G5 — red-proofs that the two repaired guards still catch what they exist for.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C3 commit.
Each mutation PLANTS a violation in a production module; its FROM text is asserted to occur
EXACTLY ONCE in its file before it is applied, the file is restored byte-for-byte after each, and
an unmutated control runs first and last. pytest runs under `python3 -B` (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_development_artifact_boundary.py",
         "tests/orchestration/test_review_subject_resolution.py"]
FUTURE = "from __future__ import annotations\n"
MUTATIONS = {
    "m1_a_second_module_reads_the_ledger": (
        "packages/orchestration/toolchain.py",
        FUTURE,
        FUTURE + '_LEDGER = ".agent/live_review.md"\n',
    ),
    "m2_config_spells_the_base_twice": (
        "packages/orchestration/config.py",
        '        env_var="REMEDY_REVIEW_BASE",\n',
        '        env_var="REMEDY_REVIEW_BASE",  # REMEDY_REVIEW_BASE\n',
    ),
    "m3_a_module_asks_for_the_base_key": (
        "packages/orchestration/job_evidence.py",
        FUTURE,
        FUTURE + '_BASE_KEY = "review.base"\n',
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

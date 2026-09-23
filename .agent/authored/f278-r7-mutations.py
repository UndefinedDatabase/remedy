"""F278 R7 G5 — mutation red-proofs of the blocking record for a lost final review, run in a DISPOSABLE worktree.

Usage: python3 mutations.py <worktree-path>. The worktree must be at the round's product commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in the file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
SRC = WT / "packages/orchestration/pingpong_job.py"
TEST = "tests/orchestration/test_pingpong_integration.py::TestRunJobFinalReviewFailure"
MUTATIONS = {
    "m1_failure_not_named_on_the_job": (
        "                job.metadata[\"final_job_review_error\"] = type(exc).__name__\n",
        "                pass  # the failure is no longer named on the job\n",
    ),
    "m2_no_blocking_record_written": (
        "                if not _fjr_path.exists():\n",
        "                if False:\n",
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or " passed" in ln or " failed" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


good = SRC.read_bytes()
run("control_before")
for name, (frm, to) in MUTATIONS.items():
    text = good.decode("utf-8")
    print(f"{name} FROM count in file: {text.count(frm)}")
    if text.count(frm) != 1:
        sys.exit(f"{name}: FROM must occur exactly once; stopping")
    SRC.write_text(text.replace(frm, to, 1), encoding="utf-8")
    run(name)
    SRC.write_bytes(good)
    print(f"{name} restored byte-identical: {SRC.read_bytes() == good}")
run("control_after")

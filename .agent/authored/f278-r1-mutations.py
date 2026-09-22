"""F278 R1 G5 — three mutation red-proofs of durable_write, run inside a DISPOSABLE worktree.

Usage: python3 mutations.py <worktree-path>. The worktree must be at the round's C3 commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in the file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
SRC = WT / "packages/common/secure_fs.py"
TEST = "tests/orchestration/test_secure_fs_durable_write.py"
MUTATIONS = {
    "m1_no_file_fsync": (
        "            os.fsync(fd)\n        finally:\n            os.close(fd)\n"
        "        os.replace(tmp_name, target)\n",
        "        finally:\n            os.close(fd)\n        os.replace(tmp_name, target)\n",
    ),
    "m2_no_dir_fsync": (
        "        try:\n            os.fsync(dir_fd)\n        finally:\n",
        "        try:\n            pass\n        finally:\n",
    ),
    "m3_fixed_sibling": (
        '    fd, tmp_name = tempfile.mkstemp(dir=directory, prefix=f".{target.name}.", '
        'suffix=".tmp")\n',
        '    tmp_name = str(target.with_suffix(".tmp"))\n'
        "    fd = os.open(tmp_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)\n",
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

"""F263 R1 G5 — mutation red-proofs of the human change record, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's product commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_human_change.py"]
HC = "packages/orchestration/human_change.py"
MUTATIONS = {
    "m1_rebase_before_the_record": (
        HC,
        "    record = write_human_change_record(job_id, repo_path, change, detected_by=detected_by,\n"
        "                                       root=root)\n"
        "    rebase(change)\n",
        "    rebase(change)\n"
        "    record = write_human_change_record(job_id, repo_path, change, detected_by=detected_by,\n"
        "                                       root=root)\n",
    ),
    "m2_untracked_files_not_captured": (
        "packages/orchestration/worktrees.py",
        '            ["git", "add", "-A", "."], cwd=str(path), env=env,\n',
        '            ["git", "add", "-u", "."], cwd=str(path), env=env,\n',
    ),
    "m3_noise_counted_as_content": (
        HC,
        '    if _is_target_noise(rel):\n',
        '    if False:\n',
    ),
    "m4_diff_digest_unchecked": (
        HC,
        "        if hashlib.sha256(diff).hexdigest() != diff_meta.get(\"sha256\"):\n",
        "        if False:\n",
    ),
    "m5_seal_unchecked": (
        HC,
        '    if body.get("record_sha256") != _seal(body):\n',
        '    if False:\n',
    ),
    "m6_record_rewritten": (
        HC,
        "    if path.exists():\n        return path\n",
        "",
    ),
    "m7_job_records_no_state": (
        "packages/orchestration/pingpong_job.py",
        '    job.target_last_known = {**state.to_dict(), "ref": ref}\n',
        "",
    ),
    "m8_import_drops_the_state": (
        "packages/orchestration/pingpong_job.py",
        '        target_last_known=data.get("target_last_known") or None,\n',
        "",
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

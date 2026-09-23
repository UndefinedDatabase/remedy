"""F263 R4 G5 — mutation red-proofs of `remedy absorb`, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's product commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/cli/test_absorb_cmd.py"]
CMD = "apps/cli/commands/absorb_cmd.py"
HC = "packages/orchestration/human_change.py"
MUTATIONS = {
    "m1_running_job_rewritten": (
        CMD,
        "        if W.lock_is_held(root, job_worktree_id(job.job_id)):\n",
        "        if False:\n",
    ),
    "m2_lock_probe_never_sees_a_holder": (
        "packages/orchestration/worktrees.py",
        "    except OSError:\n        return True\n",
        "    except OSError:\n        return False\n",
    ),
    "m3_rebase_leaves_the_ref": (
        HC,
        "        W.set_checkpoint_ref(job.repo_path, ref, change.after.tree)\n",
        "",
    ),
    "m4_rebase_not_persisted": (
        HC,
        "        save_job_plan(job, root)\n",
        "",
    ),
    "m5_every_repository_absorbed": (
        CMD,
        "            same_repo = Path(job.repo_path).resolve() == repo\n",
        "            same_repo = True\n",
    ),
    "m6_job_option_ignored": (
        CMD,
        "        if job_filter is not None and job.job_id != job_filter:\n",
        "        if False:\n",
    ),
    "m7_ended_jobs_absorbed": (
        CMD,
        "        if same_repo and state not in _ENDED:\n",
        "        if same_repo:\n",
    ),
    "m8_bare_absorb_prints_help": (
        "apps/cli/grouped.py",
        '_ALWAYS_INJECT: set[str] = {"init", "status", "absorb"}\n',
        '_ALWAYS_INJECT: set[str] = {"init", "status"}\n',
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or ln.endswith("s") and (" passed" in ln or " failed" in ln)]
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

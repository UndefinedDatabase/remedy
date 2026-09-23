"""F279 R6 G5 — mutation red-proofs of `remedy doctor toolchain` and the matrix guard, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's C3 commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/orchestration/test_toolchain.py", "tests/orchestration/test_ci_workflow.py"]
MOD = "packages/orchestration/toolchain.py"
MUTATIONS = {
    "m1_offline_reads_zero": (
        MOD,
        "def offline(_name: str) -> str:\n    return UNKNOWN\n",
        'def offline(_name: str) -> str:\n    return "0"\n',
    ),
    "m2_a_failed_fetch_reads_zero": (
        MOD,
        "    except (OSError, urllib.error.URLError, ValueError, KeyError, TypeError):\n        return UNKNOWN\n",
        '    except (OSError, urllib.error.URLError, ValueError, KeyError, TypeError):\n        return "0"\n',
    ),
    "m3_the_dev_extra_dropped": (
        MOD,
        '    declared = [*project["dependencies"], *project["optional-dependencies"]["dev"]]\n',
        '    declared = [*project["dependencies"]]\n',
    ),
    "m4_offline_ignored": (
        "apps/cli/commands/worker_facade_cmd.py",
        "    rows = toolchain_rows(fetch_newest=offline if no_network else pypi_newest)\n",
        "    rows = toolchain_rows(fetch_newest=pypi_newest)\n",
    ),
    "m5_a_third_python_in_the_matrix": (
        ".github/workflows/ci.yml",
        "        python-version: ['3.10', '3.12']\n",
        "        python-version: ['3.10', '3.11', '3.12']\n",
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

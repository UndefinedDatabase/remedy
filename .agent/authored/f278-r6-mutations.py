"""F278 R6 G5 — mutation red-proof of the fail-closed secret detector, run in a DISPOSABLE worktree.

Usage: python3 mutations.py <worktree-path>. The worktree must be at the round's product commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in the file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
SRC = WT / "packages/orchestration/run_manifest.py"
TEST = "tests/orchestration/test_run_manifest_security.py::TestSecretDetectorFailsClosed"
MUTATIONS = {
    "m1_detector_fails_open_again": (
        "    except Exception:  # noqa: BLE001 — a detector that failed cannot clear the value\n"
        "        return True\n",
        "    except Exception:  # noqa: BLE001 — a detector that failed cannot clear the value\n"
        "        return False\n",
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

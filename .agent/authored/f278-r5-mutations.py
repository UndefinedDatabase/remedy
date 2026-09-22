"""F278 R5 G5 — mutation red-proofs of the stream degradations, run in a DISPOSABLE worktree.

Usage: python3 mutations.py <worktree-path>. The worktree must be at the round's product commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in the file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
SRC = WT / "packages/orchestration/stream_evidence.py"
TEST = "tests/orchestration/test_stream_evidence.py::TestDegradations"
MUTATIONS = {
    "m1_on_cap_not_recorded": (
        "                            failed = _degradation(\"on_cap\", exc)\n"
        "                            result.degradations.append(failed)\n"
        "                            _emit(ev_fh, {\"event_type\": EVENT_DEGRADED, **failed})\n",
        "                            pass\n",
    ),
    "m2_stderr_close_not_recorded": (
        "                run_degradations.append(_degradation(\"stderr_close\", exc))\n",
        "                pass\n",
    ),
    "m3_run_degradations_not_appended": (
        "    if run_degradations:\n        _append_degradation_events(capture, run_degradations)\n",
        "",
    ),
    "m4_to_dict_drops_degradations": (
        "            \"degradations\": [dict(d) for d in self.degradations],\n",
        "",
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

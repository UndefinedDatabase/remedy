"""F263 R3 G5 — the red proof of DECISION F263 D3, in a DISPOSABLE worktree.

Usage: python3 -B ruff_probe.py <worktree-path>. The worktree must be at the round's repair commit.
Runs `ruff check .` as a control, removes the `.agent/authored` entry from `pyproject.toml`'s
`extend-exclude` (the FROM must occur exactly once), runs it again, restores the file byte for
byte, and runs the control a second time.
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
FROM = '    ".agent/authored",\n'


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-m", "ruff", "check", ".", "--output-format", "concise"],
                       cwd=WT, capture_output=True, text=True)
    print(f"{label} REAL_EXIT={r.returncode}")
    print(r.stdout.strip())


run("control_before")
path = WT / "pyproject.toml"
good = path.read_bytes()
text = good.decode("utf-8")
print(f"m8 FROM count in pyproject.toml: {text.count(FROM)}")
if text.count(FROM) != 1:
    sys.exit("m8: FROM must occur exactly once; stopping")
path.write_text(text.replace(FROM, "", 1), encoding="utf-8")
run("m8_authored_copies_linted_again")
path.write_bytes(good)
print(f"m8 restored byte-identical: {path.read_bytes() == good}")
run("control_after")

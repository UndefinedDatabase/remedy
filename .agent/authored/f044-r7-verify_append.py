#!/usr/bin/env python3
"""F044 R7 G2 — full append forensics for a prose record file (.agent/live_review.md or
.agent/decisions.md), per docs/agents/planner_reviewer_prompt.md §3 item 36 and the gate-budget
rule (these two files are one of the two targets that earn full byte forensics). Takes the
PRE-APPLY BYTE LENGTH, never a duplicate copy of a multi-megabyte file: `git apply` already
proves the pre-existing bytes are untouched (a hunk whose context does not match the tracked
file fails `--check`), so this script's own job is reading (b), the one property `git apply`
does not check.

Usage: python3 verify_append.py <pre-apply-byte-length> <post-commit-file> <appended-slice>

Reading (a), the byte reader: post-commit byte length == pre-apply length + slice byte length,
exactly (the prefix identity itself is `git apply`'s own proof, not re-read here).
Reading (b), the structural reader: split the post-commit file's TAIL into blank-line-delimited
paragraph units; the last N of them, in order, equal the slice's own N paragraph units, where N
is COUNTED from the slice, never asserted.
Negative control: flip one byte inside the FIRST appended paragraph of a throwaway copy of the
post-commit file and confirm reading (b) then REJECTS it, proving reading (b) is not vacuous.
"""
from __future__ import annotations

import sys
from pathlib import Path


def paragraphs(text: str) -> list[str]:
    # Blank-line-delimited units; drop empty units from repeated blank lines at the edges,
    # and strip a bare leading/trailing newline a split boundary can leave on a unit (a slice
    # read on its own carries no preceding blank line, while the same unit read from the whole
    # file does — stripping makes the two comparable without discarding real content).
    units = [u.strip("\n") for u in text.split("\n\n") if u.strip() != ""]
    return units


def reading_b(post_text: str, slice_paragraphs: list[str]) -> bool:
    post_paragraphs = paragraphs(post_text)
    n = len(slice_paragraphs)
    return post_paragraphs[-n:] == slice_paragraphs


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: verify_append.py <pre-apply-byte-length> <post> <slice>", file=sys.stderr)
        return 2
    pre_length = int(sys.argv[1])
    post_path, slice_path = Path(sys.argv[2]), Path(sys.argv[3])

    post = post_path.read_bytes()
    slice_bytes = slice_path.read_bytes()

    ok = True

    # Reading (a): the byte length only — the prefix's own bytes are git apply's proof.
    a_ok = len(post) == pre_length + len(slice_bytes)
    print(f"reading (a) post length == pre length + slice length: {a_ok} ({len(post)} == {pre_length} + {len(slice_bytes)})")
    ok = ok and a_ok

    # Reading (b): structural, paragraph units.
    post_text = post.decode()
    slice_text = slice_bytes.decode()
    slice_paras = paragraphs(slice_text)
    b_ok = reading_b(post_text, slice_paras)
    print(f"reading (b) last {len(slice_paras)} paragraph unit(s) match the slice, in order: {b_ok}")
    ok = ok and b_ok

    # Negative control: flip a byte in the FIRST appended paragraph of a throwaway copy.
    first_para = slice_paras[0]
    idx = post_text.rindex(first_para)
    flipped_char = "X" if first_para[0] != "X" else "Y"
    mutated_post_text = post_text[:idx] + flipped_char + post_text[idx + 1 :]
    control_ok = not reading_b(mutated_post_text, slice_paras)
    print(f"negative control (byte flipped in first appended paragraph) correctly REJECTED: {control_ok}")
    ok = ok and control_ok

    print(f"ALL READINGS OK: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

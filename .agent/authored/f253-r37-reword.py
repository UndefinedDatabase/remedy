#!/usr/bin/env python3
"""Copy F253's branch history onto new commit objects with five subjects reworded (DECISION F253 D32).

Operator question Q16, answered on 2026-10-09 and recorded as DECISION F253 D32, gives the loop
leave to reword the five commit subjects that hold a slash-led route token, by copying the branch's
history onto a branch with a new name, so that the old branch stays untouched as the record.

This script writes commit OBJECTS only; it moves, creates and deletes no ref. For every commit from
the fork point to the old tip, oldest first, it reads the raw commit object, replaces its parent
line with the parent's copy, and for the five commits below replaces the subject line, and nothing
else: tree, author, committer, both dates and time zones, the body and every trailer stay byte for
byte. The copy is therefore deterministic: the same inputs give the same new tip on every machine.

It refuses (exit 1) on a merge commit, a signed commit, an old subject other than the one expected,
a copy whose tree differs from its original, a copy that differs from its original anywhere but
the parent line and the subject, or any subject of the copied history that the review package's
metadata scan rejects. It exits 0 and prints `new tip <sha>` when every check holds.

Usage, from the repository root: python3 <this file>
"""
import subprocess
import sys

FORK = "1474a65ea6ed9f8063ce57f5294f9afaf95deee4"
OLD_TIP = "83d266f5c7c8560b5931555cfa91b7e6fe0be49c"
REWORD = {
    "bb01d85cfc931b42eed73259c98004400af59fa8": (
        "F253 R1 C2: the public HTTP API's route registry and GET /api/v1/interface on the shared "
        "handler (S1, DECISION F253 D1)",
        "F253 R1 C2: the public HTTP API's route registry and the interface route under api v1 on "
        "the shared handler (S1, DECISION F253 D1)"),
    "00be6f560404dce66a11966030cdb21c401dbc7c": (
        "F253 R2 C2: a ledger line for every call under the public HTTP API, query keys a route "
        "declares, and GET /api/v1/digest (S2a, DECISION F253 D2)",
        "F253 R2 C2: a ledger line for every call under the public HTTP API, query keys a route "
        "declares, and the digest route under api v1 (S2a, DECISION F253 D2)"),
    "352e1d17bff6914c868009f918e0d1ea190c28c1": (
        "F253 R3 C2: GET /api/v1/jobs/{job}/proof, named path segments and each route's refusal "
        "statuses (S2b, DECISION F253 D3)",
        "F253 R3 C2: the proof route of a job under api v1, named path segments and each route's "
        "refusal statuses (S2b, DECISION F253 D3)"),
    "c3fe323847838d20795297eee0b66e9d2e521902": (
        "F253 R5 C3: GET /api/v1/changes, twinned with remedy client changes, with the first query "
        "key that takes a value (S3b, DECISION F253 D5)",
        "F253 R5 C3: the changes route under api v1, twinned with remedy client changes, with the "
        "first query key that takes a value (S3b, DECISION F253 D5)"),
    "300105d0f07e4e2be0879de9e4d55fbda505d753": (
        "F253 R8 C3: POST /api/v1/jobs/{job}/decisions/{decision} answers remedy decision resolve "
        "through the supervisor (S4a, DECISION F253 D9)",
        "F253 R8 C3: the decision answer route of a job under api v1 answers remedy decision "
        "resolve through the supervisor (S4a, DECISION F253 D9)"),
}


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", *args], input=data, capture_output=True, check=True).stdout


def split_commit(raw: bytes) -> tuple[list[bytes], bytes]:
    header, _, message = raw.partition(b"\n\n")
    return header.split(b"\n"), message


def main() -> int:
    sys.path.insert(0, ".")
    from packages.orchestration.review_subject import _metadata_is_safe

    commits = git("rev-list", "--reverse", "--topo-order", f"{FORK}..{OLD_TIP}").decode().split()
    print(f"commits to copy {len(commits)}")
    copy: dict[str, str] = {}
    reworded = 0
    for old in commits:
        raw = git("cat-file", "commit", old)
        header, message = split_commit(raw)
        parents = [ln for ln in header if ln.startswith(b"parent ")]
        if len(parents) != 1:
            print(f"ERROR: {old} has {len(parents)} parents; stopping")
            return 1
        if any(ln.startswith(b"gpgsig") for ln in header):
            print(f"ERROR: {old} is signed; stopping")
            return 1
        parent = parents[0][len(b"parent "):].decode()
        new_parent = copy.get(parent, parent)
        if parent not in copy and parent != FORK:
            print(f"ERROR: {old}'s parent {parent} is neither copied nor the fork point; stopping")
            return 1
        new_header = [b"parent " + new_parent.encode() if ln.startswith(b"parent ") else ln
                      for ln in header]
        subject, nl, rest = message.partition(b"\n")
        if old in REWORD:
            want_old, want_new = REWORD[old]
            if subject.decode() != want_old:
                print(f"ERROR: {old}'s subject is not the expected one: {subject.decode()!r}")
                return 1
            subject = want_new.encode()
            reworded += 1
        new_raw = b"\n".join(new_header) + b"\n\n" + subject + nl + rest
        new = git("hash-object", "-t", "commit", "-w", "--stdin", data=new_raw).decode().strip()
        if git("rev-parse", f"{new}^{{tree}}") != git("rev-parse", f"{old}^{{tree}}"):
            print(f"ERROR: {new}'s tree differs from {old}'s; stopping")
            return 1
        back = new_raw.replace(b"parent " + new_parent.encode(), b"parent " + parent.encode(), 1)
        if old in REWORD:
            back = back.replace(REWORD[old][1].encode(), REWORD[old][0].encode(), 1)
        if back != raw:
            print(f"ERROR: {new} differs from {old} beyond its parent line and subject; stopping")
            return 1
        copy[old] = new
    if reworded != len(REWORD):
        print(f"ERROR: reworded {reworded} of {len(REWORD)} subjects; stopping")
        return 1
    new_tip = copy[OLD_TIP]
    subjects = git("log", "--format=%s", f"{FORK}..{new_tip}").decode().splitlines()
    unsafe = [s for s in subjects if not _metadata_is_safe(s)]
    old_unsafe = [s for s in git("log", "--format=%s", f"{FORK}..{OLD_TIP}").decode().splitlines()
                  if not _metadata_is_safe(s)]
    print(f"subjects in the copy {len(subjects)}, rejected by the metadata scan {len(unsafe)} {unsafe}")
    print(f"red control: subjects of the old branch rejected by the scan {len(old_unsafe)}")
    if unsafe or len(old_unsafe) != len(REWORD):
        return 1
    for old in REWORD:
        print(f"reworded {old[:9]} -> {copy[old][:9]}")
    same_tree = git("rev-parse", f"{new_tip}^{{tree}}") == git("rev-parse", f"{OLD_TIP}^{{tree}}")
    print(f"tip trees equal {same_tree}")
    print(f"new tip {new_tip}")
    return 0 if same_tree else 1


if __name__ == "__main__":
    sys.exit(main())

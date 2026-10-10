"""Refuse a commit whose subject the review package's metadata scanner would reject.

It takes one argument, the path of the commit message file git hands a commit-msg hook. It reads
the first line that is not empty and does not begin with "#". It puts the repository root, the
parent of the scripts folder, at the front of the import path and imports the scanner's check,
`_metadata_is_safe`, from `packages.orchestration.review_subject`. It exits 0 when there is no
subject or the subject is safe. It exits 0 with one line on stderr when the import fails, so a
checkout without Remedy's dependencies can still commit. It exits 1 when the subject is unsafe.
"""
from __future__ import annotations

import sys
from pathlib import Path


def _subject(path: str) -> str:
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            return line
    return ""


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_commit_subject.py <commit-message-file>", file=sys.stderr)
        return 0
    try:
        subject = _subject(argv[1])
    except (OSError, UnicodeDecodeError) as exc:
        print(f"commit subject not checked: {exc}", file=sys.stderr)
        return 0
    if not subject:
        return 0
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    try:
        from packages.orchestration.review_subject import _metadata_is_safe
    except ImportError as exc:
        print(f"commit subject not checked: {exc}", file=sys.stderr)
        return 0
    if _metadata_is_safe(subject):
        return 0
    print(
        "This commit subject would be rejected by the review package's metadata scanner, because it "
        "holds a slash-led path token, an absolute path or a secret-like string.\n"
        "Name the route or path in words (for example \"the interface route under api v1\") or, for a "
        "web route under /api/, keep it as it is, which the scanner accepts since amend1010.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

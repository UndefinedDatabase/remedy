"""The command line over the package.

Progress lines go to stdout and errors to stderr, which is what gauntlet
orders g03 (``--quiet``) and g08 (``--dry-run``) build on.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .errors import SampleProjError
from .importer import import_records
from .report import build_report


def _read_lines(source: str) -> list[str]:
    if source == "-":
        return sys.stdin.read().splitlines()
    path = Path(source)
    if not path.is_file():
        raise SampleProjError(f"no such input file: {source}")
    return path.read_text(encoding="utf-8").splitlines()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sampleproj")
    sub = parser.add_subparsers(dest="command", required=True)

    imp = sub.add_parser("import", help="import records into a directory")
    imp.add_argument("source", help="input file, or - for stdin")
    imp.add_argument("target", help="directory to write into")

    rep = sub.add_parser("report", help="report on an imported directory")
    rep.add_argument("target", help="directory to report on")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "import":
            written = import_records(_read_lines(args.source), args.target)
            print(f"importing from {args.source}")
            for path in written:
                print(f"  wrote {path.name}")
            print(f"imported {len(written)} record(s)")
            return 0
        sys.stdout.write(build_report(args.target))
        return 0
    except SampleProjError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

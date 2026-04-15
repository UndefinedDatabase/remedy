"""
Remedy CLI entrypoint.

Usage:
    remedy create-job "<prompt>"
"""

from __future__ import annotations

import argparse

from packages.core.models import Job, RunState
from packages.orchestration.storage import save_job


def _cmd_create_job(prompt: str) -> None:
    job = Job(
        name=prompt[:50],
        user_prompt=prompt,
        state=RunState.PENDING,
    )
    save_job(job)
    print(job.id)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="remedy",
        description="Remedy orchestration CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create-job", help="Create and persist a new job")
    create.add_argument("prompt", help="User prompt describing the job")

    args = parser.parse_args()

    if args.command == "create-job":
        _cmd_create_job(args.prompt)


if __name__ == "__main__":
    main()

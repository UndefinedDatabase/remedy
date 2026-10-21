"""The `job certificate` and `verify` entries of the command catalog (F060 T003, DECISION F060 D4).

Kept in a module of its own because `apps/cli/command_catalog.py` may not grow (its row in
`docs/system/structure-ledger-v1.md`); `_BASE_CATALOG` splices `JOB_CERTIFICATE_COMMANDS` in right
after `job.evidence`, so the help lists the two files a job can hand on together, and
`VERIFY_COMMANDS` at the end of its list.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import _JSON_OPT, ArgDef, CommandEntry

JOB_CERTIFICATE_COMMANDS: tuple[CommandEntry, ...] = (
    CommandEntry(
        command_id="job.certificate",
        group_id="job",
        subcommand="certificate",
        description="Make the certificate of a job under its mission that has ended: one small bundle of its report, cost, checks, ownership and run evidence with a hash manifest and its claims. It is a proof of integrity, not a signature; `remedy verify` checks it on any machine.",
        action_class="local_state_change",
        supports_json=True,
        args=(
            ArgDef("job_id", "Job ID to certify (under its mission)"),
            ArgDef("--out", "Path of the certificate file to write; it must not exist yet (default: remedy-certificate-<id>-<issue>.zip in the current folder)", required=False, is_option=True),
            ArgDef("--max-bytes", "Size budget of the certificate in bytes (default: 8388608, 8 MiB); a diff or log that does not fit is listed with its hash instead of embedded", required=False, is_option=True),
            _JSON_OPT,
        ),
        related=("job.evidence", "verify.run"),
        exit_codes=(0, 1, 2, 3),
    ),
)

VERIFY_COMMANDS: tuple[CommandEntry, ...] = (
    CommandEntry(
        command_id="verify.run",
        group_id="verify",
        subcommand="run",
        description="Check the certificate of a job under its mission on any machine, with no data folder: every member against its hash and every claim against its member. Exits 0 when it is intact and 1 when it is not.",
        action_class="read_only",
        supports_json=True,
        args=(
            ArgDef("bundle", "Path of the certificate file to check"),
            _JSON_OPT,
        ),
        related=("job.certificate",),
        exit_codes=(0, 1, 2),
    ),
)

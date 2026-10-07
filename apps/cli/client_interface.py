"""F298 T001 — the machine client interface as data, read from the code (DECISION F298 D2).

`docs/roadmap/features/T12_F298.md` T001 asks for one document, generated from the code and never
written by hand, that names what a program meets when it drives Remedy's command line. This
module builds it. Every list in it is read from the place the product already keeps it: the
command catalog for the operations, their arguments and the exit codes each can reach;
`apps/cli/exit_codes.py` for what each exit code means; `RunState` for the job states;
`MISSION_STATUSES` for the mission status words; `docs/contracts/` for the contract templates;
`JobBudgets` for the budget kinds; and `apps/cli/json_envelope.py` for the envelope every
`--json` answer wears. A change in any of those places changes the document. Two things are
declared here: which catalog commands a client uses, `CLIENT_OPERATION_IDS`, and the tree of the
keys the digest returns, `DIGEST_KEY_TREE`, which `tests/cli/test_client_interface.py` holds equal
to the keys `packages/orchestration/client_digest.py` writes and to what a real run's digest
returns (DECISION F298 D3).

The feature file calls this document the contract. The product calls it the machine client
interface, because `docs/system/vocabulary.md` reserves "contract" for a mission's acceptance
criteria and nothing else (DECISION F298 D2).

Inside one major version the document only grows: a later minor version adds names and never
removes one.
"""

from __future__ import annotations

import copy
from typing import Any

#: The document's own version. Its major number changes only when a name is removed or changes
#: its meaning; adding a name raises the minor number.
CLIENT_INTERFACE_VERSION = "1.1"

#: The catalog commands a machine client uses: the path of DECISION F295 D17's page (propose,
#: read, answer, run on, approve and apply, prove), the hunk decision a client may choose, the
#: budget refusal of `job resume`, abandoning a mission, and this document's own command.
CLIENT_OPERATION_IDS: tuple[str, ...] = (
    "do.run",
    "status.run",
    "decision.resolve",
    "job.run",
    "job.resume",
    "job.apply",
    "change.proof",
    "job.evidence",
    "patch.hunks",
    "patch.approve-hunks",
    "patch.approve",
    "patch.reject",
    "mission.abandon",
    "client.interface",
)

#: The keys of the `client` object in `remedy status --json` (DECISION F295 D4, D5, D7), as a tree:
#: each key maps to the tree of the object under it, or of every element of the list under it,
#: and a key with no keys under it maps to an empty tree (DECISION F298 D3).
DIGEST_KEY_TREE: dict[str, Any] = {
    "version": {},
    "read_at": {},
    "supervisor": {"answers": {}},
    "projects": {
        "project_id": {},
        "slug": {},
        "missions": {
            "mission_id": {},
            "status": {},
            "goal": {},
            "job_ids": {},
            "order_source_path": {},
            "order_source_sha256": {},
        },
        "cost_today": {"day": {}, "value_usd": {}, "basis": {}, "calls": {}},
    },
    "jobs": {
        "job_id": {},
        "project_id": {},
        "mission_id": {},
        "title": {},
        "state": {},
        "waits_for_apply": {},
        "cost": {"value_usd": {}, "basis": {}},
        "evidence": {
            "evidence_dir": {},
            "run_ids": {},
            "postmortem_path": {},
            "run_manifest_path": {},
            "result_diff_path": {},
            "result_diff_sha256": {},
        },
    },
    "awaiting_apply": {},
    "decisions": {
        "job_id": {},
        "project_id": {},
        "decision_id": {},
        "type": {},
        "severity": {},
        "question": {},
        "default": {},
        "options": {},
        "clarifications": {"id": {}, "question": {}, "default": {}},
        "created_at": {},
        "age_seconds": {},
    },
    "degraded": {},
    "skipped_files": {},
}


def _argument_entry(arg: Any) -> dict[str, Any]:
    """One catalog `ArgDef` as the document names it."""
    return {
        "name": arg.name,
        "help": arg.help,
        "option": arg.is_option,
        "required": arg.required,
        "takes_value": not arg.is_flag,
        "repeatable": arg.is_repeatable,
    }


def _operation_entry(command_id: str) -> dict[str, Any]:
    """One operation, read from its catalog entry; `KeyError` when the catalog has no such id."""
    from apps.cli.command_catalog import get_command

    entry = get_command(command_id)
    return {
        "command_id": entry.command_id,
        "command": f"remedy {entry.group_id} {entry.subcommand}",
        "description": entry.description,
        "arguments": [_argument_entry(arg) for arg in entry.args],
        "exit_codes": list(entry.exit_codes),
    }


# WHY: the one builder of the document, so `remedy client interface` and F253's HTTP call print
# the same thing and the page is rendered from the same value (DECISION F298 D2).
def build_client_interface() -> dict[str, Any]:
    """The machine client interface as one JSON-ready dict; reads only, never writes."""
    from apps.cli.exit_codes import CLI_EXIT_CODES
    from apps.cli.json_envelope import RESERVED_KEYS, SCHEMA_VERSION
    from packages.core.models import JobBudgets, RunState
    from packages.orchestration.contract_templates import list_contract_templates
    from packages.orchestration.mission_state import MISSION_STATUSES

    return {
        "interface_version": CLIENT_INTERFACE_VERSION,
        "envelope": {
            "schema_version": SCHEMA_VERSION,
            "reserved_keys": list(RESERVED_KEYS),
            "error_keys": ["error", "message"],
        },
        "operations": [_operation_entry(command_id) for command_id in CLIENT_OPERATION_IDS],
        "exit_codes": [
            {"code": meaning.code, "name": meaning.name, "meaning": meaning.meaning}
            for meaning in CLI_EXIT_CODES
        ],
        "job_states": [state.value for state in RunState],
        "mission_statuses": list(MISSION_STATUSES),
        "contract_templates": list(list_contract_templates()),
        "budget_kinds": list(JobBudgets.model_fields),
        "digest": copy.deepcopy(DIGEST_KEY_TREE),
    }

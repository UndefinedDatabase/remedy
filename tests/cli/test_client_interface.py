"""F298 T001 — the machine client interface is read from the code (DECISION F298 D2).

`apps/cli/client_interface.py` builds the document a program relies on, and
`remedy client interface` prints it. These tests hold every list in the document to the place the
product keeps it, and prove the reading is live: a change made to the catalog while the test
runs appears in the document without any edit to the interface module.
"""
from __future__ import annotations

import json
from dataclasses import replace

import pytest

from apps.cli import command_catalog
from apps.cli.client_interface import (
    CLIENT_INTERFACE_VERSION,
    CLIENT_OPERATION_IDS,
    build_client_interface,
)
from apps.cli.command_catalog import ArgDef, get_command
from apps.cli.exit_codes import CLI_EXIT_CODES
from apps.cli.grouped import main
from apps.cli.json_envelope import RESERVED_KEYS, SCHEMA_VERSION
from packages.core.models import JobBudgets, RunState
from packages.orchestration.contract_templates import list_contract_templates
from packages.orchestration.mission_state import MISSION_STATUSES


def test_the_document_carries_its_own_version():
    assert build_client_interface()["interface_version"] == CLIENT_INTERFACE_VERSION == "1.1"


def test_each_operation_is_its_catalog_entry_in_the_declared_order():
    operations = build_client_interface()["operations"]
    assert [op["command_id"] for op in operations] == list(CLIENT_OPERATION_IDS)
    for op in operations:
        entry = get_command(op["command_id"])
        assert op["command"] == f"remedy {entry.group_id} {entry.subcommand}"
        assert op["description"] == entry.description
        assert op["exit_codes"] == list(entry.exit_codes)
        assert [arg["name"] for arg in op["arguments"]] == [arg.name for arg in entry.args]
        for arg, catalog_arg in zip(op["arguments"], entry.args):
            assert arg == {
                "name": catalog_arg.name,
                "help": catalog_arg.help,
                "option": catalog_arg.is_option,
                "required": catalog_arg.required,
                "takes_value": not catalog_arg.is_flag,
                "repeatable": catalog_arg.is_repeatable,
            }


def test_an_argument_added_to_the_catalog_appears_in_the_document(monkeypatch):
    added = ArgDef("--added-for-the-test", "An option only this test adds", required=False,
                   is_option=True, is_flag=True)
    catalog = tuple(replace(entry, args=(*entry.args, added)) if entry.command_id == "job.apply"
                    else entry for entry in command_catalog.CATALOG)
    monkeypatch.setattr(command_catalog, "CATALOG", catalog)
    apply_op = next(op for op in build_client_interface()["operations"]
                    if op["command_id"] == "job.apply")
    assert apply_op["arguments"][-1] == {
        "name": "--added-for-the-test", "help": "An option only this test adds", "option": True,
        "required": False, "takes_value": False, "repeatable": False,
    }


def test_an_operation_the_catalog_lacks_is_an_error_not_a_silent_gap(monkeypatch):
    catalog = tuple(entry for entry in command_catalog.CATALOG if entry.command_id != "job.apply")
    monkeypatch.setattr(command_catalog, "CATALOG", catalog)
    with pytest.raises(KeyError):
        build_client_interface()


def test_the_vocabularies_are_the_products_own():
    interface = build_client_interface()
    assert interface["exit_codes"] == [
        {"code": m.code, "name": m.name, "meaning": m.meaning} for m in CLI_EXIT_CODES]
    assert interface["job_states"] == [state.value for state in RunState]
    assert interface["mission_statuses"] == list(MISSION_STATUSES)
    assert interface["contract_templates"] == list(list_contract_templates())
    assert interface["budget_kinds"] == list(JobBudgets.model_fields)
    assert interface["envelope"] == {"schema_version": SCHEMA_VERSION,
                                     "reserved_keys": list(RESERVED_KEYS),
                                     "error_keys": ["error", "message"]}


def test_the_command_prints_the_document_as_one_envelope(capsys):
    main(["client", "interface", "--json"])
    body = json.loads(capsys.readouterr().out)
    assert body.pop("ok") is True
    assert body.pop("schema_version") == SCHEMA_VERSION
    assert body == json.loads(json.dumps(build_client_interface()))


def test_the_text_output_names_every_operation(capsys):
    main(["client", "interface"])
    out = capsys.readouterr().out
    assert out.startswith(f"Machine client interface {CLIENT_INTERFACE_VERSION}\n")
    for op in build_client_interface()["operations"]:
        assert f"  {op['command']} — " in out
    assert "remedy client interface --json" in out

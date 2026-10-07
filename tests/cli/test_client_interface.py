"""F298 T001 — the machine client interface is read from the code (DECISION F298 D2).

`apps/cli/client_interface.py` builds the document a program relies on, and
`remedy client interface` prints it. These tests hold every list in the document to the place the
product keeps it, and prove the reading is live: a change made to the catalog while the test
runs appears in the document without any edit to the interface module.

The digest's key tree is declared in the interface module, so it is held from two sides
(DECISION F298 D3): its names equal the string keys of the dict literals the digest's code
writes, read from that code's syntax tree, and a real run's digest returns no key the tree does
not name, at the place the tree names it.
"""
from __future__ import annotations

import ast
import json
import os
from dataclasses import replace
from pathlib import Path

import pytest

from apps.cli import command_catalog
from apps.cli.client_interface import (
    CLIENT_INTERFACE_VERSION,
    CLIENT_OPERATION_IDS,
    DIGEST_KEY_TREE,
    build_client_interface,
)
from apps.cli.command_catalog import ArgDef, get_command
from apps.cli.exit_codes import CLI_EXIT_CODES
from apps.cli.grouped import main
from apps.cli.json_envelope import RESERVED_KEYS, SCHEMA_VERSION
from packages.core.models import JobBudgets, RunState
from packages.orchestration.contract_templates import list_contract_templates
from packages.orchestration.mission_state import MISSION_STATUSES
from tests.cli.test_machine_client_contract import (
    _GIT_IDENTITY,
    ORDER_FILE_TEXT,
    PAST_DEADLINE,
    _remedy,
    _scratch_repo,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]


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
    assert interface["digest"] == DIGEST_KEY_TREE


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
    assert f"Digest (remedy status --json, under client): {', '.join(DIGEST_KEY_TREE)}\n" in out
    assert "remedy client interface --json" in out


# The digest's keys (DECISION F298 D3).

def _key_paths(tree: dict, prefix: tuple[str, ...] = ()) -> set[tuple[str, ...]]:
    """Every path from the root of a key tree to one of its keys."""
    paths: set[tuple[str, ...]] = set()
    for key, below in tree.items():
        paths.add((*prefix, key))
        paths |= _key_paths(below, (*prefix, key))
    return paths


def _key_tree(value) -> dict:
    """The key tree of a JSON value: an object's keys, a list's elements merged, a scalar empty."""
    if isinstance(value, dict):
        return {key: _key_tree(below) for key, below in value.items()}
    if isinstance(value, list):
        merged: dict = {}
        for element in value:
            for key, below in _key_tree(element).items():
                merged.setdefault(key, {}).update(below)
        return merged
    return {}


def _dict_literal_keys(path: Path, function: str | None = None) -> set[str]:
    """The string keys of every dict literal in a module, or in one of its functions."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    if function is not None:
        [tree] = [node for node in ast.walk(tree)
                  if isinstance(node, ast.FunctionDef) and node.name == function]
    return {key.value for node in ast.walk(tree) if isinstance(node, ast.Dict)
            for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)}


def test_the_digest_tree_names_exactly_the_keys_the_digest_code_writes():
    orchestration = _REPO_ROOT / "packages" / "orchestration"
    written = (_dict_literal_keys(orchestration / "client_digest.py")
               | _dict_literal_keys(orchestration / "project_cockpit.py", "project_cost_of_day"))
    named = {path[-1] for path in _key_paths(DIGEST_KEY_TREE)}
    assert sorted(written - named) == [], "the digest's code writes keys the interface does not name"
    assert sorted(named - written) == [], "the interface names digest keys the code does not write"


def test_a_real_runs_digest_returns_only_keys_the_tree_names(tmp_path):
    repo = _scratch_repo(tmp_path)
    order_file = tmp_path / "order.md"
    order_file.write_text(ORDER_FILE_TEXT, encoding="utf-8")
    env = {**os.environ, **_GIT_IDENTITY, "REMEDY_DATA_DIR": str(tmp_path / "data")}
    code, _done = _remedy(
        ["do", str(order_file), "--no-ui", "--yes", "--no-llm",
         "--builder-provider", "fake", "--reviewer-provider", "fake",
         "--deadline", PAST_DEADLINE], repo, env)
    assert code == 1
    code, status = _remedy(["status"], repo, env)
    assert code == 0
    returned = _key_paths(_key_tree(status["client"]))
    # The run raised its budget decision and filed its mission, so the reading reaches every level.
    assert {("decisions", "decision_id"), ("projects", "missions", "mission_id"),
            ("projects", "cost_today", "calls"), ("jobs", "evidence", "run_manifest_path")} <= returned
    assert sorted(returned - _key_paths(DIGEST_KEY_TREE)) == []

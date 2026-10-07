"""F298 T001 — the machine client interface is read from the code (DECISION F298 D2).

`apps/cli/client_interface.py` builds the document a program relies on, and
`remedy client interface` prints it. These tests hold every list in the document to the place the
product keeps it, and prove the reading is live: a change made to the catalog while the test
runs appears in the document without any edit to the interface module.

The digest's key tree is declared in the interface module, so it is held from two sides
(DECISION F298 D3): its names equal the string keys of the dict literals the digest's code
writes, read from that code's syntax tree, and a real run's digest returns no key the tree does
not name, at the place the tree names it.

Each operation's refusal tokens are declared in the interface module too, and held to a static
reading of the operation's handler (DECISION F298 D4) that walks the code the way
`tests/cli/test_exit_codes.py` walks it for exit codes.
"""
from __future__ import annotations

import ast
import inspect
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
    OPERATION_REFUSAL_TOKENS,
    build_client_interface,
)
from apps.cli.command_catalog import ArgDef, get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.exit_codes import CLI_EXIT_CODES
from apps.cli.grouped import main
from apps.cli.json_envelope import RESERVED_KEYS, SCHEMA_VERSION
from packages.core.models import JobBudgets, RunState
from packages.orchestration.contract_templates import list_contract_templates
from packages.orchestration.mission_state import MISSION_STATUSES
from tests.cli.test_exit_codes import _module_info
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
        assert op["refusal_tokens"] == list(OPERATION_REFUSAL_TOKENS[op["command_id"]])
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


# The refusal tokens (DECISION F298 D4).

#: The calls whose first argument, or `error` keyword, is a refusal envelope's `error` token.
_TOKEN_CALLS = frozenset({"fail", "emit_error", "build_error"})

#: A token site this static reading cannot resolve to a string, keyed
#: `<module>:<function>:<expression>`, with the tokens a reader verified by hand and why. A site
#: absent from this mapping fails the reading test with its location.
UNRESOLVED_TOKEN_SITES: dict[str, tuple[frozenset[str], str]] = {
    "apps.cli.commands.do_cmd:_cmd_do:exc.error": (
        frozenset({"order_file_empty", "order_file_invalid_header", "order_file_not_found",
                   "order_file_unreadable"}),
        "an OrderFileError's token; every OrderFileError(...) in "
        "packages/orchestration/order_file.py names one of these four",
    ),
    "apps.cli.commands.decision:_consume_plan_approval:exc.code": (
        frozenset(),
        "consume_plan_approval in packages/orchestration/plan_editing.py raises PlanEditRefused "
        "only as approval_closed, which the line above answers as no_pending_plan_approval",
    ),
    "apps.cli.serve_client:forward_effect:error": (
        frozenset({"job_not_started"}),
        "forward_effect passes its caller's `error` through; on a client's path its one caller, "
        "_cmd_job_run in apps/cli/commands/do_cmd.py, passes job_not_started",
    ),
    "apps.cli.commands.patch:_cmd_approve_hunks:result.code": (
        frozenset({"duplicate_hunk", "empty_decision", "missing_reason", "no_diff_available",
                   "overlapping_sets", "unknown_hunk", "untrustworthy_view"}),
        "a HunkApprovalRefusal's code; record_hunk_decision_from_view returns the two of "
        "packages/orchestration/hunk_decision_record.py and the five of decide_hunk_approval",
    ),
}

_token_memo: dict[tuple[str, str], tuple[set[str], set[str]]] = {}


def _token_sites(fn: ast.AST, modname: str) -> tuple[set[str], set[str], set[str]]:
    """The literal tokens in `fn`'s own body, its unresolved token sites, and its bare-name calls."""
    tokens: set[str] = set()
    unresolved: set[str] = set()
    calls: set[str] = set()
    for node in ast.walk(fn):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
            continue
        if node.func.id not in _TOKEN_CALLS:
            calls.add(node.func.id)
            continue
        arg = node.args[0] if node.args else None
        for keyword in node.keywords:
            if keyword.arg == "error":
                arg = keyword.value
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            tokens.add(arg.value)
        else:
            unresolved.add(f"{modname}:{fn.name}:{ast.unparse(arg) if arg is not None else ''}")
    return tokens, unresolved, calls


def _token_reach(modname: str, funcname: str, stack: tuple = ()) -> tuple[set[str], set[str]]:
    """Every token `modname.funcname` can answer with, and every unresolved site it reaches, through
    the same-module functions it calls by bare name and the `apps.cli` functions it imports."""
    key = (modname, funcname)
    if key in _token_memo:
        return _token_memo[key]
    if key in stack:
        return set(), set()
    _mod, funcs, imports = _module_info(modname)
    if funcname not in funcs:
        if funcname in imports:
            return _token_reach(*imports[funcname], stack + (key,))
        return set(), set()
    tokens, unresolved, calls = _token_sites(funcs[funcname], modname)
    for called in calls:
        more_tokens, more_unresolved = _token_reach(modname, called, stack + (key,))
        tokens |= more_tokens
        unresolved |= more_unresolved
    _token_memo[key] = (tokens, unresolved)
    return tokens, unresolved


def _handler_tokens(command_id: str) -> set[str]:
    handler = inspect.unwrap(collect_all_handlers()[command_id])
    names = handler.__code__.co_names if handler.__name__ == "<lambda>" else (handler.__name__,)
    tokens: set[str] = set()
    for name in names:
        reached, unresolved = _token_reach(handler.__module__, name)
        tokens |= reached
        unknown = sorted(site for site in unresolved if site not in UNRESOLVED_TOKEN_SITES)
        assert unknown == [], f"{command_id}: token sites with no entry in UNRESOLVED_TOKEN_SITES: {unknown}"
        for site in unresolved:
            tokens |= UNRESOLVED_TOKEN_SITES[site][0]
    return tokens


def test_every_operation_declares_its_refusal_tokens():
    assert sorted(OPERATION_REFUSAL_TOKENS) == sorted(CLIENT_OPERATION_IDS)
    for command_id, tokens in OPERATION_REFUSAL_TOKENS.items():
        assert list(tokens) == sorted(set(tokens)), f"{command_id}: tokens not sorted or repeated"


@pytest.mark.parametrize("command_id", CLIENT_OPERATION_IDS)
def test_declared_tokens_equal_the_tokens_the_handler_reaches(command_id):
    assert sorted(_handler_tokens(command_id)) == list(OPERATION_REFUSAL_TOKENS[command_id])


def test_the_hand_verified_token_sets_still_equal_what_their_code_names():
    from packages.orchestration import hunk_approval, hunk_decision_record

    order_file = ast.parse((_REPO_ROOT / "packages/orchestration/order_file.py").read_text(encoding="utf-8"))
    raised = {node.args[0].value for node in ast.walk(order_file)
              if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
              and node.func.id == "OrderFileError" and isinstance(node.args[0], ast.Constant)}
    assert raised == UNRESOLVED_TOKEN_SITES["apps.cli.commands.do_cmd:_cmd_do:exc.error"][0]
    hunk_codes = ({value for name, value in vars(hunk_approval).items() if name.startswith("REFUSAL_")}
                  | {value for name, value in vars(hunk_decision_record).items()
                     if name.startswith("HUNK_RECORD_REFUSAL_")})
    assert hunk_codes == UNRESOLVED_TOKEN_SITES["apps.cli.commands.patch:_cmd_approve_hunks:result.code"][0]

"""F298 T001 — the machine client interface is read from the code (DECISION F298 D2).

`apps/cli/client_interface.py` builds the document a program relies on, and
`remedy client interface` prints it. These tests hold every list in the document to the place the
product keeps it, and prove the reading is live: a change made to the catalog while the test
runs appears in the document without any edit to the interface module. Whether an argument takes
a value and may be repeated is held to the parser `remedy` really runs, which gives some options
their own rules by name (R-1178, DECISION F298 D19).

The digest's key tree is declared in the interface module, so it is held from two sides
(DECISION F298 D3): its names equal the string keys of the dict literals the digest's code
writes, read from that code's syntax tree, and a real run's digest returns no key the tree does
not name, at the place the tree names it.

Each operation's refusal tokens are declared in the interface module too, and held to a static
reading of the operation's handler (DECISION F298 D4) that walks the code the way
`tests/cli/test_exit_codes.py` walks it for exit codes.

The top-level keys of the operations' answers are declared there as well, and held the same two
ways as the digest's (DECISIONs F298 D5, D6 and D7): a static reading of each handler, the same walk,
and a real run of the path and of the operations after it, whose every answer returns no key the
declaration does not name.

The keys under those top-level keys are declared there as trees, and held the same two ways
(DECISIONs F298 D8 to D18): each tree's names equal what the code that builds it names, and the real run's
answers return no key below the top level that the trees do not name, at the place they name it.

The last section of `docs/system/machine-client-contract-v1.md` is the interface rendered, and is
held two ways (DECISION F298 D20): its bytes equal the rendering of the interface the code builds,
and reading it back line by line gives that interface again, every name, word, number and tree.

F295's gate test is the one client this repository writes down. Every command it drives is an
operation of the interface and every flag it passes is an argument of one of them, and its file
is pinned by digest, because F298 keeps it and its path unchanged (R-1179, R-1180).
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import inspect
import json
import os
import re
from dataclasses import replace
from pathlib import Path

import pytest

from apps.cli import command_catalog
from apps.cli.client_interface import (
    ANSWER_KEY_TREES,
    CLIENT_INTERFACE_PAGE_BEGIN,
    CLIENT_INTERFACE_PAGE_END,
    CLIENT_INTERFACE_PAGE_PATH,
    CLIENT_INTERFACE_VERSION,
    CLIENT_OPERATION_IDS,
    DIGEST_KEY_TREE,
    EXECUTION_CONFIG_KEY_TREE,
    JOB_BUDGETS_KEY_TREE,
    JOB_REPORT_KEY_TREES,
    KEY_TREE_REPEAT_MARK,
    MISSION_CONTRACT_KEY_TREE,
    OPERATION_ANSWER_KEYS,
    OPERATION_REFUSAL_TOKENS,
    TARGET_GUARD_KEY_TREE,
    build_client_interface,
    render_client_interface_markdown,
    write_client_interface_page,
)
from apps.cli.command_catalog import ArgDef, get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.exit_codes import CLI_EXIT_CODES
from apps.cli.grouped import _DEFAULT_COMMAND, build_parser, main
from apps.cli.json_envelope import RESERVED_KEYS, SCHEMA_VERSION
from packages.core.models import JobBudgets, RunState
from packages.orchestration.client_digest import APPROVAL_RECOMMENDATIONS, APPROVAL_RISKS
from packages.orchestration.contract_templates import list_contract_templates
from packages.orchestration.mission_state import MISSION_STATUSES
from tests.cli.test_exit_codes import _module_info
from tests.cli.test_machine_client_contract import (
    _GIT_IDENTITY,
    LATER_DEADLINE,
    ORDER_FILE_TEXT,
    PAST_DEADLINE,
    _gate_names,
    _remedy,
    _scratch_repo,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]


def test_the_document_carries_its_own_version():
    assert build_client_interface()["interface_version"] == CLIENT_INTERFACE_VERSION == "1.5"


def _command_parser_actions(command_id: str) -> dict[str, argparse.Action]:
    """The actions of one command's parser inside the parser `remedy` really runs, by argument name."""
    entry = get_command(command_id)

    def choices(parser: argparse.ArgumentParser) -> dict[str, argparse.ArgumentParser]:
        return next(action for action in parser._actions
                    if isinstance(action, argparse._SubParsersAction)).choices

    command = choices(choices(build_parser())[entry.group_id])[entry.subcommand]
    return {name: action for action in command._actions
            for name in (action.option_strings or [action.dest])}


def test_each_operation_is_its_catalog_entry_in_the_declared_order():
    operations = build_client_interface()["operations"]
    assert [op["command_id"] for op in operations] == list(CLIENT_OPERATION_IDS)
    for op in operations:
        entry = get_command(op["command_id"])
        actions = _command_parser_actions(op["command_id"])
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
                "takes_value": actions[catalog_arg.name].nargs != 0,
                "repeatable": isinstance(actions[catalog_arg.name], argparse._AppendAction),
            }


def test_a_switch_takes_no_value_and_a_collected_option_repeats():
    """R-1178: the parser gives `--json`, `--approve` and others their own rules by name, so the
    catalog's `is_flag` alone said they take a value; the document says what the parser does."""
    arguments = {(op["command_id"], arg["name"]): arg
                 for op in build_client_interface()["operations"] for arg in op["arguments"]}
    for switch in (("job.apply", "--approve"), ("job.apply", "--dry-run"), ("do.run", "--json"),
                   ("do.run", "--no-ui"), ("do.run", "--yes"), ("job.run", "--stream-evidence"),
                   ("job.resume", "--dry-run"), ("client.interface", "--json")):
        assert arguments[switch]["takes_value"] is False, switch
    for valued in (("decision.resolve", "--reason"), ("do.run", "--max-cost-usd"),
                   ("do.run", "--project"), ("do.run", "goal")):
        assert arguments[valued]["takes_value"] is True, valued
    assert arguments[("job.evidence", "--verification-command")]["repeatable"] is True
    assert arguments[("decision.resolve", "--answer")]["repeatable"] is True
    assert arguments[("job.apply", "--approve")]["repeatable"] is False


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
    assert interface["approval_recommendations"] == list(APPROVAL_RECOMMENDATIONS)
    assert interface["approval_risks"] == list(APPROVAL_RISKS)
    assert interface["envelope"] == {"schema_version": SCHEMA_VERSION,
                                     "reserved_keys": list(RESERVED_KEYS),
                                     "error_keys": ["error", "message"]}
    assert interface["digest"] == DIGEST_KEY_TREE
    assert interface["answers"] == {command_id: list(keys)
                                    for command_id, keys in OPERATION_ANSWER_KEYS.items()}
    assert interface["answer_trees"] == ANSWER_KEY_TREES


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
    "apps.cli.commands.do_cmd:_cmd_job_apply:error": (
        frozenset({"apply_failed", "blocked_paths", "commit_refused", "history_merge_refused",
                   "job_not_found", "job_not_ready", "merge_conflict", "post_test_failed",
                   "push_failed", "push_no_upstream", "push_refused", "push_refused_by_contract",
                   "target_changed", "target_detached_head", "target_dirty"}),
        "the token apply_refusal in packages/orchestration/job_apply.py returns, one of its "
        "APPLY_REFUSAL_TOKENS, which tests/cli/test_job_apply_refusals.py drives to every one "
        "(DECISION F304 D4)",
    ),
}

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


def _reach(read_sites, memo: dict, modname: str, funcname: str,
           stack: tuple = ()) -> tuple[set[str], set[str]]:
    """Every name `read_sites` finds in `modname.funcname`, and every unresolved site it reaches,
    through the same-module functions it calls by bare name and the `apps.cli` functions it imports."""
    key = (modname, funcname)
    if key in memo:
        return memo[key]
    if key in stack:
        return set(), set()
    _mod, funcs, imports = _module_info(modname)
    if funcname not in funcs:
        if funcname in imports:
            return _reach(read_sites, memo, *imports[funcname], stack + (key,))
        return set(), set()
    found, unresolved, calls = read_sites(funcs[funcname], modname)
    for called in calls:
        more_found, more_unresolved = _reach(read_sites, memo, modname, called, stack + (key,))
        found |= more_found
        unresolved |= more_unresolved
    memo[key] = (found, unresolved)
    return found, unresolved


def _handler_reading(command_id: str, read_sites, memo: dict,
                     unresolved_sites: dict[str, tuple[frozenset[str], str]]) -> set[str]:
    """What `read_sites` finds from the operation's handler on, with its hand-verified sites folded in;
    a site `unresolved_sites` does not name fails with its location."""
    handler = inspect.unwrap(collect_all_handlers()[command_id])
    names = handler.__code__.co_names if handler.__name__ == "<lambda>" else (handler.__name__,)
    found: set[str] = set()
    for name in names:
        reached, unresolved = _reach(read_sites, memo, handler.__module__, name)
        found |= reached
        unknown = sorted(site for site in unresolved if site not in unresolved_sites)
        assert unknown == [], f"{command_id}: sites with no hand-verified entry: {unknown}"
        for site in unresolved:
            found |= unresolved_sites[site][0]
    return found


_token_memo: dict[tuple[str, str], tuple[set[str], set[str]]] = {}


def _handler_tokens(command_id: str) -> set[str]:
    return _handler_reading(command_id, _token_sites, _token_memo, UNRESOLVED_TOKEN_SITES)


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
    from packages.orchestration.job_apply import APPLY_REFUSAL_TOKENS

    assert frozenset(APPLY_REFUSAL_TOKENS) == UNRESOLVED_TOKEN_SITES[
        "apps.cli.commands.do_cmd:_cmd_job_apply:error"][0]


# The top-level keys of the answers (DECISIONs F298 D5, D6 and D7).

#: The calls that print or build an answer envelope; a keyword of any of them is an answer key.
_ANSWER_CALLS = frozenset({"emit_ok", "build_ok", "fail", "emit_error", "build_error"})

#: The keywords of those calls that are not answer keys: the envelope's own two and the arguments
#: of `fail` that choose the output and the exit code.
_NOT_ANSWER_KEYS = frozenset({"error", "message", "json_output", "exit_code"})

#: The envelope's keys, which every answer carries and the interface names under `envelope`.
_ENVELOPE_KEYS = frozenset({"schema_version", "ok", "error", "message"})

#: An answer site this static reading cannot resolve to keys, keyed `<module>:<function>:**<expression>`,
#: with the keys a reader verified by hand and why. A site absent from this mapping fails the
#: reading test with its location.
UNRESOLVED_ANSWER_SITES: dict[str, tuple[frozenset[str], str]] = {
    "apps.cli.job_id_arg:refuse_ambiguous_job_id:**payload": (
        frozenset(),
        "passes its caller's keywords through; every call on these operations' paths passes none",
    ),
    "apps.cli.job_id_arg:resolve_job_id_or_fail:**payload": (
        frozenset(),
        "passes its caller's keywords through; every call on these operations' paths passes none",
    ),
    "apps.cli.commands.do_cmd:_cmd_job_run:**report": (
        frozenset({
            "context_strategy", "cost_mirror", "created_at", "execution_config", "finished_at",
            "handoff_available", "has_workspace_changes", "isolation_mode", "job_id", "job_title",
            "job_workspace_path", "next_command", "pending_tasks", "postmortem",
            "repair_rounds_allowed", "repair_rounds_source", "repo_path", "result_diff", "status",
            "target_guard", "tasks", "warning", "worktree",
        }),
        "the keys export_job_report in packages/orchestration/pingpong_job.py returns, and the "
        "cost_mirror _cmd_job_run stores into that report",
    ),
    "apps.cli.commands.do_cmd:_cmd_job_apply:**export_job_apply_json(result)": (
        frozenset({
            "approved", "blocked_reason", "blocked_reasons", "commit_message_mode", "commit_sha",
            "commit_with_history", "context_strategy", "dry_run", "execution_config",
            "file_readiness", "files_applied", "files_blocked", "files_planned", "files_skipped",
            "finished_at", "history_commits", "job_apply_id", "job_id", "job_status", "job_title",
            "job_workspace_path", "merge_commit", "merge_conflicts", "merged_branch",
            "missing_source_files", "modes_applied", "post_test_command_present",
            "post_test_passed", "post_test_summary", "push", "push_error", "push_open_criteria",
            "push_ref", "push_remote", "pushed", "reviewed_task_files", "skip_blocked",
            "source_changed_files", "started_at", "status", "target_branch", "target_clean",
            "target_guard_ok", "target_repo", "task_summaries", "temporary_worktree_cleanup",
            "unexpected_source_files",
        }),
        "the keys export_job_apply_json in packages/orchestration/job_apply.py returns",
    ),
    "apps.cli.commands.change:_cmd_change_proof:**export_proof_chain_json(chain)": (
        frozenset({
            "changes", "generated_at", "goal", "job_applies", "job_id", "missing_links",
            "next_safe_action", "next_safe_action_obj", "overall_status", "path_filter", "version",
        }),
        "the keys export_proof_chain_json in packages/orchestration/proof_chain.py returns",
    ),
    "apps.cli.commands.do_cmd:_cmd_job_evidence:**result": (
        frozenset({"files", "job_id", "manifest", "out_dir"}),
        "the keys export_job_evidence in packages/orchestration/job_evidence.py returns; its "
        "other return, a missing job, is answered as job_not_found and never printed",
    ),
    "apps.cli.commands.patch:_cmd_approve_hunks:**result.exported": (
        frozenset({"attempt", "decided_at", "hunks", "task_id"}),
        "a HunkDecisionRecord's exported record, whose keys are _RECORD_KEYS in "
        "packages/orchestration/hunk_decision_record.py",
    ),
    "apps.cli.commands.client_cmd:_cmd_client_interface:**interface": (
        frozenset({
            "answer_trees", "answers", "approval_recommendations", "approval_risks", "budget_kinds",
            "contract_templates", "digest", "envelope", "exit_codes", "interface_version",
            "job_states", "mission_statuses", "operations",
        }),
        "the keys build_client_interface in apps/cli/client_interface.py returns",
    ),
    "apps.cli.commands.client_cmd:_cmd_client_changes:**changes": (
        frozenset({
            "applies", "closed_decisions", "cursor", "decisions", "degraded", "jobs", "missions",
            "overlap_seconds", "read_at", "since", "skipped_files",
        }),
        "the keys build_client_changes in packages/orchestration/client_changes.py returns",
    ),
    "apps.cli.commands.job:_cmd_job_resume:**preview": (
        frozenset({
            "action", "budget_stop", "checkpoint_index", "job_id", "pending_tasks",
            "plan_approval_gate", "resumed", "state", "stop_request", "would_run", "worktree_head",
        }),
        "the keys _resume_preview in apps/cli/commands/job.py returns",
    ),
    "apps.cli.commands.job:_cmd_job_run_cycles:**result.to_json()": (
        frozenset({
            "awaiting_checks", "cycles", "cycles_run", "job_id", "job_status", "open_decision_ids",
            "stop_reason", "terminal_status",
        }),
        "the keys CycleLoopResult.to_json in packages/orchestration/long_run_executor.py returns; "
        "run_cycles returns a CycleLoopResult",
    ),
    "apps.cli.commands.job:_cmd_resume:**_payload": (
        frozenset({
            "blocked_reason", "checkpoint_id", "checkpoint_kind", "output_truncated",
            "persisted_output_bytes", "redaction", "resume_mode", "resumed", "stage",
            "stop_reason", "test_run_id", "tests_passed", "worktrees",
        }),
        "the keys export_resume_result_json in packages/orchestration/event_replay.py returns, and "
        "the worktrees _cmd_resume stores into that payload",
    ),
    "apps.cli.commands.job:_cmd_resume:**export_dry_run_json(dr)": (
        frozenset({
            "blocked_reason", "can_resume", "checkpoint_id", "checkpoint_kind", "job_id",
            "next_command", "redaction", "required_approvals", "required_capabilities",
            "safety_summary", "would_run_stage",
        }),
        "the keys export_dry_run_json in packages/orchestration/event_replay.py returns",
    ),
    "apps.cli.commands.client_cmd:_cmd_client_order:**payload": (
        frozenset({
            "answer", "ended_at", "exit_code", "order_file", "order_id", "started_at", "state",
        }),
        "the keys order_record_payload in packages/orchestration/serve_runs.py returns, shared "
        "with GET /api/v1/orders/{order} and the 202 answer of POST /api/v1/orders (DECISION "
        "F253 D14 (4))",
    ),
    "apps.cli.commands.client_cmd:_cmd_client_run:**payload": (
        frozenset({
            "answer", "ended_at", "err_log", "exit_code", "job_id", "out_log", "pid",
            "started_at", "state",
        }),
        "the keys run_record_payload in packages/orchestration/serve_runs.py returns, shared "
        "with GET /api/v1/jobs/{job}/run and the 202 answer of POST /api/v1/jobs/{job}/run "
        "(DECISION F253 D20)",
    ),
}


def _dict_display_keys(value: ast.AST | None) -> set[str] | None:
    """The string keys of a dict literal, or of a `dict(...)` call made of keywords alone; None for
    any other expression."""
    if isinstance(value, ast.Dict):
        return {key.value for key in value.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)}
    if (isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "dict"
            and not value.args and all(keyword.arg is not None for keyword in value.keywords)):
        return {keyword.arg for keyword in value.keywords}
    return None


def _bound_dict_keys(fn: ast.AST, name: str) -> set[str] | None:
    """The string keys of the dict literal, or keyword-only `dict(...)` call, `name` is bound to in
    `fn`, with every `name["key"] = ...` store there; None when `fn` binds `name` to neither."""
    keys: set[str] = set()
    bound = False
    for node in ast.walk(fn):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        for target in node.targets if isinstance(node, ast.Assign) else [node.target]:
            displayed = _dict_display_keys(node.value)
            if isinstance(target, ast.Name) and target.id == name and displayed is not None:
                bound = True
                keys |= displayed
            if (isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name)
                    and target.value.id == name and isinstance(target.slice, ast.Constant)
                    and isinstance(target.slice.value, str)):
                keys.add(target.slice.value)
    return keys if bound else None


def _answer_sites(fn: ast.AST, modname: str) -> tuple[set[str], set[str], set[str]]:
    """The answer keys `fn`'s own body names, its unresolved answer sites, and its bare-name calls."""
    keys: set[str] = set()
    unresolved: set[str] = set()
    calls: set[str] = set()
    for node in ast.walk(fn):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
            continue
        if node.func.id not in _ANSWER_CALLS:
            calls.add(node.func.id)
            continue
        for keyword in node.keywords:
            if keyword.arg is not None:
                if keyword.arg not in _NOT_ANSWER_KEYS:
                    keys.add(keyword.arg)
                continue
            bound = (_bound_dict_keys(fn, keyword.value.id)
                     if isinstance(keyword.value, ast.Name) else None)
            if bound is None:
                unresolved.add(f"{modname}:{fn.name}:**{ast.unparse(keyword.value)}")
            else:
                keys |= bound
    return keys, unresolved, calls


_answer_memo: dict[tuple[str, str], tuple[set[str], set[str]]] = {}


def _handler_answer_keys(command_id: str) -> set[str]:
    return _handler_reading(command_id, _answer_sites, _answer_memo, UNRESOLVED_ANSWER_SITES)


def _function_def(path: str, function: str) -> ast.FunctionDef:
    """The one definition of `function` in `path`; `Class.method` names a method of one class."""
    scope: ast.AST = ast.parse((_REPO_ROOT / path).read_text(encoding="utf-8"))
    *classes, name = function.split(".")
    for class_name in classes:
        [scope] = [node for node in ast.walk(scope)
                   if isinstance(node, ast.ClassDef) and node.name == class_name]
    [fn] = [node for node in ast.walk(scope) if isinstance(node, ast.FunctionDef) and node.name == name]
    return fn


def _stored_keys(path: str, function: str, name: str) -> set[str]:
    """Every key `function` in `path` stores into `name` with `name["key"] = ...`."""
    return {target.slice.value for node in ast.walk(_function_def(path, function))
            if isinstance(node, ast.Assign) for target in node.targets
            if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name)
            and target.value.id == name and isinstance(target.slice, ast.Constant)}


def _returned_dict_keys(path: str, function: str) -> set[str]:
    """The string keys of the dict literal `function` in `path` returns, directly or as the name its
    `return` statement passes on."""
    fn = _function_def(path, function)
    [returned] = [node.value for node in fn.body if isinstance(node, ast.Return)]
    if isinstance(returned, ast.Call) and returned.args:
        returned = returned.args[0]
    if isinstance(returned, ast.Name):
        keys = _bound_dict_keys(fn, returned.id)
        assert keys is not None, f"{function} returns {returned.id}, which it binds to no dict literal"
        return keys
    assert isinstance(returned, ast.Dict), f"{function} returns no dict literal"
    return {key.value for key in returned.keys if isinstance(key, ast.Constant)}


def test_every_declared_answer_is_a_sorted_list_of_payload_keys():
    assert sorted(OPERATION_ANSWER_KEYS) == sorted(CLIENT_OPERATION_IDS)
    for command_id, keys in OPERATION_ANSWER_KEYS.items():
        assert list(keys) == sorted(set(keys)), f"{command_id}: keys not sorted or repeated"
        assert not set(keys) & _ENVELOPE_KEYS, f"{command_id}: names an envelope key as its own"


@pytest.mark.parametrize("command_id", sorted(OPERATION_ANSWER_KEYS))
def test_declared_answer_keys_equal_the_keys_the_handler_reaches(command_id):
    assert sorted(_handler_answer_keys(command_id)) == list(OPERATION_ANSWER_KEYS[command_id])


def test_the_hand_verified_answer_key_sets_still_equal_what_their_code_names():
    from packages.orchestration import hunk_decision_record

    sites = {site: keys for site, (keys, _why) in UNRESOLVED_ANSWER_SITES.items()}
    assert sites["apps.cli.commands.do_cmd:_cmd_job_run:**report"] == (
        _returned_dict_keys("packages/orchestration/pingpong_job.py", "export_job_report")
        | _stored_keys("apps/cli/commands/do_cmd.py", "_cmd_job_run", "report"))
    assert sites["apps.cli.commands.do_cmd:_cmd_job_apply:**export_job_apply_json(result)"] == (
        _returned_dict_keys("packages/orchestration/job_apply.py", "export_job_apply_json"))
    assert sites["apps.cli.commands.change:_cmd_change_proof:**export_proof_chain_json(chain)"] == (
        _returned_dict_keys("packages/orchestration/proof_chain.py", "export_proof_chain_json"))
    assert sites["apps.cli.commands.do_cmd:_cmd_job_evidence:**result"] == (
        _returned_dict_keys("packages/orchestration/job_evidence.py", "export_job_evidence"))
    assert sites["apps.cli.commands.patch:_cmd_approve_hunks:**result.exported"] == (
        set(hunk_decision_record._RECORD_KEYS))
    assert sites["apps.cli.commands.client_cmd:_cmd_client_interface:**interface"] == (
        _returned_dict_keys("apps/cli/client_interface.py", "build_client_interface"))
    assert sites["apps.cli.commands.job:_cmd_job_resume:**preview"] == (
        _returned_dict_keys("apps/cli/commands/job.py", "_resume_preview"))
    assert sites["apps.cli.commands.job:_cmd_job_run_cycles:**result.to_json()"] == (
        _returned_dict_keys("packages/orchestration/long_run_executor.py", "CycleLoopResult.to_json"))
    assert sites["apps.cli.commands.job:_cmd_resume:**_payload"] == (
        _returned_dict_keys("packages/orchestration/event_replay.py", "export_resume_result_json")
        | _stored_keys("apps/cli/commands/job.py", "_cmd_resume", "_payload"))
    assert sites["apps.cli.commands.job:_cmd_resume:**export_dry_run_json(dr)"] == (
        _returned_dict_keys("packages/orchestration/event_replay.py", "export_dry_run_json"))


# The keys under the answers' top-level keys (DECISION F298 D8).

def _tree_names(tree: dict | str | None) -> set[str]:
    """Every key a tree names at any depth, without the data key `*`."""
    names: set[str] = set()
    for key, below in (tree if isinstance(tree, dict) else {}).items():
        if key != "*":
            names.add(key)
        names |= _tree_names(below)
    return names


def _leaf_paths(tree: dict, leaf: str | None, prefix: tuple[str, ...] = ()) -> set[tuple[str, ...]]:
    """Every path in a tree whose key maps to `leaf`, None or the repeat mark, instead of a tree."""
    paths: set[tuple[str, ...]] = set()
    for key, below in tree.items():
        if below == leaf:
            paths.add((*prefix, key))
        elif isinstance(below, dict):
            paths |= _leaf_paths(below, leaf, (*prefix, key))
    return paths


def _undeclared_paths(returned: dict, declared: dict | None,
                      prefix: tuple[str, ...] = ()) -> list[tuple[str, ...]]:
    """Every path of a returned key tree that a declared tree does not name; `*` names any key, a
    declared None admits everything under it, and the repeat mark names the declared tree that holds
    it again."""
    if declared is None:
        return []
    undeclared: list[tuple[str, ...]] = []
    for key, below in returned.items():
        if key not in declared and "*" not in declared:
            undeclared.append((*prefix, key))
            continue
        below_declared = declared.get(key, declared.get("*"))
        if below_declared == KEY_TREE_REPEAT_MARK:
            below_declared = declared
        undeclared += _undeclared_paths(below, below_declared, (*prefix, key))
    return undeclared


def _expression_keys(path: str, expression: str) -> set[str]:
    """Every key the module in `path` adds to `expression`: the keys of the dict literal it appends,
    the keywords of its `update(...)` and every `expression["key"] = ...` store."""
    keys: set[str] = set()
    for node in ast.walk(ast.parse((_REPO_ROOT / path).read_text(encoding="utf-8"))):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and ast.unparse(node.func.value) == expression):
            if node.func.attr == "append":
                [appended] = node.args
                assert isinstance(appended, ast.Dict), f"{expression}.append of no dict literal"
                keys |= {key.value for key in appended.keys if isinstance(key, ast.Constant)}
            if node.func.attr == "update":
                assert not node.args and all(k.arg is not None for k in node.keywords), (
                    f"{expression}.update with keys no reader resolves")
                keys |= {keyword.arg for keyword in node.keywords}
        if isinstance(node, ast.Assign):
            keys |= {target.slice.value for target in node.targets
                     if isinstance(target, ast.Subscript)
                     and ast.unparse(target.value) == expression
                     and isinstance(target.slice, ast.Constant)}
    return keys


def test_every_answer_tree_hangs_under_a_declared_top_level_key():
    assert sorted(ANSWER_KEY_TREES) == sorted(CLIENT_OPERATION_IDS), "an operation without an entry"
    repeated: set[tuple[str, ...]] = set()
    for command_id, trees in ANSWER_KEY_TREES.items():
        assert sorted(set(trees) - set(OPERATION_ANSWER_KEYS[command_id])) == [], command_id
        for key, tree in trees.items():
            assert isinstance(tree, dict) and tree, f"{command_id} {key}: an empty or opaque tree"
            assert all(path[-2:] == ("check", "spec") for path in _leaf_paths(tree, None)), (
                f"{command_id} {key}: a key the interface does not fix, other than a check's spec")
            repeated |= {(command_id, key, *path) for path in _leaf_paths(tree, KEY_TREE_REPEAT_MARK)}
    # The shapes that repeat themselves: a mission plan's earlier versions, and the key trees the
    # interface itself answers.
    assert repeated == {("mission.abandon", "mission", "mission_plan", "_versions"),
                        ("client.interface", "digest", "*"),
                        ("client.interface", "answer_trees", "*", "*", "*")}


def test_the_do_answer_trees_name_exactly_what_their_code_builds():
    from packages.orchestration import mission_contract
    from packages.orchestration.dod_schema import DoDCheck

    do_sequence = "packages/orchestration/do_sequence.py"
    contracts = "packages/orchestration/mission_contract.py"
    trees = ANSWER_KEY_TREES["do.run"]
    contract = trees["contract"]
    assert contract is MISSION_CONTRACT_KEY_TREE
    assert set(contract) == set(mission_contract._CONTRACT_FIELDS) == (
        _returned_dict_keys(contracts, "MissionContract.to_json"))
    assert set(contract["criteria"]) == set(mission_contract._CRITERION_FIELDS) == (
        _returned_dict_keys(contracts, "ContractCriterion.to_json"))
    assert set(contract["amendments"]) == set(mission_contract._AMENDMENT_FIELDS)
    assert set(contract["criteria"]["check"]) == set(DoDCheck.model_fields)
    assert _tree_names(trees["cost"]) == _dict_literal_keys(_REPO_ROOT / do_sequence,
                                                            "do_cost_summary")
    assert _tree_names(trees["jobs"]) == _dict_literal_keys(_REPO_ROOT / do_sequence,
                                                            "do_job_task_listing")
    assert set(trees["steps"]) == _returned_dict_keys(do_sequence, "DoStepResult.to_json")
    assert set(trees["landed"]) == _expression_keys(do_sequence, "ctx.landed")
    assert set(trees["push"]) == (_returned_dict_keys(do_sequence, "_do_push_record")
                                  | _expression_keys(do_sequence, "ctx.push_outcome"))


def _dict_value_keys(path: str, function: str, key: str) -> set[str]:
    """The string keys of every dict literal `function` in `path` puts under `key`, as the value of
    a dict literal's entry or of a `name["key"] = ...` store, either branch of a conditional
    expression and the element of a list comprehension included."""
    values: list[ast.AST] = []
    for node in ast.walk(_function_def(path, function)):
        if isinstance(node, ast.Dict):
            values += [value for name, value in zip(node.keys, node.values)
                       if isinstance(name, ast.Constant) and name.value == key]
        if isinstance(node, ast.Assign):
            values += [node.value for target in node.targets
                       if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant)
                       and target.slice.value == key]
    keys: set[str] = set()
    for value in values:
        for branch in (value.body, value.orelse) if isinstance(value, ast.IfExp) else (value,):
            if isinstance(branch, ast.ListComp):
                branch = branch.elt
            keys |= _dict_display_keys(branch) or set()
    assert keys, f"{function} puts no dict literal under {key}"
    return keys


def test_the_job_run_answer_trees_name_exactly_what_their_code_builds():
    pingpong = "packages/orchestration/pingpong_job.py"
    trees = ANSWER_KEY_TREES["job.run"]
    assert trees is JOB_REPORT_KEY_TREES
    tasks = trees["tasks"]
    assert set(tasks) == _bound_dict_keys(_function_def(pingpong, "export_job_report"), "report")
    assert set(tasks["apply_manifest"]) == _returned_dict_keys(pingpong, "_export_apply_manifest")
    assert set(tasks["apply_manifest"]["applied_file_proofs"]) == (
        _returned_dict_keys(pingpong, "_export_file_proof"))
    assert set(tasks["proof_summary"]) == _returned_dict_keys(pingpong, "_export_proof_summary")
    assert set(tasks["veto"]) == _dict_value_keys(pingpong, "export_job_report", "veto")
    assert set(tasks["steering_not_consumed"]) == _dict_literal_keys(
        _REPO_ROOT / pingpong, "_task_steering_not_consumed_map")
    for key in ("worktree", "result_diff", "postmortem", "context_strategy"):
        assert set(trees[key]) == _dict_value_keys(pingpong, "export_job_report", key), key
    assert trees["execution_config"] is EXECUTION_CONFIG_KEY_TREE
    assert set(EXECUTION_CONFIG_KEY_TREE) == _returned_dict_keys(pingpong, "_export_execution_config")
    assert not any(EXECUTION_CONFIG_KEY_TREE.values()), "an execution config key with keys below it"
    assert trees["target_guard"] is TARGET_GUARD_KEY_TREE
    assert set(TARGET_GUARD_KEY_TREE) == _returned_dict_keys(pingpong, "_export_target_guard")
    assert not any(TARGET_GUARD_KEY_TREE.values()), "a target guard key with keys below it"
    assert set(trees["cost_mirror"]) == _dict_literal_keys(
        _REPO_ROOT / "packages/orchestration/job_evidence.py", "mirror_job_run_into_ledger")


def test_the_job_resume_answer_trees_name_exactly_what_their_code_builds():
    from typing import Any, get_type_hints

    from packages.orchestration import worktree_resume
    from packages.orchestration.long_run_executor import CycleLoopResult, CycleRecord

    job_cmd = "apps/cli/commands/job.py"
    trees = ANSWER_KEY_TREES["job.resume"]
    # A job the ping-pong engine already ran is handed to `remedy job run`'s handler, so the
    # answer is that job's report, under the same trees.
    [handoff] = [ast.unparse(node) for node in ast.walk(_function_def(job_cmd, "_cmd_job_resume"))
                 if isinstance(node, ast.Call) and ast.unparse(node.func) == "_cmd_job_run"]
    assert handoff == "_cmd_job_run(str(job.job_id), json_output=json_output)"
    assert all(trees[key] is below for key, below in JOB_REPORT_KEY_TREES.items())
    # The preview answers what each of its checks would decide.
    preview = _function_def(job_cmd, "_resume_preview")
    [returned] = [node.value for node in preview.body if isinstance(node, ast.Return)]
    values = {key.value: ast.unparse(value) for key, value in zip(returned.keys, returned.values)}
    for key, name in (("stop_request", "stop"), ("worktree_head", "head"), ("budget_stop", "budget_stop")):
        assert values[key] == name and set(trees[key]) == _bound_dict_keys(preview, name), key
    # The single pass answers each check its verification failed.
    [failures] = [keyword.value for node in ast.walk(_function_def(job_cmd, "_cmd_run_next_task_local"))
                  if isinstance(node, ast.Call) and ast.unparse(node.func) == "dict"
                  for keyword in node.keywords if keyword.arg == "failures"]
    assert isinstance(failures, ast.ListComp)
    assert set(trees["failures"]) == _dict_display_keys(failures.elt)
    # The multi-cycle executor answers one record per cycle it ran.
    long_run = "packages/orchestration/long_run_executor.py"
    assert set(trees["cycles"]) == _returned_dict_keys(long_run, "CycleRecord.to_json")
    assert ast.unparse(_bound_dict_values(long_run, "CycleLoopResult.to_json", "payload")["cycles"]) == (
        "[c.to_json() for c in self.cycles]")
    assert get_type_hints(CycleLoopResult)["cycles"] == tuple[CycleRecord, ...]
    # A replay resume answers each worktree it prepared, as each worktree's outcome.
    assert set(trees["worktrees"]) == _returned_dict_keys(
        "packages/orchestration/worktree_resume.py", "WorktreeResumeOutcome.to_json")
    resume = _function_def(job_cmd, "_cmd_resume")
    assert {ast.unparse(keyword.value) for node in ast.walk(resume) if isinstance(node, ast.Call)
            for keyword in node.keywords if keyword.arg == "worktrees"} == {
        "[o.to_json() for o in wt_outcomes]", "wt_json"}
    assert _bound_sources(job_cmd, "_cmd_resume", "wt_json") == {"[o.to_json() for o in wt_outcomes]"}
    assert _subscript_stores(job_cmd, "_cmd_resume", "_payload") == {"'worktrees'"}
    assert _subscript_stores(job_cmd, "_cmd_resume", "wt_json") == {"idx"}
    assert _bound_sources(job_cmd, "_cmd_resume", "out") == {
        "_wtr.finalize_worktree_resume(s)", "_wtr.retain_worktree_resume(s, reason)"}
    for function in (worktree_resume.finalize_worktree_resume, worktree_resume.retain_worktree_resume):
        assert get_type_hints(function)["return"] is worktree_resume.WorktreeResumeOutcome
    assert get_type_hints(worktree_resume.prepare_job_worktrees)["return"] == (
        list[tuple[Any, worktree_resume.WorktreeResumeOutcome]])


#: Every expression the functions `remedy job resume` answers through write each top-level key with
#: that `ANSWER_KEY_TREES` gives no tree, per function, read by hand: each is a word, a number, a
#: flag, a path, an id, None or a count, so it carries no keys below the top level. The keys of the
#: job report the resume hands to `remedy job run`'s handler are that command's.
_RESUME_PLAIN_SOURCES: dict[str, dict[str, set[str]]] = {
    "_cmd_job_resume": {
        "action": {"'noop'", "'stopped'"},
        "decision_id": {"_decision_id"},
        "job_id": {"jid"},
        "reason": {"'all_green'"},
        "resumed": {"False"},
        "stop_reason": {"decision.reason"},
    },
    "_resume_preview": {
        "action": {"'preview'"},
        "checkpoint_index": {"getattr(checkpoint, 'cycle_index', None) if checkpoint else None"},
        "job_id": {"jid"},
        "pending_tasks": {"len(pending_tasks)"},
        "plan_approval_gate": {"gate"},
        "resumed": {"False"},
        "state": {"state"},
        "would_run": {"not stop['pending'] and head_outcome != 'drift' and (gate == 'open') and "
                      "(state not in ('all_green', 'cancelled')) and (not budget_stopped)"},
    },
    "_cmd_run_next_task_local": {
        "dry_run": {"dry_run_block or None"},
        "elapsed_ms": {"round(elapsed_ms)"},
        "file": {"str(mf.path)"},
        "job_id": {"str(job.job_id)", "str(result.job.job_id)"},
        "log": {"str(log.path)"},
        "model": {"builder.model"},
        "outcome": {"'no_pending_tasks'"},
        "patch_intents": {"patch_intent_count"},
        "remaining": {"pending_remaining"},
        "repo": {"repo_applied[0] if repo_applied else None"},
        "task_id": {"str(result.task_id)"},
        "task_type": {"task_type"},
        "verified": {"False", "True"},
    },
    "_cmd_resume": {
        "blocked_reason": {"'ambiguous_recoverable_worktrees'", "'resume_mode_not_implemented'",
                           "'worktree_recovery_blocked'"},
        "checkpoint_kind": {"cp.kind"},
        "resume_mode": {"cp.resume_mode"},
        "resumed": {"False"},
    },
}

#: The dicts those functions answer whole, by the expression they expand.
_RESUME_EXPANDED: dict[str, set[str]] = {
    "_cmd_job_resume": {"preview"},
    "_cmd_job_run_cycles": {"result.to_json()"},
    "_cmd_run_next_task_local": {"envelope_payload"},
    "_cmd_resume": {"_payload", "export_dry_run_json(dr)"},
}


def _plain_hint(hint) -> bool:
    """A type whose JSON value carries no keys: a word, a number, a flag, None, an optional one of
    those, or a list or tuple of words."""
    from typing import Union, get_args, get_origin

    if hint in (str, int, float, bool, type(None)):
        return True
    if get_origin(hint) in (Union, __import__("types").UnionType):
        return all(_plain_hint(arg) for arg in get_args(hint))
    return get_origin(hint) in (list, tuple) and set(get_args(hint)) <= {str, Ellipsis}


def test_the_job_resume_keys_without_a_tree_hold_no_object():
    from typing import get_type_hints

    from packages.orchestration.event_replay import ResumeDryRun, ResumeResult
    from packages.orchestration.long_run_executor import CycleLoopResult

    job_cmd = "apps/cli/commands/job.py"
    trees = ANSWER_KEY_TREES["job.resume"]
    for function in sorted(set(_RESUME_PLAIN_SOURCES) | set(_RESUME_EXPANDED)):
        expected = _RESUME_PLAIN_SOURCES.get(function, {})
        fn = _function_def(job_cmd, function)
        sources: dict[str, set[str]] = {}
        expanded: set[str] = set()
        for node in ast.walk(fn):
            if not isinstance(node, ast.Call):
                continue
            answered = isinstance(node.func, ast.Name) and node.func.id in _ANSWER_CALLS
            if answered or ast.unparse(node.func) == "dict":
                for keyword in node.keywords:
                    if keyword.arg is None:
                        expanded.add(ast.unparse(keyword.value))
                    elif keyword.arg not in _NOT_ANSWER_KEYS | {"json_output", "exit_code"}:
                        sources.setdefault(keyword.arg, set()).add(ast.unparse(keyword.value))
        if function == "_resume_preview":
            [returned] = [node.value for node in fn.body if isinstance(node, ast.Return)]
            sources = {key.value: {ast.unparse(value)} for key, value in zip(returned.keys, returned.values)}
        assert expanded == _RESUME_EXPANDED.get(function, set()), function
        assert {key: below for key, below in sources.items() if key not in trees} == expected, function
    # The dicts answered whole are exports of records whose fields are plain, but for the cycles,
    # which `job.resume` gives a tree.
    exports = (("packages/orchestration/event_replay.py", "export_resume_result_json", ResumeResult),
               ("packages/orchestration/event_replay.py", "export_dry_run_json", ResumeDryRun),
               ("packages/orchestration/long_run_executor.py", "CycleLoopResult.to_json", CycleLoopResult))
    for path, function, record in exports:
        fn = _function_def(path, function)
        [returned] = [node.value for node in fn.body if isinstance(node, ast.Return)]
        if isinstance(returned, ast.Name):
            returned = _bound_dict_values(path, function, returned.id)
        else:
            returned = dict(zip((key.value for key in returned.keys), returned.values))
        hints = get_type_hints(record)
        for key, value in returned.items():
            if key in trees and trees[key]:
                continue
            # A `str(...)` answers a word; a `list(...)` answers the elements of what it copies.
            if isinstance(value, ast.Constant) or (
                    isinstance(value, ast.Call) and ast.unparse(value.func) == "str"):
                continue
            if isinstance(value, ast.Call) and ast.unparse(value.func) == "list":
                [value] = value.args
            assert isinstance(value, ast.Attribute), f"{function}: {key} answers {ast.unparse(value)}"
            field = value.attr
            hint = (hints[field] if field in hints
                    else get_type_hints(getattr(record, field).fget)["return"])
            assert _plain_hint(hint), f"{function}: {key} answers a {hint}"


def _bound_dict_values(path: str, function: str, name: str) -> dict[str, ast.AST]:
    """The values of the dict literal `function` in `path` binds `name` to, by key."""
    [bound] = [node.value for node in ast.walk(_function_def(path, function))
               if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict)
               and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)]
    return {key.value: value for key, value in zip(bound.keys, bound.values)}


def test_the_job_apply_answer_trees_name_exactly_what_their_code_builds():
    from typing import get_type_hints

    from packages.orchestration.job_apply import JobApplyResult

    job_apply = "packages/orchestration/job_apply.py"
    trees = ANSWER_KEY_TREES["job.apply"]
    for key in ("temporary_worktree_cleanup", "task_summaries", "file_readiness"):
        assert set(trees[key]) == _dict_value_keys(job_apply, "export_job_apply_json", key), key
    # The paths a job changed are the keys of `modes_applied`, each mapped to its file mode.
    assert trees["modes_applied"] == {"*": {}}
    assert get_type_hints(JobApplyResult)["modes_applied"] == dict[str, str]
    # The apply's execution configuration is the job's, through the exporter `job run` answers.
    assert trees["execution_config"] is EXECUTION_CONFIG_KEY_TREE
    module = ast.parse((_REPO_ROOT / job_apply).read_text(encoding="utf-8"))
    sources = {ast.unparse(node.value) for node in ast.walk(module) if isinstance(node, ast.Assign)
               and any(ast.unparse(target) in ("result.execution_config", "ec")
                       for target in node.targets)}
    assert sources == {"_export_execution_config(job.execution_config)", "ec or {}"}


def test_the_status_and_proof_answer_trees_name_exactly_what_their_code_builds():
    from packages.orchestration.job_apply import JOB_APPLY_PROOF_FIELDS

    status_cmd = "apps/cli/commands/status_cmd.py"
    proof_chain = "packages/orchestration/proof_chain.py"
    status = ANSWER_KEY_TREES["status.run"]
    # `jobs` maps each job state word to the jobs in that state.
    assert set(status["jobs"]) == {"*"}
    assert set(status["jobs"]["*"]) == _expression_keys(status_cmd, "by_state[state]")
    # `client` is the digest, which the digest's own tests hold.
    assert status["client"] is DIGEST_KEY_TREE
    stored = {ast.unparse(node.value) for node in ast.walk(_function_def(status_cmd, "_cmd_status"))
              if isinstance(node, ast.Assign)
              and any(ast.unparse(target) == "result['client']" for target in node.targets)}
    assert stored == {"build_client_digest(every_ended_job=all_ended_jobs)"}
    proof = ANSWER_KEY_TREES["change.proof"]
    next_action = _dict_literal_keys(_REPO_ROOT / proof_chain, "_export_next_action")
    assert set(proof["next_safe_action_obj"]) == next_action == (
        _returned_dict_keys(proof_chain, "_export_next_action"))
    assert set(proof["changes"]) == _dict_value_keys(proof_chain, "export_proof_chain_json", "changes")
    assert set(proof["changes"]["next_safe_action_obj"]) == next_action
    assert set(proof["job_applies"]) == set(JOB_APPLY_PROOF_FIELDS)


def test_the_job_evidence_answer_trees_name_exactly_what_their_code_builds():
    from packages.orchestration import job_evidence, pingpong_job

    evidence = "packages/orchestration/job_evidence.py"
    trees = ANSWER_KEY_TREES["job.evidence"]
    # `files` maps the path of each file written into the bundle to where it was written.
    assert trees["files"] == {"*": {}}
    [written] = [node for node in ast.walk(_function_def(evidence, "export_job_evidence"))
                 if isinstance(node, ast.AnnAssign) and ast.unparse(node.target) == "written"]
    assert ast.unparse(written.annotation) == "dict[str, str]"
    manifest = trees["manifest"]
    assert set(manifest) == (_returned_dict_keys(evidence, "_build_job_manifest")
                             | _stored_keys(evidence, "export_job_evidence", "manifest"))
    [returned] = [node.value for node in _function_def(evidence, "_build_job_manifest").body
                  if isinstance(node, ast.Return)]
    values = {key.value: value for key, value in zip(returned.keys, returned.values)}
    # The two maps are keyed by task id, each holding a word.
    for key in ("task_statuses", "task_run_ids"):
        assert manifest[key] == {"*": {}} and isinstance(values[key], ast.DictComp), key
    assert manifest["execution_config"] is EXECUTION_CONFIG_KEY_TREE
    assert ast.unparse(values["execution_config"]) == "_export_execution_config(job.execution_config)"
    assert job_evidence._export_execution_config is pingpong_job._export_execution_config
    assert manifest["target_guard"] is TARGET_GUARD_KEY_TREE
    assert ast.unparse(values["target_guard"]) == "_export_target_guard(job.target_guard)"
    assert job_evidence._export_target_guard is pingpong_job._export_target_guard


def test_the_patch_answer_trees_name_exactly_what_their_code_builds():
    from packages.orchestration.hunk_ledger import _EXPORT_ENTRY_KEYS

    parser = "packages/orchestration/diff_parser.py"
    patch_cmd = "apps/cli/commands/patch.py"
    view = ANSWER_KEY_TREES["patch.hunks"]["view"]
    assert set(view) == _bound_dict_keys(
        _function_def("packages/orchestration/diff_view_source.py", "build_diff_view"), "view")
    files = view["files"]
    assert set(files) == _expression_keys(parser, "files")
    assert set(files["stats"]) == _dict_value_keys(parser, "parse_unified_diff_to_view", "stats")
    assert set(files["hunks"]) == _expression_keys(parser, "hunks_out")
    assert set(files["hunks"]["lines"]) == (_expression_keys(parser, "hunk['lines']")
                                            | _stored_keys(parser, "_apply_intraline_spans", "entry"))
    decision = ANSWER_KEY_TREES["patch.hunks"]["decision"]
    assert _tree_names(decision) == _dict_literal_keys(
        _REPO_ROOT / "packages/orchestration/hunk_decision_record.py", "recorded_hunk_decision")
    assert set(decision) == _bound_dict_keys(_function_def(patch_cmd, "_cmd_show_hunks"), "decision")
    assert set(ANSWER_KEY_TREES["patch.approve-hunks"]["hunks"]) == set(_EXPORT_ENTRY_KEYS)


def test_the_patch_intent_answers_carry_no_keys_below_the_top_level():
    from packages.orchestration.approval_queue import RISK_LEVELS, RISK_UNKNOWN

    patch_cmd = "apps/cli/commands/patch.py"
    for command_id, function in (("patch.approve", "_cmd_approve_patch_intent"),
                                 ("patch.reject", "_cmd_reject_patch_intent")):
        assert ANSWER_KEY_TREES[command_id] == {}
        [answer] = [node for node in ast.walk(_function_def(patch_cmd, function))
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "emit_ok"]
        for keyword in answer.keywords:
            value = ast.unparse(keyword.value)
            assert (isinstance(keyword.value, ast.Constant) or value.startswith("bool(")
                    or value in ("entry['intent_id']", "entry['target_path']", "entry['risk']")), (
                f"{command_id}: {keyword.arg} answers {value}")
    assert all(isinstance(level, str) for level in (*RISK_LEVELS, RISK_UNKNOWN))


def _model_tree(model) -> dict:
    """The key tree a pydantic model's `model_dump()` writes: each field, and under a field whose type
    is a model, or a list of one, that model's tree."""
    from typing import get_args, get_origin

    from pydantic import BaseModel

    tree: dict = {}
    for name, field in model.model_fields.items():
        inner = get_args(field.annotation)[0] if get_origin(field.annotation) is list else field.annotation
        tree[name] = _model_tree(inner) if isinstance(inner, type) and issubclass(inner, BaseModel) else {}
    return tree


def _subscript_stores(path: str, function: str, name: str) -> set[str]:
    """The source of every subscript `function` in `path` stores into `name` with `name[...] = ...`."""
    return {ast.unparse(target.slice) for node in ast.walk(_function_def(path, function))
            if isinstance(node, ast.Assign) for target in node.targets
            if isinstance(target, ast.Subscript) and ast.unparse(target.value) == name}


def _bound_sources(path: str, function: str, name: str) -> set[str]:
    """The source of every expression `function` in `path` binds `name` to."""
    return {ast.unparse(node.value) for node in ast.walk(_function_def(path, function))
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)}


def test_the_mission_answer_trees_name_exactly_what_their_code_builds():
    from packages.orchestration.mission_compiler import PLAN_VERSION_KEY, PLAN_VERSIONS_KEY
    from packages.orchestration.mission_plan_schema import MissionPlan
    from packages.orchestration.orchestrator_loop import MILESTONES_DONE_KEY

    mission_state = "packages/orchestration/mission_state.py"
    mission_cmd = "apps/cli/commands/mission_cmd.py"
    compiler = "packages/orchestration/mission_compiler.py"
    loop = "packages/orchestration/orchestrator_loop.py"
    mission = ANSWER_KEY_TREES["mission.abandon"]["mission"]
    # The answer's mission is the record's own export, whose job links `_mission_json` widens.
    assert set(mission) == _returned_dict_keys(mission_state, "Mission.to_json")
    assert _bound_sources(mission_cmd, "_mission_json", "body") == {"mission.to_json()"}
    assert _stored_keys(mission_cmd, "_mission_json", "body") == {"job_links"}
    [link] = [node.elt for node in ast.walk(_function_def(mission_cmd, "_mission_json"))
              if isinstance(node, ast.ListComp)]
    assert [ast.unparse(value) for key, value in zip(link.keys, link.values) if key is None] == [
        "link.to_json()"]
    assert set(mission["job_links"]) == (
        _returned_dict_keys(mission_state, "MissionJobLink.to_json")
        | _dict_value_keys(mission_cmd, "_mission_json", "job_links"))
    assert set(mission["order"]) == _returned_dict_keys(mission_state, "MissionOrder.to_json")
    assert mission["contract"] is MISSION_CONTRACT_KEY_TREE
    # A mission's plan is the plan model's dump with the keys its two writers store into it.
    plan = mission["mission_plan"]
    stored = {PLAN_VERSIONS_KEY, PLAN_VERSION_KEY, MILESTONES_DONE_KEY}
    assert {key: below for key, below in plan.items() if key not in stored} == _model_tree(MissionPlan)
    assert _bound_sources(compiler, "plan_mission", "body") == {"plan.model_dump()"}
    assert _subscript_stores(compiler, "plan_mission", "body") == {"PLAN_VERSIONS_KEY", "PLAN_VERSION_KEY"}
    assert _bound_sources(loop, "mark_milestone_done", "body") == {"dict(mission.mission_plan or {})"}
    assert _subscript_stores(loop, "mark_milestone_done", "body") == {"MILESTONES_DONE_KEY"}
    writers = set()
    for path in sorted((_REPO_ROOT / "packages").rglob("*.py")) + sorted((_REPO_ROOT / "apps").rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        if "set_mission_plan" in source:
            writers |= {(path.relative_to(_REPO_ROOT).as_posix(), fn.name)
                        for fn in ast.walk(ast.parse(source)) if isinstance(fn, ast.FunctionDef)
                        for call in ast.walk(fn) if isinstance(call, ast.Call)
                        and ast.unparse(call.func).split(".")[-1] == "set_mission_plan"}
    assert writers == {(compiler, "plan_mission"), (loop, "mark_milestone_done")}
    # Each earlier version is a whole plan body, with its own earlier versions; the other two are
    # a number and a list of milestone ids.
    assert plan[PLAN_VERSIONS_KEY] == KEY_TREE_REPEAT_MARK
    assert _bound_sources(compiler, "plan_mission", "previous") == {
        "mission.mission_plan if isinstance(mission.mission_plan, dict) else None"}
    assert plan[PLAN_VERSION_KEY] == plan[MILESTONES_DONE_KEY] == {}


#: Every expression `_cmd_decision_resolve` answers each key with, over all its answer shapes, read
#: by hand: the three keys `ANSWER_KEY_TREES` names hold objects, and the others hold a word, an
#: id, a path, None or a list of ids (`closed` and the cross references are decision ids), so they
#: carry no keys below the top level. `outcome` is a word written as a literal at every site.
_DECISION_ANSWER_SOURCES: dict[str, set[str]] = {
    "answer": {"answered['answer']"},
    "answers": {"answer_records"},
    "assumption_log": {"log_path"},
    "budgets": {"result['budgets']"},
    "closed_decisions": {"closed"},
    "cross_references": {"list(answered.get('cross_references', []))"},
    "decision_id": {"decision_id"},
    "follow_up_job_id": {"follow_up_job_id"},
    "follow_up_mission": {"follow_up"},
    "job_id": {"job_id_str"},
    "mission_id": {"mission_id"},
    "next_command": {"next_command"},
    "next_step": {"REJECTED_PLAN_NEXT_STEP"},
    "option": {"answered_option"},
    "raised": {"raised"},
    "reason_code": {"sr.reason_code"},
    "state": {"result['state']"},
    "stop_id": {"sr.id"},
    "task_id": {"task_id"},
}


def test_the_decision_answer_trees_name_exactly_what_their_code_builds():
    from packages.core.models import JobBudgets

    decision = "apps/cli/commands/decision.py"
    budget = "packages/orchestration/budget_decision.py"
    trees = ANSWER_KEY_TREES["decision.resolve"]
    resolve = _function_def(decision, "_cmd_decision_resolve")
    sources: dict[str, set[str]] = {}
    for node in ast.walk(resolve):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "emit_ok":
            for keyword in node.keywords:
                sources.setdefault(keyword.arg, set()).add(ast.unparse(keyword.value))
    outcomes = sources.pop("outcome")
    assert all(ast.literal_eval(source) for source in outcomes)
    assert sources == _DECISION_ANSWER_SOURCES
    # A plan approval answers one record per bundled question.
    [records] = [node.value for node in ast.walk(resolve) if isinstance(node, ast.Assign)
                 and any(ast.unparse(target) == "answer_records" for target in node.targets)]
    assert isinstance(records, ast.ListComp)
    assert set(trees["answers"]) == _dict_display_keys(records.elt)
    # An extend answers the job's budgets after it, and the limits it raised by their names.
    assert trees["budgets"] is trees["raised"] is JOB_BUDGETS_KEY_TREE
    assert JOB_BUDGETS_KEY_TREE == _model_tree(JobBudgets)
    assert _bound_sources(decision, "_cmd_decision_resolve", "raised") == {"result['raised']"}
    [extended] = [node.value for node in _function_def(budget, "answer_budget_decision").body
                  if isinstance(node, ast.Return)]
    values = {key.value: ast.unparse(value) for key, value in zip(extended.keys, extended.values)}
    assert (values["raised"], values["budgets"]) == ("dict(raised)", "budgets_json")
    assert _bound_sources(budget, "answer_budget_decision", "budgets_json") == {
        "merged.model_dump(mode='json')"}
    assert _bound_sources(budget, "answer_budget_decision", "merged") == {
        "JobBudgets(**{**current.model_dump(mode='python'), **parsed})"}
    assert _bound_sources(budget, "answer_budget_decision", "raised") == {
        "{name: budgets_json[name] for name in parsed}"}


def _tree_leaves(tree: dict) -> list:
    """Every value in a key tree that is not a tree of its own."""
    leaves: list = []
    for below in tree.values():
        leaves += _tree_leaves(below) if isinstance(below, dict) else [below]
    return leaves


def test_the_interface_answer_trees_name_exactly_what_their_code_builds():
    interface = "apps/cli/client_interface.py"
    trees = ANSWER_KEY_TREES["client.interface"]
    [returned] = [node.value for node in _function_def(interface, "build_client_interface").body
                  if isinstance(node, ast.Return)]
    values = {key.value: value for key, value in zip(returned.keys, returned.values)}
    assert set(trees["envelope"]) == _dict_display_keys(values["envelope"])
    # Each operation is `_operation_entry`'s answer, with `_argument_entry`'s under `arguments`.
    assert ast.unparse(values["operations"]) == (
        "[_operation_entry(command_id) for command_id in CLIENT_OPERATION_IDS]")
    assert set(trees["operations"]) == _returned_dict_keys(interface, "_operation_entry")
    [entry] = [node.value for node in _function_def(interface, "_operation_entry").body
               if isinstance(node, ast.Return)]
    arguments = {key.value: value for key, value in zip(entry.keys, entry.values)}["arguments"]
    assert ast.unparse(arguments) == "[_argument_entry(arg, actions[arg.name]) for arg in entry.args]"
    assert set(trees["operations"]["arguments"]) == _returned_dict_keys(interface, "_argument_entry")
    assert isinstance(values["exit_codes"], ast.ListComp)
    assert set(trees["exit_codes"]) == _dict_display_keys(values["exit_codes"].elt)
    # The digest and the answer trees are key trees: under each name stands a key tree again, so
    # their names are data; `answers` maps each command id to a list of names.
    assert trees["digest"] == {"*": KEY_TREE_REPEAT_MARK}
    assert ast.unparse(values["digest"]) == "copy.deepcopy(DIGEST_KEY_TREE)"
    assert trees["answer_trees"] == {"*": {"*": {"*": KEY_TREE_REPEAT_MARK}}}
    assert ast.unparse(values["answer_trees"]) == "copy.deepcopy(ANSWER_KEY_TREES)"
    assert trees["answers"] == {"*": {}}
    # `ast.unparse` writes a comprehension's tuple target in brackets on Python 3.10 and without
    # them on 3.12, so the expected source is unparsed by the running interpreter too (R-1182).
    assert ast.unparse(values["answers"]) == ast.unparse(ast.parse(
        "{command_id: list(keys) for command_id, keys in OPERATION_ANSWER_KEYS.items()}", mode="eval").body)
    # A key tree holds, under a name, a tree, None or the repeat mark, and nothing else.
    assert _tree_leaves(DIGEST_KEY_TREE) == []
    assert {leaf for tree in ANSWER_KEY_TREES.values() for leaf in _tree_leaves(tree)} == {
        None, KEY_TREE_REPEAT_MARK}
    # The other top-level keys hold a word or a list of words.
    built = build_client_interface()
    for key in sorted(set(built) - set(trees)):
        assert isinstance(built[key], str) or (
            isinstance(built[key], list) and all(isinstance(word, str) for word in built[key])), key


def test_a_real_runs_answers_return_only_keys_the_interface_names(tmp_path):
    repo = _scratch_repo(tmp_path)
    order_file = tmp_path / "order.md"
    order_file.write_text(ORDER_FILE_TEXT, encoding="utf-8")
    env = {**os.environ, **_GIT_IDENTITY, "REMEDY_DATA_DIR": str(tmp_path / "data")}
    answers: dict[str, list[dict]] = {}

    def answer(command_id: str, args: list[str], expected_code: int) -> dict:
        code, body = _remedy(args, repo, env)
        assert code == expected_code, body
        answers.setdefault(command_id, []).append(body)
        return body

    answer("project.register", ["project", "register", "--repo", str(repo)], 0)
    done = answer("do.run", ["do", str(order_file), "--no-ui", "--yes", "--no-llm",
                             "--builder-provider", "fake", "--reviewer-provider", "fake",
                             "--deadline", PAST_DEADLINE], 1)
    job_id = done["job_ids"][0]
    status = answer("status.run", ["status"], 0)
    [budget] = [d for d in status["client"]["decisions"]
                if d["job_id"] == job_id and d["type"] == "token_budget"]
    # While its budget decision is open, the job's resume previews and refuses.
    previewed = answer("job.resume", ["job", "resume", job_id, "--dry-run"], 0)
    answer("job.resume", ["job", "resume", job_id], 3)
    resolved = answer("decision.resolve", ["decision", "resolve", job_id, budget["decision_id"],
                                           "--reason", "extend", "--answer",
                                           f"deadline={LATER_DEADLINE}"], 0)
    ran = answer("job.run", ["job", "run", job_id], 0)
    answer("job.apply", ["job", "apply", job_id], 0)
    applied = answer("job.apply", ["job", "apply", job_id, "--approve"], 0)
    # A result that landed cannot be declined (DECISION F304 D5).
    refused = answer("job.decline", ["job", "decline", job_id, "--reason", "not needed"], 3)
    assert refused["error"] == "job_already_applied"
    proved = answer("change.proof", ["change", "proof", job_id], 0)
    exported = answer("job.evidence", ["job", "evidence", job_id], 0)
    hunks = answer("patch.hunks", ["patch", "hunks", job_id], 0)
    answer("patch.approve-hunks", ["patch", "approve-hunks", job_id], 1)
    answer("patch.approve", ["patch", "approve", job_id, "no-such-intent"], 1)
    answer("patch.reject", ["patch", "reject", job_id, "no-such-intent"], 1)
    abandoned = answer("mission.abandon", ["mission", "abandon", done["mission_id"]], 0)
    interfaced = answer("client.interface", ["client", "interface"], 0)
    changes = answer("client.changes",
                     ["client", "changes", "--since", "2000-01-01T00:00:00Z"], 0)
    # No order the supervisor started exists on this data root; the refusal alone is this
    # combined run's coverage of client.order (DECISION F253 D13); its own real run, through
    # `OrderLauncher`, is tests/cli/test_client_order_cmd.py's.
    refused_order = answer("client.order", ["client", "order", "0123456789abcdef"], 3)
    assert refused_order["error"] == "order_not_found"
    # Likewise no run the supervisor started exists here; the refusal is this run's coverage of
    # client.run (DECISION F253 D20); its real run is tests/cli/test_client_run_cmd.py's.
    refused_run = answer("client.run", ["client", "run", "0123456789abcdef"], 3)
    assert refused_run["error"] == "run_not_found"
    assert sorted(answers) == sorted(OPERATION_ANSWER_KEYS)
    # The run reaches the levels the trees name under the answers of `remedy do`, `remedy job run`,
    # `remedy job apply`, `remedy status`, `remedy change proof`, `remedy patch hunks`,
    # `remedy job evidence`, `remedy mission abandon`, `remedy client interface`,
    # `remedy decision resolve`, `remedy job resume`'s preview and `remedy client changes`.
    assert {("contract", "criteria", "check", "kind"), ("jobs", "tasks", "deliverable"),
            ("steps", "detail")} <= _key_paths(_key_tree(done))
    assert {("tasks", "apply_manifest", "applied_file_proofs", "final_mode"),
            ("execution_config", "builder"), ("cost_mirror", "ledger_mirrored")} <= (
        _key_paths(_key_tree(ran)))
    assert {("task_summaries", "applied_files"), ("file_readiness", "workspace_status"),
            ("temporary_worktree_cleanup", "cleanup_status"), ("execution_config", "builder")} <= (
        _key_paths(_key_tree(applied)))
    assert applied["modes_applied"], "the approved apply names no path it applied"
    assert {("jobs", "stopped", "short_id"), ("client", "jobs", "cost", "basis")} <= (
        _key_paths(_key_tree(status)))
    assert {("job_applies", "commit_sha"), ("next_safe_action_obj", "label")} <= (
        _key_paths(_key_tree(proved)))
    assert {("view", "files", "hunks", "lines", "intraline"), ("view", "files", "stats", "added"),
            ("decision", "attempt_key")} <= _key_paths(_key_tree(hunks))
    assert {("manifest", "execution_config", "builder"),
            ("manifest", "target_guard", "target_mutated")} <= _key_paths(_key_tree(exported))
    assert exported["files"] and exported["manifest"]["task_statuses"], "no path or task was named"
    assert {("mission", "job_links", "job_state"), ("mission", "order", "source_sha256"),
            ("mission", "mission_plan", "milestones", "jobs_draft", "est_band"),
            ("mission", "contract", "criteria", "check", "kind")} <= _key_paths(_key_tree(abandoned))
    # A first plan has no earlier version, so a plan with two is built from the real one: the tree
    # names each earlier version's keys, and a key one of them adds is still caught.
    declared = ANSWER_KEY_TREES["mission.abandon"]
    plan = abandoned["mission"]["mission_plan"]
    for versions, undeclared in (
            ([plan, {**plan, "_versions": [plan], "_version": 2}], []),
            ([{**plan, "_versions": [{**plan, "added_key": 1}]}],
             [("mission", "mission_plan", "_versions", "_versions", "added_key")])):
        mission = {**abandoned["mission"], "mission_plan": {**plan, "_versions": versions}}
        assert _undeclared_paths(_key_tree({"mission": mission}), declared) == undeclared
    assert {("envelope", "error_keys"), ("operations", "arguments", "takes_value"),
            ("exit_codes", "meaning"), ("digest", "projects", "missions", "mission_id"),
            ("answer_trees", "mission.abandon", "mission", "mission_plan", "_versions")} <= (
        _key_paths(_key_tree(interfaced)))
    assert {("raised", "deadline"), ("budgets", "max_cost_usd"), ("budgets", "deadline")} <= (
        _key_paths(_key_tree(resolved)))
    assert {("stop_request", "pending"), ("worktree_head", "outcome"),
            ("budget_stop", "decision_id")} <= _key_paths(_key_tree(previewed))
    assert {("jobs", "evidence", "run_manifest_path"), ("missions", "job_ids")} <= (
        _key_paths(_key_tree(changes)))
    for command_id, bodies in answers.items():
        for body in bodies:
            returned = set(body) - _ENVELOPE_KEYS
            assert sorted(returned - set(OPERATION_ANSWER_KEYS[command_id])) == [], command_id
            if command_id in ANSWER_KEY_TREES:
                declared = {key: ANSWER_KEY_TREES[command_id].get(key, {})
                            for key in OPERATION_ANSWER_KEYS[command_id]}
                payload = {key: value for key, value in body.items() if key not in _ENVELOPE_KEYS}
                assert _undeclared_paths(_key_tree(payload), declared) == [], command_id


# The page's generated section is the interface rendered, and reads back as the interface
# (DECISION F298 D20).

_REGENERATE_PAGE = ('python3 -c "from apps.cli.client_interface import write_client_interface_page; '
                    'write_client_interface_page()"')
_CHILD = re.compile(r"`([^`]+)`( \(keys not fixed\)| \(repeats the object that holds it\))?")


def _page_section() -> str:
    """The generated section of the committed page, both markers included."""
    text = (_REPO_ROOT / CLIENT_INTERFACE_PAGE_PATH).read_text(encoding="utf-8")
    assert text.count(CLIENT_INTERFACE_PAGE_BEGIN) == text.count(CLIENT_INTERFACE_PAGE_END) == 1
    start = text.index(CLIENT_INTERFACE_PAGE_BEGIN)
    return text[start:text.index(CLIENT_INTERFACE_PAGE_END) + len(CLIENT_INTERFACE_PAGE_END) + 1]


def _listed_words(line: str, label: str) -> list[str]:
    """The backticked words of a `<label>: ...` line, which ends in a full stop."""
    assert line.startswith(f"{label}: ") and line.endswith("."), (label, line)
    body = line[len(label) + 2:-1]
    return [] if body == "none" else [word for word, _ in _CHILD.findall(body)]


def _table_cells(row: str) -> list[str]:
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", row)[1:-1]]


def _read_tree(bullets: list[str]) -> dict:
    """A key tree read back from its rendered bullets, one per key that holds keys."""
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for line in bullets:
        depth = (len(line) - len(line.lstrip(" "))) // 2
        name, children = re.fullmatch(r"- `([^`]+)`: (.+)", line.strip()).groups()
        while stack[-1][0] >= depth:
            stack.pop()
        parent = stack[-1][1]
        assert parent is root or parent.get(name) == {}, (name, line)
        parent[name] = {child: KEY_TREE_REPEAT_MARK if "repeats" in mark else None if mark else {}
                        for child, mark in _CHILD.findall(children)}
        stack.append((depth, parent[name]))
    return root


def _read_page_section(section: str) -> dict:
    """The interface read back from its rendered section, line by line."""
    read: dict = {"envelope": {}, "exit_codes": [], "operations": [], "answers": {},
                  "answer_trees": {}}
    labels = {"Job states": "job_states", "Mission statuses": "mission_statuses",
              "Contract templates": "contract_templates", "Budget kinds": "budget_kinds",
              "Approval recommendations": "approval_recommendations",
              "Approval risks": "approval_risks"}
    place, operation, bullets = "", None, []
    for line in [*section.splitlines(), "### End"]:
        if line.startswith(("#### ", "### ")) and bullets:
            tree = _read_tree(bullets)
            if operation is None:
                read["digest"].update(tree)
            else:
                read["answer_trees"][operation["command_id"]] = tree
            bullets = []
        label = line.split(": ", 1)[0]
        if line.startswith("### "):
            place, operation = line[4:], None
        elif line.startswith("#### "):
            operation = {"command": line[6:-1], "arguments": []}
            read["operations"].append(operation)
        elif label == "Interface version":
            read["interface_version"] = _listed_words(line, label)[0]
        elif label == "Schema version":
            read["envelope"]["schema_version"] = int(_listed_words(line, label)[0])
        elif label in ("Reserved keys", "Refusal keys"):
            key = "reserved_keys" if label == "Reserved keys" else "error_keys"
            read["envelope"][key] = _listed_words(line, label)
        elif label in labels:
            read[labels[label]] = _listed_words(line, label)
        elif label == "Command id":
            operation["command_id"] = _listed_words(line, label)[0]
        elif label == "Description":
            operation["description"] = line[len("Description: "):]
        elif label == "Exit codes" and operation is not None:
            operation["exit_codes"] = [int(code) for code in _listed_words(line, label)]
        elif label == "Refusal tokens":
            operation["refusal_tokens"] = _listed_words(line, label)
        elif label == "Answer keys":
            read["answers"][operation["command_id"]] = _listed_words(line, label)
            read["answer_trees"][operation["command_id"]] = {}
        elif label == "Keys" and place == "Digest":
            read["digest"] = {key: {} for key in _listed_words(line, label)}
        elif line.startswith(("- ", "  ")):
            bullets.append(line)
        elif line.startswith("| `") and place == "Exit codes of every command":
            code, name, meaning = _table_cells(line)
            read["exit_codes"].append({"code": int(code.strip("`")), "name": name.strip("`"),
                                       "meaning": meaning})
        elif line.startswith("| `") and operation is not None:
            name, option, required, takes_value, repeatable, help_text = _table_cells(line)
            operation["arguments"].append({
                "name": name.strip("`"), "help": help_text, "option": option == "yes",
                "required": required == "yes", "takes_value": takes_value == "yes",
                "repeatable": repeatable == "yes"})
    return read


def _flat_text(text: str) -> str:
    return " ".join(text.split())


def test_the_pages_generated_section_is_the_interface_rendered():
    assert _page_section() == render_client_interface_markdown(build_client_interface()), (
        f"{CLIENT_INTERFACE_PAGE_PATH} differs from the interface; regenerate it with "
        f"{_REGENERATE_PAGE}")


def test_the_pages_generated_section_reads_back_as_the_interface():
    """Every name, word, number and tree of the interface can be read back from the page, so the
    page names nothing the code does not return and leaves out nothing it does."""
    interface = json.loads(json.dumps(build_client_interface()))
    for row in interface["exit_codes"]:
        row["meaning"] = _flat_text(row["meaning"])
    for operation in interface["operations"]:
        operation["description"] = _flat_text(operation["description"])
        for argument in operation["arguments"]:
            argument["help"] = _flat_text(argument["help"])
    interface["answer_trees"] = {command_id: {key: tree for key, tree in trees.items() if tree != {}}
                                 for command_id, trees in interface["answer_trees"].items()}
    assert _read_page_section(_page_section()) == interface


def test_the_writer_replaces_only_the_generated_section(tmp_path):
    page = tmp_path / CLIENT_INTERFACE_PAGE_PATH
    page.parent.mkdir(parents=True)
    before, after = "# Written by hand\n\nThe walk.\n\n", "\nAfter the section.\n"
    page.write_text(f"{before}{CLIENT_INTERFACE_PAGE_BEGIN}\nstale\n{CLIENT_INTERFACE_PAGE_END}\n{after}",
                    encoding="utf-8")
    assert write_client_interface_page(tmp_path) == page
    assert page.read_text(encoding="utf-8") == (
        before + render_client_interface_markdown(build_client_interface()) + after)


# F295's gate test, the one client written down, against the interface (R-1179, R-1180).

#: The sha256 of `tests/cli/test_machine_client_contract.py`, F295's gate test, as F295 accepted it
#: and as F298 keeps it (R-1179). A change to that file is deliberate: it updates this digest in the
#: same commit and its DECISION says why.
F295_GATE_TEST_SHA256 = "e6f4d57bc3c0b81e85d4c6cf145f89fca2c64c89ace4558c329b8d5487eb304f"


def test_f295s_gate_test_is_unchanged():
    gate_test = _REPO_ROOT / "tests" / "cli" / "test_machine_client_contract.py"
    assert hashlib.sha256(gate_test.read_bytes()).hexdigest() == F295_GATE_TEST_SHA256, (
        "F295's gate test changed; a deliberate change updates F295_GATE_TEST_SHA256 with it")


def test_every_command_and_flag_the_gate_test_drives_is_in_the_interface():
    """R-1180: a command a client drives that the interface leaves out, or a flag it passes that no
    operation it drives declares, fails here; a group alone runs its default command."""
    operations = {op["command"]: op for op in build_client_interface()["operations"]}
    used = _gate_names()
    driven = set()
    for command in used["commands"]:
        words = command.split()
        driven.add(" ".join(words if len(words) > 2 else [*words, _DEFAULT_COMMAND[words[1]]]))
    assert sorted(driven - set(operations)) == [], "the gate test drives a command the interface lacks"
    declared = {arg["name"] for command in driven for arg in operations[command]["arguments"]}
    assert used["flags"] and sorted(used["flags"] - declared) == [], (
        "the gate test passes a flag no operation it drives declares")

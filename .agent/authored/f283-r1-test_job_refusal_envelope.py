"""F283 T001 slice A — `job`'s refusals answer a machine in the envelope.

F277 landed `fail()` and migrated nine command groups onto it; `job` was not one of
them, so every refusal it raised under ``--json`` printed a prose line to stderr and
left stdout empty — a parser waiting for an object got nothing at all.

This slice migrates the twenty refusal sites of `apps/cli/commands/job.py` whose
handler ALREADY carries `json_output`, so nothing is threaded and no caller changes.
The twenty that remain sit in handlers with no flag in scope; threading it is its own
round, and the guard below counts them so the split cannot be lost.
"""

from __future__ import annotations

import ast
import contextlib
import io
import json
import pathlib

import pytest

_JOB_PY = pathlib.Path(__file__).resolve().parents[2] / "apps" / "cli" / "commands" / "job.py"


def _refusal_sites() -> tuple[list[int], list[int]]:
    """Partition job.py's `print(..., file=sys.stderr)` + `sys.exit(n)` pairs.

    Returns (sites whose handler has `json_output` in scope, sites without it).
    Reading the code is the point: a prose claim about how many sites were migrated
    is exactly the claim that goes stale, and this reads the tree instead.
    """
    tree = ast.parse(_JOB_PY.read_text())
    parent: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[child] = node

    def enclosing_def(node: ast.AST):
        cur = node
        while cur in parent:
            cur = parent[cur]
            if isinstance(cur, ast.FunctionDef | ast.AsyncFunctionDef):
                return cur
        return None

    flagged: list[int] = []
    unflagged: list[int] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
            continue
        func = node.value.func
        if not (
            isinstance(func, ast.Attribute)
            and func.attr == "exit"
            and isinstance(func.value, ast.Name)
            and func.value.id == "sys"
        ):
            continue

        body = None
        cur: ast.AST = node
        while cur in parent:
            cur = parent[cur]
            for field in ("body", "orelse", "finalbody"):
                seq = getattr(cur, field, None)
                if isinstance(seq, list) and node in seq:
                    body = seq
                    break
            if body is not None:
                break
        assert body is not None
        index = body.index(node)
        prev = body[index - 1] if index > 0 else None
        is_stderr_print = (
            isinstance(prev, ast.Expr)
            and isinstance(prev.value, ast.Call)
            and isinstance(prev.value.func, ast.Name)
            and prev.value.func.id == "print"
            and any(kw.arg == "file" for kw in prev.value.keywords)
        )
        if not is_stderr_print:
            continue

        fn = enclosing_def(node)
        assert fn is not None
        args = [a.arg for a in fn.args.args] + [a.arg for a in fn.args.kwonlyargs]
        (flagged if "json_output" in args else unflagged).append(node.lineno)
    return flagged, unflagged


class TestTheFlaggedRefusalsAreAllMigrated:
    def test_no_flagged_print_then_exit_pair_survives(self):
        flagged, _ = _refusal_sites()
        assert flagged == [], (
            "these job.py refusals have `json_output` in scope and still print prose: "
            f"lines {flagged}"
        )

    def test_the_unflagged_sites_are_counted_not_forgotten(self):
        """The rest of T001. When the flag is threaded this number falls; it never rises."""
        _, unflagged = _refusal_sites()
        assert len(unflagged) == 20, (
            f"expected the 20 sites whose handler has no json flag, found {len(unflagged)} "
            f"at lines {unflagged}"
        )

    def test_the_module_calls_the_shared_helper(self):
        assert "from apps.cli.json_envelope import fail" in _JOB_PY.read_text()


def _invoke(fn, **kwargs) -> tuple[int | None, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code: int | None = None
    with pytest.raises(SystemExit) as exc:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            fn(**kwargs)
    code = exc.value.code
    return code, out.getvalue(), err.getvalue()


class TestARefusalIsAnEnvelopeUnderJson:
    def test_an_unknown_sort_field_names_the_condition(self):
        from apps.cli.commands.job import _cmd_list_jobs

        code, out, err = _invoke(_cmd_list_jobs, sort="not-a-field", json_output=True)
        assert code == 1
        assert err == ""
        body = json.loads(out)
        assert body["schema_version"] == 1
        assert body["ok"] is False
        assert body["error"] == "invalid_list_option"
        assert "not-a-field" in body["message"]

    def test_an_unknown_job_names_the_condition(self):
        from apps.cli.commands.job import _cmd_job_budget_set

        code, out, err = _invoke(
            _cmd_job_budget_set,
            job_id="zzzznotajob",
            field_name="max_loops",
            raw_value="5",
            json_output=True,
        )
        assert code == 1
        assert err == ""
        body = json.loads(out)
        assert body["error"] == "job_not_found"
        assert body["ok"] is False

    def test_the_exit_code_a_site_already_used_is_preserved(self):
        """`job run --cycles -3` exited 2 before this slice and exits 2 after it."""
        from apps.cli.commands.job import _cmd_job_run_cycles

        code, out, err = _invoke(
            _cmd_job_run_cycles, job_id_str="zzzznotajob", cycles=-3, json_output=True
        )
        assert code == 2
        assert err == ""
        body = json.loads(out)
        assert body["error"] == "invalid_argument"
        assert "-3" in body["message"]


class TestWithoutJsonTheOperatorSeesTheSameBytes:
    def test_the_prose_line_is_unchanged(self):
        from apps.cli.commands.job import _cmd_job_budget_set

        code, out, err = _invoke(
            _cmd_job_budget_set,
            job_id="zzzznotajob",
            field_name="max_loops",
            raw_value="5",
            json_output=False,
        )
        assert code == 1
        assert out == ""
        assert err == "Error: No job matches 'zzzznotajob'. Try: remedy job list.\n"

    def test_the_rejected_plan_sentence_keeps_its_prefix_for_the_unmigrated_sites(self):
        """`_plan_rejected_error` still writes `Error: ` for the sites still on print()."""
        from apps.cli.commands.job import _plan_rejected_error, _plan_rejected_message

        job_id = "0123456789abcdef"
        assert _plan_rejected_error(job_id) == "Error: " + _plan_rejected_message(job_id)
        assert not _plan_rejected_message(job_id).startswith("Error: ")

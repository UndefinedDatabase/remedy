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

#: R-1020's remainder at F283 round 4's C3, measured at `3b4acafd` by an alias-aware
#: reading (DECISION F283 D1's correction — `decision.py` also binds the resolver as
#: `_rji`). Falls as each commit below migrates a module; never rises.
_EXITING_RESOLVER_REMAINING = {
    "change.py": 3,
    "contract_cmd.py": 1,
    "decision.py": 4,
    "job_context_cmd.py": 1,
    "project.py": 1,
    "teacher_cmd.py": 2,
}


def _exiting_resolver_calls(source: str) -> int:
    """Every call ``source`` reaches ``resolve_job_id`` through, alias-aware.

    Collects the names a ``from packages.orchestration.data_paths import
    resolve_job_id`` (or ``... as <alias>``) binds, at module level or inside a
    function ANYWHERE in the tree, then counts the ``ast.Call`` nodes whose callee is
    one of those names, OR an attribute access whose final segment is
    ``resolve_job_id`` (``data_paths.resolve_job_id``, an ``__import__`` expression,
    any base at all) — so a call that dodges the alias set by reaching through the
    module object still counts. Round 3's guard matched only the bare name
    ``resolve_job_id`` and missed `decision.py`'s `_rji` alias; this is the repair.
    """
    tree = ast.parse(source)
    aliases: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ImportFrom)
            and node.module == "packages.orchestration.data_paths"
        ):
            for alias in node.names:
                if alias.name == "resolve_job_id":
                    aliases.add(alias.asname or alias.name)

    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in aliases:
            count += 1
        elif isinstance(func, ast.Attribute) and func.attr == "resolve_job_id":
            count += 1
    return count


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
        """The rest of T001. When the flag is threaded this number falls; it never rises.

        20 at the slice-A round; 8 once slice B threaded `_cmd_show_job`,
        `_cmd_create_job`, `_cmd_plan_job_local` and `_refuse_budget_set`. The eight left
        are all in `_cmd_run_next_task_local`, which ten tests monkeypatch with a
        single-positional lambda — threading it moves those tests too, so it is its own
        round.
        """
        _, unflagged = _refusal_sites()
        assert len(unflagged) == 8, (
            f"expected the 8 sites whose handler has no json flag, found {len(unflagged)} "
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

    def test_a_threaded_command_answers_a_bad_id_in_the_envelope(self):
        """R-1020 repaired FOR THIS COMMAND; the finding stays open for the rest.

        `job.show` declares `supports_json: True`. Its handler takes `json_output`, and
        as of F283 round 3 it resolves the id through
        `apps.cli.job_id_arg.resolve_job_id_or_fail`, which catches what `lookup_job_id`
        raises instead of letting `resolve_job_id` print prose and exit above it. This
        test carried a `strict` xfail for exactly one round; the mark was deleted in the
        commit that turned it green.

        R-1020 is NOT resolved by that. `resolve_job_id` keeps 17 call sites in eight
        other command modules — `change`, `contract_cmd`, `decision`, `job_context_cmd`,
        `job_stop_cmd`, `patch`, `project`, `teacher_cmd` — and every `supports_json`
        command reached through one of them still answers a bad id in prose. The guard
        below counts them so the remainder cannot be forgotten.
        """
        from apps.cli.commands.job import _cmd_show_job

        code, out, err = _invoke(_cmd_show_job, job_id_str="zzzznotajob", json_output=True)
        assert code == 1
        assert err == ""
        body = json.loads(out)
        assert body["error"] == "invalid_job_id"

    def test_the_rejected_plan_sentence_keeps_its_prefix_for_the_unmigrated_sites(self):
        """`_plan_rejected_error` still writes `Error: ` for the sites still on print()."""
        from apps.cli.commands.job import _plan_rejected_error, _plan_rejected_message

        job_id = "0123456789abcdef"
        assert _plan_rejected_error(job_id) == "Error: " + _plan_rejected_message(job_id)
        assert not _plan_rejected_message(job_id).startswith("Error: ")


class TestTheExitingResolverIsStillReachable:
    """R-1020's remainder, counted rather than remembered.

    `resolve_job_id` prints a prose refusal and exits. Every call site of it is a
    `supports_json` command that cannot answer a machine. `_EXITING_RESOLVER_REMAINING`
    falls as the sweep reaches each module; it never grows.
    """

    def test_a_binding_inside_a_function_is_still_counted(self):
        source = (
            "def f():\n"
            "    from packages.orchestration.data_paths import resolve_job_id as _x\n"
            "    return _x('a')\n"
        )
        assert _exiting_resolver_calls(source) == 1

    def test_an_attribute_call_is_counted_even_without_an_alias(self):
        """The round 3 mutation the guard missed: reaching the resolver through the
        module object rather than a bare name."""
        source = (
            "def f():\n"
            "    return data_paths.resolve_job_id('a')\n"
        )
        assert _exiting_resolver_calls(source) == 1

    def test_the_remaining_call_sites_match_the_measured_dict(self):
        root = pathlib.Path(__file__).resolve().parents[2] / "apps" / "cli"
        found: dict[str, int] = {}
        for path in sorted(root.rglob("*.py")):
            n = _exiting_resolver_calls(path.read_text())
            if n:
                found[path.name] = n
        assert "job.py" not in found
        assert "job_id_arg.py" not in found
        assert found == _EXITING_RESOLVER_REMAINING, (
            f"measured {found}, constant says {_EXITING_RESOLVER_REMAINING}"
        )


class TestTheAmbiguousBranchAnswersInTheEnvelope:
    """R-1020's coverage gap, closed. Round 3 landed `resolve_job_id_or_fail`'s ambiguous
    exit with no test reaching it; this proves its exit code, its token and its `matches`
    payload, and proves the text branch byte-identical to the exiting resolver's — computed
    against the real function, not typed by hand."""

    @staticmethod
    def _two_ambiguous_jobs(monkeypatch, tmp_path) -> list[str]:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        jobs_path = tmp_path / "jobs"
        ids = [
            "aaaa1111-0000-0000-0000-000000000001",
            "aaaa1111-0000-0000-0000-000000000002",
        ]
        for job_id in ids:
            record_dir = jobs_path / job_id
            record_dir.mkdir(parents=True, exist_ok=True)
            (record_dir / "job.json").write_text(json.dumps({"job_id": job_id}))
        return sorted(ids)

    def test_json_output_carries_the_matches_and_leaves_stderr_empty(
        self, monkeypatch, tmp_path
    ):
        from apps.cli.job_id_arg import resolve_job_id_or_fail

        matches = self._two_ambiguous_jobs(monkeypatch, tmp_path)
        code, out, err = _invoke(resolve_job_id_or_fail, raw="aaaa1111", json_output=True)
        assert code == 2
        assert err == ""
        body = json.loads(out)
        assert body["ok"] is False
        assert body["schema_version"] == 1
        assert body["error"] == "ambiguous_job_id"
        assert body["matches"] == matches

    def test_without_json_stderr_matches_the_exiting_resolver_byte_for_byte(
        self, monkeypatch, tmp_path
    ):
        from apps.cli.job_id_arg import resolve_job_id_or_fail
        from packages.orchestration.data_paths import resolve_job_id

        self._two_ambiguous_jobs(monkeypatch, tmp_path)
        code, out, err = _invoke(resolve_job_id_or_fail, raw="aaaa1111", json_output=False)
        assert code == 2
        assert out == ""
        _, _, reference_err = _invoke(resolve_job_id, raw="aaaa1111")
        assert err == reference_err

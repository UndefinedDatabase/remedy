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

#: R-1020's remainder, measured at `3b4acafd` by an alias-aware reading (the alias
#: correction — `decision.py` also binds the resolver as `_rji` — is recorded in the
#: `Gate: F283 R3` entry of `.agent/live_review.md`) and driven to EMPTY by F283 round
#: 4: no module under `apps/cli/` calls the exiting resolver.
_EXITING_RESOLVER_REMAINING: dict[str, int] = {}

#: R-1021's own remainder: every `lookup_job_id` call site under `apps/cli/`, falling
#: to `job_id_arg.py` and `job_stop_cmd.py` alone once the sweep is done — the two
#: callers that handle `JobIdAmbiguous` themselves and so keep talking to
#: `lookup_job_id` directly instead of through `resolve_job_id_or_fail`. Measured at
#: `63141657`.
_LOOKUP_CALLERS: dict[str, int] = {
    "job_id_arg.py": 1,
    "job_stop_cmd.py": 1,
}


def _lookup_calls(source: str) -> int:
    """Every call ``source`` makes to ``lookup_job_id``, by bare name or attribute.

    Counts an ``ast.Call`` node whose callee is the name ``lookup_job_id`` OR an
    attribute access whose final segment is ``lookup_job_id`` (``mod.lookup_job_id``),
    so a caller that reaches it through a module object still counts.
    """
    tree = ast.parse(source)
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == "lookup_job_id":
            count += 1
        elif isinstance(func, ast.Attribute) and func.attr == "lookup_job_id":
            count += 1
    return count


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


def _refusal_sites(filename: str = "job.py") -> tuple[list[int], list[int]]:
    """Partition a command module's `print(..., file=sys.stderr)` + `sys.exit(n)` pairs.

    Returns (sites whose handler has `json_output` in scope, sites without it).
    Reading the code is the point: a prose claim about how many sites were migrated
    is exactly the claim that goes stale, and this reads the tree instead. Defaults to
    `job.py`, so its existing callers do not change.
    """
    path = _JOB_PY.parent / filename
    tree = ast.parse(path.read_text())
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


def _raise_systemexit_lines(filename: str) -> list[int]:
    """Every `raise SystemExit(...)` line in a command module, AST-read.

    `stats_ledger_cmd.py`, `bench_cmd.py`, `failure_stats_cmd.py` and
    `job_stop_cmd.py` refuse with a `raise SystemExit(n)` statement rather than
    a `sys.exit(n)` expression, so `_refusal_sites` (which matches only the
    latter, `job.py`'s own shape) never sees them; this is the same reading for
    the `raise` form.
    """
    path = _JOB_PY.parent / filename
    tree = ast.parse(path.read_text())
    lines: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Raise):
            continue
        exc = node.exc
        if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == "SystemExit":
            lines.append(node.lineno)
    return lines


class TestStatsRefusalsAreAllMigrated:
    """F283 round 11 C3 — `stats_ledger_cmd.py`, `bench_cmd.py` and
    `failure_stats_cmd.py`'s refusals move onto `fail()`, the exiting helpers
    (`_validate_by`, `_validate_period_bound`, `_one_project_ledger`,
    `_require_evidence_dir`, `_validate_multiplier`, `_one_project_history`,
    `_validate_since`) taking a REQUIRED `json_output` every caller now passes.
    `stats_ledger_cmd.py::_cmd_stats_verify_ledger`'s `raise SystemExit(EXIT_DRIFT)`
    is a RESULT, not a refusal (this round's block, restating DECISIONs F277
    D7-D9), and is the one survivor this ratchet allows. Round 11 C4 extends this
    class to `job_stop_cmd.py`: `_unknown_job`, the `validate_job_id` refusal,
    `job_not_stoppable` and `stop_not_requested` move the same way, and no
    `raise SystemExit` is left in that module at all."""

    _MODULES = ("stats_ledger_cmd.py", "bench_cmd.py", "failure_stats_cmd.py",
                "job_stop_cmd.py")

    def test_no_mechanical_print_then_exit_pair_survives(self):
        for filename in self._MODULES:
            flagged, unflagged = _refusal_sites(filename)
            assert flagged == [] and unflagged == [], (
                f"expected no print-then-exit pair left in {filename}, found "
                f"flagged={flagged} unflagged={unflagged}"
            )

    def test_stats_ledger_keeps_only_the_verify_ledger_drift_exit(self):
        lines = _raise_systemexit_lines("stats_ledger_cmd.py")
        assert len(lines) == 1, (
            f"expected exactly one raise SystemExit left in stats_ledger_cmd.py, "
            f"found {lines}"
        )
        source = (_JOB_PY.parent / "stats_ledger_cmd.py").read_text()
        assert "EXIT_DRIFT" in source.splitlines()[lines[0] - 1]

    def test_bench_and_failure_stats_have_no_raise_systemexit_left(self):
        assert _raise_systemexit_lines("bench_cmd.py") == []
        assert _raise_systemexit_lines("failure_stats_cmd.py") == []

    def test_job_stop_has_no_raise_systemexit_left(self):
        assert _raise_systemexit_lines("job_stop_cmd.py") == []


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
        `_cmd_create_job`, `_cmd_plan_job_local` and `_refuse_budget_set`; 0 once round 6
        threaded `_cmd_run_next_task_local` and moved its eight mechanical pairs onto
        `fail()`, updating the ten tests that monkeypatched it with a single-positional
        lambda in the same commit. The verification-failure loop at the end of that
        function prints more than one line before its exit, so it was never mechanical
        and is not counted here.
        """
        _, unflagged = _refusal_sites()
        assert unflagged == [], (
            f"expected no sites left whose handler has no json flag, found {unflagged}"
        )

    def test_the_module_calls_the_shared_helper(self):
        """`fail` is imported from `apps.cli.json_envelope` — alone or, as of F283 round
        8's `emit_ok` (DECISION F283 D3 part (a)), alongside another name on the same
        line. Read with `ast` rather than a literal substring, so a second import on
        that line does not make this check stale (finding, this round's own sweep)."""
        tree = ast.parse(_JOB_PY.read_text())
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "apps.cli.json_envelope"
            for alias in node.names
        }
        assert "fail" in imported


class TestDecisionsRefusalsAreAllMigrated:
    """F283 round 6 — `decision.py`'s refusal pairs move onto `fail()` under DECISION
    F277 D8's one-token-per-condition rule. F283 R15 C4 (DECISION F283 D9) gives
    `_cmd_decision_resolve` a `json_output` flag and reshapes the derived-decision
    refusal near the end of the handler onto `if json_output: fail(...) else: <the two
    prints>` followed by one shared `sys.exit(1)` — the `sys.exit(1)` no longer sits
    directly after a `print(..., file=sys.stderr)` in the same body (an `if`/`else`
    statement sits between them instead), so this ratchet's AST rule no longer counts
    it as a site at all: no flagged and no unflagged site is left."""

    def test_no_flagged_print_then_exit_pair_survives(self):
        flagged, _ = _refusal_sites("decision.py")
        assert flagged == [], (
            "these decision.py refusals have `json_output` in scope and still print "
            f"prose: lines {flagged}"
        )

    def test_exactly_one_unflagged_site_remains(self):
        _, unflagged = _refusal_sites("decision.py")
        assert unflagged == [], (
            f"expected no sites left whose handler has no json flag, found {unflagged}"
        )


class TestBrainRefusalsAreAllMigrated:
    """F283 round 7 — every one of `brain.py`'s 13 mechanical print-then-exit pairs is
    `Error: `-prefixed with a single print before its exit, so the migration rule
    excludes none of them: no flagged and no unflagged site is left."""

    def test_no_flagged_print_then_exit_pair_survives(self):
        flagged, _ = _refusal_sites("brain.py")
        assert flagged == [], (
            "these brain.py refusals have `json_output` in scope and still print "
            f"prose: lines {flagged}"
        )

    def test_no_unflagged_print_then_exit_pair_survives(self):
        _, unflagged = _refusal_sites("brain.py")
        assert unflagged == [], (
            f"expected no sites left whose handler has no json flag, found {unflagged}"
        )


class TestPatchRefusalsAreAllMigrated:
    """F283 round 7 — `patch.py`'s refusal pairs move onto `fail()`. Two sites print MORE
    THAN ONE line before their exit, so the migration rule excludes both and they stay:
    `_cmd_show_patch_intent`'s intent-not-found message (its handler carried no
    `json_output`, so it counted as the one unflagged site) and
    `_cmd_revert_patch_intent`'s revert-blocked message (its handler carries
    `json_output`, so it counts as the one flagged site). Round 12 migrates
    `_cmd_revert_patch_intent`'s three BRANCHED sites (`ambiguous_intent_id`,
    `no_apply_record`, `no_target_repo`) onto `fail()` too, but none of the three was
    ever a mechanical `print`-then-`sys.exit` PAIR by this ratchet's own AST rule — the
    `print` sat inside an `if`/`else`, never directly before the `sys.exit` — so this
    class's two counts are unchanged by that round. F283 R14 C5 (DECISION F283 D9)
    migrates the show-intent pair too — its two `print(..., file=sys.stderr)` lines
    become ONE `fail("patch_intent_not_found", ...)` call, so no unflagged site is
    left at all; the flagged revert-blocked site is untouched by that round."""

    def test_exactly_one_flagged_site_remains(self):
        flagged, _ = _refusal_sites("patch.py")
        assert len(flagged) == 1, (
            f"expected exactly the one revert-blocked multi-print site left unmigrated, "
            f"found {len(flagged)} at lines {flagged}"
        )

    def test_no_unflagged_site_remains(self):
        _, unflagged = _refusal_sites("patch.py")
        assert unflagged == [], (
            f"expected the show-intent multi-print site to be migrated onto fail(), "
            f"found unflagged sites at lines {unflagged}"
        )


class TestDoRefusalsAreAllMigrated:
    """F283 round 8 — 14 of `do_cmd.py`'s 18 mechanical print-then-exit pairs (11 whose
    handler carried `json_output`, 3 in `_validate_role_override`, which carries none)
    move onto `fail()`. F283 round 9 migrates the three round 8 correctly declined —
    `_cmd_do`'s no-such-contract-template site (token `unsupported_contract_template`),
    `_cmd_run_show`'s no-such-run site (token `run_not_found`) and `_cmd_run_list`'s
    invalid-sort-field site (reusing `invalid_list_option`) — repairing in the same
    commit the tests in `tests/cli/test_do_sequence_cli.py` and `tests/cli/test_cli_ux.py`
    that pinned their old `--json` shape (empty stdout, prose on stderr).

    F283 round 10 migrates the last one, `_cmd_do_order`'s `ctx.failed` site, by
    DECISION F283 D5: the `--json` branch now builds its result document and, on a
    failed walk, passes it as `fail()`'s own `**payload` — `fail("step_failed", ...,
    json_output=True, failed_step=last.name, **document)` — instead of printing the
    document and THEN a separate trailing print+exit, so there is only ever one
    envelope on stdout. The text branch's trailing line becomes
    `fail("step_failed", ..., json_output=False)`, byte-identical on stderr. The AST
    rule now sees a single `fail()` call at that site, not a print-then-exit pair, so
    no flagged site remains.

    `_refuse_before_any_step` prints one line per refusal sentence before its one
    `sys.exit(2)` — more than one print is possible — so it is not mechanical by the
    rule and stays too; `_refusal_sites` does not count it either, since its immediate
    predecessor statement is the `for` loop, not a `print` call."""

    def test_no_flagged_print_then_exit_pair_survives(self):
        flagged, _ = _refusal_sites("do_cmd.py")
        assert flagged == [], (
            f"expected no flagged sites left, found {len(flagged)} at lines {flagged}"
        )

    def test_no_unflagged_print_then_exit_pair_survives(self):
        _, unflagged = _refusal_sites("do_cmd.py")
        assert unflagged == [], (
            f"expected no sites left whose handler has no json flag, found {unflagged}"
        )


class TestProjectRefusalsAreAllMigrated:
    """F283 round 9 — 23 of `project.py`'s 25 mechanical print-then-exit pairs move onto
    `fail()`, the six uppercase `ERROR: ` sites among them migrated under DECISION F283
    D4 (they now read `Error: `). Two sites stay, one in each split, because their
    `print` carries no prefix at all (`print(str(exc), file=sys.stderr)`) and D4 reaches
    only a prefixed line: `_cmd_project_current`'s `(ProjectNotFoundError,
    InvalidProjectSelectorError)` branch (its handler carries `json_output`, so it is
    the one flagged site) and `_cmd_project_attach_repo`'s identical branch (its handler
    carries none, so it is the one unflagged site). Round 12 (DECISION F283 D7) gives
    `_cmd_project_current`'s branch an `if json_output:` guard whose `else` is the
    ORIGINAL two lines, byte for byte, so the print-then-exit pair this ratchet counts
    now sits one level deeper — still the SAME one flagged site, just behind the guard,
    answering `project_not_found` or `invalid_project_selector` under `--json` while the
    text branch is untouched. `_cmd_project_attach_repo`'s unflagged site is untouched by
    this round and stays as it was."""

    def test_exactly_one_flagged_site_remains(self):
        flagged, _ = _refusal_sites("project.py")
        assert len(flagged) == 1, (
            "expected exactly the one unprefixed ProjectNotFoundError/"
            f"InvalidProjectSelectorError site left unmigrated, found {len(flagged)} "
            f"at lines {flagged}"
        )

    def test_exactly_one_unflagged_site_remains(self):
        _, unflagged = _refusal_sites("project.py")
        assert len(unflagged) == 1, (
            "expected exactly the one unprefixed ProjectNotFoundError/"
            f"InvalidProjectSelectorError site left unmigrated, found {len(unflagged)} "
            f"at lines {unflagged}"
        )

    def test_the_module_calls_the_shared_helper(self):
        path = pathlib.Path(__file__).resolve().parents[2] / "apps" / "cli" / "commands" / "project.py"
        tree = ast.parse(path.read_text())
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "apps.cli.json_envelope"
            for alias in node.names
        }
        assert "fail" in imported


class TestGroupedRefusalsAreAllMigrated:
    """F283 round 10 — every parse-level refusal in `apps/cli/grouped.py::main` asks
    `_wants_json(raw)` and answers in the envelope when it holds (DECISION F283 D6):
    the conflicting-options pair, the unknown-group and unknown-subcommand pairs, the
    unrecognized-arguments pair, the usage error on a known subcommand, and the two
    post-parse pairs (`unknown_command` when no command id was resolved, `no_handler`
    when the dispatch table has none), the last two now calling `fail()` directly. No
    `print(..., file=sys.stderr)` + `sys.exit(n)` pair whose immediate predecessor
    statement is the print itself survives in the module: the ones the AST rule could
    once see are gone, and `_usage_refusal`'s own text-mode print sits inside an
    `if`/`else`, never directly before its `sys.exit`, so it was never mechanical by
    the rule's own definition."""

    def test_no_pair_survives(self):
        flagged, unflagged = _refusal_sites("../grouped.py")
        assert flagged == [] and unflagged == [], (
            f"expected no print-then-exit pair left in grouped.py, found "
            f"flagged={flagged} unflagged={unflagged}"
        )


class TestTestCmdsRefusalsAreAllMigrated:
    """F283 round 10 — `apps/cli/commands/test_cmds.py`'s three refusals move onto
    `fail()`: `_cmd_discover_commands`'s `except Exception` catch-all (reusing
    `job_store_error`, the token `job.py`'s own `require_job_plan` failure already
    uses for the identical condition) and its branched `no_target_repo` site, and
    `_cmd_test_status`'s branched `job_not_found` site, both migrated by the BRANCHED
    rule with their extra payload keys (`job_id` / `candidates`, `job_id`) kept.
    `_cmd_run_tests` stays — it prints a result document, T002's own shape, not a
    mechanical print-then-exit pair."""

    def test_no_pair_survives(self):
        flagged, unflagged = _refusal_sites("test_cmds.py")
        assert flagged == [] and unflagged == [], (
            f"expected no print-then-exit pair left in test_cmds.py, found "
            f"flagged={flagged} unflagged={unflagged}"
        )


class TestSnapshotCmdsRefusalsAreAllMigrated:
    """F283 round 12 — `snapshot_cmds.py`'s three refusals (two `job_not_found`
    branches and one `snapshot_not_found` branch) move onto `fail()`. Each was
    BRANCHED on `as_json` rather than a mechanical single-line print, so none was
    ever counted by `_refusal_sites` either; the ratchet below reads the module for
    no PAIR left at all, mechanical or branched, the same shape the other migrated
    modules pin."""

    def test_no_pair_survives(self):
        flagged, unflagged = _refusal_sites("snapshot_cmds.py")
        assert flagged == [] and unflagged == [], (
            f"expected no print-then-exit pair left in snapshot_cmds.py, found "
            f"flagged={flagged} unflagged={unflagged}"
        )

    def test_the_module_calls_the_shared_helper(self):
        path = _JOB_PY.parent / "snapshot_cmds.py"
        tree = ast.parse(path.read_text())
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "apps.cli.json_envelope"
            for alias in node.names
        }
        assert "fail" in imported


class TestRealTestExecutionRefusalsAreAllMigrated:
    """F283 round 12 — `real_test_execution_cmd.py`'s three refusals
    (`_cmd_test_result`'s `test_run_not_found`, `_cmd_test_list`'s reused
    `invalid_list_option`, `_cmd_snapshot_show`'s `snapshot_proof_not_found`) move
    onto `fail()` by the plain rule; each handler takes a single `args` parameter and
    reads its flag with `getattr(args, "json", False)`, so `_refusal_sites`'s
    `json_output`-in-scope test never applied here — all three sat in the unflagged
    list before this round and neither list holds anything now."""

    def test_no_pair_survives(self):
        flagged, unflagged = _refusal_sites("real_test_execution_cmd.py")
        assert flagged == [] and unflagged == [], (
            f"expected no print-then-exit pair left in real_test_execution_cmd.py, "
            f"found flagged={flagged} unflagged={unflagged}"
        )

    def test_the_module_calls_the_shared_helper(self):
        path = _JOB_PY.parent / "real_test_execution_cmd.py"
        tree = ast.parse(path.read_text())
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "apps.cli.json_envelope"
            for alias in node.names
        }
        assert "fail" in imported


class TestSelfCmdRefusalsAreAllMigrated:
    """F283 round 12 — `self_cmd.py`'s one refusal (`self propose --top`'s
    `invalid_argument`) moves onto `fail()` by the plain rule, exit 1 unchanged."""

    def test_no_pair_survives(self):
        flagged, unflagged = _refusal_sites("self_cmd.py")
        assert flagged == [] and unflagged == [], (
            f"expected no print-then-exit pair left in self_cmd.py, found "
            f"flagged={flagged} unflagged={unflagged}"
        )

    def test_the_module_calls_the_shared_helper(self):
        path = _JOB_PY.parent / "self_cmd.py"
        tree = ast.parse(path.read_text())
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "apps.cli.json_envelope"
            for alias in node.names
        }
        assert "fail" in imported


class TestRuntimeCmdRefusalsAreAllMigrated:
    """F283 round 13 (DECISION F283 D8) — `runtime_cmd.py`'s local `_fail` is deleted;
    every refusal now calls the module's own `_runtime_refusal`, which calls `fail()`
    with the token keyed on `error_class`. The four result-shaped failure exits D8
    names (the one-shot probe's cleanup survivors, its readiness failure, a served
    runtime's failed health check, and a `stop` that did not stop) each print their own
    message behind an `if json_output: ... else: ...` branch and only THEN reach
    `sys.exit`, so the `sys.exit`'s immediate predecessor statement is the `if`/`else`
    itself, never a bare `print(..., file=sys.stderr)` — none of the four was ever a
    mechanical pair by this ratchet's own AST rule, and none is now either. Both lists
    come back empty."""

    def test_no_fail_function_is_defined(self):
        path = _JOB_PY.parent / "runtime_cmd.py"
        tree = ast.parse(path.read_text())
        names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        assert "_fail" not in names

    def test_no_pair_survives(self):
        flagged, unflagged = _refusal_sites("runtime_cmd.py")
        assert flagged == [] and unflagged == [], (
            f"expected no print-then-exit pair left in runtime_cmd.py, found "
            f"flagged={flagged} unflagged={unflagged}"
        )

    def test_the_module_calls_the_shared_helper(self):
        path = _JOB_PY.parent / "runtime_cmd.py"
        tree = ast.parse(path.read_text())
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "apps.cli.json_envelope"
            for alias in node.names
        }
        assert "fail" in imported


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

    def test_the_rejected_plan_sentence_carries_no_error_prefix(self):
        """`_plan_rejected_message` is the one form now; `fail()` writes the prefix."""
        from apps.cli.commands.job import _plan_rejected_message

        job_id = "0123456789abcdef"
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


class TestLookupJobIdIsPinnedToItsTwoHandlers:
    """R-1021's sweep, counted rather than remembered. `_LOOKUP_CALLERS` falls as each
    hand-caught site moves onto `resolve_job_id_or_fail`; it never grows, and it falls
    to `job_id_arg.py` and `job_stop_cmd.py` alone — the two callers that handle
    `JobIdAmbiguous` themselves."""

    def test_an_attribute_call_in_a_source_string_counts(self):
        source = (
            "def f():\n"
            "    return mod.lookup_job_id('a')\n"
        )
        assert _lookup_calls(source) == 1

    def test_the_call_sites_match_the_measured_dict(self):
        root = pathlib.Path(__file__).resolve().parents[2] / "apps" / "cli"
        found: dict[str, int] = {}
        for path in sorted(root.rglob("*.py")):
            n = _lookup_calls(path.read_text())
            if n:
                found[path.name] = n
        assert found == _LOOKUP_CALLERS, (
            f"measured {found}, constant says {_LOOKUP_CALLERS}"
        )


class TestResolveJobIdOrFailForwardsAPayload:
    """R-1021's layer change: `resolve_job_id_or_fail` (and the `refuse_ambiguous_job_id`
    it calls) forward `**payload` to every `fail()` they make, so a caller that already
    carried its own envelope key — `snapshot_cmds.py` and
    `test_cmds.py::_cmd_test_status`, both of which print a `job_id` key today — keeps
    it after moving onto the shared resolver."""

    def test_the_not_found_branch_carries_the_extra_payload(self):
        from apps.cli.job_id_arg import resolve_job_id_or_fail

        code, out, err = _invoke(
            resolve_job_id_or_fail, raw="zzzznotajob", json_output=True, job_id="x"
        )
        assert code == 1
        assert err == ""
        body = json.loads(out)
        assert body["error"] == "invalid_job_id"
        assert body["job_id"] == "x"

    def test_the_ambiguous_branch_carries_the_extra_payload(self, monkeypatch, tmp_path):
        """Round 5's probe (d) found this path unproved: no test passed a payload on
        the ambiguous branch, so its forwarding was asserted nowhere. This is that
        test, over the same two-ambiguous-jobs fixture
        `TestTheAmbiguousBranchAnswersInTheEnvelope` uses."""
        from apps.cli.job_id_arg import resolve_job_id_or_fail

        matches = TestTheAmbiguousBranchAnswersInTheEnvelope._two_ambiguous_jobs(
            monkeypatch, tmp_path
        )
        code, out, err = _invoke(
            resolve_job_id_or_fail, raw="aaaa1111", json_output=True, job_id="x"
        )
        assert code == 2
        assert err == ""
        body = json.loads(out)
        assert body["error"] == "ambiguous_job_id"
        assert body["matches"] == matches
        assert body["job_id"] == "x"


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


class TestEveryMigratedJsonCommandAnswersABadIdInTheEnvelope:
    """C8 — the whole layer proved through the REAL parser, not the handler directly.

    Every command below now resolves its job id through
    `apps.cli.job_id_arg.resolve_job_id_or_fail` (round 3 for `job.*`, round 4 for the
    rest). `zzzznotajob` is neither a UUID nor a short hex prefix, so it fails
    `lookup_job_id`'s shape check before any command-specific logic runs — the SAME
    refusal, `invalid_job_id` at exit 1, for every command here except `job.stop`,
    whose bespoke handling in `job_stop_cmd.py` answers `job_not_found` at exit 3
    (C3's SPEC). A command whose refusal fires before it reaches the resolver would be
    left out of this table and named in its round's handback; in round 4, none was.
    """

    #: command_id -> the positional args after group/subcommand, read off the catalog
    #: entry (`apps.cli.command_catalog.CATALOG`) for each command's own required
    #: positionals. `teacher.ask` takes its job id through `--job-id`, an option, not
    #: a positional — so its "placeholder" is the required `question` positional and
    #: the job id is passed as the option explicitly.
    _ARGV_TAIL: dict[str, list[str]] = {
        "change.list": ["zzzznotajob"],
        "change.show": ["zzzznotajob", "intent-placeholder"],
        "change.proof": ["zzzznotajob"],
        "decision.list": ["zzzznotajob"],
        "decision.show": ["zzzznotajob", "decision-placeholder"],
        "job.contract": ["zzzznotajob"],
        "job.context": ["zzzznotajob"],
        "job.stop": ["zzzznotajob"],
        "patch.list": ["zzzznotajob"],
        "patch.apply": ["zzzznotajob", "intent-placeholder"],
        "patch.revert": ["zzzznotajob", "intent-placeholder"],
        "patch.approve-hunks": ["zzzznotajob"],
        "teacher.narrate": ["zzzznotajob"],
        "teacher.ask": ["question-placeholder", "--job-id", "zzzznotajob"],
    }

    @pytest.mark.parametrize("command_id", sorted(_ARGV_TAIL))
    def test_a_bad_job_id_answers_in_the_envelope(self, command_id, monkeypatch, tmp_path):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.grouped import main

        entry = next(c for c in CATALOG if c.command_id == command_id)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        argv = [entry.group_id, entry.subcommand, *self._ARGV_TAIL[command_id], "--json"]

        out, err = io.StringIO(), io.StringIO()
        with pytest.raises(SystemExit) as caught:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                main(argv)

        assert err.getvalue() == ""
        body = json.loads(out.getvalue())
        assert body["ok"] is False
        assert body["schema_version"] == 1
        if command_id == "job.stop":
            assert caught.value.code == 3
            assert body["error"] == "job_not_found"
        else:
            assert caught.value.code == 1
            assert body["error"] == "invalid_job_id"


class TestAPrefixTwoJobsShareIsRefusedAsAmbiguousThroughTheParser:
    """C8 — R-1021 proved through the REAL parser, not the handler directly.

    Every migrated site (rounds 4 and 5) now resolves its job id through
    `apps.cli.job_id_arg.resolve_job_id_or_fail`, so a prefix two jobs share raises
    `JobIdAmbiguous` there and answers `ambiguous_job_id` at exit 2 — instead of the
    false `invalid_job_id`/"no job matches" R-1021 named — for every one of these
    commands.

    `event.replay` is deliberately NOT in either table below: `_cmd_event_replay`
    (`apps/cli/commands/event.py`) hands `job_id_str` straight to
    `packages.orchestration.event_replay.replay_job`, which never calls
    `lookup_job_id` — it loads whatever run-log events exist for that literal string
    and returns a degraded `JobReplayState` rather than failing. An ambiguous prefix
    therefore never reaches the resolver on this command's argv, so it is left out
    rather than forced or skipped (measured by reading `event.py` and
    `packages/orchestration/event_replay.py`).
    """

    #: command_id -> the catalog entry's own positionals plus required options, read
    #: off `apps.cli.command_catalog.CATALOG` — never typed by hand.
    _JSON_COMMAND_IDS: tuple[str, ...] = (
        "brain.graph", "brain.node", "brain.context", "brain.continue",
        "event.list", "event.show", "event.timeline",
        "file.why", "memory.learn",
        "snapshot.inspect", "snapshot.list-applies",
        "test.discover", "test.status",
    )
    #: command_id -> the same, for the five commands with no `--json` at all.
    _TEXT_COMMAND_IDS: tuple[str, ...] = (
        "brain.view", "brain.trust", "brain.timeline", "brain.cockpit",
        "brain.constitution",
    )

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

    @staticmethod
    def _argv_tail(entry) -> list[str]:
        """`aaaa1111` for the job id, a name-derived placeholder for every other
        required positional, and `--flag value` for every required option — all read
        off the catalog entry rather than hand-typed per command."""
        tail: list[str] = []
        for arg in entry.args:
            if arg.is_option:
                continue
            tail.append("aaaa1111" if arg.name == "job_id" else f"{arg.name}-placeholder")
        for arg in entry.args:
            if arg.is_option and arg.required:
                tail.extend([arg.name, f"{arg.name.lstrip('-')}-placeholder"])
        return tail

    @pytest.mark.parametrize("command_id", _JSON_COMMAND_IDS)
    def test_a_json_command_answers_ambiguous_in_the_envelope(
        self, command_id, monkeypatch, tmp_path
    ):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.grouped import main

        matches = self._two_ambiguous_jobs(monkeypatch, tmp_path)
        entry = next(c for c in CATALOG if c.command_id == command_id)
        argv = [entry.group_id, entry.subcommand, *self._argv_tail(entry), "--json"]

        out, err = io.StringIO(), io.StringIO()
        with pytest.raises(SystemExit) as caught:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                main(argv)

        assert caught.value.code == 2
        assert err.getvalue() == ""
        body = json.loads(out.getvalue())
        assert body["ok"] is False
        assert body["error"] == "ambiguous_job_id"
        assert body["matches"] == matches

    @pytest.mark.parametrize("command_id", _TEXT_COMMAND_IDS)
    def test_a_text_command_matches_the_exiting_resolvers_stderr(
        self, command_id, monkeypatch, tmp_path
    ):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.grouped import main
        from packages.orchestration.data_paths import resolve_job_id

        self._two_ambiguous_jobs(monkeypatch, tmp_path)
        entry = next(c for c in CATALOG if c.command_id == command_id)
        argv = [entry.group_id, entry.subcommand, *self._argv_tail(entry)]

        out, err = io.StringIO(), io.StringIO()
        with pytest.raises(SystemExit) as caught:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                main(argv)

        assert caught.value.code == 2
        assert out.getvalue() == ""

        _, _, reference_err = _invoke(resolve_job_id, raw="aaaa1111")
        assert err.getvalue() == reference_err


class TestRound10sUntestedRefusalsNowPinned:
    """F283 round 10 migrated these two lines onto `fail()` but the round's own
    probe found both unpinned: renaming either token left the whole 561-test
    selection green. Round 11 closes both gaps.

    Both refusals sit BEHIND `resolve_job_id_or_fail`, so each test's job id is a
    fresh, full UUID: `lookup_job_id` returns it without touching disk (it is
    already a valid UUID string), which is the resolver "accepting" it, while the
    job store genuinely holds no such job — the shape C5's block orders.
    """

    def test_test_status_job_not_found_answers_in_the_envelope(
        self, monkeypatch, tmp_path
    ):
        from uuid import uuid4

        from apps.cli.commands.test_cmds import _cmd_test_status

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job_id = str(uuid4())

        code, out, err = _invoke(_cmd_test_status, job_id_str=job_id, as_json=True)

        assert code == 1
        assert err == ""
        body = json.loads(out)
        assert body["schema_version"] == 1
        assert body["ok"] is False
        assert body["error"] == "job_not_found"
        assert body["job_id"] == job_id

    def test_discover_commands_job_store_error_answers_in_the_envelope(
        self, monkeypatch, tmp_path
    ):
        from uuid import uuid4

        import apps.cli.commands.test_cmds as test_cmds_mod
        from packages.orchestration import pingpong_job

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job_id = str(uuid4())

        def _raise(*_args, **_kwargs):
            raise RuntimeError("job store is unreachable")

        monkeypatch.setattr(pingpong_job, "require_job_plan", _raise)

        code, out, err = _invoke(
            test_cmds_mod._cmd_discover_commands, job_id_str=job_id, as_json=True
        )

        assert code == 1
        assert err == ""
        body = json.loads(out)
        assert body["schema_version"] == 1
        assert body["ok"] is False
        assert body["error"] == "job_store_error"
        assert "job store is unreachable" in body["message"]

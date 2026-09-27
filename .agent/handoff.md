# Handoff — F028, round 4

## Session

SESSION 1 of feature F028 · round 4 · rounds so far 4. Context remaining at
handback: comfortable — this round wrote two new production helpers, a new
CLI command module (three commands), a catalog registration, a docs/guide
row set and an allowlist entry, plus roughly 480 lines of tests, with one
self-caught implementation bug (an `emit_ok` keyword collision, fixed and
declared below) and no repair loop otherwise — every gate matched cleanly
and all 10 red-proof mutations were caught on the first run.

## Range

Review of `aa38800a1`..`HEAD` (`HEAD` is this handback's own commit, `F028
R4 C7`, on `feature/f028-task-injection`).

## Commits

### c048626e2 F028 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r4-block.md | 264/0 | copy of this round's block |
| .agent/authored/f028-r4-plan.md | 30/0 | copy of the plan payload |
| .agent/authored/f028-r4-records.diff | 61/0 | copy of the records diff payload |

Measured insertions: 355 (block's own line count 264 + 91), matching the
block's expectation exactly, under the 500-line cap.

### d39fe3de9 F028 R4 C2: book round 3, resolve R-1077, record D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 41/0 | DECISION F028 D4 appended |
| .agent/live_review.md | 4/0 | round 3's Gate entry and R-1077's `Done:` paragraph appended |
| .agent/plan.md | 9/10 | rewrite from the plan payload |

Matches the block's expected numstat (41/0, 4/0, 9/10) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of
`records.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### 58d2fc6f1 F028 R4 C3: mark an unseen confirmation, share the budget and planner inputs, and recompute an extension
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/task_injection.py | 82/2 | S1: `confirm_task_injection` gains `unseen`, stores `confirmed_unseen`; `_validate_confirmed_record` accepts it absent or bool; `apply_injection_to_job`'s injection block always carries it. S2: `injection_budget_inputs` and `injection_call_fn` added, `__all__` updated. S3: `answer_injection_shortfall`'s `extend_budget` branch re-checks the current counters and takes the larger of the recomputed sum and the seed's amount |

82 insertions, under the 500-line cap — no split needed. The block sized
neither C3 nor C4 individually (only C1 and C2), so no expected-insertion
comparison applies here per "WHAT TO REPORT."

### c7797dcc9 F028 R4 C4: add remedy job inject, inject-confirm and inject-answer
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job_inject_cmd.py | 274/0 | S4: the three command handlers, the usage/not-ready exit-code split, `_resolve_after`, the print helpers, `COMMAND_HANDLERS` |
| apps/cli/command_catalog.py | 60/0 | S5: three `CommandEntry` items placed directly after `job.veto-task`, vocabulary-compliant descriptions and arg help |
| apps/cli/commands/__init__.py | 2/1 | S5: `job_inject_cmd` joins the import list (alphabetical, beside `job_context_cmd`/`job_pause_cmd`) and the handler tuple (beside `job_veto_cmd`) |
| docs/guides/exit-codes.md | 3/0 | S5: three rows after `job veto-task`, each `| 3 |` |
| tests/orchestration/import_reachability_allowlist.txt | 1/0 | S5: `apps.cli.commands.job_inject_cmd` between `job_context_cmd` and `job_pause_cmd` |

340 insertions total, under the 500-line cap — no split needed.

### 10e853b8a F028 R4 C5: test the injection commands, the audit mark, the inputs and the amount
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_inject.py | 287/0 | NEW FILE: drafting (human + JSON), `--after` by planned id and by entry id, `--yes` (confirms unseen / refuses a shortfall), `inject-confirm`, `inject-answer` per option, and one exit code per class |
| tests/orchestration/test_task_injection.py | 192/4 | `_confirmed_record` gains `confirmed_unseen`; `TestInjectionBudgetInputs` (6 cases) and `TestInjectionCallFn`; `unseen` stored/defaults-false in `TestConfirmTaskInjection`; the one pinned-dict test corrected to include `confirmed_unseen: False` (declared below); `TestConfirmedRecordFieldValidation` gains 3 confirmed_unseen cases; `TestApplyInjectionToJobConfirmedUnseen` (2 cases); `TestAnswerInjectionShortfall` gains the two S3 recompute cases |

479 insertions total (287 + 192), under the 500-line cap — no split needed.

### 604d26fee F028 R4 C6: add the round 4 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r4-mutations.py | 205/0 | the G5 mutation (red-proof) tool, 10 mutations (m1–m10) across the two touched production files |

### F028 R4 C7: rewrite handoff for round 4 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- No branch creation this round — the block continues on
  `feature/f028-task-injection`, already checked out from round 3.
- `git worktree add --detach .remedy-wt/f028-r4-mut 604d26fee` (at C6, G5's
  own ordered worktree) — succeeded; `git worktree remove --force
  .remedy-wt/f028-r4-mut` and `git worktree prune` afterwards — both
  succeeded. `git worktree list | wc -l` read 64 before the add and 64
  after the remove (step 4's own reading, unchanged).
- `git push` after C7 — reported under G6 in this round's reply (run after
  this file is committed).
- No `gh pr create` (the block does not order one this round), no `gh pr
  merge`, no checkout of `main`, no branch deletion, no force-push, no `git
  stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `plan.md`: 30 lines, 1117 bytes, sha256
  `d0f9fdc2973dd87cf4c30e757eb7b5916db02f459deb776c9bcc0428cc191d49`.
- `records.diff`: 61 lines, 9995 bytes, sha256
  `2d18615311914a367e8ef7eae5e20ddcf75792c73d0071dcbbadf5ae08f9c9ad`.
- Block: 264 lines, sha256
  `c8a91e4d1ec531a5dd27b39f7689552a778837375b0aaa59af57197e2a579bf4` — MATCH
  against both readings the delegation message stated.

Each `.agent/authored/f028-r4-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`c048626e2`), compared byte-for-byte (sha256)
against its source — all three MATCH:
```
.agent/authored/f028-r4-block.md byte-identical: True sha_src=c8a91e4d1ec531a5dd27b39f7689552a778837375b0aaa59af57197e2a579bf4 sha_committed=c8a91e4d1ec531a5dd27b39f7689552a778837375b0aaa59af57197e2a579bf4
.agent/authored/f028-r4-records.diff byte-identical: True sha_src=2d18615311914a367e8ef7eae5e20ddcf75792c73d0071dcbbadf5ae08f9c9ad sha_committed=2d18615311914a367e8ef7eae5e20ddcf75792c73d0071dcbbadf5ae08f9c9ad
.agent/authored/f028-r4-plan.md byte-identical: True sha_src=d0f9fdc2973dd87cf4c30e757eb7b5916db02f459deb776c9bcc0428cc191d49 sha_committed=d0f9fdc2973dd87cf4c30e757eb7b5916db02f459deb776c9bcc0428cc191d49
```

### G2 — THE RECORDS
`git show <sha>:<path>`, bytes and sha256, each read from C2 (`d39fe3de9`),
MATCHING the reviewer's table exactly:
```
.agent/live_review.md bytes=321066 sha256=28649ba056ab1f7c4b3da41d3fda66ac7c066b45ad444c03801b9a528860fafc
.agent/decisions.md   bytes=2263097 sha256=52b1935b5398fcdb838f8be59a142c72c6c02863c2aa5081f66269319329124f
.agent/plan.md        bytes=1117   sha256=d0f9fdc2973dd87cf4c30e757eb7b5916db02f459deb776c9bcc0428cc191d49
```
All three MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text: at `aa38800a1`
reads `['R-1077']`; at C2 (`d39fe3de9`) reads `[]` — MATCH against the
reviewer's stated readings (`['R-1077']` and `[]`). `git diff --name-only
c048626e2 d39fe3de9` names exactly: `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md` — the table's three paths, no
more, no fewer.

### G3 — THE CODE
```
$ bash -c 'python3 -m ruff check packages/orchestration/task_injection.py apps/cli/commands/job_inject_cmd.py apps/cli/command_catalog.py apps/cli/commands/__init__.py tests/cli/test_job_inject.py tests/orchestration/test_task_injection.py; echo "REAL_EXIT=$?"'
All checks passed!
REAL_EXIT=0
```

The three handlers, quoted whole (C6 state, `apps/cli/commands/job_inject_cmd.py`):
```python
def _cmd_inject(job_id_str: str, text: str, *, after: str | None = None, yes: bool = False,
                json_output: bool = False) -> None:
    from packages.orchestration import task_injection as ti
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    resolved_after = _resolve_after(job, after)

    try:
        budgets, counters, config = ti.injection_budget_inputs(job)
    except ti.TaskInjectionRefused as exc:
        code = exc.code
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, exc.detail, json_output=json_output, exit_code=refusal_exit, job_id=job_id)
        return

    call_fn = ti.injection_call_fn()
    answer = ti.draft_task_injection(
        job, text, call_fn=call_fn, budgets=budgets, counters=counters, config=config,
        actor=CLI_ACTOR, after=resolved_after)

    if answer["outcome"] == "refused":
        code = answer["code"]
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, answer["detail"], json_output=json_output, exit_code=refusal_exit,
             job_id=job_id)
        return

    if answer["outcome"] == "shortfall":
        if json_output:
            emit_ok(**answer)
        else:
            _print_shortfall(job_id, answer)
        if yes:
            fail("draft_needs_decision",
                 "a shortfall draft needs its decision answered before it can be confirmed",
                 json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job_id)
        return

    # outcome == "drafted"
    if yes:
        confirmation = ti.confirm_task_injection(
            job, answer["confirm_token"], actor=CLI_ACTOR, unseen=True)
        if confirmation["outcome"] == "refused":
            code = confirmation["code"]
            refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
                EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
            fail(code, confirmation["detail"], json_output=json_output,
                 exit_code=refusal_exit, job_id=job_id)
            return
        if json_output:
            emit_ok(job_id=job_id, draft=answer, confirmation=confirmation)
            return
        _print_confirmation(job_id, confirmation)
        return

    if json_output:
        emit_ok(**answer)
        return
    _print_draft(job_id, answer)


def _cmd_inject_confirm(job_id_str: str, token: str, *, json_output: bool = False) -> None:
    from packages.orchestration import task_injection as ti
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    result = ti.confirm_task_injection(job, token, actor=CLI_ACTOR)

    if result["outcome"] == "refused":
        code = result["code"]
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, result["detail"], json_output=json_output, exit_code=refusal_exit,
             job_id=job_id)
        return

    if json_output:
        emit_ok(**result)
        return
    _print_confirmation(job_id, result)


def _cmd_inject_answer(job_id_str: str, draft_id: str, *, option: str = "",
                       json_output: bool = False) -> None:
    from packages.orchestration import task_injection as ti
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    try:
        budgets, counters, config = ti.injection_budget_inputs(job)
    except ti.TaskInjectionRefused as exc:
        code = exc.code
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, exc.detail, json_output=json_output, exit_code=refusal_exit, job_id=job_id)
        return

    answer = ti.answer_injection_shortfall(
        job, draft_id, option, actor=CLI_ACTOR, budgets=budgets, counters=counters,
        config=config)

    if answer["outcome"] == "refused":
        code = answer["code"]
        refusal_exit = EXIT_USAGE if code in _USAGE_CODES else (
            EXIT_NOT_READY if code in _NOT_READY_CODES else 1)
        fail(code, answer["detail"], json_output=json_output, exit_code=refusal_exit,
             job_id=job_id)
        return

    if answer["outcome"] == "dropped":
        if json_output:
            emit_ok(**answer)
            return
        print(f"Injection draft {draft_id} dropped for job {job_id}; nothing added.")
        return

    if answer["outcome"] == "shortfall":
        if json_output:
            emit_ok(**answer)
        else:
            _print_shortfall(job_id, answer)
        return

    # outcome == "drafted" — a derived draft, prints as `job inject` prints a draft.
    if json_output:
        emit_ok(**answer)
        return
    _print_draft(job_id, answer)
```

`injection_budget_inputs`, quoted whole (C6 state,
`packages/orchestration/task_injection.py`):
```python
def injection_budget_inputs(job: Any) -> tuple[Any, Any, Any]:
    """``(budgets, counters, config)`` for a job about to draft or answer an injection.

    ``budgets`` is None when ``job.budgets`` is None, else ``JobBudgets.model_validate(
    job.budgets)``; ``counters`` is ``BudgetCounters()`` when ``job.budget_actuals`` is
    None, else decoded and built from it; ``config`` is the repo's predictive budget
    config. A pydantic ``ValidationError``, a ``budget_guard.BudgetCounterError``, a
    ``ValueError`` or a ``TypeError`` raised while reading the budgets or the counters
    raises ``TaskInjectionRefused("budget_unreadable", ...)`` instead — a job whose stored
    state cannot be trusted must never be read as a job that has spent nothing.
    """
    from packages.core.models import JobBudgets
    from packages.orchestration.budget_resolution import resolve_predictive_budget_config

    try:
        budgets = None if job.budgets is None else JobBudgets.model_validate(job.budgets)
        if job.budget_actuals is None:
            counters = budget_guard.BudgetCounters()
        else:
            validated = budget_guard.decode_persisted_budget_actuals(
                job.budget_actuals, first_running_at=job.first_running_at or None)
            counters = budget_guard.counters_from_persisted(validated)
    except (ValidationError, budget_guard.BudgetCounterError, ValueError, TypeError) as exc:
        raise TaskInjectionRefused(
            "budget_unreadable", f"this job's budget state cannot be read: {exc}") from exc

    config = resolve_predictive_budget_config(project_root=job.repo_path or None)
    return budgets, counters, config
```

### G4 — THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/cli/test_job_inject.py tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/cli/test_job_veto.py tests/cli/test_cli_ux.py tests/test_command_catalog.py tests/test_grouped_cli.py tests/test_help_renderer.py tests/orchestration/test_dead_command_check.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1605 passed, 7 skipped in 110.27s (0:01:50)
REAL_EXIT=0
```
The reviewer's own baseline (same selection LESS `tests/cli/test_job_inject.py`,
at `aa38800a1`) read `1563 passed, 7 skipped` at exit 0. `--collect-only -q`
node counts of the two edited test files:
```
                          aa38800a1   C6 (604d26fee)
test_task_injection.py       116          136
test_job_inject.py             0           16
```
Delta from the two edited files: (136-116) + (16-0) = 20 + 16 = 36. The
remaining (1605-1563) - 36 = 6 comes from `tests/cli/test_exit_codes.py`,
whose two tests are parametrized one node per catalog command (measured:
323 nodes at the old catalog, 329 at the current one, via a temporary
swap-in of the old `apps/cli/command_catalog.py` bytes, collect-only, then
restore — confirmed byte-identical to `HEAD` afterwards) — the three new
commands each add one node to each of the two parametrized tests (3×2=6).
Every other file in the selection (`test_command_catalog.py`,
`test_advertised_commands.py`, `test_cli_ux.py`, `test_grouped_cli.py`,
`test_help_renderer.py`) collected the SAME node count before and after.
36 + 6 = 42 = 1605 - 1563 exactly — no unexplained difference. The seven
skips are the same F252 quarantines (6 in `test_named_bugs.py`, 1 in
`test_agent_tooling.py`), unchanged.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=164"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0.

### G5 — THE RED PROOFS
`git worktree add --detach .remedy-wt/f028-r4-mut 604d26fee` (C6) then
`python3 -B .agent/authored/f028-r4-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r4-mut`, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1_text_invalid_leaves_the_usage_class (apps/cli/commands/job_inject_cmd.py): exit=1 failed=1 nodes=['tests/cli/test_job_inject.py::TestInjectExitCodes::test_text_invalid_exits_2']
m2_draft_unknown_leaves_the_not_ready_class (apps/cli/commands/job_inject_cmd.py): exit=1 failed=2 nodes=['tests/cli/test_job_inject.py::TestInjectConfirm::test_an_unknown_token_answers_draft_unknown_exit_3', 'tests/cli/test_job_inject.py::TestInjectExitCodes::test_draft_unknown_exits_3']
m3_yes_over_a_shortfall_exits_0 (apps/cli/commands/job_inject_cmd.py): exit=1 failed=1 nodes=['tests/cli/test_job_inject.py::TestInjectYes::test_yes_over_a_shortfall_exits_3_with_the_seed_printed_and_nothing_confirmed']
m4_yes_confirms_with_unseen_false (apps/cli/commands/job_inject_cmd.py): exit=1 failed=1 nodes=['tests/cli/test_job_inject.py::TestInjectYes::test_yes_confirms_at_once_with_confirmed_unseen_true']
m5_after_passes_the_entrys_own_id_instead_of_its_planned_id (apps/cli/commands/job_inject_cmd.py): exit=1 failed=1 nodes=['tests/cli/test_job_inject.py::TestInjectDraft::test_after_by_planned_id_and_by_entry_id_give_the_same_depends_on']
m6_the_drafted_output_omits_the_confirm_line (apps/cli/commands/job_inject_cmd.py): exit=1 failed=1 nodes=['tests/cli/test_job_inject.py::TestInjectDraft::test_human_output_holds_the_confirm_line_with_its_token']
m7_the_confirmation_stores_confirmed_unseen_false_always (packages/orchestration/task_injection.py): exit=1 failed=2 nodes=['tests/cli/test_job_inject.py::TestInjectYes::test_yes_confirms_at_once_with_confirmed_unseen_true', 'tests/orchestration/test_task_injection.py::TestConfirmTaskInjection::test_unseen_true_is_stored_on_disk']
m8_the_injection_block_omits_confirmed_unseen (packages/orchestration/task_injection.py): exit=1 failed=3 nodes=['tests/orchestration/test_task_injection.py::TestApplyInjectionToJob::test_appends_provenance_bumps_version_and_reseals_an_approved_hash', 'tests/orchestration/test_task_injection.py::TestApplyInjectionToJobConfirmedUnseen::test_unseen_true_is_logged_in_the_injection_block', 'tests/orchestration/test_task_injection.py::TestApplyInjectionToJobConfirmedUnseen::test_absent_confirmed_unseen_logs_false']
m9_extend_budget_takes_the_seeds_amount_alone (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestAnswerInjectionShortfall::test_extend_budget_recomputes_the_larger_amount_when_spend_grew']
m10_injection_budget_inputs_answers_budgetcounters_for_undecodable_actuals (packages/orchestration/task_injection.py): exit=1 failed=2 nodes=['tests/orchestration/test_task_injection.py::TestInjectionBudgetInputs::test_undecodable_actuals_refuse_budget_unreadable', 'tests/orchestration/test_task_injection.py::TestInjectionBudgetInputs::test_unreadable_budgets_refuse_budget_unreadable']
restored byte-identical: True (apps/cli/commands/job_inject_cmd.py)
restored byte-identical: True (packages/orchestration/task_injection.py)
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 10 mutations red with at least one failing node each; no mutation
stayed green, so no fix-up test was needed. `git worktree remove --force
.remedy-wt/f028-r4-mut` then `git worktree prune`, both exit 0; `git
worktree list | wc -l` read 64 afterwards, matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r4-block.md`, at `c048626e2`) vs
  `.remedy-wt/f028-r4/block.md`: byte-identical, sha256
  `c8a91e4d1ec531a5dd27b39f7689552a778837375b0aaa59af57197e2a579bf4` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r4-plan.md`, at `c048626e2`) vs
  `.remedy-wt/f028-r4-payloads/plan.md`: byte-identical, sha256
  `d0f9fdc2973dd87cf4c30e757eb7b5916db02f459deb776c9bcc0428cc191d49` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `records.diff` copy (`.agent/authored/f028-r4-records.diff`, at
  `c048626e2`) vs `.remedy-wt/f028-r4-payloads/records.diff`:
  byte-identical, sha256
  `2d18615311914a367e8ef7eae5e20ddcf75792c73d0071dcbbadf5ae08f9c9ad` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production code (`task_injection.py`, `job_inject_cmd.py`,
`command_catalog.py`, `commands/__init__.py`), its tests (two files) and
the mutation tool (`f028-r4-mutations.py`) are the WORKER's own authored
code against the block's specification S1–S5, not reviewer-authored text,
so no fidelity comparison applies to them.

## Deviations & assumptions

1. **`emit_ok` call shape (job_inject_cmd.py), corrected before C4's
   commit.** S4 reads: "With `--json` each emits `emit_ok(job_id=job_id,
   **answer)`". Every one of `draft_task_injection`'s, `confirm_task_injection`'s
   and `answer_injection_shortfall`'s return dicts ALREADY carries its own
   `"job_id"` key (e.g. `draft_task_injection`'s `answer["job_id"] =
   job.job_id`, set in S1/S2's own code, unchanged by this round). Calling
   `emit_ok(job_id=job_id, **answer)` literally therefore raises
   `TypeError: emit_ok() got multiple values for keyword argument
   'job_id'` — caught immediately by this round's own new tests (`git
   diff` self-review loop, before any commit). Fixed by dropping the
   redundant `job_id=` kwarg wherever the unpacked dict already carries
   the same key (`emit_ok(**answer)`, `emit_ok(**result)`); the envelope's
   `job_id` value is identical either way, since it is the same resolved
   id in both places. The `--yes` "drafted" branch's `emit_ok(job_id=job_id,
   draft=answer, confirmation=confirmation)` is UNCHANGED from the block's
   literal text — there `answer` and `confirmation` are nested under their
   own keys rather than unpacked, so no collision exists there.
2. **One pre-existing test's pinned dict corrected (`test_task_injection.py`,
   `TestApplyInjectionToJob::test_appends_provenance_bumps_version_and_reseals_an_approved_hash`,
   not written this round).** S1 states the injection block "always"
   carries `confirmed_unseen` (`record.get("confirmed_unseen", False)`) —
   unconditional, unlike `budget_extend_to_usd`'s round-3 "only when the
   record carries that key" gating. This test asserts the WHOLE
   `entry["injection"]` dict via `==` against a literal 8-key mapping (the
   9th key, `budget_extend_to_usd`, is absent because `_confirmed_record()`
   omits it by default, which is why that field was made conditional in
   round 3 in the first place — see round 3's own Deviations §1). Adding
   the new unconditional key necessarily changes what `apply_injection_to_job`
   writes for EVERY confirmed record, including one built by the
   round-3-era `_confirmed_record()` helper that carries no `confirmed_unseen`
   key at all (so `.get(..., False)` reads `False`). Per AGENTS.md's commit
   gate, this is not "an existing test going red as an unrelated
   regression" (the rule that governs walking away and reporting) — it is
   the DIRECT, SPECIFIED, unconditional consequence of S1's own field
   addition to a dict this one test happens to pin by exact equality. The
   fix adds exactly one line, `"confirmed_unseen": False,`, with a comment
   naming DECISION F028 D4 (2) and explaining why it reads the default;
   no other assertion in that test, and no other test in the file, needed
   any change (confirmed by `TestApplyInjectionToJobBudgetExtension`'s four
   cases and the `"budget_extend_to_usd" not in entry["injection"]`
   assertion staying green unedited).
3. **Assumption: the `--yes`-over-a-shortfall sequencing.** S4 says "a
   shortfall is refused as `draft_needs_decision` with exit 3 after the
   seed is printed" without stating whether the seed's normal
   emit/print happens identically whether or not `--yes` was given. This
   round reads it as: the shortfall response (JSON envelope or the human
   seed print) is always produced first, exactly as it would be without
   `--yes`, and ONLY THEN, if `--yes` was given, `fail("draft_needs_decision",
   ..., exit_code=3)` runs afterward. Confirmed by
   `test_yes_over_a_shortfall_exits_3_with_the_seed_printed_and_nothing_confirmed`,
   which checks the seed's text is in the output, the exit code is 3, and
   `confirmed_injections` is empty.
4. **Assumption: exact print formats for a drafted task, a shortfall and a
   confirmation.** S4 names WHICH fields print (id, title, goal, every
   acceptance line, band, placement rationale, budget arithmetic, every
   fence flag, expiry, then the exact confirm line; the seed's question and
   arithmetic then per-option label and the exact answer-command line) but
   not the exact surrounding prose for each line (e.g. `"  goal: {goal}"`
   vs some other label). The two EXACT lines S4 quotes verbatim
   (`f"Confirm it with: remedy job inject-confirm {job_id} {token}"` and
   `f"  remedy job inject-answer {job_id} {draft_id} --option {option}"`)
   are reproduced byte-for-byte; every other printed line's wording is
   this round's own reasonable choice, consistent with `job_veto_cmd.py`'s
   own style.
5. Test-file/payload line/byte/sha256 measurements and the temporary
   old-catalog swap used to account for G4's node-count delta were done
   with small Python helper scripts (`python3 - <<'PY' ... PY`) rather than
   shell pipelines the sandbox denies (`wc`, command substitution,
   multi-operation one-liners) — per the block's own "THIS SANDBOX
   REFUSES SHAPES" section, which names exactly this workaround. The
   temporary catalog swap restored `apps/cli/command_catalog.py` from
   `git show HEAD:...` and was confirmed byte-identical to `HEAD` via
   `git diff --stat` reading empty before any commit touched it.

No test went red unexpectedly (the one edited pre-existing test is
declared in §2 above as a spec-mandated shape change, not an unrelated
regression), no reviewer payload was edited or retyped, no gate was
skipped, and every G5 mutation was caught on the first run — no fix-up
test was required.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | both test files fit in one commit under the 500-line cap (287+192=479); no split needed |
| C6 | done | |
| C7 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | 1605 passed, 7 skipped, exit 0; the 42-node delta from the reviewer's 1563 baseline fully accounted for (36 from the two edited test files, 6 from `test_exit_codes.py`'s per-command parametrization) |
| G5 | done | all 10 mutations caught, both controls clean, both files restored byte-identical |
| G6 | deviated | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |
| S1 | done | `unseen` keyword, `confirmed_unseen` storage/validation/logging |
| S2 | done | `injection_budget_inputs`, `injection_call_fn` |
| S3 | done | `extend_budget`'s re-check and larger-of-two amount |
| S4 | done | `job_inject_cmd.py`, its three handlers and exit-code classes |
| S5 | done | catalog registration, `__init__.py`, exit-codes.md, reachability allowlist — vocabulary-page compliant on the first run |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 4,
then the browser's command for the three steps, the run-log event of a
folded injection with every reader of its name, and the send module. Open
findings (by `open_finding_ids` at this round's head): 0. Operator
questions open: 0.
